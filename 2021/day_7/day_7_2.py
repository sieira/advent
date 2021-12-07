import argparse


def parse_file(file_name: str) -> list[int]:
    with open(file_name, encoding='utf-8') as input_file:
        return [int(point) for point in input_file.readline().strip().split(',')]


def calc(points: list[int], dest):
    return sum(((1 + abs(point - dest)) * abs(point - dest)) // 2 for point in points)


def run() -> None:
    min_fuel = float('inf')

    points = parse_file(args.file_name)
    for dest in range(max(points)):
        req_fuel = calc(points, dest)
        min_fuel = min(min_fuel, req_fuel)

    print(f'Final: {min_fuel = }')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crab min fuel.')
    parser.add_argument('file_name', type=str, help='Input file name')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='Debug')
    args = parser.parse_args()
    run()
