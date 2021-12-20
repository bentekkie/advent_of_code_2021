from typing import NamedTuple
from dataclasses import dataclass
from functools import cached_property

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


    @cached_property
    def rotations(self):
        return [frozenset(k) for k in zip(*(rotate(x,y,z) for x,y,z in self.coords))]

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

scanner_positions = {0:((0,0,0),scanners[0].rotations[0])}
doesnt_overlap = set()

def match_scanner():
    for id,scanner in scanners.items():
        if id not in scanner_positions:
            for ksid,((ksx,ksy,ksz),known_scanner_locs) in scanner_positions.items():
                if (ksid,id) not in doesnt_overlap:
                    for rot in scanner.rotations:
                        for px,py,pz in rot:
                            for qx,qy,qz in known_scanner_locs:
                                count = 0
                                for rotx,roty,rotz in rot:
                                    if (rotx + (qx-px),roty + (qy-py),rotz+ (qz-pz)) in known_scanner_locs:
                                        count += 1
                                    if count >= 12:
                                        scanner_positions[id] = ((ksx+ (qx-px),ksy+ (qy-py),ksz+ (qz-pz)), rot)
                                        return
                    doesnt_overlap.add((ksid,id))
for i in range(len(scanners)-1):
    print(i)
    match_scanner()


beacons = set()

for _,((ox,oy,oz),locs) in scanner_positions.items():
    for x,y,z in locs:
        beacons.add((x + ox,y + oy,z + oz))

print(len(beacons))