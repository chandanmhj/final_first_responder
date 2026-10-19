import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError, getCoords } from "../lib/api";
import type { ChatItem, ChatResponse, QuickReply, ScenarioInfo, ServerMessage } from "../types/chat";

let counter = 0;
const nid = () => `i${Date.now()}_${counter++}`;

type Opts = { forSelf?: boolean; ageBand?: string; image?: File | null };

function toItems(res: { messages: ServerMessage[] }): ChatItem[] {
  return res.messages.map((m) => ({ id: nid(), from: "assistant" as const, message: m }));
}

/** Conversation state: loads history, sends messages and quick-reply actions, and keeps the scenario progress. */
export function useChat(initialSessionId: string | null) {
  const [sessionId, setSessionId] = useState<string | null>(initialSessionId);
  const [items, setItems] = useState<ChatItem[]>([]);
  const [scenario, setScenario] = useState<ScenarioInfo | null>(null);
  const [incidentId, setIncidentId] = useState<string | null>(null);
  const [urgent, setUrgent] = useState(false);
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(!!initialSessionId);
  const [error, setError] = useState<string | null>(null);
  const coords = useRef<{ lat: number; lon: number } | null>(null);
  const sessionRef = useRef<string | null>(initialSessionId);
  const countRef = useRef(0);

  useEffect(() => {
    countRef.current = items.length;
  }, [items]);

  useEffect(() => {
    sessionRef.current = sessionId;
  }, [sessionId]);

  useEffect(() => {
    if (!initialSessionId) return;
    if (sessionRef.current === initialSessionId && countRef.current > 0) return; // already showing this conversation
    let alive = true;
    api
      .getMessages(initialSessionId)
      .then((r) => {
        if (!alive) return;
        const out: ChatItem[] = [];
        for (const m of r.messages) {
          if (m.role === "user") {
            out.push({ id: m.id, from: "user", message: { type: "user", text: String(m.content.text ?? ""), hasImage: !!m.content.has_image } });
          } else {
            for (const sm of (m.content.messages as ServerMessage[] | undefined) ?? []) out.push({ id: nid(), from: "assistant", message: sm });
          }
        }
        setItems(out);
        const st = r.session.state as { condition?: string; status?: ScenarioInfo["status"]; index?: number; steps?: unknown[]; location?: string; incident_id?: string };
        if (st.condition) {
          setScenario({ condition: st.condition, title: r.session.title, location: st.location ?? null, index: st.index ?? 0, total: st.steps?.length ?? 0, status: st.status ?? "idle" });
        }
        setIncidentId(st.incident_id ?? null);
      })
      .catch((e: unknown) => alive && setError(e instanceof Error ? e.message : "Could not load this conversation."))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [initialSessionId]);

  const run = useCallback(
    async (fields: Record<string, string | undefined>, userBubble: ChatItem | null, image?: File | null): Promise<ChatResponse | null> => {
      setSending(true);
      setError(null);
      if (userBubble) setItems((prev) => [...prev, userBubble]);
      const form = new FormData();
      for (const [k, v] of Object.entries(fields)) if (v !== undefined && v !== "") form.append(k, v);
      if (sessionRef.current) form.append("session_id", sessionRef.current);
      if (coords.current) {
        form.append("lat", String(coords.current.lat));
        form.append("lon", String(coords.current.lon));
      }
      if (image) form.append("image", image);
      try {
        const res = await api.chat(form);
        setSessionId(res.session_id);
        sessionRef.current = res.session_id;
        setScenario(res.scenario);
        setIncidentId(res.incident_id);
        setUrgent(res.urgent);
        setItems((prev) => [...prev, ...toItems(res)]);
        return res;
      } catch (e) {
        setError(e instanceof ApiError ? e.message : "Something went wrong.");
        return null;
      } finally {
        setSending(false);
      }
    },
    [],
  );

  const send = useCallback(
    (text: string, opts: Opts = {}) => {
      const clean = text.trim();
      if (!clean && !opts.image) return Promise.resolve(null);
      const bubble: ChatItem = {
        id: nid(),
        from: "user",
        message: { type: "user", text: clean, hasImage: !!opts.image, imageUrl: opts.image ? URL.createObjectURL(opts.image) : undefined },
      };
      return run({ message: clean, action: "message", for_self: opts.forSelf === undefined ? undefined : String(opts.forSelf), age_band: opts.ageBand }, bubble, opts.image);
    },
    [run],
  );

  const act = useCallback(
    async (action: QuickReply["action"]) => {
      if (action === "hospitals" && !coords.current) coords.current = await getCoords();
      return run({ action }, null);
    },
    [run],
  );

  return { sessionId, items, scenario, incidentId, urgent, sending, loading, error, send, act };
}

/** Plain text read aloud in hands-free mode for a set of server messages. */
export function spokenText(messages: ServerMessage[]): string {
  const parts: string[] = [];
  for (const m of messages) {
    if (m.type === "text" || m.type === "needs_location" || m.type === "report") parts.push(m.text);
    else if (m.type === "step") parts.push(`Step ${m.step.index + 1} of ${m.step.total}. ${m.step.text} Say next when you are done, or say it didn't work.`);
    else if (m.type === "animal") parts.push([m.result.headline, ...m.result.advice].join(" "));
    else if (m.type === "hospitals") {
      const h = m.hospitals[0];
      parts.push(h ? `The best match is ${h.name}, about ${h.distance_km} kilometres away.` : m.text);
    }
  }
  return parts.join(" ").replace(/\s+/g, " ").trim();
}
