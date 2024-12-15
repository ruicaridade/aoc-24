"""
This is totally over-engineered, but I wanted to have some fun with it :)
"""

import os
from collections import Counter
from dataclasses import dataclass
from time import sleep, time
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

    _last_tile: Tile | None
    _buffer: list[list[str]]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = [Tile(x, y, "ground") for y in range(height) for x in range(width)]
        self.path = []
        self.guard = Guard(0, 0, "north")

        self._last_tile = None
        self._buffer = [
            ["╔"] + ["═" for _ in range(width)] + ["╗"],
            *(["║"] + [" " for _ in range(width)] + ["║"] for _ in range(height)),
            ["╚"] + ["═" for _ in range(width)] + ["╝"],
        ]

    def load(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                if tile.kind == "obstacle":
                    self._buffer[y + 1][x + 1] = "█"
                else:
                    self._buffer[y + 1][x + 1] = " "

    def update(self) -> bool:
        try:
            self.move_guard()
            return True
        except GuardError:
            return False

    def render(self) -> None:
        if self._last_tile and self._last_tile.kind == "ground":
            self._buffer[self._last_tile.y + 1][self._last_tile.x + 1] = "░"

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

        self._buffer[self.guard.y + 1][self.guard.x + 1] = guard_symbol

        output = "\n".join(["".join(row) for row in self._buffer])
        world_metadata = f"World: {self.width}x{self.height}"
        guard_metadata = f"Guard: {self.guard}"
        visited_tiles = f"Visited tiles: {len(self.visited_tiles)}"

        os.system("clear")
        print(
            f"{output}"
            f"\n\n{world_metadata}"
            f"\n{guard_metadata}"
            f"\n{visited_tiles}\n",
        )

    def move_guard(self) -> None:
        current_tile = self.get_tile(self.guard.x, self.guard.y)
        if not self.path:
            self.path.append(current_tile)

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
        self._last_tile = current_tile

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
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Tile is out of bounds!")

        return self.tiles[y * self.width + x]

    @property
    def visited_tiles(self) -> list[Tile]:
        tiles = Counter([tile for tile in self.path if tile.kind == "ground"])
        return list(tiles.keys())

    def __str__(self) -> str:
        return f"World({self.width}, {self.height})"


def parse_world() -> World:
    orientation_symbols: dict[str, Orientation] = {
        ">": "east",
        "<": "west",
        "^": "north",
        "v": "south",
    }

    with open("inputs/day6.txt") as f:
        content = f.read()
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        world = World(
            height=len(lines),
            width=len(lines[0]),
        )
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
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
    world.load()

    start_time = time()
    tick_rate = 360
    sleep_seconds = 1 / tick_rate

    is_running = True
    while is_running:
        is_running = world.update()
        world.render()
        sleep(sleep_seconds)

    # debug_world(world)
    end_time = time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    print("Part 1:", len(world.visited_tiles))


if __name__ == "__main__":
    solve()
