#!/usr/bin/env python3
"""Build the flat S7 results file for independent verification of the sweep's
sensitive certs: (a) all generated LOSS7 children of the 14 LOSS S6s,
(b) the winning WIN7 child of each WIN S6. Cached entries are already
audited in the focus62/frontier dirs, so they are skipped (counted)."""
import json
from pathlib import Path
WORK = Path('/mnt/d/kyouen-focus-certs/s6_sweep')
sweep = json.load(open(WORK / 'sweep_results.json'))
flat = {}
skip_cached = 0
for s6, rec in sweep.items():
    tried = rec['tried']
    if rec['verdict'] == 'LOSS_for_mover':
        for k, tag in tried:
            if tag == 'LOSS7-gen':
                flat[k] = {'default_rc': 0, 'default_out': 'sweep LOSS7-gen'}
            elif tag == 'LOSS7-cached':
                skip_cached += 1
    elif rec['verdict'] == 'WIN_for_mover':
        w = rec['win_child']
        if w is not None:
            tag = dict(tried).get(w)
            if tag == 'WIN7-gen':
                flat[w] = {'default_rc': 1, 'default_out': 'sweep polarity mismatch (refute)',
                           'refute_rc': 0, 'refute_out': 'sweep WIN7-gen'}
            elif tag == 'WIN7-cached':
                skip_cached += 1
(WORK / 'results.json').write_text(json.dumps(flat, indent=2))
print('flat entries:', len(flat), 'skipped cached:', skip_cached)
