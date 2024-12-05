import datetime
import timeit
from abc import ABC

from aocd.examples import Example
from aocd.models import Puzzle
from dotenv import load_dotenv

from utils.helper_functions import generate_example

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
        print(
            f"Solution for year {self.puzzle.year}, day {self.puzzle.day}, {self.puzzle.title}"
        )
        if not (hasattr(self, "solution_a") or hasattr(self, "solution_b")):
            print("No solutions provided")

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, value):
        if self.input_transform:
            self._input_data = self.input_transform(value)
        else:
            self._input_data = value

    def solve_examples(
        self,
        p1=True,
        p2=True,
        p1_examples=None,
        p2_examples=None,
        p1_answer=None,
        p2_answer=None,
    ):
        def print_fail_msg(solution, sample, expected, was):
            print(
                f"Solution {solution} Failed for sample data {sample}. Expected: {expected}, Was {was}"
            )

        p1_examples: list[Example] = p1_examples or self.puzzle.examples
        p2_examples = p2_examples or self.puzzle.examples

        if p1_answer or p2_answer:
            new_examples = list()
            for e in p1_examples:
                new_examples = generate_example(
                    input_data=e.input_data,
                    answer_a=p1_answer if p1_answer else e.answer_a,
                    answer_b=p2_answer if p2_answer else e.answer_b,
                )
            p1_examples = new_examples
            p2_examples = new_examples

        if p1 and hasattr(self, "solution_a"):
            for e in p1_examples:
                self.input_data = e.input_data
                if e.answer_a:
                    a = self.solution_a()
                    if a != int(e.answer_a):
                        print_fail_msg(
                            solution="A",
                            sample="",
                            expected=e.answer_a,
                            was=a,
                        )
                        break
                else:
                    print("No answer provided for example A")
                    break
            else:
                print(f"Example A Passed with answer {e.answer_a}")

        if p2 and hasattr(self, "solution_b"):
            for e in p2_examples:
                self.input_data = e.input_data
                if e.answer_b:
                    b = self.solution_b()
                    if b != int(e.answer_b):
                        print_fail_msg(
                            solution="B",
                            sample="",
                            expected=e.answer_b,
                            was=b,
                        )
                        break
                else:
                    print("No answer provided for example B")
                    break
            else:
                print(f"Example B passed with answer {e.answer_b}")

    def solve_real(self, p1=True, p2=True):
        self.input_data = self.puzzle.input_data
        if p1 and hasattr(self, "solution_a"):
            a = self.solution_a()
            print(f"Puzzle A:s answer: {a}")
        if p2 and hasattr(self, "solution_b"):
            b = self.solution_b()
            print(f"Puzzle B:s answer: {b}")

    def solve_performance(self, number=1, p1=True, p2=True):
        self.input_data = self.puzzle.input_data
        if p1 and hasattr(self, "solution_a"):
            t_a = timeit.Timer(lambda: self.solution_a()).timeit(number) / number
            print(f"Solution A average time: {t_a:.3f} seconds.")
        if p2 and hasattr(self, "solution_b"):
            t_b = timeit.Timer(lambda: self.solution_b()).timeit(number) / number
            print(f"Solution B average time: {t_b:.3f} seconds.")
