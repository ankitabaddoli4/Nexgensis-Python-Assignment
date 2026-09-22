import json
import tempfile
import unittest
from pathlib import Path

from src.assignment import assign_packages
from src.distance import euclidean_distance
from src.loader import load_data
from src.report import build_report
from src.simulator import simulate_deliveries


class TestDistance(unittest.TestCase):

    def test_euclidean_distance(self):
        distance = euclidean_distance(
            (0, 0),
            (3, 4),
        )

        self.assertEqual(distance, 5.0)


class TestDeliverySystem(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "warehouses": [
                {
                    "id": "W1",
                    "location": [0, 0],
                },
                {
                    "id": "W2",
                    "location": [100, 0],
                },
            ],
            "agents": [
                {
                    "id": "A1",
                    "location": [5, 0],
                },
                {
                    "id": "A2",
                    "location": [95, 0],
                },
            ],
            "packages": [
                {
                    "id": "P1",
                    "warehouse_id": "W1",
                    "destination": [10, 10],
                },
                {
                    "id": "P2",
                    "warehouse_id": "W2",
                    "destination": [90, 10],
                },
            ],
        }

    def create_temp_json(self):
        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        )

        json.dump(self.test_data, temp_file)
        temp_file.close()

        return Path(temp_file.name)

    def test_load_data(self):
        path = self.create_temp_json()

        try:
            warehouses, agents, packages = load_data(path)

            self.assertEqual(len(warehouses), 2)
            self.assertEqual(len(agents), 2)
            self.assertEqual(len(packages), 2)

        finally:
            path.unlink(missing_ok=True)

    def test_nearest_agent_assignment(self):
        path = self.create_temp_json()

        try:
            warehouses, agents, packages = load_data(path)

            assignments = assign_packages(
                agents,
                warehouses,
                packages,
            )

            self.assertEqual(
                [item[0].id for item in assignments["A1"]],
                ["P1"],
            )

            self.assertEqual(
                [item[0].id for item in assignments["A2"]],
                ["P2"],
            )

        finally:
            path.unlink(missing_ok=True)

    def test_all_packages_delivered(self):
        path = self.create_temp_json()

        try:
            warehouses, agents, packages = load_data(path)

            assignments = assign_packages(
                agents,
                warehouses,
                packages,
            )

            records = simulate_deliveries(
                agents,
                warehouses,
                assignments,
            )

            self.assertEqual(
                len(records),
                len(packages),
            )

            package_ids = {
                record.package_id
                for record in records
            }

            self.assertEqual(
                package_ids,
                {"P1", "P2"},
            )

        finally:
            path.unlink(missing_ok=True)

    def test_report(self):
        path = self.create_temp_json()

        try:
            warehouses, agents, packages = load_data(path)

            assignments = assign_packages(
                agents,
                warehouses,
                packages,
            )

            records = simulate_deliveries(
                agents,
                warehouses,
                assignments,
            )

            report = build_report(
                agents,
                records,
            )

            self.assertEqual(
                report["A1"]["packages_delivered"],
                1,
            )

            self.assertEqual(
                report["A2"]["packages_delivered"],
                1,
            )

            self.assertIn(
                report["best_agent"],
                {"A1", "A2"},
            )

        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
