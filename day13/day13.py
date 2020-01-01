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
        


def parse_output(out, screen = None, score = 0):
    screen = screen or {}
    score = score
    for ii in range(len(out) // 3):
        ii *= 3
        x = out[ii]
        y = out[ii + 1]
        value = out[ii + 2]
        if x == -1 and y == 0:
            score = value
        else:
            screen[(x, y)] = value

    return screen, score


def part1(data):
    c = Computer(data,inputs=None)
    c.run()
    out = c._outputs
    screen, score = parse_output(c._outputs)
    print(len([v for v in screen.values() if v == 2]))


def print_screen(screen, score):
    xs, ys = set([]), set([])
    for (x, y) in screen.keys():
        xs.add(x)
        ys.add(y)
    

    for y in range(min(ys), max(ys) + 1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            if screen.get((x, y)) == 1:
                row.append("#")
            elif screen.get((x, y)) == 2:
                row.append("B")
            elif screen.get((x, y)) == 3:
                row.append("-")
            elif screen.get((x, y)) == 4:
                row.append("O")
            else:
                row.append(" ")
        print("".join(row))
    print(score)


def part2(data):
    data = data[:]
    data[0] = 2
    c = Computer(data, inputs=(x for x in [None]))
    screen = {}
    score = 0
    while c.running:
        c.run()
        
        out = c._outputs
        screen, score = parse_output(c._outputs, screen=screen, score=score)
        c._outputs = []
        balls = [key for (key, value) in screen.items() if value == 4]
        ball_x = balls[0][0]
        pads = [key for (key, value) in screen.items() if value == 3]
        pad_x = pads[0][0]

        inp = 0
        if pad_x < ball_x:
            inp = 1
        elif pad_x > ball_x:
            inp = -1
        c.inputs = (x for x in [inp, None])

    print(score)


part1(data)
part2(data)