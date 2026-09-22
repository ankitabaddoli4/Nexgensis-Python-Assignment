from dataclasses import dataclass, field
from typing import List, Tuple


Coordinate = Tuple[float, float]


@dataclass(frozen=True)
class Warehouse:
    """Represents a warehouse and its coordinates."""

    id: str
    location: Coordinate


@dataclass
class Package:
    """Represents a package that must be delivered."""

    id: str
    warehouse_id: str
    destination: Coordinate


@dataclass
class Agent:
    """Represents a delivery agent."""

    id: str
    location: Coordinate
    assigned_packages: List[str] = field(default_factory=list)
    total_distance: float = 0.0


@dataclass(frozen=True)
class DeliveryRecord:
    """Represents one completed package delivery."""

    package_id: str
    agent_id: str
    warehouse_id: str
    assignment_distance: float
    warehouse_distance: float
    delivery_distance: float
    total_distance: float
    destination: Coordinate