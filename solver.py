import copy

UNKNOWN = 0
FILLED = 1
EMPTY = -1


def generate_configurations(length, clue):
    minimum = sum(clue) + len(clue) - 1

    #no clue for this line
    if minimum == 0 or not clue:
        return [[EMPTY]*length]
    
    #clue takes up whole space
    elif minimum == length:
        if len(clue) == 1:
            return [[FILLED]*length]
        #fill in each element in clue with a space in between
        else:
            return_config = []
            for i in clue:
                return_config.extend([FILLED]*i)
                return_config.append(EMPTY)
            return_config.pop()
            return [return_config]
        
    # non trivial solution, must be multiple potential options.
    first_clue = clue[0]
    other_clues = clue[1:]

    latest_start_index = length - minimum

    gap = 1 if other_clues else 0

    potential_configurations = []

    for start_index in range(latest_start_index+1):
        prepend = ([EMPTY]*start_index + [FILLED]*first_clue)
        if gap:
            prepend.append(EMPTY)
        appends = generate_configurations(length - start_index - first_clue - gap, other_clues)

        for append in appends:
            new_config = prepend + append
            if (len(new_config) < length):
                new_config.extend([EMPTY]*(length - len(new_config)))
            potential_configurations.append(new_config)

    return potential_configurations

def filter_configurations(configurations, line):
    filtered_configurations = []
    for config in configurations:
        valid = True
        for i in range(len(config)):
            if line[i] != UNKNOWN and line[i] != config[i]:
                valid = False
                break
        if valid:
            filtered_configurations.append(config)
    return filtered_configurations

def deduce_line(filtered_configurations):

    if not filtered_configurations:
        return None

    length = len(filtered_configurations[0])

    result = []

    for i in range(length):
        values = []

        for config in filtered_configurations:
            values.append(config[i])

        if all(value == FILLED for value in values):
            result.append(FILLED)
        
        elif all(value == EMPTY for value in values):
            result.append(EMPTY)

        else:
            result.append(UNKNOWN)

    return result

def update_row(board, new_row, index):
    changed = False
    for i in range(len(new_row)):
        if (board[index][i] == UNKNOWN and new_row[i] != UNKNOWN):
            board[index][i] = new_row[i]
            changed = True
    return board, changed

def update_column(board, new_column, index):
    changed = False
    for i in range(len(new_column)):
        if(board[i][index] == UNKNOWN and new_column[i] != UNKNOWN):
            board[i][index] = new_column[i]
            changed = True
    return board, changed

def print_board(board):
    width = len(board[0])

    # top border
    print("┌" + "───┬" * (width - 1) + "───┐")

    for row_index, row in enumerate(board):
        line = "│"

        for cell in row:
            if cell == FILLED:
                symbol = "██"
            elif cell == EMPTY:
                symbol = "  "
            else:
                symbol = "??"

            line += " " + symbol + "│"

        print(line)

        # middle/bottom borders
        if row_index != len(board) - 1:
            print("├" + "───┼" * (width - 1) + "───┤")
    
    print("└" + "───┴" * (width - 1) + "───┘")
    
    print("\n")

    for row in board:
        print(row)
        print("\n")

def propagate(board, row_clues, column_clues, row_configurations, column_configurations):
    
    changed = False

    for i in range(len(row_clues)):
        row_configs = row_configurations[i]
        filtered_configs = filter_configurations(row_configs, board[i])

        if not filtered_configs:
            return None # contradiction

        line = deduce_line(filtered_configs)
        board, row_changed = update_row(board, line, i)
        changed = changed or row_changed
    
    for j in range(len(column_clues)):
        column_configs = column_configurations[j]

        column = []
        for k in range(len(board)):
            column.append(board[k][j])

        filtered_configs = filter_configurations(column_configs, column)

        if not filtered_configs:
            return None # contradiction
        
        line = deduce_line(filtered_configs)
        board, column_changed = update_column(board, line, j)
        changed = changed or column_changed

    return changed

def solved(board):
    for row in board:
        if UNKNOWN in row:
            return False
    return True

def find_unknown(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == UNKNOWN:
                return r, c
    return None

def solve_nonogram(board, row_clues, column_clues, row_configurations, column_configurations):

    while True:
        result = propagate(board, row_clues, column_clues, row_configurations, column_configurations)

        if result is None:
            return None # contradiction

        if not result:
            break # no more logical deductions

    if solved(board):
        return board

    r, c = find_unknown(board)
    print("guessing")

    guess_board = copy.deepcopy(board)
    guess_board[r][c] = FILLED

    result = solve_nonogram(guess_board, row_clues, column_clues, row_configurations, column_configurations)

    if result is not None:
        return result

    guess_board = copy.deepcopy(board)
    guess_board[r][c] = EMPTY

    return solve_nonogram(guess_board, row_clues, column_clues, row_configurations, column_configurations)

def create_configurations(board, row_clues, column_clues):
    row_configurations = []
    column_configurations = []

    for clue in row_clues:
        row_configurations.append(generate_configurations(len(board[0]), clue))

    for clue in column_clues:
        column_configurations.append(generate_configurations(len(board), clue))

    return row_configurations, column_configurations

def main():

    length = 6
    height = 6
    board = [[UNKNOWN for _ in range(length)] for _ in range(height)]

    row_clues = [
        [1, 1],
        [2, 1],
        [2, 1],
        [3, 2],
        [1, 2],
        [2]
    ]

    column_clues = [
        [4],
        [3],
        [3],
        [1, 1],
        [1, 2],
        [3]
    ]

    row_configurations, column_configurations = create_configurations(board, row_clues, column_clues)   
    board = solve_nonogram(board, row_clues, column_clues, row_configurations, column_configurations)
    print_board(board)
    

if __name__ == "__main__":
    main()
