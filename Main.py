import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import font
import random


class SudokuSolver:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.possible_numbers_in_the_field_list = None

    @staticmethod
    def internal_square_index_position(index_table):
        for i in range(len(index_table)):
            if index_table[i] < 3:
                index_table[i] = 0
            elif index_table[i] < 6:
                index_table[i] = 3
            else:
                index_table[i] = 6

        return index_table

    def possible_numbers_in_the_field(self):
        possible_numbers_in_the_field_list = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    continue
                used_numbers = []
                used_numbers.append(self.grid[i])

                row = []
                for k in range(len(self.grid)):
                    row.append(self.grid[k][j])
                used_numbers.append(row)

                internal_square_begin_index = (self.internal_square_index_position([i, j]))
                for k in range(3):
                    used_numbers.append(self.grid[internal_square_begin_index[0] + k][internal_square_begin_index[1]:internal_square_begin_index[1] + 3])

                used_numbers = [el for row in used_numbers for el in row]
                possible_numbers_in_the_field_list.append([number for number in [1, 2, 3, 4, 5, 6, 7, 8, 9] if number not in used_numbers])

        return possible_numbers_in_the_field_list

    def locate_field_with_only_one_possibility(self):
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if len(self.possible_numbers_in_the_field_list[i]) == 1:
                return i

        return -1

    def change_number_on_the_grid(self, number, empty_field_index):
        counter = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    counter += 1
                if counter == empty_field_index + 1:
                    self.grid[i][j] = number
                    return

    def check_if_grid_is_possible_to_solve(self):
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if not len(self.possible_numbers_in_the_field_list[i]):
                return False

        return True

    def locate_the_field_with_the_lowest_amount_of_possibilities(self):
        minimum_index, minimum = 0, 10
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if len(self.possible_numbers_in_the_field_list[i]) < minimum:
                minimum = len(self.possible_numbers_in_the_field_list[i])
                minimum_index = i

        return minimum_index


    def main(self):
        loop_status = True
        array_backup, assumption_index_backup, assumption_backup = [], [], []

        while loop_status:
            self.possible_numbers_in_the_field_list = self.possible_numbers_in_the_field()
            loop_status = bool(len(self.possible_numbers_in_the_field_list))
            if loop_status:
                if self.check_if_grid_is_possible_to_solve():
                    if self.locate_field_with_only_one_possibility() >= 0:
                        min_index = self.locate_field_with_only_one_possibility()
                        self.change_number_on_the_grid(self.possible_numbers_in_the_field_list[min_index][0], min_index)
                    else:
                        array_backup.append([[el for el in row] for row in self.grid])
                        assumption_index_backup.append(self.locate_the_field_with_the_lowest_amount_of_possibilities())
                        field_possible_numbers = self.possible_numbers_in_the_field_list[self.locate_the_field_with_the_lowest_amount_of_possibilities()]
                        random.shuffle(field_possible_numbers)
                        assumption_backup.append(field_possible_numbers)
                        self.change_number_on_the_grid(assumption_backup[-1][0], assumption_index_backup[-1])
                else:
                    del assumption_backup[-1][0]
                    if len(assumption_backup[-1]):
                        self.grid = array_backup[-1]
                        self.change_number_on_the_grid(assumption_backup[-1][0], assumption_index_backup[-1])
                    else:
                        loop_status2 = True
                        while loop_status2:
                            del assumption_backup[-1]
                            del assumption_backup[-1][0]
                            del assumption_index_backup[-1]
                            del array_backup[-1]
                            loop_status2 = not (bool(len(assumption_backup[-1])))

                        self.grid = array_backup[-1]
                        self.change_number_on_the_grid(assumption_backup[-1][0], assumption_index_backup[-1])

        return self.grid

    
class SudokuCreator:
    def __init__(self, solved_grid):
        self.solved_grid = solved_grid
        self.grid = [[' ' for _ in range(len(self.solved_grid))] for _ in range(len(self.solved_grid[0]))]
        self.difficulty_parameters_dictionary = {'easy': (31, 36), 'medium': (25, 30), 'hard': (19, 24)}
        self.difficulty = None

    def remove_fields(self):
        indexes = [i for i in range(81)]
        indexes_to_keep = random.sample(indexes, random.randint(self.difficulty_parameters_dictionary[self.difficulty][0], self.difficulty_parameters_dictionary[self.difficulty][1]))
        for index_to_keep in indexes_to_keep:
            i, j = index_to_keep // 9, index_to_keep - 9 * (index_to_keep // 9)
            self.grid[i][j] = self.solved_grid[i][j]

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def main(self):
        root = tk.Tk()
        root.title('Sudoku Creator')

        tk.Label(root, text='Sudoku Creator:', font=font.Font(family='Helvetica', size=14, weight='bold')).pack()
        tk.Label(root, text='').pack()
        tk.Label(root, text='Please select a difficulty level', font=font.Font(family='Helvetica', size=12, weight='normal')).pack()

        tk.Button(root, text=f'EASY ({self.difficulty_parameters_dictionary["easy"][0]}-{self.difficulty_parameters_dictionary["easy"][1]} clues)', bd=4, font=12, command=lambda: [root.destroy(), self.set_difficulty('easy'), self.remove_fields(), self.format_output()]).pack()
        tk.Button(root, text=f'MEDIUM ({self.difficulty_parameters_dictionary["medium"][0]}-{self.difficulty_parameters_dictionary["medium"][1]} clues)', bd=4, font=12, command=lambda: [root.destroy(), self.set_difficulty('medium'), self.remove_fields(), self.format_output()]).pack()
        tk.Button(root, text=f'HARD ({self.difficulty_parameters_dictionary["hard"][0]}-{self.difficulty_parameters_dictionary["hard"][1]} clues)', bd=4, font=12, command=lambda: [root.destroy(), self.set_difficulty('hard'), self.remove_fields(), self.format_output()]).pack()
        tk.Label(root, text='').pack()
        tk.Button(root, text='EXIT', bd=4, font=12, command=lambda: [root.destroy()]).pack()

        self.window_on_top_update(root)
        self.window_position_adjuster(root)
        root.mainloop()

    def format_output(self, cell_dimension=0.1):
        cell_text = [[str(el) for el in row] for row in self.grid]
        final_grid = plt.table(cell_text, loc='center', rowLoc='center', colLoc='center', cellLoc='center')

        cell_dict = final_grid.get_celld()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cell_dict[(i, j)].set_height(cell_dimension)
                cell_dict[(i, j)].set_width(cell_dimension)

        final_grid.auto_set_font_size(False)
        final_grid.set_fontsize(20)
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for i in range(4):
            ax.axhline(xmin=cell_dimension / 2, xmax=1 - cell_dimension / 2, y=3 * i * cell_dimension + cell_dimension / 2, linewidth=3, color='black')
            ax.axvline(ymin=cell_dimension / 2, ymax=1 - cell_dimension / 2, x=3 * i * cell_dimension + cell_dimension / 2, linewidth=3, color='black')

        plt.box(on=None)
        plt.show()

    @staticmethod
    def window_position_adjuster(window, width_adjuster=0.7, height_adjuster=0.7):
        window.update()
        window.geometry('%dx%d+%d+%d' % (window.winfo_width(), window.winfo_height(), width_adjuster * ((window.winfo_screenwidth() - window.winfo_width()) / 2), height_adjuster * ((window.winfo_screenheight() - window.winfo_height()) / 2)))

    @staticmethod
    def window_on_top_update(window):
        window.attributes('-topmost', True)
        window.update()
        window.attributes('-topmost', False)
        window.focus_force()
        window.update()
