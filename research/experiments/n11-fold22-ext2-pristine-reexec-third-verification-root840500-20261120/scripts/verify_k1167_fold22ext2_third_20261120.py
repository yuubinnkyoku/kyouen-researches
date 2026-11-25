#!/usr/bin/env python3
"""Third verification of the published K1167 fold22 external second verification.

K1167 = external second verification of the published fold22 (K1132) receipt
fold (experiment dir n11-fold22-external-second-verification-root840500-20261120,
part1 commit 4eb6cbf05, published by another lane).  This harness re-executes,
from published bytes only, everything needed to reproduce the K1167 audit
byte-identically:

  pin          fetch the 5 published K1167 experiment files at the pinned
               commit and verify their SHA-256 pins fail-closed
  reconstruct-w1/-w2  run the published reconstruct_inputs.py twice at its
               fixed Git ref, building two independent W trees and two
               fold22 publication byte copies
  wcmp         byte-compare the two W trees (55 pins + 4 chain machines,
               excluding the path-bearing reconstruct manifests) and the two
               fold22 publication copies
  rerun-r1..r4 pristine re-executions of the published K1167 verifier
               ((same cwd x2) + (isolated cwd/HOME) + (isolated +
               PYTHONHASHSEED=random)); every audit output must be
               byte-identical to the published audit b4b082f8...
  tampers      three fail-closed probes at this lane's own offsets:
               t1 worklist.csv XOR@1234 and t2 K1125 certificate XOR@17522
               inside a copytree W    -> published verifier's own W pin gates;
               t3 published audit byte XOR@4096 in a copy of the experiment
               dir                      -> this harness's own pin gate
  finalize     assemble the audit JSON from the stage records (fail-closed
               on any missing or inconsistent record); deterministic output,
               no clock or runtime fields

Bookkeeping only: no row is closed, no game value is claimed, the 11x11 empty
board and two-stone roots remain UNKNOWN.

Usage: python3 verify_k1167_fold22ext2_third_20261120.py <stage> [<args>]
  stages: pin | reconstruct-w1 | reconstruct-w2 | wcmp | rerun-r1 | rerun-r2 |
          rerun-r3 | rerun-r4 | tampers | finalize
All state lives under /home/user/work/k1167third/ (default, overridable by env
K1167THIRD_ROOT for the isolated finalize runs).
stdlib only.  Fail-closed: exit 1 and no stage record write on any mismatch.
"""
import hashlib, json, os, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(os.environ.get('K1167THIRD_ROOT', '/home/user/work/k1167third'))
REPO_RAW = 'https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/'
PIN_COMMIT = '4eb6cbf05'
REF = '34c29854c64286bbb1792ff28dc1973aef341e20'

FILES = {  # experiment-relative -> (sha256, byte size)
    'README.md': ('6b32ce997aa160cbb82bed10e89c11e9eba31d77dccf2c94cbe46e2694206d88', 10287),
    'scripts/reconstruct_inputs.py': ('dfa50996463fe31000e2bc3b03e37dabe33981bf00708a29ae7634d4a6594a27', 10102),
    'scripts/verify_fold22_external_20261120.py': ('ca11cbbc4b9d5ce3b1569d0af67060d20ec2873efdf3bd22720b3ba50b683792', 48949),
    'output/external-audit.json': ('b4b082f8cb0aa943aad7458ae0c6eb179a27704c5ea781eb18907d869c97522c', 141752),
    'output/reproduction.log': ('5059c458ec08e046a74356bfb7fb6a796865b0c0fb97f12ca983093991c53a90', 2559),
}
PUB_AUDIT_SHA = FILES['output/external-audit.json'][0]
FOLD22_PUB_SHA = {  # verify against the published fold22 receipt side too
    'output/win8-root840500-receipt-fold-20261120.json': 'f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488',
    'scripts/fold_win8_root840500.py': 'd5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d',
    'scripts/build_fold22.py': 'a73995be2ac448f2e56f804b3263330513c5bcb8a9e4042661c56e1deb4d7085',
    'README.md': '0e6861bf2970bead67ce77de9361e11a435cb27ee668e066a565a6fe808c29da',
}

stage_name = sys.argv[1] if len(sys.argv) > 1 else ''
ST = ROOT / 'stages'
W1 = ROOT / 'W1'; W2 = ROOT / 'W2'
PUBW1 = ROOT / 'pub1'; PUBW2 = ROOT / 'pub2'
PUB = ROOT / 'pub_k1167'

def sha(b): return hashlib.sha256(b).hexdigest()
def hf(p): return sha(pathlib.Path(p).read_bytes())

