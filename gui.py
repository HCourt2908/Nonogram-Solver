import tkinter as tk
from solver import *

board_size = 6

board = [
    [UNKNOWN for _ in range(6)]
    for _ in range(6)
]


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

def update_display():
    for r in range(board_size):
        for c in range(board_size):
            if board[r][c] == FILLED:
                buttons[r][c].config(bg="black", text = "")
            elif board[r][c] == EMPTY:
                buttons[r][c].config(bg="white", text = " ")
            else:
                buttons[r][c].config(bg="lightgray", text = "?")

def solve_pressed():
    global board
    board = solve_nonogram(board, row_clues, column_clues, row_configurations, column_configurations)

    update_display()

window = tk.Tk()
window.title("Nonogram Solver")

buttons = []

for r in range(board_size):
    row = []

    for c in range(board_size):
        button = tk.Button(
            window,
            width = 4,
            height = 2,
            text = "?"
        )

        button.grid(row = r, column = c)

        row.append(button)

    buttons.append(row)

solve_button = tk.Button(
    window,
    text="Solve",
    command=solve_pressed
)

solve_button.grid(
    row=board_size + 1,
    column=0,
)

window.mainloop()