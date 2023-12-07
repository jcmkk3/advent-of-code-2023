import collections
import math
from dataclasses import dataclass
from typing import Self, Sequence


@dataclass(frozen=True)
class ScratchCard:
    card_number: int
    player_numbers: set[int]
    winning_numbers: set[int]

    @classmethod
    def from_str(cls, text: str) -> Self:
        card_number, numbers = text.split(":")
        winning, player = numbers.split(" | ")
        return cls(
            card_number=int(card_number.removeprefix("Card ")),
            player_numbers=set(int(n) for n in player.split()),
            winning_numbers=set(int(n) for n in winning.split()),
        )

    @property
    def n_matching(self) -> set[int]:
        return len(self.player_numbers & self.winning_numbers)

    @property
    def points(self) -> int:
        if self.n_matching <= 1:
            return self.n_matching
        else:
            power = self.n_matching - 1
            return int(math.exp2(power))

    @property
    def cards_won(self) -> set[int]:
        return set(range(self.card_number + 1, self.card_number + self.n_matching + 1))


def total_cards(cards: Sequence[ScratchCard]) -> int:
    n_cards = len(cards)
    q = collections.deque()

    for card in cards:
        q.extend(card.cards_won)

    while q:
        n_cards += 1
        next_card = cards[q.pop() - 1]
        q.extend(next_card.cards_won)

    return n_cards


def solve1(cards: Sequence[ScratchCard]) -> int:
    return sum(card.points for card in cards)


def solve2(cards: Sequence[ScratchCard]) -> int:
    return total_cards(cards)


with open("input/04.txt") as f:
    cards = [ScratchCard.from_str(line) for line in f.readlines()]


solve1(cards) == 25174
solve2(cards) == 6420979
