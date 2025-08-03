# 4×4 Sudoku‑Style Puzzle Solver Using Genetic Algorithms

This repository contains a Python application that solves a 4×4 grid puzzle (Sudoku‑style) using a Genetic Algorithm (GA) implemented with PyGAD.

## 📖 Overview

The application generates a random 4×4 puzzle with three clues and allows the user to choose any four distinct letters for the puzzle. The GA evolves candidate grids so that each row, column, and 2×2 sub‑grid contains each letter exactly once. All fixed cells are respected, and only valid, solvable puzzles are offered for solving.

## ✅ Features

* Accept any user‑specified set of four distinct letters.
* Honor fixed cells from the system-generated puzzle.
* Enforce uniqueness constraints for rows, columns, and 2×2 sub‑grids.
* Pre-check that every puzzle is solvable before GA begins.
* Find all unique valid solutions for a puzzle, not just one.
* Print detailed progress and show all solutions found.
* Provide clear, user-friendly diagnostics if no solution is found.
* Modular, PEP8‑compliant code with comprehensive docstrings and inline comments.
* Clean, maintainable file structure for easy extension.

## 🗂 Project Structure

```bash
genetic_sudoku/
│
├── main.py           # Entry point; user interaction, puzzle setup, result display
├── grid_utils.py     # Grid generation, input, Sudoku logic, and solvability check
├── fitness.py        # Fitness calculation, gene space building, and validation
├── ga_solver.py      # Genetic Algorithm setup, solution tracking, progress
└── README.md
```

## ⚙️ Requirements

* Python 3.7+
* NumPy
* Pandas
* PyGAD 2.20.0 or later

Install dependencies via:

```bash
pip install numpy pandas pygad
```

## 🛠 Installation

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd groupProjectGeneticAlgorithm
   ```
2. Install dependencies as shown above.

## 🚀 Usage

1. Run the solver:

   ```bash
   python main.py
   ```
2. When prompted, enter 4 distinct letters without separators.
3. Review the automatically generated grid (with three random clues). Confirm or regenerate as you wish.
4. The program will print:
* Progress bar (%)
* All found solutions in readable grid form
* Fitness (max = 48)
* Validity check (True/False)
* If no solution is found, detailed diagnostics and suggestions.

### Example

```bash
Enter 4 distinct letters (no separators): WORX

Initial grid setting:
[['-' '-' '-' 'O']
 ['-' 'X' '-' '-']
 ['O' '-' '-' '-']
 ['-' '-' 'W' '-']]
is_grid_solvable returned: True
Press 'y' to confirm and start solving, or 'n' to re-generate initial grid: y

Solving the puzzle now:
0%...1%...2%...
I found one solution!
...
I found all solutions

--- Solution 1 ---
[['W' 'O' 'R' 'X']
 ['R' 'X' 'W' 'O']
 ['O' 'R' 'X' 'W']
 ['X' 'W' 'O' 'R']]
Fitness: 48
Valid: True

Total unique solutions found: 2
```

### Running tests

Tests are slpit into two parts: Unit tests and End to End tests. End-to-end tests take longer to run but test the algorithm with multiple cases and run the full GA process. Unit tests are much faster and test individual components.

To run the unit tests, run:
```bash
python -m unittest discover -s tests/unit
```

To run the end-to-end tests, run:
```bash
python -m unittest discover -s tests/e2e
```

## 🔧 Configuration

* **Hyperparameters** can be tuned in `ga_solver.py`:
  * `sol_per_pop` (population size)
  * `num_generations`
  * `mutation_percent_genes`
  * `parent_selection_type`, `crossover_type`, etc.
* You can also adjust how clues are generated or how many generations to use for advanced users.

## ⚙️ Implementation Details

* Data structures: The grid is represented as a flat list of 16 integers (0–3) mapped to the four user-selected letters.
* Fitness: Penalises duplicate letters in rows, columns, and blocks. Perfect score = 48.
* All-solutions search: The GA runs for all generations, collecting every unique valid solution found.
* Diagnostics: If no solution is found, the program prints detailed possible causes and next steps.
* PEP8 compliance: All code is modular, with docstrings, inline comments, and clear structure.
