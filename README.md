# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The *naked twins* in each unit constraint other unresolved boxes in the same unit, i.e. they could
   not have the same digits as in the twins. By eliminating those digits, we start dealing with smaller search space and could possibly create more
   naked twins and/or other constraints like one-choice, and hence has opportunities to eliminate more digits from those unresolved boxes.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Diagonal* adds new contraints to what we could set in each box. 1 though 9 could only appear once in both primary and secondary diagonals. The resolved boxes constraint what could be put in other unresolved boxes in the same diagonal, i.e. they could not take the same digit as in the resolved one. By elminiating those digits from the unresolved boxes in the same diagonal, we reduce the search space, and create more opportunities to further apply other strategies like one-choice, naked twins, i.e. constraints propogate, eliminate in each step, and lead us closer to the solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.