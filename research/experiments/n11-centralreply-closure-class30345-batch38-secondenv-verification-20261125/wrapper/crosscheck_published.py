#!/usr/bin/env python3
"""crosscheck_published.py RAWDIR STATUSFILE: internal consistency of the PUBLISHED
batch-38 evidence (regular raw files + status.log): every regular raw's replay
budget/result/nodes must equal its status.log PASS row triple exactly; p1/p2 pairs
identical; replay_done present; forbidden-quadruple header constant; every status
TRUNCATED-RETRY marker must have a matching truncated sidecar WITHOUT replay_done.
Fail-closed: rc!=0 on any problem (an unparseable file is a problem, never a crash)."""
import re, os, sys
rawdir, statusfile = sys.argv[1], sys.argv[2]
HDR = '# exact replay: order=0 (0=count-asc 1=count-desc 2=key-asc 3=s5-count-desc 4=s5-target92) share_tt=0'
def repfields(p):
    t = open(p, 'rb').read().decode()
    m = re.search(r'^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)$', t, re.M)
    fq = re.search(r'# forbidden quadruples: (\d+)', t)
    return (m.groups() if m else None, fq.group(1) if fq else None,
            '# replay_done rows=' in t, t.splitlines()[0])
passrows = {}; problems = []; trunct = 0
for ln in open(statusfile).read().splitlines():
    m = re.match(r'^(\S+) (ai\d{3}) PASS (\d+),(\d+),(\d+)$', ln)
    if m: passrows[m.group(2)] = (m.group(3), m.group(4), m.group(5))
    if 'TRUNCATED-RETRY' in ln: trunct += 1
raws = os.listdir(rawdir)
side = sorted(k for k in raws if '.truncated.' in k)
if trunct != len(side):
    problems.append(f'truncated marker/file count mismatch markers={trunct} sidecars={len(side)}')
for k in side:
    if '# replay_done' in open(rawdir + '/' + k, 'rb').read().decode():
        problems.append(k + ' sidecar carries replay_done')
n = 0
for k in sorted(raws):
    if '.truncated.' in k or not k.endswith('.out'): continue
    n += 1
    kid, p = k.rsplit('.', 2)[0], k.rsplit('.', 2)[1]
    fld, fq, done, hdr = repfields(rawdir + '/' + k)
    if fld is None: problems.append(k + ' no replay line'); continue
    st = passrows.get(kid)
    if st is None: problems.append(k + ' no status PASS row')
    elif st != (fld[4], fld[5], fld[6]):
        problems.append(f'{k} {fld[4]},{fld[5]},{fld[6]} != status {st}')
    if not done: problems.append(k + ' no replay_done')
    if hdr != HDR: problems.append(k + ' header drift')
    if fq != '95670': problems.append(k + ' fq drift ' + str(fq))
    if p == 'p2':
        f1 = repfields(f'{rawdir}/{kid}.p1.out')
        if f1[0] is None: problems.append(kid + ' p1 unparseable')
        elif (f1[0][4], f1[0][5], f1[0][6]) != (fld[4], fld[5], fld[6]):
            problems.append(kid + ' p1/p2 field difference')
print(f'published raws cross-checked: {n}, truncated sidecars: {len(side)}, problems: {len(problems)}')
for p in problems: print(' -', p)
sys.exit(1 if problems else 0)
