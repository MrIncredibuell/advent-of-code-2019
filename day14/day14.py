import math
from collections import defaultdict

def parse_data(lines):
    data = {}
    for line in lines:
        parsed_inputs = []
        inputs, output = line.split(" => ")
        for term in inputs.split(", "):
            count, name = term.split(" ")
            parsed_inputs.append({"count": int(count), "name": name})
        count, name = output.split(" ")
        data[name] = {
            "count": int(count),
            "inputs": parsed_inputs
        }

    return data

data = parse_data(open("input1.txt").read().split("\n"))

def get_required_inputs(data, output, count, remainders):
    if output == "ORE":
        return count, remainders
    if output in remainders:
        diff = min(remainders[output], count)
        count -= diff
        remainders[output] -= diff
    required = data[output]
    multiple = math.ceil(count / required["count"])
    required_count = 0
    for requirement in required["inputs"]:
        inc, remainders = get_required_inputs(
            data=data,
            output=requirement["name"],
            count=requirement["count"] * multiple,
            remainders=remainders
        )
        required_count += inc
    if multiple * required["count"] > count:
        remainders[output] += (multiple * required["count"]) - count
    return required_count, remainders


def part1(data):
    print(get_required_inputs(data, "FUEL", 1, defaultdict(int))[0])

def binary_search(f, target, lower, upper):
    if lower == upper:
        return lower

    # I always fuck up the base case for binary search so don't worry about it
    if upper - lower < 10:
        for n in range(lower, upper + 1):
            if f(n)[0] > target:
                return n - 1
        return upper + 1

    mid = (lower + upper) // 2
    result = f(mid)[0]
    if result == target:
        return mid
    elif result > target:
        return binary_search(f, target, lower, mid)
    else:
        return binary_search(f, target, mid, upper) 

def part2(data):
    n = 1
    target = 1000000000000
    while get_required_inputs(data, "FUEL", n, defaultdict(int))[0] <= target:
        n *= 2

    result = binary_search(
        lambda x: get_required_inputs(data, "FUEL", x, defaultdict(int)),
        target=target,
        lower=n // 2,
        upper=n,
    )

    print(result)

part1(data)
part2(data)