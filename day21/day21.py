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

def part1(data):
    c = Computer(data, inputs=(x for x in [None]))
    c.run()
    # print("".join([chr(x) for x in c._outputs]))
    
    program = [
        "NOT A T",
        "NOT B J",
        "OR J T",
        "NOT C J",
        "OR J T",
        "NOT T J",
        "NOT J J",
        "AND D J",
        "WALK",
        ""
    ]
    program = [x for x in "\n".join(program)] + [None]

    c.inputs = (ord(x) for x in program)
    c.run()
    print(c._outputs[-1])


def part2(data):
    c = Computer(data, inputs=(x for x in [None]))
    c.run()
    
    program = [
        # CAN DO A SECOND JUMP
        "OR E T",
        "AND I T",
        "OR H J",
        "OR T J",
        "AND D J",

        # DON'T JUMP IF ALL CLEAR
        "NOT A T",
        "NOT T T",
        "AND B T",
        "AND C T",
        "NOT T T",
        "AND T J",
        
        # JUMP IF NO CHOICE
        "NOT A T",
        "OR T J",

        "RUN",
        ""
    ]
    program = [x for x in "\n".join(program)] + [None]

    c.inputs = (ord(x) for x in program)
    c.run()
    print(c._outputs[-1])

# part1(data)
part2(data)