from collections import defaultdict


def parse_lists() -> tuple[list[int], list[int]]:
    left, right = [], []
    with open("inputs/day1.txt") as f:
        for line in f.read().splitlines():
            tokens = [x for x in line.split(" ") if x]
            left.append(int(tokens[0].strip()))
            right.append(int(tokens[1].strip()))

    return left, right


def part_1():
    left, right = parse_lists()
    if len(left) != len(right):
        raise ValueError("Lists are not of the same length, input might be wrong?")

    left.sort()
    right.sort()

    deviation = 0
    for i in range(len(left)):
        deviation += abs(right[i] - left[i])

    print(deviation)


def part_2():
    left, right = parse_lists()
    if len(left) != len(right):
        raise ValueError("Lists are not of the same length, input might be wrong?")

    matches = defaultdict(int)
    for n in right:
        matches[n] += 1

    similarity = 0
    for n in left:
        similarity += n * matches[n]

    print(similarity)


if __name__ == "__main__":
    part_1()
    part_2()
