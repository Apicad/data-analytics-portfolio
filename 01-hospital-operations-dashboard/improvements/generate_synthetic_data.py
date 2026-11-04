#!/usr/bin/env python3
"""Generate clearly SYNTHETIC rows for the 13-table Hospital schema.

PORTFOLIO IMPROVEMENT. The only capstone artifact that survived is a schema-only
mysqldump (../original/dump-Hospital-202512151315.sql). No data rows survived, so
there is nothing real to check for privacy. Everything this script writes is made
up, with a fixed random seed so the output is identical every run:

* People are "FirstName LastName" drawn from two short name lists.
* SSN columns hold 9-digit integers that start with 900. The Social Security
  Administration never issues 900-series numbers, so none of these can be real.
* Phone numbers use the 555-01xx block that is reserved for fiction.
* Addresses are "City, ST" only, so the patient-distribution view has something
  to group by. No street addresses.
* Appointments cover calendar year 2025 with a seasonal pattern and uneven
  physician workloads so the dashboard views have a visible story.

Run with stock Python (no third-party packages):

    python generate_synthetic_data.py            # writes CSVs to ./synthetic_data/
    python generate_synthetic_data.py --seed 7   # different but still fake data
"""
from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "synthetic_data"

FIRST = [
    "Ana", "Luis", "Maya", "Omar", "Priya", "Jonah", "Keiko", "Marcus", "Sofia", "Devin",
    "Grace", "Hugo", "Ines", "Tariq", "Nadia", "Felix", "Rosa", "Elias", "Leah", "Dante",
    "Amara", "Noor", "Caleb", "Yara", "Ravi", "Lena", "Mateo", "Zoe", "Idris", "Carmen",
]
LAST = [
    "Rivera", "Chen", "Okafor", "Patel", "Nguyen", "Alvarez", "Kim", "Haddad", "Silva", "Brooks",
    "Mensah", "Novak", "Diaz", "Tanaka", "Osei", "Romero", "Larsen", "Ibrahim", "Castro", "Walsh",
]
CITIES = [  # (city, state, weight) weights make the geographic view uneven on purpose
    ("Phoenix", "AZ", 22), ("Mesa", "AZ", 14), ("Tempe", "AZ", 12), ("Chandler", "AZ", 10),
    ("Scottsdale", "AZ", 9), ("Glendale", "AZ", 8), ("Gilbert", "AZ", 7), ("Peoria", "AZ", 5),
    ("Tucson", "AZ", 4), ("Flagstaff", "AZ", 3), ("Las Vegas", "NV", 3), ("Albuquerque", "NM", 3),
]
DEPARTMENTS = [
    "General Medicine", "Pediatrics", "Cardiology", "Orthopedics",
    "Dermatology", "Oncology", "Neurology", "Psychiatry",
]
PHYSICIAN_POSITIONS = ["Attending Physician", "Senior Attending", "Resident", "Staff Physician"]
NURSE_POSITIONS = ["Head Nurse", "Nurse", "Nurse Practitioner", "Nursing Assistant"]
ROOM_TYPES = ["Single", "Double", "Suite", "ICU"]
MEDICATIONS = [
    ("Lisinopril", "Zestril", "Blood pressure"), ("Metformin", "Glucophage", "Type 2 diabetes"),
    ("Atorvastatin", "Lipitor", "Cholesterol"), ("Amoxicillin", "Amoxil", "Antibiotic"),
    ("Albuterol", "Ventolin", "Asthma inhaler"), ("Omeprazole", "Prilosec", "Acid reflux"),
    ("Sertraline", "Zoloft", "Antidepressant"), ("Ibuprofen", "Advil", "Pain and inflammation"),
    ("Levothyroxine", "Synthroid", "Thyroid"), ("Amlodipine", "Norvasc", "Blood pressure"),
    ("Gabapentin", "Neurontin", "Nerve pain"), ("Cetirizine", "Zyrtec", "Allergy"),
    ("Prednisone", "Deltasone", "Steroid"), ("Losartan", "Cozaar", "Blood pressure"),
    ("Azithromycin", "Zithromax", "Antibiotic"), ("Montelukast", "Singulair", "Asthma"),
    ("Insulin glargine", "Lantus", "Diabetes"), ("Hydrochlorothiazide", "Microzide", "Diuretic"),
    ("Escitalopram", "Lexapro", "Antidepressant"), ("Pantoprazole", "Protonix", "Acid reflux"),
]
PROCEDURES = [
    ("Annual physical", 180.0), ("Blood panel", 95.0), ("X-ray", 240.0), ("MRI scan", 1450.0),
    ("CT scan", 1100.0), ("Echocardiogram", 850.0), ("Stress test", 620.0), ("Skin biopsy", 410.0),
    ("Colonoscopy", 1900.0), ("Knee arthroscopy", 5200.0), ("Cast application", 320.0),
    ("Ultrasound", 390.0), ("EKG", 150.0), ("Allergy testing", 280.0), ("Vaccination", 60.0),
    ("Physical therapy session", 140.0), ("Chemotherapy infusion", 3200.0), ("EEG", 700.0),
    ("Sleep study", 1600.0), ("Minor laceration repair", 450.0),
]
# Relative appointment volume by month (1 = Jan). Flu season high, summer dip.
MONTH_WEIGHTS = [1.25, 1.15, 1.0, 0.95, 0.9, 0.8, 0.75, 0.85, 1.0, 1.05, 1.15, 1.2]


