"""Explicitly separate RAT-only acceptance from RUP, and test missing assumption guards."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from verify import HERE,TRIM,sha,save,run,derivation


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists()
    provenance=json.loads((TRIM/'vendor/provenance.json').read_bytes())
    for name,digest in provenance['files'].items():assert sha((TRIM/'vendor'/name).read_bytes())==digest
    rows=[]
    with tempfile.TemporaryDirectory(prefix='p2539-native-controls-') as temporary:
        td=Path(temporary);exe=td/'trim.exe';cp,pp=td/'input.cnf',td/'proof.drat'
        subprocess.run(['gcc',str(TRIM/'vendor/drat-trim.c'),*provenance['build_flags'],'-o',str(exe)],check=True,timeout=60)
        # Fresh positive3 has no negative occurrences, so is vacuously RAT; F does not entail3.
        cp.write_bytes(b'p cnf 3 1\n1 2 0\n');pp.write_bytes(b'3 0\n')
        for only_rup,expected in [(False,True),(True,False)]:
            cmd=[str(exe),str(cp),str(pp),'-f','-t','30']+(['-U'] if only_rup else [])
            r=run(cmd);assert derivation(r)==expected,(only_rup,r)
            rows.append(dict(name='fresh-variable-RAT-only',rup_only=only_rup,expected_derivation=expected,**r))
        cp.write_bytes(b'p cnf 3 4\n-1 2 3 0\n-1 2 -3 0\n-1 -2 3 0\n-1 -2 -3 0\n')
        for name,proof,expected in [('guarded-lift',b'2 -1 0\n-1 0\n',True),('guard-omitted',b'2 0\n0\n',False)]:
            pp.write_bytes(proof);r=run([str(exe),str(cp),str(pp),'-f','-U','-t','30']);assert derivation(r)==expected,(name,r)
            rows.append(dict(name=name,rup_only=True,expected_derivation=expected,**r))
    save(a.output,dict(cases=rows,checker_source_sha256=provenance['files']['drat-trim.c'],source_sha256=sha(Path(__file__).read_bytes()),
        scope='Fresh-variable unit is accepted as RAT without-U and rejected with-U; missing assumption guard is rejected while its lifted proof is accepted.'))
    print('PASS explicit RAT/RUP distinction and actual guarded/missing-guard native controls')


if __name__=='__main__':main()
