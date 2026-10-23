import { useCallback, useEffect, useRef } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { ChatInput, type SendOptions } from "../components/chat/ChatInput";
import { ChatWindow } from "../components/chat/ChatWindow";
import { useShell } from "../components/chat/AppShell";
import { HandsFreeOverlay } from "../components/chat/HandsFreeOverlay";
import { HospitalPopup } from "../components/chat/HospitalPopup";
import { StepTimeline } from "../components/chat/StepTimeline";
import { useChat, spokenText } from "../hooks/useChat";
import { useHandsFree } from "../hooks/useHandsFree";
import type { QuickReply, ServerMessage } from "../types/chat";

/** A new `fresh` value in the navigation state gives a brand-new chat. */
export default function ChatPage() {
  const loc = useLocation();
  return <Chat key={(loc.state as { fresh?: number } | null)?.fresh ?? 0} />;
}

function Chat() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { refreshSessions } = useShell();
  const sessionId = id && id !== "new" ? id : null;
  const chat = useChat(sessionId);
  const ctx = useRef<SendOptions>({});
  const location = useLocation();
  const started = useRef(false);
  const handled = useRef<string | null>(null);

  useEffect(() => {
    const start = (location.state as { start?: string } | null)?.start;
    if (start && !started.current && !sessionId) {
      started.current = true;
      void chat.send(start, {});
    }
  }, [location.state, sessionId, chat]);

  useEffect(() => {
    if (chat.sessionId && !sessionId && handled.current !== chat.sessionId) {
      handled.current = chat.sessionId;
      refreshSessions();
      navigate(`/app/c/${chat.sessionId}`, { replace: true, state: location.state });
    }
  }, [chat.sessionId, sessionId, navigate, refreshSessions, location.state]);

  const newChat = (text?: string) => navigate("/app/c/new", { state: { start: text, fresh: Date.now() } });
  const onSend = useCallback((text: string, opts: SendOptions) => {
    if (chat.ended) { newChat(text); return; }
    ctx.current = opts; void chat.send(text, opts);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chat]);
  const onAction = useCallback((a: QuickReply["action"], text?: string) => {
    if (a === "ask") { void chat.send(text ?? "", ctx.current); return; } // a suggested reply is sent as the person's message
    void chat.act(a);
  }, [chat]);
  const hf = useHandsFree({
    onText: async (t) => { const r = await chat.send(t, ctx.current); return r ? spokenText(r.messages) : null; },
    onAction: async (a) => { const r = await chat.act(a); return r ? spokenText(r.messages) : null; },
  });

  const lastStep = [...chat.items].reverse().map((i) => i.message).find((m): m is Extract<ServerMessage, { type: "step" }> => m.type === "step");
  const idle = !chat.scenario || chat.scenario.status !== "active";

  return (
    <div className="flex min-h-0 flex-1 flex-col bg-gradient-to-b from-white to-ink-50">
      <div className="flex items-center justify-between gap-3 border-b border-ink-100 bg-white px-4 py-2.5 sm:px-8">
        <StepTimeline scenario={chat.scenario} />
      </div>
      {chat.loading ? <p className="p-8 text-sm text-ink-500">Loading conversation...</p> : chat.items.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center px-6 text-center">
          <h1 className="font-display text-3xl font-bold text-ink-950">What's happening?</h1>
          <p className="mt-2 max-w-md text-ink-500">Describe the emergency, send a photo, or turn on hands-free.</p>
        </div>
      ) : <ChatWindow items={chat.items} sending={chat.sending} error={chat.error} onAction={onAction} />}
      {chat.ended && (
        <div className="flex items-center justify-between gap-3 border-t border-ink-100 bg-white px-4 py-3 text-sm sm:px-8">
          <span className="text-ink-500">This emergency chat has ended.</span>
          <button onClick={() => newChat()} className="h-10 rounded-xl bg-brand-600 px-4 font-semibold text-white hover:bg-brand-700">Start new chat</button>
        </div>
      )}
      <ChatInput onSend={onSend} disabled={chat.sending} showContext={idle && !chat.ended} onHandsFree={() => void hf.start()} handsFreeSupported={hf.supported} />
      <HandsFreeOverlay state={hf.state} level={hf.level} transcript={hf.transcript} stepText={lastStep?.step.text ?? null} error={hf.error} onEnd={hf.stop} onAction={(a) => void hf.say("").then(() => chat.act(a)).then((r) => r && hf.say(spokenText(r.messages)))} />
      {chat.prompt && <HospitalPopup prompt={chat.prompt} incidentId={chat.incidentId} onClose={chat.dismissPrompt} />}
    </div>
  );
}