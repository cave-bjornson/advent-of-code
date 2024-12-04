from itertools import pairwise

import aocd

from utils.fixture import Solution
from utils.helper_functions import split_to_int, my_sign


def check_rules(x, y, former_sign) -> bool:
    level_diff = x - y
    current_sign = my_sign(level_diff)
    if current_sign == 0 or current_sign != former_sign:
        return False

    return 1 <= abs(level_diff) <= 3


class Day2(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        safe_reports = 0
        for line in self.input_data:
            report = split_to_int(line)
            level_pairs = pairwise(report)
            former_sign = my_sign(report[0] - report[1])

            for lvl_pair in level_pairs:
                if not check_rules(lvl_pair[0], lvl_pair[1], former_sign):
                    break
            else:
                safe_reports += 1

        return safe_reports


if __name__ == "__main__":
    sol = Day2()
    sol.solve_examples()
    sol.solve_real()
