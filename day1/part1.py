
inc = 0
with open("input.txt") as f:
    prev = None
    for line in f:
        if prev is not None and int(line) > prev:
            inc += 1
        prev = int(line)

print(inc)

