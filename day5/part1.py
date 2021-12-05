from dataclasses import dataclass
from typing import Counter

@dataclass
class Line:
    x1: int
    x2: int
    y1: int
    y2: int

    def of(str_line : str):
        xs,ys = str_line.split("->")
        x1,y1 = xs.split(",")
        x2,y2 = ys.split(",")
        return Line(int(x1), int(x2), int(y1), int(y2))

    def horizontal(self):
        return self.x1 == self.x2
    def vertical(self):
        return self.y1 == self.y2

    def points(self):
        if self.horizontal():
            min_y = min(self.y1,self.y2)
            max_y = max(self.y1,self.y2) + 1
            for y in range(min_y, max_y):
                yield self.x1, y
        elif self.vertical():
            min_x = min(self.x1,self.x2)
            max_x = max(self.x1,self.x2) + 1
            for x in range(min_x, max_x):
                yield x, self.y1


with open("input.txt") as f:
    lines = [Line.of(s) for s in f.readlines()]

lines = [l for l in lines if l.horizontal() or l.vertical()]


points = Counter(p for l in lines for p in l.points())

more_than_two = sum(1 for _,c in points.items() if c > 1)

print(more_than_two)
