#!/usr/bin/env python3
# Third verification (pristine re-execution) harness for the published external
# second verification of fold10 (the seventeenth WIN7 receipt fold).
#
# Subject ext2 publication: commit 452af0c5cc91a195dd24f4e4086af9bba11e807f,
#   research/experiments/n11-seventeenth-receipt-fold-second-verification-20261120/
#   (README.md, scripts/verify_fold10_second.py, output/fold10-second-verification-20261120.json)
# W inputs (published artifacts, pinned inside the published verifier):
#   fold10 record bed7d331..., fold9 record 24db2352..., seventeenth cert 21dd2f0e...
#
# Stages: pin / recon / rerun / tampers / finalize.  stdlib only, fail-closed,
# byte-deterministic audit (no wall time, no absolute paths, no volatile fields).
# Single-owner declaration:
#   research/log/2026-11-21-n11-fold10-17threceipt-ext2-pristine-reexec-third-single-owner-note.md
#   (declaration commit 4987c2b7dffd98d590ba65499bfb1caed3e1e939, declared at HEAD dcc5b96238c023...)
import sys, os, json, hashlib, shutil, subprocess, urllib.request, tempfile

OWNER, REPO = 'yuubinnkyoku', 'kyouen-researches'
PIN_COMMIT = '452af0c5cc91a195dd24f4e4086af9bba11e807f'   # ext2 publish commit
REF_A = 'dcc5b96238c0232f0ff8eb07bd50be4243262938'        # declaration-time HEAD
REF_B = '4987c2b7dffd98d590ba65499bfb1caed3e1e939'        # declaration commit

EXT2_DIR = 'research/experiments/n11-seventeenth-receipt-fold-second-verification-20261120'
PINS = {
  'readme':   (f'{EXT2_DIR}/README.md', 3982,  '240c8e588d07d72212bc5419d6606812d87f9181affe2ab0785ec336a14e3197'),
  'verifier': (f'{EXT2_DIR}/scripts/verify_fold10_second.py', 11145, '7178fbe5fc31045ca36880863b72c6014c2997aa7e4731ac6dc20a88f85ac84f'),
  'ext2audit':(f'{EXT2_DIR}/output/fold10-second-verification-20261120.json', 5410, 'a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054'),
}
W = {
  'fold10': {
    'repo': 'research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json',
    'target': '/home/user/work/fold10v/fold10.json',
    'bytes': 12918, 'sha256': 'bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a'},
  'fold9': {
    'repo': 'research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json',
    'target': '/home/user/work/fold9/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json',
    'bytes': 24399, 'sha256': '24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2'},
  'cert': {
    'repo': 'research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11',
    'target': '/home/user/work/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11',
    'bytes': 1791541, 'sha256': '21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8'},
}
T1_KEY, T1_OFF = 'fold10', 12345      # lane-chosen tamper offset (unique vs all recorded lanes)
T2_KEY, T2_OFF = 'cert', 1234567      # lane-chosen tamper offset (unique vs all recorded lanes)
VERIFY_OUTPUT_NAME = 'fold10-second-verification-20261120.json'

def raw_url(ref, path):
    return f'https://raw.githubusercontent.com/{OWNER}/{REPO}/{ref}/{path}'

def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def die(stage, why):
    print(f'STAGE FAILED [{stage}]: {why}')
    sys.exit(1)

def gate(rec, name, ok, detail=''):
    rec.append({'gate': name, 'pass': bool(ok), 'detail': str(detail)[:220]})

def load_parts(base):
    d = {}
    for k in ('pin', 'recon', 'rerun', 'tampers'):
        p = os.path.join(base, 'parts', k + '.json')
        with open(p) as f:
            d[k] = json.load(f)
    return d

def allpass(rec):
    return all(g['pass'] for g in rec)

