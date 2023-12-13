import enum
import functools
import math
from collections import namedtuple
from enum import Enum
from itertools import batched
from typing import NamedTuple

# Point = namedtuple("Point", ["x", "y"])

DIRECTION_NAMES = ("N", "S", "NE", "SW", "E", "W", "SE", "NW")
DIRECTION_CHARS = ("8", "2", "9", "1", "6", "4", "3", "7")
END_POINTS = ((0, 1), (0, -1), (1, 1), (-1, -1), (1, 0), (-1, 0), (1, -1), (-1, 1))
PIPE_CHARS = ("|", "/", "-", "\\")


class Point(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    name: str
    char: str
    end_point: Point


class Pipe(NamedTuple):
    char: str
    path: tuple[Direction, Direction]
    opposite: tuple[Direction, Direction]


def direction_factory(
    direction_names=DIRECTION_NAMES,
    direction_chars=DIRECTION_CHARS,
    end_points=END_POINTS,
):
    directions = [
        Direction(*d) for d in zip(direction_names, direction_chars, end_points)
    ]
    direction_from_name = dict(zip(direction_names, directions))
    direction_from_char = dict(zip(direction_chars, directions))

    return directions, direction_from_name, direction_from_char


def pipe_factory(
    pipe_chars=PIPE_CHARS,
    direction_pairs=batched(direction_factory()[0], 2),
):
    pipes = [
        Pipe(char=char, path=pair[0], opposite=pair[1])
        for char, pair in zip(pipe_chars, direction_pairs)
    ]

    pipe_from_char = dict(zip(pipe_chars, pipes))

    return pipes, pipe_from_char


def pipe_exit_direction(pipe: Pipe, direction: Direction) -> Direction | None:
    if direction == pipe.path[0]:
        return pipe.path[1]
    elif direction == pipe.opposite[0]:
        return pipe.opposite[1]


def point_from_direction(point: Point, direction: Direction) -> Point:
    x, y = direction.end_point
    return Point(x=point.x + x, y=point.y + y)


def neighbours_from_point(origin: Point, directions) -> dict[Direction, Point]:
    n = dict[Direction, Point]()
    for d in directions:
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


if __name__ == "__main__":
    _, p_from_chars = pipe_factory()
    print(p_from_chars)
    p = p_from_chars["|"]
    _, d_from_name, _ = direction_factory()
    print(pipe_exit_direction(p, d_from_name["N"]))
