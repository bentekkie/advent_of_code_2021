from dataclasses import dataclass

with open("input.txt") as f:
    octs = [[int(x) for x in line.strip()] for line in f.readlines()]

def neighbours(i,j):
    if i > 0:
        yield (i - 1, j)
    if j > 0:
        yield (i, j - 1)
    if i > 0 and j > 0:
        yield (i - 1, j - 1)
    if i + 1 < len(octs):
        yield (i + 1, j)
    if j + 1 < len(octs[i]):
        yield (i, j + 1)
    if i + 1 < len(octs) and j + 1 < len(octs[i]):
        yield (i + 1, j + 1)
    if i > 0 and j + 1 < len(octs[i]):
        yield (i - 1, j + 1)
    if j > 0 and i + 1 < len(octs):
        yield (i + 1, j - 1)


def get_flashable():
    for i in range(len(octs)):
        for j in range(len(octs[i])):
            if octs[i][j] > 9:
                yield (i,j)

def print_oct():
    print("\n".join("".join(str(x) for x in line) for line in octs))


total_flashes = 0
for step in range(100):
    flashed = set()
    for i in range(len(octs)):
        for j in range(len(octs[i])):
            octs[i][j] += 1
    flashable = {x for x in get_flashable()}
    while flashed != flashable:
        to_be_flashed = flashable.difference(flashed)
        for fi,fj in to_be_flashed:
            for ni,nj in neighbours(fi, fj):
                octs[ni][nj] += 1
        flashed.update(flashable)
        flashable = {x for x in get_flashable()}
    total_flashes += len(flashed)
    for i, j in flashed:
        octs[i][j] = 0
print(total_flashes)

