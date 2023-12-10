import itertools

import aocd

from utils.fixture import Solution
from utils.helper_functions import split_to_int


def extrapolate_seq(seq: list[int], end_sum: int) -> iter:
    if not any(seq):
        return end_sum + seq[-1]
    end_sum += seq[-1]
    new_seq = [y - x for x, y in itertools.pairwise(seq)]
    return extrapolate_seq(new_seq, end_sum)


class Day9(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(
            year,
            day,
            input_transform=lambda x: [
                split_to_int(y) for y in [x for x in x.splitlines()]
            ],
        )

    def solution_a(self) -> int:
        report = self.input_data
        val_sum = 0
        for history in report:
            val_sum += extrapolate_seq(history, 0)

        return val_sum

    def solution_b(self) -> int:
        report = self.input_data
        val_sum = 0
        for history in report:
            line = list(reversed(history))
            val_sum += extrapolate_seq(line, 0)

        return val_sum


if __name__ == "__main__":
    sol = Day9()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
