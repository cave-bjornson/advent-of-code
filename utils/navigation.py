import enum
import functools
import math
from collections import namedtuple
from enum import Enum

Point = namedtuple("Point", ["x", "y"])

Direction = Enum(
    "Direction",
    {
        "N": Point(0, 1),
        "NE": Point(1, 1),
        "E": Point(1, 0),
        "SE": Point(1, -1),
        "S": Point(0, -1),
        "SW": Point(-1, -1),
        "W": Point(-1, 0),
        "NW": Point(-1, 1),
    },
)


def point_from_direction(point: Point, direction: Direction) -> Point:
    x, y = direction.value
    return Point(x=point.x + x, y=point.y + y)


def neighbours_from_point(origin: Point) -> dict[Direction, Point]:
    n = dict[Direction, Point]()
    for d in Direction:
        n[d] = point_from_direction(origin, d)

    return n


class Grid:
    def __init__(
        self,
        origin=Point(x=0, y=0),
        x_min=-math.inf,
        x_max=math.inf,
        y_min=-math.inf,
        y_max=math.inf,
    ):
        self.current_position = origin
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    # TODO Check if origin point is within bounds.

    def point_from_direction(
        self, direction: Direction, point: Point = None
    ) -> Point | None:
        if not point:
            point = self.current_position

        new_point = point_from_direction(point, direction)

        if (
            self.x_min <= new_point.x <= self.x_max
            and self.y_min <= new_point.y <= self.y_max
        ):
            return new_point
        else:
            return None

    def neighbours_from_point(self, point=None) -> dict[Direction, Point]:
        if not point:
            point = self.current_position

        n = dict[Direction, Point]()
        for d in Direction:
            n_point = self.point_from_direction(d, point)
            if n_point:
                n[d] = n_point

        return n
