# Installation

## 1. Local Python environment

```bash
cd /path/to/watchdog-forensic-fincrime-companion
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

This repo uses the Python standard library only.

## 2. Bootstrap the public demo

```bash
python3 scripts/bootstrap_public_demo.py
```

Generated locally:

- `data/processed/forensic_fincrime_public.db`
- `data/processed/neo4j_seed/articles.csv`
- `data/processed/neo4j_seed/datasets.csv`
- `data/processed/neo4j_seed/article_datasets.csv`
- `outputs/generated/article_inventory.md`
- `outputs/generated/dataset_coverage.md`
- `outputs/generated/reproducibility_matrix.md`

## 3. Optional local Neo4j

```bash
docker compose up -d neo4j
```

This setup is for localhost development only.
The ports are bound to `127.0.0.1`, and `NEO4J_AUTH=none` is not appropriate
for any publicly reachable environment.

## 4. Manual data drop

This repo documents where a reader can place manually acquired datasets:

- `data/manual_drop/icij_offshore_leaks/`
- `data/manual_drop/opensanctions/`
- `data/manual_drop/companies_house/`
- `data/manual_drop/elliptic_bitcoin/`
- `data/manual_drop/ibm_it_aml_hi_small/`

The repo does not fetch or redistribute these materials automatically.
