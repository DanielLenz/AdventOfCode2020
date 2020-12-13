from copy import deepcopy
import operator
import functools
import itertools as it
from collections import Counter
from typing import List, Set, Tuple

TEST = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

DIRECTIONS = {
    "N": (0, 1),
    "S": (0, -1),
    "W": (-1, 0),
    "E": (1, 0),
    "NE": (1, 1),
    "NW": (-1, 1),
    "SW": (-1, -1),
    "SE": (1, -1),
}

SEAT_AREA = List[List[str]]


def count_visible(seats: SEAT_AREA, row_idx: int, col_idx: int) -> int:
    nrows, ncols = len(seats), len(seats[0])
    visible = 0

    for name, direction in DIRECTIONS.items():
        new_row_idx = row_idx + direction[1]
        new_col_idx = col_idx + direction[0]
        while (new_row_idx < nrows) and (new_col_idx < ncols) and (new_row_idx >= 0) and (new_col_idx >= 0):

            # print(name, new_row_idx, new_col_idx)
            # If we hit an empty seat, do not increase visible and move to next direction
            if seats[new_row_idx][new_col_idx] == "L":
                break
            # If we hit a seat, increase visible and move to next direction
            if seats[new_row_idx][new_col_idx] == "#":
                visible += 1
                break

            new_row_idx += direction[1]
            new_col_idx += direction[0]

    return visible


def update_conf2(seats: SEAT_AREA) -> SEAT_AREA:
    """For part 2"""
    new_seats = deepcopy(seats)
    nrows, ncols = len(seats), len(seats[0])

    for row_idx, col_idx in it.product(range(nrows), range(ncols)):
        seat = seats[row_idx][col_idx]
        visible = count_visible(seats, row_idx=row_idx, col_idx=col_idx)

        # Empty areas produce occupied seats
        if (seat == "L") and (visible == 0):
            new_seats[row_idx][col_idx] = "#"

        # Full areas empty seats
        if (seat == "#") and (visible >= 5):
            new_seats[row_idx][col_idx] = "L"

    return new_seats


def count_adjacent(seats: SEAT_AREA, row_idx: int, col_idx: int) -> Counter:
    nrows, ncols = len(seats), len(seats[0])
    # print('NN', nrows, ncols)

    adjacent: Counter = Counter()
    for d_col in range(col_idx if col_idx == 0 else -1, 1 if col_idx == ncols else 2):
        for d_row in range(
            row_idx if row_idx == 0 else -1, 1 if row_idx == nrows else 2
        ):
            if d_row == d_col == 0:
                continue
            if col_idx + d_col >= ncols:
                continue
            if row_idx + d_row >= nrows:
                continue

            # print(row_idx + d_row)
            # print(col_idx + d_col)
            adjacent.update(seats[row_idx + d_row][col_idx + d_col])

    return adjacent


def update_conf1(seats: SEAT_AREA) -> SEAT_AREA:
    """For part 1"""
    new_seats = deepcopy(seats)
    nrows, ncols = len(seats), len(seats[0])

    for row_idx, col_idx in it.product(range(nrows), range(ncols)):
        seat = seats[row_idx][col_idx]
        adjacent = count_adjacent(seats, row_idx=row_idx, col_idx=col_idx)

        # Empty areas produce occupied seats
        if (seat == "L") and (adjacent["#"] == 0):
            new_seats[row_idx][col_idx] = "#"

        # Full areas empty seats
        if (seat == "#") and (adjacent["#"] >= 4):
            new_seats[row_idx][col_idx] = "L"

    return new_seats


def count_seats(seats: SEAT_AREA) -> int:
    counter = Counter(functools.reduce(operator.add, seats))

    return counter["#"]


def hash_seats(seats: SEAT_AREA) -> int:
    return hash(tuple(tuple(x) for x in seats))


def print_seats(seats: SEAT_AREA):

    for line in seats:
        print("".join(line))

    print()
    print('-'*80)

def part1(seats: SEAT_AREA) -> int:

    hashes = set()

    while (hash_val := hash_seats(seats)) not in hashes:
        seats = update_conf1(seats)
        hashes.add(hash_val)

        n_seats = count_seats(seats)

    return n_seats


def part2(seats: SEAT_AREA) -> int:

    hashes = set()

    print_seats(seats)
    while (hash_val := hash_seats(seats)) not in hashes:
        seats = update_conf2(seats)
        # print_seats(seats)
        hashes.add(hash_val)

        n_seats = count_seats(seats)

    return n_seats


if __name__ == "__main__":
    test_data = [list(x) for x in TEST.strip().split("\n")]

    with open("input.txt") as f:
        data = [list(x) for x in f.read().strip().split("\n")]

    # Part 1
    assert part1(test_data) == 37
    print("Part 1:", part1(data))

    # Part 2
    assert part2(test_data) == 26
    print("Part 2:", part2(data))
