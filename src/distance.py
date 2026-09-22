import math

from .models import Coordinate


def euclidean_distance(
    point_a: Coordinate,
    point_b: Coordinate,
) -> float:
    """
    Calculate the Euclidean distance between two 2D points.

    Formula:
        distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """

    if len(point_a) != 2 or len(point_b) != 2:
        raise ValueError(
            "Coordinates must contain exactly two values."
        )

    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]

    return math.hypot(dx, dy)


def rounded_distance(
    distance: float,
    digits: int = 2,
) -> float:
    """Round a distance to the requested number of decimal places."""

    return round(distance, digits)