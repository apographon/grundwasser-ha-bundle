#!/usr/bin/env python3
"""
Import grundwasser_poing_historie.csv into Home Assistant recorder (states table).

Usage:
  1. Stop Home Assistant: ha core stop
  2. Backup DB: cp /config/home-assistant_v2.db /config/home-assistant_v2.db.bak
  3. Run: python3 import-grundwasser-csv-to-recorder.py <csv> <db> [--force]
  4. Start Home Assistant: ha core start

Options: --dry-run, --limit N, --force (backfill when entity already has newer data).
See doc/csv-import.md in this bundle.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


ENTITY_ID = "sensor.grundwasser_poing_d83_m_u_nn"
ATTRIBUTES_JSON = json.dumps({"unit_of_measurement": "m"})


def parse_csv(csv_path: Path) -> list[tuple[datetime, float]]:
    """Parse CSV, return list of (datetime, value) for rows with valid values."""
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            parts = line.split(";")
            if len(parts) < 2:
                continue
            date_str = parts[0].strip()
            value_str = parts[1].strip()
            if not value_str:
                continue
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                dt = dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            value_str = value_str.replace(",", ".")
            try:
                v = float(value_str)
            except ValueError:
                continue
            if not (400 < v < 600):
                continue
            rows.append((dt, v))
    return rows


def fnv1a32(data: bytes) -> int:
    h = 2166136261
    for b in data:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


def get_or_create_metadata(cursor: sqlite3.Cursor) -> int:
    cursor.execute(
        "SELECT metadata_id FROM states_meta WHERE entity_id = ?", (ENTITY_ID,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO states_meta (entity_id) VALUES (?)", (ENTITY_ID,)
    )
    return cursor.lastrowid


def get_or_create_attributes(cursor: sqlite3.Cursor) -> int:
    attrs_bytes = ATTRIBUTES_JSON.encode("utf-8")
    h = fnv1a32(attrs_bytes)
    cursor.execute(
        "SELECT attributes_id FROM state_attributes WHERE hash = ? AND shared_attrs = ?",
        (h, ATTRIBUTES_JSON),
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO state_attributes (hash, shared_attrs) VALUES (?, ?)",
        (h, ATTRIBUTES_JSON),
    )
    return cursor.lastrowid


def get_max_last_updated(cursor: sqlite3.Cursor, metadata_id: int) -> float | None:
    cursor.execute(
        "SELECT MAX(last_updated_ts) FROM states WHERE metadata_id = ?",
        (metadata_id,),
    )
    row = cursor.fetchone()
    return row[0] if row and row[0] else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import Grundwasser CSV into Home Assistant recorder"
    )
    parser.add_argument("csv", type=Path, help="Path to grundwasser_poing_historie.csv")
    parser.add_argument("db", type=Path, help="Path to home-assistant_v2.db")
    parser.add_argument("--dry-run", action="store_true", help="Parse and report only")
    parser.add_argument("--limit", type=int, default=0, help="Limit rows (0 = all)")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Insert all rows even if entity has newer data (backfill)",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"Error: CSV not found: {args.csv}", file=sys.stderr)
        return 1
    if not args.db.exists():
        print(f"Error: DB not found: {args.db}", file=sys.stderr)
        return 1

    rows = parse_csv(args.csv)
    print(f"Parsed {len(rows)} rows with valid values from {args.csv}")

    if args.limit:
        rows = rows[: args.limit]
        print(f"Limited to {args.limit} rows")

    if not rows:
        print("No data to import.")
        return 0

    if args.dry_run:
        print(f"Dry run: would import {len(rows)} states for {ENTITY_ID}")
        print(f"  Date range: {rows[0][0].date()} to {rows[-1][0].date()}")
        return 0

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    metadata_id = get_or_create_metadata(cursor)
    attributes_id = get_or_create_attributes(cursor)
    existing_max_ts = None if args.force else get_max_last_updated(cursor, metadata_id)

    batch = []
    skipped = 0
    for dt, value in rows:
        ts = dt.timestamp()
        if existing_max_ts is not None and ts <= existing_max_ts:
            skipped += 1
            continue
        state_str = f"{value:.2f}"
        batch.append((metadata_id, state_str, attributes_id, ts, ts, ts, 0))

    cursor.executemany(
        """
        INSERT INTO states (
            metadata_id, state, attributes_id,
            last_updated_ts, last_changed_ts, last_reported_ts,
            origin_idx
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        batch,
    )
    inserted = len(batch)

    conn.commit()
    conn.close()

    print(f"Inserted {inserted} states")
    if skipped:
        print(f"Skipped {skipped} (already in DB or older)")
    print("Done. Restart Home Assistant: ha core start")
    return 0


if __name__ == "__main__":
    sys.exit(main())
