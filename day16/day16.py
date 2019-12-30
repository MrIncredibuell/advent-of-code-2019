import numpy as np

data = [int(c) for c in open("input1.txt").read()]
data = [int(c) for c in "80871224585914546619083218645595"]
# data = [int(c) for c in "12345678"]

def get_digit(index, data):
    base_pattern = [0, 1, 0, -1]
    d = 0
    for ii, x in enumerate(data):
        m = base_pattern[((ii + 1) // (index + 1)) % len(base_pattern)]
        d += (m * x)
    return abs(d) % 10

def phase(data):
    return [get_digit(ii, data) for ii in range(len(data))]


def part1(data):
    for ii in range(100):
        data = phase(data)
    print("".join([str(x) for x in data[:8]]))

def part2(data):
    data = data * 10000
    # print(len(data))

    base_pattern = [0, 1, 0, -1]
    m = []
    for jj in range(len(data)):
        row = [0] * len(data)
        # for ii in range(len(data)):
        #     row[ii] = base_pattern[((ii + 1) // (jj + 1)) % len(base_pattern)]
        m.append(row)
        print(jj / len(data))

    # operand = np.array(m)
    # data = np.array([data]).reshape(len(data), 1)
    # res = np.matmul(operand, data)
    # print(res)
            

    # for ii in range(1):
    #     data =
    # print("".join([str(x) for x in data[:8]])) 

# part1(data[:])
part2(data[:])