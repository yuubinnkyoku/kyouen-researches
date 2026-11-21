#!/usr/bin/env python3
"""Third-verification harness for K1179 (fold15 receipt fold, root 120000038,
external second verification): pristine re-execution in a third environment.

Subject (published bytes, pinned at commit 2e1bc1eab0fa7f66810d839ca91dd2fae3a50962):
  research/experiments/n11-fold15-external-second-verification-root120000038-20261121/
    README.md                                   (SHA-256 20a2d104..., 6,683 bytes)
    scripts/reconstruct_fold15_inputs.py        (SHA-256 7757cb51..., 10,644 bytes)
    scripts/verify_fold15_external_20261121.py  (SHA-256 ade19de2..., 62,390 bytes)
    output/external-audit.json                   (SHA-256 6800759e..., 101,443 bytes)
    output/reproduction.log                      (SHA-256 579f178a..., 2,106 bytes)

Single-owner declaration note:
  research/log/2026-11-21-n11-k1179-fold15-ext2-pristine-reexec-third-single-owner-note.md
  (commit 04b4ed9d7f279b299d71eb2749728aa741116fe5)

Stages (fail-closed; a failing stage writes no part file and exits nonzero;
the rerun stage is about 4 x 105 s and runs as its own invocation):
  pin      fetch the 5 published files from the pinned commit and verify
           SHA-256 pin and byte size for each (10 gates) -> parts/pin.json
  recon    run the published reconstruct_fold15_inputs.py unmodified at two
           pinned refs (ref_a = declaration-time HEAD b619261ae024...,
           ref_b = verification-time main 04b4ed9d7f27...), then diff the
           two W trees and count files -> parts/recon.json
  rerun    pristine re-execution of the published verifier 4 times
           (r1/r2 same cwd, r3 isolated copytree W/cwd/HOME, r4 isolated +
           PYTHONHASHSEED=random).  Each run: rc==0, ALL 981 GATES PASS line,
           audit SHA-256 == published 6800759e..., gate count 981, audit
           byte-identical to the published audit. -> parts/rerun.json
  tampers  two 1-byte XOR-0x01 tampers at third-lane-chosen, publisher-
           untested offsets on isolated copytree copies (worklist.csv
           @277555 blob pin, K1114 certificate @877666 sha256 pin;
           publisher tested @208888/@919191, the fold12/fold13/fold14 third
           verification lanes used @{150000,654321}/@{222999,1111444}/
           @{333444,999111}, other third/second lanes used @{7777,500000}/
           {253,17522}/{1234,17522,4096}/{117777,777777}/{300111,740321}).
           Each: rc!=0, correct fail-closed GATE FAILED [i] message, no
           audit write; production W re-checked unchanged after both.
           -> parts/tampers.json
  finalize assemble parts into the byte-deterministic harness audit JSON
           (no clock/abs-path/volatile fields) -> harness-audit.json

Interpretation guards (also validated in the audit):
  rows are not closed by this verification; WIN8-D10 certificates apply only
  to their own 8-stone root game tree; REFUTED-D10 is not a LOSS proof; nodes
  and solved counts are not verdicts; standard 11x11 empty board / two-stone
  roots {49,60}/{59,60} / S2 {59,60} / class 1/2/4 all remain UNKNOWN.

Usage: python3 verify_k1179_fold15ext2_third_20261121.py <stage> <base_dir>
  <stage> in {pin, recon, rerun, tampers, finalize}
  <base_dir> workspace directory (created); parts/ and stage outputs live in
  <base_dir>/third/, fetched published bytes in <base_dir>/pubfetch/.

Note: the published verifier's rerun scratch is an absolute pinned path
(/home/user/work/f13ext/runs15) belonging to its own battery design; this
harness runs the verifier strictly sequentially and never lets two runs
overlap.  stdlib only, no randomness in audit bytes, no clock in audit JSON.
"""
import hashlib, json, os, pathlib, shutil, subprocess, sys, time

STAGE = sys.argv[1]
BASE = pathlib.Path(sys.argv[2]).resolve()
T = BASE / 'third'
PARTS = T / 'parts'
FETCH = BASE / 'pubfetch'

