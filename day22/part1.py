def contains(cube: tuple[int,int,int], range_tuple : tuple[tuple[int,int],tuple[int,int],tuple[int,int]]):
    return range_tuple[0][0] <= cube[0] <= range_tuple[0][1] and range_tuple[1][0] <= cube[1] <= range_tuple[1][1] and range_tuple[2][0] <= cube[2] <= range_tuple[2][1]

def is_outside(step : tuple[int,tuple[tuple[int,int],tuple[int,int],tuple[int,int]]]):
    return any(l > 50 or h < -50 for l,h in step[1])

def parse_range(range_str : str):
    low,high = range_str[2:].split("..")
    return int(low),int(high)

def parse_line(line :str):
    return ("on" in line, tuple(parse_range(r) for r in line.strip().split(" ")[1].split(",")))

with open("input.txt") as f:
    steps = [s for line in f.readlines() if not is_outside(s:=parse_line(line))]




on_cubes = set()

for x in range(-50,51):
    for y in range(-50,51):
        for z in range(-50,51):
            cube = (x,y,z)
            status = False
            for on,range_tuple in steps:
                if on != status and contains(cube, range_tuple):
                    status = on
            if status:
                on_cubes.add(cube)

print(len(on_cubes))