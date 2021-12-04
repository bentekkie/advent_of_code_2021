from dataclasses import dataclass
from typing import List

@dataclass
class Cell:
    n: int
    marked: bool = False

    def mark(self):
        self.marked = True

def has_won(board : List[List[Cell]]):
    return (any(all(c.marked for c in line) for line in board) 
            or any(all(c.marked for c in line) for line in reversed(list(zip(*board)))))

def search(boards, nums):
    for n in nums:
        for board in boards:
            changed = False
            for line in board:
                for cell in line:
                    if cell.n == n:
                        cell.mark()
                        changed = True
            if changed and has_won(board):
                return n, board
                
with open("input.txt") as f:
    nums = [int(n) for n in f.readline().split(",")]
    board_lines = f.readlines()
    boards = [[[Cell(int(n)) for n in line.split()] for line in board_lines[i+1:i+6]] for i in range(0,len(board_lines), 6)]
            
last_n, winning_board = search(boards, nums)

print(last_n * sum(cell.n for line in winning_board for cell in line if not cell.marked))