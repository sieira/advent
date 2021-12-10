import argparse
import numpy

Row = list[int]
Sequence = list[int]


class Board:
    @property
    def is_win(self):
        return (
            any(all(mark for mark in row) for row in self.marked)
            or any(all(mark for mark in row) for row in numpy.transpose(self.marked))
        )

    @property
    def unmarked_sum(self):
        total = 0
        for row_index, row in enumerate(self.rows):
            for column_index, number in enumerate(row):
                if not self.marked[row_index][column_index]:
                    total += number
        return total

    def __init__(self, rows: list[Row]) -> None:
        self.rows = rows
        self.marked = [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]

    def mark(self, ball: int) -> None:
        for row_index, row in enumerate(self.rows):
            for column_index, number in enumerate(row):
                if number == ball:
                    self.marked[row_index][column_index] = True

    def __str__(self):
        output = ''
        for row_index, row in enumerate(self.rows):
            for column_index, number in enumerate(row):
                if self.marked[row_index][column_index]:
                    output += f'\033[1m\u001b[33m {number:>2} \033[0m'
                else:
                    output += f' {number:>2} '
            output += '\n'
        return output


def parse_file(file_name: str) -> tuple[Sequence, list[Board]]:
    with open(file_name) as input_file:
        sequence = [int(number) for number in input_file.readline().strip().split(',')]
        boards = []

        rest_of_file = [line.split() for line in input_file.read().splitlines()]
        raw_boards = [rest_of_file[i+1:i + 6] for i in range(0, len(rest_of_file), 6)]

        for board in raw_boards:
            boards.append(Board([[int(elem) for elem in row] for row in board]))

        return sequence, boards


def play(sequence: Sequence, boards: list[Board]) -> tuple[Board, int]:
    for ball in sequence:
        print(f'\n{ball = }\n=========')
        for board in list(boards):
            board.mark(ball)
            print(board)
            if board.is_win:
                if len(boards) == 1:
                     return boards[0], ball
                else:
                    boards.remove(board)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some measurements.')
    parser.add_argument('file_name', type=str, help='Input file name')
    args = parser.parse_args()

    sequence, boards = parse_file(args.file_name)
    winning_board, winning_ball = play(sequence, boards)
    unmarked_sum = winning_board.unmarked_sum
    print(f'{unmarked_sum * winning_ball = }')
    print(winning_board)
