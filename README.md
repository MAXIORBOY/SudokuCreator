# Sudoku Creator is a web application, created in Django, which allows a user to solve an automatically generated Sudoku grid. 

## Features:
* 3 levels of difficulty:
  * Easy
  * Medium
  * Hard
* Secured input: Only digits from 1 to 9 are allowed (any other character will be automatically erased).
* Reset all filled forms.
* Solution to the current grid.  

## Method:
Application uses my own methods to create and solve a Sudoku grid.  

Solver:
You can find my solver here: [link](https://github.com/MAXIORBOY/SudokuSolver)  

Creator:
At first the application solves a Sudoku grid with no clues at all. Then the application randomly removes clue by clue from the solved grid, making sure that the desired level of difficulty is maintained. It can be done by monitoring the ```number_of_assumptions``` parameter from the solver.

## Launch:
* From the command line, type: ```python manage.py runserver```. Then launch any internet browser and go the site, which will show up in the command line (by default it should be: 127.0.0.1:8000/).

## Technology:
* ```Python``` 3.8
* ```Django``` 3.1.2
* ```numpy``` 1.19.3  

## Screenshots: 
![sudoku1](https://user-images.githubusercontent.com/71539614/108204315-ef72bc00-7123-11eb-8aa9-a1167ead458c.png)
![sudoku2](https://user-images.githubusercontent.com/71539614/108204316-f00b5280-7123-11eb-96be-011c0da55652.png)
![sudoku3](https://user-images.githubusercontent.com/71539614/108204318-f00b5280-7123-11eb-95b1-71f799dde89a.png)
![sudoku4](https://user-images.githubusercontent.com/71539614/108204320-f0a3e900-7123-11eb-8da0-9fba6e907c21.png)
![sudoku5](https://user-images.githubusercontent.com/71539614/108204322-f0a3e900-7123-11eb-9db1-a7fb895266c8.png)
![sudoku6](https://user-images.githubusercontent.com/71539614/108204312-eeda2580-7123-11eb-923d-d839f24c7a41.png)

