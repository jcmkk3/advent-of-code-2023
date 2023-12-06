from dataclasses import dataclass
from typing import Iterable, Self


@dataclass
class RangeMap:
    ranges: list[range]
    offsets: list[int]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        ranges = []
        offsets = []
        for line in lines:
            dest, src, length = [int(n) for n in line.split()]
            ranges.append(range(src, src + length))
            offsets.append(dest - src)

        return cls(ranges=ranges, offsets=offsets)

    def translate(self, source: int) -> int:
        for range_, offset in zip(self.ranges, self.offsets):
            if source in range_:
                return source + offset

        # If no matches found
        return source


def solve1(text: str) -> int:
    seeds, *maps = text.split("\n\n")
    seeds = [int(seed) for seed in seeds.removeprefix("seeds: ").split()]

    dependencies = []
    range_maps = {}

    for map in maps:
        source, *lines = map.splitlines()
        source, _ = source.split("-", maxsplit=1)
        dependencies.append(source)
        range_maps[source] = RangeMap.from_lines(lines)

    seed_locations = []

    for seed in seeds:
        for source in dependencies:
            seed = range_maps[source].translate(seed)

        seed_locations.append(seed)

    return min(seed_locations)


with open("input/05.txt") as f:
    source_map = f.read()


assert solve1(source_map) == 621354867
