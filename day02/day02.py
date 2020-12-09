import typing
import re


def read_data() -> typing.List[str]:
    with open("input.txt", mode="r") as f:
        d = [line.strip() for line in f.readlines()]

    return d


def parse_entry(s: str) -> typing.Dict:
    pattern = re.compile(
        r"(?P<min_>\d+)\-(?P<max_>\d+) (?P<char>\w): (?P<password>\w+)"
    )

    match = pattern.search(s)

    return match.groupdict()


def is_valid_part1(s: str) -> bool:
    info = parse_entry(s)

    count = int(info["password"].count(info["char"]))

    if int(info["min_"]) <= count <= int(info["max_"]):
        return True
    else:
        return False


def is_valid_part2(s: str) -> bool:
    info = parse_entry(s)

    pos1 = info["password"][int(info["min_"]) - 1]
    pos2 = info["password"][int(info["max_"]) - 1]

    return (pos1 == info["char"]) ^ (pos2 == info["char"])


if __name__ == "__main__":
    test_data = [
        "1-3 a: abcde",
        "1-3 b: cdefg",
        "2-9 c: ccccccccc",
    ]

    data = read_data()

    # Part1
    assert len(list(filter(is_valid_part1, test_data))) == 2
    print("Part 1:", len(list(filter(is_valid_part1, data))))

    # Part 2
    assert len(list(filter(is_valid_part2, test_data))) == 1
    print("Part 2:", len(list(filter(is_valid_part2, data))))
