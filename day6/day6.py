from collections import defaultdict

data = [l.split(")") for l in open("input1.txt").read().split("\n")]


def part1(data):
    graph = defaultdict(list)
    reverse_graph = {}
    for source, dest in data:
        graph[source] += [dest]
        reverse_graph[dest] = source

    visited = {"COM": 0}
    to_visit = set(graph["COM"])
    while to_visit:
        planet = to_visit.pop()
        visited[planet] = visited[reverse_graph[planet]] + 1
        to_visit.update(graph[planet])

    print(sum(visited.values()))

def part2(data):
    graph = defaultdict(list)
    for source, dest in data:
        graph[source] += [dest]
        graph[dest] += [source]

    # BREADTH FIRST SEARCH
    visited = {"SAN": 0}
    to_visit = {p: 1 for p in graph["SAN"]}
    while to_visit:
        dist = min(to_visit.values())
        planet = [key for key in to_visit.keys() if to_visit[key] == dist][0]
        del to_visit[planet]
        visited[planet] = dist
        
        for p in graph[planet]:
            if p not in to_visit and p not in visited:
                to_visit[p] = dist + 1

    print(visited["YOU"]-2)

part1(data)
part2(data)