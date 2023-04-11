# piramide problem AI
from ortools.sat.python import cp_model as cp

class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, n, x):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__n = n 
        self.__x = x
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print(f"Solution #{self.__solution_count}:")
        for i in range(self.__n):
          
          # corrimiento para simular piramide
          if i%2:
            [print('    ',end='') for k in range (self.__n - i//2)]
          else:
            [print('    ',end='') for k in range (self.__n - i//2)]
            print('  ',end='')
          
          for j in range(i+1):
            print('{:3d} '.format(self.Value(self.__x[i][j])),end='')
          print()
        print()

    def SolutionCount(self):
        return self.__solution_count

def solver_piramide(puzzle, n):
    # Creates the model.
    model = cp.CpModel()

    # Creates the variables.
    piramide = []
    for i in range(n):
        row = []
        for j in range(i+1):
            if puzzle[i][j]:
                val = puzzle[i][j]
                row.append(model.NewIntVar(val, val, 'x({},{})'.format(i, j)))
            else:
                #puzzle Malaga basta con limite 717
                row.append(model.NewIntVar(1, 717, 'x({},{})'.format(i, j)))
        piramide.append(row)

    # Creates the constraints.
    for i in range(n-1):
        for j in range(i+1):
            model.Add(piramide[i][j] == piramide[i+1][j] + piramide[i+1][j+1])

    # Creates a solver and solves the model.
    solver = cp.CpSolver()
    solution_printer = SolutionPrinter(n, piramide)
    status = solver.SearchForAllSolutions(model, solution_printer)

#puzzles
malaga = [[717], [0,0], [168,0,203], [0,0,0,0], [56,0,40,0,49], [0,0,0,0,0,0], [16,0,4,0,16,0,3]]
n = len(malaga)

#puzzle1 = [[213], [0, 0], [0, 55, 0], [24, 0, 0, 24], [15, 0, 0, 6, 0]]
#n1 = len(puzzle1)

#puzzle2 = [[0], [0, 0], [375, 0, 171], [125, 250, 98, 0]]
#n2 = len(puzzle2)

#puzzle3 = [[80], [0, 0], [19, 0, 0], [0, 0, 0, 0], [0, 0, 6, 0, 5], [1, 0, 0, 0, 0, 4]]
#n3 = len(puzzle3)

solver_piramide(malaga, n)
#solver_piramide(puzzle1, n1)
#solver_piramide(puzzle2, n2)
#solver_piramide(puzzle3, n3)
