import re

import aocd

from utils.fixture import Solution
from utils.helper_functions import generate_example

# anticipating more instructions in real data for answer b
mul_pattern_a = re.compile(
    r"(?P<instruction>do|dont't|mul)\((?P<op_1>\d+),(?P<op_2>\d+)\)"
)

mul_pattern_b = re.compile(
    r"(?P<instruction>do|don't|mul)\(((?P<op_1>\d+),(?P<op_2>\d+))?\)"
)

# example does not parse right
example = generate_example(
    input_data="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
    answer_a=161,
    answer_b=48,
)


class Day3(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        mul_sum = 0
        for line in self.input_data:
            res = re.finditer(mul_pattern_a, line)
            for r in res:
                mul_sum += int(r.group("op_1")) * int(r.group("op_2"))

        return mul_sum

    def solution_b(self) -> int:
        mul_sum = 0
        mul_enabled = True
        for line in self.input_data:
            res = re.finditer(mul_pattern_b, line)
            for r in res:
                match r.group("instruction"):
                    case "mul":
                        if mul_enabled:
                            mul_sum += int(r.group("op_1")) * int(r.group("op_2"))
                    case "do":
                        mul_enabled = True
                    case "don't":
                        mul_enabled = False

        return mul_sum


if __name__ == "__main__":
    sol = Day3()
    sol.solve_examples(p1_examples=example, p2_examples=example)
    sol.solve_real()
