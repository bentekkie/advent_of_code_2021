from typing import NamedTuple
from dataclasses import dataclass, field
from itertools import combinations

class Coord(NamedTuple):
    x: int
    y: int
    z: int

def rotate_around(x,y,z):
    yield (x,y,z)
    yield (x,z,-y)
    yield (x,-z,y)
    yield (x,-y,-z)

def rotate(x,y,z):
    yield from rotate_around(x,y,z)
    yield from rotate_around(-y,x,z)
    yield from rotate_around(y,-x,z)
    yield from rotate_around(-z,y,x)
    yield from rotate_around(z,y,-x)
    yield from rotate_around(-x,y,-z)



@dataclass
class Scanner:
    id:int
    coords: set[tuple[int,int,int]]
    rotations : list[tuple[set[tuple[int,int,int]],list[tuple[int,int,int]]]] = field(init=False)

    def __post_init__(self):
        self.rotations = [(frozenset(k),list(k)) for k in zip(*(rotate(x,y,z) for x,y,z in self.coords))]


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    scanners : dict[int,Scanner] = {}
    id = None
    coords : set[tuple[int,int,int]] = set()
    for line in lines:
        if line.startswith("--- scanner "):
            if id is not None:
                scanners[id] = Scanner(id,coords)
            id = int(line.removeprefix("--- scanner ").removesuffix(" ---"))
            coords = set()
        elif "," in line:
            x,y,z= line.split(",")
            coords.add((int(x),int(y),int(z)))
    if id is not None:
        scanners[id] = Scanner(id,coords)

scanner_positions = {0:((0,0,0),0)}
doesnt_overlap = set()

def tupsub(ax,ay,az,bx,by,bz):
    return (ax - bx, ay - by, az - bz)

def check(scanner : Scanner, id : int):
    for ksid,((kx,ky,kz),known_scanner_locs) in scanner_positions.items():
        krot,krotlist = scanners[ksid].rotations[known_scanner_locs]
        if (ksid,id) not in doesnt_overlap:
            for roti,(_,rotlist) in enumerate(scanner.rotations):
                for p in rotlist:
                    for q in krotlist:
                        dx,dy,dz = tupsub(*q,*p)
                        count = 0
                        for rx,ry,rz in rotlist:
                            if (rx + dx, ry + dy, rz + dz) in krot:
                                count += 1
                                if count >= 12:
                                    scanner_positions[id] = ((kx + dx, ky + dy, kz + dz), roti)
                                    return
            doesnt_overlap.add((ksid,id))

def heuristic(id):
    return sum(1 for _,id1 in doesnt_overlap if id1 == id)

def match_scanner():
    for id in sorted((t for t in scanners.keys() if t not in scanner_positions.keys()),key=heuristic):
        check(scanners[id], id)
i = 0
while len(scanner_positions) < len(scanners):
    print(i,len(scanner_positions) )
    match_scanner()
    i += 1


def manhattan(x1,y1,z1,x2,y2,z2):
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)

print(max(manhattan(*a,*b) for a,b in combinations((p for _,(p,_) in scanner_positions.items()), 2)))