import argparse
from statistics import median


def parse_file(file_name: str) -> list[int]:
    with open(file_name, encoding='utf-8') as input_file:
        return [int(point) for point in input_file.readline().strip().split(',')]


def run() -> None:
    points = parse_file(args.file_name)
    median_point = round(median(points))
    min_fuel = sum(abs(median_point - point) for point in points)
    print(f'Final: {min_fuel = }')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crab min fuel.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()
    run()
