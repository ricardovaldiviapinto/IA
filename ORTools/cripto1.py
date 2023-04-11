# cripto problem AI
from ortools.sat.python import cp_model as cp

class VarArraySolutionPrinter(cp.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('{} = {}'.format(v, self.Value(v)), end=', ')
        print()

    def solution_count(self):
        return self.__solution_count 


# Creates the model.
model = cp.CpModel()

# Creates the variables.
s = model.NewIntVar(1, 9, 'S')
e = model.NewIntVar(0, 9, 'E')
n = model.NewIntVar(0, 9, 'N')
d = model.NewIntVar(0, 9, 'D')
m = model.NewIntVar(1, 9, 'M')
o = model.NewIntVar(0, 9, 'O')
r = model.NewIntVar(0, 9, 'R')
y = model.NewIntVar(0, 9, 'Y')

letters = [s, e, n, d, m, o, r, y]

# Creates the constraints.
model.AddAllDifferent(letters)

model.Add(1000*s + 100*e + 10*n + d + 1000*m + 100*o + 10*r + e == 10000*m + 1000*o + 100*n + 10*e + y)

# Creates a solver and solves the model.
solver = cp.CpSolver()
solution_printer = VarArraySolutionPrinter(letters)
status = solver.SearchForAllSolutions(model, solution_printer)
