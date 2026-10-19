# data/hospitals/

- `raw/ambulance_hospitals.json`: put your full scraped list here (a JSON list of records). Not committed by default.
- `raw/sample_hospitals_raw.json`: 46 sample rows used for development and tests.
- `hospitals_clean.json`: the file the API reads. **The one shipped in the project is a 38-row sample.** Run
  `python scripts/clean_hospitals.py` to replace it with your cleaned full list.
- `excluded.json` and `CLEANING_REPORT.md`: what the cleaner dropped and why.
- `capability_overrides.yaml`: facts you verify about specific hospitals.
- `emergency_requirements.yaml`: which hospital tier and capability suits which emergency.

Coverage is whatever the loaded list covers. The app shows hospitals near the user from this list, and tells the user to call 108 when none is close.
Check the licence or terms of the source you scraped from, and add any required attribution to the app's About page.
