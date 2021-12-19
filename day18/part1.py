from dataclasses import dataclass, field
from typing import Generator, Optional
from modgrammar import Grammar, WORD, L, REF
from math import floor, ceil

@dataclass
class SnailFish:
    pass
@dataclass
class SnailFishPair(SnailFish):
    left : SnailFish
    right : SnailFish
    parent : "SnailFishPair" = field(init=False, default=None)

    def __post_init__(self):
        self.left.parent = self
        self.right.parent = self

    def replace(self, old_child : SnailFish ,new_child : SnailFish):
        new_child.parent = self
        if self.left is old_child:
            self.left = new_child
        else:
            self.right = new_child

    def magnitude(self):
        return self.left.magnitude()*3 + self.right.magnitude()*2

@dataclass
class SnailFishNumber(SnailFish):
    parent : "SnailFishPair" = field(init=False, default=None)
    val : int
    left_num : Optional["SnailFishNumber"] = None
    right_num : Optional["SnailFishNumber"] = None

    def magnitude(self):
        return self.val

class SnailFishPairGrammar(Grammar):
    grammar = (L('['),REF('SnailFishGrammar'),L(','),REF('SnailFishGrammar'),L(']'))

    def value(self):
        return SnailFishPair(self[1].value(), self[3].value())


class SnailFishNumberGrammar(Grammar):
    grammar = (WORD('0-9'),)

    def value(self):
        return SnailFishNumber(int(self.string))


class SnailFishGrammar(Grammar):
    grammar_collapse = True
    grammar = (SnailFishPairGrammar | SnailFishNumberGrammar)





def parse(line: str):
    g = SnailFishPairGrammar.parser()
    root = g.parse_string(line).value()
    order = list(in_order_nums(root))
    for i in range(len(order)):
        if i > 0:
            order[i].left_num = order[i-1]
        if i+1 < len(order):
            order[i].right_num = order[i+1]
    return root

def find_explode(num: SnailFish, depth : int = 0) -> Optional[SnailFishPair]:
    if isinstance(num, SnailFishPair):
        if depth == 4:
            return num
        else:
            if n := find_explode(num.left, depth + 1):
                return n
            return find_explode(num.right, depth + 1)
    return None

def in_order_nums(all : SnailFish):
    if isinstance(all, SnailFishNumber):
        yield all
    elif isinstance(all, SnailFishPair):
        yield from in_order_nums(all.left)
        yield from in_order_nums(all.right)

def find_split(num: SnailFish) -> Optional[SnailFishNumber]:
    if isinstance(num, SnailFishPair):
        if n := find_split(num.left):
            return n
        return find_split(num.right)
    else:
        if num.val >= 10:
            return num
    return None


def reduce(sum: SnailFishPair):
    changed = True
    while changed:
        changed = False
        if exp := find_explode(sum):
            changed = True
            new_explode = SnailFishNumber(0,exp.left.left_num, exp.right.right_num)
            if exp.left.left_num:
                exp.left.left_num.val += exp.left.val
                exp.left.left_num.right_num = new_explode
            if exp.right.right_num:
                exp.right.right_num.val += exp.right.val
                exp.right.right_num.left_num = new_explode
            exp.parent.replace(exp, new_explode)
        elif split := find_split(sum):
            changed = True
            left = SnailFishNumber(floor(split.val/2),left_num=split.left_num)
            right = SnailFishNumber(ceil(split.val/2),right_num=split.right_num)
            pair = SnailFishPair(left,right)
            left.right_num = right
            right.left_num = left
            if split.left_num:
                split.left_num.right_num = left
            if split.right_num:
                split.right_num.left_num = right
            split.parent.replace(split,pair)
    return sum

def add(left : SnailFish, right : SnailFish):
    sum = SnailFishPair(left,right)
    left_num = left
    while isinstance(left_num, SnailFishPair):
        left_num = left_num.right
    right_num = right
    while isinstance(right_num, SnailFishPair):
        right_num = right_num.left
    left_num.right_num = right_num
    right_num.left_num = left_num
    return reduce(sum)


with open("input.txt") as f:
    nums = [parse(line.strip()) for line in f.readlines()]

number = nums[0]
for n in nums[1:]:
    number = add(number,n)

print(number.magnitude())