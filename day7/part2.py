from statistics import median
from functools import cache

with open("input.txt") as f:
    pos_list = [int(x) for x in f.readline().split(",")]

@cache
def sumn(n):
    return (n*(n+1))/2

@cache
def fuel(h_pos):
    return sum(sumn(abs(h_pos - x)) for x in pos_list)

print(min(fuel(x) for x in range(min(pos_list), max(pos_list) + 1)))
