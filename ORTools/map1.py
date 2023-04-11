# map coloring problem AI
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
            if   self.Value(v) == 1: print('{} = green'.format(v.Name()), end = ', ')
            elif self.Value(v) == 2: print('{} = red  '.format(v.Name()), end = ', ')
            elif self.Value(v) == 3: print('{} = blue '.format(v.Name()), end = ', ')
        print()

    def solution_count(self):
        return self.__solution_count 

# Creates the model.
model = cp.CpModel()

# Creates the variables.
wa  = model.NewIntVar(1, 3, 'WA')
nt  = model.NewIntVar(1, 3, 'NT')
sa  = model.NewIntVar(1, 3, 'SA')
q   = model.NewIntVar(1, 3, 'Q')
nsw = model.NewIntVar(1, 3, 'NSW')
v   = model.NewIntVar(1, 3, 'V')

australia = [wa, nt, sa, q, nsw, v]

mapa = [(wa,nt), (wa,sa), (nt,sa), (nt,q), (sa,q), (sa,nsw), (sa,v), (q,nsw), (v,nsw)]

# Creates the constraints.
for r1, r2 in mapa:
    model.Add(r1 != r2)

# Creates a solver and solves the model.
solver = cp.CpSolver()
solution_printer = VarArraySolutionPrinter(australia)

# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True

# Solve.
status = solver.SearchForAllSolutions(model, solution_printer)

print('Status = {}'.format(solver.StatusName(status)))
print('Number of solutions found: {}'.format(solution_printer.solution_count()))
