"""Data access. One interface, two implementations: in memory (tests, local dev) and Supabase (production)."""
import uuid
from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class MemoryRepository:
    """Keeps everything in Python dicts. Not persistent."""

    def __init__(self):
        self.profiles, self.sessions, self.messages, self.incidents, self.events, self.reports, self.uploads = {}, {}, {}, {}, {}, {}, {}

    # profiles
    def get_profile(self, user_id):
        return self.profiles.get(user_id)

    def upsert_profile(self, user_id, patch):
        p = {**self.profiles.get(user_id, {"id": user_id}), **patch, "updated_at": _now()}
        self.profiles[user_id] = p
        return p

    # sessions
    def create_session(self, user_id, title="New conversation"):
        s = {"id": str(uuid.uuid4()), "user_id": user_id, "title": title, "state": {}, "created_at": _now(), "updated_at": _now()}
        self.sessions[s["id"]] = s
        self.messages[s["id"]] = []
        return s

    def list_sessions(self, user_id):
        return sorted((s for s in self.sessions.values() if s["user_id"] == user_id), key=lambda s: s["updated_at"], reverse=True)

    def get_session(self, user_id, sid):
        s = self.sessions.get(sid)
        return s if s and s["user_id"] == user_id else None

    def update_session(self, user_id, sid, patch):
        s = self.get_session(user_id, sid)
        if s:
            s.update(patch)
            s["updated_at"] = _now()
        return s

    def delete_session(self, user_id, sid):
        if self.get_session(user_id, sid):
            self.sessions.pop(sid, None)
            self.messages.pop(sid, None)
            return True
        return False

    # messages
    def add_message(self, user_id, sid, role, content):
        m = {"id": str(uuid.uuid4()), "session_id": sid, "user_id": user_id, "role": role, "content": content, "created_at": _now()}
        self.messages.setdefault(sid, []).append(m)
        return m

    def list_messages(self, user_id, sid):
        return [m for m in self.messages.get(sid, []) if m["user_id"] == user_id]

    # incidents and events
    def create_incident(self, user_id, data):
        i = {"id": str(uuid.uuid4()), "user_id": user_id, "started_at": _now(), "status": "active", **data}
        self.incidents[i["id"]] = i
        self.events[i["id"]] = []
        return i

    def get_incident(self, user_id, iid):
        i = self.incidents.get(iid)
        return i if i and i["user_id"] == user_id else None

    def update_incident(self, user_id, iid, patch):
        i = self.get_incident(user_id, iid)
        if i:
            i.update(patch)
        return i

    def list_incidents(self, user_id):
        return sorted((i for i in self.incidents.values() if i["user_id"] == user_id), key=lambda i: i["started_at"], reverse=True)

    def add_event(self, user_id, iid, event_type, payload=None, occurred_at=None):
        e = {"id": str(uuid.uuid4()), "incident_id": iid, "user_id": user_id, "event_type": event_type,
             "payload": payload or {}, "occurred_at": occurred_at or _now()}
        self.events.setdefault(iid, []).append(e)
        return e

    def list_events(self, user_id, iid):
        return [e for e in self.events.get(iid, []) if e["user_id"] == user_id]

    def save_report(self, user_id, iid, report):
        self.reports[iid] = {"user_id": user_id, "report": report, "created_at": _now()}

    def save_upload(self, user_id, data: bytes, mime: str) -> str:
        path = f"{user_id}/{uuid.uuid4()}"
        self.uploads[path] = (data, mime)
        return path


class SupabaseRepository:
    """Production storage in Supabase Postgres and Storage (service-role key, so every query filters by user_id)."""

    def __init__(self, client):
        self.c = client

    def _one(self, res):
        data = res.data or []
        return data[0] if data else None

    def get_profile(self, user_id):
        return self._one(self.c.table("profiles").select("*").eq("id", user_id).limit(1).execute())

    def upsert_profile(self, user_id, patch):
        row = {"id": user_id, **patch}
        return self._one(self.c.table("profiles").upsert(row).execute())

    def create_session(self, user_id, title="New conversation"):
        return self._one(self.c.table("chat_sessions").insert({"user_id": user_id, "title": title, "state": {}}).execute())

    def list_sessions(self, user_id):
        return self.c.table("chat_sessions").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute().data or []

    def get_session(self, user_id, sid):
        return self._one(self.c.table("chat_sessions").select("*").eq("id", sid).eq("user_id", user_id).limit(1).execute())

    def update_session(self, user_id, sid, patch):
        return self._one(self.c.table("chat_sessions").update({**patch, "updated_at": _now()}).eq("id", sid).eq("user_id", user_id).execute())

    def delete_session(self, user_id, sid):
        if not self.get_session(user_id, sid):
            return False
        self.c.table("chat_sessions").delete().eq("id", sid).eq("user_id", user_id).execute()
        return True

    def add_message(self, user_id, sid, role, content):
        return self._one(self.c.table("chat_messages").insert({"session_id": sid, "user_id": user_id, "role": role, "content": content}).execute())

    def list_messages(self, user_id, sid):
        return self.c.table("chat_messages").select("*").eq("session_id", sid).eq("user_id", user_id).order("created_at").execute().data or []

    def create_incident(self, user_id, data):
        return self._one(self.c.table("incidents").insert({"user_id": user_id, **data}).execute())

    def get_incident(self, user_id, iid):
        return self._one(self.c.table("incidents").select("*").eq("id", iid).eq("user_id", user_id).limit(1).execute())

    def update_incident(self, user_id, iid, patch):
        return self._one(self.c.table("incidents").update(patch).eq("id", iid).eq("user_id", user_id).execute())

    def list_incidents(self, user_id):
        return self.c.table("incidents").select("*").eq("user_id", user_id).order("started_at", desc=True).execute().data or []

    def add_event(self, user_id, iid, event_type, payload=None, occurred_at=None):
        row = {"incident_id": iid, "user_id": user_id, "event_type": event_type, "payload": payload or {}}
        if occurred_at:
            row["occurred_at"] = occurred_at
        return self._one(self.c.table("incident_events").insert(row).execute())

    def list_events(self, user_id, iid):
        return self.c.table("incident_events").select("*").eq("incident_id", iid).eq("user_id", user_id).order("occurred_at").execute().data or []

    def save_report(self, user_id, iid, report):
        self.c.table("handover_reports").insert({"incident_id": iid, "user_id": user_id, "report": report}).execute()

    def save_upload(self, user_id, data: bytes, mime: str) -> str:
        import uuid as _uuid

        path = f"{user_id}/{_uuid.uuid4()}"
        try:
            self.c.storage.from_("user-uploads").upload(path, data, {"content-type": mime})
        except Exception:
            return ""
        return path


def make_supabase_client(url: str, key: str):
    """Create a Supabase client (imported lazily so tests do not need the package)."""
    from supabase import create_client

    return create_client(url, key)
