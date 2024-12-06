import sys
from collections import Counter
from dataclasses import dataclass
from time import sleep
from typing import Literal

TileKind = Literal["ground"] | Literal["obstacle"]
Orientation = Literal["north"] | Literal["east"] | Literal["south"] | Literal["west"]


@dataclass
class Guard:
    x: int
    y: int
    orientation: Orientation

    def __str__(self) -> str:
        return f"Guard({self.x}, {self.y}, {self.orientation})"


@dataclass
class Tile:
    x: int
    y: int
    kind: TileKind

    def __str__(self) -> str:
        return f"Tile({self.x}, {self.y}, {self.kind})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class GuardError(Exception):
    pass


class World:
    guard: Guard
    width: int
    height: int
    tiles: list[Tile]
    path: list[Tile]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = [Tile(x, y, "ground") for y in range(height) for x in range(width)]
        self.path = []
        self.guard = Guard(0, 0, "north")

    def update(self) -> bool:
        try:
            self.move_guard()
            return True
        except GuardError:
            return False

    def render(self) -> None:
        lines: list[str] = []
        lines.append("".join(["╔"] + ["═" for _ in range(self.width)] + ["╗"]))
        for y in range(self.height):
            line: str = "║"
            for x in range(self.width):
                tile = self.get_tile(x, y)
                if tile.kind == "obstacle":
                    line += "█"
                else:
                    line += " "
            line += "║"

            lines.append(line)

        lines.append("".join(["╚"] + ["═" for _ in range(self.width)] + ["╝"]))

        for tile in self.path:
            line = lines[tile.y + 1]
            lines[tile.y + 1] = line[: tile.x + 1] + "░" + line[tile.x + 2 :]

        guard_symbol = "O"
        match self.guard.orientation:
            case "north":
                guard_symbol = "▲"
            case "east":
                guard_symbol = "►"
            case "south":
                guard_symbol = "▼"
            case "west":
                guard_symbol = "◄"

        line = lines[self.guard.y + 1]
        lines[self.guard.y + 1] = (
            line[: self.guard.x + 1] + guard_symbol + line[self.guard.x + 2 :]
        )

        output = "\n".join(lines)
        sys.stdout.write(f"\r{output}")
        sys.stdout.flush()

    def move_guard(self) -> None:
        try:
            next_tile = self.get_next_tile()
        except IndexError:
            raise GuardError("Guard has exited the world")

        rotations = 0
        while next_tile.kind == "obstacle":
            match self.guard.orientation:
                case "north":
                    self.guard.orientation = "east"
                case "east":
                    self.guard.orientation = "south"
                case "south":
                    self.guard.orientation = "west"
                case "west":
                    self.guard.orientation = "north"

            rotations += 1
            if rotations == 4:
                raise GuardError("Guard is stuck in a loop")

            next_tile = self.get_next_tile()

        self.guard.x = next_tile.x
        self.guard.y = next_tile.y
        self.path.append(next_tile)

    def get_next_tile(self) -> Tile:
        match self.guard.orientation:
            case "north":
                return self.get_tile(self.guard.x, self.guard.y - 1)
            case "east":
                return self.get_tile(self.guard.x + 1, self.guard.y)
            case "south":
                return self.get_tile(self.guard.x, self.guard.y + 1)
            case "west":
                return self.get_tile(self.guard.x - 1, self.guard.y)

    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[y * self.width + x]

    @property
    def visited_tiles(self) -> list[Tile]:
        tiles = Counter([tile for tile in self.path if tile.kind == "ground"])
        return list(tiles.keys())


def parse_world() -> World:
    orientation_symbols: dict[str, Orientation] = {
        ">": "east",
        "<": "west",
        "^": "north",
        "v": "south",
    }

    with open("inputs/day6.txt") as f:
        lines = f.readlines()
        world = World(
            height=len(lines),
            width=len(lines[0]),
        )

        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                tile = world.get_tile(int(x), int(y))

                match c:
                    case ".":
                        tile.kind = "ground"
                    case "#":
                        tile.kind = "obstacle"
                    case ">" | "<" | "^" | "v":
                        tile.kind = "ground"
                        world.guard = Guard(x, y, orientation_symbols[c])

        return world


def solve() -> None:
    world = parse_world()

    is_running = True
    ticks = 0
    while is_running:
        is_running = world.update()
        world.render()
        ticks += 1
        sleep(0.1)

    print(f"Completed in {ticks} ticks!")

    # debug_world(world)
    print("Part 1:", len(world.visited_tiles))


if __name__ == "__main__":
    solve()
