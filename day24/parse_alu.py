
from dataclasses import dataclass

# Run python3 parse_alu.py > alu.py to generate alu code



@dataclass
class ALU:
    order: list[str]
    variables : dict[str, list[str]]

    def get_var(self, a : str):
        if a.isdigit() or (a[0] == "-" and a[1:].isdigit()):
            return a
        else:
            return f"{a}{len(self.variables[a])-1}"

    def add(self, a : str, b : str):
        left = self.get_var(a)
        right = self.get_var(b)
        self.variables[a].append(f"({left} + {right})")
        self.order.append(f"{a}{len(self.variables[a])-1}=({left} + {right})")
        return True

    def mul(self, a : str, b : str):
        left = self.get_var(a)
        right = self.get_var(b)
        self.variables[a].append(f"({left} * {right})")
        self.order.append(f"{a}{len(self.variables[a])-1}=({left} * {right})")
        return True

    def div(self, a : str, b : str):
        left = self.get_var(a)
        right = self.get_var(b)
        self.variables[a].append(f"(trunc({left} / {right}))")
        self.order.append(f"if {right} == 0:return None")
        self.order.append(f"{a}{len(self.variables[a])-1}=(trunc({left} / {right}))")
        return True

    def mod(self, a : str, b : str):
        left = self.get_var(a)
        right = self.get_var(b)
        self.variables[a].append(f"({left} % {right})")
        self.order.append(f"if {right} <= 0 or {left} < 0:return None")
        self.order.append(f"{a}{len(self.variables[a])-1}=({left} % {right})")
        return True

    def eql(self, a : str, b : str):
        left = self.get_var(a)
        right = self.get_var(b)
        self.variables[a].append(f"(1 if {left} == {right} else 0)")
        self.order.append(f"{a}{len(self.variables[a])-1}=(1 if {left} == {right} else 0)")
        return True


    def run(self,  instructions : list[str], inp : str):
        self.variables["w"].append(inp)
        for instruction in instructions:
            #print(instruction)
            #print(self.variables)
            inst, a, b = instruction.split(" ")
            if inst == "add":
                self.add(a,b)
            elif inst == "mul":
                self.mul(a,b)
            elif inst == "div":
                if not self.div(a,b):
                    return None
            elif inst == "mod":
                if not self.mod(a,b):
                    return None
            elif inst == "eql":
                self.eql(a,b)
        return self


def split_into_digits(all_inst : list[str]):
    curr = []
    for inst in all_inst:
        if inst == "inp w":
            yield curr
            curr = []
        else:
            curr.append(inst)
    yield curr


with open("input.txt") as f:
    all_instructions = list(split_into_digits(line.strip() for line in f.readlines()))[1:]



a = ALU([],{"w":[],"x":["0"],"y":["0"],"z":["0"]})

print("from math import trunc")

prevxyz = "x0,y0,z0"

for i in range(14):
    a.run(all_instructions[i],f"w{i}")
    print(f"def run_w{i}(w{i},{prevxyz}):")
    for v in a.order:
        print(f"\t{v}")
    prevxyz = f"x{len(a.variables['x'])-1},y{len(a.variables['y'])-1},z{len(a.variables['z'])-1}"
    print(f"\treturn {prevxyz}")
    a.order = []

print("program = [run_w0,run_w1,run_w2,run_w3,run_w4,run_w5,run_w6,run_w7,run_w8,run_w9,run_w10,run_w11,run_w12,run_w13]")
            



    