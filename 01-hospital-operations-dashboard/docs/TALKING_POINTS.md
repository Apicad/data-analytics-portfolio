# Talking points: hospital operations dashboard

## The 60-second version

For my capstone I built an operations dashboard for an outpatient clinic, end to end: I designed
the database, implemented it in MySQL with proper keys and foreign keys, wrote the SQL behind three
views (appointments by month and department, physician workload, where patients live), and built
the Power BI report. The original Power BI file was lost with my Year Up account, so for the
portfolio I rebuilt the pipeline in a way anyone can run in a minute: a generator for clearly
synthetic data, a script that converts the MySQL dump to SQLite and loads it with foreign-key checks
on, the same five queries, and the three views drawn in Python. The repo documents every table and
exactly which joins and aggregations feed each view.

## Questions I expect, and what I say

**Why thirteen tables for a dashboard that uses seven?**
The database serves the whole clinic, not just the dashboard. Rooms, stays, procedures and
certifications are the inpatient side. The dashboard reads the outpatient tables and ignores the
rest, which is how it should be.

**How do you avoid double counting?**
Two places. A physician can be in several departments, so I credit each appointment to their
primary department only. And when I add prescriptions and procedures to the workload view I use
correlated subqueries, because joining them onto one-row-per-appointment would multiply them.

**Why LEFT JOIN on appointments?**
So a physician with zero visits still shows up with a zero. A workload view that hides the idle
people is answering the wrong question.

**What would you change about the schema?**
Patients are keyed by SSN. That is a teaching-schema habit and a bad idea in production: use a
surrogate ID, keep SSN out of the database or encrypt it. I would also split `Address` into city,
state and postal code, so the map visual has clean keys.

**Is any of this real data?**
No. The capstone used sample data and it did not survive. Everything here is generated with a seed,
with SSNs in a never-issued range and fictional phone numbers. I say that on every chart.

**Why SQLite instead of MySQL in the portfolio?**
So a reviewer can run it without installing anything. The dump is still the original MySQL schema;
the script only translates types. Any query that uses a MySQL-specific function has the MySQL line
in a comment.

**How did the Power BI report use these queries?**
Each query is a table in the data model. Month and department slicers are `WHERE` clauses on the
same columns. Cards for totals, a column chart by month, a bar chart by department, a table for
workload, a map for patients by city.

## Technical details, if asked

- mysqldump 9.5.0, InnoDB, utf8mb4, 13 tables, 16 secondary indexes on foreign-key columns.
- Conversion: `bit(1)` to INTEGER, `datetime` to TEXT, `varchar` to TEXT, `KEY` lines to `CREATE INDEX`.
- Loading order follows the foreign keys: physicians before departments, patients before appointments.
- Synthetic sizes: 40 physicians, 30 nurses, 8 departments, 400 patients, 3,000 appointments, ~2,150 prescriptions, 250 stays, 320 procedures performed.
