import argparse

SignalPattern = str
DisplaySignalPatterns = list[SignalPattern]
OutputDigit = str
DisplayInfo = tuple[DisplaySignalPatterns, list[OutputDigit]]


def parse_file(file_name: str) -> list[DisplayInfo]:
    display_info = []

    with open(file_name, encoding='utf-8') as input_file:
        for display in input_file.read().splitlines():
            display_signal_patterns, display_output_digits = display.split(' | ')
            display_info.append((display_signal_patterns.split(), display_output_digits.split()))
    return display_info


def run() -> None:
    parser = argparse.ArgumentParser(description='Display magic.')
    parser.add_argument('file_name', type=str, help='Input file name')
    # parser.add_argument('--debug', dest='debug', default=False, action='store_true', help='Debug')
    args = parser.parse_args()

    display_info = parse_file(args.file_name)

    n_segments = {'1': 2, '4': 4, '7': 3, '8': 7}
    total = 0

    for _, display_output_digits in display_info:
        total += len([
            output_digit for output_digit in display_output_digits
            if len(output_digit) in n_segments.values()
        ])
    print(f'Final: {total = }')


if __name__ == '__main__':
    run()
