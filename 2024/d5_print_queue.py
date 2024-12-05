from collections import defaultdict, deque

import aocd
from icecream import ic

from utils.fixture import Solution
from utils.helper_functions import split_two_sections


def page_dict_and_list(input_data):
    page_ordering_rules, update_sequence = input_data
    rule_dict = defaultdict(set)
    for line in page_ordering_rules:
        before, after = line.split("|")
        rule_dict[before].add(after)

    update_sequence_list = [line.split(",") for line in update_sequence]

    return rule_dict, update_sequence_list


class Day5(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(
            year, day, input_transform=lambda x: split_two_sections(x, sep="\n\n")
        )

    def solution_a(self) -> int:
        rule_dict, update_sequence = page_dict_and_list(self.input_data)

        mid_pages_sum = 0
        for line in update_sequence:
            update_q = deque(line)
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

    def solution_b(self) -> int:
        rule_dict, update_sequence = page_dict_and_list(self.input_data)

        corrections = list()
        for line in update_sequence:
            update_q = deque(line)
            right_order = True
            while len(update_q) > 1 and right_order:
                current_page = update_q.popleft()
                for page in update_q:
                    right_order = page in rule_dict[current_page]
                    if not right_order:
                        corrections.append(line)
                        break

        mid_page_sum = 0
        for line in corrections:
            correction_q = deque(line)
            corrected = list()
            while correction_q:
                current_page = correction_q.popleft()
                for page in correction_q:
                    if page not in rule_dict[current_page]:
                        correction_q.append(current_page)
                        break
                else:
                    corrected.append(current_page)
            mid_page_sum += int(corrected[len(corrected) // 2])

        return mid_page_sum


if __name__ == "__main__":
    sol = Day5()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
