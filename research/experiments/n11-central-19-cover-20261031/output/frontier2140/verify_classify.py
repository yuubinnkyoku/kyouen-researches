#!/usr/bin/env python3
"""Independent audit for a classification results dir (results.json + *.cert).
Usage: python3 verify_classify.py [WORK_DIR]  (default /mnt/d/kyouen-focus-certs)
"""
import json, hashlib, sys
from pathlib import Path
from multiprocessing import Pool
sys.path.insert(0, str(Path(r'/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/n11-central-19-cover-20261031')))
import verify_five_terminal_loss7 as vf
WORK = Path(sys.argv[1] if len(sys.argv) > 1 else '/mnt/d/kyouen-focus-certs')


def one(item):
    root, rec = item
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
        return root, None, (rec.get('default_out', '') + ' / ' + rec.get('refute_out', ''))
    try:
        data = path.read_bytes()
        strategy = vf.parse(data, root, header=header)
        stats = vf.verify(int(root, 16), strategy, winner_parity=parity)
        return root, {'type': expected_type, 'sha256': hashlib.sha256(data).hexdigest(), 'stats': stats}, None
    except Exception as e:
        return root, None, str(e)


def main():
    r = json.load(open(WORK / 'results.json'))
    verified = {}
    fails = {}
    with Pool(8) as pool:
        for root, rec, err in pool.imap_unordered(one, sorted(r.items())):
            if rec is not None:
                verified[root] = rec
                print('PASS', root, rec['type'], flush=True)
            else:
                fails[root] = err
                print('FAIL', root, err, flush=True)
    out = {'verified': verified, 'fails': fails,
           'loss': sorted(k for k, v in verified.items() if v['type'] == 'LOSS7'),
           'win': sorted(k for k, v in verified.items() if v['type'] == 'WIN7')}
    (WORK / 'verified.json').write_text(json.dumps(out, indent=2))
    print('loss', len(out['loss']), 'win', len(out['win']), 'fails', len(fails))


if __name__ == '__main__':
    main()
