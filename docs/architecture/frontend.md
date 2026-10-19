# Frontend (React + TypeScript on Netlify)

Status: structure **Proposed**; the folders exist in `frontend/src/`.

## Pages
Landing, Login, Signup, Forgot password, Reset password, Verify email, Auth callback, Chat, Conversations, Profile, Not found.

## Landing page sections
Navbar (Login / Sign up), Hero, How it works, Features, Scenarios, Voice mode, Safety, FAQ, Footer.

## Chat components
Sidebar, ChatWindow, MessageBubble, StepCard, QuickReplies, MediaPlayer, ImageUpload, ChatInput, HandsFreeOverlay, CitationList, EmergencyCallBanner, TypingIndicator.

## Hooks
useAuth, useChatStream, useHandsFree, useVoiceActivity, useAudioPlayback, useMediaPrefetch.

## Notes
- `public/_redirects` makes client-side routes work on Netlify.
- Styling approach is an open question (11).
