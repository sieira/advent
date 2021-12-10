import argparse
from typing import Generator

Measurement = int


def window_generator(measurements: list[Measurement], window_size: int) -> Generator[int, None, None]:
    for index in range(0, len(measurements) - window_size + 1):
        yield sum(measurements[index:index + window_size])


def count_n_increases(measurements: list[Measurement], window_size: int) -> int:
    previous = None
    count = 0

    window_iterator = window_generator(measurements, window_size)

    for step_value in window_iterator:
        if previous is not None and previous < step_value:
            count += 1
            delta = 'increased'
        elif previous is None:
            delta = 'N/A - no previous measurement'
        elif previous == step_value:
            delta = 'no change'
        else:
            delta = 'decreased'
        print(f'{step_value} ({delta})')
        previous = step_value
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some measurements.')
    parser.add_argument('file_name', type=str, help='Input file name')
    parser.add_argument('window_size', type=int, help='Window size')
    args = parser.parse_args()

    with open(args.file_name) as input_file:
        measurement_list = [int(line) for line in input_file.read().splitlines()]

    increase_count = count_n_increases(measurement_list, args.window_size)
    print(f'A total of {increase_count} measurements where larger than the previous')
