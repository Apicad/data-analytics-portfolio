# From schema to dashboard: how each view is built

The capstone dashboard (Power BI) had three views. The original `.pbix` and its queries were not
recovered, so the SQL in `../reconstruction/queries/` is a **reconstruction** from the schema and the
project proposal. Each query runs on SQLite via `../improvements/build_sqlite.py`; the MySQL
equivalent of any non-portable function is in a comment next to it.

| View | Question it answers | Query | Tables | Join path | Aggregation |
|---|---|---|---|---|---|
| Appointment counts (by month) | How busy is the clinic over the year? | `01_appointments_by_month.sql` | Appointment | none | `COUNT(*)`, `COUNT(DISTINCT Patient)`, `COUNT(DISTINCT Physician)`, average minutes from `Starto`/`Endo`, grouped by `SUBSTR(Starto, 1, 7)` |
| Appointment counts (by department) | Which departments carry the visits? | `02_appointments_by_department.sql` | Appointment, Affiliated_With, Department | Appointment.Physician → Affiliated_With.Physician (where `PrimaryAffiliation = 1`) → Department | `COUNT(*)`, distinct patients and physicians, appointments per physician |
| Physician workload | Who sees the most patients, writes the most prescriptions, does the most procedures? | `03_physician_workload.sql` | Physician, Affiliated_With, Department, Appointment, Prescribes, Undergoes, Patient | Physician LEFT JOIN Appointment; department via primary affiliation; prescriptions, procedures and PCP panel via correlated subqueries | `COUNT`, `SUM` of hours, `COUNT(DISTINCT Patient)` per physician |
| Patient distribution (by place) | Where do patients live? | `04_patient_distribution.sql` | Patient, Appointment | Patient grouped by Address; appointments via subquery on Appointment.Patient = Patient.SSN | `COUNT(*)`, share of all patients, distinct PCPs, appointments |
| Patient distribution (by department) | Which departments do patients belong to through their PCP? | `05_patients_by_primary_care_department.sql` | Patient, Affiliated_With, Department | Patient.PCP → Affiliated_With (primary) → Department | `COUNT(*)`, PCPs per department, average panel size |

## Design choices worth explaining

**Primary affiliation only.** `Affiliated_With` is many-to-many. Joining through it without the
`PrimaryAffiliation = 1` filter would count an appointment once per department the physician belongs
to and inflate department totals. The filter makes every appointment land in exactly one department.

**Subqueries for the side counts.** In the workload query, joining Prescribes and Undergoes directly
onto a row set that already includes one row per appointment would multiply prescriptions by
appointments. Correlated subqueries keep each count independent.

**`LEFT JOIN` on Appointment.** A physician with zero visits should still appear in the workload
view with a zero, not vanish. `COALESCE(SUM(...), 0)` keeps the hours column numeric for them.

**Date handling.** `SUBSTR(Starto, 1, 7)` gives `YYYY-MM` in both MySQL and SQLite. Durations differ:
SQLite uses `julianday(Endo) - julianday(Starto)`, MySQL uses `TIMESTAMPDIFF(MINUTE, ...)`.

**Address parsing.** `Patient.Address` is a single `varchar(30)`. The distribution view only works
because the synthetic data stores "City, ST". A production version would add separate city, state
and postal-code columns (or a geography table) so Power BI's map visual gets clean keys.

## In Power BI terms

- The five queries would be the report's data model tables (or DAX measures over imported tables).
- Month and department slicers correspond to `WHERE` filters on `Starto` and `Department.Name`.
- The map visual on View 3 keys on city/state; the bar chart in `dashboard_views.ipynb` stands in
  for it because the synthetic data has no coordinates.
