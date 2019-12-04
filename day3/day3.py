lines = open("input1.txt").read().split('\n')
data = [[(row[0], int(row[1:])) for row in line.split(",")] for line in lines]

def walk(grid, line, line_value):
    x,y = 0,0
    for direction, distance in line:
        if direction == 'U':
            for ii in range(1,distance):
                if (x, y + ii) not in grid:
                    grid[(x, y + ii)] = [line_value]
                else:
                    grid[(x, y + ii)].append(line_value)
            y += distance
        elif direction == 'D':
            for ii in range(1,distance):
                if (x, y - ii) not in grid:
                    grid[(x, y - ii)] = [line_value]
                else:
                    grid[(x, y - ii)].append(line_value)
            y -= distance
        elif direction == 'R':
            for ii in range(1,distance):
                if (x + ii, y) not in grid:
                    grid[(x + ii, y)] = [line_value]
                else:
                    grid[(x + ii, y)].append(line_value)
            x += distance
        elif direction == 'L':
            for ii in range(1,distance):
                if (x - ii, y) not in grid:
                    grid[(x - ii, y)] = [line_value]
                else:
                    grid[(x - ii, y)].append(line_value)
            x -= distance
        
    return grid

def part1(data):
    grid = {}
    for ii, line in enumerate(data):
        grid = walk(grid, line, ii)

    collisions = [(x,y) for ((x,y), v) in grid.items() if len(set(v)) > 1]
    print(min([(abs(x) + abs(y)) for (x,y) in collisions]))


def walk2(grid, line, line_value):
    x,y = 0,0
    d = -1
    for direction, distance in line:
        d += 1
        if direction == 'U':
            for ii in range(1,distance):
                d += 1
                if (x, y + ii) not in grid:
                    grid[(x, y + ii)] = {line_value: d}
                elif line_value not in grid[(x, y + ii)]:
                    grid[(x, y + ii)][line_value] = d
            y += distance
        elif direction == 'D':
            for ii in range(1,distance):
                d += 1
                if (x, y - ii) not in grid:
                    grid[(x, y - ii)] = {line_value: d}
                elif line_value not in grid[(x, y - ii)]:
                    grid[(x, y - ii)][line_value] = d
            y -= distance
        elif direction == 'R':
            for ii in range(1,distance):
                d += 1
                if (x + ii, y) not in grid:
                    grid[(x + ii, y)] = {line_value: d}
                elif line_value not in grid[(x + ii, y)]:
                    grid[(x + ii, y)][line_value] = d
            x += distance
        elif direction == 'L':
            for ii in range(1,distance):
                d += 1
                if (x - ii, y) not in grid:
                    grid[(x - ii, y)] = {line_value: d}
                elif line_value not in grid[(x - ii, y)]:
                    grid[(x - ii, y)][line_value] = d
            x -= distance
        
    return grid

def part2(data):
    grid = {}
    for ii, line in enumerate(data):
        grid = walk2(grid, line, ii)

    collisions = {(x,y): v for ((x,y), v) in grid.items() if len(v) > 1}
    print(min([sum(v.values()) for v in collisions.values()]))


# part1(data)
part2(data)