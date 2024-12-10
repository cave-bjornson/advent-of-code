import aocd

from utils.fixture import Solution


class Day7(Solution):
    def __init__(self):
        day, year = aocd.get_day_and_year()
        super().__init__(year, day)

    def solution_a(self) -> int:
        def get_normalized_bit(value, bit_index):
            return (value >> bit_index) & 1

        # equations = [
        #     (int(test_val), [int(cn) for cn in cal_numbers.split()])
        #     for test_val, cal_numbers in [
        #         cal_eq.split(":") for cal_eq in self.input_data
        #     ]
        # ]

        operations = [lambda x, y: x * y, lambda x, y: x + y]

        total_cal_result = 0
        for cal_eq in self.input_data:
            test_val, cal_numbers = cal_eq.split(":")
            test_val = int(test_val)
            cal_numbers = [int(cn) for cn in cal_numbers.split()]
            size = 2 ** (len(cal_numbers) - 1)
            for i in range(size):
                n_sum = cal_numbers[0]
                for j in range(len(cal_numbers) - 1):
                    op_index = get_normalized_bit(i, j)
                    n_sum = operations[op_index](n_sum, cal_numbers[j + 1])
                if n_sum == test_val:
                    total_cal_result += n_sum
                    break

        return total_cal_result


if __name__ == "__main__":
    sol = Day7()
    sol.solve_examples()
    sol.solve_real()
    sol.solve_performance()
