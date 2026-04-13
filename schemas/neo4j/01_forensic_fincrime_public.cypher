CREATE CONSTRAINT series_id_unique IF NOT EXISTS
FOR (s:Series) REQUIRE s.series_id IS UNIQUE;

CREATE CONSTRAINT article_id_unique IF NOT EXISTS
FOR (a:Article) REQUIRE a.article_id IS UNIQUE;

CREATE CONSTRAINT dataset_id_unique IF NOT EXISTS
FOR (d:Dataset) REQUIRE d.dataset_id IS UNIQUE;

CREATE INDEX article_title_idx IF NOT EXISTS
FOR (a:Article) ON (a.title);

CREATE INDEX dataset_name_idx IF NOT EXISTS
FOR (d:Dataset) ON (d.name);
