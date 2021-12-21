from dataclasses import dataclass


@dataclass
class Dice:
    last: int = 0
    rolls: int = 0

    def roll(self):
        self.last += 1
        self.rolls += 1
        if self.last == 101:
            self.last = 1
        return self.last

@dataclass
class Player:
    location: int
    score: int = 0

    def parse(line: str):
        return Player(int(line[-1]))

    def move(self, dice : Dice):
        distance = dice.roll() + dice.roll() + dice.roll()
        self.location += distance
        while self.location > 10:
            self.location -= 10
        self.score += self.location

with open("input.txt") as f:
    p1 = Player.parse(f.readline().strip())
    p2 = Player.parse(f.readline().strip())


def play(p1 : Player,p2 : Player):
    dice = Dice()
    while True:
        p1.move(dice)
        if p1.score >= 1000:
            return p2.score * dice.rolls
        p2.move(dice)
        if p2.score >= 1000:
            return p1.score * dice.rolls

print(play(p1,p2))