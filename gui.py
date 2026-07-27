import tkinter as tk
from solver import *

def parse_clues(text):
    clues = []

    for line in text.split("\n"):
        if line.strip():
            clues.append(
                [int(x) for x in line.split()]
            )
    return clues

def create_puzzle():

    global board
    global row_clues
    global column_clues
    global row_configurations
    global column_configurations
    global buttons

    width = int(width_entry.get())
    height = int(height_entry.get())

    row_clues = parse_clues(row_clue_box.get("1.0", tk.END))
    column_clues = parse_clues(column_clue_box.get("1.0", tk.END))

    board = [
        [UNKNOWN for _ in range(width)]
        for _ in range(height)
    ]

    row_configurations, column_configurations = create_configurations(board, row_clues, column_clues)

    create_grid()

    width_label.destroy()
    width_entry.destroy()
    height_label.destroy()
    height_entry.destroy()
    row_clue_box.destroy()
    column_clue_box.destroy()
    create_button.destroy()
    row_label.destroy()
    column_label.destroy()

def create_grid():
    global buttons

    buttons = []

    for r in range(len(board)):
        window.rowconfigure(r, weight=1)
        row = []

        for c in range(len(board[0])):
            window.columnconfigure(c, weight=1)

            button = tk.Button(window)

            button.grid(
                row=r,
                column=c,
                sticky="nsew",
            )

            row.append(button)

        buttons.append(row)

    solve_button = tk.Button(
    window,
    text="Solve",
    command=solve_pressed
    )

    solve_button.grid(
        row=len(board) + 6,
        column=0,
    )

window = tk.Tk()
window.title("Nonogram Solver")

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

width_label = tk.Label(window, text="Width")
width_label.grid(row=0, column=0)

width_entry = tk.Entry(window)
width_entry.grid(row=0, column=1)

height_label = tk.Label(window, text="Height")
height_label.grid(row=1, column=0)

height_entry = tk.Entry(window)
height_entry.grid(row=1, column=1)

row_label = tk.Label(
    window,
    text="Row Clues"
)
row_label.grid(row=2, column=0, sticky="e")

row_clue_box = tk.Text(
    window
)
row_clue_box.grid(row=2, column = 1, sticky = "nsew")

column_label = tk.Label(
    window,
    text="Column Clues"
)
column_label.grid(row=3, column=0, sticky="e")

column_clue_box = tk.Text(
    window
)
column_clue_box.grid(row=3, column = 1, sticky = "nsew")


def update_display():
    for r in range(len(board)):
        for c in range(len(board[0])):
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


create_button = tk.Button(
    window,
    text="Create Puzzle",
    command=create_puzzle
)

create_button.grid(
    row=4,
    column=0
)

window.mainloop()