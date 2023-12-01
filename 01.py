import re
import string
from typing import Iterable, Mapping

# {"0": "0", "1": "1", ...}
digits = dict(zip(string.digits, string.digits))

# {"zero": "0", "one": "1", ...}
digits_name = dict(
    zip("zero one two three four five six seven eight nine".split(), string.digits)
)


def recover_value(text: str, digits_map: Mapping[str, str]) -> int:
    """Recover an amended calibration value.

    >>> recover_value("1abc2", digits)
    12

    Merge multiple mappings for more complex criteria:
    >>> recover_value("xtwone3four", digits | digits_name)
    24

    """
    pattern = "|".join(digits_map.keys())
    first = re.search(pattern, text).group()
    last = re.search(pattern[::-1], text[::-1]).group()[::-1]  # [::-1] reverses string
    return int(digits_map[first] + digits_map[last])


def solve1(lines: Iterable[str]) -> int:
    return sum(recover_value(line, digits) for line in lines)


def solve2(lines: Iterable[str]) -> int:
    return sum(recover_value(line, digits | digits_name) for line in lines)


with open("input/01.txt") as f:
    lines = f.readlines()

assert solve1(lines) == 54634
assert solve2(lines) == 53855
