from typing import Dict, List, Tuple

from .distance import euclidean_distance
from .models import Agent, DeliveryRecord, Package, Warehouse


def simulate_deliveries(
    agents: List[Agent],
    warehouses: List[Warehouse],
    assignments: Dict[str, List[Tuple[Package, float]]],
) -> List[DeliveryRecord]:
    """
    Simulate all assigned deliveries.

    For every package:

        current agent position
            -> warehouse
            -> destination

    After completing a delivery, the agent's current position becomes the
    package destination.

    The assignment itself is NOT recalculated after the agent moves.
    """

    warehouse_map = {
        warehouse.id: warehouse
        for warehouse in warehouses
    }

    agent_map = {
        agent.id: agent
        for agent in agents
    }

    records: List[DeliveryRecord] = []

    for agent_id, assigned_packages in assignments.items():
        agent = agent_map[agent_id]

        for package, assignment_distance in assigned_packages:
            warehouse = warehouse_map[package.warehouse_id]

            # Agent -> warehouse
            warehouse_distance = euclidean_distance(
                agent.location,
                warehouse.location,
            )

            # Warehouse -> destination
            delivery_distance = euclidean_distance(
                warehouse.location,
                package.destination,
            )

            package_total_distance = (
                warehouse_distance + delivery_distance
            )

            agent.total_distance += package_total_distance
            agent.assigned_packages.append(package.id)

            records.append(
                DeliveryRecord(
                    package_id=package.id,
                    agent_id=agent.id,
                    warehouse_id=warehouse.id,
                    assignment_distance=assignment_distance,
                    warehouse_distance=warehouse_distance,
                    delivery_distance=delivery_distance,
                    total_distance=package_total_distance,
                    destination=package.destination,
                )
            )

            # The agent is now located at the destination.
            agent.location = package.destination

    return records