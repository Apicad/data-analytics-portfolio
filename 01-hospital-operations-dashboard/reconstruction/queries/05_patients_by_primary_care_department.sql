-- RECONSTRUCTION. Second slice of the patient-distribution view: where patients sit in the org,
-- by the primary department of their primary care physician (PCP).
SELECT d.Name                         AS pcp_department,
       COUNT(*)                       AS patients,
       COUNT(DISTINCT pt.PCP)         AS pcps_in_department,
       ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT pt.PCP), 1) AS avg_panel_size
FROM Patient         AS pt
JOIN Affiliated_With AS aw ON aw.Physician = pt.PCP AND aw.PrimaryAffiliation = 1
JOIN Department      AS d  ON d.DepartmentID = aw.Department
GROUP BY d.Name
ORDER BY patients DESC;
