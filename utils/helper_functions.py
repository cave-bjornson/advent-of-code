def split_to_integers(text: str, sep: str) -> list[int]:
    return [int(x) for x in text.split(sep)]
