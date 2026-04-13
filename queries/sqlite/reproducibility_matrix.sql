SELECT
    a.series_order AS ord,
    a.title,
    a.reproducibility,
    SUM(CASE WHEN rs.requires_manual_dataset = 1 THEN 1 ELSE 0 END) AS manual_steps,
    SUM(CASE WHEN rs.is_executable = 1 THEN 1 ELSE 0 END) AS executable_steps,
    COUNT(rs.step_id) AS total_steps
FROM articles a
LEFT JOIN reproduction_steps rs ON rs.article_id = a.article_id
GROUP BY a.article_id, a.series_order, a.title, a.reproducibility
ORDER BY a.series_order;
