from collections import defaultdict

with open("input.txt") as f:
    enhancement = [c for c in f.readline().strip()]
    f.readline()
    image = defaultdict(lambda: '.')
    raw_image = [[c for c in line.strip()] for line in f.readlines()]
    for i,line in enumerate(raw_image):
        for j,c in enumerate(line):
            image[(i,j)] = c

center = (len(raw_image)//2, len(raw_image[0])//2)
#center = (0,0)
images = [image,dict(),dict()]

def ring(dist: int):
    yield from ((center[0]+dist,j) for j in range(center[1]-dist,center[1]+dist))
    yield from ((center[0]-dist,j) for j in range(center[1]-dist,center[1]+dist))
    yield from ((i,center[1]+dist) for i in range(center[0]-dist,center[0]+dist+1))
    yield from ((i,center[1]-dist) for i in range(center[0]-dist+1,center[0]+dist))

def enhance(n: int, pixel : tuple[int,int]):
    if pixel in images[n]:
        return images[n][pixel]
    elif n == 0:
        return '.'
    else:
        i,j = pixel
        raw_bitstring = [
            enhance(n-1, (i-1,j-1)),
            enhance(n-1, (i-1,j)),
            enhance(n-1, (i-1,j+1)),
            enhance(n-1, (i,j-1)),
            enhance(n-1, (i,j)),
            enhance(n-1, (i,j+1)),
            enhance(n-1, (i+1,j-1)),
            enhance(n-1, (i+1,j)),
            enhance(n-1, (i+1,j+1))
            ]
        images[n][pixel]=enhancement[int("".join("1" if c == "#" else "0" for c in raw_bitstring), base=2)]
        return images[n][pixel]

def enhance_3_ring(n: int, ring_n: int):
    for pixel in ring(ring_n):
        yield enhance(n,pixel)
    for pixel in ring(ring_n+1):
        yield enhance(n,pixel)
    for pixel in ring(ring_n+2):
        yield enhance(n,pixel)

dist = 0
changed = True
while changed:
    changed = False
    for c in enhance_3_ring(2,dist):
        if c =="#":
            changed = True
    dist += 3


print("\n".join("".join(
    images[2][(i,j)] if (i,j) in images[2] else "." for j in range(min(j for _,j in images[2].keys()),max(j for _,j in images[2].keys())+1)
) for i in range(min(i for i,_ in images[2].keys()), max(i for i,_ in images[2].keys())+1)))

print(sum(1 for c in images[2].values() if c == "#"))