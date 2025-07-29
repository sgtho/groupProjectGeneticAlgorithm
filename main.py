# Import functions and modules required from other files
from grid_utils import prompt_user_letters, random_initial_grid, is_grid_solvable, contains_word_on_edges
from fitness import build_gene_space
from ga_solver import run_ga_solver
import numpy as np  # NumPy is used here to manipulate 2D grid arrays

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
    print("Sudoku-like 4x4 puzzle with Genetic Algorithm\n")

    # Step 1: Prompt the user to input 4 distinct letters (e.g., W, O, R, D)
    letters = prompt_user_letters()

    # Step 2: Create mappings from letters to integers and vice versa.
    # This is necessary because the GA works with numerical values, not characters.
    letter_to_int = {l: i for i, l in enumerate(letters)}
    int_to_letter = {i: l for l, i in letter_to_int.items()}

    # Loop until a valid (solvable) initial grid is generated and accepted
    while True:
        # Step 3: Randomly generate a partially-filled 4x4 grid with the given letters
        initial_grid = random_initial_grid(letters)

        # Step 4: Convert the letter grid to an integer grid for algorithm processing
        int_grid = np.full((4, 4), -1)  # Initialize 4x4 grid with -1 (empty)
        for r in range(4):
            for c in range(4):
                if initial_grid[r, c] != '-':  # '-' indicates an empty cell
                    int_grid[r, c] = letter_to_int[initial_grid[r, c]]

        # Step 5: Define allowed values (0 to 3) based on 4 letters
        allowed_vals = set(letter_to_int.values())

        # Define the target word (e.g., "WORD") to check if it appears on the edge
        target_word = ''.join(letters)

        # Step 6: Check if the puzzle is solvable using custom logic
        solvable = is_grid_solvable(int_grid.copy(), allowed_vals)

        print("\nInitial grid setting:")
        print(initial_grid)
        print("Is this grid possible to solve? :", solvable)

        # Step 7: Ask user to confirm this grid before proceeding
        conf = input(
            "Press 'y' to confirm and start solving (I will check again the grid is solvable or not before solving), or 'n' to re-generate initial grid: "
        ).strip().lower()

        if solvable and conf == 'y':
            break  # Exit loop if user confirms and grid is solvable
        elif not solvable:
            print("This grid is not solvable, regenerating automatically...\n")

    print("\nInitial grid for solving:")
    print(initial_grid)

    # Step 8: Prepare the gene space (possible values for each cell) based on initial grid
    gene_space = build_gene_space(initial_grid, letter_to_int)

    print("\nSolving the puzzle now...")

    # Step 9: Run the genetic algorithm to find all valid solutions
    all_solutions, fitnesses, validations = run_ga_solver(gene_space, letter_to_int, int_to_letter)

    # Step 10: If there are valid solutions
    if all_solutions:
        print("\n🎯 All valid solutions found:\n")
        matching_solutions = []  # Store solutions where target_word is found on the grid's edge
        non_matching_solutions = []  # Store solutions without the edge word

        # Step 11: Classify each solution based on whether it matches the target word on the edge
        for idx, (decoded, fit, valid) in enumerate(zip(all_solutions, fitnesses, validations), 1):
            if contains_word_on_edges(decoded, target_word):
                matching_solutions.append((idx, decoded, fit, valid))
            else:
                non_matching_solutions.append((idx, decoded, fit, valid))

        # Step 12: Display solutions where the target word appears along the edge
        print(f"\n✅ Solutions with '{target_word}' along an edge:\n")
        if matching_solutions:
            for idx, grid, fit, valid in matching_solutions:
                print(f"--- Solution {idx} ---")
                for row in grid:
                    print(' '.join(row))  # Print row as space-separated letters
                print(f"Fitness: {fit}")
                print(f"Valid: {valid} 🌟 MATCH\n")
        else:
            print("None found.\n")

        # Step 13: Display other valid solutions that do not contain the edge word
        print(f"\n📦 Other valid solutions without edge match:\n")
        if non_matching_solutions:
            for idx, grid, fit, valid in non_matching_solutions:
                print(f"--- Solution {idx} ---")
                for row in grid:
                    print(' '.join(row))
                print(f"Fitness: {fit}")
                print(f"Valid: {valid}\n")
        else:
            print("All valid solutions contain the word on an edge.\n")

        # Step 14: Print summary statistics
        print(f"Summary:")
        print(f"- Total valid solutions: {len(all_solutions)}")
        print(f"- With edge word '{target_word}': {len(matching_solutions)}")
        print(f"- Without edge word: {len(non_matching_solutions)}")

    else:
        # Step 15: No solution was found
        print("\n❌ No solution was found.")
        print("Possible reasons:")
        print("1. The genetic algorithm may not have found a solution within the allowed generations.")
        print("2. The search space is large or too constrained.")
        print("3. Rare but possible: a bug or parameter issue.")
        print("Try regenerating the grid or adjusting GA settings.")

# Python entry point — this ensures main() is only run when executing this file directly
if __name__ == '__main__':
    main()
