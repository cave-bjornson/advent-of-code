import re
from textwrap import dedent

import aocd
from aocd.examples import Example

from utils.fixture import Solution

p2_examples = [
    Example(
        input_data=dedent(
            """\
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen
            """
        ),
        answer_a=None,
        answer_b="281",
        extra=None,
    )
]


class Day1(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        two_dig_num = ""
        cal_val = 0
        for line in self.input_data:
            for c in line:
                if c.isnumeric():
                    two_dig_num += c
                    break

            for c in reversed(line):
                if c.isnumeric():
                    two_dig_num += c
                    break

            cal_val += int(two_dig_num)
            two_dig_num = ""

        return cal_val

    def solution_b(self) -> int:
        dig_dict = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }

        pattern = re.compile(rf"\d|{'|'.join(dig_dict.keys())}")
        reverse_pattern = re.compile(rf"\d|{'|'.join(dig_dict.keys())[::-1]}")
        cal_val = 0
        two_dig_num = ""
        for line in self.input_data:
            first_dig = re.search(pattern, line).group()
            second_dig = re.search(reverse_pattern, line[::-1]).group()[::-1]
            two_dig_num += first_dig if first_dig.isnumeric() else dig_dict[first_dig]
            two_dig_num += (
                second_dig if second_dig.isnumeric() else dig_dict[second_dig]
            )
            cal_val += int(two_dig_num)
            two_dig_num = ""

        return cal_val


if __name__ == "__main__":
    sol = Day1()
    sol.solve_examples(p2_examples=p2_examples)
    sol.solve_real()
    sol.solve_performance(10)