def fail(msg):
    print('STAGE FAILED [' + stage_name + ']: ' + msg)
    sys.exit(1)

def gate(rec, ok, msg):
    if not ok:
        fail(msg)
    rec.setdefault('gates', []).append(msg)

def write_record(name, rec):
    ST.mkdir(parents=True, exist_ok=True)
    (ST / (name + '.json')).write_text(json.dumps(rec, sort_keys=True, indent=1) + '\n')

def load_record(name):
    p = ST / (name + '.json')
    if not p.exists():
        fail('missing stage record ' + name)
    return json.loads(p.read_text())

def check_pub_dir(d):
    d = pathlib.Path(d)
    for rel, (want, size) in FILES.items():
        f = d / rel
        if not f.exists():
            return 'missing ' + rel
        b = f.read_bytes()
        if len(b) != size or sha(b) != want:
            return 'pin mismatch ' + rel

def fetch(url, timeout=300):
    import urllib.request
    return urllib.request.urlopen(url, timeout=timeout).read()

def run_verifier(wdir, pubdir, outpath, env_extra, cwd):
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/root')}
    env.update(env_extra)
    return subprocess.run([sys.executable, str(PUB / 'scripts' / 'verify_fold22_external_20261120.py'),
                           str(wdir), str(pubdir), str(outpath)],
                          capture_output=True, text=True, env=env, cwd=str(cwd))

# ------------------------------------------------------------------ stages
def st_pin():
    rec = {'stage': 'pin', 'commit': PIN_COMMIT, 'files': {}}
    for rel, (want, size) in FILES.items():
        data = fetch(REPO_RAW + PIN_COMMIT + '/research/experiments/n11-fold22-external-second-verification-root840500-20261120/' + rel)
        gate(rec, len(data) == size and sha(data) == want, 'published byte pin ' + rel)
        out = PUB / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        rec['files'][rel] = {'sha256': sha(data), 'bytes': len(data)}
    gate(rec, check_pub_dir(PUB) is None, 'pin stage self check of experiment dir')
    write_record('pin', rec)
    print('pin OK: 5/5 published bytes pinned at %s' % PIN_COMMIT)

def st_reconstruct(which):
    wdir = W1 if which == 'w1' else W2
    pubdir = PUBW1 if which == 'w1' else PUBW2
    if wdir.exists(): shutil.rmtree(wdir)
    if pubdir.exists(): shutil.rmtree(pubdir)
    if (ROOT / ('reconstruct-manifest-%s.json' % which)).exists():
        (ROOT / ('reconstruct-manifest-%s.json' % which)).unlink()
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/root')}
    p = subprocess.run([sys.executable, str(PUB / 'scripts' / 'reconstruct_inputs.py'),
                        str(wdir), str(pubdir), REF],
                       capture_output=True, text=True, env=env, cwd=str(ROOT))
    rec = {'stage': 'reconstruct-' + which, 'ref': REF, 'returncode': p.returncode}
    if p.returncode != 0:
        write_record('reconstruct-' + which, rec)
        fail('published reconstruct failed (rc=%d): %s' % (p.returncode, (p.stdout + p.stderr)[-800:]))
    out = p.stdout
    rec['pub_lines'] = sum(1 for l in out.splitlines() if l.startswith('pub '))
    rec['blob_lines'] = sum(1 for l in out.splitlines() if l.startswith('blob '))
    rec['sha256_lines'] = sum(1 for l in out.splitlines() if l.startswith('sha256 '))
    rec['final_line'] = out.strip().splitlines()[-1]
    for rel, want in FOLD22_PUB_SHA.items():
        f = pubdir / rel
        gate(rec, f.exists() and hf(f) == want, 'reconstruct fold22 publication byte pin ' + rel)
    # the reconstruct script moves its manifest next to W root; exclude by name below
    mn = ROOT / 'reconstruct-manifest.json'
    if mn.exists():
        mn.rename(ROOT / ('reconstruct-manifest-%s.json' % which))
    write_record('reconstruct-' + which, rec)
    print('reconstruct-%s OK' % which)

