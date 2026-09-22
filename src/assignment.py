from typing import Dict, List, Tuple

from .distance import euclidean_distance
from .models import Agent, Package, Warehouse


def assign_packages(
    agents: List[Agent],
    warehouses: List[Warehouse],
    packages: List[Package],
) -> Dict[str, List[Tuple[Package, float]]]:
    """
    Assign every package to the nearest agent.

    Distance is calculated from the agent's current starting
    location to the package's warehouse.

    If two agents are equally close, the agent with the
    lexicographically smaller ID is selected.

    Returns:
        {
            "A1": [(package_object, assignment_distance), ...],
            "A2": [...],
        }
    """

    # Quick lookup for warehouses and agents.
    warehouse_map = {
        warehouse.id: warehouse
        for warehouse in warehouses
    }

    assignments: Dict[str, List[Tuple[Package, float]]] = {
        agent.id: []
        for agent in agents
    }

    for package in packages:

        # Find the warehouse where this package is located.
        warehouse = warehouse_map[package.warehouse_id]

        candidates = []

        # Calculate distance from every agent to the warehouse.
        for agent in agents:

            distance = euclidean_distance(
                agent.location,
                warehouse.location,
            )

            candidates.append(
                (
                    distance,
                    agent.id,
                    agent,
                )
            )

        # Select nearest agent.
        #
        # First priority  -> shortest distance
        # Second priority -> agent ID for deterministic tie-breaking
        _, _, selected_agent = min(
            candidates,
            key=lambda item: (item[0], item[1]),
        )

        assignment_distance = euclidean_distance(
            selected_agent.location,
            warehouse.location,
        )

        assignments[selected_agent.id].append(
            (
                package,
                assignment_distance,
            )
        )

    # Keep package processing deterministic.
    for agent_id in assignments:
        assignments[agent_id].sort(
            key=lambda item: item[0].id
        )

    return assignments