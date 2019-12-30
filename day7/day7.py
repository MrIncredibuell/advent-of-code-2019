from itertools import permutations

data = [int(row) for row in open("input1.txt").read().split(",")]
data = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

def parse_op(value):
    opcode = value % 100
    p1 = (value // 100) % 10
    p2 = (value // 1000) % 10
    p3 = (value // 10000) % 10
    return opcode, p1, p2, p3

def get_increment(opcode):
    if opcode in [1, 2, 7, 8]:
        return 4
    elif opcode in [3, 4]:
        return 2
    elif opcode in [5, 6]:
        return 3
    raise NotImplementedError(f"Unknown Opcode {opcode}")

def get_value(mode, index, data, inputs):
    if mode == 0:
        return data[index]
    elif mode == 1:
        return index
    raise NotImplementedError("Unknown parameter mode")

def process(index, data, inputs, outputs):
    op, m1, m2, m3 = parse_op(data[index])

    try:
        p1 = get_value(m1, data[index + 1], data, inputs)
    except:
        p1 = None
    
    try:
        p2 = get_value(m2, data[index + 2], data, inputs)
    except:
        p2 = None
    
    try:
        p3 = get_value(m3, data[index + 3], data, inputs)
    except:
        p3 = None

    if op == 99:
        return None, data, inputs, outputs
    elif op == 1:
        data[data[index + 3]] = p1 + p2
    elif op == 2:
        data[data[index + 3]] =  p1 *   p2
    elif op == 3:
        data[data[index + 1]] = next(inputs)
    elif op == 4:
        outputs.append(p1)
    elif op == 5:
        if p1 != 0:
            return p2, data, inputs, outputs
    elif op == 6:
        if p1 == 0:
            return p2, data, inputs, outputs
    elif op == 7:
        if p1 < p2:
            data[data[index + 3]] = 1
        else:
            data[data[index + 3]] = 0
    elif op == 8:
        if p1 == p2:
            data[data[index + 3]] = 1
        else:
            data[data[index + 3]] = 0

    return index + get_increment(op), data, inputs, outputs

def constant_inputs(x):
    while True:
        yield x

def run_to_completion(data, inputs):
    data = data[:]
    index = 0
    outputs = []
    while index is not None:
        index, data, inputs, outputs = process(index, data, inputs, outputs)
    return outputs[-1]

def try_permutation(data, p):
    output = 0
    for i in p:
        output = run_to_completion(data, (x for x in (i, output)))
    return output


class Computer:
    def __init__(self, data, inputs, index=0):
        self.data = data
        self.inputs = inputs
        self.index = index
        self._outputs = []
        self.running = True

    @staticmethod
    def parse_op(value):
        opcode = value % 100
        p1 = (value // 100) % 10
        p2 = (value // 1000) % 10
        p3 = (value // 10000) % 10
        return opcode, p1, p2, p3

    @staticmethod
    def get_increment(opcode):
        if opcode in [1, 2, 7, 8]:
            return 4
        elif opcode in [3, 4]:
            return 2
        elif opcode in [5, 6]:
            return 3
        raise NotImplementedError(f"Unknown Opcode {opcode}")

    @staticmethod
    def get_value(mode, index, data, inputs):
        if mode == 0:
            return data[index]
        elif mode == 1:
            return index
        raise NotImplementedError("Unknown parameter mode")

    
    def process(self):
        data = self.data
        index = self.index
        op, m1, m2, m3 = parse_op(data[index])

        try:
            p1 = get_value(m1, data[index + 1], data, self.inputs)
        except:
            p1 = None
        
        try:
            p2 = get_value(m2, data[index + 2], data, self.inputs)
        except:
            p2 = None
        
        try:
            p3 = get_value(m3, data[index + 3], data, self.inputs)
        except:
            p3 = None

        if op == 99:
            self.running = False
            return
        elif op == 1:
            data[data[index + 3]] = p1 + p2
        elif op == 2:
            data[data[index + 3]] =  p1 *   p2
        elif op == 3:
            data[data[index + 1]] = next(self.inputs)
        elif op == 4:
            self._outputs.append(p1)
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
                data[data[index + 3]] = 1
            else:
                data[data[index + 3]] = 0
        elif op == 8:
            if p1 == p2:
                data[data[index + 3]] = 1
            else:
                data[data[index + 3]] = 0

        self.index = index + get_increment(op)

    def outputs(self):
        def gen():
            i = 0
            while i < len(self.outputs):
                yield self.outputs[i]
                i += 1
            raise Exception("Tried to read output that doesn't exist")
        return gen()

    def run(self):
        while self.running:
            self.process()


def part1(data):
    print(max(try_permutation(data, p) for p in permutations(range(5))))


def part2(data):
   c = Computer(data, (x for x in (0, 0)))
   outputs = c.outputs()
   c.run()
   print(outputs)
   

# part1(data[:])
part2(data[:])