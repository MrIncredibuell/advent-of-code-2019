data = (193651, 649729)

def is_valid(n):
    s = str(n)
    has_double = False
    for ii, c in enumerate(s[1:]):
        ii = ii + 1
        if s[ii - 1] == c:
            has_double = True
        if int(c) < int(s[ii - 1]):
            return False
    return has_double

def has_exact_double(n):
    s = str(n)
    current_index = 0
    current_char = s[0]
    for ii, c in enumerate(s[1:]):
        ii += 1
        if c != current_char:
            if ii - current_index == 2:
                return True
            current_index = ii
            current_char = c
    return current_index == len(s) - 2

def part1(lower_bound, upper_bound):
    count = 0
    for n in range(lower_bound, upper_bound + 1):
        if is_valid(n):
            count += 1
    print(count)

def part2(lower_bound, upper_bound):
    valids = [n for n in range(lower_bound, upper_bound + 1) if is_valid(n)]
    valids = [n for n in valids if has_exact_double(n)]
    print(len(valids))

part1(*data)
part2(*data)