# ------------------------------------------------------------------ pin
def stage_pin(base):
    rec = []
    stored = {}
    for k, (path, nbytes, sha) in PINS.items():
        try:
            b = fetch(raw_url(PIN_COMMIT, path))
        except Exception as e:
            die('pin', f'fetch {k}: {e}')
        stored[k] = b
        gate(rec, f'pin/{k} byte count == {nbytes}', len(b) == nbytes, f'{len(b)}')
        gate(rec, f'pin/{k} sha256 == published {sha[:8]}…', sha256_bytes(b) == sha, sha256_bytes(b))
    if not allpass(rec):
        os.makedirs(os.path.join(base, 'parts'), exist_ok=True)
        with open(os.path.join(base, 'parts', 'pin.json'), 'w') as f:
            json.dump({'gates': rec}, f)
        die('pin', 'gate failure')
    os.makedirs(os.path.join(base, 'parts'), exist_ok=True)
    with open(os.path.join(base, 'parts', 'pin.json'), 'w') as f:
        json.dump({'gates': rec}, f)

# ------------------------------------------------------------------ recon
def stage_recon(base):
    rec = []
    w_a = {}
    for k, spec in W.items():
        try:
            wa = fetch(raw_url(REF_A, spec['repo']))
            wb = fetch(raw_url(REF_B, spec['repo']))
        except Exception as e:
            die('recon', f'fetch {k}: {e}')
        w_a[k] = wa
        gate(rec, f"recon/{k} ref_a sha256 == verifier pin {spec['sha256'][:8]}…",
             sha256_bytes(wa) == spec['sha256'], sha256_bytes(wa))
        gate(rec, f"recon/{k} ref_b sha256 == verifier pin {spec['sha256'][:8]}…",
             sha256_bytes(wb) == spec['sha256'], sha256_bytes(wb))
        gate(rec, f'recon/{k} W_A == W_B bytes', wa == wb, f'{len(wa)} vs {len(wb)}')
        gate(rec, f"recon/{k} byte count == {spec['bytes']}", len(wa) == spec['bytes'], len(wa))
    # install at the verifier's fixed absolute paths
    for k, spec in W.items():
        os.makedirs(os.path.dirname(spec['target']), exist_ok=True)
        with open(spec['target'], 'wb') as f:
            f.write(w_a[k])
        gate(rec, f'recon/{k} installed W sha256 == pin', sha256_file(spec['target']) == spec['sha256'],
             sha256_file(spec['target']))
    if not allpass(rec):
        with open(os.path.join(base, 'parts', 'recon.json'), 'w') as f:
            json.dump({'gates': rec}, f)
        die('recon', 'gate failure')
    with open(os.path.join(base, 'parts', 'recon.json'), 'w') as f:
        json.dump({'gates': rec}, f)

# ------------------------------------------------------------------ rerun
def _run_once(base, runname, dirlabel, verifier_bytes, env_extra_isolated, hashseed_random):
    rundir = os.path.join(base, 'runs', dirlabel)
    os.makedirs(os.path.join(rundir, 'scripts'), exist_ok=True)
    spath = os.path.join(rundir, 'scripts', 'verify_fold10_second.py')
    with open(spath, 'wb') as f:
        f.write(verifier_bytes)
    rec = []
    gate(rec, f'rerun/{runname} script copy byte == published pin',
         sha256_bytes(verifier_bytes) == PINS['verifier'][2])
    if env_extra_isolated:
        iso = os.path.join(base, 'iso', runname)
        home = os.path.join(iso, 'home'); tmp = os.path.join(iso, 'tmp')
        os.makedirs(home, exist_ok=True); os.makedirs(tmp, exist_ok=True)
        env = {'HOME': home, 'TMPDIR': tmp, 'PATH': '/usr/bin:/bin'}
        if hashseed_random:
            env['PYTHONHASHSEED'] = 'random'
    else:
        env = None
    r = subprocess.run([sys.executable, spath], cwd=rundir, env=env,
                       capture_output=True, timeout=600)
    outp = os.path.join(rundir, 'output', VERIFY_OUTPUT_NAME)
    gate(rec, f'rerun/{runname} rc == 0', r.returncode == 0, f'rc={r.returncode} stderr_tail={r.stderr[-200:].decode("utf8", "replace")}')
    try:
        out = open(outp, 'rb').read()
    except FileNotFoundError:
        gate(rec, f'rerun/{runname} output byte == published ext2 audit', False, 'output missing')
        return rec
    gate(rec, f'rerun/{runname} output byte == published ext2 audit',
         sha256_bytes(out) == PINS['ext2audit'][2] and len(out) == PINS['ext2audit'][1],
         f'{len(out)}B {sha256_bytes(out)[:8]}…')
    try:
        stdout = json.loads(r.stdout.decode('utf8'))
    except Exception:
        stdout = {}
    ok = (stdout.get('status') == 'second-verified' and stdout.get('gates_total') == 31
          and stdout.get('all_pass') is True and stdout.get('sha256') == PINS['ext2audit'][2])
    gate(rec, f'rerun/{runname} stdout status/gates_total/all_pass/sha256', ok,
         f'{stdout.get("status")}/{stdout.get("gates_total")}/{stdout.get("all_pass")}')
    j = json.loads(out.decode('utf8'))
    ok2 = (j.get('status') == 'second-verified' and j.get('gates_total') == 31
           and j.get('gates_all_pass') is True and j.get('schema') == 'n11-fold10-second-verification-20261120-v1'
           and isinstance(j.get('gates'), list) and len(j.get('gates', [])) == 31
           and all(g.get('pass') for g in j.get('gates', [])))
    gate(rec, f'rerun/{runname} audit JSON 31 gates all pass + schema', ok2, '')
    gate(rec, f'rerun/{runname} audit inputs_verified_by_sha256 == W pins',
         j.get('inputs_verified_by_sha256') == {'fold10_record': W['fold10']['sha256'],
                                                'fold9_record': W['fold9']['sha256'],
                                                'seventeenth_certificate': W['cert']['sha256']}, '')
    return rec

