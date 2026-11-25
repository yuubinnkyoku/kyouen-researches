from itertools import combinations

def safe6(m):
    s=[{a+b,a+c,b+c} for a,b,c in combinations(range(m),3)]
    return sum(not (x&y) for x in s for y in s)

if __name__=='__main__':
    print([(m,safe6(m)) for m in range(3,13)])
