-- RECONSTRUCTION. The SQL behind the original Power BI "appointment counts" view was not recovered.
-- Rebuilt from the schema in ../../original/dump-Hospital-202512151315.sql and the project proposal.
-- Written for SQLite (see build_sqlite.py). MySQL equivalents are in the comments.

-- Appointments per month, with how many distinct patients and physicians were involved.
SELECT SUBSTR(a.Starto, 1, 7)       AS month,                      -- MySQL: DATE_FORMAT(a.Starto, '%Y-%m')
       COUNT(*)                     AS appointments,
       COUNT(DISTINCT a.Patient)    AS distinct_patients,
       COUNT(DISTINCT a.Physician)  AS physicians_with_visits,
       ROUND(AVG((julianday(a.Endo) - julianday(a.Starto)) * 24 * 60), 1) AS avg_minutes
                                                                   -- MySQL: AVG(TIMESTAMPDIFF(MINUTE, a.Starto, a.Endo))
FROM Appointment AS a
GROUP BY month
ORDER BY month;
