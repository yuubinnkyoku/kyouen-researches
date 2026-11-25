#!/usr/bin/env python3
import json, hashlib, sys
from pathlib import Path
sys.path.insert(0, str(Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')))
import verify_five_terminal_loss7 as vf
WORK = Path('/mnt/d/kyouen-focus-certs')
r = json.load(open(WORK / 'results.json'))
verified = {}
fails = {}
for root, rec in r.items():
    data = None
    parity = None
    if rec.get('default_rc') == 0:
        path = WORK / (root + '.cert')
        header = 'n11-terminal-strategy-v1 original_first_LOSS7 second_to_move_WIN'
        parity = 0
        expected_type = 'LOSS7'
    elif rec.get('refute_rc') == 0:
        path = WORK / (root + '.win7.cert')
        header = 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
        parity = 1
        expected_type = 'WIN7'
    else:
        fails[root] = 'no generated cert'
        continue
    try:
        data = path.read_bytes()
        strategy = vf.parse(data, root, header=header)
        stats = vf.verify(int(root, 16), strategy, winner_parity=parity)
        verified[root] = {
            'type': expected_type,
            'sha256': hashlib.sha256(data).hexdigest(),
            'stats': stats,
        }
        print('PASS', root, expected_type, stats, flush=True)
    except Exception as e:
        fails[root] = str(e)
        print('FAIL', root, e, flush=True)
out = {'verified': verified, 'fails': fails, 'loss': sorted(k for k,v in verified.items() if v['type']=='LOSS7'), 'win': sorted(k for k,v in verified.items() if v['type']=='WIN7')}
(WORK / 'verified.json').write_text(json.dumps(out, indent=2))
print('loss', len(out['loss']), 'win', len(out['win']), 'fails', len(fails))
