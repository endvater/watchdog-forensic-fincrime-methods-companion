MATCH (a:Article)-[r:USES_DATASET]->(d:Dataset)
RETURN a.series_order AS ord,
       a.title AS article,
       d.name AS dataset,
       d.category AS category,
       r.role AS role,
       r.is_required AS required
ORDER BY ord, dataset;
