# instant insanity problem AI
from time import perf_counter

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
    for m1 in move(cubes[0]):
        for m2 in move(cubes[1]):
            for m3 in move(cubes[2]):
                for m4 in move(cubes[3]):
                    
                    if  differents([m1[1][0], m2[1][0], m3[1][0], m4[1][0]]) \
                    and differents([m1[1][1], m2[1][1], m3[1][1], m4[1][1]]) \
                    and differents([m1[1][2], m2[1][2], m3[1][2], m4[1][2]]) \
                    and differents([m1[1][3], m2[1][3], m3[1][3], m4[1][3]]):
                        yield ([m1, m2, m3, m4])


# red   = 1
# white = 2
# blue  = 3
# green = 4

cube1 = [1, [1, 2, 3, 4], 1]
cube2 = [2, [2, 1, 4, 3], 3]
cube3 = [1, [1, 2, 2, 3], 4]
#versión open:
#cube3 = [1, [3, 2, 2, 1], 4]
cube4 = [3, [1, 2, 4, 4], 3]

cubes = [cube1, cube2, cube3, cube4]

start = perf_counter() 
i = insanity(cubes)
while True:
    try:
        print(next(i))
    except StopIteration:
        break
end = perf_counter()

execution_time = (end - start)
print(execution_time)