import functools
import operator
import typing


def read_data(input_file: str) -> typing.List[str]:

    with open(input_file, mode="r") as f:
        d = [line.strip() for line in f.readlines()]

    return d


def count_trees_on_slope(data: typing.List[str], slope: typing.Tuple[int]) -> int:
    sideways, down = slope

    height, width = len(data), len(data[0])

    xpos = 0
    num_trees = 0
    for row in data[::down]:
        if row[xpos % width] == '#':
            num_trees += 1
        xpos += sideways

    return num_trees

if __name__ == "__main__":

    # Load data
    data = read_data("input.txt")
    test_data = read_data("testinput.txt")


    down = 1
    # Positive is to the right
    sideways = +3

    # Part 1
    assert count_trees_on_slope(test_data, slope=(sideways, down)) == 7
    print("Part 1:", count_trees_on_slope(data, slope=(sideways, down)))

    # Part 2
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    test_num_trees = functools.reduce(operator.mul, [count_trees_on_slope(test_data, slope=slope) for slope in slopes])
    assert test_num_trees == 336

    num_trees = [count_trees_on_slope(data, slope=slope) for slope in slopes]
    print("Part 2:", functools.reduce(operator.mul, num_trees))