def stage_rerun(base):
    with open(os.path.join(base, 'parts', 'pin.json')) as f:
        pin = json.load(f)
    verifier_bytes = fetch(raw_url(PIN_COMMIT, PINS['verifier'][0]))
    if sha256_bytes(verifier_bytes) != PINS['verifier'][2]:
        die('rerun', 'verifier fetch does not match pin')
    rec = []
    # r1, r2: same cwd (shared run dir r12), inherited env
    for name, dlabel, iso, seed in (('r1', 'r12', False, False), ('r2', 'r12', False, False),
                                    ('r3', 'r3', True, False), ('r4', 'r4', True, True)):
        rec.extend(_run_once(base, name, dlabel, verifier_bytes, iso, seed))
    if not allpass(rec):
        with open(os.path.join(base, 'parts', 'rerun.json'), 'w') as f:
            json.dump({'gates': rec}, f)
        die('rerun', 'gate failure')
    with open(os.path.join(base, 'parts', 'rerun.json'), 'w') as f:
        json.dump({'gates': rec}, f)

# ------------------------------------------------------------------ tampers
def _tamper_run(base, name, verifier_bytes, env_isolated=True, hashseed_random=False):
    rundir = os.path.join(base, 'runs', name)
    os.makedirs(os.path.join(rundir, 'scripts'), exist_ok=True)
    spath = os.path.join(rundir, 'scripts', 'verify_fold10_second.py')
    with open(spath, 'wb') as f:
        f.write(verifier_bytes)
    if env_isolated:
        iso = os.path.join(base, 'iso', name)
        home = os.path.join(iso, 'home'); tmp = os.path.join(iso, 'tmp')
        os.makedirs(home, exist_ok=True); os.makedirs(tmp, exist_ok=True)
        env = {'HOME': home, 'TMPDIR': tmp, 'PATH': '/usr/bin:/bin'}
        if hashseed_random:
            env['PYTHONHASHSEED'] = 'random'
    else:
        env = None
    r = subprocess.run([sys.executable, spath], cwd=rundir, env=env,
                       capture_output=True, timeout=600)
    outp = os.path.join(rundir, 'output', VERIFY_OUTPUT_NAME)
    return r, outp, rundir

