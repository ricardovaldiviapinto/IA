# nonogram problem AI
"""This model implements a nonogram solver."""

from ortools.sat.python import cp_model as cp
# AddAutomata es incompatible con numpy: import numpy as np

class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, n, x):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__n = n 
        self.__x = x
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print('Solution #{}'.format(self.__solution_count))

        for i in range(self.__n):
          for j in range(self.__n):
            print('{:3d}'.format(self.Value(self.__x[i][j])), end=" ")
          print()
        print()

    def SolutionCount(self):
        return self.__solution_count

def solve_nonogram(picr, picc, n, m):
    """Solves a nonogram problem with the CP-SAT solver."""
    # Create the model.
    model = cp.CpModel()

    # variables
    raw_mtrx = [[model.NewIntVar(0, 1, 'x({},{})'.format(i, j)) for j in range(n)] for i in range(m)]
    
    # transpuesta
    raw_mtrx_T = [[raw_mtrx[j][i] for j in range(m)] for i in range(n)]
    
    #constraints

    for row1, row2 in zip(picr, raw_mtrx):
        state, automata = make_automata(row1)
        model.AddAutomaton(row2, 0, [state], automata)

    for row1, row2 in zip(picc, raw_mtrx_T):
        state, automata = make_automata(row1)
        model.AddAutomaton(row2, 0, [state], automata)

    # solution and search
    solver = cp.CpSolver()

    # status = solver.Solve(model)
    solution_printer = SolutionPrinter(n, raw_mtrx)
  
    print('Dimension: {}x{}'.format(n,m))
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

# basado en : http://www.hakank.org/
# estrategia: nonogram_automaton_sat
def make_automata(pattern):
    """Make an automata from a pattern, e.g. [3,2,1]"""
    
    state = 0
    automata = [(state, 0, state)] # 0*
    if not pattern[0]: return state, automata

    limit = len(pattern)
    for i in range(limit):
        for _ in range(pattern[i]):      
            automata.append((state, 1, state+1)) # 1{pattern[i]}
            state += 1

        if i < limit-1:
            automata.append((state, 0, state+1)) # 0+
            state += 1
  
        automata.append((state, 0, state)) # 0*
  
    return state, automata

#solve_nonogram([[0],[1],[3],[1],[0]],[[0],[1],[3],[1],[0]], 5, 5)
#solve_nonogram([[0],[1],[1,1],[1],[0]],[[0],[1],[1,1],[1],[0]], 5, 5)
#solve_nonogram([[3],[2],[2],[2],[4]],[[3],[3],[1,1],[2,1],[2]], 5, 5)

#solve_nonogram([[3,3],[1,6],[6],[4],[2],[2,1],[1,1,1],[4],[2,6],[7]],[[1,1,1],[1,2,1],[7],[4,1],[3,2],[3,2],[3,3],[2,3],[1,1,3],[1,4]], 10, 10)

#solve_nonogram([[3,3],[3,3],[1,3,1,4],[7,3],[6],[1,5],[2,4,3],[5,1,4],[3,7],[4,5],[8],[1,3,2,2],[3,2,3],[1,1,1,2],[1,2]],
#               [[3,8],[2,5,1],[2,7],[1,1,3],[7,2,1],[5,1,1],[9],[4,5],[3,3,3],[3,3],[1,4],[1,2],[4,1,2],[4,4],[4,3]], 15, 15)

#solve_nonogram([[1,1,5,5],[1,1,3,4],[9,2],[1,8,2],[3,7,2,2],[2,1,4,1,2],[2,2,1,1],[2,4],[3,1,4],[3,5,3],[3,6,2],[3,4,1],[4,1],[5,2],[1,4,1,2],[2,3,2,6],[1,3,3],[2,4,4,3],[12,2],[10,4,2]],
#               [[6,3,1,3],[14,1,3],[1,1,6,2],[4,1,4,3],[2,1,5],[3,1,3],[3,3],[5,1,1,2],[5,2,3,2],[6,3,7],[1,2,6,3],[1,2,4,3],[1,3,1,1],[3,1],[3,1,1],[1,1],[2,4,3,2],[2,3,5],[11,4],[6,5,2,1]], 20, 20)
