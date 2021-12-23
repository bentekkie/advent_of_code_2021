
from shapely.geometry import box
from collections import defaultdict, Counter

def parse_range(range_str : str):
    low,high = range_str[2:].split("..")
    return int(low),int(high)

def parse_line(line :str):
    range_tuple = tuple(parse_range(r) for r in line.strip().split(" ")[1].split(","))
    (x1,x2),(y1,y2),z = range_tuple
    return ("on" in line, z, box(x1,y1,x2+1,y2+1))

with open("input.txt") as f:
    steps = [parse_line(line) for line in f.readlines()]


def final_area(boxes : tuple[int]):
    curr = None
    for i in boxes:
        if steps[i][0]:
            if curr is None:
                curr = steps[i][2]
            else:
                curr = curr.union(steps[i][2])
        else:
            if curr is not None:
                curr = curr.difference(steps[i][2])
    return curr.area if curr else 0

zaxis = defaultdict(list)
for id,(_,(z1,z2),_) in enumerate(steps):
    for k in range(z1,z2+1):
        zaxis[k].append(id)
print(sum(v*final_area(k) for k,v in Counter(tuple(s) for s in zaxis.values()).items()))
