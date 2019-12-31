from itertools import permutations, chain

data = [int(row) for row in open("input1.txt").read().split(",")]

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


class AwaitingInput(Exception):
    pass

class Computer:
    def __init__(self, data, inputs, index=0, name="Fred"):
        self.data = data
        self.inputs = inputs
        self.index = index
        self._outputs = []
        self.running = True
        self.name = name
        self.awaiting = False

    def parse_op(self):
        value = self.data[self.index]
        opcode = value % 100

        values = []
        for ii, p in enumerate([(value // 10 ** e) % 10 for e in range(2, 5)]):
            try:
                parameter = self.data[self.index + 1 + ii]
                if p == 0:
                    values.append(self.data[parameter])
                elif p == 1:
                    values.append(parameter)
                else:
                    raise NotImplementedError("Unknown parameter mode")
            except Exception as e:
                # print(e)
                values.append(None)
        

        return opcode, values

    @staticmethod
    def get_increment(opcode):
        if opcode in [1, 2, 7, 8]:
            return 4
        elif opcode in [3, 4]:
            return 2
        elif opcode in [5, 6]:
            return 3
        raise NotImplementedError(f"Unknown Opcode {opcode}")

    def get_value(self, mode, index):
        if mode == 0:
            return self.data[index]
        elif mode == 1:
            return index
        raise NotImplementedError("Unknown parameter mode")

    
    def process(self):
        op, (p1, p2, p3) = self.parse_op()

        if op == 99:
            self.running = False
            return
        elif op == 1:
            self.data[self.data[self.index + 3]] = p1 + p2
        elif op == 2:
            self.data[self.data[self.index + 3]] =  p1 *   p2
        elif op == 3:
            input_value = next(self.inputs)
            if input_value is None:
                self.awaiting = True
                return
            self.data[self.data[self.index + 1]] = input_value
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
                self.data[self.data[self.index + 3]] = 1
            else:
                self.data[self.data[self.index + 3]] = 0
        elif op == 8:
            if p1 == p2:
                self.data[self.data[self.index + 3]] = 1
            else:
                self.data[self.data[self.index + 3]] = 0

        self.index = self.index + self.get_increment(op)

    def outputs(self):
        def gen():
            i = 0
            # while i < len(self._outputs):
                # if i == len(self._outputs) and self.running:
                #     print(f"{self.name} should try to get more outputs")

            while True:
                if i >= len(self._outputs):
                    self.awaiting = True
                    # raise AwaitingInput(f"{self.name} tried to read output that doesn't exist")
                    yield None
                else:
                    # print(f"{self.name} output {self._outputs[i]}")
                    yield self._outputs[i]
                    i += 1

        return gen()

    def run(self):
        # print(f"{self.name} beginning an execution")
        self.awaiting = False
        while self.running and not self.awaiting:
            self.process()
        
        # print(f"{self.name} completed")


def part1(data):
    print(max(try_permutation(data, p) for p in permutations(range(5))))


def try_permutation_2(data, perm):
    computers = [Computer(data[:], None, name=f"Comp {i}") for i in range(5)]

    for ii, p in enumerate(perm):
        if ii == 0:
            init = (x for x in (p, 0,))
        else:
            init = (x for x in (p,))
        computers[ii].inputs = chain(
            init,
            computers[(ii - 1) % 5].outputs(),
        )

    ii = len(computers) - 1
    ii = 0
    while computers[-1].running == True:
        computers[ii].run()
        ii = (ii + 1) % 5
    return computers[-1]._outputs[-1]

def part2(data):
    print(max(try_permutation_2(data, p) for p in permutations(range(5, 10))))


part1(data[:])
part2(data[:])