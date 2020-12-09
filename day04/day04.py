import re
import pathlib
import functools
import operator
import typing

PATTERNS = [
    r"byr:(?P<byr>\d{4})",
    r"iyr:(?P<iyr>\d{4})",
    r"eyr:(?P<eyr>\d{4})",
    r"hgt:(?P<hgt>\d{2,3})(?P<hgt_unit>\w{2})",
    r"ecl:(?P<ecl>\w{3})",
    r"hcl:(?P<hcl>#[a-f0-9]{6})",
    r"pid:(?P<pid>\d{9})",
]


def read_data(input_file: str) -> typing.List:

    # Read as a single string, newlines separated by \n
    p = pathlib.Path(input_file)
    d = p.read_text()

    d = d.split("\n\n")

    # Remove newlines and trailing whitespace
    d = [item.replace("\n", " ").strip() for item in d]

    return d


def is_valid1(data: typing.List[str], required=typing.Set[str]) -> typing.List[str]:

    valid = []
    for item in data:
        is_valid = True

        for req in required:
            if not req in item:
                is_valid = False
                break
        if is_valid:
            valid.append(item)

    return valid


def is_valid2(line: str, patterns=PATTERNS) -> bool:

    keys = {}
    for pattern in patterns:
        if (match := re.search(pattern, line)) is None:
            return False
        else:
            keys = {**keys, **match.groupdict()}

    # BYR
    if not (1920 <= int(keys["byr"]) <= 2002):
        return False

    # IYR
    if not (2010 <= int(keys["iyr"]) <= 2020):
        return False

    # EYR
    if not (2020 <= int(keys["eyr"]) <= 2030):
        return False

    # Height
    if keys["hgt_unit"] == "in":
        if not (59 <= int(keys["hgt"]) <= 76):
            return False
    elif keys["hgt_unit"] == "cm":
        if not (150 <= int(keys["hgt"]) <= 193):
            return False
    else:
        return False

    # ECL
    if not keys["ecl"] in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]):
        return False

    return True


if __name__ == "__main__":

    # Load data
    data = read_data("input.txt")
    # data = read_data("testinput.txt")
    # data = read_data("valid.txt")
    # data = read_data("invalid.txt")

    required = set(
        [
            "byr",
            "iyr",
            "eyr",
            "hgt",
            "hcl",
            "ecl",
            "pid",
        ]
    )

    # Part 1
    valid1 = is_valid1(data, required=required)
    print("Part 1:", len(valid1))

    # Part 2
    # The answer I get is 124, which is one too many: The
    # correct answer is 123. No idea which entry is invalid though
    valid2 = list(filter(is_valid2, data))
    print("Part 2:", len(valid2))
