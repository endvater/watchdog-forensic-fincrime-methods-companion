LOAD CSV WITH HEADERS FROM 'file:///articles.csv' AS row
MERGE (a:Article {article_id: row.article_id})
SET a.title = row.title,
    a.series_order = toInteger(row.series_order),
    a.part_no = CASE WHEN row.part_no = '' THEN NULL ELSE toInteger(row.part_no) END,
    a.url = row.url,
    a.reproducibility = row.reproducibility;

LOAD CSV WITH HEADERS FROM 'file:///datasets.csv' AS row
MERGE (d:Dataset {dataset_id: row.dataset_id})
SET d.name = row.name,
    d.category = row.category,
    d.access_mode = row.access_mode,
    d.source_url = row.source_url;

LOAD CSV WITH HEADERS FROM 'file:///article_datasets.csv' AS row
MATCH (a:Article {article_id: row.article_id})
MATCH (d:Dataset {dataset_id: row.dataset_id})
MERGE (a)-[r:USES_DATASET]->(d)
SET r.role = row.role,
    r.is_required = CASE row.is_required WHEN '1' THEN true ELSE false END;
