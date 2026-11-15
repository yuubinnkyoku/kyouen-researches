#!/usr/bin/env python3
"""Second independent verifier for the cost-72c WIN7 certificates (2026-11-15).
Pure Python stdlib, exact-integer Bareiss 4x4 determinants of [x^2+y^2,x,y,1]
(zero det = concyclic or collinear quadruple). No repo engine import.

Semantics (from the certificate header 'original_first_WIN7 second_to_move_LOSS'):
the player to move at the 7-stone root is the LOSER; the original first player
(the winner) answers. For every loser first move at the root the winner follows
the certificate's recorded move; the loser then expands ALL legal replies with
incremental exact forbidden masks. Every loser branch must end with the loser
stuck, and the union of consumed winner rows must equal the full strategy."""
import sys, json

XR=[i%11 for i in range(121)]
YR=[i//11 for i in range(121)]
QR=[XR[i]*XR[i]+YR[i]*YR[i] for i in range(121)]

def det4rows(a,b,c,d):
    mm=[[QR[a],XR[a],YR[a],1],[QR[b],XR[b],YR[b],1],[QR[c],XR[c],YR[c],1],[QR[d],XR[d],YR[d],1]]
    prev=1
    for k in range(3):
        if mm[k][k]==0:
            for r in range(k+1,4):
                if mm[r][k]!=0:
                    mm[k],mm[r]=mm[r],mm[k]; break
            else:
                return 0
        for i in range(k+1,4):
            for j in range(k+1,4):
                mm[i][j]=(mm[i][j]*mm[k][k]-mm[i][k]*mm[k][j])//prev
        prev=mm[k][k]
    return mm[3][3]

_tmask={}
def triple_mask(a,b,c):
    key=tuple(sorted((a,b,c)))
    m=_tmask.get(key)
    if m is not None: return m
    mask=0
    for d in range(121):
        if det4rows(a,b,c,d)==0: mask|=1<<d
    _tmask[key]=mask
    return mask

def cells_of(occ):
    return [i for i in range(121) if (occ>>i)&1]

def mask_over(cells):
    F=0; n=len(cells)
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                F|=triple_mask(cells[i],cells[j],cells[k])
    return F

def main(path, expect_mobility, expect_rows):
    lines=[l for l in open(path).read().splitlines() if l.strip()]
    assert lines[0]=="n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS", lines[0]
    assert lines[1].split()[0]=="root"
    root_hex=lines[1].split()[1]
    root=int(root_hex,16)
    stones=cells_of(root)
    assert len(stones)==7, len(stones)
    strat={}
    prev=""
    for l in lines[2:]:
        h,m=l.split(); strat[h]=int(m)
        assert h>prev, "rows not sorted"
        prev=h
    assert len(strat)==expect_rows, (len(strat),expect_rows)
    rootF=mask_over(stones)
    rootocc=root
    rootlegal=[p for p in range(121) if not (rootocc>>p)&1 and not (rootF>>p)&1]
    assert len(rootlegal)==expect_mobility, (len(rootlegal),expect_mobility)
    consumed=set(); terminals=set(); states=0
    sys.setrecursionlimit(100000)
    def winner_turn(occ, F):
        nonlocal states
        states+=1
        key=f"{occ:032x}"
        m=strat.get(key)
        assert m is not None, f"missing strategy row {key}"
        assert not (occ>>m)&1 and not (F>>m)&1, f"illegal winner move {m} at {key}"
        consumed.add(key)
        pre=cells_of(occ)
        # after the winner plays m, the loser's forbidden set grows by all
        # triples (m, a, b) over stones already on the board
        F2=F
        n=len(pre)
        for i in range(n):
            for j in range(i+1,n):
                F2|=triple_mask(pre[i],pre[j],m)
        occ2=occ|(1<<m)
        rep=[p for p in range(121) if not (occ2>>p)&1 and not (F2>>p)&1]
        if not rep:
            terminals.add(bin(occ2).count("1")); return
        cells2=pre+[m]
        n2=len(cells2)
        for p in rep:
            F3=F2
            for i in range(n2):
                for j in range(i+1,n2):
                    F3|=triple_mask(cells2[i],cells2[j],p)
            winner_turn(occ2|(1<<p), F3)
    for mv in rootlegal:
        # loser plays mv at the root; winner answers from root|mv
        add=0
        for i in range(7):
            for j in range(i+1,7):
                add|=triple_mask(stones[i],stones[j],mv)
        winner_turn(rootocc|(1<<mv), rootF|add)
    assert consumed==set(strat.keys()), (len(consumed),len(strat))
    result={
      "cert": path.split("/")[-1],
      "verdict": "WIN7 certificate independently verified (Bareiss replay, all loser replies expanded)",
      "root_hex": root_hex, "root_stones": 7,
      "root_loser_mobility": len(rootlegal), "subroots_passed": len(rootlegal),
      "strategy_rows": len(strat), "consumed_rows": len(consumed),
      "union_missing": len(set(strat)-consumed), "union_extra": len(consumed-set(strat)),
      "terminal_stone_range": sorted(terminals),
      "visited_winner_states": states,
    }
    print(json.dumps(result))

if __name__=="__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
