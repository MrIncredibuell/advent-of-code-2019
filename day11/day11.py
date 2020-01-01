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
        


class Hull():
    def __init__(self, starting_color=0):
        self.location = (0, 0)
        self.direction = 0 # up
        self.grid = {(0,0): starting_color}
        self.paint_next = True # True if we expect the next input to be a color

    def __next__(self):
        color = self.grid.get(self.location)
        if color is None:
            color = 0
        return color

    def handle_input(self, value):
        if self.paint_next:
            self.grid[(self.location)] = value
            self.paint_next = False
        else:
            if value == 0:
                self.direction = (self.direction - 1) % 4
            else:
                self.direction = (self.direction + 1) % 4

            (x,y) = self.location
            if self.direction == 0:
                self.location = (x, y - 1)
            elif self.direction == 1:
                self.location = (x + 1, y)
            elif self.direction == 2:
                self.location = (x, y + 1)
            elif self.direction == 3:
                self.location = (x - 1, y)
            else:
                raise Exception("I'M LOST")
        
            self.paint_next = True

def part1(data):
    h = Hull()
    c = Computer(data, inputs=h, on_output=h.handle_input)
    c.run()
    print(len(h.grid))

def part2(data):
    h = Hull(starting_color=1)
    c = Computer(data, inputs=h, on_output=h.handle_input)
    c.run()
    xs, ys = set([]), set([])
    for (x, y) in h.grid.keys():
        xs.add(x)
        ys.add(y)
    

    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            if h.grid.get((x, y)) == 1:
                row.append("#")
            else:
                row.append(" ")
        print("".join(row))


part1(data)
part2(data)