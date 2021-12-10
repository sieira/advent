import argparse
from enum import Enum, auto


class Direction(Enum):
    forward = auto()
    down = auto()
    up = auto()

Coordinates = tuple[int, int]
Command = tuple[Direction, int]
Route = list[Command]


def navigate(route: Route) -> Coordinates:
    x, y = (0, 0)

    for direction, amount in route:
        if direction == Direction.forward:
            x += amount
        elif direction == Direction.down:
            y -= amount
        elif direction == Direction.up:
            y += amount

    return (x, y)


def parse_command(raw_command: str) -> Command:
    raw_direction, raw_amount = raw_command.split()
    return (Direction[raw_direction], int(raw_amount))


def parse_file(file_name: str) -> Route:
    with open(file_name) as input_file:
        return [parse_command(raw_command) for raw_command in input_file.read().splitlines()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some measurements.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    route = parse_file(args.file_name)
    x, y = navigate(route)
    print(f'{x * -y = }')
