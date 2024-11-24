import random
import os
import sys

# Game constants
SIZE = 4
EMPTY = 0
WINNING_TILE = 2048

# Direction constants
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'

# Functions for moving tiles and merging them
def initialize_board():
    """Initialize a 4x4 board with two random tiles."""
    board = [[EMPTY] * SIZE for _ in range(SIZE)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    """Add a new tile (2 or 4) to a random empty position on the board."""
    empty_positions = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == EMPTY]
    if not empty_positions:
        return
    row, col = random.choice(empty_positions)
    board[row][col] = random.choice([2, 4])

def compress_line(line):
    """Compress a line (move all non-zero values to the left)."""
    new_line = [value for value in line if value != EMPTY]
    new_line += [EMPTY] * (SIZE - len(new_line))
    return new_line

def merge_line(line):
    """Merge a line (combine tiles of the same value)."""
    for i in range(SIZE - 1):
        if line[i] == line[i + 1] and line[i] != EMPTY:
            line[i] *= 2
            line[i + 1] = EMPTY
    return line

def move_left(board):
    """Move all tiles to the left and merge where possible."""
    for r in range(SIZE):
        board[r] = compress_line(board[r])
        board[r] = merge_line(board[r])
        board[r] = compress_line(board[r])

def move_right(board):
    """Move all tiles to the right and merge where possible."""
    for r in range(SIZE):
        board[r] = board[r][::-1]
        board[r] = compress_line(board[r])
        board[r] = merge_line(board[r])
        board[r] = compress_line(board[r])
        board[r] = board[r][::-1]

def move_up(board):
    """Move all tiles up and merge where possible."""
    board = list(zip(*board))  # Transpose the board
    for r in range(SIZE):
        board[r] = list(board[r])  # Convert the tuple back to a list
        board[r] = compress_line(board[r])
        board[r] = merge_line(board[r])
        board[r] = compress_line(board[r])
    return list(zip(*board))  # Transpose back to original orientation

def move_down(board):
    """Move all tiles down and merge where possible."""
    board = list(zip(*board))  # Transpose the board
    for r in range(SIZE):
        board[r] = list(board[r])  # Convert the tuple back to a list
        board[r] = board[r][::-1]
        board[r] = compress_line(board[r])
        board[r] = merge_line(board[r])
        board[r] = compress_line(board[r])
        board[r] = board[r][::-1]
    return list(zip(*board))  # Transpose back to original orientation

def game_won(board):
    """Check if the player has won (2048 tile present)."""
    return any(WINNING_TILE in row for row in board)

def game_lost(board):
    """Check if the player has lost (no moves left)."""
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == EMPTY:
                return False
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return False
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return False
    return True

def print_board(board):
    """Print the game board to the terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')
    print("2048 Game!")
    print('-' * 21)
    for row in board:
        print('|', end=' ')
        for cell in row:
            print(f"{cell:4}", end=' ')
        print('|')
    print('-' * 21)

def main():
    """Main game loop."""
    board = initialize_board()

    while True:
        print_board(board)
        
        if game_won(board):
            print("You win!")
            break

        if game_lost(board):
            print("Game over! No more moves left.")
            break

        move = input("Use WASD to move (w=up, s=down, a=left, d=right): ").lower()

        if move == UP:
            board = move_up(board)
        elif move == DOWN:
            board = move_down(board)
        elif move == LEFT:
            move_left(board)
        elif move == RIGHT:
            move_right(board)
        else:
            print("Invalid input. Please use w, a, s, or d.")

        add_random_tile(board)

if __name__ == "__main__":
    main()
