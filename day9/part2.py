with open("input.txt") as f:
    nums = [[int(x) for x in line.strip()] for line in f.readlines()]

def neighbours(i,j):
    if i > 0:
        yield (i - 1,j)
    if j > 0:
        yield (i,j - 1)
    if i + 1 < len(nums):
        yield (i + 1,j)
    if j + 1 < len(nums[i]):
        yield (i,j + 1)

def explore_basin(visited : set[tuple[int,int]]):
    new_neighbours = {
        n for p in visited for n in neighbours(p[0],p[1]) 
        if n not in visited and nums[n[0]][n[1]] != 9}
    if len(new_neighbours) == 0:
        return visited
    return explore_basin(visited.union(new_neighbours))

low_points = [
    (i,j) for i in range(len(nums)) for j in range(len(nums[i]))
    if all(nums[i][j] < nums[n[0]][n[1]] for n in neighbours(i, j))]




basins = sorted([explore_basin({low_point,}) for low_point in low_points], key=len, reverse=True)

print(len(basins[0])*len(basins[1])*len(basins[2]))