def fake_ssn(block: int, i: int) -> int:
    """9-digit integer that always starts with 900, a series the SSA never issues.

    900 B iiiii, where B is 0 for patients, 1 for physicians, 2 for nurses.
    """
    return 900_000_000 + block * 100_000 + i


def person_name(rng: random.Random) -> str:
    return f"{rng.choice(FIRST)} {rng.choice(LAST)}"


def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def weighted_month(rng: random.Random) -> int:
    return rng.choices(range(1, 13), weights=MONTH_WEIGHTS)[0]


def random_business_datetime(rng: random.Random, year: int) -> datetime:
    """A weekday appointment start between 08:00 and 16:30, on a quarter hour."""
    while True:
        month = weighted_month(rng)
        day = rng.randint(1, 28)
        dt = datetime(year, month, day)
        if dt.weekday() < 5:
            break
    return dt + timedelta(hours=rng.randint(8, 16), minutes=rng.choice([0, 15, 30, 45]))


def generate(seed: int = 2025, year: int = 2025) -> dict[str, list[dict]]:
    rng = random.Random(seed)
    tables: dict[str, list[dict]] = {}

    # Physician -----------------------------------------------------------
    physicians = []
    for i in range(1, 41):
        physicians.append(
            {"EmployeeID": i, "Name": person_name(rng),
             "Position": rng.choice(PHYSICIAN_POSITIONS), "SSN": fake_ssn(1, i)}
        )
    tables["Physician"] = physicians

    # Department (Head must be a physician) --------------------------------
    heads = rng.sample(range(1, 41), len(DEPARTMENTS))
    tables["Department"] = [
        {"DepartmentID": d + 1, "Name": name, "Head": heads[d]} for d, name in enumerate(DEPARTMENTS)
    ]

    # Affiliated_With: everyone has one primary department, a third have a second
    affiliations = []
    primary_dept: dict[int, int] = {}
    for p in physicians:
        dept = rng.randint(1, len(DEPARTMENTS))
        primary_dept[p["EmployeeID"]] = dept
        affiliations.append({"Physician": p["EmployeeID"], "Department": dept, "PrimaryAffiliation": 1})
        if rng.random() < 0.33:
            other = rng.choice([d for d in range(1, len(DEPARTMENTS) + 1) if d != dept])
            affiliations.append({"Physician": p["EmployeeID"], "Department": other, "PrimaryAffiliation": 0})
    # department heads should at least be affiliated with the department they run
    for d in tables["Department"]:
        if not any(a["Physician"] == d["Head"] and a["Department"] == d["DepartmentID"] for a in affiliations):
            affiliations.append({"Physician": d["Head"], "Department": d["DepartmentID"], "PrimaryAffiliation": 0})
    tables["Affiliated_With"] = affiliations

    # Procedures and Trained_In -------------------------------------------
    tables["Procedures"] = [
        {"Code": c + 1, "Name": name, "Cost": cost} for c, (name, cost) in enumerate(PROCEDURES)
    ]
    trained = []
    trained_lookup: dict[int, list[int]] = {}
    for p in physicians:
        codes = rng.sample(range(1, len(PROCEDURES) + 1), rng.randint(2, 6))
        for code in codes:
            cert = datetime(year - rng.randint(1, 6), rng.randint(1, 12), rng.randint(1, 28))
            trained.append(
                {"Physician": p["EmployeeID"], "Treatment": code,
                 "CertificationDate": fmt(cert), "CertificationExpires": fmt(cert.replace(year=cert.year + 7))}
            )
            trained_lookup.setdefault(code, []).append(p["EmployeeID"])
    tables["Trained_In"] = trained

    # Nurse ----------------------------------------------------------------
    nurses = []
    for i in range(1, 31):
        nurses.append(
            {"EmployeeID": 100 + i, "Name": person_name(rng), "Position": rng.choice(NURSE_POSITIONS),
             "Registered": 1 if rng.random() < 0.8 else 0, "SSN": fake_ssn(2, i)}
        )
    tables["Nurse"] = nurses
    nurse_ids = [n["EmployeeID"] for n in nurses]

    # Patient --------------------------------------------------------------
    city_weights = [c[2] for c in CITIES]
    patients = []
    for i in range(1, 401):
        city, state, _ = rng.choices(CITIES, weights=city_weights)[0]
        patients.append(
            {"SSN": fake_ssn(0, i), "Name": person_name(rng), "Address": f"{city}, {state}",
             "Phone": f"555-01{rng.randint(0, 99):02d}", "InsuranceID": 70_000 + i,
             "PCP": rng.randint(1, 40)}
        )
    tables["Patient"] = patients
    patient_ids = [p["SSN"] for p in patients]

    # Appointment: uneven physician workload via per-physician weights ------
    physician_weights = [rng.choice([0.4, 0.7, 1.0, 1.0, 1.3, 1.8, 2.4]) for _ in physicians]
    appointments = []
    for i in range(1, 3001):
        start = random_business_datetime(rng, year)
        minutes = rng.choice([20, 30, 30, 45, 60])
        appointments.append(
            {"AppointmentID": i, "Patient": rng.choice(patient_ids),
             "PrepNurse": rng.choice(nurse_ids) if rng.random() < 0.85 else "",
             "Physician": rng.choices(range(1, 41), weights=physician_weights)[0],
             "Starto": fmt(start), "Endo": fmt(start + timedelta(minutes=minutes)),
             "ExaminationRoom": f"Exam {rng.randint(1, 24)}"}
        )
    tables["Appointment"] = appointments

    # Medication and Prescribes --------------------------------------------
    tables["Medication"] = [
        {"Code": c + 1, "Name": n, "Brand": b, "Description": d} for c, (n, b, d) in enumerate(MEDICATIONS)
    ]
    prescribes = []
    seen = set()
    for appt in appointments:
        if rng.random() < 0.6:
            for _ in range(rng.choice([1, 1, 1, 2])):
                med = rng.randint(1, len(MEDICATIONS))
                key = (appt["Physician"], appt["Patient"], med, appt["Starto"])
                if key in seen:
                    continue
                seen.add(key)
                prescribes.append(
                    {"Physician": appt["Physician"], "Patient": appt["Patient"], "Medication": med,
                     "Date": appt["Starto"], "Appointment": appt["AppointmentID"],
                     "Dose": rng.choice(["5 mg daily", "10 mg daily", "20 mg daily", "250 mg twice daily", "as needed"])}
                )
    tables["Prescribes"] = prescribes

    # Room and Stay --------------------------------------------------------
    rooms = []
    for i in range(1, 41):
        rooms.append(
            {"RoomNumber": 100 * (1 + (i - 1) // 10) + (i - 1) % 10 + 1,
             "RoomType": rng.choice(ROOM_TYPES), "BlockFloor": 1 + (i - 1) // 10,
             "BlockCode": rng.randint(1, 3), "Unavailable": 1 if rng.random() < 0.1 else 0}
        )
    tables["Room"] = rooms
    room_numbers = [r["RoomNumber"] for r in rooms]
    stays = []
    for i in range(1, 251):
        start = datetime(year, weighted_month(rng), rng.randint(1, 28), rng.randint(6, 20))
        stays.append(
            {"StayID": i, "Patient": rng.choice(patient_ids), "Room": rng.choice(room_numbers),
             "StayStart": fmt(start), "StayEnd": fmt(start + timedelta(days=rng.randint(1, 9), hours=rng.randint(0, 12)))}
        )
    tables["Stay"] = stays

    # Undergoes: physician must be trained in the procedure ----------------
    undergoes = []
    seen = set()
    for _ in range(320):
        stay = rng.choice(stays)
        code = rng.randint(1, len(PROCEDURES))
        if code not in trained_lookup:
            continue
        when = datetime.strptime(stay["StayStart"], "%Y-%m-%d %H:%M:%S") + timedelta(hours=rng.randint(1, 48))
        key = (stay["Patient"], code, stay["StayID"], fmt(when))
        if key in seen:
            continue
        seen.add(key)
        undergoes.append(
            {"Patient": stay["Patient"], "Procedures": code, "Stay": stay["StayID"],
             "DateUndergoes": fmt(when), "Physician": rng.choice(trained_lookup[code]),
             "AssistingNurse": rng.choice(nurse_ids) if rng.random() < 0.7 else ""}
        )
    tables["Undergoes"] = undergoes
    return tables


def write_csvs(tables: dict[str, list[dict]], out_dir: Path = OUT_DIR) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        path = out_dir / f"{name}.csv"
        with path.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"{name:16s} {len(rows):5d} rows -> {path.relative_to(out_dir.parent)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Write synthetic CSVs for the Hospital schema.")
    parser.add_argument("--seed", type=int, default=2025)
    parser.add_argument("--year", type=int, default=2025)
    args = parser.parse_args()
    write_csvs(generate(seed=args.seed, year=args.year))
    print("All rows above are synthetic. SSNs are in the never-issued 900 series; phones are 555-01xx.")


if __name__ == "__main__":
    main()
