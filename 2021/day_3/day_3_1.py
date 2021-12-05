import argparse


Bitcount = list[int]


def parse_file(file_name: str) -> list[str]:
    with open(file_name) as input_file:
        return input_file.read().splitlines()


def get_bit_count(measurements: list[str]) -> list[Bitcount]:
    bitcount: list[Bitcount] = []
    for measurement in measurements:
        for index, bit in enumerate(measurement):
            try:
                bitcount[index][int(bit)] += 1
            except IndexError:
                bitcount.append([0, 0])
                bitcount[index][int(bit)] += 1

    print(bitcount)
    return bitcount


def get_rates(measurements: list[str]) -> tuple[int, int]:
    gamma_rate_str = ''
    for bitcount in get_bit_count(measurements):
        gamma_rate_str += '0' if bitcount[0] > bitcount[1] else '1'
    gamma_rate = int(gamma_rate_str, 2)
    epsilon_rate = ~gamma_rate & (2 ** gamma_rate.bit_length() - 1)
    print(f'{gamma_rate = :b} {epsilon_rate = :b}')
    return gamma_rate, epsilon_rate


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some measurements.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    measurements = parse_file(args.file_name)
    gamma, epsilon = get_rates(measurements)
    print(gamma * epsilon)
