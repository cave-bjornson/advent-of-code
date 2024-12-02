import aocd

from utils.fixture import Solution
from utils.helper_functions import split_to_int


class Day1(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        left_list = list()
        right_list = list()
        for line in self.input_data:
            left_id, right_id = split_to_int(line)
            left_list.append(left_id)
            right_list.append(right_id)

        left_list.sort()
        right_list.sort()
        paired_ids = zip(left_list, right_list)
        distances = (abs(right_id - left_id) for left_id, right_id in paired_ids)
        return sum(distances)

    def solution_b(self) -> int:
        left_list = list()
        right_list = list()
        for line in self.input_data:
            left_id, right_id = line.split()
            left_list.append(left_id)
            right_list.append(right_id)

        similarity_score = 0
        for left_id in left_list:
            similarity_score += int(left_id) * right_list.count(left_id)

        return similarity_score


if __name__ == "__main__":
    sol = Day1()
    sol.solve_examples()
    sol.solve_real()
