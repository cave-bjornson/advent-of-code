import re

import aocd

from utils.fixture import Solution
from utils.helper_functions import generate_example

example = generate_example(
    input_data="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""",
    answer_a=18,
    answer_b=48,
)


def make_diagonal(array):
    horizontal_length = len(array[0])
    vertical_length = len(array)

    diagonal = list()
    for c in range(horizontal_length - 3):
        diagonal.append(
            [
                array[0 + t][c + t]
                for t in range(
                    vertical_length - max(0, c - (horizontal_length - vertical_length))
                )
            ]
        )

    for line in range(1, vertical_length - 3):
        diagonal.append([array[line + t][0 + t] for t in range(vertical_length - line)])

    for col_idx, line in enumerate(diagonal):
        diagonal[col_idx] = "".join(line)

    return diagonal


class Day4(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        horizontal_length = len(self.input_data[0])
        vertical = [list() for _ in range(horizontal_length)]

        for row_idx, row in enumerate(self.input_data):
            for col_idx, col in enumerate(row):
                vertical[col_idx].append(col)

        for col_idx, line in enumerate(vertical):
            vertical[col_idx] = "".join(reversed(line))

        x_diagonal = make_diagonal(self.input_data)
        y_diagonal = make_diagonal(vertical)

        combined = ",".join([*self.input_data, *vertical, *x_diagonal, *y_diagonal])

        xmas_count = combined.count("XMAS") + combined.count("SAMX")

        return xmas_count


if __name__ == "__main__":
    sol = Day4()
    sol.solve_examples(p1_examples=example)
    sol.solve_real()
