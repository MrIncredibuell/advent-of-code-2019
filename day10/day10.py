import math

rows = open("input1.txt").read().split("\n")


def can_see(source, destination, asteroids):
    (x1, y1) = source
    (x2, y2) = destination
    rise = y2 - y1
    run = x2 - x1

    x_direction = -1 if run < 0 else 1
    y_direction = -1 if rise < 0 else 1

    if run == 0:
        if rise == 0:
            return False # same asteroid
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            if (x1, y) in asteroids:
                return False
    elif rise == 0:
        for x in range(min(x1, x2) + 1, (max(x1, x2))):
            if (x, y1) in asteroids:
                return False

    else:
        slope = rise / run
        x = x1 + x_direction
        y = y1
        delta = 1
        while (x != x2) and (y != y2):
            y = (y1 + ( x_direction * slope * delta))
            if y == int(y) and (x, int(y)) in asteroids:
                return False
                
            x += x_direction
            delta += 1
        
    return True

def part1(rows):
    asteroids = []
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            if value == "#":
                asteroids.append((x, y))

    counts = {}
                
    for source in asteroids:
        visible = []
        for destination in asteroids:
            if can_see(source, destination, asteroids):
                visible.append(destination)

        counts[source] = len( visible)


    count, source = max((count, source) for (source, count) in counts.items())
    print(count, source)
    return source

def part2(rows):
    asteroids = []
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            if value == "#":
                asteroids.append((x, y))


    center_x, center_y = part1(rows[:])
    asteroids.remove((center_x, center_y))

    
    polar_coordinates = []
    for (x, y) in asteroids:
        theta = -1 * (math.atan(-1 * (y - center_y) / (x - center_x) if x != center_x else (math.inf if y > center_y else - 1 * math.inf)) + (math.pi / 2))
        radius = (((x - center_x) ** 2 + (y-center_y) ** 2) ** (0.5))
        
        while theta < 0:
            theta += math.pi
        
        if x < center_x:
            theta += math.pi
        if x == center_x and y > center_y:
            theta += math.pi

        while theta > math.pi * 2:
            theta -= 2 * math.pi
        polar_coordinates.append({
            "original": (x, y),
            "theta": theta,
            "radius": radius
        })

    count = 0

    while len(polar_coordinates) > 0:
        last_theta = None
        coordinates = sorted(
            polar_coordinates,
            key=lambda k: (k["theta"], k["radius"])
        )
        remaining = []

        for v in coordinates:
            if v["theta"] == last_theta:
                remaining.append(v)
            else:
                count += 1
                last_theta = v["theta"]
                # if count in [1,2,3,10,20,50,100,199,200,201,299]:
                if count == 200:
                    print(f"removing {count}: {v['original']}, {v['theta']}, {v['radius']}")

        polar_coordinates = remaining


    return 

part2(rows)