# 4×4 Sudoku‑Style Puzzle Solver Using Genetic Algorithms

This repository contains a Python application that solves a 4×4 grid puzzle (Sudoku‑style) using a Genetic Algorithm (GA) implemented with PyGAD.

## 📖 Overview

The application fills a 4×4 grid with four distinct letters so that each row, column, and 2×2 sub‑grid contains each letter exactly once. Users provide a partially completed grid and choose any four distinct letters (including the pre‑filled ones). The GA evolves candidate solutions until a valid grid is found or the maximum attempts are reached.

## ✅ Features

* Accept any user‑specified set of four distinct letters.
* Honor fixed cells from the user’s initial puzzle.
* Enforce uniqueness constraints for rows, columns, and 2×2 sub‑grids.
* Retry up to three GA runs with tuned hyperparameters if no perfect solution is found on the first attempt.
* PEP8‑compliant code with comprehensive docstrings and inline comments.

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
2. When prompted, enter **4 distinct letters** without separators, ensuring you include the existing pre‑filled ones (displayed in the prompt).
3. The program will print:

   * **Best fitness** (max = 48)
   * **Solved grid** in array form
   * **Validity** check (True/False)

### Example

```bash
Enter 4 distinct letters (no separators), and include these existing ones: ['W', 'O', 'R']: WORX

Best fitness: 48
Solved Grid:
[['W' 'O' 'R' 'X']
 ['R' 'X' 'W' 'O']
 ['O' 'R' 'X' 'W']
 ['X' 'W' 'O' 'R']]
Valid solution? True
```

## 🔧 Configuration

* **Hyperparameters** can be tuned in `main()`:

  * `sol_per_pop` (population size)
  * `num_generations`
  * `mutation_percent_genes`
  * `parent_selection_type`, `crossover_type`, etc.
* **Attempts** parameter controls how many GA restarts are allowed.

## ⚙️ Implementation Details

* **Data structures**: The grid is represented as a flat list of 16 integers (0–3) mapped from letters.
* **Fitness**: Penalizes duplicate letters in rows, columns, and blocks. Perfect score = 48.
* **Early stop**: The GA stops when a solution with fitness 48 is found.
* **PEP8 compliance**: Code is broken into functions with docstrings and clear comments.
