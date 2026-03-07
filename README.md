# Grundwasser Poing D83 – Home Assistant Bundle

Data feed, historical CSV import, and dashboard cards for **Grundwasserstand Messstelle Poing D 83** (NID Bayern: [gkd.bayern.de](https://www.gkd.bayern.de)).

## Contents

| Path | Description |
|------|-------------|
| `integration/grundwasser.yaml` | REST sensors: level (m ü. NN), level (m u. Gelände), situation |
| `scripts/import-grundwasser-csv-to-recorder.py` | Import historical CSV into the recorder |
| `ui/apex-grundwasser-card.yaml` | ApexCharts card: year comparison (Jan–Dec, multiple years) |
| `ui/tile-grundwasser-situation.yaml` | Tile card: situation with color (green/amber/red) |
| `docs/csv-import.md` | Import instructions and troubleshooting |

## Requirements

- Home Assistant with **REST** and **Recorder** (SQLite)
- **apexcharts-card** (HACS) for the chart
- **card-mod** (HACS) for the situation tile colors
- **Python 3.8+** for the import script (when running outside HA)

## Quick setup

### 1. Data feed (live sensors)

- Copy `integration/grundwasser.yaml` into your HA `config/integrations/` (or include it from `configuration.yaml`).
- Restart Home Assistant and add the integration (or reload REST).
- Entities: `sensor.grundwasser_poing_d83_m_u_nn`, `sensor.grundwasser_poing_d83_m_u_gelande`, `sensor.grundwasser_poing_d83_situation` (your instance may show e.g. `sensor.grundwasser_poing_d83_situation_3` – use the ID from **Developer Tools → States** in the tile config).

### 2. Historical data (optional)

- Get the CSV from [NID Bayern](https://www.nid.bayern.de/grundwasser/inn/poing-d-83-16268/tabelle) (export/historical data) and save as `grundwasser_poing_historie.csv`. Format: `Datum;Grundwasserstand [m ü. NN];Prüfstatus` (header in first 8 lines, data from line 9).
- Put the CSV in `config/www/` so it is served at `/local/grundwasser_poing_historie.csv` (optional; needed for import path below).
- Copy `scripts/import-grundwasser-csv-to-recorder.py` to your HA host (e.g. `config/`).
- Follow **docs/csv-import.md**: stop HA, backup DB, run script with `--dry-run` then without, start HA. Use `--force` if the entity already has newer data and you want to backfill.
- To keep long history, set `recorder.purge_keep_days` to a large value (e.g. 13514) before importing.

### 3. Dashboard cards

- **Chart (year comparison):** In Lovelace, add a card → **Raw configuration** → paste contents of `ui/apex-grundwasser-card.yaml`. Requires **apexcharts-card**.
- **Situation tile:** Add a card → **Raw configuration** → paste contents of `ui/tile-grundwasser-situation.yaml`. Adjust the `entity` (and in `card_mod` the `states('...')` call) if your situation sensor has another ID (e.g. `sensor.grundwasser_poing_d83_situation_3`). Requires **card-mod**.

## CSV format (for import)

- Semicolon-separated; header/metadata in lines 1–8; data from line 9.
- Data rows: `YYYY-MM-DD;value;status` (value with comma as decimal, e.g. `511,22`).
- Rows with empty value are skipped (measurement gaps).

## License

MIT. Data source: Bayerisches Landesamt für Umwelt (LfU), [gkd.bayern.de](https://www.gkd.bayern.de).

MIT. Data source: Bayerisches Landesamt für Umwelt (LfU), [gkd.bayern.de](https://www.gkd.bayern.de).
