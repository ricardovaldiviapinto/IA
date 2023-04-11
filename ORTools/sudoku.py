# sudoku problem AI

"""This model implements a sudoku solver."""

from ortools.sat.python import cp_model as cp
import numpy as np
import samples_sudoku as ss

class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, n, x):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__n = n 
        self.__x = x
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print('Solution #{}:'.format(self.__solution_count))

        for i in range(self.__n):
          for j in range(self.__n):
            print("%3i" % self.Value(self.__x[i,j]), end=" ")
          print()
        print()

    def SolutionCount(self):
        return self.__solution_count

def solve_sudoku(grid):
    """Solves the sudoku problem with the CP-SAT solver."""
    # Create the model.
    model = cp.CpModel()

    # variables
    raw_mtrx = []
    for i in range(9):
        row = []
        for j in range(9):
            if grid[i][j]:
                val = int(grid[i][j])
                row.append(model.NewIntVar(val, val, 'x({},{})'.format(i, j)))
            else:
                row.append(model.NewIntVar(1, 9, 'x({},{})'.format(i, j)))
        raw_mtrx.append(row) 
    
    np_mtrx = np.array(raw_mtrx)
    
    # constraints
    
    # 1. filas 
    for row in np_mtrx:
        model.AddAllDifferent(row)
    
    # 2. columnas
    np_mtrx_T = np_mtrx.transpose()
    for col in np_mtrx_T:
        model.AddAllDifferent(col)

    # 3. celdas
    for i1,i2 in ((0,3),(3,6),(6,9)):
        for j1,j2 in ((0,3),(3,6),(6,9)):
            model.AddAllDifferent(np_mtrx[i1:i2,j1:j2].flatten())

    # Solve and print out the solution.
    solver = cp.CpSolver()

    # status = solver.Solve(model)
    solution_printer = SolutionPrinter(9, np_mtrx)
  
    # solution_printer = SimpleSolutionCounter(x)
    status = solver.SearchForAllSolutions(model, solution_printer)

    if not (status == cp.FEASIBLE or status == cp.OPTIMAL):
        print("No solution found!")

    print()
    print('NumSolutions: {}'.format(solution_printer.SolutionCount()))
    print('NumConflicts: {}'.format(solver.NumConflicts()))
    print('NumBranches:  {}'.format(solver.NumBranches()))
    print('WallTime:     {}'.format(solver.WallTime()))
    print()

solve_sudoku(ss.sample2)
