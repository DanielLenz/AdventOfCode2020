from typing import List, Iterator
from dataclasses import dataclass


RAW = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


@dataclass
class Line:
    cmd: str
    val: int


def part1(lines: List[Line]) -> int:

    total = 0
    idx = 0
    seen = set()

    term = "regular"
    while idx < len(lines):
        line = lines[idx]

        if idx in seen:
            term = "early"
            break

        # Save position
        seen.add(idx)

        # Add
        if line.cmd == "acc":
            total += line.val
            idx += 1
        # Jump
        elif line.cmd == "jmp":
            idx += line.val
        # Pass
        else:
            idx += 1

    return term, total


def get_perms(lines: List[Line]):
    length = len(lines)

    swap_dict = {"nop": "jmp", "jmp": "nop"}
    for i in range(length - 1):
        curr = lines[i]
        if curr.cmd in swap_dict:
            o = (
                lines[:i]
                + [
                    Line(val=curr.val, cmd=swap_dict[curr.cmd]),
                ]
                + lines[i + 1 :]
            )
            yield o


def lines_from_raw(d: List[str]) -> List[Line]:
    lines = []
    for line in d:
        cmd, val = line.split()
        lines.append(Line(cmd=cmd, val=int(val)))

    return lines


if __name__ == "__main__":

    # Test input
    test_data = RAW.strip().split("\n")

    # Real input
    with open("input.txt") as f:
        data = f.read().strip().split("\n")

    test_lines = lines_from_raw(test_data)
    lines = lines_from_raw(data)

    # Part 1
    _, total = part1(test_lines)
    assert total == 5
    print("Part 1:", part1(lines)[1])

    # Part 2
    perms: Iterator = get_perms(lines)

    for perm in perms:
        termination, total = part1(perm)
        if termination == "regular":
            print("Part 2:", total)
            break
