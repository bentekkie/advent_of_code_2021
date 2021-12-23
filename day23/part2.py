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
    for i in range(4):
        if i < 3:
            neighbours[f"{letter}{i}"].add(f"{letter}{i+1}")
        if i > 0:
            neighbours[f"{letter}{i}"].add(f"{letter}{i-1}")
        else:
            neighbours[f"h{hallway_num}"].add(f"{letter}0")
            neighbours[f"{letter}0"].add(f"h{hallway_num}")


hallway("a","2")
hallway("b","4")
hallway("c","6")
hallway("d","8")

def paths(letter: str, starting: str):
    all_paths = [(starting,)] + [(f"h{i}",) for i in (0,1,3,5,7,9,10)]
    hallway_ends =  {f"h{i}" for i in (0,1,3,5,7,9,10)}
    room_ends = {f"{letter.lower()}0",f"{letter.lower()}1",f"{letter.lower()}2",f"{letter.lower()}3"}
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
                    if path[0] == starting and neighbour in hallway_ends:
                        yield new_path
        all_paths = new_paths

cost_per_move = {
    "A":1,
    "B":10,
    "C":100,
    "D":1000
}
def path_costs(letter: str, starting: str):
    costed_paths = defaultdict(list)
    for path in paths(letter,starting):
        cost = (len(path) - 1) * cost_per_move[letter]
        costed_paths[path[0]].append((cost,path[1:],path[-1]))
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
starting[second[3]].append("a3")
starting[second[5]].append("b3")
starting[second[7]].append("c3")
starting[second[9]].append("d3")
starting["A"].extend(["d1","c2"])
starting["B"].extend(["c1","b2"])
starting["C"].extend(["b1","d2"])
starting["D"].extend(["a1","a2"])

id = ["i","j","k","l"]

current_pos : dict[str,str] = {f"{l},{id[i]}":val for l in starting for i,val in enumerate(starting[l])}


lower = {
    "A":"a","B":"b","C":"c","D":"d"
}

states = [current_pos]

all_costed_paths = {k:path_costs(k[0],v) for k,v in current_pos.items()}
start = tuple(sorted((current_pos.items())))
g = Graph()
visited = set()
complete = set()
to_visit = {start,}
indexes = {k:i for i,(k,_) in enumerate(start)}


def is_valid(path, occupied, room_invalid_occupied_dict):
    if path[-1][0] != "h" and path[-1][0] in room_invalid_occupied_dict:
        return False
    i = 0
    l = len(path)
    while i < l:
        if path[i] in occupied:
            return False
        i+= 1
    return True

def room_invalid_occupied(state):
    return {pos[0] for token,pos in state if pos[0] != "h" and lower[token[0]] != pos[0]}

def process_token(state, state_list, occupied, token, loc):
    room_invalid_occupied_dict = {pos[0] for token,pos in state if pos[0] != "h" and lower[token[0]] != pos[0]}
    not_invalid = not room_invalid_occupied_dict
    for new_cost, path,last in all_costed_paths[token][loc]:
        if is_valid(path, occupied, room_invalid_occupied_dict):
            state_list[indexes[token]] = (token,last)
            new_pos = tuple(state_list)
            g.add_edge(state,new_pos,new_cost)
            if new_pos not in visited:
                if new_pos not in complete:
                    if last[0] == lower[token[0]] and not_invalid and is_complete(new_pos):
                        complete.add(new_pos)
                    else:
                        yield new_pos

def process_state(state : tuple[tuple[str,str],...]):
    occupied = {x for _,x in state}
    yield from (t for token,loc in state for t in process_token(state, list(state), occupied, token, loc))


while len(to_visit) > 0:
    new_to_visit = set()
    visited.update(to_visit)
    to_visit = {x for state in to_visit for x in process_state(state)}
    print(len(to_visit),len(complete))

pred = single_source_shortest_paths(g,start)

print(min(extract_shortest_path_from_predecessor_list(pred,d).total_cost for d in complete))