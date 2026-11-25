#!/usr/bin/env python3
"""Third-verification harness for K1175 (fold12 receipt fold, root 8005021,
external second verification): pristine re-execution in a third environment.

Subject (published bytes, pinned at commit adb1e8f605b6903f6a671d9447c001b79f401398):
  research/experiments/n11-fold12-external-second-verification-root8005021-20261121/
    README.md                                   (SHA-256 d1eae779..., 5,258 bytes)
    scripts/reconstruct_fold12_inputs.py        (SHA-256 caa30f34..., 8,906 bytes)
    scripts/verify_fold12_external_20261121.py  (SHA-256 43afc1cd..., 53,934 bytes)
    output/external-audit.json                   (SHA-256 c309d693..., 70,149 bytes)
    output/reproduction.log                      (SHA-256 d85d8c3d..., 5,668 bytes)

Single-owner declaration note:
  research/log/2026-11-21-n11-k1175-fold12-ext2-pristine-reexec-third-single-owner-note.md
  (commit 4c7a12f1aed44205f20824be024a382d161a7a4c)

Stages (each <300 s, fail-closed; a failing stage writes no part file and
exits nonzero):
  pin      fetch the 5 published files from the pinned commit and verify
           SHA-256 pin and byte size for each (10 gates) -> parts/pin.json
  recon    run the published reconstruct_fold12_inputs.py unmodified at two
           pinned refs (ref_a = declaration-time HEAD 91f2f0f13164...,
           ref_b = verification-time main 4c7a12f1aed4...), then diff the
           two W trees and count files -> parts/recon.json
  rerun    pristine re-execution of the published verifier 4 times
           (r1/r2 same cwd, r3 isolated copytree W/cwd/HOME, r4 isolated +
           PYTHONHASHSEED=random).  Each run: rc==0, ALL 655 GATES PASS line,
           audit SHA-256 == published c309d693..., gate count 655, audit
           byte-identical to the published audit. -> parts/rerun.json
  tampers  two 1-byte XOR tampers at third-lane-chosen, publisher-untested
           offsets on isolated copytree copies (worklist.csv @150000 blob
           pin, K1106 certificate @654321 sha256 pin; publisher tested
           @96300/@456789, other third/second lanes used
           @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}/
           {200222,888222}/{208888,919191}/{300111,740321}).  Each: rc!=0,
           correct fail-closed GATE FAILED [i] message, no audit write;
           production W re-checked unchanged after both.
           -> parts/tampers.json
  finalize assemble parts into the byte-deterministic harness audit JSON
           (no clock/abs-path/volatile fields) -> harness-audit.json

Interpretation guards (also validated in the audit):
  rows are not closed by this verification; WIN8-D10 certificates apply only
  to their own 8-stone root game tree; REFUTED-D10 is not a LOSS proof; nodes
  and solved counts are not verdicts; standard 11x11 empty board / two-stone
  roots {49,60}/{59,60} / S2 {59,60} / class 1/2/4 all remain UNKNOWN.

Usage: python3 verify_k1175_fold12ext2_third_20261121.py <stage> <base_dir>
  <stage> in {pin, recon, rerun, tampers, finalize}
  <base_dir> workspace directory (created); parts/ and stage outputs live in
  <base_dir>/third/, fetched published bytes in <base_dir>/pubfetch/.

Note: the published verifier's rerun scratch is an absolute pinned path
(/home/user/work/f12ext/runs) belonging to its own battery design; this
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
PIN_COMMIT = 'adb1e8f605b6903f6a671d9447c001b79f401398'
REF_A = '91f2f0f13164bfe3bd4734f907d5ea3fd27e1c7c'
REF_B = '4c7a12f1aed44205f20824be024a382d161a7a4c'
DECL_COMMIT = '4c7a12f1aed44205f20824be024a382d161a7a4c'
PUB_DIR = ('research/experiments/'
           'n11-fold12-external-second-verification-root8005021-20261121')

WORKLIST = 'inputs/worklist.csv'
CERT = ('k1106/certs/'
        'win8-root-00000000000000003800000008005021-20261120.n11')
WORKLIST_SHA = '6d8a449e8a3e8ca19f47fe7a42b30f16021797b47509fe592561f60e16e7cef0'
CERT_SHA = '69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5'
AUDIT_SHA = ('c309d69337461518390b7a5cb466e49da6c5c98b7'
             'fbcd0a4fd187bf03b52eb07')

FILES = [
    ('README.md',
     'd1eae7793398051b44c1a0d1ecf65404e239e13e1e63a90d7da240d329cc6a1e', 5258),
    ('scripts/reconstruct_fold12_inputs.py',
     'caa30f346ede97324f0cc268c2b3adf74ae8ce26a8691be4dadbaf66f3da6710', 8906),
    ('scripts/verify_fold12_external_20261121.py',
     '43afc1cd31d5d731858388532d5b07266ac60b2e7265f2490fc6574d5a6578f9', 53934),
    ('output/external-audit.json',
     'c309d69337461518390b7a5cb466e49da6c5c98b7fbcd0a4fd187bf03b52eb07', 70149),
    ('output/reproduction.log',
     'd85d8c3d59a406f2a798716ad779d916cf4d45193cd4bee567dd0fb956d7e199', 5668),
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
        rc, log, ms = run([sys.executable, str(s / 'reconstruct_fold12_inputs.py'),
                           str(wa), str(pa), ref], BASE)
        lines = [l for l in log.splitlines() if l.strip()]
        ok_rc = rc == 0
        ok_done = lines and lines[-1].startswith('RECONSTRUCTED W at') \
            and lines[-1].endswith('PINS 12 PIN256 13')
        ok_subset = any(
            l == 'subset-check fold11 pins 12 pin256 10 subset of '
            'fold12 12+13 OK' for l in lines)
        ok_blob = sum(1 for l in lines if l.startswith('blob ')) == 12
        ok_s256 = sum(1 for l in lines if l.startswith('sha256 ')) == 15
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
            'manifest_pins': '12 blob + 13 sha256 (+fold11/fold12 machines)',
            'chain_subset_check': ('fold11 pins 12+10 subset of '
                                   'fold12 12+13'),
            'w_files': nfiles,
            'wall_ms_not_in_audit': ms,
        }
        out['gates'] += ['recon_%s rc0' % tag,
                         'recon_%s last line PINS 12 PIN256 13' % tag,
                         'recon_%s subset check fold11 12+10 of 12+13' % tag,
                         'recon_%s 12 blob lines' % tag,
                         'recon_%s 15 sha256 lines (13 pins + 2 machines)' % tag,
                         'recon_%s 3 published-file lines' % tag,
                         'recon_%s w file count %d' % (tag, nfiles)]
    # diff of the two W trees (fresh recon dirs)
    rc, log, _ = run(['diff', '-r', str(T / 'wa_a'), str(T / 'wa_b')], BASE)
    if rc != 0:
        die('diff wa_a wa_b not clean: ' + log[:400])
    n_a = out['recon_a']['w_files']
    n_b = out['recon_b']['w_files']
    if n_a != n_b or n_a != 27:
        die('unexpected W file count %d/%d (want 27)' % (n_a, n_b))
    out['diff_wa_wb'] = 'byte-identical'
    out['gates'] += ['diff -r wa_a wa_b clean',
                     'w file count 27 == 27']
    write_part('recon', out)
    print('recon OK: both refs, 27 files each, diff clean')
    sys.exit(0)

# ---------------------------------------------------------------- rerun
if STAGE == 'rerun':
    s = ensure_fetched()
    recon = load_part('recon')
    if not recon:
        die('recon part missing')
    wa = T / 'wa_a'
    pub = T / 'pub_a'
    os.makedirs('/home/user/work/f12ext', exist_ok=True)
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
        vscript = (rundir / 'vscripts' / 'verify_fold12_external_20261121.py') \
            if i >= 3 else (s / 'verify_fold12_external_20261121.py')
        audit = rundir / 'audit.json'
        rc, log, ms = run([sys.executable, str(vscript), str(w), str(p),
                           str(audit)], BASE if i <= 2 else rundir, env)
        line1 = log.splitlines()[0] if log.strip() else ''
        ok_rc = rc == 0
        ok_line = line1.startswith('ALL 655 GATES PASS')
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
        ok_count = gatecount == 655 and j.get('all_gates_pass') is True
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
            'first_line': 'ALL 655 GATES PASS',
            'audit_sha256': a_sha,
            'gate_count': gatecount,
            'byte_identical_to_published_audit': ok_ident,
            'byte_identical_to_run1': same_as_r1,
            'wall_ms_not_in_audit': ms,
        })
        out['gates'] += ['run%d rc0' % i,
                         'run%d ALL 655 GATES PASS line' % i,
                         'run%d audit sha == c309d693...' % i,
                         'run%d gate count 655 + all_gates_pass' % i]
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
        ('t1_worklist_blob_pin_xor_150000',
         [(WORKLIST, 150000)],
         'GATE FAILED [i]: W blob pin ' + WORKLIST),
        ('t2_k1106_cert_sha256pin_xor_654321',
         [(CERT, 654321)],
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
                           str(s / 'verify_fold12_external_20261121.py'),
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
            'publisher_offset': ('worklist@96300' if name.startswith('t1')
                                 else 'cert@456789'),
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
        'k1106_cert_sha256': CERT_SHA,
        'unchanged': True,
    }
    out['gates'] += ['production W worklist sha unchanged',
                     'production W k1106 cert sha unchanged']
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
        'subject': ('K1175 fold12 external second verification pristine '
                    're-execution third verification'),
        'root_hex': '00000000000000003800000008005021',
        'declaration_note': ('research/log/2026-11-21-n11-k1175-fold12-'
                             'ext2-pristine-reexec-third-single-owner-note.md'),
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
