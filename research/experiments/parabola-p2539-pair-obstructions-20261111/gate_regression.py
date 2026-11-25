"""Exhaust the counting argument for hitting an originally empty pair on small domains."""
import argparse
import json
from pathlib import Path
from verify import HERE,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    checked=0;improvements=0
    for p in [7,11]:
        fixed={0,1,p-1};free=sorted(set(range(p))-fixed)
        sets=[fixed|{v for i,v in enumerate(free) if mask&(1<<i)} for mask in range(1<<len(free))]
        for seed in sets:
            e={u for u in range(1,p) if u not in seed and p-u not in seed}
            for t in sets:
                if [i for i in range(1,(p+1)//2) if i in t and p-i in t]!=[1]:continue
                added=t-seed;deleted=seed-t;single=added-e
                assert {p-u for u in single}<=deleted and len(single)==len({p-u for u in single})
                if len(t)>len(seed):assert t&e and len(added)>len(deleted);improvements+=1
                checked+=1
    receipt=json.loads((HERE/'gate-output/receipt.json').read_bytes())
    assert receipt['verified_parent_only_derivation'] and not receipt['parent_unsat_claimed'] and len(receipt['empty_pair_points'])==26
    save(a.output,dict(small_seed_target_cases=checked,improvement_cases=improvements,source_sha256=sha(Path(__file__).read_bytes()),gate_source_sha256=sha((HERE/'empty_gate.py').read_bytes()),
        scope='Finite exhaustive confirmation of the mirror injection and necessary empty-pair addition; the universal counting proof and actual26-literal RUP check remain separate.'))
    print('PASS',checked,'seed/target pairs,',improvements,'strict improvements require an empty-pair point')


if __name__=='__main__':main()
