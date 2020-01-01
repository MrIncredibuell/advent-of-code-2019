from collections import defaultdict

data = [int(x) for x in open("input1.txt").read().split(",")]
class Computer:
    def __init__(self, data, inputs, index=0, name="Fred", on_output=None):
        self.data = defaultdict(int)
        for (ii, value) in enumerate(data):
            self.data[ii] = value
        self.inputs = inputs
        self.index = index
        self._outputs = []
        self.running = True
        self.name = name
        self.awaiting = False
        self.relative_base = 0
        self.on_output = on_output

    def parse_op(self):
        value = self.data[self.index]
        opcode = value % 100

        values = []
        modes = [(value // (10 ** e)) % 10 for e in range(2, 5)]
        for ii, m in enumerate(modes):
            try:
                parameter = self.data[self.index + 1 + ii]
                if m == 0:
                    values.append(self.data[parameter])
                elif m == 1:
                    values.append(parameter)
                elif m == 2:
                    values.append(self.data[self.relative_base + parameter])
                else:
                    raise NotImplementedError("Unknown parameter mode")
            except Exception as e:
                # print(e)
                values.append(None)

        if opcode in [1, 2, 7, 8]:
            if modes[2] == 0:
                values[2] = self.data[self.index + 3]
            elif modes[2] == 2:
                values[2] = self.relative_base + self.data[self.index + 3]
        if opcode in [3]:
            if modes[0] == 0:
                values[0] = self.data[self.index + 1]
            elif modes[0] == 2:
                values[0] = self.relative_base + self.data[self.index + 1]
            
        

        return opcode, values

    @staticmethod
    def get_increment(opcode):
        if opcode in [1, 2, 7, 8]:
            return 4
        elif opcode in [3, 4, 9]:
            return 2
        elif opcode in [5, 6]:
            return 3
        raise NotImplementedError(f"Unknown Opcode {opcode}")

    def process(self):
        op, (p1, p2, p3) = self.parse_op()

        if op == 99:
            self.running = False
            return
        elif op == 1:
            self.data[p3] = p1 + p2
        elif op == 2:
            self.data[p3] =  p1 *   p2
        elif op == 3:
            input_value = next(self.inputs)
            if input_value is None:
                self.awaiting = True
                return
            self.data[p1] = input_value
        elif op == 4:
            self._outputs.append(p1)
            if self.on_output is not None:
                self.on_output(p1)
        elif op == 5:
            if p1 != 0:
                self.index = p2
                return
        elif op == 6:
            if p1 == 0:
                self.index = p2
                return
        elif op == 7:
            if p1 < p2:
                self.data[p3] = 1
            else:
                self.data[p3] = 0
        elif op == 8:
            if p1 == p2:
                self.data[p3] = 1
            else:
                self.data[p3] = 0
        elif op == 9:
            self.relative_base += p1
        else:
            raise NotImplementedError(f"Unknown Opcode {op}")

        self.index = self.index + self.get_increment(op)

    def outputs(self):
        def gen():
            i = 0
            while True:
                if i >= len(self._outputs):
                    self.awaiting = True
                    yield None
                else:
                    yield self._outputs[i]
                    i += 1

        return gen()

    def run(self):
        self.awaiting = False
        while self.running and not self.awaiting:
            self.process()
        

def get_neighbors(location):
    x,y = location
    return [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
    ]

def find_candidates(grid):
    candidates = set([])
    for (location, value) in grid.items():
        # print(location)
        if value == 1:
            for c in get_neighbors(location):
                if c not in grid:
                    candidates.add(c)
    return candidates

def find_candidate(grid, source):
    to_visit = {source: []}
    visited = {}
    visiting = source
    path = []
    while True:
        del to_visit[visiting]
        neighbors = get_neighbors(visiting)

        for ii, n in enumerate(neighbors):
            new_path = path + [ii + 1]
            if grid.get(n) == 0:
                continue
            if n not in grid:
                return n, new_path
            if n not in visited:
                # if len(to_visit.get(n, new_path)) >= len(new_path):
                to_visit[n] = new_path
        
        visited[visiting] = path

        if len(to_visit) == 0:
            return None, []
        l, visiting = min([(len(path), node) for node, path in to_visit.items()])
  
        path = to_visit[visiting]

    return path

def find_longest_path(grid, source):
    to_visit = {source: []}
    visited = {}
    visiting = source
    path = []
    while len(to_visit) > 0:
        del to_visit[visiting]
        neighbors = get_neighbors(visiting)

        for ii, n in enumerate(neighbors):
            new_path = path + [ii + 1]
            if grid.get(n) == 0:
                continue
            if n not in grid:
                return n, new_path
            if n not in visited:
                # if len(to_visit.get(n, new_path)) >= len(new_path):
                to_visit[n] = new_path
        
        visited[visiting] = path

        if len(to_visit) == 0:
            return max([len(path) for path in visited.values()])
        l, visiting = min([(len(path), node) for node, path in to_visit.items()])
  
        path = to_visit[visiting]

    return path

def find_path(grid, source, destination):
    to_visit = {source: []}
    visited = {}
    visiting = source
    path = []
    while visiting != destination:
        neighbors = get_neighbors(visiting)
        for ii, n in enumerate(neighbors):
            if grid.get(n) == 0:
                continue
            new_path = path+[ii + 1]
            if n not in visited:
                if len(to_visit.get(n, new_path)) >= len(new_path):
                    to_visit[n] = new_path
        visited[visiting] = path
        del to_visit[visiting]

        l, visiting = min([(len(path), node) for node, path in to_visit.items()])
        path = to_visit[visiting]

    return path
        

def print_grid(grid, location=None):
    xs, ys = set([]), set([])
    for (x, y) in grid.keys():
        xs.add(x)
        ys.add(y)
    

    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            if (x, y) == location:
                row.append("X")
            elif grid.get((x, y)) == 0:
                row.append("#")
            elif grid.get((x, y)) == 1:
                row.append(".")
            elif grid.get((x, y)) == 2:
                row.append("0")

        print("".join(row))

def part1(data):
    grid = {(0, 0): 1}
    while True:
        (node, path) = find_candidate(grid, (0,0))
        c = Computer(data[:], inputs=None,)
        c.inputs = (x for x in path + [None])
        c.run()
        if 0 in c._outputs[:-1]:
            print("hit an early wall!")
        grid[node] = c._outputs[-1]
        if grid[node] == 2:
            print(len(path))
            return


def part2(data):
    grid = {(0, 0): 1}

    while True:
        # print(len(grid))
        (node, path) = find_candidate(grid, (0, 0))
        if not node:
            break
        c = Computer(data[:], inputs=None,)
        c.inputs = (x for x in path + [None])
        c.run()
        if 0 in c._outputs[:-1]:
            print("hit an early wall!")
        grid[node] = c._outputs[-1]
        if grid[node] == 2:
            source = node

    print("DONE")
    print(find_longest_path(grid, source))

# part1(data)
part2(data)