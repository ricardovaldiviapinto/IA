# logic puzzles library
# author: Ricardo Valdivia
# date: 07-02-2023

from kanren import *
from kanren.constraints import neq
from itertools import combinations, product


#funciones posicionales
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


# funciones differents
def clean_var(p):
    for i in p:
        for j in i:
            if isvar(j): return(False)
    return(True)

def different(l, par, idx):
    lcache = tuple(tuple(r[i] for i in idx) for r in l)

    return lall(neq(p,c) for p in par for c in lcache)

def differents(l, d):
    par = tuple(tuple(product(m, n)) for m, n in combinations(d, 2))
    idx = tuple(combinations((i for i in range(len(d))),2))
    
    # limpia atributos no instanciados
    lst = tuple((p, i) for p, i in zip(par, idx) if clean_var(p))

    return lall(different(l, p, i) for p, i in lst)
