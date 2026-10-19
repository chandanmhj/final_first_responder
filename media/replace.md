# Media placeholders (replace.md)

You add the videos and images. Each step below has a video name and an image name. Provide either, both, or neither. If neither exists for a step, the app sends text only.

Steps are grouped by **module**. A module is reused by many scenarios (for example `cpr_adult` appears in every cardiac arrest scenario), so one clip serves all of them. Work from the top: the list is sorted by how many scenarios use each module.

## How to name and store files

- Put originals in `media/emergencies/<module>/` using the names below, compressed outputs in `media/processed/`.
- Video: MP4 (H.264), 480p to 720p, about 10 to 20 seconds, muted unless audio is needed. Image: WebP.
- Tick the box when a file is added, and update `media/manifest.yaml` status (`video`, `image` or `both`).
- Re-running `python scripts/expand_scenarios.py --overwrite-replace` rebuilds this file and erases your ticks.

## Production priority

| Module | Title | Used in scenarios | Steps |
|---|---|---|---|
| `scene_safety` | Scene safety check | 139 | 6 |
| `safe_transfer` | Safe transport and handover | 109 | 9 |
| `call_for_help` | Call for help | 82 | 3 |
| `primary_assessment` | Primary assessment (AVPU, signs of life) | 29 | 8 |
| `hazard_vehicle_journey` | Hazard: patient in a vehicle during a journey | 16 | 3 |
| `bleeding_control` | Bleeding control | 15 | 9 |
| `shock` | Shock | 14 | 6 |
| `aed` | Using an AED | 13 | 7 |
| `hazard_industrial` | Hazard: heavy machinery or factory | 13 | 2 |
| `fracture_sprain` | Fracture or sprain (RICE) | 10 | 6 |
| `burns` | Burns | 9 | 7 |
| `cpr_adult` | CPR: adult chest compressions | 9 | 12 |
| `hazard_road_scene` | Hazard: road accident scene | 9 | 4 |
| `neck_stabilization` | Neck stabilisation | 9 | 4 |
| `breathing_difficulty` | Breathing difficulty | 7 | 5 |
| `heat_illness` | Heat illness and heatstroke | 7 | 5 |
| `log_roll` | Log roll (4 people) | 7 | 5 |
| `seizure` | Seizure (fit) | 7 | 10 |
| `anaphylaxis` | Severe allergic reaction (anaphylaxis) | 6 | 7 |
| `asthma_attack` | Asthma attack | 6 | 6 |
| `infection_red_flags` | Infection: when to see a doctor now | 6 | 3 |
| `panic_attack` | Panic or anxiety | 6 | 5 |
| `recovery_position` | Recovery position | 6 | 2 |
| `chest_abdomen_injury` | Chest or abdomen injury | 5 | 5 |
| `fainting` | Feeling faint or fainting | 5 | 6 |
| `head_injury` | Head injury | 5 | 4 |
| `heart_attack` | Heart attack | 5 | 10 |
| `low_blood_sugar` | Low blood sugar | 5 | 8 |
| `poisoning` | Poisoning | 5 | 7 |
| `stroke` | Stroke | 5 | 7 |
| `amputation` | Amputation | 4 | 5 |
| `choking_adult_child` | Choking: adult and child (awake) | 4 | 7 |
| `choking_special_cases` | Choking: special cases | 4 | 3 |
| `cpr_child_infant` | CPR: child and infant | 4 | 7 |
| `electric_shock` | Electric shock | 4 | 3 |
| `emergency_childbirth` | Emergency childbirth | 4 | 8 |
| `hazard_animal_snake` | Hazard: snake nearby | 4 | 2 |
| `insect_sting` | Insect bite or sting | 4 | 5 |
| `scorpion_sting` | Scorpion sting | 4 | 7 |
| `snake_bite` | Snake bite | 4 | 9 |
| `wound_care_minor` | Minor wound care | 4 | 2 |
| `animal_bite` | Animal bite (dog, cat, other animals) | 3 | 4 |
| `choking_self` | Choking: if you are alone | 3 | 3 |
| `fever` | Fever | 3 | 4 |
| `hazard_water` | Hazard: water (reach, throw, don't go) | 3 | 3 |
| `high_blood_sugar` | High blood sugar | 3 | 3 |
| `hypothermia` | Hypothermia (cold) | 3 | 5 |
| `nosebleed` | Nosebleed | 3 | 3 |
| `choking_infant` | Choking: infant | 2 | 7 |
| `drowning` | Drowning | 2 | 9 |
| `helmet_removal` | Helmet removal | 2 | 8 |
| `car_patient_placement` | Car accident: patient placement | 1 | 4 |
| `hazard_fire_smoke` | Hazard: fire and smoke | 1 | 5 |
| `hazard_railway` | Hazard: railway | 1 | 2 |
| `hazard_electric` | Hazard: live electrical wires | 0 | 2 |
| `rescue_breaths` | Rescue breaths (trained responders) | 0 | 3 |

## Scene safety check (`scene_safety`)
Used in 139 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | scene_safety.01 | Ask yourself: Am I safe? Is my team safe? Are we safe from approach... | `scene_safety/01-ask-yourself-am-i-safe.mp4` | `scene_safety/01-ask-yourself-am-i-safe.webp` |
| [ ] | scene_safety.02 | Look, listen and smell for hazards: sparks, trains or fast traffic,... | `scene_safety/02-look-listen-and-smell-for.mp4` | `scene_safety/02-look-listen-and-smell-for.webp` |
| [ ] | scene_safety.03 | Check the patient is safe. Move them away from immediate danger (ra... | `scene_safety/03-check-the-patient-is-safe.mp4` | `scene_safety/03-check-the-patient-is-safe.webp` |
| [ ] | scene_safety.04 | Check the whole environment: moving traffic, toxic fumes, loose wir... | `scene_safety/04-check-the-whole-environment-moving.mp4` | `scene_safety/04-check-the-whole-environment-moving.webp` |
| [ ] | scene_safety.05 | Count the victims. If there are several, help those who need immedi... | `scene_safety/05-count-the-victims-if-there.mp4` | `scene_safety/05-count-the-victims-if-there.webp` |
| [ ] | scene_safety.06 | Do not start resuscitation, and do not touch body fluids or pestici... | `scene_safety/06-do-not-start-resuscitation-and.mp4` | `scene_safety/06-do-not-start-resuscitation-and.webp` |

## Safe transport and handover (`safe_transfer`)
Used in 109 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | safe_transfer.01 | Plan before you move: where and how to take the patient, the receiv... | `safe_transfer/01-plan-before-you-move-where.mp4` | `safe_transfer/01-plan-before-you-move-where.webp` |
| [ ] | safe_transfer.02 | Choose an ambulance, or a vehicle with trained people and the right... | `safe_transfer/02-choose-an-ambulance-or-a.mp4` | `safe_transfer/02-choose-an-ambulance-or-a.webp` |
| [ ] | safe_transfer.03 | If the patient cannot walk, move them on a stretcher. If there is n... | `safe_transfer/03-if-the-patient-cannot-walk.mp4` | `safe_transfer/03-if-the-patient-cannot-walk.webp` |
| [ ] | safe_transfer.04 | If a spine injury is possible, move the patient with the log roll t... | `safe_transfer/04-if-a-spine-injury-is.mp4` | `safe_transfer/04-if-a-spine-injury-is.webp` |
| [ ] | safe_transfer.05 | Keep the neck neutral and avoid bending the neck or back. | `safe_transfer/05-keep-the-neck-neutral-and.mp4` | `safe_transfer/05-keep-the-neck-neutral-and.webp` |
| [ ] | safe_transfer.06 | Keep the patient cool: AC or fan, no blankets. | `safe_transfer/06-keep-the-patient-cool-ac.mp4` | `safe_transfer/06-keep-the-patient-cool-ac.webp` |
| [ ] | safe_transfer.07 | Re-check the patient every 5 minutes during transport (breathing, r... | `safe_transfer/07-recheck-the-patient-every-5.mp4` | `safe_transfer/07-recheck-the-patient-every-5.webp` |
| [ ] | safe_transfer.08 | Hand over using ISBAR: Identify, Situation, Background, Assessment... | `safe_transfer/08-hand-over-using-isbar-identify.mp4` | `safe_transfer/08-hand-over-using-isbar-identify.webp` |
| [ ] | safe_transfer.09 | Follow the receiving doctor's instructions during transport and rep... | `safe_transfer/09-follow-the-receiving-doctors-instructions.mp4` | `safe_transfer/09-follow-the-receiving-doctors-instructions.webp` |

## Call for help (`call_for_help`)
Used in 82 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | call_for_help.01 | Call 108 for an ambulance, or point at one person nearby and tell t... | `call_for_help/01-call-108-for-an-ambulance.mp4` | `call_for_help/01-call-108-for-an-ambulance.webp` |
| [ ] | call_for_help.02 | Ask for the right equipment: an AED for a collapsed or unresponsive... | `call_for_help/02-ask-for-the-right-equipment.mp4` | `call_for_help/02-ask-for-the-right-equipment.webp` |
| [ ] | call_for_help.03 | Give the exact location, what happened, how many people are hurt, a... | `call_for_help/03-give-the-exact-location-what.mp4` | `call_for_help/03-give-the-exact-location-what.webp` |

## Primary assessment (AVPU, signs of life) (`primary_assessment`)
Used in 29 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | primary_assessment.01 | Check how responsive they are (AVPU). Alert? Talk loudly and tap th... | `primary_assessment/01-check-how-responsive-they-are.mp4` | `primary_assessment/01-check-how-responsive-they-are.webp` |
| [ ] | primary_assessment.02 | If they respond only to pain or not at all, it is serious. Call for... | `primary_assessment/02-if-they-respond-only-to.mp4` | `primary_assessment/02-if-they-respond-only-to.webp` |
| [ ] | primary_assessment.03 | Cover your face and theirs with a mask or cloth. | `primary_assessment/03-cover-your-face-and-theirs.mp4` | `primary_assessment/03-cover-your-face-and-theirs.webp` |
| [ ] | primary_assessment.04 | Look at the chest for rise (breathing) for up to 10 seconds. Watch... | `primary_assessment/04-look-at-the-chest-for.mp4` | `primary_assessment/04-look-at-the-chest-for.webp` |
| [ ] | primary_assessment.05 | If you are trained: feel for a pulse at one side of the neck (carot... | `primary_assessment/05-if-you-are-trained-feel.mp4` | `primary_assessment/05-if-you-are-trained-feel.webp` |
| [ ] | primary_assessment.06 | Not responding and no breathing or signs of life (and no pulse, if... | `primary_assessment/06-not-responding-and-no-breathing.mp4` | `primary_assessment/06-not-responding-and-no-breathing.webp` |
| [ ] | primary_assessment.07 | Pulse present but not breathing: call for help and, if trained, hel... | `primary_assessment/07-pulse-present-but-not-breathing.mp4` | `primary_assessment/07-pulse-present-but-not-breathing.webp` |
| [ ] | primary_assessment.08 | Pulse and breathing present: place in the recovery position (protec... | `primary_assessment/08-pulse-and-breathing-present-place.mp4` | `primary_assessment/08-pulse-and-breathing-present-place.webp` |

## Hazard: patient in a vehicle during a journey (`hazard_vehicle_journey`)
Used in 16 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_vehicle_journey.01 | If you are driving and feel unwell, slow down, signal and pull over... | `hazard_vehicle_journey/01-if-you-are-driving-and.mp4` | `hazard_vehicle_journey/01-if-you-are-driving-and.webp` |
| [ ] | hazard_vehicle_journey.02 | Switch on the hazard lights, stop the engine and apply the parking... | `hazard_vehicle_journey/02-switch-on-the-hazard-lights.mp4` | `hazard_vehicle_journey/02-switch-on-the-hazard-lights.webp` |
| [ ] | hazard_vehicle_journey.03 | Do not keep driving with a collapsing patient. Stop first, then cal... | `hazard_vehicle_journey/03-do-not-keep-driving-with.mp4` | `hazard_vehicle_journey/03-do-not-keep-driving-with.webp` |

## Bleeding control (`bleeding_control`)
Used in 15 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | bleeding_control.01 | Wear gloves or put plastic over your hand if you can. Press firmly... | `bleeding_control/01-wear-gloves-or-put-plastic.mp4` | `bleeding_control/01-wear-gloves-or-put-plastic.webp` |
| [ ] | bleeding_control.02 | Suspect severe bleeding if clothes are soaked with blood or blood i... | `bleeding_control/02-suspect-severe-bleeding-if-clothes.mp4` | `bleeding_control/02-suspect-severe-bleeding-if-clothes.webp` |
| [ ] | bleeding_control.03 | If it keeps bleeding or you need your hands free, put a thick pad o... | `bleeding_control/03-if-it-keeps-bleeding-or.mp4` | `bleeding_control/03-if-it-keeps-bleeding-or.webp` |
| [ ] | bleeding_control.04 | Check the dressing often to make sure the bleeding has stopped. | `bleeding_control/04-check-the-dressing-often-to.mp4` | `bleeding_control/04-check-the-dressing-often-to.webp` |
| [ ] | bleeding_control.05 | If a limb keeps bleeding heavily despite a pressure dressing, put a... | `bleeding_control/05-if-a-limb-keeps-bleeding.mp4` | `bleeding_control/05-if-a-limb-keeps-bleeding.webp` |
| [ ] | bleeding_control.06 | Use a band at least 3 to 4 finger-widths wide, such as a cloth stri... | `bleeding_control/06-use-a-band-at-least.mp4` | `bleeding_control/06-use-a-band-at-least.webp` |
| [ ] | bleeding_control.07 | Write down the time the tourniquet was applied and tell the ambulan... | `bleeding_control/07-write-down-the-time-the.mp4` | `bleeding_control/07-write-down-the-time-the.webp` |
| [ ] | bleeding_control.08 | Signs of internal bleeding: severe pain, large bruises on the chest... | `bleeding_control/08-signs-of-internal-bleeding-severe.mp4` | `bleeding_control/08-signs-of-internal-bleeding-severe.webp` |
| [ ] | bleeding_control.09 | When moving the patient, avoid bending the neck and back. | `bleeding_control/09-when-moving-the-patient-avoid.mp4` | `bleeding_control/09-when-moving-the-patient-avoid.webp` |

## Shock (`shock`)
Used in 14 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | shock.01 | Help them lie down on their back, or in the most comfortable positi... | `shock/01-help-them-lie-down-on.mp4` | `shock/01-help-them-lie-down-on.webp` |
| [ ] | shock.02 | Treat the cause if you can. For example press on a bleeding wound. | `shock/02-treat-the-cause-if-you.mp4` | `shock/02-treat-the-cause-if-you.webp` |
| [ ] | shock.03 | Call 108 immediately. | `shock/03-call-108-immediately.mp4` | `shock/03-call-108-immediately.webp` |
| [ ] | shock.04 | Keep them warm with a blanket or clothing and protect them from a c... | `shock/04-keep-them-warm-with-a.mp4` | `shock/04-keep-them-warm-with-a.webp` |
| [ ] | shock.05 | Reassure them and watch their responsiveness and breathing. If they... | `shock/05-reassure-them-and-watch-their.mp4` | `shock/05-reassure-them-and-watch-their.webp` |
| [ ] | shock.06 | If it helps them feel better and there is no injury, you may raise... | `shock/06-if-it-helps-them-feel.mp4` | `shock/06-if-it-helps-them-feel.webp` |

## Using an AED (`aed`)
Used in 13 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | aed.01 | Switch the AED on as soon as it arrives and follow its voice prompts. | `aed/01-switch-the-aed-on-as.mp4` | `aed/01-switch-the-aed-on-as.webp` |
| [ ] | aed.02 | Attach the pads to the person's chest and plug the pad connector in... | `aed/02-attach-the-pads-to-the.mp4` | `aed/02-attach-the-pads-to-the.webp` |
| [ ] | aed.03 | When it says it is analysing, stop compressions and make sure nobod... | `aed/03-when-it-says-it-is.mp4` | `aed/03-when-it-says-it-is.webp` |
| [ ] | aed.04 | If it says shock is advised, say loudly: stay away, I am clear, you... | `aed/04-if-it-says-shock-is.mp4` | `aed/04-if-it-says-shock-is.webp` |
| [ ] | aed.05 | Restart compressions immediately after the shock. Do not check the... | `aed/05-restart-compressions-immediately-after-the.mp4` | `aed/05-restart-compressions-immediately-after-the.webp` |
| [ ] | aed.06 | If it says no shock is advised, continue chest compressions. | `aed/06-if-it-says-no-shock.mp4` | `aed/06-if-it-says-no-shock.webp` |
| [ ] | aed.07 | Leave the AED attached even if the pulse returns. The heart can sto... | `aed/07-leave-the-aed-attached-even.mp4` | `aed/07-leave-the-aed-attached-even.webp` |

## Hazard: heavy machinery or factory (`hazard_industrial`)
Used in 13 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_industrial.01 | Make sure heavy machinery is switched off before you go near the pa... | `hazard_industrial/01-make-sure-heavy-machinery-is.mp4` | `hazard_industrial/01-make-sure-heavy-machinery-is.webp` |
| [ ] | hazard_industrial.02 | Count the victims. In factories, several people may be hurt: help t... | `hazard_industrial/02-count-the-victims-in-factories.mp4` | `hazard_industrial/02-count-the-victims-in-factories.webp` |

## Fracture or sprain (RICE) (`fracture_sprain`)
Used in 10 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | fracture_sprain.01 | Rest: do not move the injured part or put weight on it. | `fracture_sprain/01-rest-do-not-move-the.mp4` | `fracture_sprain/01-rest-do-not-move-the.webp` |
| [ ] | fracture_sprain.02 | Control any bleeding first, before you apply a splint. | `fracture_sprain/02-control-any-bleeding-first-before.mp4` | `fracture_sprain/02-control-any-bleeding-first-before.webp` |
| [ ] | fracture_sprain.03 | Immobilise: splint with a stick or pipe padded with cloth. Extend i... | `fracture_sprain/03-immobilise-splint-with-a-stick.mp4` | `fracture_sprain/03-immobilise-splint-with-a-stick.webp` |
| [ ] | fracture_sprain.04 | Check circulation often (pale colour, swelling). | `fracture_sprain/04-check-circulation-often-pale-colour.mp4` | `fracture_sprain/04-check-circulation-often-pale-colour.webp` |
| [ ] | fracture_sprain.05 | Ice: apply ice on intact skin above the fracture or sprain. | `fracture_sprain/05-ice-apply-ice-on-intact.mp4` | `fracture_sprain/05-ice-apply-ice-on-intact.webp` |
| [ ] | fracture_sprain.06 | Elevate: keep the injured part above the level of the heart. | `fracture_sprain/06-elevate-keep-the-injured-part.mp4` | `fracture_sprain/06-elevate-keep-the-injured-part.webp` |

## Burns (`burns`)
Used in 9 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | burns.01 | Cool the burn under running water for 15 to 20 minutes. | `burns/01-cool-the-burn-under-running.mp4` | `burns/01-cool-the-burn-under-running.webp` |
| [ ] | burns.02 | Remove jewellery near the burn before swelling starts. | `burns/02-remove-jewellery-near-the-burn.mp4` | `burns/02-remove-jewellery-near-the-burn.webp` |
| [ ] | burns.03 | Cover the burn loosely with a clean cloth. | `burns/03-cover-the-burn-loosely-with.mp4` | `burns/03-cover-the-burn-loosely-with.webp` |
| [ ] | burns.04 | Do NOT put anything on the burn. Do NOT break blisters. | `burns/04-do-not-put-anything-on.mp4` | `burns/04-do-not-put-anything-on.webp` |
| [ ] | burns.05 | Keep a burned limb raised to reduce swelling. | `burns/05-keep-a-burned-limb-raised.mp4` | `burns/05-keep-a-burned-limb-raised.webp` |
| [ ] | burns.06 | Control any bleeding that comes with the burn. | `burns/06-control-any-bleeding-that-comes.mp4` | `burns/06-control-any-bleeding-that-comes.webp` |
| [ ] | burns.07 | Burns are life-threatening if caused by electric shock, if they inv... | `burns/07-burns-are-lifethreatening-if-caused.mp4` | `burns/07-burns-are-lifethreatening-if-caused.webp` |

## CPR: adult chest compressions (`cpr_adult`)
Used in 9 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | cpr_adult.01 | Start chest compressions right away if the person is unresponsive a... | `cpr_adult/01-start-chest-compressions-right-away.mp4` | `cpr_adult/01-start-chest-compressions-right-away.webp` |
| [ ] | cpr_adult.02 | Lay them on a hard, flat surface. If they are on a bed, move them t... | `cpr_adult/02-lay-them-on-a-hard.mp4` | `cpr_adult/02-lay-them-on-a-hard.webp` |
| [ ] | cpr_adult.03 | Kneel at their side, level with the chest, with your shoulders in l... | `cpr_adult/03-kneel-at-their-side-level.mp4` | `cpr_adult/03-kneel-at-their-side-level.webp` |
| [ ] | cpr_adult.04 | Put the heel of one hand on the middle of the chest, on the lower h... | `cpr_adult/04-put-the-heel-of-one.mp4` | `cpr_adult/04-put-the-heel-of-one.webp` |
| [ ] | cpr_adult.05 | Lock your elbows and keep your arms straight. Push with your body w... | `cpr_adult/05-lock-your-elbows-and-keep.mp4` | `cpr_adult/05-lock-your-elbows-and-keep.webp` |
| [ ] | cpr_adult.06 | Push down about one-third of the chest depth, at 100 to 120 pushes... | `cpr_adult/06-push-down-about-onethird-of.mp4` | `cpr_adult/06-push-down-about-onethird-of.webp` |
| [ ] | cpr_adult.07 | Do not stop. If someone else is there, swap every 2 minutes with as... | `cpr_adult/07-do-not-stop-if-someone.mp4` | `cpr_adult/07-do-not-stop-if-someone.webp` |
| [ ] | cpr_adult.08 | Use an AED as soon as one arrives and follow its voice prompts. | `cpr_adult/08-use-an-aed-as-soon.mp4` | `cpr_adult/08-use-an-aed-as-soon.webp` |
| [ ] | cpr_adult.09 | Stop only if: they show signs of life (open eyes, breathe, make sou... | `cpr_adult/09-stop-only-if-they-show.mp4` | `cpr_adult/09-stop-only-if-they-show.webp` |
| [ ] | cpr_adult.10 | Every 2 minutes (about 200 to 240 compressions) pause for no more t... | `cpr_adult/10-every-2-minutes-about-200.mp4` | `cpr_adult/10-every-2-minutes-about-200.webp` |
| [ ] | cpr_adult.11 | If there is no pulse or sign of life after 20 to 40 minutes, the te... | `cpr_adult/11-if-there-is-no-pulse.mp4` | `cpr_adult/11-if-there-is-no-pulse.webp` |
| [ ] | cpr_adult.12 | Do not do chest compressions if a pulse is present. | `cpr_adult/12-do-not-do-chest-compressions.mp4` | `cpr_adult/12-do-not-do-chest-compressions.webp` |

## Hazard: road accident scene (`hazard_road_scene`)
Used in 9 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_road_scene.01 | Do not stand in moving traffic. Check for approaching vehicles befo... | `hazard_road_scene/01-do-not-stand-in-moving.mp4` | `hazard_road_scene/01-do-not-stand-in-moving.webp` |
| [ ] | hazard_road_scene.02 | Ask bystanders to warn oncoming traffic and keep the crowd back. | `hazard_road_scene/02-ask-bystanders-to-warn-oncoming.mp4` | `hazard_road_scene/02-ask-bystanders-to-warn-oncoming.webp` |
| [ ] | hazard_road_scene.03 | Ask for engines to be switched off and for nobody to smoke. Watch f... | `hazard_road_scene/03-ask-for-engines-to-be.mp4` | `hazard_road_scene/03-ask-for-engines-to-be.webp` |
| [ ] | hazard_road_scene.04 | Do not move injured people unless there is immediate danger such as... | `hazard_road_scene/04-do-not-move-injured-people.mp4` | `hazard_road_scene/04-do-not-move-injured-people.webp` |

## Neck stabilisation (`neck_stabilization`)
Used in 9 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | neck_stabilization.01 | Suspect a neck injury in every trauma patient until it is ruled out. | `neck_stabilization/01-suspect-a-neck-injury-in.mp4` | `neck_stabilization/01-suspect-a-neck-injury-in.webp` |
| [ ] | neck_stabilization.02 | Keep the neck in a neutral position, especially when moving or tran... | `neck_stabilization/02-keep-the-neck-in-a.mp4` | `neck_stabilization/02-keep-the-neck-in-a.webp` |
| [ ] | neck_stabilization.03 | Fit a cervical collar if one is available. | `neck_stabilization/03-fit-a-cervical-collar-if.mp4` | `neck_stabilization/03-fit-a-cervical-collar-if.webp` |
| [ ] | neck_stabilization.04 | Tell them not to move their head, and keep them still. | `neck_stabilization/04-tell-them-not-to-move.mp4` | `neck_stabilization/04-tell-them-not-to-move.webp` |

## Breathing difficulty (`breathing_difficulty`)
Used in 7 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | breathing_difficulty.01 | Help them into a comfortable position, usually sitting. Leaning for... | `breathing_difficulty/01-help-them-into-a-comfortable.mp4` | `breathing_difficulty/01-help-them-into-a-comfortable.webp` |
| [ ] | breathing_difficulty.02 | If they have their own medicine (for example an inhaler), help them... | `breathing_difficulty/02-if-they-have-their-own.mp4` | `breathing_difficulty/02-if-they-have-their-own.webp` |
| [ ] | breathing_difficulty.03 | Call 108 at once if: the medicine is not working after a couple of... | `breathing_difficulty/03-call-108-at-once-if.mp4` | `breathing_difficulty/03-call-108-at-once-if.webp` |
| [ ] | breathing_difficulty.04 | If you are trained and oxygen is available, give it as needed. | `breathing_difficulty/04-if-you-are-trained-and.mp4` | `breathing_difficulty/04-if-you-are-trained-and.webp` |
| [ ] | breathing_difficulty.05 | Stay with them and keep watching until breathing is back to normal... | `breathing_difficulty/05-stay-with-them-and-keep.mp4` | `breathing_difficulty/05-stay-with-them-and-keep.webp` |

## Heat illness and heatstroke (`heat_illness`)
Used in 7 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | heat_illness.01 | Stop all activity. Move them to a cool place and take off extra clo... | `heat_illness/01-stop-all-activity-move-them.mp4` | `heat_illness/01-stop-all-activity-move-them.webp` |
| [ ] | heat_illness.02 | Cool them quickly: cold water on hands and feet, ice packs on the n... | `heat_illness/02-cool-them-quickly-cold-water.mp4` | `heat_illness/02-cool-them-quickly-cold-water.webp` |
| [ ] | heat_illness.03 | If they are not vomiting, give water, a sports drink or cold sweet... | `heat_illness/03-if-they-are-not-vomiting.mp4` | `heat_illness/03-if-they-are-not-vomiting.webp` |
| [ ] | heat_illness.04 | Call 108 immediately if they are confused, drowsy, aggressive, have... | `heat_illness/04-call-108-immediately-if-they.mp4` | `heat_illness/04-call-108-immediately-if-they.webp` |
| [ ] | heat_illness.05 | Keep checking their temperature and responsiveness until they recov... | `heat_illness/05-keep-checking-their-temperature-and.mp4` | `heat_illness/05-keep-checking-their-temperature-and.webp` |

## Log roll (4 people) (`log_roll`)
Used in 7 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | log_roll.01 | You need at least 4 people: one to hold the head and neck and lead,... | `log_roll/01-you-need-at-least-4.mp4` | `log_roll/01-you-need-at-least-4.webp` |
| [ ] | log_roll.02 | Leader holds head and neck. Helper 1 holds shoulder and hip. Helper... | `log_roll/02-leader-holds-head-and-neck.mp4` | `log_roll/02-leader-holds-head-and-neck.webp` |
| [ ] | log_roll.03 | On the leader's count of three, roll the person like a log, all at... | `log_roll/03-on-the-leaders-count-of.mp4` | `log_roll/03-on-the-leaders-count-of.webp` |
| [ ] | log_roll.04 | Examine the back and slide a spine board or stretcher in. | `log_roll/04-examine-the-back-and-slide.mp4` | `log_roll/04-examine-the-back-and-slide.webp` |
| [ ] | log_roll.05 | On the leader's count of three, roll them back together onto the bo... | `log_roll/05-on-the-leaders-count-of.mp4` | `log_roll/05-on-the-leaders-count-of.webp` |

## Seizure (fit) (`seizure`)
Used in 7 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | seizure.01 | Stay calm. Most fits stop by themselves. | `seizure/01-stay-calm-most-fits-stop.mp4` | `seizure/01-stay-calm-most-fits-stop.webp` |
| [ ] | seizure.02 | If the whole body is shaking, clear hard or sharp objects away and... | `seizure/02-if-the-whole-body-is.mp4` | `seizure/02-if-the-whole-body-is.webp` |
| [ ] | seizure.03 | Remove glasses and loosen anything tight around the neck, such as a... | `seizure/03-remove-glasses-and-loosen-anything.mp4` | `seizure/03-remove-glasses-and-loosen-anything.webp` |
| [ ] | seizure.04 | Do NOT hold the person down. Do NOT put anything in their mouth. | `seizure/04-do-not-hold-the-person.mp4` | `seizure/04-do-not-hold-the-person.webp` |
| [ ] | seizure.05 | Watch the time. Call 108 if the fit lasts more than 5 minutes. | `seizure/05-watch-the-time-call-108.mp4` | `seizure/05-watch-the-time-call-108.webp` |
| [ ] | seizure.06 | When it stops, reassure them and tell them what happened. Be aware... | `seizure/06-when-it-stops-reassure-them.mp4` | `seizure/06-when-it-stops-reassure-them.webp` |
| [ ] | seizure.07 | If they are sleepy, place them in the recovery position until they... | `seizure/07-if-they-are-sleepy-place.mp4` | `seizure/07-if-they-are-sleepy-place.webp` |
| [ ] | seizure.08 | Check blood sugar if you can. If it is low, treat it. | `seizure/08-check-blood-sugar-if-you.mp4` | `seizure/08-check-blood-sugar-if-you.webp` |
| [ ] | seizure.09 | Help them get home or to a healthcare facility. If they missed thei... | `seizure/09-help-them-get-home-or.mp4` | `seizure/09-help-them-get-home-or.webp` |
| [ ] | seizure.10 | If it happened while driving, swimming or near machinery, check for... | `seizure/10-if-it-happened-while-driving.mp4` | `seizure/10-if-it-happened-while-driving.webp` |

## Severe allergic reaction (anaphylaxis) (`anaphylaxis`)
Used in 6 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | anaphylaxis.01 | Call 108 as soon as you see signs of a severe allergic reaction (sw... | `anaphylaxis/01-call-108-as-soon-as.mp4` | `anaphylaxis/01-call-108-as-soon-as.webp` |
| [ ] | anaphylaxis.02 | Ask about known allergies and remove the cause if you can (for exam... | `anaphylaxis/02-ask-about-known-allergies-and.mp4` | `anaphylaxis/02-ask-about-known-allergies-and.webp` |
| [ ] | anaphylaxis.03 | Help them lie down. If they have trouble breathing, help them sit u... | `anaphylaxis/03-help-them-lie-down-if.mp4` | `anaphylaxis/03-help-them-lie-down-if.webp` |
| [ ] | anaphylaxis.04 | If they have an epinephrine (adrenaline) auto-injector, help them u... | `anaphylaxis/04-if-they-have-an-epinephrine.mp4` | `anaphylaxis/04-if-they-have-an-epinephrine.webp` |
| [ ] | anaphylaxis.05 | If there is no improvement in five to ten minutes and help has not... | `anaphylaxis/05-if-there-is-no-improvement.mp4` | `anaphylaxis/05-if-there-is-no-improvement.webp` |
| [ ] | anaphylaxis.06 | Keep checking responsiveness and breathing until help arrives. If t... | `anaphylaxis/06-keep-checking-responsiveness-and-breathing.mp4` | `anaphylaxis/06-keep-checking-responsiveness-and-breathing.webp` |
| [ ] | anaphylaxis.07 | If there is no auto-injector, call 108 immediately and keep them ly... | `anaphylaxis/07-if-there-is-no-autoinjector.mp4` | `anaphylaxis/07-if-there-is-no-autoinjector.webp` |

## Asthma attack (`asthma_attack`)
Used in 6 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | asthma_attack.01 | Help them sit comfortably and reassure them. Leaning forward and re... | `asthma_attack/01-help-them-sit-comfortably-and.mp4` | `asthma_attack/01-help-them-sit-comfortably-and.webp` |
| [ ] | asthma_attack.02 | Help them use their own inhaler. A spacer, if they have one, helps... | `asthma_attack/02-help-them-use-their-own.mp4` | `asthma_attack/02-help-them-use-their-own.webp` |
| [ ] | asthma_attack.03 | Move them away from triggers such as smoke or dust. If there is no... | `asthma_attack/03-move-them-away-from-triggers.mp4` | `asthma_attack/03-move-them-away-from-triggers.webp` |
| [ ] | asthma_attack.04 | Call 108 at once if: there is no inhaler and the attack lasts sever... | `asthma_attack/04-call-108-at-once-if.mp4` | `asthma_attack/04-call-108-at-once-if.webp` |
| [ ] | asthma_attack.05 | If you are trained and oxygen is available, give it as needed. | `asthma_attack/05-if-you-are-trained-and.mp4` | `asthma_attack/05-if-you-are-trained-and.webp` |
| [ ] | asthma_attack.06 | Stay with them. Help them follow their own doctor's instructions fo... | `asthma_attack/06-stay-with-them-help-them.mp4` | `asthma_attack/06-stay-with-them-help-them.webp` |

## Infection: when to see a doctor now (`infection_red_flags`)
Used in 6 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | infection_red_flags.01 | Most infections get better at home with rest, fluids and medicines. | `infection_red_flags/01-most-infections-get-better-at.mp4` | `infection_red_flags/01-most-infections-get-better-at.webp` |
| [ ] | infection_red_flags.02 | See a doctor immediately if there is confusion or unconsciousness,... | `infection_red_flags/02-see-a-doctor-immediately-if.mp4` | `infection_red_flags/02-see-a-doctor-immediately-if.webp` |
| [ ] | infection_red_flags.03 | Diabetics, people with low immunity (for example cancer or AIDS) an... | `infection_red_flags/03-diabetics-people-with-low-immunity.mp4` | `infection_red_flags/03-diabetics-people-with-low-immunity.webp` |

## Panic or anxiety (`panic_attack`)
Used in 6 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | panic_attack.01 | Introduce yourself if they do not know you. Tell them they are safe... | `panic_attack/01-introduce-yourself-if-they-do.mp4` | `panic_attack/01-introduce-yourself-if-they-do.webp` |
| [ ] | panic_attack.02 | Ask how you can help. Speak slowly, in short sentences, with a calm... | `panic_attack/02-ask-how-you-can-help.mp4` | `panic_attack/02-ask-how-you-can-help.webp` |
| [ ] | panic_attack.03 | Tell them what they feel is frightening but it will pass. Reassure... | `panic_attack/03-tell-them-what-they-feel.mp4` | `panic_attack/03-tell-them-what-they-feel.webp` |
| [ ] | panic_attack.04 | Show slow, even breaths and ask them to breathe with you. | `panic_attack/04-show-slow-even-breaths-and.mp4` | `panic_attack/04-show-slow-even-breaths-and.webp` |
| [ ] | panic_attack.05 | When their coping works, tell them they are doing well. If they ref... | `panic_attack/05-when-their-coping-works-tell.mp4` | `panic_attack/05-when-their-coping-works-tell.webp` |

## Recovery position (`recovery_position`)
Used in 6 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | recovery_position.01 | Roll the breathing person onto their side so the airway stays open.... | `recovery_position/01-roll-the-breathing-person-onto.mp4` | `recovery_position/01-roll-the-breathing-person-onto.webp` |
| [ ] | recovery_position.02 | Keep watching their breathing. If they stop breathing or you cannot... | `recovery_position/02-keep-watching-their-breathing-if.mp4` | `recovery_position/02-keep-watching-their-breathing-if.webp` |

## Chest or abdomen injury (`chest_abdomen_injury`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | chest_abdomen_injury.01 | Call 108. Help them lie down comfortably and watch them closely. | `chest_abdomen_injury/01-call-108-help-them-lie.mp4` | `chest_abdomen_injury/01-call-108-help-them-lie.webp` |
| [ ] | chest_abdomen_injury.02 | Abdomen: lying with the knees pulled up is usually most comfortable... | `chest_abdomen_injury/02-abdomen-lying-with-the-knees.mp4` | `chest_abdomen_injury/02-abdomen-lying-with-the-knees.webp` |
| [ ] | chest_abdomen_injury.03 | If internal organs are showing, do not push them back. Cover them w... | `chest_abdomen_injury/03-if-internal-organs-are-showing.mp4` | `chest_abdomen_injury/03-if-internal-organs-are-showing.webp` |
| [ ] | chest_abdomen_injury.04 | Chest: sit them up leaning toward the injured side, with one leg sl... | `chest_abdomen_injury/04-chest-sit-them-up-leaning.mp4` | `chest_abdomen_injury/04-chest-sit-them-up-leaning.webp` |
| [ ] | chest_abdomen_injury.05 | Reassure them and watch breathing, circulation and responsiveness,... | `chest_abdomen_injury/05-reassure-them-and-watch-breathing.mp4` | `chest_abdomen_injury/05-reassure-them-and-watch-breathing.webp` |

## Feeling faint or fainting (`fainting`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | fainting.01 | Help them sit or lie down somewhere safe where they cannot fall. | `fainting/01-help-them-sit-or-lie.mp4` | `fainting/01-help-them-sit-or-lie.webp` |
| [ ] | fainting.02 | Ask them to squat, or to cross their legs and tense the leg and but... | `fainting/02-ask-them-to-squat-or.mp4` | `fainting/02-ask-them-to-squat-or.webp` |
| [ ] | fainting.03 | Reassure them and watch their breathing and responsiveness. Ask why... | `fainting/03-reassure-them-and-watch-their.mp4` | `fainting/03-reassure-them-and-watch-their.webp` |
| [ ] | fainting.04 | If there is chest pain or a racing heartbeat, call 108. | `fainting/04-if-there-is-chest-pain.mp4` | `fainting/04-if-there-is-chest-pain.webp` |
| [ ] | fainting.05 | When they have recovered and can swallow, offer water. They should... | `fainting/05-when-they-have-recovered-and.mp4` | `fainting/05-when-they-have-recovered-and.webp` |
| [ ] | fainting.06 | If they fell, check for injuries. If they stay unresponsive, check... | `fainting/06-if-they-fell-check-for.mp4` | `fainting/06-if-they-fell-check-for.webp` |

## Head injury (`head_injury`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | head_injury.01 | Take them out of what they were doing and ask them to rest. | `head_injury/01-take-them-out-of-what.mp4` | `head_injury/01-take-them-out-of-what.webp` |
| [ ] | head_injury.02 | Watch for signs of concussion and for any change in how responsive... | `head_injury/02-watch-for-signs-of-concussion.mp4` | `head_injury/02-watch-for-signs-of-concussion.webp` |
| [ ] | head_injury.03 | If the injury is serious: call 108, keep the head and neck as still... | `head_injury/03-if-the-injury-is-serious.mp4` | `head_injury/03-if-the-injury-is-serious.webp` |
| [ ] | head_injury.04 | If it is mild, help them rest and treat small injuries. Keep watchi... | `head_injury/04-if-it-is-mild-help.mp4` | `head_injury/04-if-it-is-mild-help.webp` |

## Heart attack (`heart_attack`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | heart_attack.01 | Suspect a heart attack with chest pain, pressure or tightness, whic... | `heart_attack/01-suspect-a-heart-attack-with.mp4` | `heart_attack/01-suspect-a-heart-attack-with.webp` |
| [ ] | heart_attack.02 | Make them stop all activity and rest. Reassure them and keep them c... | `heart_attack/02-make-them-stop-all-activity.mp4` | `heart_attack/02-make-them-stop-all-activity.webp` |
| [ ] | heart_attack.03 | Call 108 now and ask for an ambulance with an AED. Do not wait to s... | `heart_attack/03-call-108-now-and-ask.mp4` | `heart_attack/03-call-108-now-and-ask.webp` |
| [ ] | heart_attack.04 | Trained providers only: chewable aspirin 325 mg may be given if the... | `heart_attack/04-trained-providers-only-chewable-aspirin.mp4` | `heart_attack/04-trained-providers-only-chewable-aspirin.webp` |
| [ ] | heart_attack.05 | If oxygen is available, give it. | `heart_attack/05-if-oxygen-is-available-give.mp4` | `heart_attack/05-if-oxygen-is-available-give.webp` |
| [ ] | heart_attack.06 | Stay with them. If they become unresponsive and you cannot find sig... | `heart_attack/06-stay-with-them-if-they.mp4` | `heart_attack/06-stay-with-them-if-they.webp` |
| [ ] | heart_attack.07 | Note the exact time the symptoms started and tell the ambulance team. | `heart_attack/07-note-the-exact-time-the.mp4` | `heart_attack/07-note-the-exact-time-the.webp` |
| [ ] | heart_attack.08 | Keep them lying flat for transport. Never take a heart attack patie... | `heart_attack/08-keep-them-lying-flat-for.mp4` | `heart_attack/08-keep-them-lying-flat-for.webp` |
| [ ] | heart_attack.09 | Keep them cool: use AC or a fan, open windows, and remove sweaters... | `heart_attack/09-keep-them-cool-use-ac.mp4` | `heart_attack/09-keep-them-cool-use-ac.webp` |
| [ ] | heart_attack.10 | Go to a hospital that can treat heart attacks (clot-dissolving medi... | `heart_attack/10-go-to-a-hospital-that.mp4` | `heart_attack/10-go-to-a-hospital-that.webp` |

## Low blood sugar (`low_blood_sugar`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | low_blood_sugar.01 | Suspect low sugar in a person on diabetes treatment who missed or d... | `low_blood_sugar/01-suspect-low-sugar-in-a.mp4` | `low_blood_sugar/01-suspect-low-sugar-in-a.webp` |
| [ ] | low_blood_sugar.02 | Signs: confusion, dizziness, anxiety, heavy sweating, blurred visio... | `low_blood_sugar/02-signs-confusion-dizziness-anxiety-heavy.mp4` | `low_blood_sugar/02-signs-confusion-dizziness-anxiety-heavy.webp` |
| [ ] | low_blood_sugar.03 | If you can, check blood sugar. Below about 70 mg/dl is low. | `low_blood_sugar/03-if-you-can-check-blood.mp4` | `low_blood_sugar/03-if-you-can-check-blood.webp` |
| [ ] | low_blood_sugar.04 | If they are awake and can swallow, give juice, sugar, sweets or cho... | `low_blood_sugar/04-if-they-are-awake-and.mp4` | `low_blood_sugar/04-if-they-are-awake-and.webp` |
| [ ] | low_blood_sugar.05 | Recheck the sugar. If it is still low, repeat until they improve. | `low_blood_sugar/05-recheck-the-sugar-if-it.mp4` | `low_blood_sugar/05-recheck-the-sugar-if-it.webp` |
| [ ] | low_blood_sugar.06 | Stop insulin and diabetes tablets until a doctor has seen them. If... | `low_blood_sugar/06-stop-insulin-and-diabetes-tablets.mp4` | `low_blood_sugar/06-stop-insulin-and-diabetes-tablets.webp` |
| [ ] | low_blood_sugar.07 | If they are drowsy or unconscious: give nothing by mouth. Get them... | `low_blood_sugar/07-if-they-are-drowsy-or.mp4` | `low_blood_sugar/07-if-they-are-drowsy-or.webp` |
| [ ] | low_blood_sugar.08 | Trained personnel, including in an ambulance, can give glucose by I... | `low_blood_sugar/08-trained-personnel-including-in-an.mp4` | `low_blood_sugar/08-trained-personnel-including-in-an.webp` |

## Poisoning (`poisoning`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | poisoning.01 | Stop or reduce further contact with the poison. If it is toxic gas,... | `poisoning/01-stop-or-reduce-further-contact.mp4` | `poisoning/01-stop-or-reduce-further-contact.webp` |
| [ ] | poisoning.02 | Find out what the substance is, how much, and when. Only touch the... | `poisoning/02-find-out-what-the-substance.mp4` | `poisoning/02-find-out-what-the-substance.webp` |
| [ ] | poisoning.03 | Call 108 or a poison control centre. Tell them everything you know... | `poisoning/03-call-108-or-a-poison.mp4` | `poisoning/03-call-108-or-a-poison.webp` |
| [ ] | poisoning.04 | If possible, help them lie on their left side. Watch their breathin... | `poisoning/04-if-possible-help-them-lie.mp4` | `poisoning/04-if-possible-help-them-lie.webp` |
| [ ] | poisoning.05 | Keep any bottles, packets or labels to give to the ambulance team. | `poisoning/05-keep-any-bottles-packets-or.mp4` | `poisoning/05-keep-any-bottles-packets-or.webp` |
| [ ] | poisoning.06 | If they vomit while lying down, turn them on their side so they do... | `poisoning/06-if-they-vomit-while-lying.mp4` | `poisoning/06-if-they-vomit-while-lying.webp` |
| [ ] | poisoning.07 | Wear gloves or a mask if a harmful substance is suspected. If a har... | `poisoning/07-wear-gloves-or-a-mask.mp4` | `poisoning/07-wear-gloves-or-a-mask.webp` |

## Stroke (`stroke`)
Used in 5 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | stroke.01 | Suspect a stroke if there are sudden balance problems or dizziness,... | `stroke/01-suspect-a-stroke-if-there.mp4` | `stroke/01-suspect-a-stroke-if-there.webp` |
| [ ] | stroke.02 | Check: ask them to walk (balance), smile (does the mouth droop?), l... | `stroke/02-check-ask-them-to-walk.mp4` | `stroke/02-check-ask-them-to-walk.webp` |
| [ ] | stroke.03 | Do not waste time. Call 108 and go straight to a hospital with CT s... | `stroke/03-do-not-waste-time-call.mp4` | `stroke/03-do-not-waste-time-call.webp` |
| [ ] | stroke.04 | Do NOT give aspirin or any medicine at home. Some strokes are cause... | `stroke/04-do-not-give-aspirin-or.mp4` | `stroke/04-do-not-give-aspirin-or.webp` |
| [ ] | stroke.05 | Check blood sugar if you can. Low sugar can look like a stroke and... | `stroke/05-check-blood-sugar-if-you.mp4` | `stroke/05-check-blood-sugar-if-you.webp` |
| [ ] | stroke.06 | Note the exact time the symptoms began. Clot-dissolving treatment w... | `stroke/06-note-the-exact-time-the.mp4` | `stroke/06-note-the-exact-time-the.webp` |
| [ ] | stroke.07 | If they become unresponsive and show no signs of life, start CPR. | `stroke/07-if-they-become-unresponsive-and.mp4` | `stroke/07-if-they-become-unresponsive-and.webp` |

## Amputation (`amputation`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | amputation.01 | Call 108. | `amputation/01-call-108.mp4` | `amputation/01-call-108.webp` |
| [ ] | amputation.02 | Stop heavy bleeding by pressing on the wound. | `amputation/02-stop-heavy-bleeding-by-pressing.mp4` | `amputation/02-stop-heavy-bleeding-by-pressing.webp` |
| [ ] | amputation.03 | Partial amputation: keep the limb as still as possible, in normal a... | `amputation/03-partial-amputation-keep-the-limb.mp4` | `amputation/03-partial-amputation-keep-the-limb.webp` |
| [ ] | amputation.04 | Complete amputation: cover the wound with a clean cloth. Keep the s... | `amputation/04-complete-amputation-cover-the-wound.mp4` | `amputation/04-complete-amputation-cover-the-wound.webp` |
| [ ] | amputation.05 | Keep the person still, reassure them, and watch for shock. | `amputation/05-keep-the-person-still-reassure.mp4` | `amputation/05-keep-the-person-still-reassure.webp` |

## Choking: adult and child (awake) (`choking_adult_child`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | choking_adult_child.01 | A person clutching their throat, unable to talk, cough or breathe,... | `choking_adult_child/01-a-person-clutching-their-throat.mp4` | `choking_adult_child/01-a-person-clutching-their-throat.webp` |
| [ ] | choking_adult_child.02 | If they can cough, encourage a forceful cough and let them lean for... | `choking_adult_child/02-if-they-can-cough-encourage.mp4` | `choking_adult_child/02-if-they-can-cough-encourage.webp` |
| [ ] | choking_adult_child.03 | Help with back slaps: stand to one side, bend them forward, support... | `choking_adult_child/03-help-with-back-slaps-stand.mp4` | `choking_adult_child/03-help-with-back-slaps-stand.webp` |
| [ ] | choking_adult_child.04 | If coughing does not clear it, or they cannot cough, give 5 abdomin... | `choking_adult_child/04-if-coughing-does-not-clear.mp4` | `choking_adult_child/04-if-coughing-does-not-clear.webp` |
| [ ] | choking_adult_child.05 | Heimlich: stand behind them with one leg between theirs and your ar... | `choking_adult_child/05-heimlich-stand-behind-them-with.mp4` | `choking_adult_child/05-heimlich-stand-behind-them-with.webp` |
| [ ] | choking_adult_child.06 | Alternate 5 abdominal thrusts with 5 back slaps until it comes out... | `choking_adult_child/06-alternate-5-abdominal-thrusts-with.mp4` | `choking_adult_child/06-alternate-5-abdominal-thrusts-with.webp` |
| [ ] | choking_adult_child.07 | If they become unresponsive: call for help, ask for an AED, and sta... | `choking_adult_child/07-if-they-become-unresponsive-call.mp4` | `choking_adult_child/07-if-they-become-unresponsive-call.webp` |

## Choking: special cases (`choking_special_cases`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | choking_special_cases.01 | Pregnant woman: no abdominal thrusts. Put your hands higher, over t... | `choking_special_cases/01-pregnant-woman-no-abdominal-thrusts.mp4` | `choking_special_cases/01-pregnant-woman-no-abdominal-thrusts.webp` |
| [ ] | choking_special_cases.02 | Person taller than you: ask them to spread their legs wider, or sta... | `choking_special_cases/02-person-taller-than-you-ask.mp4` | `choking_special_cases/02-person-taller-than-you-ask.webp` |
| [ ] | choking_special_cases.03 | Small child or toddler: kneel behind them, or place the child on a... | `choking_special_cases/03-small-child-or-toddler-kneel.mp4` | `choking_special_cases/03-small-child-or-toddler-kneel.webp` |

## CPR: child and infant (`cpr_child_infant`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | cpr_child_infant.01 | Start chest compressions straight away if a child or baby is unresp... | `cpr_child_infant/01-start-chest-compressions-straight-away.mp4` | `cpr_child_infant/01-start-chest-compressions-straight-away.webp` |
| [ ] | cpr_child_infant.02 | Press on the lower half of the breastbone, one-third of the chest d... | `cpr_child_infant/02-press-on-the-lower-half.mp4` | `cpr_child_infant/02-press-on-the-lower-half.webp` |
| [ ] | cpr_child_infant.03 | Child: one hand may be enough. If one hand reaches one-third depth,... | `cpr_child_infant/03-child-one-hand-may-be.mp4` | `cpr_child_infant/03-child-one-hand-may-be.webp` |
| [ ] | cpr_child_infant.04 | Baby: use two fingers of one hand if you are alone, or the two-thum... | `cpr_child_infant/04-baby-use-two-fingers-of.mp4` | `cpr_child_infant/04-baby-use-two-fingers-of.webp` |
| [ ] | cpr_child_infant.05 | Press at about 120 compressions a minute for babies. | `cpr_child_infant/05-press-at-about-120-compressions.mp4` | `cpr_child_infant/05-press-at-about-120-compressions.webp` |
| [ ] | cpr_child_infant.06 | Baby pulse: feel on the inner side of the upper arm, just above the... | `cpr_child_infant/06-baby-pulse-feel-on-the.mp4` | `cpr_child_infant/06-baby-pulse-feel-on-the.webp` |
| [ ] | cpr_child_infant.07 | If you are trained and no pulse is felt after the first compression... | `cpr_child_infant/07-if-you-are-trained-and.mp4` | `cpr_child_infant/07-if-you-are-trained-and.webp` |

## Electric shock (`electric_shock`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | electric_shock.01 | Do not touch the person until the power is off. Switch off the supp... | `electric_shock/01-do-not-touch-the-person.mp4` | `electric_shock/01-do-not-touch-the-person.webp` |
| [ ] | electric_shock.02 | Check responsiveness and signs of life. Electric shock and lightnin... | `electric_shock/02-check-responsiveness-and-signs-of.mp4` | `electric_shock/02-check-responsiveness-and-signs-of.webp` |
| [ ] | electric_shock.03 | Cover burns with a clean cloth. Electrical burns can be life-threat... | `electric_shock/03-cover-burns-with-a-clean.mp4` | `electric_shock/03-cover-burns-with-a-clean.webp` |

## Emergency childbirth (`emergency_childbirth`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | emergency_childbirth.01 | Call 108 or a midwife and follow their instructions. Make a private... | `emergency_childbirth/01-call-108-or-a-midwife.mp4` | `emergency_childbirth/01-call-108-or-a-midwife.webp` |
| [ ] | emergency_childbirth.02 | When the baby is about to be born, help her find a comfortable posi... | `emergency_childbirth/02-when-the-baby-is-about.mp4` | `emergency_childbirth/02-when-the-baby-is-about.webp` |
| [ ] | emergency_childbirth.03 | Support the baby's head as it comes out. Do not pull on the head or... | `emergency_childbirth/03-support-the-babys-head-as.mp4` | `emergency_childbirth/03-support-the-babys-head-as.webp` |
| [ ] | emergency_childbirth.04 | If the cord is around the neck, gently ease it over the head. Do no... | `emergency_childbirth/04-if-the-cord-is-around.mp4` | `emergency_childbirth/04-if-the-cord-is-around.webp` |
| [ ] | emergency_childbirth.05 | Dry the baby, wrap in a clean cloth, cover the head, and place the... | `emergency_childbirth/05-dry-the-baby-wrap-in.mp4` | `emergency_childbirth/05-dry-the-baby-wrap-in.webp` |
| [ ] | emergency_childbirth.06 | Do not cut the cord. Do not push on her stomach. The afterbirth usu... | `emergency_childbirth/06-do-not-cut-the-cord.mp4` | `emergency_childbirth/06-do-not-cut-the-cord.webp` |
| [ ] | emergency_childbirth.07 | If bleeding is severe, help her lie down, keep her warm and treat a... | `emergency_childbirth/07-if-bleeding-is-severe-help.mp4` | `emergency_childbirth/07-if-bleeding-is-severe-help.webp` |
| [ ] | emergency_childbirth.08 | If the baby is not responding and breathing abnormally, open the ai... | `emergency_childbirth/08-if-the-baby-is-not.mp4` | `emergency_childbirth/08-if-the-baby-is-not.webp` |

## Hazard: snake nearby (`hazard_animal_snake`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_animal_snake.01 | Keep away from the snake. Do not try to catch it. | `hazard_animal_snake/01-keep-away-from-the-snake.mp4` | `hazard_animal_snake/01-keep-away-from-the-snake.webp` |
| [ ] | hazard_animal_snake.02 | Move the person calmly away from the snake. | `hazard_animal_snake/02-move-the-person-calmly-away.mp4` | `hazard_animal_snake/02-move-the-person-calmly-away.webp` |

## Insect bite or sting (`insect_sting`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | insect_sting.01 | If a bee stinger is left in the skin, remove it quickly by gently s... | `insect_sting/01-if-a-bee-stinger-is.mp4` | `insect_sting/01-if-a-bee-stinger-is.webp` |
| [ ] | insect_sting.02 | A tick should be pulled out with fine tweezers or a tick remover, c... | `insect_sting/02-a-tick-should-be-pulled.mp4` | `insect_sting/02-a-tick-should-be-pulled.webp` |
| [ ] | insect_sting.03 | Wash the area with clean water, then use an antiseptic. | `insect_sting/03-wash-the-area-with-clean.mp4` | `insect_sting/03-wash-the-area-with-clean.webp` |
| [ ] | insect_sting.04 | Watch for a severe allergic reaction. If swelling of the face, mout... | `insect_sting/04-watch-for-a-severe-allergic.mp4` | `insect_sting/04-watch-for-a-severe-allergic.webp` |
| [ ] | insect_sting.05 | Try not to scratch. If it gets redder, more painful or warm after a... | `insect_sting/05-try-not-to-scratch-if.mp4` | `insect_sting/05-try-not-to-scratch-if.webp` |

## Scorpion sting (`scorpion_sting`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | scorpion_sting.01 | Move away from where the scorpion is. Do not try to catch or kill i... | `scorpion_sting/01-move-away-from-where-the.mp4` | `scorpion_sting/01-move-away-from-where-the.webp` |
| [ ] | scorpion_sting.02 | Keep the person calm and still. Let them sit or lie down comfortably. | `scorpion_sting/02-keep-the-person-calm-and.mp4` | `scorpion_sting/02-keep-the-person-calm-and.webp` |
| [ ] | scorpion_sting.03 | Gently wash the sting with soap and clean water. Take off rings or... | `scorpion_sting/03-gently-wash-the-sting-with.mp4` | `scorpion_sting/03-gently-wash-the-sting-with.webp` |
| [ ] | scorpion_sting.04 | A cool wet cloth, or an ice pack wrapped in cloth, on the sting may... | `scorpion_sting/04-a-cool-wet-cloth-or.mp4` | `scorpion_sting/04-a-cool-wet-cloth-or.webp` |
| [ ] | scorpion_sting.05 | Do NOT cut the wound, suck it, or tie a tight band above it. Do not... | `scorpion_sting/05-do-not-cut-the-wound.mp4` | `scorpion_sting/05-do-not-cut-the-wound.webp` |
| [ ] | scorpion_sting.06 | Go to a hospital. Go urgently, and call 108, for a child, an older... | `scorpion_sting/06-go-to-a-hospital-go.mp4` | `scorpion_sting/06-go-to-a-hospital-go.webp` |
| [ ] | scorpion_sting.07 | Note the time of the sting and the symptoms, and tell the doctor. | `scorpion_sting/07-note-the-time-of-the.mp4` | `scorpion_sting/07-note-the-time-of-the.webp` |

## Snake bite (`snake_bite`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | snake_bite.01 | Keep away from the snake. Do not try to catch it. | `snake_bite/01-keep-away-from-the-snake.mp4` | `snake_bite/01-keep-away-from-the-snake.webp` |
| [ ] | snake_bite.02 | Reassure the person and keep them calm and still. Most bites do not... | `snake_bite/02-reassure-the-person-and-keep.mp4` | `snake_bite/02-reassure-the-person-and-keep.webp` |
| [ ] | snake_bite.03 | Immobilise the limb and the person. Splint the bitten limb like a f... | `snake_bite/03-immobilise-the-limb-and-the.mp4` | `snake_bite/03-immobilise-the-limb-and-the.webp` |
| [ ] | snake_bite.04 | Take off shoes, rings, watches, jewellery and tight clothing from t... | `snake_bite/04-take-off-shoes-rings-watches.mp4` | `snake_bite/04-take-off-shoes-rings-watches.webp` |
| [ ] | snake_bite.05 | Do NOT cut, suck, wash, rub or put anything on the wound. | `snake_bite/05-do-not-cut-suck-wash.mp4` | `snake_bite/05-do-not-cut-suck-wash.webp` |
| [ ] | snake_bite.06 | The person must not run or drive to the hospital. Use an ambulance... | `snake_bite/06-the-person-must-not-run.mp4` | `snake_bite/06-the-person-must-not-run.webp` |
| [ ] | snake_bite.07 | Get to a hospital immediately. Traditional remedies have no proven... | `snake_bite/07-get-to-a-hospital-immediately.mp4` | `snake_bite/07-get-to-a-hospital-immediately.webp` |
| [ ] | snake_bite.08 | Tell the doctor about symptoms: pain, weakness, bleeding, blurred v... | `snake_bite/08-tell-the-doctor-about-symptoms.mp4` | `snake_bite/08-tell-the-doctor-about-symptoms.webp` |
| [ ] | snake_bite.09 | If it is safe, a photo of the snake from a distance can help the do... | `snake_bite/09-if-it-is-safe-a.mp4` | `snake_bite/09-if-it-is-safe-a.webp` |

## Minor wound care (`wound_care_minor`)
Used in 4 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | wound_care_minor.01 | Wash the wound with clean water and soap. Do not put anything on it. | `wound_care_minor/01-wash-the-wound-with-clean.mp4` | `wound_care_minor/01-wash-the-wound-with-clean.webp` |
| [ ] | wound_care_minor.02 | Cover it with a clean bandage, or a clean cloth if you have no band... | `wound_care_minor/02-cover-it-with-a-clean.mp4` | `wound_care_minor/02-cover-it-with-a-clean.webp` |

## Animal bite (dog, cat, other animals) (`animal_bite`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | animal_bite.01 | Wash the wound straight away with soap and warm water, then rinse u... | `animal_bite/01-wash-the-wound-straight-away.mp4` | `animal_bite/01-wash-the-wound-straight-away.webp` |
| [ ] | animal_bite.02 | Caregivers must not touch the wound with bare hands. | `animal_bite/02-caregivers-must-not-touch-the.mp4` | `animal_bite/02-caregivers-must-not-touch-the.webp` |
| [ ] | animal_bite.03 | Apply antibiotic ointment or a disinfectant such as iodine. | `animal_bite/03-apply-antibiotic-ointment-or-a.mp4` | `animal_bite/03-apply-antibiotic-ointment-or-a.webp` |
| [ ] | animal_bite.04 | Go to the nearest health centre as soon as possible for rabies and... | `animal_bite/04-go-to-the-nearest-health.mp4` | `animal_bite/04-go-to-the-nearest-health.webp` |

## Choking: if you are alone (`choking_self`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | choking_self.01 | If you can cough, lean forward and cough hard until it comes out. | `choking_self/01-if-you-can-cough-lean.mp4` | `choking_self/01-if-you-can-cough-lean.webp` |
| [ ] | choking_self.02 | If you cannot cough, lean over a firm edge such as a chair back, co... | `choking_self/02-if-you-cannot-cough-lean.mp4` | `choking_self/02-if-you-cannot-cough-lean.webp` |
| [ ] | choking_self.03 | Put your fists between your navel and the lower end of your breastb... | `choking_self/03-put-your-fists-between-your.mp4` | `choking_self/03-put-your-fists-between-your.webp` |

## Fever (`fever`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | fever.01 | Rest and dress lightly. | `fever/01-rest-and-dress-lightly.mp4` | `fever/01-rest-and-dress-lightly.webp` |
| [ ] | fever.02 | Drink fluids to replace what is lost by sweating. | `fever/02-drink-fluids-to-replace-what.mp4` | `fever/02-drink-fluids-to-replace-what.webp` |
| [ ] | fever.03 | If they feel unwell, the usual dose of paracetamol can be given. Sp... | `fever/03-if-they-feel-unwell-the.mp4` | `fever/03-if-they-feel-unwell-the.webp` |
| [ ] | fever.04 | Watch for new symptoms. | `fever/04-watch-for-new-symptoms.mp4` | `fever/04-watch-for-new-symptoms.webp` |

## Hazard: water (reach, throw, don't go) (`hazard_water`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_water.01 | Do not enter the water unless you are trained. Rescuers who are not... | `hazard_water/01-do-not-enter-the-water.mp4` | `hazard_water/01-do-not-enter-the-water.webp` |
| [ ] | hazard_water.02 | Rescue from land: reach with a pole, or throw a rope or a floating... | `hazard_water/02-rescue-from-land-reach-with.mp4` | `hazard_water/02-rescue-from-land-reach-with.webp` |
| [ ] | hazard_water.03 | Only once the person is out of the water and the area is safe, star... | `hazard_water/03-only-once-the-person-is.mp4` | `hazard_water/03-only-once-the-person-is.webp` |

## High blood sugar (`high_blood_sugar`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | high_blood_sugar.01 | Suspect it in a known diabetic who urinates a lot, is very thirsty,... | `high_blood_sugar/01-suspect-it-in-a-known.mp4` | `high_blood_sugar/01-suspect-it-in-a-known.webp` |
| [ ] | high_blood_sugar.02 | If they are awake, encourage them to drink plenty of water. | `high_blood_sugar/02-if-they-are-awake-encourage.mp4` | `high_blood_sugar/02-if-they-are-awake-encourage.webp` |
| [ ] | high_blood_sugar.03 | See a doctor immediately. High sugar can become life-threatening (d... | `high_blood_sugar/03-see-a-doctor-immediately-high.mp4` | `high_blood_sugar/03-see-a-doctor-immediately-high.webp` |

## Hypothermia (cold) (`hypothermia`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hypothermia.01 | Take them out of the cold or protect them from further cooling. | `hypothermia/01-take-them-out-of-the.mp4` | `hypothermia/01-take-them-out-of-the.webp` |
| [ ] | hypothermia.02 | Remove wet clothes if you can, dry them gently and cover them well. | `hypothermia/02-remove-wet-clothes-if-you.mp4` | `hypothermia/02-remove-wet-clothes-if-you.webp` |
| [ ] | hypothermia.03 | If they are awake and shivering, wrap them in blankets. If they can... | `hypothermia/03-if-they-are-awake-and.mp4` | `hypothermia/03-if-they-are-awake-and.webp` |
| [ ] | hypothermia.04 | If they are drowsy or not shivering, warm them gradually with hot w... | `hypothermia/04-if-they-are-drowsy-or.mp4` | `hypothermia/04-if-they-are-drowsy-or.webp` |
| [ ] | hypothermia.05 | Reassure them and watch their breathing and responsiveness. Call 10... | `hypothermia/05-reassure-them-and-watch-their.mp4` | `hypothermia/05-reassure-them-and-watch-their.webp` |

## Nosebleed (`nosebleed`)
Used in 3 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | nosebleed.01 | Sit down and lean the head slightly forward. Pinch the soft part of... | `nosebleed/01-sit-down-and-lean-the.mp4` | `nosebleed/01-sit-down-and-lean-the.webp` |
| [ ] | nosebleed.02 | If it is still bleeding after 15 minutes, or they feel light-headed... | `nosebleed/02-if-it-is-still-bleeding.mp4` | `nosebleed/02-if-it-is-still-bleeding.webp` |
| [ ] | nosebleed.03 | If it followed an injury and there are signs of brain injury, a ben... | `nosebleed/03-if-it-followed-an-injury.mp4` | `nosebleed/03-if-it-followed-an-injury.webp` |

## Choking: infant (`choking_infant`)
Used in 2 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | choking_infant.01 | A baby who suddenly cannot cry, cough or breathe, drools, or turns... | `choking_infant/01-a-baby-who-suddenly-cannot.mp4` | `choking_infant/01-a-baby-who-suddenly-cannot.webp` |
| [ ] | choking_infant.02 | If you can see the object, hook it out with a finger. NEVER do blin... | `choking_infant/02-if-you-can-see-the.mp4` | `choking_infant/02-if-you-can-see-the.webp` |
| [ ] | choking_infant.03 | If it is not visible and the baby is awake, alternate 5 back blows... | `choking_infant/03-if-it-is-not-visible.mp4` | `choking_infant/03-if-it-is-not-visible.webp` |
| [ ] | choking_infant.04 | Back blows: sit down, rest the baby face-down along your thigh with... | `choking_infant/04-back-blows-sit-down-rest.mp4` | `choking_infant/04-back-blows-sit-down-rest.webp` |
| [ ] | choking_infant.05 | Chest thrusts: turn the baby over and press the lower half of the b... | `choking_infant/05-chest-thrusts-turn-the-baby.mp4` | `choking_infant/05-chest-thrusts-turn-the-baby.webp` |
| [ ] | choking_infant.06 | Repeat until the baby coughs, cries or breathes, or becomes unrespo... | `choking_infant/06-repeat-until-the-baby-coughs.mp4` | `choking_infant/06-repeat-until-the-baby-coughs.webp` |
| [ ] | choking_infant.07 | If the baby becomes unresponsive: call for help and start infant ch... | `choking_infant/07-if-the-baby-becomes-unresponsive.mp4` | `choking_infant/07-if-the-baby-becomes-unresponsive.webp` |

## Drowning (`drowning`)
Used in 2 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | drowning.01 | Once the person is out of the water and the area is safe, check res... | `drowning/01-once-the-person-is-out.mp4` | `drowning/01-once-the-person-is-out.webp` |
| [ ] | drowning.02 | Cover your face and theirs, look for chest rise and, if trained, fe... | `drowning/02-cover-your-face-and-theirs.mp4` | `drowning/02-cover-your-face-and-theirs.webp` |
| [ ] | drowning.03 | If they are breathing: place them in the recovery position and warm... | `drowning/03-if-they-are-breathing-place.mp4` | `drowning/03-if-they-are-breathing-place.webp` |
| [ ] | drowning.04 | If they are not breathing: drowning arrests are caused by lack of o... | `drowning/04-if-they-are-not-breathing.mp4` | `drowning/04-if-they-are-not-breathing.webp` |
| [ ] | drowning.05 | Then 30 compressions to 2 breaths for an adult, 15 to 2 for a child... | `drowning/05-then-30-compressions-to-2.mp4` | `drowning/05-then-30-compressions-to-2.webp` |
| [ ] | drowning.06 | Use an AED if there is one, but do not let it delay breaths or comp... | `drowning/06-use-an-aed-if-there.mp4` | `drowning/06-use-an-aed-if-there.webp` |
| [ ] | drowning.07 | In cold water the person may be hypothermic. Warm them with blanket... | `drowning/07-in-cold-water-the-person.mp4` | `drowning/07-in-cold-water-the-person.webp` |
| [ ] | drowning.08 | Do not routinely immobilise the neck. Do it only if there was divin... | `drowning/08-do-not-routinely-immobilise-the.mp4` | `drowning/08-do-not-routinely-immobilise-the.webp` |
| [ ] | drowning.09 | Anyone who needed rescue breaths or CPR must go to a hospital, even... | `drowning/09-anyone-who-needed-rescue-breaths.mp4` | `drowning/09-anyone-who-needed-rescue-breaths.webp` |

## Helmet removal (`helmet_removal`)
Used in 2 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | helmet_removal.01 | If the person is unconscious or has signs of spinal injury (numbnes... | `helmet_removal/01-if-the-person-is-unconscious.mp4` | `helmet_removal/01-if-the-person-is-unconscious.webp` |
| [ ] | helmet_removal.02 | If they are conscious, tell them you will remove the helmet and ask... | `helmet_removal/02-if-they-are-conscious-tell.mp4` | `helmet_removal/02-if-they-are-conscious-tell.webp` |
| [ ] | helmet_removal.03 | Person 1 kneels at the head and holds the helmet on both sides with... | `helmet_removal/03-person-1-kneels-at-the.mp4` | `helmet_removal/03-person-1-kneels-at-the.webp` |
| [ ] | helmet_removal.04 | Person 2, at the side, undoes or cuts the strap. | `helmet_removal/04-person-2-at-the-side.mp4` | `helmet_removal/04-person-2-at-the-side.webp` |
| [ ] | helmet_removal.05 | Person 2 then holds the neck: one hand behind the neck and the back... | `helmet_removal/05-person-2-then-holds-the.mp4` | `helmet_removal/05-person-2-then-holds-the.webp` |
| [ ] | helmet_removal.06 | Full-face helmet: remove glasses first. | `helmet_removal/06-fullface-helmet-remove-glasses-first.mp4` | `helmet_removal/06-fullface-helmet-remove-glasses-first.webp` |
| [ ] | helmet_removal.07 | Person 1 gently widens the helmet sideways to clear the ears, tilts... | `helmet_removal/07-person-1-gently-widens-the.mp4` | `helmet_removal/07-person-1-gently-widens-the.webp` |
| [ ] | helmet_removal.08 | Person 1 takes over holding the neck in a neutral position once the... | `helmet_removal/08-person-1-takes-over-holding.mp4` | `helmet_removal/08-person-1-takes-over-holding.webp` |

## Car accident: patient placement (`car_patient_placement`)
Used in 1 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | car_patient_placement.01 | Do not move the person unless there is immediate danger (fire, traf... | `car_patient_placement/01-do-not-move-the-person.mp4` | `car_patient_placement/01-do-not-move-the-person.webp` |
| [ ] | car_patient_placement.02 | If you must move them, support the head and neck in a neutral posit... | `car_patient_placement/02-if-you-must-move-them.mp4` | `car_patient_placement/02-if-you-must-move-them.webp` |
| [ ] | car_patient_placement.03 | If there is no danger, keep them still in the seat and hold the hea... | `car_patient_placement/03-if-there-is-no-danger.mp4` | `car_patient_placement/03-if-there-is-no-danger.webp` |
| [ ] | car_patient_placement.04 | To lay them down, use the log-roll technique with a spine board, ke... | `car_patient_placement/04-to-lay-them-down-use.mp4` | `car_patient_placement/04-to-lay-them-down-use.webp` |

## Hazard: fire and smoke (`hazard_fire_smoke`)
Used in 1 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_fire_smoke.01 | Do not open doors and windows: fresh air makes the fire stronger. | `hazard_fire_smoke/01-do-not-open-doors-and.mp4` | `hazard_fire_smoke/01-do-not-open-doors-and.webp` |
| [ ] | hazard_fire_smoke.02 | Hold a wet cloth or tissue over your face and crawl along the floor... | `hazard_fire_smoke/02-hold-a-wet-cloth-or.mp4` | `hazard_fire_smoke/02-hold-a-wet-cloth-or.webp` |
| [ ] | hazard_fire_smoke.03 | Switch off the power supply and remove any live electrical wire. | `hazard_fire_smoke/03-switch-off-the-power-supply.mp4` | `hazard_fire_smoke/03-switch-off-the-power-supply.webp` |
| [ ] | hazard_fire_smoke.04 | If the person is on fire, wrap them in a heavy blanket and roll the... | `hazard_fire_smoke/04-if-the-person-is-on.mp4` | `hazard_fire_smoke/04-if-the-person-is-on.webp` |
| [ ] | hazard_fire_smoke.05 | Never ignore fire hazards. | `hazard_fire_smoke/05-never-ignore-fire-hazards.mp4` | `hazard_fire_smoke/05-never-ignore-fire-hazards.webp` |

## Hazard: railway (`hazard_railway`)
Used in 1 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_railway.01 | Stay off the tracks. Trains can approach fast and quietly. | `hazard_railway/01-stay-off-the-tracks-trains.mp4` | `hazard_railway/01-stay-off-the-tracks-trains.webp` |
| [ ] | hazard_railway.02 | Move the patient away from the tracks only if it is safe, and call... | `hazard_railway/02-move-the-patient-away-from.mp4` | `hazard_railway/02-move-the-patient-away-from.webp` |

## Hazard: live electrical wires (`hazard_electric`)
Used in 0 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | hazard_electric.01 | Do not touch the person until the power is off. Switch off the supp... | `hazard_electric/01-do-not-touch-the-person.mp4` | `hazard_electric/01-do-not-touch-the-person.webp` |
| [ ] | hazard_electric.02 | Look for live wires and sparks before you approach. | `hazard_electric/02-look-for-live-wires-and.mp4` | `hazard_electric/02-look-for-live-wires-and.webp` |

## Rescue breaths (trained responders) (`rescue_breaths`)
Used in 0 scenarios.

| Done | Step | What it shows | Video file | Image file |
|---|---|---|---|---|
| [ ] | rescue_breaths.01 | If you are trained, give 2 rescue breaths with a pocket mask, bag v... | `rescue_breaths/01-if-you-are-trained-give.mp4` | `rescue_breaths/01-if-you-are-trained-give.webp` |
| [ ] | rescue_breaths.02 | Then continue 30 compressions to 2 breaths for an adult, or 15 to 2... | `rescue_breaths/02-then-continue-30-compressions-to.mp4` | `rescue_breaths/02-then-continue-30-compressions-to.webp` |
| [ ] | rescue_breaths.03 | Pulse present but not breathing: assist the breathing with a bag va... | `rescue_breaths/03-pulse-present-but-not-breathing.mp4` | `rescue_breaths/03-pulse-present-but-not-breathing.webp` |
