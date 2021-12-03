from dataclasses import dataclass

@dataclass
class Position:
    horizontal_pos : int
    depth : int

    def apply(self, command, amt):
        if command == "down":
            return self.down(amt)
        if command == "up":
            return self.up(amt)
        if command == "forward":
            return self.forward(amt)

    def down(self, amt):
        return Position(self.horizontal_pos, self.depth + amt)
    
    def up(self, amt):
        return Position(self.horizontal_pos, self.depth - amt)

    def forward(self, amt):
        return Position(self.horizontal_pos + amt, self.depth)


with open("input.txt") as f:
    lines = f.readlines()
p = Position(0,0)
for line in lines:
    command, amt = line.split(" ")
    p = p.apply(command, int(amt))

print(p.horizontal_pos*p.depth)