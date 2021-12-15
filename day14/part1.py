from collections import Counter

with open("input.txt") as f:
    template = f.readline().strip()
    f.readline()
    rules = dict()
    for line in f.readlines():
        pair, insert = line.strip().split(" -> ")
        rules[pair] = insert
    
for step in range(10):
    i = 0
    while i + 1 < len(template):
        if template[i:i+2] in rules:
            template = template[:i+1] + rules[template[i:i+2]] + template[i+1:]
            i += 1
        i += 1

counter = Counter(template)

print(max(counter.values()) - min(counter.values()))