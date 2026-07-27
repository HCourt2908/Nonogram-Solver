# Nonogram-Solver
This application is able to solve any nonogram (also known as a japanese crossword).

# Features:

- Uses deduction on the current board state to decide which row/column configurations are possible
- Looks for common filled or empty squares in the row/column and updates the game board for this
- When advanced puzzles can't be solved by just deduction, the program will guess a square is filled and either continue to solve the puzzle or backtrack on finding a contradiction
