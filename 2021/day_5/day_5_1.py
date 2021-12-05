from copy import deepcopy
from dataclasses import dataclass
from collections import defaultdict
from typing import NamedTuple
import argparse
import numpy


class Coordinates(NamedTuple):
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class Segment:
    start: Coordinates
    end: Coordinates


class PathMap:
    def __init__(self) -> None:
        self.hit_map = defaultdict(lambda: defaultdict(int))
        self.max_x: int = 0
        self.max_y: int = 0

    def hit(self, point: Coordinates) -> int:
        self.max_x = max(self.max_x, point.x)
        self.max_y = max(self.max_y, point.y)
        self.hit_map[point.x][point.y] += 1
        return self.hit_map[point.x][point.y]

    def __str__(self):
        hit_map = deepcopy(self.hit_map)
        output = ''
        for y in range(self.max_y + 1):
            row = ''
            for x in range(self.max_x + 1):
                if hit_map[x][y] == 0:
                    row += '. '
                elif hit_map[x][y] == 1:
                    row += '\033[1m\u001b[33m1 \033[0m'
                else:
                    row += f'\033[1m\u001b[35m{hit_map[x][y]} \033[0m'
            output += f'{row}\n'
        return output


def parse_file(file_name: str) -> set[Segment]:
    with open(file_name, encoding='utf-8') as input_file:
        segments = set()
        raw_segments = [line.split(' -> ') for line in input_file.read().splitlines()]
        for raw_start, raw_end in raw_segments:
            start_coordinates = Coordinates(
                *(int(coordenate) for coordenate in raw_start.split(','))
            )
            end_coordinates = Coordinates(
                *(int(coordenate) for coordenate in raw_end.split(','))
            )
            segments.add(Segment(start_coordinates, end_coordinates))
        return segments


def get_segment_path(segment: Segment) -> list[Coordinates]:
    start, end = segment.start, segment.end
    delta_x = abs(end.x - start.x)
    delta_y = abs(end.y - start.y)

    # Uncomment for part 1
    # if delta_x != 0 and delta_y != 0:
    #   return []

    n_steps = max(delta_x + 1, delta_y + 1)

    x_path = numpy.round(numpy.linspace(start.x, end.x, n_steps)).astype(numpy.int32)
    y_path = numpy.round(numpy.linspace(start.y, end.y, n_steps)).astype(numpy.int32)

    return [Coordinates(*coord) for coord in zip(x_path, y_path)]


def run() -> None:
    total_overlaps = 0
    path_map = PathMap()

    parser = argparse.ArgumentParser(description='Process some measurements.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()
    segments = parse_file(args.file_name)
    for segment in segments:
        for point in get_segment_path(segment):
            if path_map.hit(point) == 2:
                total_overlaps += 1
        # print(segment)
        # print(path_map)
    print(f'{total_overlaps = }')


if __name__ == '__main__':
    run()
