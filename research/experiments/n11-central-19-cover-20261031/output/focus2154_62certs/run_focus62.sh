#!/bin/bash
set -euo pipefail
REPO=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches
DIR=$REPO/research/experiments/n11-central-19-cover-20261031
OUT=/mnt/d/kyouen-focus-certs
mkdir -p "$OUT"
cd "$DIR"
g++ -O3 -std=c++17 -o "$OUT/gen" generate_five_terminal_loss7.cpp
python3 - <<'PY'
import json, subprocess, pathlib, concurrent.futures, hashlib
work = pathlib.Path('/mnt/d/kyouen-focus-certs')
plan = json.load(open('output/focus2154_plan.json'))
keys = plan['unverified_s7']
results = {}
def run(k, attempt=0):
    root = k
    cert = work / (k + ('.win7.cert' if attempt else '.cert'))
    args = [str(work / 'gen'), k, str(cert)] + (['original_first_WIN7'] if attempt else [])
    r = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=90)
    return k, r.returncode, r.stdout.strip(), cert
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(run, k, 0): k for k in keys}
    for fut in concurrent.futures.as_completed(futs):
        k, rc, out, cert = fut.result()
        results[k] = {'default_rc': rc, 'default_out': out[-500:]}
        print(k, rc, out.splitlines()[-1] if out else '', flush=True)

# try refutation polarity for default failures (where default rc != 0 and output contains mismatch)
for k in list(results):
    if results[k]['default_rc'] != 0 and 'does not match requested polarity' in results[k]['default_out']:
        try:
            k2, rc, out, cert = run(k, 1)
            results[k]['refute_rc'] = rc
            results[k]['refute_out'] = out[-500:]
            print('WIN7', k, rc, flush=True)
        except subprocess.TimeoutExpired:
            results[k]['refute_rc'] = 'timeout'

(work / 'results.json').write_text(json.dumps(results, indent=2))
print('done')
PY
cat "$OUT/results.json"
