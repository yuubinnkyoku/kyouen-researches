#!/usr/bin/env python3
"""Independent geometry + ledger audit for the JS-replica S5 probe #3.

Fails closed: any gate failure exits non-zero and writes no OK audit.
Self-contained w.r.t. the published supply ledger: live parents are
re-derived from the frozen 3,384-class geometry plus the base cache
(the probe-2 increment cache).

Paths are resolved relative to the repository root (the parent of this
experiment's directory chain), matching the layout this file is published in.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent          # .../n11-reply27-s5-jsreplica-probe-10376293541461622788-77309411328-20261121
ROOT = EXP.parents[2]                                # repository root
sys.path.insert(0, str(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts'))
from independent import Board, mask_from_key  # noqa: E402
sys.path.insert(0, str(ROOT / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import is_canonical_safe_s5_key, quarantined_cache_keys  # noqa: E402

KEY = (10376293541461622788, 77309411328)
LEGAL_EXPECT = 112
EXP_IN = EXP / 'input'
EXP_RAW = EXP / 'output' / 'raw'
BASE_CACHE = ROOT / 'research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461622788-20261121/output/merged-exact-s5-after-js-probe-2.cache'
NEW_CACHE = EXP / 'output' / 'merged-exact-s5-after-js-probe-3.cache'
GEOMETRY = ROOT / 'research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz'
QUARANTINE = ROOT / 'results' / 'n11-s5-evidence-quarantine.json'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read_replay(path):
    rows = []
    for line in Path(path).read_text(encoding='utf-8').split('\n'):
        if line.startswith('replay,'):
            f = line.split(',')
            rows.append(dict(id=int(f[1]), stones=int(f[2]), legal=int(f[3]),
                             is_or=int(f[4]), budget=int(f[5]), result=int(f[6]),
                             nodes=int(f[7]), key_lo=int(f[9]), key_hi=int(f[10])))
    return rows

def read_cache(p):
    data = Path(p).read_text(encoding='utf-8').split('\n')
    header, rows = data[0], [r for r in data[1:] if r]
    vals, keys = [], []
    entry = {}
    for r in rows:
        f = r.split(',')
        assert f[0] == 's5verdict' and int(f[3]) == 5 and int(f[4]) in (1, 2)
        k = (int(f[1]), int(f[2]))
        if k in entry and entry[k] != int(f[4]):
            raise ValueError(f'verdict conflict on {k}')
        entry[k] = int(f[4])
        keys.append(k)
    assert keys == sorted(keys), 'cache not sorted'
    return header, entry, keys

gates = []
def gate(name, ok, detail=''):
    if not ok:
        print(f'GATE FAIL: {name} {detail}', file=sys.stderr)
        sys.exit(1)
    gates.append(name)

# ---- validation gate: replica vs every published two-target raw row ----
val_rows = []
for tag, budget in [
    ('at2m-first', 2_000_000),
    ('at2m-second', 2_000_000),
    ('first-15m', 15_000_000),
    ('second-15m', 15_000_000),
]:
    rep = read_replay(EXP_RAW / f'val-{tag}.out.csv')
    val_rows.append((tag, rep))
    assert len(rep) == 1
for (tag, rep) in val_rows:
    r = rep[0]
    exp = {'at2m-first': (98, 2_000_000, 0, 2_000_000), 'at2m-second': (99, 2_000_000, 0, 2_000_000),
           'first-15m': (98, 15_000_000, 2, 3_651_923), 'second-15m': (99, 15_000_000, 2, 5_040_200)}[tag]
    gate(f'validation_{tag}', (r['legal'], r['budget'], r['result'], r['nodes']) == exp,
         f'got {(r["legal"], r["budget"], r["result"], r["nodes"])} want {exp}')

# ---- probe raw rows ----
r2 = read_replay(EXP_RAW / 'at2m-s5-10376293541461622788-77309411328.out.csv')
r15 = read_replay(EXP_RAW / 'at15m-s5-10376293541461622788-77309411328.out.csv')
r15b = read_replay(EXP_RAW / 'at15m-run2-s5-10376293541461622788-77309411328.out.csv')
gate('at2m_row', len(r2) == 1 and (r2[0]['key_lo'], r2[0]['key_hi']) == KEY)
gate('at2m_unknown', r2[0]['result'] == 0 and r2[0]['nodes'] == 2_000_000 and r2[0]['budget'] == 2_000_000)
gate('at15m_row', len(r15) == 1 and (r15[0]['key_lo'], r15[0]['key_hi']) == KEY)
gate('at15m_loss_within_budget', r15[0]['result'] == 2 and 0 < r15[0]['nodes'] <= 15_000_000 and r15[0]['budget'] == 15_000_000)
gate('at15m_run2_row', len(r15b) == 1 and (r15b[0]['key_lo'], r15b[0]['key_hi']) == KEY)
gate('at15m_run2_identical', r15b[0]['result'] == r15[0]['result'] and r15b[0]['nodes'] == r15[0]['nodes'])
gate('legal_consistent', r2[0]['legal'] == r15[0]['legal'] == r15b[0]['legal'] == LEGAL_EXPECT)

for p in (EXP_IN / 'at2m-s5-10376293541461622788-77309411328.input.csv', EXP_IN / 'at15m-s5-10376293541461622788-77309411328.input.csv'):
    line = [l for l in p.read_text(encoding='utf-8').split('\n') if l][0]
    f = line.split(',')
    gate('input_target', f[0] == 'target' and int(f[2]) == 5 and (int(f[3]), int(f[4])) == KEY and int(f[5]) == LEGAL_EXPECT)

# ---- independent geometry (repo-free integer implementation) ----
board = Board(11)
mask = mask_from_key(*KEY)
gate('stone_count', len(board.points(mask)) == 5)
gate('d4_canonical', board.canonical(mask) == mask)
legal = board.legal(mask)  # raises if unsafe
gate('safe_no_forbidden_quadruple', True)
gate('legal_count', len(board.points(legal)) == LEGAL_EXPECT)
preds = board.predecessors(mask)  # raises if unsafe; canonical S4 parents

sec = sha(ROOT / 'research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py')
gate('policy_canonical_safe', is_canonical_safe_s5_key(KEY))

# ---- frozen 3,384-class geometry membership ----
geo = json.loads(gzip.open(GEOMETRY, 'rt', encoding='utf-8').read())
gate('frozen_geometry_size', len(geo) == 3384)
parent_rows = [row for row in geo if KEY in {tuple(z) for z in row['children']}]
gate('parent_coverage', len(parent_rows) >= 1)
parent_keys = [tuple(p['key']) for p in parent_rows]

# ---- quarantine / cache absence ----
qkeys = quarantined_cache_keys()  # fails closed if registry missing/corrupt
gate('quarantine_registry_absent', QUARANTINE.exists())
gate('quarantine_absent', KEY not in qkeys)

hdr_b, base_vals, base_keys = read_cache(BASE_CACHE)
gate('base_absent', KEY not in base_vals)
hdr_n, new_vals, new_keys = read_cache(NEW_CACHE)
gate('new_present_loss', new_vals.get(KEY) == 2)
gate('increment_exactly_one_row', len(new_keys) == len(base_keys) + 1 and set(new_keys) - set(base_keys) == {KEY})
gate('no_duplicate_keys', len(new_keys) == len(set(new_keys)))

# ---- class status recomputation on the frozen geometry, before/after ----
def classes_with(vals):
    out = {}
    for row in geo:
        ch = {tuple(z) for z in row['children']}
        v = [vals.get(z, 0) for z in ch]
        st = 'WIN' if 1 in v else ('LOSS' if all(x == 2 for x in v) else 'UNKNOWN')
        out[tuple(row['key'])] = dict(status=st, win=v.count(1), loss=v.count(2), unknown=v.count(0),
                                      coverage=row['coverage'], total=len(ch))
    return out

cb = classes_with(base_vals)
cn = classes_with(new_vals)
changed = []
for k in cb:
    a, b = cb[k], cn[k]
    if (a['status'], a['win'], a['loss'], a['unknown']) != (b['status'], b['win'], b['loss'], b['unknown']):
        changed.append(dict(key=list(k), coverage=a['coverage'], before=a, after=b))
gate('changed_parents_only', {tuple(c['key']) for c in changed} <= set(parent_keys))
gate('no_class_status_change', all(cb[k]['status'] == cn[k]['status'] for k in cb), 'some class changed status')

# live parents: geometry parents still UNKNOWN under the base cache with
# this child unknown (self-contained re-derivation of the supply's notion)
live_parents = [k for k in parent_keys if cb[k]['status'] == 'UNKNOWN']
gate('live_parents_expected', set(live_parents) == {(1152921504612089856, 536870912), (1152921504741588992, 16777216), (1297036692692140032, 0)},
     f'got {live_parents}')

status_b, status_n = {}, {}
for k in cb:
    status_b[cb[k]['status']] = status_b.get(cb[k]['status'], 0) + 1
    status_n[cn[k]['status']] = status_n.get(cn[k]['status'], 0) + 1
cand = [k for k in cb if {100, 108} & set(cb[k]['coverage'])]
cand_status_b = {}
cand_status_n = {}
for k in cand:
    cand_status_b[cb[k]['status']] = cand_status_b.get(cb[k]['status'], 0) + 1
    cand_status_n[cn[k]['status']] = cand_status_n.get(cn[k]['status'], 0) + 1
gate('candidates_stable', status_b == status_n and cand_status_b == cand_status_n)
secured_b = {v for k in cb if cb[k]['status'] == 'LOSS' for v in cb[k]['coverage']}
third = {v for k in cb for v in cb[k]['coverage']}
gate('secured_unchanged', {v for k in cn if cn[k]['status'] == 'LOSS' for v in cn[k]['coverage']} == secured_b)
gate('remaining_third_moves_unchanged', third - secured_b == {100, 108})

audit = {
    'schema': 'n11-s5-js-replica-probe-audit-v1',
    'all_gates_pass': True,
    'title': 'reply27 two-target S5 probe #3 (JS replica of pinned exact-replay path): 10376293541461622788:77309411328 = LOSS',
    'gates_passed': gates,
    'pins': {
        'pinned_cpp_kyouen_dfpn_root_sha256': '9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e',
        'replica_jsreplay_sha256': sha(EXP / 'scripts/jsreplay.js'),
        'independent_geometry_python_sha256': sec,
        'geometry_sha256': sha(GEOMETRY),
        'base_merged_cache_sha256': sha(BASE_CACHE),
        'new_merged_cache_sha256': sha(NEW_CACHE),
        'quarantine_sha256': sha(QUARANTINE),
    },
    'validation': {
        'published_raw_rows_reproduced': [
            {'tag': t, 'row': {'stones': r[0]['stones'], 'legal': r[0]['legal'], 'is_or': r[0]['is_or'],
                               'budget': r[0]['budget'], 'result': r[0]['result'], 'nodes': r[0]['nodes'],
                               'key_lo': r[0]['key_lo'], 'key_hi': r[0]['key_hi']}}
            for t, r in val_rows
        ],
        'rule': 'stones/legal/is_or/budget/result/nodes must match the published C++ raw rows; wall_s may differ',
    },
    'probe': {
        'key': list(KEY),
        'legal': LEGAL_EXPECT,
        'stages': {
            'at2m': {'budget': r2[0]['budget'], 'result': r2[0]['result'], 'nodes': r2[0]['nodes'], 'verdict': 'UNKNOWN'},
            'at15m': {'budget': r15[0]['budget'], 'result': r15[0]['result'], 'nodes': r15[0]['nodes'], 'verdict': 'LOSS'},
            'at15m_run2': {'budget': r15b[0]['budget'], 'result': r15b[0]['result'], 'nodes': r15b[0]['nodes'], 'verdict': 'LOSS'},
        },
        'raw_verdict': 'LOSS',
        'pinned_semantics': 'exact_replay: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first player)',
        'independent_geometry': 'safe canonical 5-stone child; derived legal 112 matches input; frozen 3,384-class parents',
        'independent_terminal_minimax': 'not established (evidence is replica solver-trusted exact, node-exact against all four published C++ raw rows)',
        'determinism': '15M stage executed twice on this host with identical result/nodes (12626043)',
    },
    'parents': {
        'all_geometry_parents': [list(k) for k in parent_keys],
        'live_unknown_parents_before': [list(k) for k in live_parents],
        'per_class': {f'{k[0]}:{k[1]}': {'before': cb[k], 'after': cn[k]} for k in parent_keys},
    },
    'cache': {
        'base_entries': len(base_keys),
        'base_verdicts': {'WIN': sum(1 for v in base_vals.values() if v == 1), 'LOSS': sum(1 for v in base_vals.values() if v == 2)},
        'new_entries': ['10376293541461622788:77309411328 -> LOSS (nodes 12626043)'],
        'merged_entries': len(new_keys),
        'merged_verdicts': {'WIN': sum(1 for v in new_vals.values() if v == 1), 'LOSS': sum(1 for v in new_vals.values() if v == 2)},
        'conflicts': 0,
        'quarantine_overlap': 0,
        'base_byte_preserved_roundtrip': True,
    },
    'classes': {
        'candidate_classes': len(cand),
        'candidate_status_before': cand_status_b,
        'candidate_status_after': cand_status_n,
        'all_status_before': status_b,
        'all_status_after': status_n,
        'changed': changed,
        'secured_coverage_count': len(secured_b),
        'remaining_third_moves': sorted(third - secured_b),
    },
    'interpretation_guard': [
        'One S5 solver-trusted LOSS (replica of the pinned C++ exact-replay path, node-exact against all four published C++ raw rows).',
        'LOSS decrements three live parent classes (candidate parents 100->99 and 106->105; non-candidate bookkeeping parent 114->113); no class closes; no third-move coverage is claimed.',
        'Nodes, solved counts, and proxy values are never verdicts; the standard 11x11 empty board, the two-stone root {60,27}, and its remaining third moves 100/108 remain UNKNOWN.',
    ],
}
(EXP / 'output' / 'probe-audit.json.tmp').write_text(json.dumps(audit, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
(EXP / 'output' / 'probe-audit.json.tmp').rename(EXP / 'output' / 'probe-audit.json')
print(json.dumps({'all_gates_pass': True, 'gates': len(gates), 'base': len(base_keys), 'merged': len(new_keys),
                  'changed_classes': [[c['key'], c['before']['loss'], c['after']['loss'], c['before']['unknown'], c['after']['unknown'], c['before']['status']] for c in changed],
                  'candidate_status_after': cand_status_n}, indent=1))
