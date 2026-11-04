-- RECONSTRUCTION. Feeds the "patient geographic distribution" view.
-- Patient.Address is a single varchar(30). The synthetic data stores "City, ST" so it can be split;
-- the original clinic data would need the same convention or a separate city/state column.
SELECT TRIM(SUBSTR(pt.Address, 1, INSTR(pt.Address, ',') - 1))  AS city,
                                                -- MySQL: TRIM(SUBSTRING_INDEX(pt.Address, ',', 1))
       TRIM(SUBSTR(pt.Address, INSTR(pt.Address, ',') + 1))     AS state,
                                                -- MySQL: TRIM(SUBSTRING_INDEX(pt.Address, ',', -1))
       COUNT(*)                                                 AS patients,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Patient), 1) AS pct_of_patients,
       COUNT(DISTINCT pt.PCP)                                   AS distinct_pcps,
       (SELECT COUNT(*) FROM Appointment a JOIN Patient p2 ON p2.SSN = a.Patient
         WHERE p2.Address = pt.Address)                         AS appointments
FROM Patient AS pt
GROUP BY pt.Address
ORDER BY patients DESC;
