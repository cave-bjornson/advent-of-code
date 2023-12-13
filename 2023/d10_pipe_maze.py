import itertools

import aocd

from utils.fixture import Solution
from utils.helper_functions import split_to_int, generate_example
from utils.navigation import (
    Point,
    direction_factory,
    pipe_factory,
    neighbours_from_point,
    point_from_direction,
    pipe_exit_direction,
)

SQUARE_LOOP = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

dirs, p_dir, _ = direction_factory(
    direction_names=("N", "S", "E", "W"), end_points=((0, 1), (0, -1), (1, 0), (-1, 0))
)

pipes, p_from_char = pipe_factory(
    pipe_chars=("|", "-", "L", "J", "7", "F"),
    direction_pairs=(
        ((p_dir["N"], p_dir["N"]), (p_dir["S"], p_dir["S"])),
        ((p_dir["E"], p_dir["E"]), (p_dir["W"], p_dir["W"])),
        ((p_dir["S"], p_dir["E"]), (p_dir["W"], p_dir["N"])),
        ((p_dir["S"], p_dir["W"]), (p_dir["E"], p_dir["N"])),
        ((p_dir["N"], p_dir["W"]), (p_dir["E"], p_dir["S"])),
        ((p_dir["N"], p_dir["E"]), (p_dir["W"], p_dir["S"])),
    ),
)


class Day9(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(
            year,
            day,
        )

    def solution_a(self) -> int:
        metal_field = self.input_data
        start_pos = None
        start_dir = None
        for tile_y, field_row in enumerate(metal_field):
            s_x = field_row.find("S")
            if s_x != -1:
                start_pos = Point(x=s_x, y=-tile_y)
                # get start direction:
                for n_d, n_p in neighbours_from_point(start_pos, dirs).items():
                    x, y = n_p
                    adjacent_pipe = p_from_char[metal_field[-y][x]]
                    # check entrance
                    if pipe_exit_direction(adjacent_pipe, n_d):
                        start_dir = n_d
                        break
                else:
                    continue
                break

        # start navigation:
        current_dir = start_dir
        current_pos = start_pos
        steps = 0
        while True:
            steps += 1
            x, y = current_pos = point_from_direction(current_pos, current_dir)
            field_char = metal_field[-y][x]
            if field_char == "S":
                return steps // 2

            current_dir = pipe_exit_direction(p_from_char[field_char], current_dir)

    def solution_b(self) -> int:
        return 0


if __name__ == "__main__":
    sol = Day9()
    sol.solve_examples(p2=False, p1_examples=generate_example(SQUARE_LOOP, answer_a=4))
    sol.solve_real(p2=False)
    sol.solve_performance(p2=False)
