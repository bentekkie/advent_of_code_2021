from dataclasses import dataclass
from collections import defaultdict
from typing import List, Set, Dict

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
    number : int

    def of(line : str):
        input_str, output_str = line.strip().split(" | ")
        mapping = Entry.build_mapping([set(s) for s in input_str.split(" ")])

        output_digits = [tuple(sorted(o)) for o in output_str.split(" ")]


        return Entry(int("".join(str(mapping[o]) for o in output_digits)))

    def build_mapping(inputs : List[Set[str]]):
        mapping = {}
        lengths : Dict[int,List[Set[str]]] = defaultdict(list)
        for i in inputs:
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
        return {tuple(sorted(v)):k for k,v in mapping.items()}

        
        

with open("input.txt") as f:
    entries = [Entry.of(line) for line in f.readlines()]

def is_valid(output):
    return len(output) == 2 or len(output) == 4 or len(output) == 3 or len(output) == 7

print(sum(e.number for e in entries))