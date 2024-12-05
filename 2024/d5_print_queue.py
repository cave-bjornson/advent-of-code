from collections import defaultdict, deque

import aocd

from utils.fixture import Solution
from utils.helper_functions import split_two_sections


class Day5(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(
            year, day, input_transform=lambda x: split_two_sections(x, sep="\n\n")
        )

    def solution_a(self) -> int:
        page_ordering_rules, update_sequence = self.input_data
        rule_dict = defaultdict(set)
        for line in page_ordering_rules:
            before, after = line.split("|")
            rule_dict[before].add(after)

        mid_pages_sum = 0
        for line in update_sequence:
            update_q = deque(line.split(","))
            middle_page = update_q[len(update_q) // 2]
            right_order = True
            while len(update_q) > 1 and right_order:
                current_page = update_q.popleft()
                for page in update_q:
                    right_order = page in rule_dict[current_page]
                    if not right_order:
                        break

            if right_order:
                mid_pages_sum += int(middle_page)

        return mid_pages_sum


if __name__ == "__main__":
    sol = Day5()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
