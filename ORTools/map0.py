# map coloring problem AI
from ortools.sat.python import cp_model as cp

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
status = solver.Solve(model)

if status == cp.OPTIMAL:
    for r in australia:
        #print(r.Name(), solver.Value(r))
        if   solver.Value(r) == 1: print('{:3s} = green'.format(r.Name()))
        elif solver.Value(r) == 2: print('{:3s} = red  '.format(r.Name()))
        elif solver.Value(r) == 3: print('{:3s} = blue '.format(r.Name()))
else:
    print('No hay solucion optima')
