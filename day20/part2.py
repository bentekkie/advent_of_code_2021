from functools import lru_cache
from typing import Literal
from itertools import chain

with open("inputex.txt") as f:
    enhancement = [c for c in f.readline().strip()]
    f.readline()
    raw_image = [[c for c in line.strip()] for line in f.readlines()]
    image = {(i,j):c for i,line in enumerate(raw_image) for j,c in enumerate(line)}

center = (len(raw_image)//2, len(raw_image[0])//2)
images = [image] + [dict() for _ in range(50)]

def ring(dist: int):
    yield from ((center[0]+dist,j) for j in range(center[1]-dist,center[1]+dist))
    yield from ((center[0]-dist,j) for j in range(center[1]-dist,center[1]+dist))
    yield from ((i,center[1]+dist) for i in range(center[0]-dist,center[0]+dist+1))
    yield from ((i,center[1]-dist) for i in range(center[0]-dist+1,center[0]+dist))

@lru_cache()
def enhance(n: int, pixel : tuple[int,int]) -> Literal[1,0]:
    if pixel in images[n]:
        return images[n][pixel] == "#"
    elif n == 0:
        return False
    else:
        i,j = pixel
        index = 0
        if enhance(n-1, (i-1,j-1)):
            index |= 256
        if enhance(n-1, (i-1,j)):
            index |= 128
        if enhance(n-1, (i-1,j+1)):
            index |= 64
        if enhance(n-1, (i,j-1)):
            index |= 32
        if enhance(n-1, (i,j)):
            index |= 16
        if  enhance(n-1, (i,j+1)):
            index |= 8
        if enhance(n-1, (i+1,j-1)):
            index |= 4
        if enhance(n-1, (i+1,j)):
            index |= 2
        if enhance(n-1, (i+1,j+1)):
            index |= 1
        images[n][pixel]=enhancement[index]
        return images[n][pixel] == "#"

count = 0
dist = 0
changed = True
while changed:
    changed = False
    for pixel in ring(dist):
        if enhance(50,pixel):
            count += 1
            changed = True
    dist += 1

print(count)