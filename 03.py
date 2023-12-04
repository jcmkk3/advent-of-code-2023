from dataclasses import dataclass
from typing import Sequence
import re

INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

symbols = set(r"/-%@+&=$#*")
_nums_pattern = re.compile(r"(\d+)")


@dataclass
class Point:
    x: int
    y: int


def _add_border(schematic: Sequence[str], char: str) -> list[str]:
    top_bottom = char * len(schematic[0])
    schematic = [top_bottom, *schematic, top_bottom]
    schematic = [char + row + char for row in schematic]
    return schematic

def is_adjacent_symbol(point: Point, schematic: Sequence[str]) -> bool:
    for x_offset in [-1, 0, 1]:
        for y_offset in [-1, 0, 1]:
            char = schematic[point.y + y_offset][point.x + x_offset]
            if char != "." and not char.isdigit():
                return True

    return False


def find_part_numbers(schematic: Sequence[str]) -> list[int]:
    schematic = _add_border(schematic, ".")
    part_numbers = []

    for row, line in enumerate(schematic):
        for match in _nums_pattern.finditer(line):
            for col in range(match.start(), match.end()):
                if is_adjacent_symbol(Point(col, row), schematic):
                    part_numbers.append(int(match.group()))
                    break
    
    return part_numbers


def solve1(schematic: Sequence[str]) -> int:
    part_numbers = find_part_numbers(schematic)
    return sum(part_numbers)

with open("input/03.txt") as f:
    schematic = [line.strip() for line in f.readlines()]

print(solve1(schematic))