def st_wcmp():
    rec = {'stage': 'wcmp'}
    def walk(root):
        out = {}
        for p in pathlib.Path(root).rglob('*'):
            if p.is_file():
                out[str(p.relative_to(root))] = p.read_bytes()
        return out
    a = walk(W1); b = walk(W2)
    ka = {k for k in a if 'reconstruct-manifest' not in k}
    kb = {k for k in b if 'reconstruct-manifest' not in k}
    gate(rec, ka == kb, 'two W trees have identical file sets (%d vs %d files)' % (len(ka), len(kb)))
    diff = [k for k in sorted(ka) if a[k] != b[k]]
    gate(rec, not diff, 'two W trees byte-identical; differing: %s' % diff[:5])
    rec['w_file_count'] = len(ka)
    rec['w_total_bytes'] = sum(len(a[k]) for k in ka)
    ma = json.loads((ROOT / 'reconstruct-manifest-w1.json').read_text()) if (ROOT / 'reconstruct-manifest-w1.json').exists() else None
    mb = json.loads((ROOT / 'reconstruct-manifest-w2.json').read_text()) if (ROOT / 'reconstruct-manifest-w2.json').exists() else None
    gate(rec, ma is not None and mb is not None, 'reconstruct manifests present')
    gate(rec, ma['head_ref'] == mb['head_ref'] == REF, 'both manifests pin the same fixed ref')
    gate(rec, ma['pins_blob'] == 12 and ma['pins_sha256'] == 43, 'manifest pin counts 12 blob + 43 sha256')
    gate(rec, json.dumps(ma['machines'], sort_keys=True) == json.dumps(mb['machines'], sort_keys=True), 'manifest machine lists equal')
    for rel, want in FOLD22_PUB_SHA.items():
        gate(rec, hf(PUBW1 / rel) == hf(PUBW2 / rel) == want, 'fold22 publication copies identical and pinned: ' + rel)
    write_record('wcmp', rec)
    print('wcmp OK: %d files, %d bytes, 2 reconstructions byte-identical' % (rec['w_file_count'], rec['w_total_bytes']))

def st_rerun(n, wdir, pubdir, env_extra, cwd):
    tag = 'rerun-r%d' % n
    rec = {'stage': tag, 'w': str(pathlib.Path(wdir).name), 'pub': str(pathlib.Path(pubdir).name)}
    cwd.mkdir(parents=True, exist_ok=True)
    err = check_pub_dir(PUB)
    gate(rec, err is None, 'pre-run K1167 experiment pin gate: ' + str(err))
    outp = ROOT / ('out-r%d.json' % n)
    if outp.exists(): outp.unlink()
    p = run_verifier(wdir, pubdir, outp, env_extra, cwd)
    if p.returncode != 0:
        write_record(tag, dict(rec, returncode=p.returncode))
        fail('published K1167 verifier run %d failed rc=%d: %s' % (n, p.returncode, (p.stdout + p.stderr)[-800:]))
    gate(rec, p.returncode == 0, 'r%d returncode 0' % n)
    gate(rec, p.stderr.strip() == '', 'r%d clean stderr' % n)
    sumline = [l for l in p.stdout.splitlines() if l.startswith('ALL ') and ' GATES PASS' in l]
    gate(rec, len(sumline) == 1 and sumline[0].startswith('ALL 1463 GATES PASS'), 'r%d summary line 1463 gates pass' % n)
    unk = [l for l in p.stdout.splitlines() if l.startswith('11x11 empty board/two-stone roots: UNKNOWN')]
    gate(rec, len(unk) == 1, 'r%d UNKNOWN guard line present' % n)
    b = outp.read_bytes()
    gate(rec, sha(b) == PUB_AUDIT_SHA, 'r%d audit sha256 == published audit b4b082f8' % n)
    gate(rec, b == (PUB / 'output' / 'external-audit.json').read_bytes(), 'r%d audit bytes == published audit bytes' % n)
    rec['audit_sha256'] = sha(b)
    write_record(tag, rec)
    print('%s OK: audit byte-identical to published b4b082f8' % tag)

