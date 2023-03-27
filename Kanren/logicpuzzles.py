# logic puzzles library
# author: Ricardo Valdivia
# date: 07-02-2023

from kanren import *
from kanren.constraints import neq
from itertools import combinations, product


# FUNCIONES POSICIONALES

def left_of(l, p, q, n=1):
    return membero((p, q), list(zip(l, l[n:])))

def right_of(l, p, q, n=1):
    return left_of(l, q, p, n)

def next_to(l, p, q, n=1):
    return lany(left_of(l, p, q, n), left_of(l, q, p, n))

def somewhat_left_of(l, p, q):
    return membero((p,q), list(combinations(l,2)))

def somewhat_right_of(l, p, q):
    return somewhat_left_of(l, q, p)


# FUNCIONES DIFFERENTS

# clean_var: verifica que cada componente en la lista de listas "p" no incluya variables no instanciadas 
def clean_var(p):
    for i in p:
        for j in i:
            if isvar(j): return(False)
    return(True)

# different: compara (neq) cada pareja en la lista "par" con sus correspondientes en la lista "l"
# indexados por la pareja de indices del parámetro "idx"
def different(l, par, idx):
    return lall(neq(p, (r[idx[0]], r[idx[1]])) for p in par for r in l)

# differents: verifica que cada atributo en la lista de listas "d" corresponda a un sujeto diferente
def differents(l, d):
    par = tuple(tuple(product(m, n)) for m, n in combinations(d, 2))
    idx = tuple(combinations((i for i in range(len(d))),2))
    
    return lall(different(l, p, i) for p, i in zip(par, idx) if clean_var(p))
