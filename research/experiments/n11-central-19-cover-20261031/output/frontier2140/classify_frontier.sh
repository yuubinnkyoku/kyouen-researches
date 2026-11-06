#!/bin/bash
set -euo pipefail
REPO=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches
DIR=$REPO/research/experiments/n11-central-19-cover-20261031
OUT=/mnt/d/kyouen-focus-certs/frontier_classify
mkdir -p "$OUT"
cd "$DIR"
g++ -O3 -std=c++17 -o "$OUT/gen" generate_five_terminal_loss7.cpp
python3 - <<'PY'
import json, subprocess, pathlib, concurrent.futures
import verify_central49_2091_descent_three_swap as vd
WORK = pathlib.Path('/mnt/d/kyouen-focus-certs/frontier_classify')
ctx = vd.context()
frontiers = ctx[7]
union = set()
for s, ch in frontiers.items():
    union |= ch
print('frontier total', len(union), flush=True)
done62 = json.load(open('/mnt/d/kyouen-focus-certs/results.json'))
todo_set = sorted(union - {int(k, 16) for k in done62})
print('todo', len(todo_set), flush=True)
WORK.mkdir(parents=True, exist_ok=True)

def attempt(args, path):
    if path.exists():
        return 0, 'cached'
    try:
        r = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=90)
        return r.returncode, r.stdout.strip()[-300:]
    except subprocess.TimeoutExpired:
        return 'timeout', 'GENERATION TIMEOUT 90s'

def run(root_int):
    k = f'{root_int:032x}'
    cert = WORK / (k + '.cert')
    win7cert = WORK / (k + '.win7.cert')
    gen = str(WORK / 'gen')
    rec = {}
    rc, out = attempt([gen, k, str(cert)], cert)
    rec['default_rc'] = rc
    rec['default_out'] = out
    if rc != 0 and isinstance(out, str) and 'does not match requested polarity' in out:
        rc2, out2 = attempt([gen, k, str(win7cert), 'original_first_WIN7'], win7cert)
        rec['refute_rc'] = rc2
        rec['refute_out'] = out2
    return k, rec

results_path = WORK / 'results.json'
results = json.load(open(results_path)) if results_path.exists() else {}
todo = [r for r in todo_set
        if not ((WORK / (f'{r:032x}.cert')).exists() or (WORK / (f'{r:032x}.win7.cert')).exists())]
print('pending after resume filter:', len(todo), flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(run, r): r for r in todo}
    done_n = 0
    for fut in concurrent.futures.as_completed(futs):
        k, rec = fut.result()
        results[k] = rec
        done_n += 1
        if done_n % 25 == 0:
            print('progress', done_n, '/', len(todo), flush=True)
            results_path.write_text(json.dumps(results, indent=2))
results_path.write_text(json.dumps(results, indent=2))
print('ALL DONE', len(results), flush=True)
PY
echo FRONTIER_CLASSIFY_DONE
