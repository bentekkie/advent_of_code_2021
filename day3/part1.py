with open("input.txt") as f:
    bin_strings = f.readlines()
gamma = ''.join(str(int(s.count('1') > s.count('0'))) for s in zip(*bin_strings))
epsilon = ''.join(str(int(s.count('0') > s.count('1'))) for s in zip(*bin_strings))
print(int(gamma, base=2))
print(int(epsilon, base=2))
print(int(gamma, base=2)*int(epsilon, base=2))