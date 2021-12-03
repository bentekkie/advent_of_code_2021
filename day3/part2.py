with open("input.txt") as f:
    bin_strings = f.readlines()

nums = list(bin_strings)
bit = 0
while len(nums) > 1:
    s = [n[bit] for n in nums]
    if s.count('0') > s.count('1'):
        crit = '0'
    else:
        crit = '1'
    nums = [n for n in nums if n[bit] == crit]
    bit += 1
ox = int(nums[0], base=2)
print(f'oxygen = {ox}')
nums = list(bin_strings)
bit = 0
while len(nums) > 1:
    s = [n[bit] for n in nums]
    if s.count('0') <= s.count('1'):
        crit = '0'
    else:
        crit = '1'
    nums = [n for n in nums if n[bit] == crit]
    bit += 1
    print(len(nums))
co = int(nums[0], base=2)
print(f'co2 = {co}')
print(ox*co)