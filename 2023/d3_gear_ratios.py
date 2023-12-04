import re

import aocd

from utils.fixture import Solution
from utils.navigation import (
    Point,
    neighbours_from_point,
    Grid,
)


def generate_neighbour_set(point_set: set[Point], grid):
    return {
        v
        for val in [[*grid.neighbours_from_point(p).values()] for p in point_set]
        for v in val
    } - point_set


def generate_set_dict(pattern, data: list[str]):
    schematic: list[str] = data
    symbols = list[Point]()
    numbers = dict[frozenset, int]()
    for y, line in enumerate(schematic):
        for match in re.finditer(pattern, line):
            if match.group().isdigit():
                point_set = frozenset(Point(x, y) for x in range(*match.span()))
                numbers[point_set] = int(match.group())
            else:
                symbols.append(Point(x=match.span()[0], y=y))

    return numbers, symbols


class Day3(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        pattern = re.compile(r"\d+")
        part_number_sum = 0
        schematic: list[str] = self.input_data
        grid = Grid(
            x_min=0, x_max=len(schematic[0]) - 1, y_min=0, y_max=len(schematic) - 1
        )
        for y, line in enumerate(schematic):
            for match in re.finditer(pattern, line):
                point_set = {Point(x, y) for x in range(*match.span())}
                neighbour_set = generate_neighbour_set(point_set, grid)
                for px, py in neighbour_set:
                    char = schematic[py][px]
                    if not (char.isdigit() or char == "."):
                        part_number_sum += int(match.group())
                        break

        return part_number_sum

    def solution_b(self) -> int:
        pattern = re.compile(r"\*|\d+")
        numbers, gears = generate_set_dict(pattern, self.input_data)
        gear_ratio_sum = 0

        for p in gears:
            neighbour_set = set(neighbours_from_point(p).values())
            gear_numbers = []
            for ps in [*numbers.keys()]:
                if neighbour_set & ps:
                    gear_numbers.append(numbers.pop(ps))
                    if len(gear_numbers) >= 2:
                        gear_ratio = gear_numbers[0] * gear_numbers[1]
                        gear_ratio_sum += gear_ratio
                        break

        return gear_ratio_sum


if __name__ == "__main__":
    sol = Day3()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
