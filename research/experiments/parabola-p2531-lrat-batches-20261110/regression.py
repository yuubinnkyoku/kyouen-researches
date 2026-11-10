"""Reject duplicate/covered work and keep UNKNOWN out of collected coverage."""
import argparse
import json
from pathlib import Path
import tempfile
from audit import parse_ds, validate_plan, collect, save, sha

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    prior = json.loads((HERE.parent/'parabola-p2531-lrat-20261110/output/batch86-100/coverage.json').read_text())
    ds = parse_ds('102-120,122-140')
    assert len(ds)==38 and len(validate_plan(prior,ds))==162
    controls = [lambda:validate_plan(prior,[102,102]),lambda:validate_plan(prior,[101]),
                lambda:validate_plan(prior,[0]),lambda:validate_plan(prior,[1266]),
                lambda:validate_plan(dict(prior,p=2207),[102]),
                lambda:validate_plan(dict(prior,verified_union_count=163),[102]),
                lambda:parse_ds('105-103')]
    for check in controls:
        try:
            check()
        except AssertionError:
            pass
        else:
            raise AssertionError('invalid plan accepted')
    with tempfile.TemporaryDirectory(prefix='p2531-collector-controls-') as directory:
        directory = Path(directory)
        save(directory/'plan.json',dict(prior_verified_d=[1],requested_d=[2,3,4,5],
             source_sha256='synthetic-control',prior_coverage_path='unused',prior_coverage_sha256='unused'))
        for d,verified,solver,rc in [(2,True,'UNSAT',0),(3,False,'UNKNOWN',0),(5,False,'UNSAT',1)]:
            case = directory/f'd{d}'
            case.mkdir()
            save(case/'result.json',dict(d=d,source_sha256='synthetic-control',verified=verified,solver=solver,lrat=dict(returncode=rc)))
        result = collect(directory)
        assert result['verified_d_union']==[1,2] and result['pending_d']==[4]
        assert result['failed_or_unknown_d']==[3,5]
        try:
            collect(directory)
        except FileExistsError:
            pass
        else:
            raise AssertionError('existing coverage overwritten')
    save(args.output,dict(valid_fresh_cases=38,rejected_invalid_plans=len(controls),
         collector_unknown_and_failure_excluded=True,collector_pending_preserved=True,
         existing_coverage_overwrite_rejected=True,source_sha256=sha(Path(__file__).read_bytes()),
         scope='Synthetic controller/collector controls only; no SAT or geometric proof.'))
    print('PASS 7 invalid plans and collector UNKNOWN/failure/pending/overwrite controls')


if __name__=='__main__':
    main()