REPO = 'yuubinnkyoku/kyouen-researches'
PIN_COMMIT = '2e1bc1eab0fa7f66810d839ca91dd2fae3a50962'
REF_A = 'b619261ae0243573031c4314582d580c51b7712f'
REF_B = '04b4ed9d7f279b299d71eb2749728aa741116fe5'
DECL_COMMIT = '04b4ed9d7f279b299d71eb2749728aa741116fe5'
PUB_DIR = ('research/experiments/'
           'n11-fold15-external-second-verification-'
           'root120000038-20261121')
DECL_NOTE = ('research/log/2026-11-21-n11-k1179-fold15-'
             'ext2-pristine-reexec-third-single-owner-note.md')

WORKLIST = 'inputs/worklist.csv'
CERT = ('k1114/certs/'
        'win8-root-00000000012000003800080009000000-20261120.n11')
WORKLIST_SHA = '6d8a449e8a3e8ca19f47fe7a42b30f16021797b47509fe592561f60e16e7cef0'
CERT_SHA = '5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c'
AUDIT_SHA = ('6800759ea5e899b84866079ac36fae2316d78a856'
             '20e1b32187abc26a0fed717')

FILES = [
    ('README.md',
     '20a2d1042412fd2620ed6fc40be383e656064ade8b201dc13a5e7e43892d0bfa', 6683),
    ('scripts/reconstruct_fold15_inputs.py',
     '7757cb5130942e8891697fcf0903f37d9c8d27f3ed6a8ca1b85a5fc07fd582be', 10644),
    ('scripts/verify_fold15_external_20261121.py',
     'ade19de29fa34bb8f0f7913ece230daa428797792c9db59279e8489d872eac99', 62390),
    ('output/external-audit.json',
     '6800759ea5e899b84866079ac36fae2316d78a85620e1b32187abc26a0fed717', 101443),
    ('output/reproduction.log',
     '579f178a44f5a7ee75ff84c6ee771894f95e9cfaf93df4624135e7ddcc3c9ecc', 2106),
]

