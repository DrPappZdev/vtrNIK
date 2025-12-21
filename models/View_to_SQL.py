ALTER VIEW [dbo].[aktiv_munkatarsak] AS
SELECT
    m.titulus,
    m.nev,
    r.rendfokozat,
    b.beosztas,
    msz.minSzint AS Nemzeti_Minosites,
    msz_n.minSzint AS NATO_Minosites,
    -- Az új EU mező a minSzintek táblából:
    msz_e.minSzint AS EU_Minosites
FROM dbo.munkatarsak AS m
LEFT OUTER JOIN dbo.beosztasok AS b ON m.beosztas = b.id
LEFT OUTER JOIN dbo.rendfokozatok AS r ON m.rendfokozat = r.id

-- Nemzeti lánc
LEFT OUTER JOIN dbo.szbtNemzeti AS sn ON m.id = sn.agentId
LEFT OUTER JOIN dbo.minSzintek AS msz ON sn.szbtNemMinSzint = msz.id

-- NATO lánc
LEFT OUTER JOIN dbo.szbtNATO AS nato ON m.id = nato.agentId
LEFT OUTER JOIN dbo.minSzintek AS msz_n ON nato.szbtNatoMinSzint = msz_n.id

-- EU lánc
LEFT OUTER JOIN dbo.szbtEU AS eu ON m.id = eu.agentId
LEFT OUTER JOIN dbo.minSzintek AS msz_e ON eu.szbtEuMinSzint = msz_e.id

WHERE (m.valid_e = 1);