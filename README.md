# Watchdog Forensic Fincrime Methods Companion

Companion repo fuer die Watchdog-Serie `Forensic Fincrime`.

Dieses Repo ist bewusst kleiner als das interne Arbeitsrepo. Es soll
interessierten Lesern helfen, die methodische Logik hinter den Artikeln
nachzuvollziehen, ohne interne Arbeitsdateien, Credentials oder private
Zwischenstaende offenzulegen.

## Was dieses Repo enthaelt

- einen oeffentlichen Serienkatalog fuer die aktuellen Artikel
- nachvollziehbare technische Steckbriefe pro Artikel
- ein kleines SQLite-Demo-Setup fuer Serieninventar und Datensatzabdeckung
- Neo4j-Seed-Exports fuer einfache Artikel-Datensatz-Graphen
- Beispielqueries fuer SQLite und Cypher
- Dokumentation zu Architektur, Grenzen und Release-Vorbereitung

## Was dieses Repo bewusst nicht enthaelt

- Credentials oder API-Keys
- interne WordPress- oder Redaktionswerkzeuge
- private HTML-Snapshots, Arbeitsnotizen oder Entwurfsstaende
- Redistribution von Leak-Daten oder Drittanbieter-Datasets
- lokale Arbeitsplatzpfade

## Schnellstart

```bash
cd /path/to/watchdog-forensic-fincrime-methods-companion
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python3 scripts/bootstrap_public_demo.py
```

Der Bootstrap erzeugt lokal:

- `data/processed/forensic_fincrime_public.db`
- `data/processed/neo4j_seed/*.csv`
- `outputs/generated/article_inventory.md`
- `outputs/generated/dataset_coverage.md`
- `outputs/generated/reproducibility_matrix.md`
- `outputs/generated/bootstrap_summary.md`

## Optionale lokale Graph-Ansicht

```bash
docker compose up -d neo4j
```

Danach kann `queries/cypher/load_seed.cypher` im Neo4j Browser geladen werden.
Das Setup bindet Neo4j absichtlich nur an `127.0.0.1` und nutzt `NEO4J_AUTH=none`
nur fuer lokale Entwicklung.

## Artikel in der Serie

- [Panama Paradox](https://watchdog.endvater.de/2026/02/panama-paradox-2/)
- [Panama Paradox II: OpenSanctions x ICIJ](https://watchdog.endvater.de/2026/04/panama-paradox-ii-opensanctions-icij/)
- [Die Weltkarte der Compliance-Schande](https://watchdog.endvater.de/2026/03/die-weltkarte-der-compliance-schande/)
- [Die Shell-Company-Fabrik](https://watchdog.endvater.de/2026/03/die-shell-company-fabrik/)
- [Follow the Bitcoin](https://watchdog.endvater.de/2026/03/follow-the-bitcoin-wie-krypto-das-aml-system-austrickst/)
- [Anatomie Verdachtsmeldung](https://watchdog.endvater.de/2026/02/anatomie-verdachtsmeldung-v2-2/)

## Repo-Prinzip

Das oeffentliche Companion Repo ist kein Vollabzug des internen
Investigations-Setups. Es ist die kuratierte, leserfreundliche Seite der
Recherche:

1. oeffentliche Methode
2. reproduzierbare Struktur
3. klare Grenzen bei Daten, Lizenzen und internen Arbeitsartefakten

Die Trennlinie ist in [docs/publication_boundary.md](docs/publication_boundary.md)
dokumentiert. Vor einer echten Oeffentlichmachung sollte ausserdem die
[Release-Checkliste](docs/release_checklist.md) abgearbeitet werden.
