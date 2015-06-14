SELECT b . * , Party, Candidate, Name
FROM (

SELECT a . * , (
Maxy /100
) * ( Turnout /100 ) *100 AS Overall
FROM (

SELECT r.ConstituencyId, MAX( Percentage ) AS Maxy, Turnout
FROM Results r
INNER JOIN Constituency c ON r.ConstituencyId = c.ConstituencyId
GROUP BY r.ConstituencyId
ORDER BY Maxy DESC
)a
)b
INNER JOIN Results r ON b.ConstituencyId = r.ConstituencyId
AND b.Maxy = Percentage
INNER JOIN Constituency c ON c.ConstituencyId = b.ConstituencyId
WHERE Overall >=40
ORDER BY Overall DESC 