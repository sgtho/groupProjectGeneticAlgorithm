import unittest
import numpy as np
from ga_solver import run_ga_solver
from fitness import build_gene_space, is_valid_solution

class TestEndToEndSolver(unittest.TestCase):

    def setUp(self):
        # Use a simple and consistent set of letters
        self.letters = ['A', 'B', 'C', 'D']
        self.letter_to_int = {l: i for i, l in enumerate(self.letters)}
        self.int_to_letter = {i: l for l, i in self.letter_to_int.items()}

    def _run_and_validate(self, initial_grid):
        # Build gene space from grid
        gene_space = build_gene_space(initial_grid, self.letter_to_int)

        # Run solver
        decoded_solutions, fitnesses, validations = run_ga_solver(
            gene_space, self.letter_to_int, self.int_to_letter
        )

        # Assertions
        self.assertGreater(len(decoded_solutions), 0, "No solutions found.")
        for decoded, fit, valid in zip(decoded_solutions, fitnesses, validations):
            self.assertEqual(fit, 48)
            self.assertTrue(valid)
            # All letters in decoded grid must be from self.letters
            flat = decoded.flatten()
            for ch in flat:
                self.assertIn(ch, self.letters)

    def test_case_1_simple_partial_grid(self):
        # One clue per row
        grid = np.array([
            ['A', '-', '-', '-'],
            ['-', 'B', '-', '-'],
            ['-', '-', 'C', '-'],
            ['-', '-', '-', 'D']
        ])
        self._run_and_validate(grid)

    def test_case_2_corner_clues(self):
        grid = np.array([
            ['A', '-', '-', 'B'],
            ['-', '-', '-', '-'],
            ['-', '-', '-', '-'],
            ['C', '-', '-', 'D']
        ])
        self._run_and_validate(grid)

    def test_case_3_diagonal_clues(self):
        grid = np.array([
            ['A', '-', '-', '-'],
            ['-', 'B', '-', '-'],
            ['-', '-', 'C', '-'],
            ['-', '-', '-', 'D']
        ])
        self._run_and_validate(grid)

    def test_case_4_almost_empty(self):
        grid = np.array([
            ['-', '-', '-', '-'],
            ['-', '-', '-', '-'],
            ['-', 'C', '-', '-'],
            ['-', '-', '-', '-']
        ])
        self._run_and_validate(grid)

    def test_case_5_maximum_clues(self):
        # Already valid solution with 12 clues
        grid = np.array([
            ['A', 'B', 'C', 'D'],
            ['C', 'D', 'A', 'B'],
            ['B', '-', '-', 'C'],
            ['D', 'C', 'B', 'A']
        ])
        self._run_and_validate(grid)

if __name__ == '__main__':
    unittest.main()