def stage_tampers(base):
    verifier_bytes = fetch(raw_url(PIN_COMMIT, PINS['verifier'][0]))
    if sha256_bytes(verifier_bytes) != PINS['verifier'][2]:
        die('tampers', 'verifier fetch does not match pin')
    rec = []
    # t1: fold10 record tamper @T1_OFF (1 byte XOR 0x01) -> json load dies, no output written
    spec = W[T1_KEY]
    orig = open(spec['target'], 'rb').read()
    gate(rec, f'tampers/t1 pre-tamper {T1_KEY} W sha256 == pin', sha256_bytes(orig) == spec['sha256'], '')
    mutated = bytearray(orig); mutated[T1_OFF] ^= 0x01
    with open(spec['target'], 'wb') as f:
        f.write(bytes(mutated))
    r, outp, rundir = _tamper_run(base, 't1', verifier_bytes)
    gate(rec, 'tampers/t1 rc != 0 (fail-closed)', r.returncode != 0, f'rc={r.returncode}')
    ok1 = False; failed1 = []
    if os.path.exists(outp):
        try:
            j1 = json.loads(open(outp, 'rb').read().decode('utf8'))
            failed1 = [g['gate'] for g in j1.get('gates', []) if not g.get('pass')]
            ok1 = (j1.get('status') == 'gate-failed' and j1.get('gates_total') == 31
                   and j1.get('gates_all_pass') is False
                   and failed1 == ['fold10 正本 sha256 == published bed7d331...'])
            others_pass = all(g.get('pass') for g in j1.get('gates', []) if g['gate'] != 'fold10 正本 sha256 == published bed7d331...')
            certgate = [g for g in j1.get('gates', []) if 'cert sha256 pin' in g['gate']]
            ok1 = ok1 and others_pass and len(certgate) == 1 and certgate[0].get('pass') is True
        except Exception:
            ok1 = False
    gate(rec, 'tampers/t1 audit written gate-failed, exactly the fold10 sha pin gate fails, all other 30 gates (incl cert sha pin) still pass',
         ok1, f'failed={failed1}')
    with open(spec['target'], 'wb') as f:
        f.write(orig)
    gate(rec, f'tampers/t1 restored {T1_KEY} W sha256 == pin', sha256_file(spec['target']) == spec['sha256'], '')
    # t2: cert tamper @T2_OFF (1 byte XOR 0x01) -> cert sha pin gate fails, audit written gate-failed
    spec2 = W[T2_KEY]
    orig2 = open(spec2['target'], 'rb').read()
    gate(rec, f'tampers/t2 pre-tamper {T2_KEY} W sha256 == pin', sha256_bytes(orig2) == spec2['sha256'], '')
    mutated2 = bytearray(orig2); mutated2[T2_OFF] ^= 0x01
    assert mutated2[T2_OFF] != orig2[T2_OFF]
    with open(spec2['target'], 'wb') as f:
        f.write(bytes(mutated2))
    r2, outp2, rundir2 = _tamper_run(base, 't2', verifier_bytes)
    gate(rec, 'tampers/t2 rc != 0 (fail-closed)', r2.returncode != 0, f'rc={r2.returncode}')
    ok2 = False; failed_names = []
    if os.path.exists(outp2):
        try:
            j = json.loads(open(outp2, 'rb').read().decode('utf8'))
            failed_names = [g['gate'] for g in j.get('gates', []) if not g.get('pass')]
            ok2 = (j.get('status') == 'gate-failed' and j.get('gates_all_pass') is False
                   and failed_names == ['cert sha256 pin matches local byte-exact file'])
            f10gate = j.get('gates', [None])[0]
            ok2 = ok2 and f10gate is not None and f10gate.get('pass') is True
        except Exception:
            ok2 = False
    gate(rec, 'tampers/t2 audit written with status gate-failed, exactly the cert sha pin gate failed, fold10 pin gate still pass',
         ok2, f'failed={failed_names}')
    with open(spec2['target'], 'wb') as f:
        f.write(orig2)
    gate(rec, f'tampers/t2 restored {T2_KEY} W sha256 == pin', sha256_file(spec2['target']) == spec2['sha256'], '')
    # final W unmodified re-check
    for k, w in W.items():
        gate(rec, f'tampers/post {k} W sha256 == pin (unmodified)', sha256_file(w['target']) == w['sha256'], '')
    if not allpass(rec):
        with open(os.path.join(base, 'parts', 'tampers.json'), 'w') as f:
            json.dump({'gates': rec}, f)
        die('tampers', 'gate failure')
    with open(os.path.join(base, 'parts', 'tampers.json'), 'w') as f:
        json.dump({'gates': rec}, f)

