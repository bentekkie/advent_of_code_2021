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

@dataclass(frozen=True)
class Path:
    path_tuple : tuple[Cave, ...]
    double_small : bool

    def of(self, cave : Cave):
        if cave.is_big or cave not in self.path_tuple:
            return Path((*self.path_tuple, cave), self.double_small)
        if not (cave == start or cave == end) and not self.double_small and not cave.is_big and cave in self.path_tuple:
            return Path((*self.path_tuple, cave), True)
        return None

def gen_new_paths(path : Path):
    for n in path.path_tuple[-1].neighbours:
        if (new_path := path.of(n)) is not None:
            yield new_path

complete_paths = set()

incompolete_paths = {Path((start,), False),}
while len(incompolete_paths) > 0:
    new_paths = {p for incomplete_path in incompolete_paths for p in gen_new_paths(incomplete_path)}
    incompolete_paths = set()
    for path in new_paths:
        if path.path_tuple[-1] == end:
            complete_paths.add(path)
        else:
            incompolete_paths.add(path)
print(len(complete_paths))
        
