def split_to_int(text: str, sep: str = " ") -> [int]:
    return [int(x) for x in text.split(sep)]
