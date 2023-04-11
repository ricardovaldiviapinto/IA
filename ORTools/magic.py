# magic square problem AI

"""
  Magic squares in Google CP-SAT Solver.

  Magic square problem.
  See https://en.wikipedia.org/wiki/Magic_square
  '''
  In recreational mathematics, a square array of numbers, usually positive integers, 
  is called a magic square if the sums of the numbers in each row, each column, 
  and both main diagonals are the same. The order of the magic square is the number of 
  integers along one side (n), and the constant sum is called the magic constant. 
  If the array includes just the positive integers 1,2,...,n^2, the magic square is 
  said to be normal. Some authors take magic square to mean normal magic squares.
  ''' 
"""
from ortools.sat.python import cp_model as cp
import numpy as np
import sys

class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, n, x, limit=0):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__n = n 
        self.__x = x
        self.__limit = limit
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print('Solution #{}:'.format(self.__solution_count))

        for i in range(self.__n):
          for j in range(self.__n):
            print('{:3d}'.format(self.Value(self.__x[i,j])), end=' ')
          print()
        print()

        if self.__limit > 0 and self.__solution_count >= self.__limit:
          self.StopSearch() 

    def SolutionCount(self):
        return self.__solution_count

def magic(n=3, limit=1):

    model = cp.CpModel()

    # variables
    raw_mtrx = []
    for i in range(n):
      row = []
      for j in range(n):
        row.append(model.NewIntVar(1, n*n, 'x({},{})'.format(i, j)))
      raw_mtrx.append(row) 

    np_mtrx = np.array(raw_mtrx)

    # magic sum
    s = ( n * (n*n + 1)) // 2

    # constraints
    np_mtrx_f = np_mtrx.flatten()
    model.AddAllDifferent(np_mtrx_f)

    for row in np_mtrx:
      model.Add(np.sum(row) == s)
    
    np_mtrx_T = np_mtrx.transpose()
    for col in np_mtrx_T:
      model.Add(np.sum(col) == s)

    diagonal1 = np_mtrx.diagonal()
    model.Add(np.sum(diagonal1) == s)

    diagonal2 = np.fliplr(np_mtrx).diagonal()
    model.Add(np.sum(diagonal2) == s)

    # solution and search
    solver = cp.CpSolver()

    # status = solver.Solve(model)
    solution_printer = SolutionPrinter(n, np_mtrx, limit)
  
    print('Dimension: {}'.format(n))
    print('Magic Sum: {}'.format(s))
    print()

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


n, limit = 3, 10
if len(sys.argv) > 1:
    n = int(sys.argv[1])
if len(sys.argv) > 2:
    limit = int(sys.argv[2])

magic(n, limit)
