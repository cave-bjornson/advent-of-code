import functools
import itertools
import math
import operator
import re

import aocd

from utils.fixture import Solution
from utils.helper_functions import split_to_int

val_pattern = re.compile(r"(?P<val>\d+) (?P<rgb>[rgb])")
id_pattern = re.compile(r"(?P<id>\d+):")


class Day2(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        order_area = 0
        for line in self.input_data:
            dim = split_to_int(line, "x")
            combinations = itertools.combinations(dim, 2)
            sides = [s for s in itertools.starmap(operator.mul, combinations)]
            slack = min(sides)
            paper_area = sum(sides) * 2
            order_area += paper_area + slack

        return order_area

    def solution_b(self) -> int:
        order_length = 0
        for line in self.input_data:
            dim = split_to_int(line, "x")
            bow = math.prod(dim)
            dim.remove(max(dim))
            ribbon = sum(dim) * 2
            order_length += ribbon + bow

        return order_length


if __name__ == "__main__":
    sol = Day2()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
