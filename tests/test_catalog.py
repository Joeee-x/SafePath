from __future__ import annotations

import unittest

from app.catalog import filter_records, load_demo_records, summarize_price_observations


class CatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = load_demo_records()

    def test_filters_by_journey_and_channel(self) -> None:
        result = filter_records(
            self.records,
            city="Harbor City",
            service_type="planned",
            channel_type="clinic",
        )
        self.assertEqual([record["record_id"] for record in result], ["DEMO-002"])

    def test_search_uses_public_catalog_fields(self) -> None:
        result = filter_records(self.records, query="remote")
        self.assertEqual([record["record_id"] for record in result], ["DEMO-004"])

    def test_pending_observations_do_not_change_price_range(self) -> None:
        summaries = summarize_price_observations(self.records)
        harbor_urgent = next(
            item
            for item in summaries
            if item["city"] == "Harbor City" and item["service_type"] == "urgent"
        )
        self.assertEqual(harbor_urgent["usable_sample_count"], 0)
        self.assertEqual(harbor_urgent["review_or_excluded_count"], 1)
        self.assertIsNone(harbor_urgent["median_observed_cost"])

    def test_usable_values_are_summarized(self) -> None:
        summary = next(
            item
            for item in summarize_price_observations(self.records)
            if item["city"] == "Harbor City" and item["service_type"] == "planned"
        )
        self.assertEqual(summary["median_observed_cost"], 340.0)
        self.assertEqual(summary["min_observed_cost"], 320.0)
        self.assertEqual(summary["max_observed_cost"], 360.0)


if __name__ == "__main__":
    unittest.main()
