import typing
import numpy as np
from collections import Counter

TEST1 = """16
10
15
5
1
11
7
19
6
12
4"""

TEST2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


def part1(data: typing.List[int]) -> int:
    diffs = np.diff(sorted(data))

    counter = Counter(diffs)
    # Add min
    counter[min(data)] += 1
    # Last element
    counter[3] += 1

    return counter


def dp(i: int):

    if i == len(data) - 1:
        return 1

    if i in DP:
        return DP[i]

    ans = 0

    for j in range(i + 1, len(data)):
        if data[j] - data[i] <= 3:
            ans += dp(j)

    DP[i] = ans

    return ans


if __name__ == "__main__":
    test_data1 = [int(x) for x in TEST1.strip().split("\n")]
    test_data2 = [int(x) for x in TEST2.strip().split("\n")]

    with open("input.txt") as f:
        data = [int(x) for x in f.read().strip().split("\n")]

    # Part 1
    expected_jolts = 22 * 10
    test_out = part1(test_data2)
    assert test_out[1] * test_out[3] == expected_jolts

    print("Part 1:", p1_out := part1(data))
    print("Part1:", p1_out[1] * p1_out[3])

    # Part 2
    data.append(0)
    data.append(max(data)+3)
    data.sort()

    test_data2.append(0)
    test_data2.append(max(test_data2)+3)
    test_data2.sort()

    # data = test_data2

    # Use DP to get the number of possible ways
    # to get to position i
    DP = {}
    print(dp(0))

