# Product spec: First Responder

Status: updated 2026-10-06 with your answers. Items marked *Open* wait for an answer in OPEN_QUESTIONS.md.

## Problem
In an emergency, people need correct, step-by-step guidance immediately, and often cannot type, read long text or search.
Existing chatbots are not grounded in verified guidelines.

## Users and roles (Decided)
Bystanders, or the patient themselves. The steps depend on the user's responsibility: bystander, self, or first responder.
When help arrives, a time-stamped **handover report** is generated for the first responders.

## Core features (Decided)
1. **Guideline-grounded RAG chat.** The most important part. Every answer comes from the guidelines. Built to be state of the art and measured for the paper.
2. **Scenario-based guidance.** 98 scenarios from 39 reusable modules, combining scene safety with each condition
   (see docs/scenarios/). Rare conditions can be added through the extension mechanism.
3. **Image + prompt.** Every image comes with a message. A snake or scorpion photo with "it just bit me": the app gives its
   best identification **with an explicit confidence** (for example "I can say with 59% confidence that it is not venomous")
   and always advises going to a hospital. *The handbook has no scorpion content (see gaps.md).*
4. **General conversation.** Handles small talk as well as emergencies.
5. **Step-by-step responses with media.** Each step can have a video or image (module-level, stored in object storage).
   The app checks if a step has media; if not, text only.
6. **Quick replies.** After each step: **Next** and a **Not worked**-style button, next to the text box.
7. **Hands-free mode.** Call-style voice: listens and speaks at the same time, decides when to send speech to the model.
8. **Hospital finder.** Finds hospitals that match the emergency, not just the nearest.
9. **Handover report.** ISBAR-style report with a timeline.
10. **Landing page.** Full, detailed; navbar Login and Sign up lead to their own pages.
11. **Authentication.** Email, Google sign-up and sign-in, forgot and reset password, email verification, hCaptcha. **No guest access.**

## UI (Decided)
- Chat UI follows the Figma "LLM Chatbots (Community)" design, without the model dropdown and model badges.
- Tailwind CSS, good-looking, proper typography, mobile-first.
- See docs/ui/design-notes.md.

## Out of scope
- NutriScan (separate project).
- Languages other than English (for now).

## Success criteria
Defined with you in Phase 1, once the evaluation set exists. No numeric targets are invented before then.
