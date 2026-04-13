PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS series (
    series_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    series_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    article_id TEXT PRIMARY KEY,
    series_id TEXT NOT NULL,
    series_order INTEGER NOT NULL,
    part_no INTEGER,
    title TEXT NOT NULL,
    slug TEXT NOT NULL,
    published_on TEXT NOT NULL,
    url TEXT NOT NULL,
    angle TEXT NOT NULL,
    technical_setup TEXT NOT NULL,
    methodology TEXT NOT NULL,
    insight TEXT NOT NULL,
    reproducibility TEXT NOT NULL,
    FOREIGN KEY (series_id) REFERENCES series(series_id)
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    access_mode TEXT NOT NULL,
    source_url TEXT NOT NULL,
    manual_drop_path TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS article_datasets (
    article_id TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'primary',
    is_required INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (article_id, dataset_id),
    FOREIGN KEY (article_id) REFERENCES articles(article_id),
    FOREIGN KEY (dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE IF NOT EXISTS reproduction_steps (
    step_id TEXT PRIMARY KEY,
    article_id TEXT NOT NULL,
    step_order INTEGER NOT NULL,
    name TEXT NOT NULL,
    summary TEXT NOT NULL,
    is_executable INTEGER NOT NULL,
    requires_manual_dataset INTEGER NOT NULL,
    FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

CREATE TABLE IF NOT EXISTS public_assets (
    asset_id TEXT PRIMARY KEY,
    article_id TEXT NOT NULL,
    label TEXT NOT NULL,
    kind TEXT NOT NULL,
    path TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

CREATE TABLE IF NOT EXISTS query_templates (
    query_id TEXT PRIMARY KEY,
    engine TEXT NOT NULL,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    goal TEXT NOT NULL
);
