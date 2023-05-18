# instant insanity problem AI

from ortools.sat.python import cp_model as cp
from time import perf_counter

class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, cubns):
        cp.CpSolverSolutionCallback.__init__(self)
        self.__cubns = cubns
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print('Solution #{}:'.format(self.__solution_count))
        SolutionPrinter.print_cube(self, self.__cubns[0])
        SolutionPrinter.print_cube(self, self.__cubns[1])
        SolutionPrinter.print_cube(self, self.__cubns[2])
        SolutionPrinter.print_cube(self, self.__cubns[3])
        SolutionPrinter.print_cube(self, self.__cubns[4])
        SolutionPrinter.print_cube(self, self.__cubns[5])
        
    def print_cube(self, c):
        print('[{:1d}, '.format(self.Value(c[0])), end=' ')
        print('[{:1d}, '.format(self.Value(c[1][0])), end=' ')
        print('{:1d}, '.format(self.Value(c[1][1])), end=' ')
        print('{:1d}, '.format(self.Value(c[1][2])), end=' ')
        print('{:1d}], '.format(self.Value(c[1][3])), end=' ')
        print('{:1d}]'.format(self.Value(c[2])), end=' ')
        print()

    def SolutionCount(self):
        return self.__solution_count
    
def flip(cube):
    return [cube[0], [cube[1][3], cube[1][0], cube[1][1], cube[1][2]], cube[2]]

def rotate(cube):
    return [cube[1][3], [cube[1][0], cube[0], cube[1][2], cube[2]], cube[1][1]]

def turn1(cube):
    return [cube[1][2], [cube[0], cube[1][1], cube[2], cube[1][3]], cube[1][0]]

def turn2(cube):
    return [cube[1][0], [cube[2], cube[1][1], cube[0], cube[1][3]], cube[1][2]]

def flips(cube):
    yield cube
    yield flip(cube)
    yield flip(flip(cube))
    yield flip(flip(flip(cube)))

def rotations(cube):       
    yield cube
    yield rotate(cube)        
    yield rotate(rotate(cube))
    yield rotate(rotate(rotate(cube)))
    yield turn1(cube)
    yield turn2(cube)

def move(cube):
    """move generador de las 24 posiciones de un cubo"""
    for f in flips(cube):
        for r in rotations(f):
            yield r

def flatten(l):
    return [l[0]]+l[1]+[l[2]]

