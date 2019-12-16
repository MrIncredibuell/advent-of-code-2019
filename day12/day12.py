from itertools import combinations

data = [
    [-4, -9, -3],
    [-13, -11, 0],
    [-17, -7, 15],
    [-16, 4, 2],
]

# data = [
#     [-1, 0, 2],
#     [2, -10, -7],
#     [4, -8, 8],
#     [3, 5, -1],
# ]

def time_step(positions, velocities):
    new_positions = [p[:] for p in positions]
    new_velocities = [v[:] for v in velocities]
    for (ii, jj) in combinations(range(len(positions)), 2):
        a, b = positions[ii], positions[jj]
        # print(ii, jj, a,b)
        for axis in range(3):
            if a[axis] > b[axis]:
                new_velocities[ii][axis] -= 1
                new_velocities[jj][axis] += 1
            elif a[axis] < b[axis]:
                new_velocities[ii][axis] += 1
                new_velocities[jj][axis] -= 1
    for ii in range(len(positions)):
        for jj in range(3):
            new_positions[ii][jj] += new_velocities[ii][jj]
    return new_positions, new_velocities

def total_energy(positions, velocities):
    total = 0
    for ii, ps in enumerate(positions):
        potential = sum([abs(x) for x in ps])
        kintetic = sum([abs(x) for x in velocities[ii]])
        total += (potential * kintetic)
    return total

def part1(data):
    positions = data
    velocities = [[0, 0, 0]] * len(data)
    for step in range(1000):
        positions, velocities = time_step(positions, velocities)
    print(total_energy(positions, velocities))


def simulate_axis(positions, velocities):
    new_positions = [p for p in positions]
    new_velocities = [v for v in velocities]
    for (ii, jj) in combinations(range(len(positions)), 2):
        a, b = positions[ii], positions[jj]

        if a > b:
            new_velocities[ii] -= 1
            new_velocities[jj] += 1
        elif a < b:
            new_velocities[ii] += 1
            new_velocities[jj] -= 1
    for ii in range(len(positions)):
        new_positions[ii] += new_velocities[ii]
    return new_positions, new_velocities

def find_period(positions, velocities):
    seen = {}
    count = 0
    while str(positions) + str(velocities) not in seen:
        seen[str(positions) + str(velocities)] = count
        positions, velocities = simulate_axis(positions, velocities)
        count += 1
    return count

# BORROWED FROM STACK OVERFLOW
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcm2(a, b, c):
    return lcm(a, lcm(b,c))



def part2(data):
    positions = data
    velocities = [[0, 0, 0]] * len(data)
    # for step in range(1000):
    #     positions, velocities = time_step(positions, velocities)
    periods = []
    for axis in range(3):
        periods.append(find_period(
            [p[axis] for p in positions],
            [v[axis] for v in velocities],
        ))
    
    print(lcm2(*periods))


part2(data)