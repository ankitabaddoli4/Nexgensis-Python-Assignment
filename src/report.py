import csv
import json
from pathlib import Path
from typing import Dict, List, Any

from .models import Agent, DeliveryRecord


def build_report(
    agents: List[Agent],
    delivery_records: List[DeliveryRecord],
) -> Dict[str, Any]:
    """
    Build the required delivery report.

    Efficiency is defined as:

        total distance / number of packages delivered

    Lower efficiency means fewer distance units travelled per delivered
    package.
    """

    records_by_agent: Dict[str, List[DeliveryRecord]] = {
        agent.id: []
        for agent in agents
    }

    for record in delivery_records:
        records_by_agent[record.agent_id].append(record)

    report: Dict[str, Any] = {}

    for agent in agents:
        packages_delivered = len(records_by_agent[agent.id])
        total_distance = agent.total_distance

        efficiency = (
            total_distance / packages_delivered
            if packages_delivered > 0
            else 0.0
        )

        report[agent.id] = {
            "packages_delivered": packages_delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": round(efficiency, 2),
        }

    active_agents = [
        agent_id
        for agent_id, details in report.items()
        if details["packages_delivered"] > 0
    ]

    if active_agents:
        # Lower distance per package is considered more efficient.
        best_agent = min(
            active_agents,
            key=lambda agent_id: (
                report[agent_id]["efficiency"],
                agent_id,
            ),
        )
    else:
        best_agent = None

    report["best_agent"] = best_agent

    return report


def save_report(
    report: Dict[str, Any],
    output_path: str | Path,
) -> None:
    """Save report as formatted JSON."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
        )


def save_top_performer_csv(
    report: Dict[str, Any],
    output_path: str | Path,
) -> None:
    """
    Optional bonus:
    Export the top performer to CSV.
    """

    best_agent = report.get("best_agent")

    if not best_agent:
        return

    details = report[best_agent]

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "agent_id",
                "packages_delivered",
                "total_distance",
                "efficiency",
            ],
        )

        writer.writeheader()

        writer.writerow(
            {
                "agent_id": best_agent,
                "packages_delivered": details["packages_delivered"],
                "total_distance": details["total_distance"],
                "efficiency": details["efficiency"],
            }
        )