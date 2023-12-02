import math
import re

import aocd

from utils.fixture import Solution

val_pattern = re.compile(r"(?P<val>\d+) (?P<rgb>[rgb])")
id_pattern = re.compile(r"(?P<id>\d+):")


class Day2(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        bag = int(bytes([12, 13, 14]).hex(), base=16)
        mask = "0000ff"
        id_sum = 0
        for line in self.input_data:
            game_id = int(re.search(id_pattern, line).group("id"))
            rgb_matches = re.finditer(val_pattern, line)
            for m in rgb_matches:
                rgb_chr = m.group("rgb")
                shift = (ord(rgb_chr) - ord("b") + 3) // 8 * 8
                if int(m.group("val")) > (bag >> shift) & int(mask, base=16):
                    break
            else:
                id_sum += game_id

        return id_sum

    def solution_b(self) -> int:
        power_sum = 0
        for line in self.input_data:
            rgb_dict = dict.fromkeys("rgb", 0)
            rgb_matches = re.finditer(val_pattern, line)
            for m in rgb_matches:
                rgb_char = m.group("rgb")
                rgb_val = int(m.group("val"))
                cur_val = rgb_dict[rgb_char]
                if rgb_val > cur_val:
                    rgb_dict[rgb_char] = rgb_val

            power_sum += math.prod(rgb_dict.values())

        return power_sum


if __name__ == "__main__":
    sol = Day2()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
