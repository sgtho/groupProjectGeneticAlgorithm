import numpy as np          # Import numpy for array operations
import pygad                # Import pygad for genetic algorithm
from fitness import fitness_func, is_valid_solution

# =====================================
# Run the genetic algorithm, collect solutions
# =====================================

def run_ga_solver(gene_space, letter_to_int, int_to_letter):
    """
    Run GA and collect all unique, valid solutions found during the process.
    Show progress percentage.
    Returns (decoded_solutions, fitnesses, validations).
    """
    solutions = set()                          # Set of unique solution keys (tuples)
    decoded_solutions = []                     # List of grids (letters) for display
    fitnesses = []                             # Fitness scores for each found solution
    validations = []                           # Validation (True/False) for each solution
    progress = {'current': 0}                  # Progress percentage tracker

    def on_generation(ga_instance):
        # Show progress if percentage has increased
        percent = int(100 * ga_instance.generations_completed / ga_instance.num_generations)
        if percent > progress['current']:
            print(f"{percent}%...", end="", flush=True)
            progress['current'] = percent
        pop = ga_instance.population           # Population: each is a candidate solution
        for solution in pop:                   # For each solution in this generation
            grid = np.array(solution, dtype=int).reshape(4, 4) # Convert gene vector to 4x4 grid
            if fitness_func(None, solution, None) == 48:       # If it's a perfect solution
                key = tuple(grid.flatten())    # Use flattened tuple as unique key
                if key not in solutions:       # Only collect if new
                    print("\nI find one solution!")
                    solutions.add(key)         # Add to set of solutions
                    decoded = np.vectorize(int_to_letter.get)(grid) # Decode grid to letters
                    decoded_solutions.append(decoded)          # Save decoded solution
                    fitnesses.append(48)                       # Save fitness (always 48 here)
                    validations.append(is_valid_solution(grid))# Save validation result

    # Configure and run the genetic algorithm
    ga = pygad.GA(
        num_generations=5000,          # Total number of generations to run
        sol_per_pop=500,               # Population size
        num_parents_mating=40,         # Number of parents for next generation
        num_genes=16,                  # Each solution represents a 4x4 grid (16 cells)
        gene_space=gene_space,         # List of allowed values for each gene
        fitness_func=fitness_func,     # Fitness function defined above
        parent_selection_type='tournament', # Parent selection method
        K_tournament=3,               # Tournament size
        keep_parents=5,               # How many parents to keep into next gen
        crossover_type='two_points',   # Crossover method
        mutation_type='random',        # Mutation method
        mutation_percent_genes=30,     # Percentage of genes to mutate
        on_generation=on_generation,   # Callback at the end of every generation
    )
    print("0%...", end="", flush=True)
    ga.run()                              # Start the genetic algorithm
    print()                               # Newline after progress
    return decoded_solutions, fitnesses, validations # Return results