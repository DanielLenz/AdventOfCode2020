import itertools as it
import pathlib
import functools
import operator
import typing
from dataclasses import dataclass, field


def read_data(input_file: str) -> typing.List[str]:

    # Read as a single string, newlines separated by \n
    with open(input_file) as f:
        d = [line.strip() for line in f.readlines()]

    return d


@dataclass
class Seat:

    row: int
    column: int
    seat_id: field(init=False) = None

    def __post_init__(self):
        self.seat_id = self.row * 8 + self.column

    @classmethod
    def from_string(cls, s: str):
        # Translate to binary string, e.g.
        # 'BFFFBBF' -> '1000110'
        trans = str.maketrans("BFRL", "1010")
        s_binary = s.translate(trans)

        # Extract row and column
        row = int(s_binary[:7], base=2)
        column = int(s_binary[7:], base=2)

        return cls(row=row, column=column)


if __name__ == "__main__":
    d = read_data("input.txt")
    # d = read_data("testinput.txt")

    tickets = [Seat.from_string(line) for line in d]

    # Part 1
    print("Part 1:", max(tickets, key=lambda ticket: ticket.seat_id))

    # Part 2
    # Sort tickets by row and column
    tickets = sorted(tickets, key=lambda ticket: (ticket.row, ticket.column))

    # Look for missing seat ids in the sorted tickets
    for curr, after in it.zip_longest(tickets[:-1], tickets[1:]):
        if curr.seat_id != (after.seat_id - 1):
            print("Part2; SEAT BEFORE YOURS:\n", curr)
