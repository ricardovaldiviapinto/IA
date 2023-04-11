# cripto problem AI
from ortools.sat.python import cp_model as cp

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
status = solver.Solve(model)

if status == cp.OPTIMAL:
    print('S = {}'.format(solver.Value(s)))
    print('E = {}'.format(solver.Value(e)))
    print('N = {}'.format(solver.Value(n)))
    print('D = {}'.format(solver.Value(d)))
    print('M = {}'.format(solver.Value(m)))
    print('O = {}'.format(solver.Value(o)))
    print('R = {}'.format(solver.Value(r)))
    print('Y = {}'.format(solver.Value(y)))
else:
    print('No hay solucion optima')
