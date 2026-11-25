"""Byte-level inventory of this frozen experiment and relevant live sources."""
from study import ROOT, EXP, OLD, BASE, sha, dump
import json
import sys
import hashlib
import subprocess

def main():
    paths={p for p in EXP.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and p.name!='artifact-manifest.json'}
    paths.update(OLD.parent/'scripts'/name for name in [
        'audit_saved_s6_targets.py','audit_saved_s7_s6_intersection.py','complete_class_local.py',
        'fixed_player_outcome.py','materialize_s7_witness_evidence.py','prepare_s7_witness_probe.py',
        'run_s7_witness_probe_local.py','verify_s7_witness_parent_win.py','verify_s7_witness_parent_win_v2.py',
        'n11_integer_circle_geometry.py'])
    front=ROOT/'research/experiments/n11-frontier-selection-20261005/scripts'
    paths.update(front/n for n in ['s5_evidence_policy.py','cache_aware_reply27_cover.py','merge_exact_s5_evidence.py'])
    paths.update([BASE,ROOT/'results/n11-s5-evidence-quarantine.json',
        ROOT/'cpp/solvers/kyouen_dfpn_root.cpp',ROOT/'cpp/solvers/kyouen_residual_micro.hpp',
        ROOT/'research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py',
        OLD/'post-5dfabf84-s7-witness-derived-s5.cache',
        OLD/'post-2199bcc8-s5-10448351135499552768-128-s7-witness-derived-s5.cache'])
    rows=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(paths)]
    dump(EXP/'output/artifact-manifest.json',dict(base_main='52239697a6a65b11889669725f8599604d53656f',
        files=rows,count=len(rows),bytes=sum(r['bytes'] for r in rows),missing=0,mismatched=0,
        historical_raw_hash_ledger='research/experiments/n11-strategy-redesign-20261010/output/history-sources.json',
        portable_certificate_verifier='research/experiments/n11-strategy-redesign-20261010/scripts/verify_certificate.py',
        note='The portable proof audit uses tracked raw copies; the broader historical ledger also records preserved .local originals.'))
    doc=json.loads((EXP/'output/artifact-manifest.json').read_text())
    assert all(sha(ROOT/r['path'])==r['sha256'] for r in doc['files'])
    print('ARTIFACT_INVENTORY_OK',doc['count'],doc['bytes'],'bytes; missing=0 mismatch=0')

if __name__=='__main__':
    if '--verify-index' in sys.argv:
        doc=json.loads((EXP/'output/artifact-manifest.json').read_text())
        tracked=set(subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines())
        assert all(r['path'] in tracked for r in doc['files'])
        bad=[r['path'] for r in doc['files'] if hashlib.sha256(subprocess.check_output(
            ['git','show',':'+r['path']],cwd=ROOT)).hexdigest()!=r['sha256']]
        assert not bad,bad
        print('STAGED_BYTE_HASHES_OK',len(doc['files']))
    else:
        main()
