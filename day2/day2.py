data = [int(row) for row in open("input1.txt").read().split(",")]

def process(index, data):
    op = data[index]
    if op == 99:
        return None, data
    elif op == 1:
        data[data[index+3]] = data[data[index + 1]] + data[data[index + 2]]
    elif op == 2:
        data[data[index+3]] = data[data[index + 1]] * data[data[index + 2]]

    return index + 4, data

def part1(data):
    index = 0
    data[1] = 12
    data[2] = 2
    while index is not None:
        index, data = process(index, data)

    print(data[0])

def part2(data):
    for noun in range(100):
        for verb in range(100):
            index = 0
            tempData = data[:]
            tempData[1] = noun
            tempData[2] = verb
            while index is not None:
                index, tempData = process(index, tempData)
            if tempData[0] == 19690720:
                print( (noun * 100) + verb)
                return


part1(data[:])
part2(data[:])