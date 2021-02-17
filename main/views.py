from django.shortcuts import render, redirect
from .forms import NewForm, NewFormSet
from .view_methods import *


def home_page(request, **kwargs):
    return render(request, 'main/home.html', {})


def sudoku(request, **kwargs):
    # Check difficulty change
    difficulty_change_flag = False
    if request.POST.get('button_difficulty', None) is not None:
        difficulty = request.POST['button_difficulty']
        difficulty_change_flag = True
    else:
        if request.session.get('difficulty', None) is not None:
            difficulty = request.session['difficulty']
        else:
            return redirect(home_page)

    # Reset session
    if request.POST.get('button_next', None) is not None or difficulty_change_flag:
        request.session.flush()

    # Restore difficulty
    request.session['difficulty'] = difficulty

    # Restore / Re-generate grid
    generated_sudoku_grid = request.session.get('generated_sudoku_grid', False)
    if not generated_sudoku_grid:
        generated_sudoku_grid = generate_new_sudoku_grid(difficulty)
        request.session['generated_sudoku_grid'] = generated_sudoku_grid

    sudoku_grid = merge_generated_and_users_data_into_one_matrix(request, generated_sudoku_grid)
    sudoku_solved_flag = False 

    # Solution button pressed event check
    if request.POST.get('button_solution', None) is not None:
        solution_button_pressed_flag = True
        solution = solve_sudoku_grid(generated_sudoku_grid)
    else:
        solution_button_pressed_flag = False
        solution = None

    # Reset / Retain form values
    if request.POST.get('button_reset', None) is not None or request.POST.get('button_next', None) is not None or request.POST.get('button_solution', None) is not None or difficulty_change_flag:
        formset = NewFormSet()
    else:
        formset = NewFormSet(request.POST or None, request.FILES or None)
        sudoku_solved_flag = sudoku_grid_solved_correctly_test(sudoku_grid)


    button_check_pressed = request.POST.get('button_check', False)

    return render(request, "main/sudoku.html", {'formset': formset, 'generated_sudoku_grid': generated_sudoku_grid, 'sudoku_solved_flag': sudoku_solved_flag,
                                                'solution_button_pressed_flag': solution_button_pressed_flag, 'solution': solution, 'difficulty': difficulty, 'button_check_pressed': button_check_pressed})
