from statistics import median

with open("input.txt") as f:
    pos_list = [int(x) for x in f.readline().split(",")]


def fuel(h_pos):
    return sum(abs(h_pos - x) for x in pos_list)


print(fuel(median(pos_list)))
