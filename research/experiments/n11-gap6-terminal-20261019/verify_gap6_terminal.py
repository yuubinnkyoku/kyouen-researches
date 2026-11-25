#!/usr/bin/env python3
"""Independent exact terminal verifier: 18 new S8 WIN and 1 new S8 LOSS.

Only standard Python and integer determinant geometry; no previous verdict cache,
ILP solver, or search TT is trusted.  All S10 boundary states for the LOSS root
are solved to terminal, including unselected states, to validate the dual bound.
"""
import json
from pathlib import Path
from functools import lru_cache
from itertools import combinations
from verify_core import canonical, children, safe, points, next_player_wins_at_s10

HERE=Path(__file__).resolve().parent

def check(condition, message):
    if not condition: raise ValueError(message)

@lru_cache(None)
def terminal(h):
    m=int(h,16)
    check(m.bit_count()==10 and canonical(m)==m and safe(m), 'bad S10 board '+h)
    return next_player_wins_at_s10(m)

def verify(cert_path=None, verbose=True):
    c=json.loads(Path(cert_path or HERE/'gap6-terminal-cert.json').read_text())
    check(c['format']=='n11-s8-gap6-terminal-certificate-v1','bad format')
    roots=set()
    all_win_leaves=set()
    for row in c['s8_win_roots']:
        h=row['root']; root=int(h,16)
        check(h not in roots and root.bit_count()==8 and safe(root) and canonical(root)==root,'bad S8 WIN root')
        roots.add(h)
        w=int(row['s9_witness'],16)
        check(w in children(root),'S9 WIN witness not a legal child of S8 '+h)
        s10=children(w)
        check(set(row['s10_win_children'])=={f'{x:032x}' for x in s10},'incomplete S10 children of S9 '+h)
        for m in s10:
            key=f'{m:032x}'
            check(terminal(key)[0], 'S10 not WIN: '+key)
            all_win_leaves.add(key)
    check(len(roots)==18,'wrong WIN root count')
    loss=c['s8_loss_root']; root=int(loss,16)
    check(loss not in roots and root.bit_count()==8 and safe(root) and canonical(root)==root,'bad S8 LOSS root')
    obligations=children(root)
    check(len(obligations)==26 and set(c['s8_loss_s9_obligations'])=={f'{x:032x}' for x in obligations},'incomplete S9 LOSS obligations')
    selected={int(h,16) for h in c['s8_loss_s10_leaves']}
    check(len(selected)==15,'wrong selected leaf count')
    boundary=set().union(*(children(s) for s in obligations))
    check(len(boundary)==243 and selected<=boundary,'incomplete S10 boundary or illegal selected leaf')
    # Exhaustive Python terminal computation: verifies the universe of all eligible LOSS leaves.
    losses={p for p in boundary if not terminal(f'{p:032x}')[0]}
    check(len(losses)==43 and selected<=losses,'wrong S10 LOSS classification')
    check(all(children(s)&selected for s in obligations),'uncovered S9 obligation')
    weights=c['s8_loss_dual_weights_halves']
    ordered=[int(h,16) for h in c['s8_loss_s9_obligations']]
    check(len(weights)==26 and all(type(w) is int and w>=0 for w in weights) and sum(weights)==30,'invalid dual weights')
    for leaf in losses:
        weight=sum(w for s,w in zip(ordered,weights) if leaf in children(s))
        check(weight<=2,'dual inequality violated')
    parents={canonical(root^(1<<p)) for p in points(root)}
    check(len(parents)==8 and {f'{p:032x}' for p in parents}==set(c['new_s7_loss_parents']),'S7 parents mismatch')
    stats={'s8_win':len(roots),'s8_loss':1,'s9_loss_obligations':len(obligations),
        's10_loss_boundary':len(boundary),'s10_loss_candidates':len(losses),
        's10_loss_selected':len(selected),'minimum_selected':15,
        'distinct_s10_win_witnesses':len(all_win_leaves),
        'python_terminal_states_unique':sum(terminal(h)[1] for h in set(all_win_leaves)|{f'{p:032x}' for p in boundary}),
        's7_loss_parents':len(parents)}
    if verbose:print('PASS',json.dumps(stats,sort_keys=True))
    return stats

if __name__=='__main__':verify()
