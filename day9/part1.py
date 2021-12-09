with open("input.txt") as f:
    nums = [[int(x) for x in line.strip()] for line in f.readlines()]

def neighbours(i,j):
    if i > 0:
        yield nums[i - 1][j]
    if j > 0:
        yield nums[i][j - 1]
    if i + 1 < len(nums):
        yield nums[i + 1][j]
    if j + 1 < len(nums[i]):
        yield nums[i][j + 1]

low_points = []
for i in range(len(nums)):
    for j in range(len(nums[i])):
        if all(nums[i][j] < n for n in neighbours(i, j)):
            low_points.append(nums[i][j] + 1)

print(sum(low_points))