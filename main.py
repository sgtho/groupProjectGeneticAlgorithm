from grid_utils import prompt_user_letters, random_initial_grid, is_grid_solvable
from fitness import build_gene_space
from ga_solver import run_ga_solver
import numpy as np                                          # Import numpy for array operations

# =====================================
#groupProjectGeneticAlgorithm/
#│
#├── main.py                                                # Entry point; handles user interaction, runs solver
#├── grid_utils.py                                          # All grid-related utilities (input, validation, random grid)
#├── ga_solver.py                                           # Genetic Algorithm setup and run logic
#└── fitness.py                                             # Fitness and validation functions
# =====================================

# =====================================
# Main program: user interface, validation, and output
# =====================================

def main():
    """
    1. Prompt for user letters.
    2. Randomly generate a legal initial grid with 3 clues.
    3. Confirm the grid is solvable.
    4. Show the grid, allow user to confirm or regenerate.
    5. Run GA, show progress, print all found solutions.
    """
    print("Sudoku-like 4x4 puzzle with Genetic Algorithm\n")
    letters = prompt_user_letters()                         # Step 1: Get user letters
    letter_to_int = {l: i for i, l in enumerate(letters)}   # Map letter to integer
    int_to_letter = {i: l for l, i in letter_to_int.items()}# Map integer to letter
    
    while True:
        initial_grid = random_initial_grid(letters)         # Step 2: Generate initial grid
        int_grid = np.full((4, 4), -1)                      # Create grid of -1s for solver
        for r in range(4):
            for c in range(4):
                if initial_grid[r, c] != '-':               # If not blank
                    int_grid[r, c] = letter_to_int[initial_grid[r, c]] # Map to int
        allowed_vals = set(letter_to_int.values())           # Set of all allowed values
        solvable = is_grid_solvable(int_grid.copy(), allowed_vals)  # Step 3: Check solvability
        print("\nInitial grid setting:")
        print(initial_grid)                                  # Show grid to user
        print("Is this grid possible to solve? :", solvable)        # Show if grid is solvable
        conf = input("Press 'y' to confirm and start solving (I will check again the grid is solvable or not before solving), or 'n' to re-generate initial grid: ").strip().lower()
        if solvable and conf == 'y':                         # If user accepts and grid is solvable
            break
        elif not solvable:                                   # If not solvable, auto-regenerate
            print("This grid is not solvable, regenerating automatically...\n")

    print("\nInitial grid for solving:")                     # Show confirmed grid again
    print(initial_grid)
    gene_space = build_gene_space(initial_grid, letter_to_int)   # Prepare GA gene space
    print("\nSolving the puzzle now...")
    all_solutions, fitnesses, validations = run_ga_solver(gene_space, letter_to_int, int_to_letter)
    if all_solutions:                                        # If any solutions found
        print("\nI found all solutions\n")
        for idx, (decoded, fit, valid) in enumerate(zip(all_solutions, fitnesses, validations), 1):
            print(f"--- Solution {idx} ---")                 # Show solution number
            print(decoded)                                   # Print grid with letters
            print(f"Fitness: {fit}")                         # Print fitness
            print(f"Valid: {valid}\n")                       # Print validity (should be True)
        print(f"Total unique solutions found: {len(all_solutions)}")
    else:
        print("\nNo solution was found.")
        print("Possible reasons:")
        print("1. Although the initial grid passed a basic solvability check,")
        print("   the genetic algorithm may not have found a solution within the allowed generations.")
        print("2. The genetic algorithm can miss rare solutions if the search space is large or too constrained.")
        print("3. It's possible, though unlikely, that a bug or parameter issue prevented a solution from being found.\n")
        print("Recommended actions:")
        print("- Try regenerating the initial grid and running again.")
        print("- Increase the number of generations (num_generations) or population size (sol_per_pop) in the GA settings in ga_solver,py.")
        print("- Double-check the grid setup for unusually restrictive clue placements.")

if __name__ == '__main__':                                  # Only run if executed as main script
    main()                                                  # Start the program

