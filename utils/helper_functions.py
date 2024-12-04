from aocd.examples import Example


def split_to_int(text: str, sep: str = None) -> [int]:
    return [int(x) for x in text.split(sep)]


def generate_example(
    input_data: str = None, answer_a: int = 0, answer_b: int = 0
) -> list[Example]:
    return [
        Example(
            input_data=input_data,
            answer_a=str(answer_a),
            answer_b=str(answer_b),
            extra="",
        )
    ]


def my_sign(x):
    return (x > 0) - (x < 0)
