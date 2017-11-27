BOARD_SIZE = 4

def is_attacked(row, column, queens):
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
    for c in range(BOARD_SIZE):
        attacked = is_attacked(row, c, queens)
        if not attacked:
            break
    if attacked and c == BOARD_SIZE:
        return False
    queens.append((row, c))
    if not row == BOARD_SIZE:
        pass
    return True

queens = []
try_row(0, queens)

queens = [(0, 0)]
print(is_attacked(1,1,queens))
print(is_attacked(2,2,queens))
print(is_attacked(1,2,queens))
