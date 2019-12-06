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

def part1(data):
    index = 0
    inputs = constant_inputs(1)
    outputs = []
    while index is not None:
        index, data, inputs, outputs = process(index, data, inputs, outputs)

    print(outputs[-1])

def part2(data):
    index = 0
    inputs = constant_inputs(5)
    outputs = []
    while index is not None:
        index, data, inputs, outputs = process(index, data, inputs, outputs)

    print(outputs[-1])

part1(data[:])
part2(data[:])