from dataclasses import dataclass
import regex as re
from collections import deque
from typing import List, Optional, Dict, Set

TESTINPUT = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

TESTINPUT2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

PATTERN = re.compile(
    r"(?P<main>\w+ \w+) bags contain (?:(?P<num>\d) (?P<sub>\w+ \w+) bags?(?:, )?)*(?:no other bags)?\."
)


@dataclass
class Bag:
    kind: str
    contains: Optional[List[str]] = None
    num_contains: Optional[List[int]] = None

    @classmethod
    def from_line(cls, line):

        match = PATTERN.match(line)
        kind = match.captures("main")[0]

        nums = match.captures("num")
        nums = [int(n) for n in nums]
        subs = match.captures("sub")

        return cls(kind=kind, contains=subs, num_contains=nums)


def dfs(bag: str, target: str):
    # End of tree
    if not BAGS[bag]:
        return 0

    # If already known, stop early
    if bag in SEEN:
        return SEEN[bag]

    # If target is found, return 1
    if target in BAGS[bag]:
        SEEN[bag] = 1
        return 1

    else:
        return max([dfs(b, target=target) for b in BAGS[bag]])


def part1() -> int:
    # Part 1


    score = sum([dfs(bag, target="shiny gold") for bag in BAGS])

    return score


def dfs2(bag: str) -> int:

    # End of tree
    if not BAGS[bag]:
        return 1

    # Return current node plus sum of subtree nodes
    return 1 + sum((num * dfs2(kind) for num, kind in BAGS[bag]))


if __name__ == "__main__":
    d = TESTINPUT2.split("\n")
    with open("input.txt") as f:
        d = f.read().split("\n")[:-1]

    BAGS: Dict[str, List[str]] = dict()
    for line in d:
        bag = Bag.from_line(line)
        BAGS[bag.kind] = [
            (num, kind) for kind, num in zip(bag.contains, bag.num_contains)
        ]

    target = "shiny gold"
    # Part 1
    # I changed the bag structure from part 1 to part 2,
    # now part 1 is broken. Should refactor is anyways.
    # SEEN: Dict[str, int] = dict()
    # score = part1()
    # print("Part 1:", score)

    # Part 2
    score = dfs2(target) - 1
    print("Part 2:", score)
