SELECT
    d.name,
    d.category,
    d.access_mode,
    COUNT(DISTINCT ad.article_id) AS article_count,
    GROUP_CONCAT(DISTINCT a.title) AS articles
FROM datasets d
LEFT JOIN article_datasets ad ON ad.dataset_id = d.dataset_id
LEFT JOIN articles a ON a.article_id = ad.article_id
GROUP BY d.dataset_id, d.name, d.category, d.access_mode
ORDER BY article_count DESC, d.name;
