import math
from dataclasses import dataclass, field
from typing import Self


@dataclass
class Map:
    instructions: str
    network: dict[str, tuple[str, str]]
    pointer: str
    count: str = field(default=0, init=False)

    @classmethod
    def from_str(cls, text: str, pointer: str) -> Self:
        instructions, _, *nodes = text.strip().splitlines()
        network = {}
        for node in nodes:
            key, choice = node.split(" = ")
            choice = choice.strip("()").split(", ")
            network[key] = choice

        return cls(instructions=instructions, network=network, pointer=pointer)

    def step(self):
        instruction = self.instructions[self.count % len(self.instructions)]
        node = self.network[self.pointer]
        self.pointer = node[instruction == "R"]
        self.count += 1


def solve1(map: Map) -> int:
    while map.pointer != "ZZZ":
        map.step()

    return map.count


def solve2(map: Map) -> int:
    counts = []
    for node in map.network.keys():
        if not node.endswith("A"):
            continue

        map = Map(instructions=map.instructions, network=map.network, pointer=node)
        while not map.pointer.endswith("Z"):
            map.step()

        counts.append(map.count)

    return math.lcm(*counts)


with open("input/08.txt") as f:
    map = Map.from_str(f.read(), "AAA")


assert solve1(map) == 21409
assert solve2(map) == 21165830176709
