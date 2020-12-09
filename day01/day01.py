import typing


def read_test_data() -> typing.List[int]:
    return [1721, 979, 366, 299, 675, 1456]


def read_data() -> typing.List[int]:
    with open("input.txt") as f:
        d = f.read().strip().split("\n")

        d = list(map(int, d))

    return d


def two_sum(numbers: typing.List[int], target: int) -> int:
    missing: typing.Dict[int, int] = dict()
    for val in numbers:
        if val in missing:
            return val * missing[val]
        else:
            missing[target - val] = val

    return -1


def three_sum(numbers: typing.List[int], target: int) -> int:
    """Find the product of the first set of three numbers that add up
    to the target. If no such triplet is found, return -1"""
    if len(numbers) < 3:
        return -1

    numbers.sort()

    for i, v1 in enumerate(numbers[:-2]):
        needed: typing.Dict[int, int] = dict()
        for v2 in numbers[i + 1 :]:
            if v2 in needed:
                return v1 * v2 * needed[v2]
            else:
                needed[target - v1 - v2] = v2
    return -1


if __name__ == "__main__":

    target = 2020
    numbers = read_data()
    test_numbers = read_test_data()

    # Part 1
    assert two_sum(test_numbers, target=target) == 514579
    print(two_sum(test_numbers, target=target))
    print("Part 1:", two_sum(numbers, target=target))

    # Part 2
    assert three_sum(test_numbers, target=target) == 241861950
    print("Part 2:", three_sum(numbers, target=target))
