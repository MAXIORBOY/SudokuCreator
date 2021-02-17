from .forms import NewForm, NewFormSet
from .sudoku_solver import SudokuSolver
from .sudoku_creator import SudokuCreator
import numpy as np

def generate_new_sudoku_grid(difficulty):
    return [[int(element) for element in list(row)] for row in SudokuCreator(difficulty).generate_new_sudoku_grid()]


def merge_generated_and_users_data_into_one_matrix(request, generated_sudoku_grid):
    sudoku_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            if generated_sudoku_grid[i][j]:
                row.append(generated_sudoku_grid[i][j])
            else:
                user_input = request.POST.get(f'form-{9 * i + j}-field', None)
                if user_input is None:
                    row.append(0)
                elif user_input == '':
                    row.append(0)
                else:
                    row.append(int(user_input))

        sudoku_grid.append(row)

    return sudoku_grid


def sudoku_grid_solved_correctly_test(grid):
    sudoku_grid = np.array(grid)
    for i in range(len(sudoku_grid)):
        if len(np.unique(sudoku_grid[i])) != 9 or 0 in sudoku_grid[i]:
            return False

    i = 0
    for j in range(len(sudoku_grid[i])):
        if len(np.unique(sudoku_grid[:, j])) != 9 or 0 in sudoku_grid[:, j]:
            return False

        i += 1

    for i in range(3):
        for j in range(3):
            array = []
            for row in sudoku_grid[3 * i: 3 * (i + 1), 3 * j: 3 * (j + 1)]:
                array.extend(row)
            if len(np.unique(array)) != 9 or 0 in array:
                return False

    return True

def solve_sudoku_grid(generated_grid):
    return [[int(element) for element in list(row)] for row in SudokuSolver(np.array(generated_grid)).solve_grid()]
