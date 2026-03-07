# Grundwasser CSV → Recorder Import

Import historical data from `grundwasser_poing_historie.csv` into the Home Assistant recorder.

## Prerequisites

- Home Assistant with SQLite recorder; entity `sensor.grundwasser_poing_d83_m_u_nn` (from the REST integration)
- Python 3.8+

## Steps

1. **Stop Home Assistant:** `ha core stop`
2. **Backup DB:** `cp /config/home-assistant_v2.db /config/home-assistant_v2.db.bak`
3. **Run import:**
   ```bash
   cd /config
   python3 import-grundwasser-csv-to-recorder.py www/grundwasser_poing_historie.csv home-assistant_v2.db
   ```
   Use `--force` if the entity already has data and you want to backfill. Use `--dry-run` to test.
4. **Start Home Assistant:** `ha core start`

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
