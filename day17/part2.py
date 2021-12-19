from dataclasses import dataclass
from enum import Enum

class direction(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4
    In = 5

@dataclass
class Probe:
    x: int
    y: int
    vx: int
    vy: int

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx = max(0,self.vx - 1)
        self.vy -= 1

@dataclass
class Area:
    x1: int
    x2: int
    y1: int
    y2: int

    def relative_pos(self, probe : Probe):
        if probe.x < self.x1:
            yield direction.Left
        if probe.x > self.x2:
            yield direction.Right
        if probe.y > self.y1:
            yield direction.Up
        if probe.y < self.y2:
            yield direction.Down
        if self.x1 <= probe.x <= self.x2 and self.y1 >= probe.y >= self.y2:
            yield direction.In


with open("input.txt") as f:
    line = f.readline().strip().removeprefix("target area: ")
    xpart,ypart = line.split(", ")
    x1,x2 = xpart[2:].split("..")
    y2,y1 = ypart[2:].split("..")
    target = Area(int(x1),int(x2),int(y1),int(y2))

def simulate(vx: int, vy: int):
    probe = Probe(0,0,vx,vy)
    while True:
        rel = set(target.relative_pos(probe))
        if direction.In in rel:
            return True
        if direction.Right in rel:
            return False
        if probe.vy < 1 and direction.Down in rel:
            return False
        probe.move()

lowest_vx = min(n for n in range(target.x1) if target.x1 <= (n*(n+1))/2 <= target.x2)

valid = 0
for vx in range(lowest_vx,target.x2+1):
    for vy in range(target.y2,-target.y2+1):
        if simulate(vx,vy):
            valid += 1

print(valid)