def insanity(cubes, n):
    model = cp.CpModel()

    cubn1 = [model.NewIntVar(1, n, 'c1l'),
            [model.NewIntVar(1, n, 'c1f'), model.NewIntVar(1, n, 'c1u'), model.NewIntVar(1, n, 'c1b'), model.NewIntVar(1, n, 'c1d')],                
             model.NewIntVar(1, n, 'c1r')]              

    cubn2 = [model.NewIntVar(1, n, 'c2l'),
            [model.NewIntVar(1, n, 'c2f'), model.NewIntVar(1, n, 'c2u'), model.NewIntVar(1, n, 'c2b'), model.NewIntVar(1, n, 'c2d')],                
             model.NewIntVar(1, n, 'c2r')] 

    cubn3 = [model.NewIntVar(1, n, 'c3l'),
            [model.NewIntVar(1, n, 'c3f'), model.NewIntVar(1, n, 'c3u'), model.NewIntVar(1, n, 'c3b'), model.NewIntVar(1, n, 'c3d')],                
             model.NewIntVar(1, n, 'c3r')] 

    cubn4 = [model.NewIntVar(1, n, 'c4l'),
            [model.NewIntVar(1, n, 'c4f'), model.NewIntVar(1, n, 'c4u'), model.NewIntVar(1, n, 'c4b'), model.NewIntVar(1, n, 'c4d')],                
             model.NewIntVar(1, n, 'c4r')] 

    cubn5 = [model.NewIntVar(1, n, 'c5l'),
            [model.NewIntVar(1, n, 'c5f'), model.NewIntVar(1, n, 'c5u'), model.NewIntVar(1, n, 'c5b'), model.NewIntVar(1, n, 'c5d')],                
             model.NewIntVar(1, n, 'c5r')] 
    
    cubn6 = [model.NewIntVar(1, n, 'c6l'),
            [model.NewIntVar(1, n, 'c6f'), model.NewIntVar(1, n, 'c6u'), model.NewIntVar(1, n, 'c6b'), model.NewIntVar(1, n, 'c6d')],                
             model.NewIntVar(1, n, 'c6r')] 
    
    cubns = [cubn1, cubn2, cubn3, cubn4, cubn5, cubn6]

    states1 = [flatten(m1) for m1 in move(cubes[0])]
    states2 = [flatten(m2) for m2 in move(cubes[1])]
    states3 = [flatten(m3) for m3 in move(cubes[2])]
    states4 = [flatten(m4) for m4 in move(cubes[3])]
    states5 = [flatten(m5) for m5 in move(cubes[4])]
    states6 = [flatten(m6) for m6 in move(cubes[5])]
    
    model.AddAllowedAssignments(flatten(cubn1), states1)
    model.AddAllowedAssignments(flatten(cubn2), states2)
    model.AddAllowedAssignments(flatten(cubn3), states3)
    model.AddAllowedAssignments(flatten(cubn4), states4)
    model.AddAllowedAssignments(flatten(cubn5), states5)
    model.AddAllowedAssignments(flatten(cubn6), states6)
    
    model.AddAllDifferent([cubn1[1][0], cubn2[1][0], cubn3[1][0], cubn4[1][0], cubn5[1][0], cubn6[1][0]])
    model.AddAllDifferent([cubn1[1][1], cubn2[1][1], cubn3[1][1], cubn4[1][1], cubn5[1][1], cubn6[1][1]])
    model.AddAllDifferent([cubn1[1][2], cubn2[1][2], cubn3[1][2], cubn4[1][2], cubn5[1][2], cubn6[1][2]])
    model.AddAllDifferent([cubn1[1][3], cubn2[1][3], cubn3[1][3], cubn4[1][3], cubn5[1][3], cubn6[1][3]])

    # solution and search
    solver = cp.CpSolver()

    # status = solver.Solve(model)
    solution_printer = SolutionPrinter(cubns)
  
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

# red   = 1
# white = 2
# blue  = 3
# green = 4
# cube1 = [1, [1, 2, 3, 4], 1]
# cube2 = [2, [2, 1, 4, 3], 3]
# cube3 = [1, [1, 2, 2, 3], 4]
# cube4 = [3, [1, 2, 4, 4], 3]

# https://www.jaapsch.net/puzzles/insanity.htm
# red   = 1
# yellow = 2
# blue  = 3
# green = 4
# cyan = 5
# orange = 6
# 1. Instant Insanity
# cube1 = [3, [1, 1, 1, 4], 2]
# cube2 = [1, [4, 2, 4, 3], 3]
# cube3 = [1, [3, 4, 1, 2], 2]
# cube4 = [4, [3, 1, 2, 4], 2]
# 2. Mutando
# cube1 = [3, [1, 2, 1, 4], 2]
# cube2 = [4, [4, 2, 2, 4], 3]
# cube3 = [1, [3, 4, 3, 2], 1]
# cube4 = [4, [4, 1, 2, 4], 2]
# 3. Drive Ya Crazy
cube1 = [6, [5, 3, 4, 2], 1]
cube2 = [6, [5, 3, 1, 2], 4]
cube3 = [6, [4, 3, 2, 1], 5]
cube4 = [6, [4, 3, 5, 1], 2]
cube5 = [6, [2, 3, 1, 5], 4]
cube6 = [6, [1, 3, 2, 4], 5]

cubes = [cube1, cube2, cube3, cube4, cube5, cube6]

start = perf_counter() 
insanity(cubes, 6)
end = perf_counter()

execution_time = (end - start)
print(execution_time)
