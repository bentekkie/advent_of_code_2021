from collections import defaultdict
from typing import FrozenSet
from dijkstar import Graph, find_path
from dijkstar.algorithm import single_source_shortest_paths, extract_shortest_path_from_predecessor_list


neighbours = defaultdict(set)
for i in range(11):
    if i < 10:
        neighbours[f"h{i}"].add(f"h{i+1}")
    if i > 0:
        neighbours[f"h{i}"].add(f"h{i-1}")

def hallway(letter, hallway_num : int):
    neighbours[f"h{hallway_num}"].add(f"{letter}0")
    neighbours[f"{letter}0"] = {f"h{hallway_num}",f"{letter}1"}
    neighbours[f"{letter}1"] = {f"{letter}0",}
hallway("a","2")
hallway("b","4")
hallway("c","6")
hallway("d","8")

def paths(letter: str, starting: str):
    all_paths = [(starting,)] + [(f"h{i}",) for i in (0,1,3,5,7,9,10)]
    hallway_ends =  {f"h{i}" for i in (0,1,3,5,7,9,10)}
    room_ends = {f"{letter.lower()}0",f"{letter.lower()}1"}
    all_ends = hallway_ends | room_ends
    while len(all_paths) > 0:
        new_paths = []
        for path in all_paths:
            for neighbour in neighbours[path[-1]]:
                if neighbour not in path:
                    new_path = (*path,neighbour)
                    new_paths.append(new_path)
                    if path[0][0] == "h" and neighbour in room_ends:
                        yield new_path
                    if path[0] == starting and neighbour in all_ends:
                        yield new_path
        all_paths = new_paths

cost_per_move = {
    "A":1,
    "B":10,
    "C":100,
    "D":1000
}
def path_costs(letter: str, starting: str):
    costed_paths = defaultdict(set)
    for path in paths(letter,starting):
        cost = (len(path) - 1) * cost_per_move[letter]
        costed_paths[path[0]].add((cost,path))
    return costed_paths

with open("input.txt") as f:
    f.readline()
    f.readline()
    first = f.readline()
    second = f.readline()

def is_complete(positions: FrozenSet[tuple[str,str]]):
    return all(k[0].lower() == v[0] for k,v in positions)
    
starting = defaultdict(list)
starting[first[3]].append("a0")
starting[first[5]].append("b0")
starting[first[7]].append("c0")
starting[first[9]].append("d0")
starting[second[3]].append("a1")
starting[second[5]].append("b1")
starting[second[7]].append("c1")
starting[second[9]].append("d1")
current_pos : dict[str,str] = {
    "Ai":starting["A"][0],
    "Aj":starting["A"][1],
    "Bi":starting["B"][0],
    "Bj":starting["B"][1],
    "Ci":starting["C"][0],
    "Cj":starting["C"][1],
    "Di":starting["D"][0],
    "Dj":starting["D"][1],
}

states = [current_pos]

all_costed_paths = {k:path_costs(k[0],v) for k,v in current_pos.items()}

g = Graph()
visited = set()
complete = set()
to_visit = {frozenset(current_pos.items()),}
while len(to_visit) > 0:
    new_to_visit = set()
    visited.update(to_visit)
    for state in to_visit:
        occupied = {x for _,x in state}
        for token,loc in state:
            for new_cost, path in all_costed_paths[token][loc]:
                if all(l not in occupied for l in path[1:]):
                    new_pos = frozenset((k,v) if k !=token else (k,path[-1]) for k,v in state)
                    g.add_edge(state,new_pos,new_cost)
                    if new_pos not in visited:
                        if new_pos not in complete:
                            if path[-1][0] == token[0].lower() and is_complete(new_pos):
                                complete.add(new_pos)
                            else:
                                new_to_visit.add(new_pos)
    to_visit = new_to_visit
    print(len(to_visit),len(complete))

pred = single_source_shortest_paths(g,frozenset(current_pos.items()))

print(min(extract_shortest_path_from_predecessor_list(pred,d).total_cost for d in complete))


