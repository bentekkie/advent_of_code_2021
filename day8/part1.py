from dataclasses import dataclass

@dataclass
class Entry:
    inputs : list[str]
    outputs : list[str]

    def of(line : str):
        input_str, output_str = line.strip().split(" | ")
        return Entry(input_str.split(" "), output_str.split(" "))

with open("input.txt") as f:
    entries = [Entry.of(line) for line in f.readlines()]

def is_valid(output):
    return len(output) == 2 or len(output) == 4 or len(output) == 3 or len(output) == 7

print(sum(sum(is_valid(output) for output in entry.outputs) for entry in entries))