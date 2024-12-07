from functools import singledispatchmethod
from typing import Self, TypeVar, Type

import aocd
from icecream import ic
from plum import dispatch

from utils.fixture import Solution
from utils.helper_functions import split_to_matrix
from utils.navigation import Point, Grid, Actor, Direction, point_from_direction


class Day6(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day, input_transform=split_to_matrix)

    def solution_a(self) -> int:
        lab = Grid(self.input_data)
        start_pos = lab.index("^")
        guard = Actor(position=start_pos, char="^")

        turn_transform = {
            Direction.N: Direction.E,
            Direction.E: Direction.S,
            Direction.S: Direction.W,
            Direction.W: Direction.N,
        }

        walked = set()

        while lab.inside(guard.position):
            ahead_pos = point_from_direction(guard.position, guard.direction)

            if lab.square(ahead_pos) == "#":
                guard.direction = turn_transform[guard.direction]
                continue

            walked.add(guard.position)
            guard.position = ahead_pos

        return len(walked)


if __name__ == "__main__":
    sol = Day6()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
