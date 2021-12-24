from alu import program

digits = {(0,0,0):""}
for d in range(14):
    new_digits = {}
    for (x,y,z),prev in digits.items():
        for w in range(1,10):
            out = program[d](w,x,y,z)
            new = prev + str(w)
            if out not in new_digits or new > new_digits[out]:
                new_digits[out] = new
    digits = new_digits


for (x,y,z),prev in digits.items():
    if z == 0:
        print(prev)