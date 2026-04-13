# Architecture

This companion repo is intentionally narrower than the internal Watchdog
investigation workspace.

Its job is to make the public method legible:

1. series knowledge
2. dataset inventory
3. public reproduction scaffolding

## Overview

```mermaid
flowchart LR
    Catalog["catalog/forensic_fincrime_public.json"] --> Bootstrap["bootstrap_public_demo.py"]
    Bootstrap --> SQLite["SQLite demo DB<br/>forensic_fincrime_public.db"]
    Bootstrap --> Reports["Markdown query reports"]
    Bootstrap --> Seed["Neo4j seed CSVs"]
    SQLite --> SqlQueries["queries/sqlite/*.sql"]
    Seed --> Neo4j["Optional local Neo4j"]
    Neo4j --> Cypher["queries/cypher/*.cypher"]
    ManualData["Manual drop datasets<br/>not redistributed here"] --> ReaderRuns["Reader-managed reruns"]
    ReaderRuns --> Neo4j
```

## Boundary by design

The internal repo remains the working workshop.

The companion repo only exposes:

- article-level technical framing
- dataset inventory and source references
- demo schemas
- example queries
- public reproducibility levels

It excludes:

- private HTML mirrors
- unpublished drafts
- live credentials
- bulk third-party data redistribution

## Reader workflow

```mermaid
sequenceDiagram
    participant R as Reader
    participant B as Bootstrap
    participant S as SQLite
    participant F as Filesystem
    participant N as Neo4j Seed

    R->>B: python3 scripts/bootstrap_public_demo.py
    B->>S: create schema
    B->>S: insert series, articles, datasets
    B->>F: write markdown reports
    B->>N: export articles.csv and datasets.csv
    R->>F: optionally add manual datasets later
```
