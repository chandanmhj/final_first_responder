export type Role = "common" | "responder";

export type StepMedia = { video: string | null; image: string | null };

export type StepData = {
  id: string;
  index: number;
  total: number;
  text: string;
  source: string;
  page: string | null;
  authored: boolean;
  source_label: string;
  unreviewed_note: string | null;
  media: StepMedia;
  next_media: StepMedia | null;
};

export type QuickReply = {
  id: string;
  action: "next" | "not_worked" | "hospitals" | "report" | "restart" | "ask";
  label: string;
  text?: string;
};

export type Citation = { source: string; topic: string; page: string | null; label: string };

export type AnimalResult = {
  is_animal: boolean;
  category: string;
  species: string;
  venomous: "yes" | "no" | "unknown";
  confidence_pct: number;
  headline: string;
  advice: string[];
  condition: string | null;
  features: string[];
};

export type Hospital = {
  id: string;
  name: string;
  lat: number;
  lon: number;
  tier: string;
  class: string;
  distance_km: number;
  emergency_status: string;
  capabilities: string[];
  phones: string[];
  reasons: string[];
  directions_url: string;
  call_url: string | null;
  verified: boolean;
};

export type HandoverReport = {
  generated_at: string;
  identify: {
    reported_by_role: string | null;
    patient: string;
    age_band: string | null;
    started_at: string | null;
    location: string | null;
    patient_details?: Record<string, string | number> | null;
  };
  situation: { what_happened: string; scenario: string | null };
  background: { notes: string[] };
  assessment_and_actions: { time: string; text: string; type: string }[];
  recommendation: { facility_needs: string | null; call: string };
};

export type ServerMessage =
  | { type: "text"; text: string; citations?: Citation[]; quick_replies?: QuickReply[]; crisis?: boolean }
  | { type: "step"; step: StepData; quick_replies: QuickReply[] }
  | { type: "animal"; text: string; result: AnimalResult }
  | { type: "hospitals"; text: string; hospitals: Hospital[]; need: string | null }
  | { type: "needs_location"; text: string }
  | { type: "report"; text: string; incident_id: string; report: HandoverReport; markdown: string }
  | { type: "hospital_prompt"; text: string; maps_url: string; condition?: string | null; hospital: { name: string; distance_km: number; tier?: string } | null };

export type ScenarioInfo = {
  condition: string;
  title: string;
  location: string | null;
  index: number;
  total: number;
  status: "idle" | "active" | "completed" | "ended";
};

export type ChatResponse = {
  session_id: string;
  incident_id: string | null;
  urgent: boolean;
  scenario: ScenarioInfo | null;
  ended?: boolean;
  messages: ServerMessage[];
};

export type UserBubble = { type: "user"; text: string; hasImage: boolean; imageUrl?: string };

export type ChatItem = { id: string; from: "user" | "assistant"; message: ServerMessage | UserBubble };

export type SessionSummary = {
  id: string;
  title: string;
  updated_at: string;
  status: string;
  condition: string | null;
  incident_id: string | null;
  pinned?: boolean;
};

export type Profile = {
  id: string;
  email: string | null;
  full_name: string | null;
  role: Role | null;
  cert_number: string | null;
  attested_at: string | null;
  age: number | null;
  sex: string | null;
  blood_group: string | null;
  allergies: string | null;
  conditions: string | null;
  medications: string | null;
  emergency_contact: string | null;
};