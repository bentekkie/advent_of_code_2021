from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Cave:
    name: str
    is_big: bool
    neighbours: set["Cave"] = field(default_factory=set, hash=False)

    def __repr__(self) -> str:
        return self.name



with open("input.txt") as f:
    caves_raw = [line.strip().split("-") for line in f.readlines()]
cave_names = {name for edge in caves_raw for name in edge}
all_caves = {name:Cave(name, name.isupper()) for name in cave_names}
for a,b in caves_raw:
    all_caves[a].neighbours.add(all_caves[b])
    all_caves[b].neighbours.add(all_caves[a])


start = all_caves["start"]
end = all_caves["end"]


def gen_new_paths(path : tuple[Cave, ...]):
    for n in path[-1].neighbours:
        if n.is_big or n not in path:
            yield (*path, n)

complete_paths = set()

incompolete_paths = {(start,),}
while len(incompolete_paths) > 0:
    new_paths = {p for incomplete_path in incompolete_paths for p in gen_new_paths(incomplete_path)}
    incompolete_paths = set()
    for path in new_paths:
        if path[-1] == end:
            complete_paths.add(path)
        else:
            incompolete_paths.add(path)

print(len(complete_paths))
        
