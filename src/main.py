import argparse
import sys
from pathlib import Path

from .assignment import assign_packages
from .loader import DataValidationError, load_data
from .report import (
    build_report,
    save_report,
    save_top_performer_csv,
)
from .simulator import simulate_deliveries


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="FastBox Mystery Delivery System"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input JSON file.",
    )

    parser.add_argument(
        "--output",
        default="output/report.json",
        help="Path for the generated JSON report.",
    )

    parser.add_argument(
        "--csv",
        default=None,
        help="Optional path for top-performer CSV output.",
    )

    return parser


def print_summary(report: dict) -> None:
    """Print a human-readable summary."""

    print("\n" + "=" * 60)
    print("FASTBOX DELIVERY REPORT")
    print("=" * 60)

    for agent_id, details in report.items():
        if agent_id == "best_agent":
            continue

        print(
            f"{agent_id}: "
            f"{details['packages_delivered']} packages | "
            f"{details['total_distance']:.2f} distance | "
            f"{details['efficiency']:.2f} per package"
        )

    print("-" * 60)
    print(f"Best agent: {report['best_agent']}")
    print("=" * 60)


def run(input_path: str, output_path: str, csv_path: str | None) -> dict:
    """Execute the complete delivery simulation."""

    warehouses, agents, packages = load_data(input_path)

    assignments = assign_packages(
        agents=agents,
        warehouses=warehouses,
        packages=packages,
    )

    delivery_records = simulate_deliveries(
        agents=agents,
        warehouses=warehouses,
        assignments=assignments,
    )

    # Required correctness check from the assignment:
    # every input package must be delivered exactly once.
    if len(delivery_records) != len(packages):
        raise RuntimeError(
            "Delivery count mismatch: "
            f"expected {len(packages)}, "
            f"got {len(delivery_records)}."
        )

    delivered_package_ids = [
        record.package_id
        for record in delivery_records
    ]

    if len(set(delivered_package_ids)) != len(packages):
        raise RuntimeError(
            "Duplicate or missing package deliveries detected."
        )

    report = build_report(
        agents=agents,
        delivery_records=delivery_records,
    )

    save_report(
        report=report,
        output_path=output_path,
    )

    if csv_path:
        save_top_performer_csv(
            report=report,
            output_path=csv_path,
        )

    print_summary(report)

    print(f"\nReport saved to: {Path(output_path).resolve()}")

    if csv_path:
        print(f"CSV saved to: {Path(csv_path).resolve()}")

    return report


def main() -> None:
    """CLI entry point."""

    parser = create_parser()
    args = parser.parse_args()

    try:
        run(
            input_path=args.input,
            output_path=args.output,
            csv_path=args.csv,
        )

    except (
        FileNotFoundError,
        DataValidationError,
        ValueError,
        RuntimeError,
    ) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()