"""Create/check a byte-level inventory of this experiment and changed source."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]
MANIFEST=EXP/'output/artifact-manifest.json'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if args.check:
        doc=json.loads(MANIFEST.read_text())
        for r in doc['artifacts']:
            p=ROOT/r['path']
            if not p.is_file() or sha(p)!=r['sha256']: raise ValueError(('hash mismatch',r['path']))
        print('ARTIFACT_HASH_OK',len(doc['artifacts']))
        return
    files={p for p in EXP.rglob('*') if p.is_file() and p!=MANIFEST and '__pycache__' not in p.parts}
    # Pin changed implementation without including generated knowledge views.
    changed=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
    changed+=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines()
    files.update(ROOT/p for p in changed if p.endswith(('.py','.cpp','.yml','.hpp')))
    files.add(ROOT/'cpp/solvers/n11_s5_quarantine.hpp')
    files.add(ROOT/'results/n11-s5-evidence-quarantine.json')
    doc=dict(schema='n11-independent-audit-artifacts-v1',
        artifacts=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(files)])
    MANIFEST.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('ARTIFACT_MANIFEST_WRITTEN',len(files))

if __name__=='__main__':main()