# ------------------------------------------------------------------ finalize
def stage_finalize(base):
    try:
        parts = load_parts(base)
    except Exception as e:
        die('finalize', f'parts incomplete: {e}')
    allg = []
    for k in ('pin', 'recon', 'rerun', 'tampers'):
        allg.extend(parts[k]['gates'])
    total = len(allg)
    passed = sum(1 for g in allg if g['pass'])
    record = {
        'schema': 'n11-fold10-17threceipt-ext2-pristine-reexec-third-harness-20261121-v1',
        'date': '2026-11-21',
        'status': 'all-gates-pass' if total == passed else 'gate-failed',
        'subject': {
            'ext2_experiment_dir': EXT2_DIR,
            'ext2_publish_commit': PIN_COMMIT,
            'target_receipt': 'fold10 = seventeenth WIN7-D10 receipt fold (root 00004000000000821082000000000100)',
            'published_files': {
                'README.md': {'bytes': PINS['readme'][1], 'sha256': PINS['readme'][2]},
                'scripts/verify_fold10_second.py': {'bytes': PINS['verifier'][1], 'sha256': PINS['verifier'][2]},
                'output/fold10-second-verification-20261120.json': {'bytes': PINS['ext2audit'][1], 'sha256': PINS['ext2audit'][2]},
            },
        },
        'refs': {'ref_a_declaration_time_head': REF_A, 'ref_b_declaration_commit': REF_B, 't1_correction_addendum_commit': '274e3e28c43dc24e0c638f498051d75a75627bad'},
        'w_inputs': {k: {'bytes': v['bytes'], 'sha256': v['sha256'], 'repo_path': v['repo']} for k, v in W.items()},
        'battery_runs': ['r1', 'r2', 'r3', 'r4'],
        'rerun_modes': {'r1': 'shared cwd, inherited env', 'r2': 'shared cwd, inherited env',
                        'r3': 'isolated copytree cwd, env -i isolated HOME/TMPDIR',
                        'r4': 'isolated as r3 + PYTHONHASHSEED=random'},
        'tamper_probes': {'t1': f'{T1_KEY} W @offset {T1_OFF} 1 byte XOR 0x01 (rc!=0, audit gate-failed, exactly the fold10 sha pin gate fails; corrected per addendum 274e3e28)',
                          't2': f'{T2_KEY} W @offset {T2_OFF} 1 byte XOR 0x01 (rc!=0, audit gate-failed, cert sha pin gate fails)'},
        'stages': {k: {'gates': parts[k]['gates'], 'gates_all_pass': allpass(parts[k]['gates'])} for k in ('pin', 'recon', 'rerun', 'tampers')},
        'gates_total': total,
        'gates_passed': passed,
        'gates_all_pass': total == passed,
        'interpretation_guard': [
            '本検証はfold10外部第二検証の再現性・入力pin・fail-closed防衛・監査byteの第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。',
            '行は1行も閉じない。fold10時点の残余簿記は当該receiptの既出版値のまま。',
            'WIN7-D10証明書は当該7石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。',
            'nodes数・solved数・coverage数を勝敗として読まない。',
            '標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。',
        ],
        'unknown_guard': 'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.',
    }
    os.makedirs(os.path.join(base, 'audit'), exist_ok=True)
    outp = os.path.join(base, 'audit', 'fold10ext2-third-harness-audit.json')
    with open(outp, 'w') as f:
        json.dump(record, f, indent=1, sort_keys=False, ensure_ascii=False)
        f.write('\n')
    print(json.dumps({'status': record['status'], 'gates_total': total, 'gates_passed': passed,
                      'audit_sha256': sha256_file(outp)}, indent=1))
    sys.exit(0 if total == passed else 1)

def main():
    if len(sys.argv) != 3:
        print('usage: verify_fold10ext2_third_20261121.py <stage|all> <basedir>')
        sys.exit(2)
    stage, base = sys.argv[1], os.path.abspath(sys.argv[2])
    os.makedirs(base, exist_ok=True)
    stages = {'pin': stage_pin, 'recon': stage_recon, 'rerun': stage_rerun,
               'tampers': stage_tampers, 'finalize': stage_finalize}
    if stage == 'all':
        for s in ('pin', 'recon', 'rerun', 'tampers', 'finalize'):
            stages[s](base)
    elif stage in stages:
        stages[stage](base)
    else:
        print(f'unknown stage {stage}')
        sys.exit(2)

if __name__ == '__main__':
    main()
