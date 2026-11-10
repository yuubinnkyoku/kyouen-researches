"""Check the incoming 1303-point model and bind its fresh geometry receipt."""
import argparse
import gzip
import json
from pathlib import Path
from audit import HERE, sha, save


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--geometry',type=Path,required=True)
    args=ap.parse_args()
    directory=HERE.parent/'parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000'
    candidate=(directory/'candidate.txt').read_bytes()
    values=list(map(int,candidate.split()))
    assert values[:2]==[2647,1303] and values[2:]==sorted(set(values[2:]))
    model_raw=(directory/'model.json').read_bytes()
    model=json.loads(model_raw)['signed_model']
    cnf=gzip.decompress((directory/'input.cnf.gz').read_bytes())
    lines=cnf.decode('ascii').splitlines()
    nv,nc=map(int,lines[0].split()[2:])
    assert [nv,nc]==[32569,117652] and len(lines)-1==nc
    assert len(model)==nv and {abs(v) for v in model}==set(range(1,nv+1))
    positive={v for v in model if v>0}
    assert all(any((v>0)==(abs(v) in positive) for v in map(int,line.split()[:-1])) for line in lines[1:])
    chosen={0,1323,1324}|{i for i in range(1,1323) if i in positive}|{2647-i for i in range(1,1323) if 1323+i in positive}
    assert sorted(chosen)==values[2:]
    receipt_raw=args.geometry.read_bytes()
    receipt=json.loads(receipt_raw)
    assert receipt['returncode']==0 and receipt['candidate_input_sha256']==sha(candidate)
    assert receipt['verifier_source_sha256']==sha((HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp').read_bytes())
    previous=set(map(int,(HERE.parent/'parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/candidate.txt').read_bytes().split()[2:]))
    result=dict(size=1303,variables=nv,clauses=nc,all_model_clauses_satisfied=True,decoded_points_match=True,
                candidate_sha256=sha(candidate),model_sha256=sha(model_raw),input_cnf_sha256=sha(cnf),
                geometry_receipt_sha256=sha(receipt_raw),removed_from_previous1302=len(previous-chosen),
                added_to_previous1302=len(chosen-previous),source_sha256=sha(Path(__file__).read_bytes()),
                scope='Stored incoming model evaluation and fresh independent geometry binding. No new SAT search or maximum-size claim.')
    save(args.output,result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
