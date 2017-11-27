#!/usr/bin/env python3

"""Solve the 8 queens puzzle using backtracking."""

BOARD_SIZE = 4

def is_attacked(row, column, queens):
    """Checks whether a field is attacked by a list of queens."""
    for q in queens:
        if row == q[0]:
            return True
        if column == q[1]:
            return True
        if row + column == q[0] + q[1]:
            return True
        if row - column == q[0] - q[1]:
            return True
    return False

def try_row(row, queens):
    """Try to place the queens using backtracking"""
    for column in range(BOARD_SIZE):
        attacked = is_attacked(row, column, queens)

        if not attacked:
            # place queen
            tmp_queens = set(queens)
            tmp_queens.add((row, column))

            if row == BOARD_SIZE - 1:
                # we are on the last row
                return tmp_queens
            else:
                # try to solve next row
                result = trying(row + 1, tmp_queens)
                if not result:
                    # we couldn't find a match
                    continue
                else:
                    # we successfully could place the last queen - break recursion
                    return result
    return False


if __name__ == '__main__':
    queens = try_row(0, set())
    print(queens)
