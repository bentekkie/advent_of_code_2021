


from collections import Counter, deque


with open("input.txt") as f:
    counter = Counter(int(x) for x in f.readline().split(','))
    fish = deque(counter[x] for x in range(9))

for day in range(256):
    old_0 = fish[0]
    fish.rotate(-1)
    fish[6] += old_0

print(sum(fish))
