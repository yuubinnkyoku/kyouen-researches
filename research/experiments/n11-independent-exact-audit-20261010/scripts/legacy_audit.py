"""Replay the two withdrawn derivations' intermediate S6 dependencies."""
import csv
import json
from independent import Board,aggregate
from audit import ROOT,OUT,dump,key,digest

def main():
    board=Board(11)
    badparents,s7,sources=set(),{},[]
    old=ROOT/'research/experiments/n11-boundary-recovery-20261006/output'
    for name in ['post-5dfabf84-s7-witness-sources.json',
                 'post-2199bcc8-s5-10448351135499552768-128-s7-witness-sources.json']:
        doc=json.loads((old/name).read_text())
        sources.append(dict(path=(old/name).relative_to(ROOT).as_posix(),sha256=digest(old/name)))
        for row in doc['raw_sources']:
            p=ROOT/row['artifact_path']
            assert digest(p)==row['sha256']
            with p.open() as f:
                for raw in csv.reader(f):
                    if raw and raw[0]=='replay':
                        m=board.canonical(int(raw[9])+(int(raw[10])<<64))
                        s7[m]=int(raw[6])
            for a,b in row['affected_s6_parents']:
                badparents.add(a+(b<<64))
    rows=[]
    for m in sorted(badparents):
        ch=board.children(m)
        rows.append(dict(key=key(m),complete_children=len(ch),known_s7_loss=sum(s7.get(c)==2 for c in ch),
            correct_outcome=aggregate(6,[s7.get(c,0) for c in ch]),withdrawn_outcome=1))
    dump('legacy-intermediate-s6.json',dict(sources=sources,false_s6_win=len(rows),parents=rows))
    print('LEGACY_INTERMEDIATE_AUDIT',len(rows),'S6 claims require withdrawal')

if __name__=='__main__': main()
