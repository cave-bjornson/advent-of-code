import os
from enum import StrEnum, auto

from plum import dispatch


class Direction(StrEnum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


class Turn(StrEnum):
    Right = auto()
    Left = auto()


def turn(direction: Direction, turn: Turn) -> Direction:
    right_turn = {
        Direction.N: Direction.E,
        Direction.E: Direction.S,
        Direction.S: Direction.W,
        Direction.W: Direction.N,
    }

    left_turn = {
        Direction.N: Direction.W,
        Direction.W: Direction.S,
        Direction.S: Direction.E,
        Direction.E: Direction.N,
    }

    return right_turn[direction] if turn.Right else left_turn[direction]


class Grid:
    def __init__(self, matrix):
        self.matrix: list[list[str]] = matrix

    @dispatch
    def square(self, point: "Point") -> str | None:
        if self.inside(point):
            return self.matrix[len(self.matrix) - 1 - point.y][point.x]
        else:
            return None

    @dispatch
    def square(self, x=0, y=0) -> str | None:
        if self.inside(x, y):
            return self.matrix[len(self.matrix) - 1 - y][x]
        else:
            return None

    def set_square(self, point: "Point", value: str):
        self.matrix[len(self.matrix) - 1 - point.y][point.x] = value

    @dispatch
    def inside(self, point: "Point") -> bool:
        return 0 <= point.x < len(self.matrix[0]) and 0 <= point.y < len(self.matrix)

    @dispatch
    def inside(self, x=0, y=0) -> bool:
        return 0 <= x < len(self.matrix[0]) and 0 <= y < len(self.matrix)

    def index(self, value):
        for y, row in enumerate(self.matrix):
            if value in row:
                return Point(x=row.index(value), y=len(self.matrix) - 1 - y)

    def __repr__(self):
        return f"Grid({self.matrix})"

    def __str__(self):
        return os.linesep.join("".join(row) for row in self.matrix)


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __eq__(self, __value):
        return self.x == __value.x and self.y == __value.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    @dispatch
    def __add__(self, other: "Point"):
        return Point(self.x + other.x, self.y + other.y)

    @dispatch
    def __add__(self, other: tuple[int, int]):
        return Point(self.x + other[0], self.y + other[1])

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class Actor:
    def __init__(self, position=Point(), char="@"):
        self.position = position
        self.direction = Direction.N
        self.char = char

    def __repr__(self):
        return f"Actor(position={self.position}, direction={self.direction}, char={self.char})"


def point_from_direction(point: Point, direction: Direction):
    transform = {
        Direction.N: (0, 1),
        Direction.E: (1, 0),
        Direction.S: (0, -1),
        Direction.W: (-1, 0),
    }

    return point + transform[direction]


def test_point_from_direction():
    p = Point()
    np = point_from_direction(p, Direction.N)
    ep = point_from_direction(p, Direction.E)
    sp = point_from_direction(p, Direction.S)
    wp = point_from_direction(p, Direction.W)
    assert np == Point(0, 1)
    assert ep == Point(1, 0)
    assert sp == Point(0, -1)
    assert wp == Point(-1, 0)


def test_add_point_to_point():
    p1 = Point()
    p2 = Point(1, 1)
    p3 = p1 + p2
    p4 = p1 + (1, 2)
    assert p3.x == 1 and p3.y == 1
    assert p4.x == 1 and p4.y == 2


def test_point_unpacking():
    p1 = Point()
    x, y = p1
    assert x == 0 and y == 0


def test_grid_square():
    g = Grid([["s"]])
    p = Point()
    s = g.square(p)
    assert s == "s"
    s = g.square(0, 0)
    assert s == "s"
