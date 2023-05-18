# instant insanity problem AI
from time import perf_counter
from itertools import product

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

def differents(l):
    return len(set(l)) == len(l)

def insanity(cubes):
    cubn1 = [m1 for m1 in move(cubes[0])]
    cubn2 = [m2 for m2 in move(cubes[1])]
    cubn3 = [m3 for m3 in move(cubes[2])]
    cubn4 = [m4 for m4 in move(cubes[3])]
    cubn5 = [m5 for m5 in move(cubes[4])]
    cubn6 = [m6 for m6 in move(cubes[5])]
    
    for state in product(cubn1, cubn2, cubn3, cubn4, cubn5, cubn6):                
        if  differents([state[0][1][0], state[1][1][0], state[2][1][0], state[3][1][0], state[4][1][0], state[5][1][0]]) \
        and differents([state[0][1][1], state[1][1][1], state[2][1][1], state[3][1][1], state[4][1][1], state[5][1][1]]) \
        and differents([state[0][1][2], state[1][1][2], state[2][1][2], state[3][1][2], state[4][1][2], state[5][1][2]]) \
        and differents([state[0][1][3], state[1][1][3], state[2][1][3], state[3][1][3], state[4][1][3], state[5][1][3]]) :
            yield (state)

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
for i, cbs in enumerate(insanity(cubes), start=1):
    print('{:2d}. {}'.format(i,cbs))
end = perf_counter()

execution_time = (end - start)
print(execution_time)