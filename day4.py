from collections import defaultdict

Map = dict[int, dict[int, str]]


def read_lines() -> list[str]:
    lines: list[str] = []
    with open("inputs/day4.txt") as f:
        for line in f.readlines():
            lines.append(line.strip().upper())

    return lines


def count_word_occurrences(map: Map, x: int, y: int) -> int:
    occurrences = 0
    if map[x][y] != "X":
        return 0

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            characters: str = ""
            for k in range(len("XMAS")):
                i = x + k * dx
                j = y + k * dy
                characters += map[i][j]

            if characters == "XMAS":
                occurrences += 1

    return occurrences


def is_cross_mas(map: Map, x: int, y: int) -> int:
    if map[x][y] != "A":
        return 0

    try:
        ch = map[x][y]
        tl = map[x - 1][y + 1]
        tr = map[x + 1][y + 1]
        bl = map[x - 1][y - 1]
        br = map[x + 1][y - 1]
    except IndexError:
        return 0

    diagonals = [
        "".join([tl, ch, br]),
        "".join([bl, ch, tr]),
    ]

    is_match = True
    for diagonal in diagonals:
        if diagonal != "MAS" and diagonal != "SAM":
            is_match = False
            break

    return 1 if is_match else 0


def solve() -> None:
    lines = read_lines()

    width = len(lines[0])
    height = len(lines)

    map: dict[int, dict[int, str]] = defaultdict(lambda: defaultdict(lambda: "."))
    for x in range(width):
        for y in range(height):
            map[x][y] = lines[y][x]

    part_1 = sum(
        count_word_occurrences(map, x, y) for x in range(width) for y in range(height)
    )
    part_2 = sum([is_cross_mas(map, x, y) for x in range(width) for y in range(height)])

    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == "__main__":
    solve()
