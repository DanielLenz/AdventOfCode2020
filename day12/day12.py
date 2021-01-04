from dataclasses import dataclass
from typing import List

TEST = """F10
N3
F7
R90
F11"""


@dataclass
class Line:
    cmd: str
    val: int

    @classmethod
    def from_str(cls, s: str):
        cmd = s[0]
        val = int(s[1:])
        return cls(cmd=cmd, val=val)


@dataclass
class State:
    x: int
    y: int
    angle: int


@dataclass
class WPState:
    x: int
    y: int


@dataclass
class ShipState:
    x: int
    y: int


DIRECTIONS = dict(
    N=(0, 1),
    S=(0, -1),
    W=(-1, 0),
    E=(1, 0),
)


def move(line: Line, state: State):
    dx, dy = DIRECTIONS[line.cmd]
    state.x += dx * line.val
    state.y += dy * line.val

    return state


def rotate(line, state: State):
    if line.cmd == "L":
        state.angle = (state.angle - line.val) % 360
    elif line.cmd == "R":
        state.angle = (state.angle + line.val) % 360
    else:
        raise ValueError("Angle must be in {L, R}")

    return state


def forward(line: Line, state: State):
    """Assuming that the ship can only face exactly north, south, east, west"""

    if state.angle == 0:
        state.x += line.val
    if state.angle == 90:
        state.y -= line.val
    if state.angle == 180:
        state.x -= line.val
    if state.angle == 270:
        state.y += line.val

    return state


def rotate2(line: Line, ship_state: ShipState, wp_state: WPState):
    """Assuming that the ship can only rotate by multiples of 90 degrees"""
    val = line.val if line.cmd == 'L' else 360 - line.val
    div, mod = divmod(val, 90)

    for _ in range(div):
        wp_state.x, wp_state.y = -wp_state.y, wp_state.x

    return ship_state, wp_state


def move2(line: Line, ship_state: ShipState, wp_state: WPState):
    dx, dy = DIRECTIONS[line.cmd]
    wp_state.x += dx * line.val
    wp_state.y += dy * line.val

    return ship_state, wp_state


def forward2(line: Line, ship_state: ShipState, wp_state: WPState):

    ship_state.x += line.val * wp_state.x
    ship_state.y += line.val * wp_state.y

    return ship_state, wp_state


def navigate2(lines: List[Line]):

    ship_state = ShipState(x=0, y=0)
    wp_state = WPState(x=10, y=1)

    instructions = dict(
        N=move2,
        S=move2,
        W=move2,
        E=move2,
        L=rotate2,
        R=rotate2,
        F=forward2,
    )

    for line in lines:
        # print(state)
        instruction = instructions[line.cmd]
        ship_state, wp_state = instruction(line, ship_state, wp_state)

    return ship_state


def navigate(lines: List[Line]):
    # Angle in degrees
    # 0 degrees is east
    # 90 degrees is north
    # 180 degrees is west
    # 270 degrees is south
    state = State(angle=0, x=0, y=0)

    instructions = dict(
        N=move,
        S=move,
        W=move,
        E=move,
        L=rotate,
        R=rotate,
        F=forward,
    )

    for line in lines:
        # print(state)
        instruction = instructions[line.cmd]
        state = instruction(line, state)

    return state


if __name__ == "__main__":

    test_data = [Line.from_str(x) for x in TEST.strip().split("\n")]
    with open("input.txt") as f:
        data = [Line.from_str(x) for x in f.read().strip().split("\n")]

    # Part 1
    final_state = navigate(test_data)
    assert abs(final_state.x) + abs(final_state.y) == 25
    final_state = navigate(data)
    print("Part 1:", final_state)
    print("Distance:", abs(final_state.x) + abs(final_state.y))

    # Part 2
    final_state = navigate2(test_data)
    assert abs(final_state.x) + abs(final_state.y) == 286

    final_state = navigate2(data)
    print("Part 2:", final_state)
    print("Distance:", abs(final_state.x) + abs(final_state.y))
