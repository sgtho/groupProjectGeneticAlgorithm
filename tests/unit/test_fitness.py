import unittest
import numpy as np
from fitness import build_gene_space, fitness_func, is_valid_solution  # adjust import as needed

class TestFitness(unittest.TestCase):

    def setUp(self):
        # Letter mapping: A-D → 0-3
        self.letter_to_int = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        self.full_values = list(self.letter_to_int.values())

    def test_build_gene_space_all_blank(self):
        grid = np.array([['-', '-', '-', '-'],
                         ['-', '-', '-', '-'],
                         ['-', '-', '-', '-'],
                         ['-', '-', '-', '-']])
        gene_space = build_gene_space(grid, self.letter_to_int)
        expected = [self.full_values] * 16
        self.assertEqual(gene_space, expected)

    def test_build_gene_space_with_fixed_values(self):
        grid = np.array([['A', '-', '-', 'B'],
                         ['-', '-', '-', '-'],
                         ['-', 'C', '-', '-'],
                         ['-', '-', '-', '-']])
        gene_space = build_gene_space(grid, self.letter_to_int)
        self.assertEqual(gene_space[0], [0])  # 'A' → 0
        self.assertEqual(gene_space[3], [1])  # 'B' → 1
        self.assertEqual(gene_space[9], [2])  # 'C' → 2
        self.assertEqual(gene_space[1], self.full_values)  # blank cell
        self.assertEqual(len(gene_space), 16)

    def test_fitness_func_perfect_solution(self):
        solution = [
            0, 1, 2, 3,
            2, 3, 0, 1,
            1, 0, 3, 2,
            3, 2, 1, 0
        ]
        class DummyGA: pass
        score = fitness_func(DummyGA(), solution, 0)
        self.assertEqual(score, 48)

    def test_fitness_func_with_duplicates(self):
        solution = [
            0, 0, 2, 3,  # duplicate 0 in row
            2, 3, 0, 1,
            1, 0, 3, 2,
            3, 2, 1, 0
        ]
        class DummyGA: pass
        score = fitness_func(DummyGA(), solution, 0)
        self.assertLess(score, 48)

    def test_is_valid_solution_true(self):
        grid = np.array([
            [0, 1, 2, 3],
            [2, 3, 0, 1],
            [1, 0, 3, 2],
            [3, 2, 1, 0]
        ])
        self.assertTrue(is_valid_solution(grid))

    def test_is_valid_solution_false_row_dup(self):
        grid = np.array([
            [0, 1, 1, 3],  # duplicate 1
            [2, 3, 0, 1],
            [1, 0, 3, 2],
            [3, 2, 1, 0]
        ])
        self.assertFalse(is_valid_solution(grid))

    def test_is_valid_solution_false_block_dup(self):
        grid = np.array([
            [0, 1, 2, 3],
            [0, 3, 0, 1],  # duplicate 0 in top-left block
            [1, 0, 3, 2],
            [3, 2, 1, 0]
        ])
        self.assertFalse(is_valid_solution(grid))

if __name__ == '__main__':
    unittest.main()
