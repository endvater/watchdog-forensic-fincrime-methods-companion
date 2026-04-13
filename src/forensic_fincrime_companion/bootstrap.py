from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from textwrap import shorten


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "catalog" / "forensic_fincrime_public.json"
SQLITE_SCHEMA_PATH = REPO_ROOT / "schemas" / "sqlite" / "01_forensic_fincrime_public.sql"
SQLITE_DB_PATH = REPO_ROOT / "data" / "processed" / "forensic_fincrime_public.db"
NEO4J_SEED_DIR = REPO_ROOT / "data" / "processed" / "neo4j_seed"
QUERY_REPORT_DIR = REPO_ROOT / "outputs" / "generated"


def ensure_dirs() -> None:
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    NEO4J_SEED_DIR.mkdir(parents=True, exist_ok=True)
    QUERY_REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def init_sqlite_demo() -> sqlite3.Connection:
    ensure_dirs()
    connection = sqlite3.connect(SQLITE_DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")
    schema = SQLITE_SCHEMA_PATH.read_text(encoding="utf-8")
    connection.executescript(schema)
    populate_sqlite(connection, load_catalog())
    connection.commit()
    return connection


def populate_sqlite(connection: sqlite3.Connection, catalog: dict) -> None:
    connection.executescript(
        """
        DELETE FROM public_assets;
        DELETE FROM reproduction_steps;
        DELETE FROM article_datasets;
        DELETE FROM articles;
        DELETE FROM datasets;
        DELETE FROM query_templates;
        DELETE FROM series;
        """
    )

    series = catalog["series"]
    connection.execute(
        """
        INSERT INTO series(series_id, title, description, series_url)
        VALUES (?, ?, ?, ?)
        """,
        (
            series["id"],
            series["title"],
            series["description"],
            series["series_url"],
        ),
    )

    for dataset in catalog["datasets"]:
        connection.execute(
            """
            INSERT INTO datasets(
                dataset_id, name, category, access_mode, source_url, manual_drop_path, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dataset["id"],
                dataset["name"],
                dataset["category"],
                dataset["access_mode"],
                dataset["source_url"],
                dataset["manual_drop_path"],
                dataset["notes"],
            ),
        )

    for query in catalog["query_templates"]:
        connection.execute(
            """
            INSERT INTO query_templates(query_id, engine, title, file_path, goal)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                query["id"],
                query["engine"],
                query["title"],
                query["file_path"],
                query["goal"],
            ),
        )

    for article in catalog["articles"]:
        connection.execute(
            """
            INSERT INTO articles(
                article_id, series_id, series_order, part_no, title, slug, published_on, url,
                angle, technical_setup, methodology, insight, reproducibility
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article["id"],
                series["id"],
                article["order"],
                article["part_no"],
                article["title"],
                article["slug"],
                article["published_on"],
                article["url"],
                article["angle"],
                article["technical_setup"],
                article["methodology"],
                article["insight"],
                article["reproducibility"],
            ),
        )

        for dataset_id in article["dataset_ids"]:
            connection.execute(
                """
                INSERT INTO article_datasets(article_id, dataset_id, role, is_required)
                VALUES (?, ?, 'primary', 1)
                """,
                (article["id"], dataset_id),
            )

        for index, asset in enumerate(article["public_assets"], start=1):
            connection.execute(
                """
                INSERT INTO public_assets(asset_id, article_id, label, kind, path, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{article['id']}__asset_{index}",
                    article["id"],
                    asset["label"],
                    asset["kind"],
                    asset["path"],
                    asset["status"],
                ),
            )

        for step in article["reproduction_steps"]:
            connection.execute(
                """
                INSERT INTO reproduction_steps(
                    step_id, article_id, step_order, name, summary, is_executable, requires_manual_dataset
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{article['id']}__step_{step['order']}",
                    article["id"],
                    step["order"],
                    step["name"],
                    step["summary"],
                    1 if step["is_executable"] else 0,
                    1 if step["requires_manual_dataset"] else 0,
                ),
            )


def export_neo4j_seed(connection: sqlite3.Connection) -> None:
    export_query_to_csv(
        connection,
        """
        SELECT article_id, title, series_order, COALESCE(part_no, '') AS part_no, url, reproducibility
        FROM articles
        ORDER BY series_order
        """,
        NEO4J_SEED_DIR / "articles.csv",
    )
    export_query_to_csv(
        connection,
        """
        SELECT dataset_id, name, category, access_mode, source_url
        FROM datasets
        ORDER BY name
        """,
        NEO4J_SEED_DIR / "datasets.csv",
    )
    export_query_to_csv(
        connection,
        """
        SELECT article_id, dataset_id, role, is_required
        FROM article_datasets
        ORDER BY article_id, dataset_id
        """,
        NEO4J_SEED_DIR / "article_datasets.csv",
    )


def export_query_to_csv(connection: sqlite3.Connection, query: str, destination: Path) -> None:
    cursor = connection.execute(query)
    fieldnames = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(fieldnames)
        writer.writerows(rows)


def run_query_reports(connection: sqlite3.Connection) -> None:
    query_dir = REPO_ROOT / "queries" / "sqlite"
    for query_path in sorted(query_dir.glob("*.sql")):
        rows, headers = run_sql_file(connection, query_path)
        write_markdown_report(query_path.stem, headers, rows)


def run_sql_file(connection: sqlite3.Connection, query_path: Path) -> tuple[list[tuple], list[str]]:
    cursor = connection.execute(query_path.read_text(encoding="utf-8"))
    rows = cursor.fetchall()
    headers = [column[0] for column in cursor.description]
    return rows, headers


def write_markdown_report(stem: str, headers: list[str], rows: list[tuple]) -> None:
    lines = [f"# {stem.replace('_', ' ').title()}", ""]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        rendered = [shorten("" if value is None else str(value), width=120, placeholder="...") for value in row]
        lines.append("| " + " | ".join(rendered) + " |")
    lines.append("")
    (QUERY_REPORT_DIR / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")


def write_bootstrap_summary(connection: sqlite3.Connection) -> None:
    article_count = connection.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    dataset_count = connection.execute("SELECT COUNT(*) FROM datasets").fetchone()[0]
    manual_only = connection.execute(
        """
        SELECT COUNT(*)
        FROM articles
        WHERE reproducibility IN ('manual_public_data', 'manual_download_data', 'mixed_snapshot')
        """
    ).fetchone()[0]
    summary = "\n".join(
        [
            "# Bootstrap Summary",
            "",
            f"- articles: {article_count}",
            f"- datasets: {dataset_count}",
            f"- articles with manual-data requirements: {manual_only}",
            f"- sqlite_db: {SQLITE_DB_PATH.relative_to(REPO_ROOT)}",
            f"- neo4j_seed_dir: {NEO4J_SEED_DIR.relative_to(REPO_ROOT)}",
            f"- reports_dir: {QUERY_REPORT_DIR.relative_to(REPO_ROOT)}",
            "",
            "This repo ships method and structure, not the original third-party raw datasets.",
            "",
        ]
    )
    (QUERY_REPORT_DIR / "bootstrap_summary.md").write_text(summary, encoding="utf-8")


def bootstrap_all() -> None:
    connection = init_sqlite_demo()
    try:
        export_neo4j_seed(connection)
        run_query_reports(connection)
        write_bootstrap_summary(connection)
    finally:
        connection.close()
