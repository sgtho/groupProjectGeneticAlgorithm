import numpy as np              # Import numpy for array operations

# =====================================
# Build the gene space for the genetic algorithm
# =====================================

def build_gene_space(grid, letter_to_int):
    """
    Build the list of allowed values for each grid cell for the GA:
    - If a cell is fixed, only that value is allowed.
    - If a cell is blank, all letters are allowed.
    Returns a list of lists of integers.
    """
    gene_space = []
    for r in range(4):                                # Loop over rows
        for c in range(4):                            # Loop over columns
            if grid[r, c] != '-':                     # If cell is fixed
                gene_space.append([letter_to_int[grid[r, c]]])
            else:                                     # If cell is free
                gene_space.append(list(letter_to_int.values()))
    return gene_space

# =====================================
# Fitness function for the genetic algorithm
# =====================================

def fitness_func(ga_instance, solution, sol_idx):
    """
    Measures quality of a GA solution.
    - Reshapes the gene vector into a grid.
    - Penalises duplicates in rows, columns, and blocks.
    - Returns a score out of 48 (perfect is 48).
    """
    grid = np.array(solution, dtype=int).reshape(4, 4)        # Convert gene vector to 4x4 grid
    penalty = 0
    for i in range(4):                                        # For each row and column
        penalty += (4 - len(set(grid[i])))                    # Penalise duplicates in row
        penalty += (4 - len(set(grid[:, i])))                 # Penalise duplicates in column
    for r in (0, 2):                                          # For each block starting row
        for c in (0, 2):                                      # For each block starting column
            block = grid[r : r + 2, c : c + 2].ravel()        # Get 2x2 block as 1D
            penalty += (4 - len(set(block)))                  # Penalise duplicates in block
    return 48 - penalty                                       # Return fitness score

# =====================================
# Validate a grid as a final solution
# =====================================

def is_valid_solution(grid):
    """
    Check if a 4x4 grid is a legal Sudoku solution.
    Returns True if no duplicates in any row, column, or block.
    """
    for i in range(4):                                        # For each row and column
        if len(set(grid[i])) != 4 or len(set(grid[:, i])) != 4:
            return False
    for r in (0, 2):                                          # For each block starting row
        for c in (0, 2):                                      # For each block starting column
            if len(set(grid[r:r+2, c:c+2].ravel())) != 4:
                return False
    return True