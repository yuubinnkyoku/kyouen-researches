#!/usr/bin/env python3
"""Pristine re-execution THIRD verification of the K1164 fold24 external second verification.

This harness belongs to the n11 long-term lane. It verifies that the published K1164
experiment (the external second verification of the fold24/K1140 receipt fold,
published by a different lane in commits 12b49de9/309d1408/afd50466) can be fully
reproduced by a third party starting only from:

  - the published bytes (fetched from GitHub at pinned commits and staged under
    <stage_root>, with every byte pinned by SHA-256 below), and
  - the W input tree, rebuilt twice (W-A and W-B) by the published
    reconstruct_inputs.py from its fixed Git reference (network step, outside
    this harness; byte equality of the two builds is checked here).

The harness re-executes the published K1164 verifier fresh four times (same cwd x2,
isolated cwd/HOME, isolated + PYTHONHASHSEED=random). Every run must produce a
byte-identical copy of the published audit c7e10332... and exit 0. It also
re-checks fail-closed behaviour on three tamper cases at offsets untouched by the
publisher's internal T-gates (worklist offset 404, fold23 record offset 3456) and on
a tampered published receipt byte (offset 2024) fed to the verifier's P-gates.

Fail-closed, stdlib only. Deterministic canonical output: one audit JSON (sorted
keys, no timestamps, no paths). No row is closed by this verification and no
game-theoretic value is proven. The standard 11x11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.

Usage:
  verify_k1164_pristine_third_20261120.py <stage_root> <W_A> <W_B> <workdir> <out_json>
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

# ------------------------------------------------------------------ constants
K1164_PART1_COMMIT = '12b49de902b0c3e52af577da8ab74e03eadc0275'
K1164_PART2_COMMIT = '309d140861aae1d94bdbc08b13e0a05716ef1bf3'
K1164_PART3_COMMIT = 'afd50466633b6c15f7a7bc0a2f5d1cc1bd58fda6'
K1140_PUB_COMMIT = 'fc4c18fdddb4072667ad019d3218a066e313ff4e'
DECLARATION_COMMIT = '3c88de5ce4101af09a861835b92f7f34d5e40637'
W_RECONSTRUCT_REF = 'b91e85a99f0480f084835bdff51533d0cf5feaa8'

PUB_VERIFIER_SHA = '9bc24e3806724cf7dd3db7e23ec26fb4598ea1952bd92c2974c5626a561d8a52'
PUB_AUDIT_SHA = 'c7e10332df04a4f1e5af7b1cbc5ec487a5c15ca7851edba102b7b3679feb7c24'
PUB_AUDIT_BYTES = 36605

STAGE_PINS = {
    'k1164/README.md': 'ff42947934d7d9df70f549e9547b42bd56f6b566749770c20b697c9850cc6994',
    'k1164/verify_fold24_external_20261120.py': PUB_VERIFIER_SHA,
    'k1164/external-audit.json': PUB_AUDIT_SHA,
    'k1164/reproduction.log': '16b7678e062d65e29e459846feff879a77293e53cefad9357c7375cbfe9950e2',
    'k1140/README.md': '77c4ee401cfe79b5a15cd723902398058225239e622e8687133792cf3451fe15',
    'k1140/win8-root438000000818-receipt-fold-20261120.json':
        'c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7',
    'k1140/fold_win8_root438000000818.py':
        'f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8',
    'k1140/independent-audit.json':
        '49f330c6e0f73c0a58fdd9b21c215c38fc3a594d35f1d617b1324468c4a3387b',
    'k1140/reproduction.log': 'cb01749a9b52e7ed4392dc2d25cf008e805b0ca17b40a25537680e9d1df0e5b2',
    'k1140/reconstruct_inputs.py':
        'f4e1fa8e69b10c07d9eec7f0b798458b0e73a97308bd418b622d1e9542873591',
    'k1140/verify_fold24_independent.py':
        'e0dbebe463a5f0f4e652779905658301d3b9e4b1506e80b581bce673d1f102aa',
    'k1140/build_fold24.py':
        '3c1e07fb785cf3bb8b3a65fbdba558bb18c57a8fb885634482957a5e6a2a6ecc',
}

# SHA-256 over the sorted "relpath sha256" manifest of the reconstructed W tree
# (both independent reconstructions must reproduce exactly this digest).
W_TREE_DIGEST = '1426b6761c1704889ba68c2a94cecc3147068e10678d680635516144fb820773'
W_FILE_COUNT = 70
MACHINE_NAME = 'fold_win8_root438000000818.py'
RECEIPT_NAME = 'win8-root438000000818-receipt-fold-20261120.json'

# Publisher-internal tamper offsets were worklist 777 and k1136 cert 12345.
# The harness chooses entirely different inputs/offsets for its own tamper feed.
TAMPER_CASES = [
    {'case': 'TA-worklist-offset-404', 'path': 'inputs/worklist.csv', 'offset': 404,
     'surface': 'W'},
    {'case': 'TB-fold23-record-offset-3456',
     'path': 'fold23/output/win8-root208090020004-receipt-fold-20261120.json',
     'offset': 3456, 'surface': 'W'},
    {'case': 'TC-pub-receipt-offset-2024', 'path': RECEIPT_NAME, 'offset': 2024,
     'surface': 'pub'},
]

RUNS = [
    {'tag': 'same-env-1', 'iso': False, 'hashseed': None},
    {'tag': 'same-env-2', 'iso': False, 'hashseed': None},
    {'tag': 'isolated-cwd-home', 'iso': True, 'hashseed': None},
    {'tag': 'isolated-hashseed-random', 'iso': True, 'hashseed': 'random'},
]

GUARD = [
    'This third verification re-executes the published K1164 external second verification. '
    'It closes no S6 row and no five-parent target row.',
    'WIN8-D10 certificates cover only the game tree of each eight-stone root; '
    'REFUTED-D10 is not a LOSS proof; node counts and solved counts are not win/loss readings.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, '
    'and classes 1/2/4 remain UNKNOWN.',
]

GATES = []


def need(ok, name):
    if not ok:
        print('GATE FAILED: ' + name)
        sys.exit(1)
    GATES.append(name)


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def tree_manifest(root):
    entries = []
    for base, _dirs, files in os.walk(root):
        for name in files:
            p = os.path.join(base, name)
            rel = os.path.relpath(p, root).replace(os.sep, '/')
            entries.append((rel, sha_file(p)))
    entries.sort()
    return entries


def run_verifier(verifier, wmaster, pubdir, outpath, workroot, iso, hashseed, tag):
    env = dict(os.environ)
    env.pop('PYTHONHASHSEED', None)
    cwd = workroot
    if iso:
        iso_home = os.path.join(workroot, 'iso-home-' + tag)
        iso_cwd = os.path.join(workroot, 'iso-cwd-' + tag)
        os.makedirs(iso_home, exist_ok=True)
        os.makedirs(iso_cwd, exist_ok=True)
        env['HOME'] = iso_home
        cwd = iso_cwd
    if hashseed is not None:
        env['PYTHONHASHSEED'] = hashseed
    p = subprocess.run([sys.executable, verifier, wmaster, pubdir, outpath],
                       env=env, cwd=cwd, capture_output=True, text=True)
    return p


def main():
    if len(sys.argv) != 6:
        print('usage: verify_k1164_pristine_third_20261120.py <stage_root> <W_A> <W_B> <workdir> <out_json>')
        return 2
    stage = os.path.abspath(sys.argv[1])
    w_a = os.path.abspath(sys.argv[2])
    w_b = os.path.abspath(sys.argv[3])
    workroot = os.path.abspath(sys.argv[4])
    outpath = os.path.abspath(sys.argv[5])

    # ---- S-gates: staged published bytes
    for rel, want in STAGE_PINS.items():
        p = os.path.join(stage, rel)
        need(os.path.isfile(p), 'S-exists-' + rel)
        need(sha_file(p) == want, 'S-pin-' + rel)
    published_audit_path = os.path.join(stage, 'k1164/external-audit.json')
    with open(published_audit_path, 'rb') as f:
        published_audit_b = f.read()
    need(len(published_audit_b) == PUB_AUDIT_BYTES, 'S-published-audit-size-36605')
    verifier = os.path.join(stage, 'k1164/verify_fold24_external_20261120.py')

    # ---- W-gates: two independent reconstructions byte-identical, digest pinned
    need(os.path.isdir(w_a) and os.path.isdir(w_b), 'W-both-trees-exist')
    ma, mb = tree_manifest(w_a), tree_manifest(w_b)
    need(len(ma) == W_FILE_COUNT, 'W-file-count-70')
    need(ma == mb, 'W-two-reconstructions-byte-identical')
    digest = sha_bytes(('\n'.join('%s %s' % e for e in ma) + '\n').encode())
    need(digest == W_TREE_DIGEST, 'W-tree-digest-pinned')
    need(not any(rel == 'fold24/output/%s' % RECEIPT_NAME for rel, _ in ma),
         'W-pristine-no-fold24-output')

    # ---- build pristine W master + flat pub dir for the verifier
    if os.path.isdir(workroot):
        shutil.rmtree(workroot)
    os.makedirs(workroot)
    wmaster = os.path.join(workroot, 'W-master')
    shutil.copytree(w_a, wmaster)
    shutil.copy(os.path.join(stage, 'k1140', MACHINE_NAME),
                os.path.join(wmaster, MACHINE_NAME))
    need(sha_file(os.path.join(wmaster, MACHINE_NAME)) == STAGE_PINS['k1140/' + MACHINE_NAME],
         'W-master-machine-pinned')
    pubdir = os.path.join(workroot, 'pubflat')
    os.makedirs(pubdir)
    for rel in [RECEIPT_NAME, MACHINE_NAME, 'independent-audit.json', 'reproduction.log',
                'reconstruct_inputs.py', 'verify_fold24_independent.py']:
        shutil.copy(os.path.join(stage, 'k1140', rel), os.path.join(pubdir, rel))
    for rel in STAGE_PINS:
        if rel.startswith('k1140/'):
            feed_name = rel.split('/', 1)[1]
            if feed_name in [RECEIPT_NAME, MACHINE_NAME, 'independent-audit.json',
                             'reproduction.log', 'reconstruct_inputs.py',
                             'verify_fold24_independent.py']:
                need(sha_file(os.path.join(pubdir, feed_name)) == STAGE_PINS[rel],
                     'P-feed-pin-' + rel)

    # ---- R-gates: fresh re-execution of the published verifier, 4 runs
    runs = []
    stdouts = []
    for spec in RUNS:
        tag = spec['tag']
        out_json = os.path.join(workroot, 'audit-%s.json' % tag)
        p = run_verifier(verifier, wmaster, pubdir, out_json, workroot,
                         spec['iso'], spec['hashseed'], tag)
        need(p.returncode == 0, 'R-' + tag + '-rc0')
        stdouts.append(p.stdout)
        out_b = open(out_json, 'rb').read()
        need(sha_bytes(out_b) == PUB_AUDIT_SHA, 'R-' + tag + '-audit-sha256')
        need(out_b == published_audit_b, 'R-' + tag + '-byte-identical-to-published')
        try:
            summ = json.loads(p.stdout)
        except json.JSONDecodeError:
            summ = {}
        need(summ.get('status') == 'PASS' and summ.get('gate_count') == 800
             and summ.get('machine_runs') == 4 and summ.get('tamper_cases') == 2,
             'R-' + tag + '-stdout-summary')
        runs.append({'tag': tag, 'rc': p.returncode,
                     'audit_sha256': sha_bytes(out_b),
                     'byte_identical_to_published': out_b == published_audit_b})
        # scrub the x-<tag> working tree the verifier created next to W-master
        xdir = os.path.join(os.path.dirname(wmaster), 'x-' + os.path.splitext(
            os.path.basename(out_json))[0])
        if os.path.isdir(xdir):
            shutil.rmtree(xdir)
        os.remove(out_json)
    need(all(s == stdouts[0] for s in stdouts), 'R-stdout-identical-across-runs')

    # ---- T-gates: fail-closed on tamper at publisher-untested offsets/surfaces
    tamper_results = []
    for case in TAMPER_CASES:
        w_case = os.path.join(workroot, 'W-' + case['case'])
        pub_case = os.path.join(workroot, 'pub-' + case['case'])
        shutil.copytree(wmaster, w_case)
        shutil.copytree(pubdir, pub_case)
        target = os.path.join(w_case if case['surface'] == 'W' else pub_case, case['path'])
        with open(target, 'rb') as f:
            b = bytearray(f.read())
        need(len(b) > case['offset'], 'T-' + case['case'] + '-offset-in-range')
        b[case['offset']] ^= 0x01
        with open(target, 'wb') as f:
            f.write(bytes(b))
        out_json = os.path.join(workroot, 'audit-%s.json' % case['case'])
        p = run_verifier(verifier, w_case, pub_case, out_json, workroot, False, None, case['case'])
        need(p.returncode == 1, 'T-' + case['case'] + '-rc1')
        need(not os.path.exists(out_json), 'T-' + case['case'] + '-no-audit-written')
        need('GATE FAILED' in (p.stdout + p.stderr), 'T-' + case['case'] + '-gate-message')
        tamper_results.append({'case': case['case'], 'surface': case['surface'],
                               'path': case['path'], 'offset': case['offset'],
                               'tampered_byte_xor': '0x01',
                               'verifier_rc': p.returncode,
                               'fail_closed': True})
        shutil.rmtree(w_case)
        shutil.rmtree(pub_case)

    # ---- canonical audit
    audit = {
        'experiment': 'n11-fold24-ext2-pristine-reexec-third-verification-20261120',
        'status': 'PASS',
        'target_publication': {
            'k1164_part1_commit': K1164_PART1_COMMIT,
            'k1164_part2_commit': K1164_PART2_COMMIT,
            'k1164_part3_commit': K1164_PART3_COMMIT,
            'k1140_publication_commit': K1140_PUB_COMMIT,
            'w_reconstruct_fixed_ref': W_RECONSTRUCT_REF,
            'single_owner_declaration_commit': DECLARATION_COMMIT,
        },
        'pinned_inputs': {'staged_published_bytes': len(STAGE_PINS),
                          'staged_pins_all_match': True},
        'w_tree': {'file_count': len(ma), 'manifest_sha256': digest,
                   'two_reconstructions_byte_identical': True,
                   'source': 'published reconstruct_inputs.py f4e1fa8e... from fixed ref'},
        'verifier_reexec_runs': runs,
        'verifier_stdout_byte_identical_across_runs': True,
        'tamper_fail_closed': tamper_results,
        'acceptance_criteria': {
            'c1_staged_pins': 'PASS',
            'c2_w_reconstructed_twice_byte_identical': 'PASS',
            'c3_verifier_reexec_4_runs_byte_identical': 'PASS',
            'c4_tamper_fail_closed_publisher_untested_offsets': 'PASS',
            'c5_harness_deterministic_audit': 'see reproduction log (3-run byte identity)',
            'c6_interpretation_guard_embedded': 'PASS',
        },
        'interpretation_guard': GUARD,
    }
    with open(outpath, 'w') as f:
        json.dump(audit, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'gate_count': len(GATES),
                      'audit_sha256': sha_bytes(open(outpath, 'rb').read()),
                      'verifier_runs': len(runs),
                      'tamper_cases': len(tamper_results)}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
