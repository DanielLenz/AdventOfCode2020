from typing import List, Set, Deque, Optional, Tuple
from collections import deque
import itertools as it

RAW = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def part1(lines: List[int], len_history) -> Optional[int]:

    past_products: Deque[Set[int]] = deque()

    # Initial fill
    for start in range(len_history):
        set_ = set(lines[start] + lines[start + i] for i in range(1, len_history))
        past_products.append(set_)

    # Roll through data
    for idx in range(len_history, len(lines) - 1):
        target = lines[idx]
        in_history = False

        # Check if target is in history
        for h in range(len_history):
            if target in past_products[h]:
                in_history = True
                break

        if not in_history:
            return target
            break
        else:
            # Add latest to history
            past_products.append(
                set(lines[idx] + lines[idx + i] for i in range(1, len_history))
            )

            # Pop oldest
            past_products.popleft()

    return None


def part2(d: List[int], target: int) -> Tuple[int]:
    min_size = 2

    window = deque(d[:min_size])
    window_sum = sum(window)

    for i in range(min_size, len(d) - 1):
        # While the sum is too large and there are elements left to remove,
        # remove them.
        while (window_sum > target) and (len(window) > 2):
            first = window.popleft()
            window_sum -= first

        # If we hit the target, return the result
        if window_sum == target:
            return min(window) + max(window)
        else:
            window.append(d[i])
            window_sum += d[i]

    # Only return None if no sequence that
    # adds up to the target is found
    return None


if __name__ == "__main__":

    # Test input
    test_data = RAW.strip().split("\n")
    test_data = [int(n) for n in test_data]

    # Real input
    with open("input.txt") as f:
        data = f.read().strip().split("\n")
        data = [int(n) for n in data]

    # Part 1
    assert part1(test_data, len_history=5) == 127
    target = part1(data, len_history=25)
    print("Part 1:", target)

    # Part 2
    assert part2(test_data, target=part1(test_data, len_history=5))
    result = part2(data, target=target)
    print("Part2: ", result)
