"""Combine accepted point derivations while deleting discharged auxiliary clauses."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
import time
from verify import HERE,TRIM,PARENT,PARENT_SHA,sha,save,derivation


def bounded(cmd,timeout):
    start=time.monotonic()
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
        return dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False,elapsed_seconds=time.monotonic()-start)
    except subprocess.TimeoutExpired as exc:
        dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
        return dict(returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True,elapsed_seconds=time.monotonic()-start)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    parent=gzip.decompress(PARENT.read_bytes());assert sha(parent)==PARENT_SHA
    original={tuple(sorted(map(int,l.split()[:-1]))) for l in parent.decode('ascii').splitlines()[1:]}
    points=json.loads((HERE.parent/'parabola-p2539-five-obstructions-20261111/output/certificate.json').read_bytes())['excluded']
    out=[];plain=[];deletions=0
    for u in points:
        d=a.saved/str(u);rec=json.loads((d/'receipt.json').read_bytes());raw=gzip.decompress((d/'lifted.rup.gz').read_bytes())
        assert rec['verified_parent_only_derivation'] and rec['derived_unit']==-(36512+u) and rec['parent_input_sha256']==PARENT_SHA
        assert sha(raw)==rec['lifted_raw_sha256'] and sha((HERE/'verify.py').read_bytes())==rec['driver_source_sha256']
        plain.append(raw);out.append(raw)
        for line in raw.decode('ascii').splitlines():
            vals=list(map(int,line.split()));assert vals[-1]==0
            if len(vals)>2 and tuple(sorted(vals[:-1])) not in original:
                out.append(('d '+line+'\n').encode('ascii'));deletions+=1
    failed=b''.join(plain);(a.output/'plain-attempt.rup.gz').write_bytes(gzip.compress(failed,mtime=0))
    save(a.output/'plain-attempt.json',dict(status='TIMEOUT',time_limit_seconds=120,exception='subprocess.TimeoutExpired',proof_sha256=sha(failed),
        source_driver='verify.py',scope='Preserved byte reconstruction of the earlier plain concatenation that exceeded120 seconds; no combined acceptance receipt was produced.'))
    proof=b''.join(out);(a.output/'all-units.rup.gz').write_bytes(gzip.compress(proof,mtime=0))
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-unit-clean-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';cp,pp=td/'parent.cnf',td/'all.rup';cp.write_bytes(parent);pp.write_bytes(proof)
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        r=bounded([str(exe),str(cp),str(pp),'-f','-U','-t','300'],330);save(a.output/'combined.json',r)
        assert not r['timed_out'] and derivation(r),r
    save(a.output/'summary.json',dict(points=points,derived_units=[-(36512+u) for u in points],all_verified=True,parent_input_sha256=PARENT_SHA,
        combined_raw_sha256=sha(proof),combined_lines=proof.count(b'\n'),deletion_lines=deletions,source_sha256=sha(Path(__file__).read_bytes()),
        individual_driver_source_sha256=sha((HERE/'verify.py').read_bytes()),checker_source_sha256=provenance['files']['drat-trim.c'],
        scope='All60 individually accepted parent-only unit derivations combined with deletions of discharged non-parent non-unit clauses. DERIVATION, not an UNSAT refutation.'))
    print('PASS cleaned combined parent-only RUP derivation:60 units,',deletions,'deletions')


if __name__=='__main__':main()