def st_tampers():
    rec = {'stage': 'tampers', 'probes': []}
    scratch = ROOT / 'tamper'
    # t1: worklist XOR@1234 inside a copytree W -> published verifier's own pin gate
    def wcopy():
        if scratch.exists(): shutil.rmtree(scratch)
        shutil.copytree(W1, scratch)
        outd = scratch / 'fold22' / 'output'
        if outd.exists(): shutil.rmtree(outd)
        return scratch
    # t1
    wt = wcopy()
    tgt = wt / 'inputs' / 'worklist.csv'
    d = bytearray(tgt.read_bytes())
    gate(rec, 1234 < len(d), 't1 offset in range')
    d[1234] ^= 0x01
    tgt.write_bytes(bytes(d))
    p = run_verifier(wt, PUBW1, ROOT / 'out-tamper1.json', {}, ROOT)
    gate(rec, p.returncode != 0, 't1 tampered worklist: verifier nonzero rc')
    gate(rec, 'W blob pin inputs/worklist.csv' in (p.stdout + p.stderr), 't1 fail message W blob pin')
    gate(rec, not (ROOT / 'out-tamper1.json').exists(), 't1 no audit written')
    rec['probes'].append({'probe': 't1', 'target': 'inputs/worklist.csv (copytree W1)', 'offset': 1234,
                          'mutation': 'XOR 0x01', 'expected': 'W blob pin fail-closed',
                          'observed': 'returncode=%d, no audit write' % p.returncode})
    # t2: K1125 certificate XOR@17522 -> sha256 pin gate
    wt = wcopy()
    cert_rel = 'k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11'
    tgt = wt / cert_rel
    d = bytearray(tgt.read_bytes())
    gate(rec, 17522 < len(d), 't2 offset in range')
    d[17522] ^= 0x01
    tgt.write_bytes(bytes(d))
    p = run_verifier(wt, PUBW1, ROOT / 'out-tamper2.json', {}, ROOT)
    gate(rec, p.returncode != 0, 't2 tampered certificate: verifier nonzero rc')
    gate(rec, ('W sha256 pin ' + cert_rel) in (p.stdout + p.stderr), 't2 fail message W sha256 pin')
    gate(rec, not (ROOT / 'out-tamper2.json').exists(), 't2 no audit written')
    rec['probes'].append({'probe': 't2', 'target': cert_rel + ' (copytree W1)', 'offset': 17522,
                          'mutation': 'XOR 0x01', 'expected': 'W sha256 pin fail-closed',
                          'observed': 'returncode=%d, no audit write' % p.returncode})
    # t3: published audit byte XOR@4096 in a copy of the experiment dir -> this harness's pin gate
    pubT = ROOT / 'pub_k1167_tampered'
    if pubT.exists(): shutil.rmtree(pubT)
    shutil.copytree(PUB, pubT)
    tgtf = pubT / 'output' / 'external-audit.json'
    d = bytearray(tgtf.read_bytes())
    gate(rec, 4096 < len(d), 't3 offset in range')
    d[4096] ^= 0x01
    tgtf.write_bytes(bytes(d))
    err = check_pub_dir(pubT)
    gate(rec, err is not None, 't3 tampered experiment dir: harness pin gate fails: ' + str(err))
    gate(rec, check_pub_dir(PUB) is None, 't3 original experiment dir still pinned clean')
    rec['probes'].append({'probe': 't3', 'target': 'output/external-audit.json (copy of experiment dir)', 'offset': 4096,
                          'mutation': 'XOR 0x01', 'expected': 'harness experiment pin gate fail-closed',
                          'observed': 'pin gate rejected: ' + str(err)})
    shutil.rmtree(scratch, ignore_errors=True)
    shutil.rmtree(pubT)
    write_record('tampers', rec)
    print('tampers OK: 3/3 fail-closed probes caught (t1 W-blob, t2 W-sha256, t3 harness pin)')

GUARDS = [
    'This record re-verifies bookkeeping, byte reproducibility, input pins and fail-closed defense of the published K1167 external second verification only.',
    'No row is closed by this record and no game value is claimed: fold22 receipt closures are frontier bookkeeping, not LOSS verdicts.',
    'WIN8-D10 certificates prove only the game tree of their eight-stone roots; REFUTED-D10 is not a LOSS proof.',
    'Node counts, solved counts and coverage counts are not win/loss readings.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
]

