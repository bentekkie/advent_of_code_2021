with open("input.txt") as f:
    fish = [int(x) for x in f.readline().split(',')]

for day in range(80):
    new_fish = fish.count(0)
    fish = [x-1 if x > 0 else 6 for x in fish] + [8] * new_fish

print(len(fish))