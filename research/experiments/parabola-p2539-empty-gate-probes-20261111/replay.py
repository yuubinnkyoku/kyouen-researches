"""Replay the adopted negative units and reduced positive gate from the augmented base alone."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import tempfile
from audit import HERE,sha,save
from verify_cases import TRIM,lifting,run


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    d=HERE/'proof-audit';m=json.loads((d/'summary.json').read_bytes());base=gzip.decompress((HERE/'output/base.cnf.gz').read_bytes())
    assert sha(base)==m['base_input_sha256'] and len(m['proved_points'])==8 and m['remaining_count']==18
    pieces=[];goals=[]
    for u in m['proved_points']:
        rec=json.loads((d/str(u)/'unit-rup.json').read_bytes());raw=gzip.decompress((d/str(u)/'negative-unit.rup.gz').read_bytes())
        assert rec['verified'] and sha(raw)==rec['proof_sha256'] and rec['base_input_sha256']==sha(base) and rec['derived_unit']==-(36512+u)
        assert raw.decode('ascii').splitlines()[-1]==f'{-(36512+u)} 0';pieces.append(raw);goals.append(-(36512+u))
    gate=gzip.decompress((d/'remaining-gate.rup.gz').read_bytes());receipt=json.loads((d/'remaining-gate.json').read_bytes())
    assert sha(gate)==receipt['proof_sha256'] and receipt['verified_derivation'] and not receipt['parent_unsat_claimed']
    assert list(map(int,gate.split()))==[36512+u for u in m['remaining_gate']]+[0]
    combined=b''.join(pieces)+gate
    for line in combined.decode('ascii').splitlines():
        values=list(map(int,line.split()));assert len(values)>=2 and values[-1]==0
    (a.output/'coverage.rup.gz').write_bytes(gzip.compress(combined,mtime=0))
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    with tempfile.TemporaryDirectory(prefix='p2539-gate-coverage-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';(td/'base.cnf').write_bytes(base);(td/'coverage.rup').write_bytes(combined)
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        r=run([str(exe),str(td/'base.cnf'),str(td/'coverage.rup'),'-f','-U','-t','150']);assert not r['timed_out'] and lifting.derivation(r)
    save(a.output/'receipt.json',dict(verified_base_only_derivation=True,parent_unsat_claimed=False,base_input_sha256=sha(base),proof_sha256=sha(combined),
        proof_lines=combined.count(b'\n'),derived_negative_units=goals,remaining_gate=m['remaining_gate'],source_sha256=sha(Path(__file__).read_bytes()),checker_source_sha256=provenance['files']['drat-trim.c'],
        scope='Eight negative units and positive18-point clause derived from the base already augmented with116 independent geometric exclusions. No original-parent-only or global UNSAT claim.',**r))
    print('REPLAY verified8 exclusions and positive18-point gate from augmented base; no global UNSAT')


if __name__=='__main__':main()
