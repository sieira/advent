import argparse


Measurement = str
Bitcount = list[int]


def parse_file(file_name: str) -> list[Measurement]:
    with open(file_name) as input_file:
        return input_file.read().splitlines()


def get_bit_count(measurements: list[Measurement], position: int) -> Bitcount:
    bitcount = [0, 0]
    for measurement in measurements:
        bitcount[int(measurement[position])] += 1
    return bitcount


def get_rating(measurements: list[Measurement], lesser: bool = False) -> int:
    remaining_measurements = measurements[:]
    position = 0

    while len(remaining_measurements) > 1:
        bitcount = get_bit_count(remaining_measurements, position)
        if lesser:
            lookfor = '0' if bitcount[0] > bitcount[1] else '1'
        else:
            lookfor = '1' if bitcount[0] > bitcount[1] else '0'

        remaining_measurements = [
            measurement for measurement in remaining_measurements
            if measurement[position] == lookfor
        ]
        print(f'{len(remaining_measurements)} remaining')
        position += 1

    assert len(remaining_measurements) == 1
    print(remaining_measurements[0])
    return int(remaining_measurements[0], 2)


def get_oxygen_rating(measurements: list[Measurement]) -> int:
    print('Oxygen')
    return get_rating(measurements)


def get_co2_rating(measurements: list[Measurement]) -> int:
    print('CO2')
    return get_rating(measurements, lesser=True)


def get_rates(measurements: list[str]) -> tuple[int, int]:
    oxygen_rating = get_oxygen_rating(measurements)
    co2_rating = get_co2_rating(measurements)
    return oxygen_rating, co2_rating


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some measurements.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    raw_measurements = parse_file(args.file_name)
    o2, co2 = get_rates(raw_measurements)
    print(o2 * co2)
