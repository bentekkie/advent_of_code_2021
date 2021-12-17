from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def coord(line: str):
    x, y = line.strip().split(",")
    return Point(int(x), int(y))


def parse_instruction(line: str):
    inst, val = line.strip().removeprefix("fold along ").split("=")
    return inst, int(val)


def fold_up(pts: set[Point], val: int):
    for p in pts:
        if p.y < val:
            yield p
        else:
            yield Point(p.x, val - (p.y - val))


def fold_left(pts: set[Point], val: int):
    for p in pts:
        if p.x < val:
            yield p
        else:
            yield Point(val - (p.x - val), p.y)


def fold(pts: set[Point], instruction: tuple[str, int]):
    if instruction[0] == "x":
        yield from fold_left(pts, instruction[1])
    if instruction[0] == "y":
        yield from fold_up(pts, instruction[1])


with open("input.txt") as f:
    grid = {coord(line) for line in f.readlines()}

with open("fold_input.txt") as f:
    instructions = [parse_instruction(line) for line in f.readlines()]
for instruction in instructions:
    grid = {p for p in fold(grid, instruction)}

print(
    "\n".join(
        "".join(
            "X" if Point(x, y) in grid else " "
            for x in range(min(x for x, _ in grid), max(x for x, _ in grid) + 1))
        for y in range(min(y for _, y in grid), max(y for _, y in grid) + 1)))
