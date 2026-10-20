"""Audit complete Grundy distributions and maxima from two independent C++ solvers."""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent

def parse(path):
    rows={}
    for line in (HERE/path).read_text().splitlines():
        m=re.match(r'n=(\d+) patterns=(\d+) distinct=(\d+) max=(-?\d+) hist=([^ ]*)',line)
        assert m, (path,line)
        n,a,b,g,h=m.groups()
        distribution={int(k):int(v) for k,v in re.findall(r'(\d+):(\d+),',h)}
        assert sum(distribution.values())==int(b)
        assert (max(distribution) if distribution else -1)==int(g)
        rows[int(n)]=(int(a),int(b),int(g),distribution)
    return rows

first=parse('all_patterns_results.txt')
second=parse('independent_results.txt')
assert first==second
assert set(first)==set(range(4,21))
assert sum(x[0] for x in first.values())==507549
assert sum(x[1] for x in first.values())==469368
assert max(x[2] for x in first.values())==6
assert first[12][3][6]==240
assert all(x[3].get(6,0)==0 for n,x in first.items() if n!=12)
print('PASS: all 17 rows, every Grundy histogram, 469368 games, maximum 6, n12 g6 exactly 240')
