# kakurasu problem AI

"""
  kakurasu
"""
from ortools.sat.python import cp_model as cp
import numpy as np

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
            print('{:3d}'.format(self.Value(self.__x[i,j])), end=" ")
          print()
        print()

        if self.__limit > 0 and self.__solution_count >= self.__limit:
          self.StopSearch() 

    def SolutionCount(self):
        return self.__solution_count


def kakurasu(n, lf, lc, limit=1):

    model = cp.CpModel()

    # variables
    raw_mtrx = [[model.NewBoolVar('x({},{})'.format(i, j)) for j in range(n)] for i in range(n)]

    np_mtrx = np.array(raw_mtrx)

    # constraints
  
    # restricciones por fila
    for cont, row in enumerate(np_mtrx):
        model.Add(sumatoria(row) == lf[cont])

    # restricciones por columna
    np_mtrx_T = np_mtrx.transpose()
    for cont, col in enumerate(np_mtrx_T):
        model.Add(sumatoria(col) == lc[cont])

    # solution and search
    solver = cp.CpSolver()

    # status = solver.Solve(model)
    solution_printer = SolutionPrinter(n, np_mtrx, limit)
  
    print('Dimension: {}'.format(n))
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

# sumatoria de los productos de los pesos (c) por la lista (l) de 0s y 1s
def sumatoria(l):
    return sum([i*j for i,j in enumerate(l, start=1)])


kakurasu(4, [4, 9, 8, 3], [8, 6, 6, 5]) #facil
# kakurasu(5,  [7, 9, 7, 4, 14], [2, 5, 11, 13, 7])
# kakurasu(6, [8,15,13,10,4,7],[13,4,7,4,5,16])
# kakurasu(7, [21,18,10,27,2,23,15], [19,15,11,19,13,13,21])
# kakurasu(9, [17,44,20,13,13,25,5,26,23], [17,35,35,10,11,9,33,5,30])
