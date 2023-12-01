import datetime
import timeit
from abc import ABC, abstractmethod

from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()


class Solution(ABC):
    def __init__(
        self,
        year=datetime.date.today().year,
        day=datetime.date.today().day,
        input_data="",
        input_transform=lambda x: x.splitlines(),
    ):
        self.puzzle = Puzzle(year=year, day=day)
        self._input_data = input_data
        self.input_transform = input_transform

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, value):
        self._input_data = self.input_transform(value)

    @abstractmethod
    def solution_a(self) -> int:
        pass

    @abstractmethod
    def solution_b(self) -> int:
        pass

    def solve_examples(self, p1_examples=None, p2_examples=None):
        def print_fail_msg(solution, sample, expected, was):
            print(
                f"Solution {solution} Failed for sample data {sample}. Expected: {expected}, Was {was}"
            )

        p1_examples = p1_examples or self.puzzle.examples
        p2_examples = p2_examples or p1_examples

        for e in p1_examples:
            self.input_data = e.input_data
            if e.answer_a:
                a = self.solution_a()
                if a != int(e.answer_a):
                    print_fail_msg(
                        solution="A", sample=e.input_data, expected=e.answer_a, was=a
                    )
                    break

        for e in p2_examples:
            self.input_data = e.input_data
            if e.answer_b:
                b = self.solution_b()
                if b != int(e.answer_b):
                    print_fail_msg(
                        solution="B", sample=e.input_data, expected=e.answer_b, was=b
                    )
                    break
        else:
            print("All samples passed.")

    def solve_real(self):
        self.input_data = self.puzzle.input_data
        a = self.solution_a()
        b = self.solution_b()
        print(f"Puzzle A:s answer: {a}")
        print(f"Puzzle B:s answer: {b}")

    def solve_performance(self, number=1):
        self.input_data = self.puzzle.input_data
        t_a = timeit.Timer(lambda: self.solution_a()).timeit(number) / number
        t_b = timeit.Timer(lambda: self.solution_b()).timeit(number) / number
        print(f"Solution A average time: {t_a:.3f} seconds.")
        print(f"Solution B average time: {t_b:.3f} seconds.")
