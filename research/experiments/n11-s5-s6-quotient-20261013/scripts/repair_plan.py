"""Repair the old joint LOSS plan after two terminal-verified S5 verdicts.

Historical inputs remain unchanged. Every selected response and complete
S5 boundary is rebuilt from independent geometry and the explicit old
solver-trusted cache plus the two terminal-verified additions.
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]
OLD=ROOT/'research/experiments/n11-joint-s5-proof-planning-20261012/output'
sys.path.insert(0,str(ROOT/'research/experiments/n11-independent-exact-audit-20261010/scripts'))
sys.path.insert(0,str(ROOT/'research/experiments/n11-central-reply-frontier-20261012/scripts'))
from independent import Board
from analyze_central_reply_frontier import load_exact_s5_cache


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def key(mask):return mask&((1<<64)-1),mask>>64


def main():
    with gzip.open(OLD/'dependency-graph.json.gz','rt') as stream:g=json.load(stream)
    old=json.loads((OLD/'chosen-plans.json').read_text())['plans']['_joint_19_roots']
    new_verdicts={}
    sources={str(p.relative_to(ROOT)):sha(p) for p in (OLD/'dependency-graph.json.gz',OLD/'chosen-plans.json')}
    for index in (558600,209644):
        receipt_path=EXP/f'output/pilot-{index}-terminal-verification.json'
        receipt=json.loads(receipt_path.read_text())
        cert_path=EXP/f'output/pilot-{index}-terminal-dag.json.gz'
        assert receipt['trusted_leaves']==0 and sha(cert_path)==receipt['certificate_sha256']
        mask=g['s5_masks'][index][0]|g['s5_masks'][index][1]<<64
        assert str(mask)==receipt['root_mask']
        new_verdicts[index]=receipt['verdict']
        sources.update({str(p.relative_to(ROOT)):sha(p) for p in (receipt_path,cert_path)})
    losses={i for i,v in new_verdicts.items() if v==2}
    wins={i for i,v in new_verdicts.items() if v==1}
    cost=[set(c)-losses for c in g['s4_cost']]
    excluded={s for s,c in enumerate(g['s4_cost']) if wins.intersection(c)}
    old_entries={(e['first'],e['reply'],e['third']):e for e in old['groups']}
    choices={};options={};pairs={};changed=[]
    for root in g['roots']:
        if root['role']=='known-loss-baseline':continue
        first,reply=root['origin_first'],root['origin_reply']
        pairs[(first,reply)]=root['pair_mask'][0]|root['pair_mask'][1]<<64
        for r in root['thirds']:
            ident=(first,reply,r['third'])
            opts=[s for s in r['options'] if s not in excluded]
            assert opts, f'no optimistic response for {ident}'
            options[ident]=opts
            if ident in old_entries:
                s=old_entries[ident]['s4_class_index']
                if s not in excluded:choices[ident]=s
            else:
                free=[s for s in opts if not cost[s]]
                assert free
                choices[ident]=min(free)
    union=set().union(*(cost[s] for s in choices.values()))
    for ident in sorted(options):
        if ident not in choices:
            s=min(options[ident],key=lambda s:(len(cost[s]-union),len(cost[s]),s))
            choices[ident]=s;union|=cost[s]
            changed.append(dict(first=ident[0],reply=ident[1],third=ident[2],
                                old_s4=old_entries[ident]['s4_class_index'],new_s4=s,
                                new_elements_added=len(cost[s]-set(old['required_new_s5']))))
    assert not wins.intersection(union) and not losses.intersection(union)
    board=Board(11)
    cache=load_exact_s5_cache(board)
    for i,v in new_verdicts.items():cache[tuple(g['s5_masks'][i])]={'verdict':v}
    s5={g['s5_masks'][i][0]|g['s5_masks'][i][1]<<64:i for i in union}
    checked={}; entries=[]
    for pair,mask in pairs.items():
        expected=set(board.points(board.legal(mask)))
        actual={ident[2] for ident in choices if ident[:2]==pair}
        assert actual==expected and len(actual)==119
    for ident,s in sorted(choices.items()):
        mask=g['s4_masks'][s][0]|g['s4_masks'][s][1]<<64
        s3=pairs[ident[:2]]|1<<ident[2]
        # Verify one concrete legal fourth move producing the selected class.
        witness=next((p for p in board.points(board.legal(s3)) if board.canonical(s3|1<<p)==mask),None)
        assert witness is not None,(ident,s)
        if s not in checked:
            children=board.children(mask)
            assert all(cache.get(key(c),{}).get('verdict')!=1 for c in children),(s,'known WIN child')
            unknown={c for c in children if key(c) not in cache}
            expected={g['s5_masks'][i][0]|g['s5_masks'][i][1]<<64 for i in cost[s]}
            assert unknown==expected,(s,'incomplete cost boundary')
            checked[s]=len(children)
        entries.append(dict(first=ident[0],reply=ident[1],third=ident[2],fourth=witness,
                            s4_class_index=s,s4_mask=g['s4_masks'][s],unknown_s5_children=len(cost[s])))
    required=set().union(*(cost[e['s4_class_index']] for e in entries))
    assert required==union
    out=dict(schema='n11-joint-plan-after-terminal-pilots-v1',source_sha256=sources,
             old_union_size=old['union_size'],union_size=len(union),roots=len(pairs),
             third_moves_covered=len(entries),free_thirds=sum(e['unknown_s5_children']==0 for e in entries),
             excluded_s4_classes=sorted(excluded),resolved_s5_verdicts=new_verdicts,
             changed_choices=changed,groups=entries,required_new_s5=sorted(union),
             verification=dict(passed=True,checked_selected_s4=len(checked),complete_third_boundaries=len(pairs),
                               complete_s5_boundaries=len(checked),known_win_selected=0),
             trust='optimistic plan only: old exact-S5 leaves remain solver-trusted; two additions terminal-verified; all remaining required S5 verdicts UNKNOWN; not a root proof')
    (EXP/'output/repaired-joint-plan.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('groups','required_new_s5','source_sha256')},indent=2))

if __name__=='__main__':main()
