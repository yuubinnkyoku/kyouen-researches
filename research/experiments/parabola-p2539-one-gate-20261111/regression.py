"""Exercise actual extra-clause corruptions and the full18-variable exact-one truth table."""
import argparse
import gzip
import itertools
from pathlib import Path
from verify import HERE,inspect,save,sha


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();raw=gzip.decompress((HERE/'output/input.cnf.gz').read_bytes());cs,_,report=inspect(raw);bad=[]
    def reject(name,mutation):
        rows=[list(c) for c in cs];mutation(rows);body=(f'p cnf 51570 {len(rows)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in rows)).encode('ascii')
        try:inspect(body)
        except (AssertionError,KeyError,ValueError,TypeError):bad.append(name);return
        raise AssertionError('accepted '+name)
    reject('missing-exclusion',lambda c:c.pop(144546))
    reject('wrong-exclusion-sign',lambda c:c[144546].__setitem__(0,-c[144546][0]))
    reject('wrong-positive-gate',lambda c:c[144767].__setitem__(0,c[144767][0]+1))
    reject('wrong-at-most-sign',lambda c:c[-1].__setitem__(0,-c[-1][0]))
    reject('missing-at-most-pair',lambda c:c.pop())
    reject('repeated-at-most-pair',lambda c:c.__setitem__(-1,c[-2]))
    gate=report['gate'];variables=[36512+u for u in gate];index={v:i for i,v in enumerate(variables)}
    masks=[sum(1<<index[-lit] for lit in c) for c in cs[144768:]];assert len(masks)==153
    accepted=0
    for assignment in range(1<<18):
        actual=assignment!=0 and all(assignment&mask!=mask for mask in masks)
        assert actual==(assignment.bit_count()==1)
        accepted+=actual
    save(a.output,dict(corruptions_rejected=bad,exact_one_truth_assignments=1<<18,accepted_exact_one_assignments=accepted,source_sha256=sha(Path(__file__).read_bytes()),verifier_source_sha256=sha((HERE/'verify.py').read_bytes())))
    print('PASS',len(bad),'actual CNF corruptions;',1<<18,'exact-one assignments;',accepted,'accepted')


if __name__=='__main__':main()
