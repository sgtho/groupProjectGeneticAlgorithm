import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from ga_solver import run_ga_solver


class TestGASolver(unittest.TestCase):

    def setUp(self):
        self.letter_to_int = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        self.int_to_letter = {v: k for k, v in self.letter_to_int.items()}
        self.full_values = list(self.letter_to_int.values())
        self.gene_space = [self.full_values] * 16

        self.perfect_solution = [
            0, 1, 2, 3,
            2, 3, 0, 1,
            1, 0, 3, 2,
            3, 2, 1, 0
        ]

    @patch('ga_solver.pygad.GA')
    def test_run_ga_solver_finds_one_solution(self, MockGA):
        mock_ga_instance = MagicMock()
        mock_ga_instance.generations_completed = 1
        mock_ga_instance.num_generations = 10
        mock_ga_instance.population = [self.perfect_solution]

        # Attach on_generation manually by extracting it from constructor args
        def fake_run():
            on_generation = MockGA.call_args[1]['on_generation']
            on_generation(mock_ga_instance)

        mock_ga_instance.run = fake_run
        MockGA.return_value = mock_ga_instance

        decoded_solutions, fitnesses, validations = run_ga_solver(
            self.gene_space, self.letter_to_int, self.int_to_letter
        )

        self.assertEqual(len(decoded_solutions), 1)
        self.assertEqual(fitnesses, [48])
        self.assertEqual(validations, [True])

        expected_letters = np.array([
            ['A', 'B', 'C', 'D'],
            ['C', 'D', 'A', 'B'],
            ['B', 'A', 'D', 'C'],
            ['D', 'C', 'B', 'A']
        ])
        np.testing.assert_array_equal(decoded_solutions[0], expected_letters)


if __name__ == '__main__':
    unittest.main()
