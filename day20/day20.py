from collections import defaultdict

data = open("input1.txt").read().split("\n")


class Maze:
    def __init__(self, data, recurse=False):
        upwarps = defaultdict(list)
        for x, c in enumerate(data[0]):
            if c != " ":
                upwarps[f"{c}{data[1][x]}"].append((x, 2))
        for x, c in enumerate(data[-1]):
            if c != " ":
                upwarps[f"{data[-2][x]}{c}"].append((x, len(data) - 3))

        for y in range(len(data)):
            if data[y][0] != " ":
                upwarps[f"{data[y][0]}{data[y][1]}"].append((2,y))

            if data[y][-1] != " ":
                upwarps[f"{data[y][-2]}{data[y][-1]}"].append((len(data[0]) - 3, y))


        x = len(data[0]) // 2
        y = len(data) // 2
        while data[y][x] not in [".", "#"]:
            y -= 1
        y += 1
        top = y
        while data[y][x] not in [".", "#"]:
            y += 1
        y -= 1
        bottom = y
        while data[y][x] not in [".", "#"]:
            x -= 1
        x += 1
        left = x
        while data[y][x] not in [".", "#"]:
            x += 1
        x -= 1
        right = x

        downwarps = defaultdict(list)
        for x in range(left, right + 1):
            if data[top][x] != " ":
                downwarps[f"{data[top][x]}{data[top+1][x]}"].append((x, top - 1))
            if data[bottom][x] != " ":
                downwarps[f"{data[bottom-1][x]}{data[bottom][x]}"].append((x, bottom + 1))
        for y in range(top, bottom + 1):
            if data[y][left] != " ":
                downwarps[f"{data[y][left]}{data[y][left + 1]}"].append((left - 1, y))
            if data[y][right] != " ":
                downwarps[f"{data[y][right -1]}{data[y][right]}"].append((right + 1, y))

        max_depth = 50

        edges = defaultdict(set)
        for depth in range(max_depth):
            for y in range(len(data)-1):
                for x in range(len(data[0])-1):
                    if data[y][x] == "." and data[y][x + 1] == ".":
                        edges[(x, y, depth)].add((x + 1, y, depth))
                        edges[(x + 1, y, depth)].add((x, y, depth))
                    if data[y][x] == "." and data[y+1][x] == ".":
                        edges[(x, y, depth)].add((x, y+1, depth))
                        edges[(x, y + 1, depth)].add((x, y, depth))

        
        warps = defaultdict(list)
        for k, v in downwarps.items():
            warps[k] += v
        for k, v in upwarps.items():
            warps[k] += v

        if recurse == False:
            for warp, locations in warps.items():
                if len(locations) == 2:
                    a, b = locations
                    edges[a].add(b)
                    edges[b].add(a)
        else:
            for depth in range(max_depth):
                for warp, locations in warps.items():
                    if len(locations) == 2:
                        a, b = locations
                        edges[(*a, depth)].add((*b, depth + 1))
                        edges[(*b, depth+1)].add((*a, depth))

        # print(warps)
        self.edges = edges
        self.nodes = set(edges.keys())
        self.start = (*warps["AA"][0], 0)
        self.end = (*warps["ZZ"][0], 0)
        self.data = data

    def bfs(self, start):
        to_visit = {start: []}
        visited = {}

        while to_visit:
            visiting, path = next(item for item in to_visit.items())
            for node in self.edges[visiting]:
                # if node in to_visit and len(to_visit[node]) >= len(path) + 1:
                #     print("HMM")
                # if node in visited and len(visited[node]) >= len(path) + 1:
                #     print("HMM")

                if (node not in to_visit) and (node not in visited):
                    to_visit[node] = path + [node]
            visited[visiting] = path
            del to_visit[visiting]
        return visited

    def print_path(self, path):
        s = ""
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if (x, y) in path:
                    s += "*"
                else:
                    s += char
            s += "\n"
        print(s)


        
def part1(data):
    m = Maze(data)
    paths = m.bfs(m.start)
    print(len(paths[m.end]))

def part2(data):
    m = Maze(data, recurse=True)
    paths = m.bfs(m.start)
    # for dest, path in paths.items():
    #     print(dest, path)
    print(len(paths[m.end]))


# part1(data)
part2(data)