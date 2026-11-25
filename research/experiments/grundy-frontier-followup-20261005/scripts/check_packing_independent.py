#!/usr/bin/env python3
"""Separate arithmetic checks of the q57 packing proof; no SAT inference."""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib,json
if not __debug__:
    raise SystemExit('Assertions are required.')
ROOT=Path(__file__).resolve().parents[4]
BASE=Path(__file__).resolve().parents[1]
PROOF=ROOT/'research/experiments/q57-frontier-followup-20261005/proof.md'

def main():
    # Direct square-residue membership, without importing the proposed verifier.
    square_residues=set(pow(x,2,9) for x in range(9))
    feasible=[]
    for c in range(9):
        for n in range(9):
            if all((n-pow(2*y+c,2,9))%9 in square_residues for y in range(5)):
                feasible.append([c,n])
    assert feasible==[]
    chord_rows=[]
    for r in range(1,101):
        chains=[]
        for j in range(1,r//2+1):
            lo=j-1;hi=r-j
            chain=[(lo,b) for b in range(lo+1,hi+1)]
            chain += [(a,hi) for a in range(lo+1,hi)]
            assert len(chain)==2*r-4*j+1
            assert all(a<=c and b<=d and (a,b)!=(c,d)
                       for (a,b),(c,d) in zip(chain,chain[1:]))
            chains.append(chain)
        assert sorted(p for c in chains for p in c)==list(combinations(range(r),2))
        profile=Counter(a+b for a,b in combinations(range(r),2))
        formula=(2*r**3-3*r**2+4*r-3*(r%2))//12
        direct=sum(c*c for c in profile.values())
        weighted=sum((2*j-1)*(2*r-4*j+1) for j in range(1,r//2+1))
        assert formula==direct==weighted
        # Equality of AP sum-group odd weights is inspected explicitly.
        for s,c in profile.items():
            indices=[j for j,chain in enumerate(chains,1) if any(a+b==s for a,b in chain)]
            assert indices==list(range(1,c+1))
            assert sum(2*j-1 for j in indices)==c*c
        chord_rows.append({'r':r,'sharp_energy':formula})
    maxima=[]
    for b in range(6):
        value,x,y=max((b+2*x+y,x,y) for x in range(175) for y in range(111)
                      if 3*x+y<=174 and y<=22*b)
        maxima.append({'target_stones':b,'unavailable_maximum':value,'x':x,'y':y})
    assert [r['unavailable_maximum'] for r in maxima]==[116,124,132,141,149,157]
    assert (comb(24,2)-3)//12==22
    assert 3*152<=2*174+110<3*153
    out={'status':'VERIFIED','kind':'independent arithmetic checks plus separately documented proof review',
        'mod9_pairs':81,'feasible_five_row_discriminants':feasible,
        'general_energy_arithmetic_progressions':chord_rows,'integer_packing_maxima':maxima,
        'five_rich_line_bound':22,'stabilization_upper_bound':158,
        'proof_sha256':hashlib.sha256(PROOF.read_bytes()).hexdigest(),
        'scope':'No square-board Grundy inference; finite checks do not replace the universal chain/inversion/Melchior proofs.'}
    (BASE/'output/packing-independent-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='general_energy_arithmetic_progressions'}))
if __name__=='__main__':main()
