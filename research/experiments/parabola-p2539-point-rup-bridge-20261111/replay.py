"""Replay the combined parent-only RUP derivation using only the adopted proof and pinned parent."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from verify import HERE,TRIM,PARENT,PARENT_SHA,sha,save,run,derivation
from combine import bounded


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();assert not a.output.exists();m=json.loads((a.saved/'summary.json').read_bytes())
    parent=gzip.decompress(PARENT.read_bytes());proof=gzip.decompress((a.saved/'all-units.rup.gz').read_bytes())
    assert sha(parent)==PARENT_SHA==m['parent_input_sha256'] and sha(proof)==m['combined_raw_sha256']
    assert sha((HERE/'combine.py').read_bytes())==m['source_sha256']
    assert sha((HERE/'verify.py').read_bytes())==m['individual_driver_source_sha256']
    expected=json.loads((HERE.parent/'parabola-p2539-five-obstructions-20261111/output/certificate.json').read_bytes())['excluded']
    assert m['points']==expected and m['derived_units']==[-(36512+u) for u in expected] and len(expected)==60
    units=[]
    for line in proof.decode('ascii').splitlines():
        parts=line.split();deletion=parts[0]=='d';values=list(map(int,parts[1:] if deletion else parts));assert len(values)>=2 and values[-1]==0 and all(0<abs(v)<=51570 for v in values[:-1])
        if deletion:continue
        if len(values)==2:units.append(values[0])
    assert set(m['derived_units'])<=set(units) and proof.count(b'\n')==m['combined_lines']
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes());assert provenance['files']['drat-trim.c']==m['checker_source_sha256']
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-unit-replay-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';cp,pp=td/'parent.cnf',td/'all.rup';cp.write_bytes(parent);pp.write_bytes(proof)
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        r=bounded([str(exe),str(cp),str(pp),'-f','-U','-t','300'],330);assert not r['timed_out'] and derivation(r),r
    save(a.output,dict(parent_input_sha256=PARENT_SHA,proof_sha256=sha(proof),derived_points=expected,verified_parent_only_derivation=True,parent_unsat_claimed=False,
        source_sha256=sha(Path(__file__).read_bytes()),checker_source_sha256=m['checker_source_sha256'],scope='All60 negative units replayed without SAT library or child proof files. DERIVATION is deliberately distinguished from an UNSAT refutation.',**r))
    print('PASS parent-only combined RUP replay:60 units; no UNSAT claim')


if __name__=='__main__':main()
