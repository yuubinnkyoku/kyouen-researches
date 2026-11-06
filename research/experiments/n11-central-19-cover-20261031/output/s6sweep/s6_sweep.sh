#!/bin/bash
set -euo pipefail
REPO=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches
DIR=$REPO/research/experiments/n11-central-19-cover-20261031
OUT=/mnt/d/kyouen-focus-certs/s6_sweep
mkdir -p "$OUT"
cd "$DIR"
g++ -O3 -std=c++17 -o "$OUT/gen" generate_five_terminal_loss7.cpp
python3 - <<'PY'
import json, subprocess, pathlib, concurrent.futures, sys
sys.path.insert(0, str(pathlib.Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')))
import verify_conditional_s6_cover_46 as base
import verify_central49_2154_two_swap_descent as source
WORK = pathlib.Path('/mnt/d/kyouen-focus-certs/s6_sweep')

data = base.reconstruct()
s5, incidence, costs = data[1:4]
s5set = set(range(len(s5)))
universe = sorted(k for k, v in incidence.items() if set(v) & s5set)
print('universe', len(universe), 's5', len(s5), flush=True)

cache = {}
for d in (pathlib.Path('/mnt/d/kyouen-focus-certs'), pathlib.Path('/mnt/d/kyouen-focus-certs/frontier_classify')):
    p = d / 'verified.json'
    if p.exists():
        for k, rec in json.load(open(p)).get('verified', {}).items():
            cache[int(k, 16)] = rec['type']
print('cached verdicts', len(cache), flush=True)

def attempt(args, path):
    if path.exists():
        return 0, 'cached'
    try:
        r = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=300)
        return r.returncode, r.stdout.strip()[-300:]
    except subprocess.TimeoutExpired:
        return 'timeout', 'GEN TIMEOUT 300s'

def job(s6):
    ch = sorted(source.fast_frontier(s6))
    tried = []
    timeouts = []
    win_child = None
    gen = str(WORK / 'gen')
    for c in ch:
        v = cache.get(c)
        if v == 'WIN7':
            tried.append((f'{c:032x}', 'WIN7-cached'))
            win_child = c
            break
        if v == 'LOSS7':
            tried.append((f'{c:032x}', 'LOSS7-cached'))
            continue
        k = f'{c:032x}'
        cert = WORK / (k + '.cert')
        win7cert = WORK / (k + '.win7.cert')
        rc, out = attempt([gen, k, str(cert)], cert)
        if rc == 'timeout':
            timeouts.append(k)
            tried.append((k, 'timeout'))
            continue
        if rc == 0:
            tried.append((k, 'LOSS7-gen'))
            continue
        if isinstance(out, str) and 'does not match requested polarity' in out:
            rc2, out2 = attempt([gen, k, str(win7cert), 'original_first_WIN7'], win7cert)
            if rc2 == 0:
                tried.append((k, 'WIN7-gen'))
                win_child = c
                break
            if rc2 == 'timeout':
                timeouts.append(k)
                tried.append((k, 'timeout-refute'))
                continue
            tried.append((k, 'other-fail'))
        else:
            tried.append((k, 'other-fail'))
    if win_child is not None:
        verdict = 'WIN_for_mover'
    elif timeouts:
        verdict = 'TIMEOUT'
    else:
        verdict = 'LOSS_for_mover'
    return f'{s6:032x}', {'children': len(ch), 'tried': tried,
                            'win_child': (f'{win_child:032x}' if win_child is not None else None),
                            'timeouts': timeouts, 'verdict': verdict}

rp = WORK / 'sweep_results.json'
results = json.load(open(rp)) if rp.exists() else {}
todo = [s for s in universe if results.get(f'{s:032x}', {}).get('verdict') not in ('WIN_for_mover', 'LOSS_for_mover')]
print('todo', len(todo), flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(job, s): s for s in todo}
    done_n = 0
    for fut in concurrent.futures.as_completed(futs):
        k, rec = fut.result()
        results[k] = rec
        done_n += 1
        if done_n % 25 == 0:
            print('progress', done_n, '/', len(todo), flush=True)
            rp.write_text(json.dumps(results))
rp.write_text(json.dumps(results))
summ = {}
for r in results.values():
    summ[r['verdict']] = summ.get(r['verdict'], 0) + 1
print(json.dumps(summ, indent=2))
print('ALL DONE', len(results), flush=True)
PY
echo S6_SWEEP_DONE
