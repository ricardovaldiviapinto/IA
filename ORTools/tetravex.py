# tetravex problem AI

from ortools.sat.python import cp_model as cp

class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, t, n, limit=0):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__t = t 
        self.__n = n
        self.__limit = limit
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print('Solution #{}:'.format(self.__solution_count))

        for i in range(self.__n):
          for j in range(self.__n):
            print('[', end='')
            for p in range(4):
                print('{:2d}'.format(self.Value(self.__t[i][j][p])), end=' ')
            print(']', end='')
          print()
        print()

        if self.__limit > 0 and self.__solution_count >= self.__limit:
          self.StopSearch() 

    def SolutionCount(self):
        return self.__solution_count

def flatten(l):
    return [item for sublist in l for item in sublist]

def tetravex(tvx, n=3, limit=1):

    model = cp.CpModel()

    # variables
    raw_mtrx = [[[model.NewIntVar(0, 9, 'l({},{})'.format(i, j)),
                  model.NewIntVar(0, 9, 'r({},{})'.format(i, j)),
                  model.NewIntVar(0, 9, 'u({},{})'.format(i, j)),
                  model.NewIntVar(0, 9, 'd({},{})'.format(i, j))] for j in range(n)] for i in range(n)]

    flat_tvx = flatten(tvx)

    # constraints
    for i in range(n):
        for j in range(n):
            model.AddAllowedAssignments(raw_mtrx[i][j], flat_tvx)
            
            if j < n-1:
                model.Add(raw_mtrx[i][j][1] == raw_mtrx[i][j+1][0]) 
            
            if i < n-1:
                model.Add(raw_mtrx[i][j][3] == raw_mtrx[i+1][j][2])


    # Elimina fichas duplicadas -----------------------------------------------------
    unq = [model.NewIntVar(0, 9999, 'u({})'.format(i)) for i in range(n*n)]
    
    flat_raw_mtrx = flatten(raw_mtrx)
    for i, p in enumerate(flat_raw_mtrx):
        model.Add(unq[i] == p[0] + p[1]*10 + p[2]*100 + p[3]*1000)
    
    model.AddAllDifferent(unq)
    # -------------------------------------------------------------------------------

    # solution and search
    solver = cp.CpSolver()

    # status = solver.Solve(model)
    solution_printer = SolutionPrinter(raw_mtrx, n, limit)
  
    print('Dimension: {}x{}'.format(n, n))
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


#tvx2 = [[[5,8,6,0], [6,7,0,4]], [[2,5,7,6], [8,6,6,8]]]
#tvx3 = [[[0,9,7,7,],[8,1,7,4],[3,8,7,2]],[[0,2,9,7],[7,6,7,7],[2,0,6,0]],[[4,7,4,6],[1,7,0,1],[7,3,1,4]]]
#tvx4 = [[[8,3,0,8],[7,4,4,7],[8,7,3,0],[6,0,2,1]],[[9,8,5,3],[7,7,6,3],[0,1,7,4],[1,8,4,5]],[[5,8,8,9],[6,1,1,2],[1,7,4,3],[0,9,2,8]],[[3,2,3,4],[7,4,8,6],[8,7,3,5],[7,7,8,6]]]
#tvx6 = [[[6,8,9,9],[8,2,6,9],[7,7,9,4],[8,4,0,9],[9,7,6,4],[2,3,4,0]],[[0,9,3,4],[3,2,7,9],[7,2,9,3],[0,6,0,1],[7,5,0,9],[5,4,9,6]],[[0,7,8,6],[7,5,2,9],[5,4,6,5],[8,0,9,4],[6,6,4,4],[4,7,5,4]],[[6,8,2,7],[2,0,6,5],[0,0,7,0],[4,7,7,4],[2,8,4,6],[0,0,9,2]],[[6,7,4,5],[4,1,2,0],[9,2,3,6],[9,5,9,2],[5,3,7,3],[8,6,4,0]],[[2,9,6,2],[3,3,5,8],[1,0,5,9],[0,8,4,3],[0,0,3,7],[4,9,9,3]]]
tvx = [[[1,9,2,2],[1,9,4,9],[6,8,9,7]],[[9,9,2,9],[0,6,9,5],[0,1,5,4]],[[4,0,7,7],[5,1,4,7],[7,0,6,4]]]
tetravex(tvx, 3)
