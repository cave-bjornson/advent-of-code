import re
from collections import defaultdict

import aocd

from utils.fixture import Solution


def hash_algorithm(string: str):
    cur_val = 0
    for c in string:
        cur_val += ord(c)
        cur_val *= 17
        cur_val %= 256

    return cur_val


lens_pattern = re.compile(r"([a-z]+)([=-])([1-9])?")


class Day15(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day, input_transform=lambda x: x.split(","))

    def solution_a(self) -> int:
        result = 0
        ascii_strings = self.input_data
        for s in ascii_strings:
            result += hash_algorithm(s)

        return result

    def solution_b(self) -> int:
        ascii_strings = self.input_data
        boxes = defaultdict[int, dict](dict[str, int])

        for s in ascii_strings:
            lbl, op, focal_len = re.match(pattern=lens_pattern, string=s).groups()
            box_n = hash_algorithm(lbl)
            if op == "=":
                boxes[box_n] |= {lbl: int(focal_len)}
            else:
                boxes[box_n].pop(lbl, None)

        sum_power = 0
        for box_n, box in boxes.items():
            for slot_idx, slot in enumerate(box.items()):
                _, focal_len = slot
                sum_power += (1 + box_n) * (slot_idx + 1) * focal_len

        return sum_power


if __name__ == "__main__":
    sol = Day15()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
