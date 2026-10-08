"""Exact integer circle geometry on an 11x11 board."""
from functools import lru_cache
from itertools import combinations

N = 11
XY = tuple((v % N, v // N) for v in range(121))
Q = tuple(x*x + y*y for x,y in XY)

def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
           -a[1]*(b[0]*c[2]-b[2]*c[0])
           +a[2]*(b[0]*c[1]-b[1]*c[0]))
