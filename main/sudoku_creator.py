import numpy as np
import random
from .sudoku_solver import SudokuSolver


class SudokuCreator:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.number_of_fields_to_remove = self.get_number_of_fields_to_remove()
        self.force_assumptions, self.max_assumptions = self.get_range_of_assumptions()

    def get_number_of_fields_to_remove(self):
        fields_probabilities_dictionary = {}

        if self.difficulty == 'easy':
            fields_probabilities_dictionary = {25: 1, 26: 2, 27: 3, 28: 3, 29: 4, 30: 8, 31: 1, 32: 4, 33: 1, 34: 0, 35: 0, 36: 4}

        elif self.difficulty == 'medium':
            fields_probabilities_dictionary = {25: 1, 26: 9, 27: 4, 28: 14, 29: 1, 30: 0, 31: 0, 32: 2, 33: 0, 34: 1, 35: 1}

        elif self.difficulty == 'hard':
            fields_probabilities_dictionary = {22: 1, 24: 8, 25: 1, 26: 13, 27: 1, 28: 7, 29: 0, 30: 1, 31: 1}

        return 81 - random.choices(list(fields_probabilities_dictionary.keys()), k=1, weights=[fields_probabilities_dictionary[key] for key in list(fields_probabilities_dictionary.keys())])[0]

    def get_range_of_assumptions(self):
        assumption_range_dictionary = {'easy': (0, 1), 'medium': (1, 3), 'hard': (1, 4)}

        return assumption_range_dictionary[self.difficulty]

    def generate_new_sudoku_grid(self):
        failed_flag = False
        empty_grid = np.array([[0 for _ in range(9)] for _ in range(9)])
        solved_sudoku_grid = SudokuSolver(empty_grid).solve_grid()
        number_of_assumptions = 0
        force_assumptions = self.force_assumptions

        sudoku_grid = np.array([[solved_sudoku_grid[i][j] for j in range(9)] for i in range(9)])
        for k in range(self.number_of_fields_to_remove):
            indexes_of_filled_cells = [(i, j) for i in range(9) for j in range(9) if sudoku_grid[i][j] != 0]
            loop_status = True

            while loop_status:
                index_to_remove = random.choice(indexes_of_filled_cells)
                backup_digit = sudoku_grid[index_to_remove[0]][index_to_remove[1]]
                sudoku_grid[index_to_remove[0]][index_to_remove[1]] = 0

                sudoku_solver_obj = SudokuSolver(np.array([[sudoku_grid[i][j] for j in range(9)] for i in range(9)]))
                sudoku_solver_obj.solve_grid()
                if sudoku_solver_obj.number_of_assumptions != number_of_assumptions:  
                    if len(indexes_of_filled_cells) > 1 and force_assumptions * random.random() < 2 / np.log((k + 2)):
                        sudoku_grid[index_to_remove[0]][index_to_remove[1]] = backup_digit
                        indexes_of_filled_cells.remove(index_to_remove)
                        loop_status = True
                    else:
                        loop_status = False
                        number_of_assumptions += 1

                        if len(indexes_of_filled_cells) > 1:
                            force_assumptions -= 1
                else:
                    loop_status = False

            if not(number_of_assumptions <= self.max_assumptions + 1):
                failed_flag = True
                break

        if not failed_flag:
            return sudoku_grid

        else:
            self.generate_new_sudoku_grid()

        return sudoku_grid
