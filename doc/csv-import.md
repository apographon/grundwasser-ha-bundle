# Grundwasser CSV → Recorder Import

Import historical data from `grundwasser_poing_historie.csv` into the Home Assistant recorder. This setup targets the **Poing D 83** station; for another station, use the same script but set the script’s `ENTITY_ID` and CSV path to match your sensor and CSV file.

## Prerequisites

- Home Assistant with **SQLite** recorder (default)
- The level entity must already exist (from the REST integration), e.g. `sensor.grundwasser_poing_d83_m_u_nn`
- **Python 3.8+** (on the HA host, e.g. via SSH add-on, or on another machine if you copy the DB and CSV there)
- CSV file: same format as NID Bayern export (`Datum;Grundwasserstand [m ü. NN];Prüfstatus`, data from line 9)

## Where to put files

- **Script:** Copy `scripts/import-grundwasser-csv-to-recorder.py` from this bundle to your HA host, e.g. `/config/`.
- **CSV:** Place the CSV where you can pass its path to the script. Typical: `config/www/grundwasser_poing_historie.csv` so the path is `www/grundwasser_poing_historie.csv` when running from `/config`.
- **DB:** The script writes to `home-assistant_v2.db` (usually in `/config/` on HA OS).

## Steps

1. **Stop Home Assistant** (required so the DB is not locked):
   ```bash
   ha core stop
   ```
2. **Backup the database:**
   ```bash
   cp /config/home-assistant_v2.db /config/home-assistant_v2.db.bak
   ```
3. **Run a dry run** (parse CSV only, no write) to verify:
   ```bash
   cd /config
   python3 import-grundwasser-csv-to-recorder.py www/grundwasser_poing_historie.csv home-assistant_v2.db --dry-run
   ```
   You should see a line like “Parsed N rows” and “would import N states”.
4. **Run the import:**
   ```bash
   python3 import-grundwasser-csv-to-recorder.py www/grundwasser_poing_historie.csv home-assistant_v2.db
   ```
   If the entity already has newer data and you want to backfill history, add `--force`.
5. **Start Home Assistant:**
   ```bash
   ha core start
   ```

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Parse and report only; do not write |
| `--limit N` | Import only the first N rows |
| `--force` | Insert all rows even if entity has newer data (backfill) |

## Recorder purge

With `purge_keep_days: 90`, older imported data will be purged. To keep full history, set `purge_keep_days: 13514` (or similar) in `configuration.yaml` before importing.

## Troubleshooting

- **Entity not found:** Check entity_id in Developer Tools → States; edit `ENTITY_ID` in the script if needed.
- **Database locked:** Ensure HA is stopped before running the script.
- **No data after import:** Run with `--dry-run`; check CSV path and format (`YYYY-MM-DD;value;status`).
