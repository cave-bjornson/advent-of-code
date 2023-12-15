import aocd

from utils.fixture import Solution


class Day15(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(
            year,
            day,
        )

    def solution_a(self) -> int:
        return 0

    def solution_b(self) -> int:
        return 0


if __name__ == "__main__":
    sol = Day15()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
