# Data dictionary: Hospital schema (13 tables)

Source: `../original/dump-Hospital-202512151315.sql`, a `mysqldump 9.5.0` export of the `Hospital`
database taken 2025-12-15. **Schema only.** The dump has no `INSERT` statements, so no patient,
staff or appointment records exist in this repository. All 13 tables are InnoDB, `utf8mb4`.

The design is the widely used "hospital" teaching schema (physicians, departments, patients,
appointments, prescriptions, rooms, stays, procedures). My Drive notes from the planning phase show
an earlier 6-table version (Department, Physician, Patient, Medication, Appointment, Prescription);
the capstone shipped on this fuller 13-table version.

Legend: **PK** primary key, **FK** foreign key, `bit(1)` is a yes/no flag, `datetime` is
`YYYY-MM-DD HH:MM:SS`. mysqldump also created a secondary index on every single-column FK (16 total).

## People and organisation

### Physician
| Column | Type | Key | Meaning |
|---|---|---|---|
| EmployeeID | int | PK | Staff number |
| Name | varchar(30) | | Full name |
| Position | varchar(30) | | Job title (attending, resident, ...) |
| SSN | int | | Social security number. **Sensitive. Never populated with real values in this repo.** |

### Nurse
| Column | Type | Key | Meaning |
|---|---|---|---|
| EmployeeID | int | PK | Staff number |
| Name | varchar(30) | | Full name |
| Position | varchar(30) | | Job title |
| Registered | bit(1) | | 1 if a registered nurse |
| SSN | int | | **Sensitive, synthetic only.** |

### Department
| Column | Type | Key | Meaning |
|---|---|---|---|
| DepartmentID | int | PK | |
| Name | varchar(30) | | Department name |
| Head | int | FK → Physician.EmployeeID | Physician who runs the department |

### Affiliated_With
Many-to-many between physicians and departments.
| Column | Type | Key | Meaning |
|---|---|---|---|
| Physician | int | PK, FK → Physician.EmployeeID | |
| Department | int | PK, FK → Department.DepartmentID | |
| PrimaryAffiliation | bit(1) | | 1 for the physician's home department. Dashboard queries credit work to this one. |

## Patients and visits

### Patient
| Column | Type | Key | Meaning |
|---|---|---|---|
| SSN | int | PK | **The patient's identifier is their SSN.** Design smell inherited from the teaching schema; see README limitation. Synthetic only here. |
| Name | varchar(30) | | |
| Address | varchar(30) | | Free text. Synthetic rows use "City, ST" so the distribution view can group by place. |
| Phone | varchar(30) | | Synthetic rows use the fictional 555-01xx block. |
| InsuranceID | int | | Insurance policy reference |
| PCP | int | FK → Physician.EmployeeID | Primary care physician |

### Appointment
| Column | Type | Key | Meaning |
|---|---|---|---|
| AppointmentID | int | PK | |
| Patient | int | FK → Patient.SSN | |
| PrepNurse | int, nullable | FK → Nurse.EmployeeID | Nurse who prepped the visit, if any |
| Physician | int | FK → Physician.EmployeeID | Physician seen |
| Starto | datetime | | Start (named `Starto` in the dump; `Start` is a reserved word) |
| Endo | datetime | | End |
| ExaminationRoom | text | | Room label |

### Medication
| Column | Type | Key | Meaning |
|---|---|---|---|
| Code | int | PK | |
| Name | varchar(30) | | Generic name |
| Brand | varchar(30) | | Brand name |
| Description | varchar(30) | | What it is for |

### Prescribes
| Column | Type | Key | Meaning |
|---|---|---|---|
| Physician | int | PK, FK → Physician.EmployeeID | |
| Patient | int | PK, FK → Patient.SSN | |
| Medication | int | PK, FK → Medication.Code | |
| Date | datetime | PK | When prescribed |
| Appointment | int, nullable | FK → Appointment.AppointmentID | Visit it came from, if any |
| Dose | varchar(30) | | Free text dose |

## Inpatient side

### Room
| Column | Type | Key | Meaning |
|---|---|---|---|
| RoomNumber | int | PK | |
| RoomType | varchar(30) | | Single, double, ICU, ... |
| BlockFloor | int | | Floor |
| BlockCode | int | | Wing / block |
| Unavailable | bit(1) | | 1 if out of service |

### Stay
| Column | Type | Key | Meaning |
|---|---|---|---|
| StayID | int | PK | |
| Patient | int | FK → Patient.SSN | |
| Room | int | FK → Room.RoomNumber | |
| StayStart | datetime | | Admission |
| StayEnd | datetime | | Discharge |

### Procedures
| Column | Type | Key | Meaning |
|---|---|---|---|
| Code | int | PK | |
| Name | varchar(30) | | |
| Cost | double | | List price |

### Trained_In
Which procedures each physician is certified to perform.
| Column | Type | Key | Meaning |
|---|---|---|---|
| Physician | int | PK, FK → Physician.EmployeeID | |
| Treatment | int | PK, FK → Procedures.Code | |
| CertificationDate | datetime | | |
| CertificationExpires | datetime | | |

### Undergoes
A procedure performed on a patient during a stay.
| Column | Type | Key | Meaning |
|---|---|---|---|
| Patient | int | PK, FK → Patient.SSN | |
| Procedures | int | PK, FK → Procedures.Code | |
| Stay | int | PK, FK → Stay.StayID | |
| DateUndergoes | datetime | PK | |
| Physician | int | FK → Physician.EmployeeID | Performing physician (should appear in Trained_In for this procedure) |
| AssistingNurse | int, nullable | FK → Nurse.EmployeeID | |

## Relationship summary

- A physician belongs to one or more departments (`Affiliated_With`), heads at most one
  (`Department.Head`), is certified in procedures (`Trained_In`), is PCP for patients
  (`Patient.PCP`), sees patients (`Appointment`), prescribes (`Prescribes`) and performs procedures
  (`Undergoes`).
- A patient has one PCP, many appointments, many prescriptions, and for inpatient care many stays,
  each in one room, during which procedures happen.
- Nurses appear only as optional helpers: `Appointment.PrepNurse` and `Undergoes.AssistingNurse`.

## Synthetic data that ships with this repo

`../improvements/synthetic_data/*.csv`, produced by `../improvements/generate_synthetic_data.py`
with a fixed seed. Sizes: 40 physicians, 30 nurses, 8 departments, 400 patients, 3,000 appointments
across calendar 2025, 20 medications, ~2,150 prescriptions, 20 procedures, 40 rooms, 250 stays, 320
procedures performed. Every SSN starts with 900 (never issued by the SSA), every phone is 555-01xx,
every address is "City, ST". Nothing in these files describes a real person.
