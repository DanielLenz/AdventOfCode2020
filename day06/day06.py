import typing
import collections
import functools


def load_data(filepath: str) -> typing.List[str]:
    with open(filepath) as f:
        d = [line.strip() for line in f.readlines()]

        return d


def part1(d):
    groups = [set()]
    for line in d:
        if not line:
            groups.append(set())
        else:
            for char in line:
                groups[-1].add(char)

    return sum([len(group) for group in groups])


def part2(d):
    groups = [[]]

    for line in d:
        if not line:
            groups.append([])

        else:
            groups[-1].append(line)

    total = 0
    for group in groups:
        first = set(group[0])
        num_intersection = len(
            first.intersection(*(set(customer) for customer in group[1:]))
        )

        total += num_intersection

    return total


if __name__ == "__main__":

    test_data = load_data("testinput.txt")
    data = load_data("input.txt")

    # Part 1
    assert part1(test_data) == 11
    print("Part 1:", part1(data))

    # Part 2
    assert part2(test_data) == 6
    print("Part 2:", part2(data))
