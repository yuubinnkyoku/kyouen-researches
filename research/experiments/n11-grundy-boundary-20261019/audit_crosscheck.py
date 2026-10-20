#!/usr/bin/env python3
"""Independently cross-check per-position C++/Python Grundy and state counts."""
import collections,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parent
python={}
for i in range(4):
    shard=json.loads((P/f'shard-{i}.json').read_text())
    assert shard['shard']==i and shard['shards']==4
    assert not (set(shard['s10'])&set(python))
    python.update(shard['s10'])
assert len(python)==3044
cpp={}
for line in (P/'s10-cpp-results.tsv').read_text().splitlines():
    mask,g,states,initial_moves=line.split('\t')
    assert mask not in cpp
    cpp[mask]=[int(g),int(states),int(initial_moves)]
assert set(cpp)==set(python)
assert all(python[k]==cpp[k][:2] for k in python)
assert sum(v[1] for v in python.values())==505832
assert collections.Counter(v[0] for v in python.values())=={0:896,1:294,2:426,3:384,4:220,5:684,6:140}
summary=json.loads((P/'summary.json').read_text())
assert summary['s10_memo_states_additive']==505832
assert {int(k):v for k,v in summary['s10_histogram'].items()}==dict(collections.Counter(v[0] for v in python.values()))
assert summary['s9_histogram']=={'1':111,'2':54,'3':69,'4':45,'5':9,'6':60,'7':39}
assert summary['s8_histogram']=={'0':18} and summary['empty_board']=='UNKNOWN'
print('PASS: 3044/3044 S10 positions: exact Grundy and memo states agree between Python and C++')
print('PASS: 387 S9 mex values and 18 S8 mex values checked in summary')
print('PASS: all 18 S8 roots Grundy 0; standard 11x11 empty-board outcome UNKNOWN')
