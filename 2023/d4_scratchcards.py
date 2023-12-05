import aocd

from utils.fixture import Solution


def get_n_matches(card: str) -> int:
    (left, right) = card.split("|")
    my_num = {*right.split()}
    _, winning = left.split(":")
    winning_num = {*winning.split()}
    my_wins = my_num & winning_num
    return len(my_wins)


def recursive(total_cards: int, wins: list[complex]) -> (int, list[complex]):
    if len(wins) == 1:
        return total_cards + int(wins[0].real)
    else:
        n_won = wins.pop()
        n_cards = int(n_won.real)
        matches = int(n_won.imag)
        new_cards = wins[-matches:]
        if matches > 0:
            x = [c + n_cards for c in new_cards]
            wins[-matches:] = x
        return recursive(total_cards + n_cards, wins)


class Day4(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        cards = self.input_data
        points = 0
        for c in cards:
            points += 2 ** (get_n_matches(c) - 1) // 1

        return int(points)

    def solution_b(self) -> int:
        cards = self.input_data
        return recursive(0, [complex(1, get_n_matches(c)) for c in reversed(cards)])


if __name__ == "__main__":
    sol = Day4()
    sol.solve_examples(p1=False)
    sol.solve_real(p1=False)
    sol.solve_performance(10)
