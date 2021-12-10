
matching = {
    "{":"}",
    "(":")",
    "[":"]",
    "<":">"
}

points = {
    ")":3,
    "]":57,
    "}":1197,
    ">":25137
}

def find_corrupt(text):
    stack = []
    for c in text:
        if c in matching.keys():
            stack.append(c)
        elif c != matching[stack.pop()]:
            return points[c]
    return 0



with open("input.txt") as f:
    print(sum(find_corrupt(text.strip()) for text in f.readlines()))
