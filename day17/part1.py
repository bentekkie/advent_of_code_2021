with open("input.txt") as f:
    line = f.readline().strip().removeprefix("target area: ")
    _,ypart = line.split(", ")
    y2,_ = ypart[2:].split("..")
    y2 = int(y2)

vy = -y2-1
print((vy*(vy+1))//2)