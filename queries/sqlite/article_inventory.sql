SELECT
    a.series_order AS ord,
    a.title,
    a.reproducibility,
    COUNT(DISTINCT ad.dataset_id) AS dataset_count,
    GROUP_CONCAT(DISTINCT d.name) AS datasets
FROM articles a
LEFT JOIN article_datasets ad ON ad.article_id = a.article_id
LEFT JOIN datasets d ON d.dataset_id = ad.dataset_id
GROUP BY a.article_id, a.series_order, a.title, a.reproducibility
ORDER BY a.series_order;
