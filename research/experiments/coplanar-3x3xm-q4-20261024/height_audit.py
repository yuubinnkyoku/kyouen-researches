"""Full height-assignment audit for 3x3x3 and 3x3x4; m=5 witness."""
from itertools import combinations, permutations, product
columns=list(product(range(3), repeat=2))
perms=list(permutations(range(4)))
sgn={p: (-1 if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 else 1) for p in perms}
def det4(points):
    a=[(*p,1) for p in points]
    return sum(sgn[p]*a[0][p[0]]*a[1][p[1]]*a[2][p[2]]*a[3][p[3]] for p in perms)
def audit(m):
    constraints=[]
    for cols in combinations(range(9),4):
        bad=set()
        for heights in product(range(m),repeat=4):
            if det4([(*columns[i],z) for i,z in zip(cols,heights)])==0:
                bad.add(heights)
        constraints.append((cols,bad))
    safe=0
    for heights in product(range(m),repeat=9):
        if all(tuple(heights[i] for i in cols) not in bad for cols,bad in constraints):
            safe+=1
    print(f'm={m} all_9_column_assignments={m**9} safe_9={safe}')
    return safe
assert audit(3)==0
assert audit(4)==0
witness=(0,0,1,2,4,1,3,1,0)
assert all(det4([(*columns[i],witness[i]) for i in cols])!=0 for cols in combinations(range(9),4))
print('m=5 explicit_9_stone_witness:', [(columns[i],witness[i]) for i in range(9)])
