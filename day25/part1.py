with open("input.txt") as f:
    raw_map = [line.strip() for line in f.readlines()]
max_i = len(raw_map)
max_j = len(raw_map[0])
east_cucumbers = []
south_cucumbers = []

def reset_filled():
    new_filled = set()
    new_filled.update(east_cucumbers)
    new_filled.update(south_cucumbers)
    return new_filled
    
for i,line in enumerate(raw_map):
    for j,c in enumerate(line): 
        if c == ">":
            east_cucumbers.append((i,j))
        if c == "v":
            south_cucumbers.append((i,j))



filled_locs = reset_filled()
moved = True
steps = 0
while moved:
    moved = False
    new_cucumbers = []
    for i,j in east_cucumbers:
        ni,nj = i,(j+1) % max_j
        if (ni,nj) in filled_locs:
            new_cucumbers.append((i,j))
        else:
            new_cucumbers.append((ni,nj))
            moved = True
    east_cucumbers = new_cucumbers
    filled_locs = reset_filled()
    new_cucumbers = []
    for i,j in south_cucumbers:
        ni,nj = (i+1) % max_i,j
        if (ni,nj) in filled_locs:
            new_cucumbers.append((i,j))
        else:
            new_cucumbers.append((ni,nj))
            moved = True
    south_cucumbers = new_cucumbers
    filled_locs = reset_filled()
    steps += 1

print(steps)

