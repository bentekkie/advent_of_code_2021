from collections import defaultdict


with open("input.txt") as f:
    caves_raw = [line.strip().split("-") for line in f.readlines()]

neighbours = defaultdict(set)
big = dict()
for a, b in caves_raw:
    neighbours[a].add(b)
    neighbours[b].add(a)
    big[a] = a.isupper()
    big[b] = b.isupper()

def path_of(path: tuple[tuple, bool], cave: str):
    if big[cave]:
        return ((cave, *path[0]), path[1])
    elif cave in path[0]:
        if cave != "start" and cave != "end" and not path[1]:
            return ((cave, *path[0]), True)
    else:
        return ((cave, *path[0]), path[1])


total = 0

incompolete_paths = {(("start",), False), }
while incompolete_paths:
    old_incomplete_paths, incompolete_paths= incompolete_paths, set()
    for path in {new_path for incomplete_path in old_incomplete_paths for n in neighbours[
            incomplete_path[0][0]] if (new_path := path_of(incomplete_path, n))}:
        if path[0][0] == "end":
            total += 1
        else:
            incompolete_paths.add(path)
print(total)
