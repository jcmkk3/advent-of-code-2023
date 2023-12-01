import re
import string

DIGIT_NAMES = "zero one two three four five six seven eight nine".split()

_lookup = dict()
_lookup |= {name: str(i) for i, name in enumerate(DIGIT_NAMES)}
_lookup |= {name[::-1]: str(i) for i, name in enumerate(DIGIT_NAMES)}
_lookup |= {digit: digit for digit in string.digits}


def recover_value(text: str, pattern) -> int:
    first = re.search(pattern, text).group()
    last = re.search(pattern, text[::-1]).group()

    return int(_lookup[first] + _lookup[last])


def solve1(lines) -> int:
    pattern = re.compile(r"\d")
    return sum(recover_value(line, pattern) for line in lines)


def solve2(lines) -> int:
    pattern = re.compile(r"|".join(_lookup.keys()))
    return sum(recover_value(line, pattern) for line in lines)


with open("input/01.txt") as f:
    lines = f.readlines()

assert solve1(lines) == 54634
assert solve2(lines) == 53855
