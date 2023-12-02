import aocd

from utils.fixture import Solution


class Q01(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day, input_transform=lambda x: x)

    def solution_a(self) -> int:
        up = self.input_data.count("(")
        down = len(self.input_data) - up
        floor = up - down
        return floor

    def solution_b(self) -> int:
        ord_sum = 0
        for idx, c in enumerate(self.input_data):
            char_pos = idx + 1
            ord_sum += ord(c)
            if ord_sum / char_pos > 40.5:
                return char_pos


if __name__ == "__main__":
    sol = Q01()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
