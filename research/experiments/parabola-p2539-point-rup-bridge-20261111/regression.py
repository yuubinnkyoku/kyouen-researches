"""Check assumption discharge against independent propagation and brute-force entailment."""
import argparse
from itertools import product
from pathlib import Path
import random
from verify import lift,HERE,sha,save


def conflict(clauses):
    clauses=list(map(set,clauses));assigned=set()
    while True:
        pending=[c for c in clauses if not c.intersection(assigned)]
        residual=[c-{-v for v in assigned} for c in pending]
        if any(not c for c in residual):return True
        units={next(iter(c)) for c in residual if len(c)==1}
        if any(-v in assigned or -v in units for v in units):return True
        units-=assigned
        if not units:return False
        assigned|=units


def rup(formula,clause):return conflict(list(formula)+[[-v] for v in clause])


def sat(formula,n):
    return any(all(any(bits[abs(v)-1]==(v>0) for v in c) for c in formula) for bits in product([False,True],repeat=n))


def closure(formula,n):
    f=[list(c) for c in formula];proof=[]
    candidates=[list(v for v in choice if v) for choice in product(*[[0,i,-i] for i in range(1,n+1)])]
    known={tuple(sorted(c)) for c in f}
    while True:
        progress=False
        for c in sorted(candidates,key=lambda c:(len(c),c)):
            key=tuple(sorted(c))
            if key in known or not rup(f,c):continue
            proof.append(c);f.append(c);known.add(key);progress=True
            if not c:return proof
        assert progress,'RUP closure unexpectedly stalled on an UNSAT tiny input'


def encode(proof):return ''.join(' '.join(map(str,c))+(' ' if c else '')+'0\n' for c in proof).encode('ascii')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists();tested=0;steps=0
    def exercise(f,n,assumption):
        nonlocal tested,steps
        child=f+[[assumption]]
        if sat(child,n):return
        proof=closure(child,n);raw=lift(encode(proof),assumption);current=[list(c) for c in f]
        for line in raw.decode('ascii').splitlines():
            c=list(map(int,line.split()))[:-1];assert rup(current,c) and not sat(f+[[-v] for v in c],n);current.append(c);steps+=1
        assert current[-1]==[-assumption] and not sat(f+[[assumption]],n);tested+=1
    base=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]
    for mask in range(1<<len(base)):
        f=[c for i,c in enumerate(base) if mask&(1<<i)]
        for assumption in [1,2]:exercise(f,2,assumption)
    rng=random.Random(2539);clauses=[list(v for v in c if v) for c in product([0,1,-1],[0,2,-2],[0,3,-3]) if any(c)]
    for _ in range(200):exercise(rng.sample(clauses,rng.randrange(len(clauses)+1)),3,1)
    guard=[[-1,2,3],[-1,2,-3],[-1,-2,3],[-1,-2,-3]];exercise(guard,3,1)
    assert lift(b'1 2 0\nd 2 0\n2 2 0\n0\n',1)==b'2 -1 0\n-1 0\n'
    rejected=[]
    for name,raw,assumption in [('missing-empty',b'2 0\n',1),('out-of-range',b'51571 0\n0\n',1),('missing-zero',b'2\n0\n',1),('invalid-assumption',b'0\n',0)]:
        try:lift(raw,assumption)
        except AssertionError:rejected.append(name)
        else:raise AssertionError(name)
    # Removing the discharging guard creates a false parent step on this SAT parent.
    assert not rup(guard,[2]) and rup(guard,[2,-1])
    save(a.output,dict(assumption_refutations_checked=tested,lifted_steps_checked=steps,rejected=rejected,missing_guard_rejected=True,
        verifier_source_sha256=sha((HERE/'verify.py').read_bytes()),source_sha256=sha(Path(__file__).read_bytes()),
        scope='Finite parent entailment and RUP checks using independent tiny propagation/brute force, plus malformed lifting controls. General assumption-discharge argument is separate.'))
    print('PASS',tested,'tiny assumption refutations,',steps,'lifted steps, 4 malformed inputs and missing-guard control')


if __name__=='__main__':main()
