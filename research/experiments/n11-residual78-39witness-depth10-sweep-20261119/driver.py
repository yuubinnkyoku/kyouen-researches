#!/usr/bin/env python3
# 43-candidate add-one-stone witness sweep (86 stranded five-parent target rows).
# runner v17 (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59), depth 10, cap 30M,
# both AND orderings, pilot_d6 control, RAW maxbit sibling child (canon_hex forbidden).
# Usage: python3 driver.py <worker_id>
import json, subprocess, sys, time, os

D = '/home/user/work/sweep39'
RUNNER = '/home/user/work/runner_v17.ts'
CAP = 30000000

def log(s):
    with open(f'{D}/output/worker{W}.log', 'a') as f:
        f.write(time.strftime('%H:%M:%S') + ' ' + s + '\n')

W = int(sys.argv[1])
roots = json.load(open(f'{D}/roots.json'))
mine = roots[W::2]
outf = f'{D}/output/probe-records-w{W}.jsonl'
done = set()
if os.path.exists(outf):
    for line in open(outf):
        try:
            d = json.loads(line)
            if 'result' in d and d.get('error') is None:
                done.add((d['root'], d['ordering']))
        except Exception:
            pass
log(f'worker {W} starting, {len(mine)} roots, {len(done)} already recorded')
for idx, item in enumerate(mine):
    root = item['root']; child = item['child']; bit = item['bit']
    for ordering in (1, 0):
        key = (root, 'andclose%d' % ordering)
        if key in done:
            continue
        rec_path = f'{D}/output/.tmp-{W}-{root}-{ordering}.jsonl'
        if os.path.exists(rec_path):
            os.remove(rec_path)
        t0 = time.time()
        cmd = ['node', '--experimental-strip-types', RUNNER,
               '--bits', str(bit), '--depth', '10', '--cap', str(CAP),
               '--andclose', str(ordering), '--child', child, '--out', rec_path]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=285)
            rc, text = r.returncode, r.stdout.strip()
        except subprocess.TimeoutExpired as e:
            rc, text = 'timeout', ''
        wall = round(time.time() - t0, 1)
        control = result = None
        if os.path.exists(rec_path):
            for line in open(rec_path):
                line = line.strip()
                if not line:
                    continue
                o = json.loads(line)
                if 'control' in o:
                    control = o
                else:
                    result = o
        rec = {'root': root, 'ordering': 'andclose%d' % ordering, 'cap': CAP,
               'worker': W, 'seq': idx, 'covered_rows': item['rows'],
               'bit': bit, 'child': child}
        if rc == 'timeout':
            rec['error'] = 'timeout-285s'; rec['control'] = control
        elif rc != 0:
            rec['error'] = 'exit-%s' % rc; rec['stdout_tail'] = text[-200:]
        else:
            rec['control'] = control; rec['result'] = result
        with open(outf, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        log(f'{root} ordering={ordering} rc={rc} wall={wall}s nodes={result["nodes"] if result else "?"} loss={result["loss"] if result else "?"} capped={result["capped"] if result else "?"}')
        if os.path.exists(rec_path):
            os.remove(rec_path)
log(f'worker {W} done')
