from dataclasses import dataclass
from collections import defaultdict
from typing import List, Set, Dict, FrozenSet

# 1 : 2
# 2 : 5
# 3 : 5
# 4 : 4
# 5 : 5
# 6 : 6
# 7 : 3
# 8 : 7
# 9 : 6
# 0 : 6

# 5 : 2,3,5
# 6 : 6,9,0

@dataclass
class Entry:
    inputs : List[FrozenSet[str]]
    outputs : List[FrozenSet[str]]

    def of(line : str):
        input_str, output_str = line.strip().split(" | ")
        return Entry([frozenset(s) for s in input_str.split(" ")], [frozenset(s) for s in output_str.split(" ")])

def calculate(entry : Entry):
    mapping = {}
    lengths : Dict[int,List[Set[str]]] = defaultdict(list)
    for i in entry.inputs:
        lengths[len(i)].append(i)
    mapping[1] = lengths[2][0]
    mapping[7] = lengths[3][0]
    mapping[4] = lengths[4][0]
    mapping[8] = lengths[7][0]

    for k in lengths[5]:
        if len(k.intersection(mapping[1])) == 2:
            mapping[3] = k
        elif len(k.intersection(mapping[4])) == 3:
            mapping[5] = k
        else:
            mapping[2] = k

    for k in lengths[6]:
        if len(k.intersection(mapping[3])) == 5:
            mapping[9] = k
        elif len(k.intersection(mapping[5])) == 5:
            mapping[6] = k
        else:
            mapping[0] = k
    mapping = {v:k for k,v in mapping.items()}

    return int("".join(str(mapping[o]) for o in entry.outputs))
        

with open("input.txt") as f:
    entries = [Entry.of(line) for line in f.readlines()]


print(sum(calculate(e) for e in entries))