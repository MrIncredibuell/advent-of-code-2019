data = [int(row) for row in open("input1.txt").read().split("\n")]

def fuel(mass):
    return (mass // 3) - 2

def part1(data):
    return sum([fuel(m) for m in data])

def recursiveFuel(mass):
    fuelAmount = 0
    while mass >= 0:
        mass = fuel(mass)
        if mass > 0:
            fuelAmount += mass
    return fuelAmount

def part2(data):
    return sum([recursiveFuel(m) for m in data])

print(part1(data))
print(part2(data))