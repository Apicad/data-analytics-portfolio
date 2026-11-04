-- RECONSTRUCTION. Department slice of the "appointment counts" view.
-- A physician can sit in several departments (Affiliated_With), so appointments are credited
-- to the physician's PRIMARY affiliation to avoid double counting.
SELECT d.Name                         AS department,
       COUNT(*)                       AS appointments,
       COUNT(DISTINCT a.Patient)      AS distinct_patients,
       COUNT(DISTINCT a.Physician)    AS physicians,
       ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT a.Physician), 1) AS appointments_per_physician
FROM Appointment      AS a
JOIN Affiliated_With  AS aw ON aw.Physician = a.Physician AND aw.PrimaryAffiliation = 1
JOIN Department       AS d  ON d.DepartmentID = aw.Department
GROUP BY d.Name
ORDER BY appointments DESC;
