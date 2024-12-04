import re

import aocd

from utils.fixture import Solution


class Day3(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        mul_sum = 0
        for line in self.input_data:
            # anticipating more instructions in real data for answer b
            mul_pattern = re.compile(
                r"((?P<instruction>mul)\((?P<op_1>\d+),(?P<op_2>\d+)\))"
            )

            res = re.finditer(mul_pattern, line)
            for r in res:
                mul_sum += int(r.group("op_1")) * int(r.group("op_2"))

        return mul_sum


if __name__ == "__main__":
    sol = Day3()
    sol.solve_examples(p1_answer=161)
    sol.solve_real()
