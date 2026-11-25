#!/bin/bash
W=$1
D=/home/user/work/sweep35
CAP=30000000
python3 - "$W" <<'PY'
import json, subprocess, sys, time, os
W = int(sys.argv[1])
D = '/home/user/work/sweep35'
roots = json.load(open(f'{D}/roots-reprobe5.json'))
mine = roots[W::2]
outf = f'{D}/output/probe-recordsfix-w{W}.jsonl'
logf = f'{D}/output/workerfix{W}.log'
def log(s):
    with open(logf,'a') as f: f.write(f'{time.strftime("%H:%M:%S")} {s}\n')
log(f'fix worker {W} starting, {len(mine)} roots')
CAP=30000000
for idx, item in enumerate(mine):
    root = item['root']; child = item['child']; bit = item['bit']
    for ordering in (1, 0):
        rec_path = f'{D}/output/.tmpfix-{W}-{root}-{ordering}.jsonl'
        if os.path.exists(rec_path): os.remove(rec_path)
        t0 = time.time()
        cmd = ['node','--experimental-strip-types', '/home/user/work/inputs/runner_v17.ts',
               '--bits',str(bit),'--depth','10','--cap',str(CAP),'--andclose',str(ordering),
               '--child',child,'--out',rec_path]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=285)
            rc = r.returncode
            text = r.stdout.strip()
        except subprocess.TimeoutExpired as e:
            rc, text = 'timeout', (e.stdout or b'').decode() if e.stdout else ''
        wall = round(time.time()-t0, 1)
        control, result = None, None
        if os.path.exists(rec_path):
            for line in open(rec_path):
                line=line.strip()
                if not line: continue
                o=json.loads(line)
                if 'control' in o: control=o
                else: result=o
        rec = {'root': root, 'ordering': 'andclose%d'%ordering, 'cap': CAP,
               'worker': W, 'seq': idx, 'covered_rows': item['rows'], 'reprobe_round': 2,
               'note': 'corrected raw child (canon_hex child bug in round 1)'}
        if rc=='timeout':
            rec['error']='timeout-285s'; rec['control']=control
        elif rc!=0:
            rec['error']=f'exit-{rc}'; rec['stdout_tail']=text[-200:]
        else:
            rec['control']=control; rec['result']=result
        with open(outf,'a') as f: f.write(json.dumps(rec)+'\n')
        log(f'{root} ordering={ordering} rc={rc} wall={wall}s nodes={result["nodes"] if result else "?"} loss={result["loss"] if result else "?"} capped={result["capped"] if result else "?"}')
    os.path.exists(rec_path) and os.remove(rec_path)
log(f'fix worker {W} done')
PY
