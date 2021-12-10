import argparse


def parse_file(file_name: str) -> list[int]:
    lanternfish_timer = [0] * 9
    with open(file_name, encoding='utf-8') as input_file:
        for timer in input_file.readline().strip().split(','):
            lanternfish_timer[int(timer)] += 1
    return lanternfish_timer


def breed(lanternfish_timer: list[int]) -> list[int]:
    breeding_lanternfishes = lanternfish_timer[0]
    lanternfish_timer = lanternfish_timer[1:]
    lanternfish_timer[6] += breeding_lanternfishes
    lanternfish_timer.append(breeding_lanternfishes)
    return lanternfish_timer


def run() -> None:
    parser = argparse.ArgumentParser(description='Count fishes.')
    parser.add_argument('file_name', type=str, help='Input file name')
    parser.add_argument('cycles', type=int, help='Number of cycles')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='Debug')
    args = parser.parse_args()

    lanternfish_timer = parse_file(args.file_name)

    for cycle in range(args.cycles):
        if args.debug:
            print(f'{cycle = }: {lanternfish_timer = }')
        lanternfish_timer = breed(lanternfish_timer)

    print(f'Final: {lanternfish_timer = }')
    print(f'{sum(lanternfish_timer) = }')


if __name__ == '__main__':
    run()
