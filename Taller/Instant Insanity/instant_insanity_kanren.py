from kanren import *
from kanren.constraints import neq
from itertools import combinations

from time import perf_counter

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

cubn1 = [var() , [var(), var(), var(), var()], var()]
cubn2 = [var() , [var(), var(), var(), var()], var()]
cubn3 = [var() , [var(), var(), var(), var()], var()]
cubn4 = [var() , [var(), var(), var(), var()], var()]
cubn5 = [var() , [var(), var(), var(), var()], var()]
cubn6 = [var() , [var(), var(), var(), var()], var()]
cuben = [cubn1, cubn2, cubn3, cubn4, cubn5, cubn6]

def flip(cube):
    return [cube[0], [cube[1][3], cube[1][0], cube[1][1], cube[1][2]], cube[2]]

def rotate(cube):
    return [cube[1][3], [cube[1][0], cube[0], cube[1][2], cube[2]], cube[1][1]]

def turn1(cube):
    return [cube[1][2], [cube[0], cube[1][1], cube[2], cube[1][3]], cube[1][0]]

def turn2(cube):
    return [cube[1][0], [cube[2], cube[1][1], cube[0], cube[1][3]], cube[1][2]]

def flips(cube, cubn):
    return lany (
        eq(cubn, cube),
        eq(cubn, flip(cube)),
        eq(cubn, flip(flip(cube))),
        eq(cubn, flip(flip(flip(cube))))
    )

def rotations(cube, cubn):       
    return lany(
        eq(cubn, cube),
        eq(cubn, rotate(cube)),        
        eq(cubn, rotate(rotate(cube))),
        eq(cubn, rotate(rotate(rotate(cube)))),
        eq(cubn, turn1(cube)),
        eq(cubn, turn2(cube))
    )

def move(cube, cubn):
    cubx = [var() , [var(), var(), var(), var()], var()]
    return lall(rotations(cube, cubx), flips(cubx, cubn))

def different(faces):
    return lall(neq(f1, f2) for f1,f2 in combinations(faces,2))

def differents(cuben):
    return lall(
       different((cuben[0][1][0], cuben[1][1][0], cuben[2][1][0], cuben[3][1][0], cuben[4][1][0], cuben[5][1][0])),
       different((cuben[0][1][1], cuben[1][1][1], cuben[2][1][1], cuben[3][1][1], cuben[4][1][1], cuben[5][1][1])),
       different((cuben[0][1][2], cuben[1][1][2], cuben[2][1][2], cuben[3][1][2], cuben[4][1][2], cuben[5][1][2])),
       different((cuben[0][1][3], cuben[1][1][3], cuben[2][1][3], cuben[3][1][3], cuben[4][1][3], cuben[5][1][3])),
    )

def insanity(cubes, cuben):
    return lall(
        # differents primero mejora notablemente el tiempo de ejecución
        differents(cuben),
        move(cubes[0], cuben[0]),
        move(cubes[1], cuben[1]),
        move(cubes[2], cuben[2]),
        move(cubes[3], cuben[3]),
        move(cubes[4], cuben[4]),
        move(cubes[5], cuben[5])
    )

start = perf_counter()             
solutions = run(0, cuben, insanity(cubes, cuben))

for i, cbs in enumerate(solutions, start=1):
    print('{:2d}. {}'.format(i,cbs))
end = perf_counter()

execution_time = (end - start)
print(execution_time)
