import clean_hospitals as ch


def rec(name, **kw):
    base = {"name": name, "lat": 12.9, "lon": 77.6, "type": "primary", "specialties": ["general"], "emergency": "unknown", "operator_type": "unknown", "phone": ""}
    return {**base, **kw}


def run(records):
    return ch.clean(records, [])


def test_drops_non_medical():
    rows, ex = run([rec("Dr Lal PathLabs", type="secondary", emergency="yes"), rec("The Local Dentist", emergency="yes"),
                    rec("Hair Loss Treatment in Bangalore - Hairline International", emergency="yes"), rec("Medical Shop")])
    assert rows == [] and len(ex) == 4


def test_clinic_is_primary_never_emergency():
    rows, _ = run([rec("Apollo Clinic", type="tertiary", emergency="yes")])
    assert rows[0]["tier"] == "primary" and rows[0]["emergency_status"] == "unlikely"


def test_hospital_status():
    rows, _ = run([rec("City Hospital", type="tertiary"), rec("Metro Hospital", type="secondary", emergency="yes", lat=13.0, lon=77.7)])
    by = {r["name"]: r for r in rows}
    assert by["City Hospital"]["emergency_status"] == "probable"
    assert by["Metro Hospital"]["emergency_status"] == "confirmed"


def test_duplicates_merged():
    rows, ex = run([rec("Sanjay Gandhi Accident and Trauma Hospital", lat=12.9356389, lon=77.5935945, type="secondary", emergency="yes"),
                    rec("Sanjay Gandhi Accident and Trauma Hospital", lat=12.9357711, lon=77.5939433, type="secondary", emergency="yes")])
    assert len(rows) == 1 and any("duplicate" in e["reason"] for e in ex)


def test_eye_and_specialty_scope():
    rows, _ = run([rec("Vasan Eye Care Hospital, Koramangala", type="secondary", emergency="yes", specialties=["ophthalmology"])])
    assert rows[0]["class"] == "eye_hospital" and rows[0]["scope"] == "specialty"


def test_phone_cleanup():
    assert ch.clean_phone('"080 2672 8455"') == ["080 2672 8455"]
    assert ch.clean_phone("+91-80-23225858;+91-80-23225868") == ["+91-80-23225858", "+91-80-23225868"]
    assert ch.clean_phone("12") == []


def test_invalid_coordinates_excluded():
    rows, ex = run([{"name": "X Hospital", "lat": "abc", "lon": 1}])
    assert rows == [] and ex[0]["reason"].startswith("missing")
