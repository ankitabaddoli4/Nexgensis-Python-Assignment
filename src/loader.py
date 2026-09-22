import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .models import Agent, Coordinate, Package, Warehouse


class DataValidationError(ValueError):
    """Raised when input JSON does not satisfy the expected structure."""


def _coordinate(value: Any, field_name: str) -> Coordinate:
    """Validate and convert a coordinate into a numeric tuple."""

    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise DataValidationError(
            f"{field_name} must contain exactly two coordinates."
        )

    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError) as exc:
        raise DataValidationError(
            f"{field_name} must contain numeric coordinates."
        ) from exc


def _parse_warehouses(raw: Any) -> List[Warehouse]:
    """Parse warehouses from dictionary or list representation."""

    warehouses: List[Warehouse] = []

    if isinstance(raw, dict):
        for warehouse_id, location in raw.items():
            warehouses.append(
                Warehouse(
                    id=str(warehouse_id),
                    location=_coordinate(location, f"warehouse {warehouse_id}"),
                )
            )

    elif isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                raise DataValidationError("Each warehouse must be an object.")

            warehouse_id = item.get("id")
            location = item.get("location")

            if warehouse_id is None or location is None:
                raise DataValidationError(
                    "Each warehouse requires 'id' and 'location'."
                )

            warehouses.append(
                Warehouse(
                    id=str(warehouse_id),
                    location=_coordinate(location, f"warehouse {warehouse_id}"),
                )
            )

    else:
        raise DataValidationError("'warehouses' must be an object or list.")

    if not warehouses:
        raise DataValidationError("At least one warehouse is required.")

    return warehouses


def _parse_agents(raw: Any) -> List[Agent]:
    """Parse agents from dictionary or list representation."""

    agents: List[Agent] = []

    if isinstance(raw, dict):
        for agent_id, location in raw.items():
            agents.append(
                Agent(
                    id=str(agent_id),
                    location=_coordinate(location, f"agent {agent_id}"),
                )
            )

    elif isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                raise DataValidationError("Each agent must be an object.")

            agent_id = item.get("id")
            location = item.get("location")

            if agent_id is None or location is None:
                raise DataValidationError(
                    "Each agent requires 'id' and 'location'."
                )

            agents.append(
                Agent(
                    id=str(agent_id),
                    location=_coordinate(location, f"agent {agent_id}"),
                )
            )

    else:
        raise DataValidationError("'agents' must be an object or list.")

    if not agents:
        raise DataValidationError("At least one agent is required.")

    return agents


def _parse_packages(raw: Any) -> List[Package]:
    """Parse packages from the input."""

    if not isinstance(raw, list):
        raise DataValidationError("'packages' must be a list.")

    packages: List[Package] = []

    for item in raw:
        if not isinstance(item, dict):
            raise DataValidationError("Each package must be an object.")

        package_id = item.get("id")

        # Both forms are supported:
        # "warehouse" and "warehouse_id"
        warehouse_id = item.get("warehouse_id", item.get("warehouse"))

        destination = item.get("destination")

        if package_id is None:
            raise DataValidationError("Package requires an 'id'.")

        if warehouse_id is None:
            raise DataValidationError(
                f"Package {package_id} requires a warehouse."
            )

        if destination is None:
            raise DataValidationError(
                f"Package {package_id} requires a destination."
            )

        packages.append(
            Package(
                id=str(package_id),
                warehouse_id=str(warehouse_id),
                destination=_coordinate(
                    destination,
                    f"package {package_id} destination",
                ),
            )
        )

    if not packages:
        raise DataValidationError("At least one package is required.")

    return packages


def load_data(file_path: str | Path) -> Tuple[
    List[Warehouse],
    List[Agent],
    List[Package],
]:
    """
    Load and validate delivery-system data from a JSON file.

    The function deliberately supports both:
      1. Dictionary-based warehouse/agent data.
      2. List-based warehouse/agent data.

    This makes the implementation reusable across the supplied test cases.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() != ".json":
        raise ValueError("Input file must be a JSON file.")

    try:
        with path.open("r", encoding="utf-8") as file:
            data: Dict[str, Any] = json.load(file)
    except json.JSONDecodeError as exc:
        raise DataValidationError(
            f"Invalid JSON in {path}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise DataValidationError("Root JSON value must be an object.")

    required_fields = {"warehouses", "agents", "packages"}
    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise DataValidationError(
            f"Missing required fields: {', '.join(sorted(missing_fields))}"
        )

    warehouses = _parse_warehouses(data["warehouses"])
    agents = _parse_agents(data["agents"])
    packages = _parse_packages(data["packages"])

    warehouse_ids = {warehouse.id for warehouse in warehouses}

    if len(warehouse_ids) != len(warehouses):
        raise DataValidationError("Warehouse IDs must be unique.")

    agent_ids = {agent.id for agent in agents}

    if len(agent_ids) != len(agents):
        raise DataValidationError("Agent IDs must be unique.")

    for package in packages:
        if package.warehouse_id not in warehouse_ids:
            raise DataValidationError(
                f"Package {package.id} references unknown warehouse "
                f"{package.warehouse_id}."
            )

    return warehouses, agents, packages