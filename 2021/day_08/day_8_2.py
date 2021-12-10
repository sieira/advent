import argparse
from typing import Union, Generator

SignalPattern = str
DisplaySignalPatterns = list[SignalPattern]
OutputDigit = str
DisplayInfo = tuple[DisplaySignalPatterns, list[OutputDigit]]

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

SEGMENTS = set('abcdefg')

NUMBER_SEGMENTS = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}


class SignalMapper:
    def __init__(self):
        self.possible_mapping = {
            'a': set('abcdefg'),
            'b': set('abcdefg'),
            'c': set('abcdefg'),
            'd': set('abcdefg'),
            'e': set('abcdefg'),
            'f': set('abcdefg'),
            'g': set('abcdefg'),
        }

    def map_segments_to(self, segments: set[str], pattern: SignalPattern):
        """Makes it so the given segments can only be one of the signals in the given pattern"""
        for segment in segments:
            # Do not add what has been discarded
            remaining = self.possible_mapping[segment].intersection(set(pattern))
            self.possible_mapping[segment] = remaining
            # If there is only one option left, discard it everywhere else
            if len(remaining) == 1:
                self.unmap_segments_to(SEGMENTS.difference(segment), remaining)

    def unmap_segments_to(self, segments: set[str], pattern: SignalPattern):
        """Makes it so the given segments cannot be any of the signals in the given pattern"""
        for segment in segments:
            self.possible_mapping[segment] = self.possible_mapping[segment].difference(pattern)

    def get_possible_pattern(self, num: int) -> SignalPattern:
        """Return all the segments that with the current information COULD be part of the number"""
        mapped_segments = set()
        for real_segment in NUMBER_SEGMENTS[num]:
            mapped_segments.update(self.possible_mapping[real_segment])
        return ''.join(mapped_segments)

    def get_segments(self, pattern: SignalPattern) -> SignalPattern:
        signal = ''
        for real_segment, mapped in self.possible_mapping.items():
            if any(pattern_segment in mapped for pattern_segment in pattern):
                signal += real_segment
        return signal

    def get_num_from_pattern(self, pattern: SignalPattern) -> Union[int, None]:
        segments = self.get_segments(pattern)
        for num, real_segments in NUMBER_SEGMENTS.items():
            if real_segments == segments:
                return num
        return None


def guess_uniq_from_segment_numb(num, display_signal_patterns, signal_mapper):
    """Guess the possible mapping for numbers that have a unique amount of segments"""
    n_seg = len(NUMBER_SEGMENTS[num])
    num_in_pattern = [pattern for pattern in display_signal_patterns if len(pattern) == n_seg][0]
    signal_mapper.map_segments_to(NUMBER_SEGMENTS[num], num_in_pattern)
    signal_mapper.unmap_segments_to(SEGMENTS.difference(NUMBER_SEGMENTS[num]), num_in_pattern)


def discern_2_5_3(display_signal_patterns, signal_mapper):
    # They have 5 segments
    five_segments_num = [pattern for pattern in display_signal_patterns if len(pattern) == 5]

    for pattern in five_segments_num:
        # 3 is the only one containing an entire 1 within
        if all(letter in pattern for letter in signal_mapper.get_possible_pattern(1)):
            signal_mapper.map_segments_to(NUMBER_SEGMENTS[3], pattern)
        # 5 without 4 has 2 segments
        elif len(set(pattern).difference(signal_mapper.get_possible_pattern(4))) == 2:
            signal_mapper.map_segments_to(NUMBER_SEGMENTS[5], pattern)
        else:
            signal_mapper.map_segments_to(NUMBER_SEGMENTS[2], pattern)


def discern_0_6_9(display_signal_patterns, signal_mapper):
    # They have 6 segments
    six_segments_num = [pattern for pattern in display_signal_patterns if len(pattern) == 6]

    for pattern in six_segments_num:
        # 9 wihout the 4 has only two segments
        if len(set(pattern).difference(signal_mapper.get_possible_pattern(4))) == 2:
            signal_mapper.map_segments_to(NUMBER_SEGMENTS[9], pattern)
        # 6 without the one has 5 segments
        elif len(set(pattern).difference(signal_mapper.get_possible_pattern(1))) == 5:
            signal_mapper.map_segments_to(NUMBER_SEGMENTS[6], pattern)
        else:
            signal_mapper.map_segments_to(NUMBER_SEGMENTS[0], pattern)


def guess_signals(display_signal_patterns: DisplaySignalPatterns) -> SignalMapper:
    signal_mapper = SignalMapper()

    for num in [1, 4, 7, 8]:
        guess_uniq_from_segment_numb(num, display_signal_patterns, signal_mapper)
    discern_2_5_3(display_signal_patterns, signal_mapper)
    discern_0_6_9(display_signal_patterns, signal_mapper)
    return signal_mapper


def parse_file(file_name: str) -> Generator[DisplayInfo, None, None]:
    with open(file_name, encoding='utf-8') as input_file:
        for display in input_file.read().splitlines():
            display_signal_patterns, display_output_digits = display.split(' | ')
            yield display_signal_patterns.split(), display_output_digits.split()


def run() -> None:
    parser = argparse.ArgumentParser(description='Display magic.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    display_info = parse_file(args.file_name)

    total = 0

    for display_signal_patterns, display_output_digits in display_info:
        line_mapper = guess_signals(display_signal_patterns)
        output = int(
            ''.join(
                str(line_mapper.get_num_from_pattern(digit)) for digit in display_output_digits
            )
        )
        total += output
    print(f'Final: {total = }')


if __name__ == '__main__':
    run()
