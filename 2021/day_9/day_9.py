import argparse
from functools import cached_property


Coordinates = tuple[int, int]
Map = list[list[int]]
Basin = set[Coordinates]


class Heightmap:
    def __init__(self, heightmap: Map):
        self.heightmap = heightmap

    @property
    def risk_level(self) -> int:
        return sum(self.heightmap[y][x] + 1 for x, y in self.low_points)

    @cached_property
    def low_points(self) -> list[Coordinates]:
        return [
            (x, y) for x in range(len(self.heightmap[0])) for y in range(len(self.heightmap))
            if self.is_low_point(x, y)
        ]

    @cached_property
    def basins(self) -> list[Basin]:
        def spread_basin(basin, x, y):
            for adj_x, adj_y in self.get_adjacent(x, y):
                if self.heightmap[adj_y][adj_x] == 9 or (adj_x, adj_y) in basin:
                    continue
                basin.add((adj_x, adj_y))
                basin.union(spread_basin(basin, adj_x, adj_y))
            return basin

        basins = [spread_basin(set(), x, y) for x, y in self.low_points]
        return sorted(basins, key=len)

    def get_adjacent(self, x: int, y: int) -> list[Coordinates]:
        delta = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [
            (x + dx, y + dy) for dx, dy in delta
            if 0 <= x + dx < len(self.heightmap[0]) and 0 <= y + dy < len(self.heightmap)
        ]

    def is_low_point(self, x: int, y: int) -> bool:
        return all(
            self.heightmap[y][x] < self.heightmap[adj_y][adj_x]
            for adj_x, adj_y in self.get_adjacent(x, y)
         )

    def __str__(self) -> str:
        out = ''
        biggest_basins = set.union(*self.basins[-3:])
        for y, row in enumerate(self.heightmap):
            for x, cell in enumerate(row):
                if (x, y) in self.low_points or (x, y) in biggest_basins:
                    out += f'\033[1m\u001b[48;5;{16 + cell}m{cell}\033[0m'
                else:
                    out += f'{cell}'
            out += '\n'
        return out


def parse_file(file_name: str) -> Heightmap:
    with open(file_name, encoding='utf-8') as input_file:
        return Heightmap([[int(cell) for cell in row] for row in input_file.read().splitlines()])


def run() -> None:
    parser = argparse.ArgumentParser(description='Check low points.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    heightmap = parse_file(args.file_name)
    print(heightmap)
    print(f'Part 1: {heightmap.risk_level}')
    prod = len(heightmap.basins[-1]) * len(heightmap.basins[-2]) * len(heightmap.basins[-3])
    print(f'Part 2: {prod}')


if __name__ == '__main__':
    run()
