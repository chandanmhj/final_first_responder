# Roles and the handover report

## Roles (Decided: responses depend on the user's responsibility)
| Role | Who | What changes |
|---|---|---|
| Bystander (B) | a person helping, with little or no training | hands-only steps, no pulse checks, no medicines |
| Self (S) | the patient is the user | only steps the patient can do alone; asks for help early |
| First responder (R) | trained responder | adds pulse checks, rescue breaths, bag valve mask, medication notes |

*Open:* how the role is chosen (at sign-up, at the start of each emergency, or both). See OPEN_QUESTIONS.md.

## Handover report (Decided)
When help arrives, the app generates a report for the first responders: **what happened and the time of each event**.
The handbook already defines a handover format, **ISBAR** (Identify, Situation, Background, Assessment/Actions, Recommendation),
and closed-loop communication. The report follows it.

### Events logged with timestamps (Proposed)
- Emergency started, scenario chosen, role.
- Each step shown, and the user's answer (Next / Not worked), with time.
- Call to 108 made, ambulance arrival.
- CPR started and each 2-minute cycle, AED attached, shocks advised or delivered.
- Tourniquet applied (time), helmet removed, patient moved.
- Photo sent (animal bite) and the result with its confidence.
- Symptom onset time (heart attack, stroke).
- Free-text notes the user adds.

### Report layout (Proposed)
Identify (who and where) > Situation (what happened) > Background (history, medicines, allergies if known) >
Assessment and actions (timeline) > Recommendation (hospital needs and what to do next).

### Storage
Reports and events are stored in Supabase (retention: forever, as you decided). See docs/architecture/database.md.