def st_finalize():
    rec = {'stage': 'finalize'}
    pin = load_record('pin')
    r1 = load_record('reconstruct-w1'); r2 = load_record('reconstruct-w2')
    wcmp = load_record('wcmp')
    runs = [load_record('rerun-r%d' % i) for i in range(1, 5)]
    tam = load_record('tampers')
    gate(rec, len(pin.get('gates', [])) == 6, 'pin record carries 6 gates')
    gate(rec, r1['ref'] == r2['ref'] == REF and r1['returncode'] == 0 and r2['returncode'] == 0,
         'both reconstruct records: pinned ref, clean rc')
    gate(rec, r1['pub_lines'] == r2['pub_lines'] == 4, 'reconstructs fetched 4 fold22 publication files each')
    gate(rec, wcmp.get('w_file_count', 0) > 0 and 'gates' in wcmp, 'wcmp record present')
    for i, rr in enumerate(runs, 1):
        gate(rec, rr.get('audit_sha256') == PUB_AUDIT_SHA, 'rerun-r%d audit sha == published' % i)
    gate(rec, len(tam.get('probes', [])) == 3, 'three tamper probes recorded')
    audit = {
        'schema': 'n11-k1167-fold22-ext2-pristine-reexec-third-verification-audit-20261120-v1',
        'date': '2026-11-20',
        'verifier': 'verify_k1167_fold22ext2_third_20261120.py (third verification; re-executes the published second-verification machine)',
        'subject': {
            'verification': 'K1167 (fold22 / K1132 external second verification)',
            'published_part1_commit': PIN_COMMIT,
            'fixed_reconstruct_ref': REF,
            'published_files_sha256': {rel: spec[0] for rel, spec in FILES.items()},
            'published_audit_sha256': PUB_AUDIT_SHA,
            'upstream_fold22_publication_sha256': FOLD22_PUB_SHA,
        },
        'stage_records': {
            'pin': {'files_pinned': len(pin['files']), 'gates': len(pin['gates'])},
            'reconstruct_w1': {'ref': r1['ref'], 'pub_lines': r1['pub_lines'], 'blob_lines': r1.get('blob_lines'), 'sha256_lines': r1.get('sha256_lines')},
            'reconstruct_w2': {'ref': r2['ref'], 'pub_lines': r2['pub_lines'], 'blob_lines': r2.get('blob_lines'), 'sha256_lines': r2.get('sha256_lines')},
            'wcmp': {'w_file_count': wcmp['w_file_count'], 'w_total_bytes': wcmp['w_total_bytes']},
            'reruns': [{'run': 'r1', 'cwd': 'stage root', 'w': W1.name, 'pub': PUBW1.name},
                       {'run': 'r2', 'cwd': 'stage root (repeat)', 'w': W1.name, 'pub': PUBW1.name},
                       {'run': 'r3', 'cwd': 'isolated', 'w': W2.name, 'pub': PUBW2.name, 'env': 'isolated HOME'},
                       {'run': 'r4', 'cwd': 'isolated', 'w': 'W4 (fresh copytree of W2)', 'pub': PUBW2.name, 'env': 'isolated HOME + PYTHONHASHSEED=random'}],
            'tampers': tam['probes'],
        },
        'rerun_outcomes': [{'run': 'r%d' % i, 'audit_sha256': runs[i - 1]['audit_sha256'],
                            'byte_identical_to_published_audit': True} for i in range(1, 5)],
        'summary': {
            'published_experiment_files_repinned': 5,
            'reconstructions_byte_identical': True,
            'w_files_compared': wcmp['w_file_count'],
            'pristine_verifier_reruns': 4,
            'all_rerun_audits_byte_identical': all(x['audit_sha256'] == PUB_AUDIT_SHA for x in runs),
            'gates_in_published_audit_reexecuted': 1463,
            'tamper_probes_fail_closed': 3,
        },
        'interpretation_guard': GUARDS,
        'all_gates_pass': True,
        'finalize_gate_count': len(rec['gates']),
    }
    out = ROOT / 'audit.json'
    out.write_text(json.dumps(audit, sort_keys=True, indent=1) + '\n')
    print('FINALIZE OK: %d finalize gates; audit written (%d bytes, sha256 %s)' % (
        len(rec['gates']), out.stat().st_size, hf(out)))
    print('third verification complete; 11x11 empty board / two-stone roots: UNKNOWN')

def main():
    os.environ.setdefault('K1167THIRD_ROOT', str(ROOT))
    if stage_name == 'pin':
        st_pin()
    elif stage_name in ('reconstruct-w1', 'reconstruct-w2'):
        st_reconstruct('w1' if stage_name == 'reconstruct-w1' else 'w2')
    elif stage_name == 'wcmp':
        st_wcmp()
    elif stage_name == 'rerun-r1':
        st_rerun(1, W1, PUBW1, {}, ROOT)
    elif stage_name == 'rerun-r2':
        st_rerun(2, W1, PUBW1, {}, ROOT)
    elif stage_name == 'rerun-r3':
        cwd3 = ROOT / 'cwd-r3'; cwd3.mkdir(parents=True, exist_ok=True)
        st_rerun(3, W2, PUBW2, {'HOME': str(cwd3)}, cwd3)
    elif stage_name == 'rerun-r4':
        cwd4 = ROOT / 'cwd-r4'; cwd4.mkdir(parents=True, exist_ok=True)
        W4 = ROOT / 'W4'
        if W4.exists(): shutil.rmtree(W4)
        shutil.copytree(W2, W4)
        st_rerun(4, W4, PUBW2, {'HOME': str(cwd4), 'PYTHONHASHSEED': 'random'}, cwd4)
    elif stage_name == 'tampers':
        st_tampers()
    elif stage_name == 'finalize':
        st_finalize()
    else:
        fail('unknown stage: %r (pin|reconstruct-w1|reconstruct-w2|wcmp|rerun-r1..r4|tampers|finalize)' % stage_name)

main()
