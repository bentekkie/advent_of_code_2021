
matching = {
    "{":"}",
    "(":")",
    "[":"]",
    "<":">"
}

points = {
    ")":1,
    "]":2,
    "}":3,
    ">":4
}

def incomplete_points(text):
    stack = []
    for c in text:
        if c in matching.keys():
            stack.append(c)
        elif c != matching[stack.pop()]:
            return 0
    return completion_string_points(completion_string(stack))


def completion_string(stack : list[str]):
    return [matching[c] for c in stack[::-1]]

def completion_string_points(comp : str):
    total_points = 0
    for c in comp:
        total_points *= 5
        total_points += points[c]
    return total_points



with open("input.txt") as f:
    all_points = sorted(p for text in f.readlines() if (p := incomplete_points(text.strip())) > 0)
    print(all_points[len(all_points) // 2])
