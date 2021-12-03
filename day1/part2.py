with open("input.txt") as f:
    nums = [int(x) for x in f]

ranges = [nums[i-2] + nums[i-1] + nums[i] for i in range(2,len(nums))]

inc = 0
prev = None
for r in ranges:
    if prev is not None and r> prev:
        inc += 1
    prev = r

print(inc)
