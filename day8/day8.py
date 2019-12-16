data = [int(x) for x in open("input1.txt").read()]

# data = [int(x) for x in "0222112222120000"]

def parse_layers(data, width, height):
    layer_size = width * height
    layers = [{} for i in range (len(data) // layer_size)]
    for index, value in enumerate(data):

        remainder = index % layer_size
        layer = index // layer_size
        x = remainder % width
        y = remainder // width
        layers[layer][(x, y)] = value
        
    return layers

def part1(data):
    layers = parse_layers(data, 25, 6)
    num_zeros, layer = min([(list(layer.values()).count(0), layer) for layer in layers])
    values = list(layer.values())
    print(values.count(1) * values.count(2))

def get_value(x, y, layers):
    for layer in layers:
        if layer[(x, y)] == 2:
            continue
        return "*" if layer[(x, y)] == 1 else " "
    raise Exception(f"All transparent at ({x}, {y})")

def part2(data):
    width = 25
    height = 6
    layers = parse_layers(data, width, height)
    # output_layer = [[2] * width for ii in range(height)]
    output = ""
    for y in range(height):
        for x in range(width):
            output += get_value(x, y, layers)
        output += "\n"

    print(output)


# part1(data[:])
part2(data[:])