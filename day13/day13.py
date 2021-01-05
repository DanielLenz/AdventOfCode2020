from functools import reduce
from dataclasses import dataclass
from typing import List, Tuple

TEST = """939
7,13,x,x,59,x,31,19"""



def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part1(schedules: List[int], my_arrival: int) -> int:
    arrival = my_arrival

    while arrival >= 0:
        for bus in schedules:
            div, mod = divmod(arrival, bus)
            if not mod:
                break

        if not mod:
            break
        arrival += 1

    return bus * (arrival - my_arrival)


def parse_lines1(input_lines: str) -> Tuple[int, List]:
    my_arrival, schedules = input_lines.split("\n")
    my_arrival = int(my_arrival)
    schedules = [int(x) for x in schedules.split(",") if x != "x"]

    return my_arrival, schedules

def parse_lines2(lines: str):
    my_arrival, schedules = lines.split("\n")
    schedules = [
        (idx, int(bus)) for idx, bus in enumerate(schedules.split(",")) if bus != "x"
    ]

    factors = [(bus, (bus - i) % bus) for i, bus in schedules]
    return schedules, factors


def part2(factors):
    n, a = zip(*factors)

    return chinese_remainder(n, a)

if __name__ == "__main__":

    test_arr, test_schedules = parse_lines1(TEST)

    with open("input.txt") as f:
        arr, schedules = parse_lines1(f.read().strip())

    print(arr, schedules)

    assert part1(my_arrival=test_arr, schedules=test_schedules) == 295

    p1 = part1(my_arrival=arr, schedules=schedules)
    print("Part1:", p1)

    # Part 2
    schedules, factors = parse_lines2(TEST)
    assert part2(factors) == 1068781

    with open("input.txt") as f:
        schedules, factors = parse_lines2(f.read().strip())

    print("Part2:", part2(factors))
