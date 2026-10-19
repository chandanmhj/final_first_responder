import { useCallback, useEffect, useRef } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { ChatInput, type SendOptions } from "../components/chat/ChatInput";
import { ChatWindow } from "../components/chat/ChatWindow";
import { useShell } from "../components/chat/AppShell";
import { EmergencyCallBanner } from "../components/chat/EmergencyCallBanner";
import { HandsFreeOverlay } from "../components/chat/HandsFreeOverlay";
import { StepTimeline } from "../components/chat/StepTimeline";
import { useChat, spokenText } from "../hooks/useChat";
import { useHandsFree } from "../hooks/useHandsFree";
import type { QuickReply, ServerMessage } from "../types/chat";

/** One conversation: messages, step cards with quick replies, photo upload, and hands-free mode. */
export default function ChatPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { refreshSessions } = useShell();
  const sessionId = id && id !== "new" ? id : null;
  const chat = useChat(sessionId);
  const first = useRef<string | null | undefined>(undefined);
  const ctx = useRef<SendOptions>({});
  const location = useLocation();
  const started = useRef(false);

  useEffect(() => {
    const start = (location.state as { start?: string } | null)?.start;
    if (start && !started.current && !sessionId) {
      started.current = true;
      void chat.send(start, {});
    }
  }, [location.state, sessionId, chat]);

    const handled = useRef<string | null>(null);
  useEffect(() => {
    if (chat.sessionId && !sessionId && handled.current !== chat.sessionId) {
      handled.current = chat.sessionId;
      refreshSessions();
      navigate(`/app/c/${chat.sessionId}`, { replace: true });
    }
  }, [chat.sessionId, sessionId, navigate, refreshSessions]);

  const onSend = useCallback((text: string, opts: SendOptions) => { ctx.current = opts; void chat.send(text, opts); }, [chat]);
  const onAction = useCallback((a: QuickReply["action"]) => { void chat.act(a); }, [chat]);

  const hf = useHandsFree({
    onText: async (t) => { const r = await chat.send(t, ctx.current); return r ? spokenText(r.messages) : null; },
    onAction: async (a) => { const r = await chat.act(a); return r ? spokenText(r.messages) : null; },
  });

  const lastStep = [...chat.items].reverse().map((i) => i.message).find((m): m is Extract<ServerMessage, { type: "step" }> => m.type === "step");
  const idle = !chat.scenario || chat.scenario.status !== "active";
  if (first.current === undefined) first.current = sessionId;

  return (
    <div className="flex min-h-0 flex-1 flex-col bg-gradient-to-b from-white to-ink-50">
      <div className="flex items-center justify-between gap-3 border-b border-ink-100 bg-white px-4 py-2.5 sm:px-8">
        <StepTimeline scenario={chat.scenario} />
        {chat.urgent && <EmergencyCallBanner urgent />}
      </div>
      {chat.loading ? <p className="p-8 text-sm text-ink-500">Loading conversation...</p> : chat.items.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center px-6 text-center">
          <h1 className="font-display text-3xl font-bold text-ink-950">What's happening?</h1>
          <p className="mt-2 max-w-md text-ink-500">Describe the emergency, send a photo, or turn on hands-free. If someone is in danger, call 108 now.</p>
        </div>
      ) : <ChatWindow items={chat.items} sending={chat.sending} error={chat.error} onAction={onAction} />}
      <ChatInput onSend={onSend} disabled={chat.sending} showContext={idle} onHandsFree={() => void hf.start()} handsFreeSupported={hf.supported} />
      <HandsFreeOverlay state={hf.state} level={hf.level} transcript={hf.transcript} stepText={lastStep?.step.text ?? null} error={hf.error} onEnd={hf.stop} onAction={(a) => void hf.say("").then(() => chat.act(a)).then((r) => r && hf.say(spokenText(r.messages)))} />
    </div>
  );
}
