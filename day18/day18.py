from math import inf
from collections import defaultdict
from itertools import permutations

data = open('input1.txt').read().split('\n')

class Maze:
    def __init__(self, data):
        self.start = None
        self.keys = {}
        self.doors = {}
        self.nodes = set([])
        self.paths = defaultdict(list)

        for y, row in enumerate(data):
            for x, c in enumerate(row):
                if c == '#':
                    continue
                else:
                    self.nodes.add((x, y))
                    if c == '.':
                        continue
                    elif c == '@':
                        self.start = (x, y)
                    elif c.isupper():
                        self.doors[c] = (x, y)
                    else:
                        self.keys[c] = (x, y)
        self.keyLocations = {v: k for k, v in self.keys.items()}
        self.doorLocations = {v: k for k, v in self.doors.items()}
        
        self.memoization = {}
                        
    def dfs(self, startPosition, visitedNodes):
        x, y = startPosition
        path = visitedNodes[:] + [(x, y)]

        candidates = set([
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]).intersection(self.nodes).difference(visitedNodes)

        if len(candidates) == 0:
            return [path]
        
        paths = []
        for c in candidates:
            paths += self.dfs(c, path)

        return paths

    def findAllPaths(self):
        for source in [self.start] + list(self.keys.values()):
            paths = self.dfs(source, [])
            for p in paths:
                requires = set([])
                for ii, node in enumerate(p[1:]):
                    if node in self.doorLocations:
                        requires.add(self.doorLocations[node].lower())
                    if node in self.keyLocations:
                        if len([path for path in self.paths[(source, node)] if path["path"] == p[1:ii+1]]) == 0:
                            self.paths[(source, node)].append(
                                {
                                    "requires": requires.copy(),
                                    "length": ii + 1,
                                    "path": p[1:ii +1]
                                })

    def tryPermutation(self, currentNode, visited):
        if (currentNode, str(sorted(visited))) in self.memoization:
            return self.memoization[(currentNode, str(sorted(visited)))]
        if len(visited) == len(self.keys):
            return 0
        lengths = [inf]
        for key, nextNode in self.keys.items():
            if key in visited:
                continue
            paths = [
                path for path in self.paths[(currentNode, nextNode)]
                if len(path["requires"].difference(visited)) == 0
            ]
            if len(paths) == 0:
                continue
            lengths.append(
                min([path['length'] for path in paths]) + self.tryPermutation(nextNode, visited + [key]))

        l = min(lengths)
        self.memoization[(currentNode, str(sorted(visited)))] = l
        return l
            
    def tryAllPermutations(self):
        return self.tryPermutation(self.start, [])


def part1(data):
    m = Maze(data)
    paths = m.dfs(m.start, [])
    m.findAllPaths()
    print(m.tryAllPermutations())
    

part1(data)