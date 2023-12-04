import math
import re

import aocd

from utils.fixture import Solution
from utils.navigation import Grid, Point, neighbours_from_point

pattern = re.compile(r"\d+")


class Day3(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        schematic: list[str] = self.input_data
        grid = Grid(
            x_min=0, x_max=len(schematic[0]) - 1, y_min=0, y_max=len(schematic) - 1
        )
        part_number_sum = 0
        for y, line in enumerate(schematic):
            for match in re.finditer(pattern, line):
                l_point = Point(match.span()[0], y)
                r_point = Point(match.span()[1] - 1, y)
                l_neighbours = grid.neighbours_from_point(l_point)
                r_neighbours = grid.neighbours_from_point(r_point)
                point_set = set[Point]([*l_neighbours.values(), *r_neighbours.values()])

                for p in point_set:
                    char = schematic[p.y][p.x]
                    if not (char == "." or char.isdigit()):
                        part_number_sum += int(match.group())
                        break

        return part_number_sum

    def solution_b(self) -> int:
        schematic: list[str] = self.input_data
        gear_ratio_sum = 0
        for y, line in enumerate(schematic):
            for match in re.finditer(r"\*", line):
                gear_point = Point(x=match.span()[0], y=y)
                gear_neighbours = neighbours_from_point(gear_point)
                gaps = 0
                number_point_1 = None
                number_point_2 = None
                neighbours = [*gear_neighbours.values()][:-1]
                for p in neighbours:
                    if schematic[p.y][p.x].isdigit():
                        if not number_point_1:
                            number_point_1 = p
                        elif number_point_1 and gaps == 1:
                            if not number_point_2:
                                number_point_2 = p
                    elif number_point_1 and gaps == 0:
                        gaps += 1
                    elif number_point_2 and gaps == 1:
                        gaps += 1
                        break

                if not gaps == 2:
                    continue

                gear_ratio = 1
                for np in (number_point_1, number_point_2):
                    number_line = schematic[np.y]
                    number_start = number_line.rfind(".", 0, np.x) + 1
                    match = re.search(pattern, number_line[number_start:])
                    gear_ratio *= int(match.group())

                gear_ratio_sum += gear_ratio
        print(gear_ratio_sum)
        return gear_ratio_sum
        67250961


if __name__ == "__main__":
    sol = Day3()
    sol.solve_examples(p1=False)
    sol.solve_real(p1=False)
    # sol.solve_performance()
