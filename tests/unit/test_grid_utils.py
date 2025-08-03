import unittest
from unittest.mock import patch
import numpy as np
from grid_utils import (
    prompt_user_letters,
    check_no_conflict,
    random_initial_grid,
    is_grid_solvable
)


class TestGridUtils(unittest.TestCase):

    def test_check_no_conflict_true(self):
        grid = np.full((4, 4), '-', dtype='<U1')
        grid[0, 1] = 'A'
        self.assertTrue(check_no_conflict(grid, 1, 1, 'B'))

    def test_check_no_conflict_false_row(self):
        grid = np.full((4, 4), '-', dtype='<U1')
        grid[2, 1] = 'C'
        self.assertFalse(check_no_conflict(grid, 2, 3, 'C'))

    def test_check_no_conflict_false_col(self):
        grid = np.full((4, 4), '-', dtype='<U1')
        grid[0, 2] = 'D'
        self.assertFalse(check_no_conflict(grid, 3, 2, 'D'))

    def test_check_no_conflict_false_block(self):
        grid = np.full((4, 4), '-', dtype='<U1')
        grid[0, 0] = 'A'
        self.assertFalse(check_no_conflict(grid, 1, 1, 'A'))

    @patch('builtins.input', side_effect=['AB12', 'AAAB', 'ABCD'])
    def test_prompt_user_letters_valid_after_invalid(self, mock_input):
        result = prompt_user_letters()
        self.assertEqual(result, ['A', 'B', 'C', 'D'])

    def test_random_initial_grid_structure_and_validity(self):
        letters = ['A', 'B', 'C', 'D']
        grid = random_initial_grid(letters)

        # Should contain exactly 3 letters, rest '-'
        num_letters = np.count_nonzero(grid != '-')
        self.assertEqual(num_letters, 3)

        # Check no violations (should be placed using check_no_conflict)
        for r in range(4):
            for c in range(4):
                if grid[r, c] != '-':
                    letter = grid[r, c]
                    temp = grid.copy()
                    temp[r, c] = '-'  # Temporarily remove
                    self.assertTrue(check_no_conflict(temp, r, c, letter))

    def test_is_grid_solvable_true(self):
        # This grid is incomplete but solvable
        grid = np.array([
            [0, 1, -1, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1]
        ])
        allowed_vals = [0, 1, 2, 3]
        self.assertTrue(is_grid_solvable(grid.copy(), allowed_vals))

    def test_is_grid_solvable_false_due_to_conflict(self):
        # Two 0s in first row → unsolvable
        grid = np.array([
            [0, 0, -1, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1]
        ])
        allowed_vals = [0, 1, 2, 3]
        self.assertFalse(is_grid_solvable(grid.copy(), allowed_vals))


if __name__ == '__main__':
    unittest.main()
