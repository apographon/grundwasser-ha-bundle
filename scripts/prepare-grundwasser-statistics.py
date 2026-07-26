#!/usr/bin/env python3
"""Prepare GKD daily groundwater values for HA long-term statistics import."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime, timezone
from pathlib import Path


STATISTIC_ID = "sensor.grundwasser_poing_d83_m_u_nn"
MAX_INTERPOLATION_GAP_DAYS = 7


def read_values(source_dir: Path, start_year: int) -> dict[date, float | None]:
    values: dict[date, float | None] = {}
    for path in sorted(source_dir.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = csv.reader(handle, delimiter=";")
            for row in rows:
                if not row or not row[0][:4].isdigit():
                    continue
                try:
                    day = date.fromisoformat(row[0])
                except ValueError:
                    continue
                if day.year < start_year:
                    continue
                values[day] = (
                    float(row[1].replace(",", ".")) if len(row) > 1 and row[1] else None
                )
    return values


def interpolate_short_gaps(
    values: dict[date, float | None],
) -> tuple[dict[date, float], set[date]]:
    result = {day: value for day, value in values.items() if value is not None}
    interpolated: set[date] = set()
    days = sorted(values)
    index = 0
    while index < len(days):
        if values[days[index]] is not None:
            index += 1
            continue
        gap_start = index
        while index < len(days) and values[days[index]] is None:
            index += 1
        gap_days = days[gap_start:index]
        previous_day = days[gap_start - 1] if gap_start else None
        next_day = days[index] if index < len(days) else None
        if (
            len(gap_days) <= MAX_INTERPOLATION_GAP_DAYS
            and previous_day is not None
            and next_day is not None
            and values[previous_day] is not None
            and values[next_day] is not None
        ):
            start_value = float(values[previous_day])
            end_value = float(values[next_day])
            steps = len(gap_days) + 1
            for step, day in enumerate(gap_days, start=1):
                result[day] = round(
                    start_value + (end_value - start_value) * step / steps, 3
                )
                interpolated.add(day)
    return result, interpolated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--start-year", type=int, default=2018)
    parser.add_argument("--chunk-size", type=int, default=750)
    args = parser.parse_args()

    raw = read_values(args.source_dir, args.start_year)
    values, interpolated = interpolate_short_gaps(raw)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = args.output_dir / "grundwasser-poing-d83-statistics.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["date", "value_m_u_nn", "quality"])
        for day, value in sorted(values.items()):
            writer.writerow(
                [day.isoformat(), f"{value:.3f}", "interpolated" if day in interpolated else "official"]
            )

    metadata = {
        "statistic_id": STATISTIC_ID,
        "source": "recorder",
        "name": None,
        "unit_of_measurement": "m",
        "unit_class": "distance",
        "mean_type": 1,
        "has_sum": False,
    }
    statistics = [
        {
            "start": datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc).isoformat(),
            "mean": value,
            "min": value,
            "max": value,
        }
        for day, value in sorted(values.items())
    ]
    for chunk_index in range(0, len(statistics), args.chunk_size):
        payload = {
            "metadata": metadata,
            "stats": statistics[chunk_index : chunk_index + args.chunk_size],
        }
        chunk_path = args.output_dir / f"import-{chunk_index // args.chunk_size + 1:02d}.json"
        chunk_path.write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )

    print(
        json.dumps(
            {
                "first": min(values).isoformat(),
                "last": max(values).isoformat(),
                "statistics": len(statistics),
                "interpolated": len(interpolated),
                "chunks": (len(statistics) + args.chunk_size - 1) // args.chunk_size,
                "csv": str(csv_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
