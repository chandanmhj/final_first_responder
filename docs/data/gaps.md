# Guideline data gaps

Found while building scenarios from the handbook. Nothing below has been invented: each item is either missing from the
handbook, unclear, or inconsistent. You decide how to fill each one (add a source, approve a draft, or drop the scenario).

## A. Missing topics (no handbook coverage, so no scenario was written)
| # | Topic | Why it matters |
|---|---|---|
| 1 | **Scorpion, spider, bee or wasp sting** | Needed for your photo feature (venomous or not). The handbook has no content on them. |
| 2 | **Venomous animal identification** | The handbook only shows pictures of cobra, krait and viper. No identifying features, no non-venomous species, no scorpions. A licensed reference image set is needed to build and test the photo feature. |
| 3 | Poisoning (pesticide, overdose, alcohol) | Only mentioned as a cause and "do not touch pesticides with bare hands". |
| 4 | Allergic reaction and anaphylaxis | Not covered. |
| 5 | Asthma and breathing difficulty | Only listed as a warning sign. |
| 6 | Fainting | Not covered. |
| 7 | Heat stroke and hypothermia (non-drowning) | Hypothermia appears only inside drowning. |
| 8 | Head injury, chest, abdominal and eye injuries, nosebleed | Not covered. |
| 9 | Chemical burns, smoke inhalation | The handbook mentions chemicals and face burns only briefly. |
| 10 | Childbirth and newborn emergencies | The Trust teaches them, but this handbook does not include them. |
| 11 | Mental health emergencies | Same. |
| 12 | Gas leak or carbon monoxide, lightning | Mentioned as hazards only. |
| 13 | Fever and dehydration care at home (ORS) | Only red flags are listed. |

## B. Unclear or incomplete content (scenarios exist but need your input)
| # | Where | Problem |
|---|---|---|
| 14 | Recovery position | Shown as a figure only, no written steps. The module uses an adapted description. |
| 15 | Helmet removal | A figure reference is unresolved ("Figure xxx"). No rule for **when** to remove a helmet, and none for an unconscious rider who is not breathing (airway and CPR). Scenario `road_not_breathing_bike` depends on this. |
| 16 | Car accident | No text on moving a person from a car, seat belts, airbags or vehicle fire. The `car_patient_placement` module is adapted and partly extension. |
| 17 | Road scene safety | Only general hazards are listed (traffic). Warning other drivers and stopping engines are adapted, not from the handbook. |
| 18 | Snake bite | No guidance on antivenom or which hospital. The venom statistics on the same page are inconsistent, so the app does not quote them. |
| 19 | Drowning | Page 28 says a trained rescuer gives 2 rescue breaths first; page 29 says a single rescuer should do compression-only without pausing for breaths. The module states both and needs your or an expert's ruling. |
| 20 | Age definitions | "Child" and "infant" are not defined by age. The app needs a cut-off to choose adult, child or infant CPR. |
| 21 | AED for children | No guidance on child pads or settings. |
| 22 | Medicines | The handbook lists medicines for heart attack for clinicians (aspirin 325 mg, others). The app shows them to **trained first responders only**, pending your decision. |
| 23 | Tourniquet | No instruction to note the application time, how long it may stay, or placement near a joint. The time note is adapted for the handover report. |
| 24 | Seizure | No guidance for children (febrile seizures) or pregnancy. |
| 25 | Hospital capabilities | The handbook says "appropriate facility" with examples (CT and stroke unit, cath lab, surgeon) but there is no list of hospitals. A data source is needed. |
| 26 | Emergency numbers | Only 108 appears. Other numbers (police, 112) are not covered. |

## C. How these will be handled
- Section A topics can be drafted as `extension` modules from general first-aid knowledge, flagged for expert review,
  or written from a source you supply. Tell me which topics to draft and I will not draft the others.
- Section B items stay flagged in the data (`source: adapted` or `extension`) until you resolve them.
