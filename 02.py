from dataclasses import dataclass
from typing import Iterable, Self


@dataclass
class Cubeset:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_str(cls, text: str) -> Self:
        cubes = {color: int(n) for n, color in map(str.split, text.split(","))}
        return Cubeset(**cubes)

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass
class Game:
    id: int
    red: list[int]
    green: list[int]
    blue: list[int]

    @classmethod
    def from_str(cls, line: str) -> Self:
        id, plays = line.split(":", maxsplit=1)
        game = cls(id=int(id.removeprefix("Game ")), red=[], green=[], blue=[])
        rounds = plays.split(";")
        for round in rounds:
            game.add_round(Cubeset.from_str(round))

        return game

    def add_round(self, cubeset: Cubeset):
        for color in ["red", "green", "blue"]:
            getattr(self, color).append(getattr(cubeset, color))

    def is_valid_cubeset(self, cubeset: Cubeset) -> bool:
        return (
            cubeset.red >= max(self.red)
            and cubeset.green >= max(self.green)
            and cubeset.blue >= max(self.blue)
        )

    @property
    def minimum_cubeset(self) -> Cubeset:
        return Cubeset(red=max(self.red), green=max(self.green), blue=max(self.blue))


def solve1(games: Iterable[Game]) -> int:
    cubeset = Cubeset(red=12, green=13, blue=14)
    return sum(game.id for game in games if game.is_valid_cubeset(cubeset))


def solve2(games: Iterable[Game]) -> int:
    return sum(cubeset.minimum_cubeset.power for cubeset in games)


with open("input/02.txt") as f:
    games = [Game.from_str(line) for line in f.readlines()]

assert solve1(games) == 2545
assert solve2(games) == 78111
