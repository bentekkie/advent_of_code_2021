from dataclasses import dataclass
from typing import List

@dataclass
class Cell:
    n: int
    marked: bool = False

    def mark(self):
        self.marked = True

@dataclass
class Board:
    cells: List[List[Cell]]
    won: bool = False

    def has_won(self):
        if self.won:
            return True
        self.won = (any(all(c.marked for c in line) for line in self.cells) 
                or any(all(c.marked for c in line) for line in reversed(list(zip(*self.cells)))))
        return self.won

def search(boards : List[Board], nums : List[int]):
    for n in nums:
        for board in boards:
            if not board.won:
                changed = False
                for line in board.cells:
                    for cell in line:
                        if cell.n == n:
                            cell.mark()
                            changed = True
                if changed and board.has_won():
                    yield n, board

with open("input.txt") as f:
    nums = [int(n) for n in f.readline().split(",")]
    board_lines = f.readlines()
    boards = [Board([[Cell(int(n)) for n in line.split()] for line in board_lines[i+1:i+6]]) for i in range(0,len(board_lines), 6)]
       
last_n, winning_board = list(search(boards, nums))[-1]

print(last_n * sum(cell.n for line in winning_board.cells for cell in line if not cell.marked))