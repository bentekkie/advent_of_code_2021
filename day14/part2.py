from collections import Counter, defaultdict


with open("input.txt") as f:
    template = f.readline().strip()
    f.readline()
    rules = dict()
    for line in f.readlines():
        pair, insert = line.strip().split(" -> ")
        rules[pair] = (pair[0] + insert, insert + pair[1])

pairs = Counter(template[i:i+2] for i in range(len(template)-1))

for step in range(40):
    new_pairs = defaultdict(int, pairs)
    for rule, (left,right) in rules.items():
        new_pairs[rule] -= pairs[rule]
        new_pairs[left] += pairs[rule]
        new_pairs[right] += pairs[rule]
    pairs = new_pairs

counts = defaultdict(int, {template[0]:.5,template[-1]:.5})
for (left,right), val in pairs.items():
    counts[left] += val/2
    counts[right] += val/2

print(max(counts.values()) - min(counts.values()))