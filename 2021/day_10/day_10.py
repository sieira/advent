import argparse


OPENING = '([{<'
CLOSING = ')]}>'

ILLEGAL_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTOCOMPLETE_SCORE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}


def parse_file(file_name: str) -> list[str]:
    with open(file_name, encoding='utf-8') as input_file:
        return input_file.read().splitlines()


def run() -> None:
    parser = argparse.ArgumentParser(description='Syntax checker.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    score = 0
    autocomplete_scores = []

    for line in parse_file(args.file_name):
        stack = []
        for char in line:
            if char in OPENING:
                stack.append(char)
            elif char in CLOSING:
                last_opened = stack.pop()
                if OPENING.index(last_opened) != CLOSING.index(char):
                    score += ILLEGAL_SCORE[char]
                    break
            else:
                # Unknown char
                continue
        else:
            # Incomplete line
            if stack:
                line_autocomplete_score = 0
                for char in stack[::-1]:
                    line_autocomplete_score *= 5
                    line_autocomplete_score += AUTOCOMPLETE_SCORE[char]
                autocomplete_scores.append(line_autocomplete_score)

    middle_autocomplete_score = sorted(autocomplete_scores)[len(autocomplete_scores) // 2]
    print(f'{score = }')
    print(f'{middle_autocomplete_score = }')


if __name__ == '__main__':
    run()
