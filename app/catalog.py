"""Core read model used by the sanitized SafePath portfolio sample.

The production project keeps operational records private.  This module works only
with the fictional, contact-free records committed in this repository.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEMO_DATA_PATH = PROJECT_ROOT / "data" / "demo_records.json"


def load_demo_records(path: Path = DEMO_DATA_PATH) -> list[dict[str, Any]]:
    """Load the deliberately fictional data that accompanies this code sample."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload["records"]
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    return records


def filter_records(
    records: Iterable[dict[str, Any]],
    *,
    city: str | None = None,
    service_type: str | None = None,
    channel_type: str | None = None,
    query: str | None = None,
) -> list[dict[str, Any]]:
    """Return catalog records that match the supplied discovery filters.

    Search deliberately operates on non-contact fields only, so a public client
    never needs to receive personal or provider contact information.
    """
    normalized_query = (query or "").strip().lower()
    result: list[dict[str, Any]] = []

    for record in records:
        if city and record["city"] != city:
            continue
        if service_type and record["service_type"] != service_type:
            continue
        if channel_type and record["channel_type"] != channel_type:
            continue

        searchable = " ".join(
            str(record[field])
            for field in ("label", "city", "district", "service_type", "channel_type")
        ).lower()
        if normalized_query and normalized_query not in searchable:
            continue
        result.append(record)

    return sorted(result, key=lambda item: (item["city"], item["label"]))


def summarize_price_observations(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Summarize usable observations without turning pending data into a claim.

    `needs_review` rows remain visible in a separate count but do not affect the
    median, minimum, or maximum.  This distinction was important to the product:
    it prevents a small, unverified sample from presenting itself as current fact.
    """
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["city"], record["service_type"])].append(record)

    summaries: list[dict[str, Any]] = []
    for (city, service_type), group in grouped.items():
        usable_values = [
            float(item["observed_cost"])
            for item in group
            if item["record_status"] == "usable" and item["observed_cost"] is not None
        ]
        summaries.append(
            {
                "city": city,
                "service_type": service_type,
                "total_records": len(group),
                "usable_sample_count": len(usable_values),
                "review_or_excluded_count": len(group) - len(usable_values),
                "median_observed_cost": median(usable_values) if usable_values else None,
                "min_observed_cost": min(usable_values) if usable_values else None,
                "max_observed_cost": max(usable_values) if usable_values else None,
            }
        )
    return sorted(summaries, key=lambda item: (item["city"], item["service_type"]))


if __name__ == "__main__":
    for summary in summarize_price_observations(load_demo_records()):
        print(summary)
