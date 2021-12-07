


from collections import Counter, deque


with open("input.txt") as f:
    counter = Counter(int(x) for x in f.readline().split(','))
    fish = deque(counter[x] for x in range(9))

for day in range(256):
    fish.rotate(-1)
    fish[6] += fish[8]

print(sum(fish))
