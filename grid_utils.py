import numpy as np          # Import numpy for array operations
import random               # Import random for random choices

# =====================================
# Prompt the user for 4 unique letters
# =====================================

def prompt_user_letters():
    """
    Prompt user for 4 unique alphabetic letters.
    Repeats until input is valid (4, unique, alphabetic).
    """
    while True:                                                        # Loop until valid input is given
        user_input = input("Enter 4 distinct letters (no separators): ").strip().upper()  # Ask for input, clean, uppercase
        if len(user_input) == 4 and len(set(user_input)) == 4 and all(ch.isalpha() for ch in user_input): # Check all conditions
            return list(user_input)                                    # Return as a list of letters
        print("Invalid input. Please enter exactly 4 different alphabetic characters.\n")  # Warn if not valid

# =====================================
# Check if a letter can be placed in a cell
# =====================================

def check_no_conflict(grid, row, col, letter):
    """
    Returns True if placing letter at (row,col) does not violate Sudoku constraints.
    """
    if letter in grid[row, :]:             # Check if letter is in the same row
        return False
    if letter in grid[:, col]:             # Check if letter is in the same column
        return False
    block_row, block_col = row//2*2, col//2*2         # Calculate top-left of 2x2 block
    if letter in grid[block_row:block_row+2, block_col:block_col+2]: # Check 2x2 block
        return False
    return True                            # Return True if no conflict found

# =====================================
# Randomly generate a 4x4 grid with 3 clues
# =====================================

def random_initial_grid(letters):
    """
    Fill a blank 4x4 grid with three clues, ensuring Sudoku constraints.
    """
    grid = np.full((4, 4), '-', dtype='<U1')          # Fill grid with '-'
    positions = list((r, c) for r in range(4) for c in range(4))   # All possible positions
    placed = 0                                        # Number of clues placed so far
    trials = 0                                        # Attempt counter (prevents infinite loops)
    while placed < 3:                                 # Until 3 clues are placed
        trials += 1
        if trials > 1000:                             # If too many attempts, restart
            return random_initial_grid(letters)
        letter = random.choice(letters)               # Pick a random letter
        empty = [(r, c) for (r, c) in positions if grid[r, c] == '-'] # All empty positions
        random.shuffle(empty)                         # Shuffle to randomise placement order
        for (r, c) in empty:                          # Try all empty spots
            if check_no_conflict(grid, r, c, letter): # Check if placement is legal
                grid[r, c] = letter                   # Place letter
                placed += 1                           # Increment clue count
                break                                 # Stop this letter, move to next
        else:
            return random_initial_grid(letters)       # If can't place letter, restart grid
    return grid                                       # Return filled grid

# =====================================
# Backtracking solver to check if a grid is solvable
# =====================================

def is_grid_solvable(grid, allowed_vals):
    """
    Returns True if the grid can be filled completely using allowed_vals, following Sudoku constraints.
    """

    def can_place(r, c, val):                         # Helper: can value val be placed at (r, c)?
        if val in grid[r, :]: return False            # Row check
        if val in grid[:, c]: return False            # Column check
        br, bc = (r//2)*2, (c//2)*2                   # Top-left of 2x2 block
        if val in grid[br:br+2, bc:bc+2]: return False # 2x2 block check
        return True

    def dfs(pos=0):                                   # Recursive depth-first search from cell pos
        if pos == 16: return True                     # Base case: past last cell, grid filled
        r, c = divmod(pos, 4)                         # Get row and col from pos (0-15)
        if grid[r, c] != -1: return dfs(pos+1)        # If cell filled, go to next cell
        for val in allowed_vals:                      # Try each allowed value
            if can_place(r, c, val):                  # If legal placement
                grid[r, c] = val                      # Place value
                if dfs(pos+1): return True            # Recurse; return True if successful
                grid[r, c] = -1                       # Backtrack if dead end
        return False                                  # No valid value found: backtrack
    return dfs()                                      # Start recursion from position 0
