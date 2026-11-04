-- RECONSTRUCTION. Feeds the "physician workload / activity" view.
-- One row per physician: visits, hours in appointments, distinct patients, prescriptions, procedures.
-- Prescriptions and procedures come from correlated subqueries so the appointment join does not inflate them.
SELECT p.EmployeeID,
       p.Name                                   AS physician,
       p.Position,
       d.Name                                   AS primary_department,
       COUNT(a.AppointmentID)                   AS appointments,
       ROUND(COALESCE(SUM((julianday(a.Endo) - julianday(a.Starto)) * 24), 0), 1) AS appointment_hours,
                                                -- MySQL: ROUND(SUM(TIMESTAMPDIFF(MINUTE, a.Starto, a.Endo)) / 60, 1)
       COUNT(DISTINCT a.Patient)                AS distinct_patients,
       (SELECT COUNT(*) FROM Prescribes pr WHERE pr.Physician = p.EmployeeID) AS prescriptions,
       (SELECT COUNT(*) FROM Undergoes  u  WHERE u.Physician  = p.EmployeeID) AS procedures_performed,
       (SELECT COUNT(*) FROM Patient    pt WHERE pt.PCP       = p.EmployeeID) AS primary_care_panel
FROM Physician            AS p
LEFT JOIN Affiliated_With AS aw ON aw.Physician = p.EmployeeID AND aw.PrimaryAffiliation = 1
LEFT JOIN Department      AS d  ON d.DepartmentID = aw.Department
LEFT JOIN Appointment     AS a  ON a.Physician = p.EmployeeID
GROUP BY p.EmployeeID, p.Name, p.Position, d.Name
ORDER BY appointments DESC, p.Name;
