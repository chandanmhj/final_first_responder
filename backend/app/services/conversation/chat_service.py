"""Orchestrates one chat turn: safety, routing, scenarios, questions, photos, hospitals and reports."""
from dataclasses import dataclass

from ...config import Settings
from ..handover.isbar_report import build_report, to_markdown
from ..handover.timeline import now_iso
from ..rag import citations
from ..rag.generation import GroqClient
from ..rag.pipeline import RagPipeline
from ..safety import disclaimers, emergency_triage, guardrails
from ..scenarios import scenario_router
from ..scenarios.composer import compose, valid_location
from ..scenarios.loader import ScenarioStore
from ..vision import animal_identification, image_understanding
from . import quick_replies, smalltalk
from .roles import adjust_condition, band_protocol, infer_age_band
from .step_manager import ScenarioState

INTRO_URGENT = "Call 108 now (or ask someone to). I'll guide you step by step while help is on the way."


@dataclass
class ChatRequest:
    """One user turn."""

    message: str = ""
    session_id: str | None = None
    action: str = "message"  # message | next | not_worked | hospitals | report | restart
    role: str | None = None
    for_self: bool | None = None
    age_band: str | None = None
    lat: float | None = None
    lon: float | None = None


class ChatService:
    """Holds the services a chat turn needs."""

    def __init__(self, settings: Settings, store: ScenarioStore, repo, llm: GroqClient, rag: RagPipeline, hospitals, media):
        self.s, self.store, self.repo, self.llm, self.rag, self.hospitals, self.media = settings, store, repo, llm, rag, hospitals, media

    # ------------------------------------------------------------------ helpers
    def _step_msg(self, state: ScenarioState) -> dict:
        step = state.current()
        is_last = state.index + 1 >= len(state.steps)
        return {
            "type": "step",
            "step": {
                **{k: step[k] for k in ("id", "index", "total", "text", "source", "page", "authored")},
                "source_label": citations.label(step["source"], step["page"]),
                "unreviewed_note": disclaimers.UNREVIEWED if step["authored"] else None,
                "media": self.media.resolve(step["id"]),
                "next_media": self.media.resolve(state.steps[state.index + 1]["id"]) if not is_last else None,
            },
            "quick_replies": quick_replies.for_step(step, is_last),
        }

    def _event(self, user_id, state, event_type, payload=None):
        if state.incident_id:
            self.repo.add_event(user_id, state.incident_id, event_type, payload)

    def _scenario_info(self, state: ScenarioState) -> dict | None:
        if not state.condition:
            return None
        return {"condition": state.condition, "title": self.store.conditions[state.condition].title, "location": state.location,
                "index": state.index, "total": len(state.steps), "status": state.status}

    def _start(self, user_id, session, state: ScenarioState, condition: str, location: str | None, role: str, for_self: bool,
               age_band: str | None, protocol: str, intro: str | None, urgent: bool, req: ChatRequest) -> list[dict]:
        cond_id = adjust_condition(condition, protocol)
        loc = valid_location(self.store, cond_id, location)
        steps = compose(self.store, cond_id, loc, role, for_self, self.s.show_authored_steps)
        if not steps:
            return [{"type": "text", "text": "I don't have steps for that yet. Please call 108 or see a doctor."}]
        cond = self.store.conditions[cond_id]
        incident = self.repo.create_incident(user_id, {
            "session_id": session["id"], "condition": cond_id, "location": loc, "role": role, "for_self": for_self,
            "age_band": age_band, "scenario_id": f"{cond_id}__{loc}",
        })
        state.status, state.condition, state.location = "active", cond_id, loc
        state.role, state.for_self, state.age_band, state.protocol = role, for_self, age_band, protocol
        state.incident_id, state.index = incident["id"], 0
        state.steps = [s.to_dict() for s in steps]
        state.lat, state.lon = req.lat, req.lon
        self._event(user_id, state, "scenario_started", {"title": cond.title, "text": cond.title})
        self._event(user_id, state, "step_shown", {"step_id": steps[0].id, "step_text": steps[0].text})
        head = intro or f"I'll guide you through: {cond.title}."
        if urgent:
            head = f"{INTRO_URGENT}\n\n{head}"
        msgs = [{"type": "text", "text": head}]
        if cond.note:
            msgs[0]["text"] += f"\n\nNote: {cond.note}"
        return msgs + [self._step_msg(state)]

    # ------------------------------------------------------------------ actions
    def _next(self, user_id, state: ScenarioState) -> list[dict]:
        if not state.active:
            return [{"type": "text", "text": "There is no active emergency. Tell me what is happening and I'll guide you."}]
        cur = state.current()
        self._event(user_id, state, "step_done", {"step_id": cur["id"], "step_text": cur["text"]})
        nxt = state.advance()
        if nxt:
            self._event(user_id, state, "step_shown", {"step_id": nxt["id"], "step_text": nxt["text"]})
            return [self._step_msg(state)]
        self._event(user_id, state, "scenario_completed", {})
        need = self.store.conditions[state.condition].facility_requirements
        if state.incident_id:
            self.repo.update_incident(user_id, state.incident_id, {"status": "completed", "ended_at": now_iso()})
        return [{"type": "text", "text": f"That's all the steps. Keep watching the person until help arrives.\n\nBest place to go: {need}\n\n{disclaimers.CALL_108}",
                 "quick_replies": quick_replies.after_completion()}]

    def _not_worked(self, user_id, state: ScenarioState) -> list[dict]:
        cur = state.current()
        if not cur:
            return [{"type": "text", "text": "Tell me what is happening and I'll guide you."}]
        self._event(user_id, state, "step_not_worked", {"step_id": cur["id"], "step_text": cur["text"]})
        hint = (cur.get("not_worked") or {}).get("hint")
        style = "clinical" if state.role == "responder" else "simple"
        ans = self.rag.answer(f"This step did not work: {cur['text']} What should I do now?", condition=state.condition,
                              condition_title=self.store.conditions[state.condition].title, step_text=cur["text"], style=style)
        text = hint or ans.text
        if hint and not ans.abstained:
            text = f"{hint}\n\n{ans.text}"
        is_last = state.index + 1 >= len(state.steps)
        return [{"type": "text", "text": text, "citations": ans.citations, "quick_replies": quick_replies.for_step(cur, is_last)}]

    def _hospitals(self, user_id, state: ScenarioState, req: ChatRequest) -> list[dict]:
        lat, lon = req.lat or state.lat, req.lon or state.lon
        if lat is None or lon is None:
            return [{"type": "needs_location", "text": "Please allow location access so I can find hospitals near you. If you can't, call 108."}]
        out = self.hospitals.nearby(lat, lon, state.condition)
        self._event(user_id, state, "hospital_viewed", {"text": f"{len(out['results'])} hospitals"})
        return [{"type": "hospitals", "hospitals": out["results"], "text": out["message"] or "Nearest suitable hospitals:",
                 "need": self.store.conditions[state.condition].facility_requirements if state.condition else None}]

    def _report(self, user_id, state: ScenarioState) -> list[dict]:
        if not state.incident_id:
            return [{"type": "text", "text": "There is no emergency to report yet."}]
        rep = self.build_handover(user_id, state.incident_id)
        return [{"type": "report", "incident_id": state.incident_id, "text": "Your handover report is ready.", "report": rep["report"]}]

    def build_handover(self, user_id: str, incident_id: str) -> dict:
        """Create the ISBAR report for an incident (also saved)."""
        inc = self.repo.get_incident(user_id, incident_id)
        events = self.repo.list_events(user_id, incident_id)
        cond = self.store.conditions.get(inc["condition"]) if inc else None
        report = build_report(inc, events, cond.title if cond else None, cond.facility_requirements if cond else None)
        self.repo.save_report(user_id, incident_id, report)
        return {"report": report, "markdown": to_markdown(report)}

    # ------------------------------------------------------------------ free text and photos
    def _answer_question(self, text: str, state: ScenarioState, history) -> list[dict]:
        cur = state.current()
        style = "clinical" if state.role == "responder" else "simple"
        cond = self.store.conditions.get(state.condition) if state.condition else None
        ans = self.rag.answer(text, condition=state.condition, condition_title=cond.title if cond else None,
                              step_text=cur["text"] if cur else None, style=style, history=history)
        msg = {"type": "text", "text": ans.text, "citations": ans.citations}
        if cur:
            msg["quick_replies"] = quick_replies.for_step(cur, state.index + 1 >= len(state.steps))
        return [msg]

    def _handle_image(self, user_id, session, state, req, role, image, text, age_band, protocol, for_self) -> list[dict]:
        data, mime = image
        self.repo.save_upload(user_id, data, mime)
        res = animal_identification.identify(self.llm, data, mime, text, self.s.data_dir)
        msgs: list[dict] = []
        if res.is_animal and res.category != "none":
            msgs.append({"type": "animal", "result": res.to_dict(), "text": res.headline})
            if state.incident_id:
                self._event(user_id, state, "photo_analyzed", {"headline": res.headline})
            if res.condition and not (state.active and state.condition == res.condition):
                started = self._start(user_id, session, state, res.condition, "outdoors", role, for_self, age_band, protocol,
                                      "I'll guide you through the first aid now.", True, req)
                if state.incident_id:
                    self._event(user_id, state, "photo_analyzed", {"headline": res.headline})
                msgs += started
            return msgs
        desc = image_understanding.describe(self.llm, data, mime, text)
        route = scenario_router.rule_based_match(f"{text} {desc}", self.store)
        if route.kind == "emergency":
            return [{"type": "text", "text": f"From the photo: {desc}"}] + self._start(
                user_id, session, state, route.condition, route.location, role, for_self, age_band, protocol, None,
                emergency_triage.is_urgent(text), req)
        return [{"type": "text", "text": (desc + "\n\n" if desc else "") + "Tell me what happened and who is hurt, so I can guide you."}]

    # ------------------------------------------------------------------ entry point
    def handle(self, user_id: str, req: ChatRequest, image: tuple[bytes, str] | None = None) -> dict:
        """Process one turn and return the messages to show."""
        profile = self.repo.get_profile(user_id) or {}
        role = profile.get("role") or req.role or "common"
        if role not in ("common", "responder"):
            role = "common"
        session = self.repo.get_session(user_id, req.session_id) if req.session_id else None
        if not session:
            session = self.repo.create_session(user_id)
        state = ScenarioState.from_dict(session.get("state"))
        text = (req.message or "").strip()
        history = [{"role": m["role"], "content": (m["content"] or {}).get("text", "")} for m in self.repo.list_messages(user_id, session["id"])[-6:]
                   if (m["content"] or {}).get("text")]
        if text or image:
            self.repo.add_message(user_id, session["id"], "user", {"text": text, "has_image": bool(image)})
        for_self = bool(req.for_self) if req.for_self is not None else state.for_self
        age_band = req.age_band or infer_age_band(text) or state.age_band
        protocol = band_protocol(self.store, age_band)
        urgent = emergency_triage.is_urgent(text)
        msgs: list[dict]

        if req.action == "next":
            msgs = self._next(user_id, state)
        elif req.action == "not_worked":
            msgs = self._not_worked(user_id, state)
        elif req.action == "hospitals":
            msgs = self._hospitals(user_id, state, req)
        elif req.action == "report":
            msgs = self._report(user_id, state)
        elif req.action == "restart":
            state = ScenarioState()
            msgs = [{"type": "text", "text": "Okay. Tell me what is happening and I'll guide you."}]
        elif guardrails.is_crisis(text):
            msgs = [{"type": "text", "text": guardrails.CRISIS_REPLY, "crisis": True}]
        elif image:
            msgs = self._handle_image(user_id, session, state, req, role, image, text, age_band, protocol, for_self)
        else:
            route = scenario_router.classify(text, self.store, self.llm, state.active)
            if route.kind == "emergency" and not (state.active and route.condition == state.condition):
                msgs = self._start(user_id, session, state, route.condition, route.location, role, for_self, age_band, protocol, None, urgent, req)
            elif route.kind == "smalltalk":
                msgs = [{"type": "text", "text": smalltalk.reply(self.llm, text, history)}]
            elif route.kind in ("question", "emergency") or state.active:
                msgs = self._answer_question(text, state, history)
            else:
                msgs = [{"type": "text", "text": route.clarify or "I want to help. Can you tell me what happened, and who needs help? For example: \"my father has chest pain\"."}]

        for m in msgs:
            if m.get("type") == "text" and "citations" not in m:
                m["citations"] = []
        title = session.get("title") or "New conversation"
        patch = {"state": state.to_dict()}
        if title == "New conversation" and text:
            patch["title"] = (self.store.conditions[state.condition].title if state.condition else text)[:60]
        self.repo.update_session(user_id, session["id"], patch)
        self.repo.add_message(user_id, session["id"], "assistant", {"messages": msgs, "text": " ".join(m.get("text", "") for m in msgs if m.get("text"))[:2000]})
        return {"session_id": session["id"], "incident_id": state.incident_id, "urgent": urgent or state.active and state.condition in
                {"cardiac_arrest_adult", "cardiac_arrest_child_infant"}, "scenario": self._scenario_info(state), "messages": msgs}
