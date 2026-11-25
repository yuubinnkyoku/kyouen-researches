#!/usr/bin/env python3
"""parity_lemmas.py — machine-complete proof of the Parity Lemmas for
cross-pair cover circles on the 3-row board, plus witness cross-check.

Master discriminant (see master_cover_identity.py):
  pair (α,a),(β,a), single (γ,g), target row d≠a; e1=γ−α, e2=γ−β.
    Δ_d = (e1+e2)^2 − 4(d−a)(d−g) + 4 e1 e2 (d−g)/(g−a)
Three canonical types arise on rows {0,1,2}:
  S: pair@outer, single@far-outer, covers middle:      Δ = e1²+e2²+4
  X: pair@middle, single@outer, covers other outer:    Δ = e1²+e2²−6e1e2−8
  Y: pair@outer, single@middle, covers other outer:    Δ = e1²+e2²+6e1e2−8

LEMMA S (both-odd impossible). e1,e2 both odd ⇒ Δ_S ≡ 1+1+4 ≡ 6 (mod 8),
  but squares mod 8 ∈ {0,1,4}. ∎ (complete: finite residue check)

LEMMA X/Y (both-even impossible). e1=2a, e2=2b ⇒ Δ = 4(a²+b²∓6ab−2).
  If Δ were a square s², then s even, s=2t, t² = a²+b²∓6ab−2.
  For (a,b) ∈ {(0,0),(0,1),(1,0),(1,1)} (mod 2) the RHS mod 4 is:
    (0,0): 0+0∓0−2 ≡ 2      (1,0): 1+0∓0−2 ≡ 3
    (0,1): 0+1∓0−2 ≡ 3      (1,1): 1+1∓2−2 ≡ 2   (−6ab≡+6ab≡2 mod 4)
  and quadratic residues mod 4 are {0,1}. Contradiction in every case. ∎
This script verifies both proofs by exhaustive residue enumeration (complete,
since the arguments are finite mod 8 / mod 4 case splits), and cross-checks the
21 published witnesses: no S-circle with both-odd e's, no X/Y-circle with
both-even e's exists among all witness pair-triples (all real circles).
"""
import json
from itertools import combinations

BASE = '/home/user/work/fastlane/q34'
def sqr_mod(m): return { (i*i) % m for i in range(m) }

def proof_S():
    # e1,e2 odd: e1=2u+1, e2=2v+1 → Δ mod 8 exhaustive over u,v mod 4
    residues = set()
    for u in range(4):
        for v in range(4):
            e1, e2 = 2*u+1, 2*v+1
            residues.add((e1*e1 + e2*e2 + 4) % 8)
    ok = residues <= ({6} if False else residues) and residues.isdisjoint(sqr_mod(8))
    return ok, sorted(residues)

def proof_XY(sign):
    # e1=2a, e2=2b → inner = a²+b²+sign*6ab−2 must be nonsquare mod 4 for all a,b parity
    bad = []
    for A in range(2):
        for B in range(2):
            val = (A*A + B*B + sign*6*A*B - 2) % 4
            if val in sqr_mod(4):
                bad.append(((A, B), val))
    return (len(bad) == 0), bad

def classify(a, g, d):
    """return delta-type 'S','X','Y', 'C' (target=single row), or None (target=pair row)"""
    if d == a:  return None
    if d == g:  return 'C'
    if (a, g, d) in ((0, 2, 1), (2, 0, 1)): return 'S'
    if (a, g, d) in ((1, 2, 0), (1, 0, 2)): return 'X'
    if (a, g, d) in ((0, 1, 2), (2, 1, 0)): return 'Y'
    raise AssertionError((a,g,d))

def delta_of(t, e1, e2):
    if t == 'S': return e1*e1 + e2*e2 + 4
    if t == 'X': return e1*e1 + e2*e2 - 6*e1*e2 - 8
    if t == 'Y': return e1*e1 + e2*e2 + 6*e1*e2 - 8
    if t == 'C': return (e1+e2)**2
    raise AssertionError(t)

def witness_crosscheck():
    import glob
    wdir = sys.argv[1] if len(sys.argv) > 1 else BASE + '/witall'
    wits = sorted(glob.glob(wdir + '/wit_3x*_4.witness.json'),
                  key=lambda s: int(s.split('3x')[1].split('_')[0]))
    wits = [{'m': json.load(open(f))['m'], 'coord': json.load(open(f))['coord']} for f in wits]
    viol = []
    n_circle = 0
    for w in wits:
        m = w['m']
        pts = [tuple(map(int, s.split(':'))) for s in w['coord'].split(',')]
        rows = {}
        for x, y in pts:
            rows.setdefault(y, []).append(x)
        for a in rows:
            for g in rows:
                if a == g: continue
                for (alpha, beta) in combinations(rows[a], 2):
                    for gamma in rows[g]:
                        e1, e2 = gamma - alpha, gamma - beta
                        for d in (0, 1, 2):
                            t = classify(a, g, d)
                            if t is None:  continue
                            delta = delta_of(t, e1, e2)
                            if delta < 0:  continue
                            r = int(delta ** 0.5)
                            if r*r != delta:  continue
                            # legal circle: hits row d in grid points
                            n_circle += 1
                            if t == 'S' and e1 % 2 == 1 and e2 % 2 == 1:
                                viol.append(('S-both-odd', m, (a,g,d), (alpha,beta,gamma)))
                            if t in ('X','Y') and e1 % 2 == 0 and e2 % 2 == 0:
                                viol.append((t+'-both-even', m, (a,g,d), (alpha,beta,gamma)))
    return n_circle, viol

def main():
    okS, resS = proof_S()
    okX, badX = proof_XY(-1)
    okY, badY = proof_XY(+1)
    print('LEMMA S (both-odd impossible for Δ=e1²+e2²+4):', 'PROVED' if okS else 'FAILED',
          'residues of Δ mod 8 =', resS, 'squares mod 8 =', sorted(sqr_mod(8)))
    print('LEMMA X (both-even impossible for Δ=e1²+e2²−6e1e2−8):', 'PROVED' if okX else 'FAILED', badX)
    print('LEMMA Y (both-even impossible for Δ=e1²+e2²+6e1e2−8):', 'PROVED' if okY else 'FAILED', badY)
    n, viol = witness_crosscheck()
    print(f'witness cross-check: {n} legal cross-pair circles scanned, parity violations: {len(viol)}')
    for v in viol[:10]:
        print('  VIOLATION', v)
    return 0 if (okS and okX and okY and not viol) else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
