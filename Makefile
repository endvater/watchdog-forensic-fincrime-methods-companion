bootstrap:
	python3 scripts/bootstrap_public_demo.py

query-report:
	python3 scripts/run_sqlite_queries.py

export-neo4j:
	python3 scripts/export_neo4j_seed.py
