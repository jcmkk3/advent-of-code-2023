import math
from dataclasses import dataclass

type Milliseconds = int
type Millimeters = int


@dataclass(frozen=True)
class Race:
    time: Milliseconds
    distance: Millimeters

    @property
    def n_winning(self):
        n_winning = 0
        for charge_time in range(self.time):
            distance = (self.time - charge_time) * charge_time
            if distance > self.distance:
                n_winning += 1

        return n_winning


def solve1(document: str) -> int:
    times, distances = [map(int, line.split()[1:]) for line in document.splitlines()]
    races = [Race(time, distance) for time, distance in zip(times, distances)]
    return math.prod(race.n_winning for race in races)


def solve2(document: str) -> int:
    time, distance = [int("".join(line.split()[1:])) for line in document.splitlines()]
    return Race(time, distance).n_winning


with open("input/06.txt") as f:
    document = f.read()


assert solve1(document) == 2065338
assert solve2(document) == 34934171
