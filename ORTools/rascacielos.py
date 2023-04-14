# skyscrapers problem AI

"""
  skyscrapers
"""
from ortools.sat.python import cp_model as cp
import numpy as np
import samples_rascacielos as src

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


def skyscrapers(n, lf, lfi, lc, lci, grid = None, limit=1):

    if grid is None: grid=np.zeros([n,n])

    model = cp.CpModel()

    # variables
    raw_mtrx = [[model.NewIntVar(grid[i][j], grid[i][j], 'x({},{})'.format(i, j))
                 if grid[i][j] else model.NewIntVar(1, n, 'x({},{})'.format(i, j))
                 for j in range(n)] for i in range(n)]

    # constraints
  
    # restricciones por fila
    # de izquierda a derecha
    np_mtrx = np.array(raw_mtrx)
    for cont, row in enumerate(np_mtrx):
        model.AddAllDifferent(row)
        if lf[cont] != 0:
            model.Add(rascacielos(model,row,n) == lf[cont])

    # de derecha a izquierda
    np_mtrx_lr = np.fliplr(np_mtrx)
    for cont, row in enumerate(np_mtrx_lr):
        if lfi[cont] != 0:
            model.Add(rascacielos(model,row,n) == lfi[cont])

    # restricciones por columna
    # de arriba hacia abajo
    np_mtrx_T = np_mtrx.transpose()
    for cont, col in enumerate(np_mtrx_T):        
        model.AddAllDifferent(col)
        if lc[cont] != 0:
            model.Add(rascacielos(model,col,n) == lc[cont])

    # de abajo hacia arriba
    np_mtrx_Tud = np.flipud(np_mtrx).transpose()
    for cont, col in enumerate(np_mtrx_Tud):
        if lci[cont] != 0:
            model.Add(rascacielos(model,col,n) == lci[cont])

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

# subproblema por row 
def rascacielos(model,row,n):

# Creates the variables.
    visibles = []
    for i in range(n):
        visibles.append(model.NewBoolVar('v({})'.format(i)))

# Creates the constraints.
    for i in range(n):
        tmp = model.NewIntVar(1, n, 'tmp')
        model.AddMaxEquality(tmp, row[:i+1])

        model.Add(row[i] == tmp).OnlyEnforceIf(visibles[i])
        model.Add(row[i] != tmp).OnlyEnforceIf(visibles[i].Not())

    return(sum(visibles))

skyscrapers(4,[0,2,0,3],[0,1,3,0],[0,1,2,0],[0,0,1,0])
#skyscrapers(4,[3,2,1,2],[1,3,2,2],[2,2,3,1],[2,2,1,3])
#skyscrapers(4,[0,4,0,0],[0,0,0,0],[2,3,0,0],[0,0,0,0])
#skyscrapers(4,[0,0,0,0],[0,1,0,0],[0,0,2,0],[0,2,0,0], src.sample1)
#skyscrapers(5,[2,1,3,3,2],[3,5,3,2,1],[2,1,2,4,4],[2,4,2,2,1])
#skyscrapers(5,[0,0,3,0,0],[5,3,0,0,3],[0,0,0,0,0],[0,0,2,2,0])
#skyscrapers(5,[0,3,0,0,3],[0,0,0,0,0],[0,1,3,0,3],[0,0,2,2,0], src.sample2)
#skyscrapers(6,[3,2,1,3,3,2],[2,3,2,1,2,2],[2,2,5,2,1,4],[2,3,1,2,6,3], src.sample3)
#skyscrapers(6,[0,0,0,6,4,0],[0,0,0,0,0,0],[0,3,3,0,0,0],[5,0,3,0,0,3])
#skyscrapers(6,[0,3,0,2,0,2],[3,0,0,1,3,0],[0,1,0,3,0,2],[0,0,3,0,3,0], src.sample4)
#skyscrapers(7,[0,0,1,3,0,0,0],[0,2,0,2,0,3,5],[2,2,0,0,3,0,0],[0,0,0,0,0,5,0], src.sample5)