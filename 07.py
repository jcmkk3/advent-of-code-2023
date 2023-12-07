import collections
import itertools
import operator
from dataclasses import dataclass, field
from enum import IntEnum, auto
from functools import total_ordering
from typing import Iterable


class HandType(IntEnum):
    """Possible types of hands ordered lowest to highest"""

    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_KIND = auto()
    FIVE_OF_KIND = auto()


def determine_type(cards: list[str]) -> str:
    counts = list(sorted(collections.Counter(cards).values(), reverse=True))
    match counts:
        case [5, *_]:
            return HandType.FIVE_OF_KIND
        case [4, *_]:
            return HandType.FOUR_OF_KIND
        case [3, 2, *_]:
            return HandType.FULL_HOUSE
        case [3, *_]:
            return HandType.THREE_OF_KIND
        case [2, 2, *_]:
            return HandType.TWO_PAIR
        case [2, *_]:
            return HandType.ONE_PAIR
        case [1, 1, 1, 1, 1]:
            return HandType.HIGH_CARD
        case _:
            raise ValueError


@total_ordering
@dataclass
class Hand:
    cards: str
    type: HandType = field(init=False)
    ranks = "23456789TJQKA"

    def __post_init__(self):
        self.type = determine_type(self.cards)

    def __lt__(self, other):
        if self.type < other.type:
            return True
        elif self.type == other.type:
            for card1, card2 in zip(self.cards, other.cards):
                if self.ranks.find(card1) < self.ranks.find(card2):
                    return True
                elif card1 == card2:
                    continue
                else:
                    return False
        else:
            return False


class HandJoker(Hand):
    ranks = "J23456789TQKA"

    def __post_init__(self):
        n_jokers = self.cards.count("J")

        if n_jokers == 0:
            self.type = determine_type(self.cards)
        else:
            cards = self.cards.replace("J", "")
            ranks = self.ranks.replace("J", "")
            combos = [
                "".join(combo)
                for combo in itertools.combinations_with_replacement(ranks, n_jokers)
            ]
            self.type = max(determine_type(combo + cards) for combo in combos)


def total_winnings(hands: Iterable[Hand]) -> int:
    ranked_hands = sorted(hands, key=operator.itemgetter(0))
    return sum(rank * bid for rank, (_, bid) in enumerate(ranked_hands, start=1))


def solve1(lines: Iterable[str]) -> int:
    hands = [(Hand(cards), int(bid)) for cards, bid in map(str.split, lines)]
    return total_winnings(hands)


def solve2(lines: Iterable[str]) -> int:
    hands = [(HandJoker(cards), int(bid)) for cards, bid in map(str.split, lines)]
    return total_winnings(hands)


with open("input/07.txt") as f:
    lines = f.readlines()

assert solve1(lines) == 250120186
assert solve2(lines) == 250665248
