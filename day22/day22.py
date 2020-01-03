data = open("input1.txt").read().split("\n")
# data = """deal with increment 7
# deal with increment 9
# cut -2""".split("\n")

def new(deck):
    return deck[::-1]

def cut(deck, n):
    return deck[n:] + deck[:n]

def increment(deck, n):
    size = len(deck)
    out = [-1] * size
    ii = 0
    for card in deck:
        out[ii] = card
        ii = (ii + n) % size
    return out

def part1(data):
    deck = list(range(10007))
    for line in data:
        if "new" in line:
            deck = new(deck)
        elif "cut" in line:
            n = int(line.split(" ")[-1])
            deck = cut(deck, n)
        elif "increment" in line:
            n = int(line.split(" ")[-1])
            deck = increment(deck, n)
    print(deck.index(2019))


def undo_new(index, size):
    return size - index - 1

def undo_cut(index, size, n):
    return size - n - index


def part2(data):
    index = 2020
    size = 119315717514047
    # deck = list(range(size))
    print("about to start")
    # for line in data:
    #     if "new" in line:
    #         deck = new(deck)
    #     elif "cut" in line:
    #         n = int(line.split(" ")[-1])
    #         deck = cut(deck, n)
    #     elif "increment" in line:
    #         n = int(line.split(" ")[-1])
    #         deck = increment(deck, n)
    print("done")


# part1(data)
part2(data)