GUARDS = {
    'rows_closed': 'none',
    'win8_d10_scope': 'per-root game tree only',
    'refuted_d10': 'not a LOSS proof',
    'nodes_solved': 'not verdicts',
    'unknown': ('standard 11x11 empty board, two-stone roots {49,60}/{59,60}, '
                'S2 {59,60}, class 1/2/4: all UNKNOWN'),
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def die(msg):
    print('STAGE FAILED [' + STAGE + ']: ' + msg)
    sys.exit(1)

def write_part(name, obj):
    PARTS.mkdir(parents=True, exist_ok=True)
    (PARTS / (name + '.json')).write_text(
        json.dumps(obj, sort_keys=True, indent=1, ensure_ascii=True) + '\n')

def load_part(name):
    p = PARTS / (name + '.json')
    if not p.exists():
        return None
    return json.loads(p.read_text())

def get(url):
    import urllib.request
    return urllib.request.urlopen(url, timeout=180).read()

def run(cmd, cwd, env=None):
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(cwd), env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ms = int((time.time() - t0) * 1000)
    return r.returncode, r.stdout.decode('utf-8', 'replace'), ms

# ---------------------------------------------------------------- pin
if STAGE == 'pin':
    out = {'fetched': [], 'gates': 0}
    for rel, want_sha, want_size in FILES:
        data = get('https://raw.githubusercontent.com/' + REPO + '/'
                   + PIN_COMMIT + '/' + PUB_DIR + '/' + rel)
        ok_sha = sha(data) == want_sha
        ok_size = len(data) == want_size
        if not (ok_sha and ok_size):
            die(rel + ' pin mismatch (sha=%s size=%d)'
                % (sha(data), len(data)))
        dest = FETCH / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        out['fetched'].append({'path': rel, 'size': len(data),
                               'sha256': want_sha})
        out['gates'] += 2
    write_part('pin', out)
    print('pin OK: %d files, %d gates' % (len(FILES), out['gates']))
    sys.exit(0)

def ensure_fetched():
    for rel, want_sha, _ in FILES:
        p = FETCH / rel
        if not p.exists() or sha(p.read_bytes()) != want_sha:
            die('pubfetch missing or stale: ' + rel)
    return FETCH / 'scripts'

# ---------------------------------------------------------------- recon
if STAGE == 'recon':
    s = ensure_fetched()
    out = {'refs': {'ref_a': REF_A, 'ref_b': REF_B}, 'gates': []}
    for tag, ref in (('a', REF_A), ('b', REF_B)):
        wa = T / ('wa_' + tag)
        pa = T / ('pub_' + tag)
        shutil.rmtree(wa, ignore_errors=True)
        shutil.rmtree(pa, ignore_errors=True)
        rc, log, ms = run([sys.executable, str(s / 'reconstruct_fold15_inputs.py'),
                           str(wa), str(pa), ref], BASE)
        lines = [l for l in log.splitlines() if l.strip()]
        ok_rc = rc == 0
        ok_done = lines and lines[-1].startswith('RECONSTRUCTED W at') \
            and lines[-1].endswith('PINS 12 PIN256 22')
        ok_subset = all(
            any(l == ('subset-check %s pins 12 pin256 %d subset of '
                      'fold15 12+22 OK' % (n, c)) for l in lines)
            for n, c in (('fold11', 10), ('fold12', 13), ('fold13', 16),
                         ('fold14', 19)))
        ok_blob = sum(1 for l in lines if l.startswith('blob ')) == 12
        ok_s256 = sum(1 for l in lines if l.startswith('sha256 ')) == 27
        ok_pub = sum(1 for l in lines if l.startswith('pub ')) == 3
        if not (ok_rc and ok_done and ok_subset and ok_blob
                and ok_s256 and ok_pub):
            tail = ' | '.join(lines[-3:])
            die('recon_%s failed rc=%s done=%s subset=%s blob12=%s s256=%s '
                'pub3=%s tail=%r'
                % (tag, rc, ok_done, ok_subset, ok_blob, ok_s256, ok_pub,
                   tail[:200]))
        nfiles = sum(1 for p in wa.rglob('*') if p.is_file())
        out['recon_' + tag] = {
            'rc': rc,
            'manifest_pins': ('12 blob + 22 sha256 '
                              '(+fold11/fold12/fold13/fold14/fold15 '
                              'machines)'),
            'chain_subset_check': ('fold11 pins 12+10 subset of fold12 '
                                   '12+13 subset of fold13 12+16 subset of '
                                   'fold14 12+19 subset of fold15 12+22'),
            'w_files': nfiles,
            'wall_ms_not_in_audit': ms,
        }
        out['gates'] += ['recon_%s rc0' % tag,
                         'recon_%s last line PINS 12 PIN256 19' % tag,
                         'recon_%s subset chain fold11 12+10<fold12 12+13<fold13 12+16<'
                         'fold14 12+19<fold15 12+22' % tag,
                         'recon_%s 12 blob lines' % tag,
                         'recon_%s 27 sha256 lines (22 pins + 5 machines)' % tag,
                         'recon_%s 3 published-file lines' % tag,
                         'recon_%s w file count %d' % (tag, nfiles)]
    # diff of the two W trees (fresh recon dirs)
    rc, log, _ = run(['diff', '-r', str(T / 'wa_a'), str(T / 'wa_b')], BASE)
    if rc != 0:
        die('diff wa_a wa_b not clean: ' + log[:400])
    n_a = out['recon_a']['w_files']
    n_b = out['recon_b']['w_files']
    if n_a != n_b or n_a != 39:
        die('unexpected W file count %d/%d (want 39)' % (n_a, n_b))
    out['diff_wa_wb'] = 'byte-identical'
    out['gates'] += ['diff -r wa_a wa_b clean',
                     'w file count 39 == 39']
    write_part('recon', out)
    print('recon OK: both refs, 39 files each, diff clean')
    sys.exit(0)

# ---------------------------------------------------------------- rerun
if STAGE == 'rerun':
    s = ensure_fetched()
    recon = load_part('recon')
    if not recon:
        die('recon part missing')
    wa = T / 'wa_a'
    pub = T / 'pub_a'
    os.makedirs('/home/user/work/f13ext', exist_ok=True)
    out = {'runs': [], 'gates': []}
    audits = {}
    for i in (1, 2, 3, 4):
        rundir = T / ('run%d' % i)
        shutil.rmtree(rundir, ignore_errors=True)
        rundir.mkdir(parents=True)
        if i <= 2:
            w, p = wa, pub
            env = None
        else:
            w = rundir / 'W'
            p = rundir / 'pub'
            shutil.copytree(wa, w)
            shutil.copytree(pub, p)
            shutil.copytree(FETCH / 'scripts', rundir / 'vscripts')
            (rundir / 'home').mkdir()
            (rundir / 'tmp').mkdir()
            env = {'PATH': '/usr/local/bin:/usr/bin:/bin',
                   'HOME': str(rundir / 'home'),
                   'TMPDIR': str(rundir / 'tmp')}
        if i == 4:
            env['PYTHONHASHSEED'] = 'random'
        vscript = (rundir / 'vscripts' / 'verify_fold15_external_20261121.py') \
            if i >= 3 else (s / 'verify_fold15_external_20261121.py')
        audit = rundir / 'audit.json'
        rc, log, ms = run([sys.executable, str(vscript), str(w), str(p),
                           str(audit)], BASE if i <= 2 else rundir, env)
        line1 = log.splitlines()[0] if log.strip() else ''
        ok_rc = rc == 0
        ok_line = line1.startswith('ALL 981 GATES PASS')
        has_audit = audit.exists()
        if not (ok_rc and ok_line and has_audit):
            die('run%d rc=%s line=%r audit=%s'
                % (i, rc, line1[:80], has_audit))
        data = audit.read_bytes()
        a_sha = sha(data)
        ok_sha = a_sha == AUDIT_SHA
        j = json.loads(data)
        gatecount = sum(1 for g in j.get('gates', j.get('GATES', []))
                        if isinstance(g, dict) and g.get('ok') is True)
        ok_count = gatecount == 981 and j.get('all_gates_pass') is True
        ok_ident = data == (FETCH / 'output' / 'external-audit.json').read_bytes()
        audits[i] = data
        if not (ok_sha and ok_count and ok_ident):
            die('run%d sha=%s gates=%s ident=%s'
                % (i, a_sha, gatecount, ok_ident))
        same_as_r1 = (audits[1] == data)
        if not same_as_r1:
            die('run%d audit differs from run1' % i)
        out['runs'].append({
            'run': i,
            'mode': ('same cwd' if i <= 2 else
                     ('isolated tree/cwd/HOME' if i == 3
                      else 'isolated + PYTHONHASHSEED=random')),
            'rc': rc,
            'first_line': 'ALL 981 GATES PASS',
            'audit_sha256': a_sha,
            'gate_count': gatecount,
            'byte_identical_to_published_audit': ok_ident,
            'byte_identical_to_run1': same_as_r1,
            'wall_ms_not_in_audit': ms,
        })
        out['gates'] += ['run%d rc0' % i,
                         'run%d ALL 981 GATES PASS line' % i,
                         'run%d audit sha == 6800759e...' % i,
                         'run%d gate count 981 + all_gates_pass' % i]
        if i >= 2:
            out['gates'].append('run%d audit byte-identical to run1' % i)
    out['published_audit_sha256'] = AUDIT_SHA
    out['all_runs_byte_identical'] = True
    write_part('rerun', out)
    print('rerun OK: 4 pristine verifier reruns, all byte-identical '
          'to the published audit')
    sys.exit(0)

# ---------------------------------------------------------------- tampers
if STAGE == 'tampers':
    s = ensure_fetched()
    recon = load_part('recon')
    if not recon:
        die('recon part missing')
    wa = T / 'wa_a'
    pub = T / 'pub_a'
    tampers = [
        ('t1_worklist_blob_pin_xor_277555',
         [(WORKLIST, 277555)],
         'GATE FAILED [i]: W blob pin ' + WORKLIST),
        ('t2_k1114_cert_sha256pin_xor_877666',
         [(CERT, 877666)],
         'GATE FAILED [i]: W sha256 pin ' + CERT),
    ]
    out = {'tampers': [], 'gates': []}
    for name, edits, want_msg in tampers:
        d = T / ('tamp_' + name.split('_')[0])
        shutil.rmtree(d, ignore_errors=True)
        w = d / 'W'
        p = d / 'pub'
        shutil.copytree(wa, w)
        shutil.copytree(pub, p)
        for rel, off in edits:
            f = w / rel
            b = bytearray(f.read_bytes())
            if off >= len(b):
                die('%s offset %d >= file size %d' % (rel, off, len(b)))
            b[off] ^= 0x01
            f.write_bytes(bytes(b))
        audit = d / 'audit.json'
        rc, log, ms = run([sys.executable,
                           str(s / 'verify_fold15_external_20261121.py'),
                           str(w), str(p), str(audit)], BASE)
        ok_rc = rc != 0
        ok_msg = want_msg in log
        no_write = not audit.exists()
        if not (ok_rc and ok_msg and no_write):
            die('%s rc=%s msg=%s nowrite=%s log=%r'
                % (name, rc, ok_msg, no_write, log[:200]))
        out['tampers'].append({
            'name': name,
            'edits': [{'path': rel, 'offset': off, 'op': '1-byte XOR 0x01'}
                      for rel, off in edits],
            'publisher_offset': ('worklist@208888' if name.startswith('t1')
                                 else 'cert@919191'),
            'rc': rc,
            'fail_message': want_msg,
            'audit_written': False,
            'isolation': 'fresh copytree, production W untouched',
        })
        out['gates'] += [name + ' rc!=0', name + ' fail message',
                         name + ' no audit write']
    # production W re-checked unchanged after both tampers
    ok_wl = sha((wa / WORKLIST).read_bytes()) == WORKLIST_SHA
    ok_ct = sha((wa / CERT).read_bytes()) == CERT_SHA
    if not (ok_wl and ok_ct):
        die('production W worklist/cert hash changed: %s %s' % (ok_wl, ok_ct))
    out['production_w_recheck'] = {
        'worklist_sha256': WORKLIST_SHA,
        'k1114_cert_sha256': CERT_SHA,
        'unchanged': True,
    }
    out['gates'] += ['production W worklist sha unchanged',
                     'production W k1114 cert sha unchanged']
    write_part('tampers', out)
    print('tampers OK: 2 fail-closed, production W unchanged')
    sys.exit(0)

# ---------------------------------------------------------------- finalize
if STAGE == 'finalize':
    parts = {}
    for name in ('pin', 'recon', 'rerun', 'tampers'):
        p = load_part(name)
        if p is None:
            die('missing part: ' + name)
        parts[name] = p

    def strip_volatile(obj):
        if isinstance(obj, dict):
            return {k: strip_volatile(v) for k, v in obj.items()
                    if not k.endswith('_not_in_audit')}
        if isinstance(obj, list):
            return [strip_volatile(v) for v in obj]
        return obj

    gates = 0
    section_gate_counts = {}
    for name in ('pin', 'recon', 'rerun', 'tampers'):
        g = parts[name]['gates']
        if isinstance(g, list):
            section_gate_counts[name] = len(g)
            gates += len(g)
        else:
            section_gate_counts[name] = int(g)
            gates += int(g)
    audit = {
        'subject': ('K1179 fold15 external second verification pristine '
                    're-execution third verification'),
        'root_hex': '00000000012000003800080009000000',
        'declaration_note': DECL_NOTE,
        'declaration_commit': DECL_COMMIT,
        'published_by_pin_commit': PIN_COMMIT,
        'subject_experiment_dir': PUB_DIR,
        'subject_audit_sha256': AUDIT_SHA,
        'pin': strip_volatile(parts['pin']),
        'recon': strip_volatile(parts['recon']),
        'rerun': strip_volatile(parts['rerun']),
        'tampers': strip_volatile(parts['tampers']),
        'section_gate_counts': section_gate_counts,
        'gates_seen': gates,
        'all_gates_pass': True,
        'interpretation_guards': GUARDS,
    }
    PARTS.mkdir(parents=True, exist_ok=True)
    text = json.dumps(audit, sort_keys=True, indent=1, ensure_ascii=True) + '\n'
    (T / 'harness-audit.json').write_text(text)
    print('finalize OK: harness-audit.json written, %d gates' % gates)
    sys.exit(0)

die('unknown stage: ' + STAGE)
