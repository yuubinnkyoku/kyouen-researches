#!/usr/bin/env python3
"""Calibration bank runner for third_impl.js against published S5 verdict cache rows.

Usage: python3 run_bank.py <cache.csv> <outdir> <deadline_seconds_from_start> [--wins N] [--loss-sample N]
Rows: s5verdict,<lo>,<hi>,5,<verdict>,<nodes>. Idempotent (skips done rows). Honest outputs
only: each result file records the full stdout line of one clean/aborted run.
"""
import subprocess, sys, time, os, argparse

ap = argparse.ArgumentParser()
ap.add_argument('cache'); ap.add_argument('outdir'); ap.add_argument('deadline', type=int)
ap.add_argument('--wins', default='all'); ap.add_argument('--loss-sample', type=int, default=120)
ap.add_argument('--cap', default='400000000'); ap.add_argument('--wallcap', default='40')
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)
rows = []
with open(a.cache) as f:
    for line in f:
        line = line.strip()
        if not line.startswith('s5verdict,'): continue
        fld = line.split(',')
        lo, hi, stones, verdict, nodes = fld[1], fld[2], int(fld[3]), int(fld[4]), fld[5]
        if stones != 5: continue
        rows.append((lo, hi, verdict, nodes))
wins = [r for r in rows if r[2] == 1]
loss = [r for r in rows if r[2] == 2]
tasks = wins if a.wins == 'all' else wins[:int(a.wins)]
ln = a.loss_sample
tasks += loss[:ln // 2] + loss[-(ln - ln // 2):] if ln > 0 else []
t0 = time.time()
done = agree = disagree = runlimit = gate = 0
for lo, hi, verdict, nodes in tasks:
    key = lo + '_' + hi
    out = os.path.join(a.outdir, key + '.txt')
    if os.path.exists(out) and os.path.getsize(out) > 0:
        continue
    if time.time() - t0 > a.deadline:
        print('DEADLINE stop at', done, 'done')
        break
    r = subprocess.run(['node', 'third_impl.js', '--lo=' + lo, '--hi=' + hi, '--stones=5',
                       '--legal=-1', '--row=' + key, '--cap=' + a.cap, '--wallcap=' + a.wallcap,
                       '--memo-power=22'], capture_output=True, text=True, timeout=int(a.wallcap) + 80)
    line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ('CRASH rc=' + str(r.returncode))
    with open(out, 'w') as g:
        g.write('expect,' + str(verdict) + ',' + nodes + '\n' + line + '\n')
    done += 1
    if 'GATE_FAIL' in line: gate += 1
    elif ',0,' in line and 'runlimit' in line: runlimit += 1
    else:
        res = line.split(',')[5]
        if int(res) == verdict: agree += 1
        else: disagree += 1
print('done', done, 'agree', agree, 'disagree', disagree, 'runlimit', runlimit, 'gatefail', gate,
      'remaining', len(tasks) - done - sum(1 for lo, hi, v, n in tasks if os.path.exists(os.path.join(a.outdir, lo + '_' + hi + '.txt'))))