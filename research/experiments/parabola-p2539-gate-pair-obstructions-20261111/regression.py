"""Exercise real certificate corruption and bounded hitting controls against brute force."""
import argparse
import copy
import itertools
import json
from pathlib import Path
from verify import HERE,audit,checker,save,sha
from produce import search


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();cert=json.loads((HERE/'output/certificate.json').read_bytes());audit(cert)
    bad=[]
    def reject(name,mutation):
        c=copy.deepcopy(cert);mutation(c)
        try:audit(c)
        except (AssertionError,KeyError,ValueError,TypeError):bad.append(name);return
        raise AssertionError('accepted '+name)
    reject('missing-pair',lambda c:c['entries'].pop())
    reject('repeated-pair',lambda c:c['entries'].__setitem__(1,c['entries'][0]))
    reject('wrong-gate',lambda c:c['gate'].__setitem__(0,61))
    reject('wrong-fixed',lambda c:c['fixed'].__setitem__(1,7))
    reject('wrong-budget',lambda c:c.__setitem__('max_deletions',6))
    reject('missing-exclusion',lambda c:c['excluded_pairs'].pop())
    positive=next(i for i,e in enumerate(cert['entries']) if e['status']=='HITTING_WITNESS')
    negative=next(i for i,e in enumerate(cert['entries']) if e['status']=='EXCLUDED' and sum(e['pair'])!=2539)
    reject('empty-hitting-witness',lambda c:c['entries'][positive].__setitem__('deletions',[]))
    reject('false-empty-refutation',lambda c:c['entries'][negative].__setitem__('refutation',dict(type='empty',edge=0)))
    pool=[frozenset(t) for k in range(3) for t in itertools.combinations(range(4),k)];tested=0
    for family in itertools.combinations(pool,3):
        for budget in range(3):
            expected=any(all(set(d)&r for r in family) for k in range(budget+1) for d in itertools.combinations(range(4),k))
            ok,data,_=search.solve(family,budget);assert ok==expected
            if ok:checker.check_hitting(family,budget,data,range(4))
            else:checker.check_tree(family,budget,data)
            tested+=1
    save(a.output,dict(corruptions_rejected=bad,brute_force_hitting_cases=tested,verifier_source_sha256=sha((HERE/'verify.py').read_bytes()),source_sha256=sha(Path(__file__).read_bytes())))
    print('PASS',len(bad),'real certificate corruptions rejected;',tested,'brute-force hitting comparisons')


if __name__=='__main__':main()
