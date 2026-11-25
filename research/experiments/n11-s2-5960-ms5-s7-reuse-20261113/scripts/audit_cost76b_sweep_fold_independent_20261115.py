#!/usr/bin/env python3
"""Independent second audit of the cost-76b sweep + certificates + fold
bookkeeping (long-lane second-verification session, 2026-11-15).

Audits, from published main artifacts only:
  output/class2-lane-cost76b-inflight-20261115.json               (claim, completed)
  output/class2-lane-cost76b-raw-batch{1..10}-20261115.jsonl      (raw sweep records)
  output/class2-lane-cost76b-v16-determinism-rerun-20261115.jsonl (batch-5 rerun)
  output/class2-lane-cost76b-v15-crosscheck-20261115.jsonl       (cross-engine anchors)
  output/class2-lane-cost76b-certificates/ (bit72 whole, bit96 part1of2+part2of2)
  output/tmp-cost76b/ (receipts, bigint/tsverify summaries, consumed dumps, legal-moves)
  output/class-frontier-merged-cost65l-74g-69i-recompute-20261115.json  (head 1277)
  output/class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv
  output/class-frontier-cost76b-receipts-recompute-20261115.json        (head 1280)
  output/class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv
  output/class2-lane-merged-1277-certificates-second-verification-20261115.json

This audit runs AFTER the sweeping lane's one-commit landing (sweep +
certificates + fold with embedded controls), so it is a second, independent
post-hoc audit rather than a pre-audit. In addition to geometry and
bookkeeping checks it RE-RUNS the published Bareiss replay verifier
(verify_cost73h_win7_bareiss_independent.py) and the rational third-system
verifier (verify_cost75d_win7_rational_independent.py) on the joined
certificate bytes and asserts the consumed winner-state sets agree with the
published fold-input dumps at the distinct level (the 76b dumps hold the
per-subroot visited multiset; the distinct level equals the certificate rows).

Independent method: Python standard library only; exact-integer Bareiss 4x4
determinants; an independent 8-element D4 board-group canonicalization; no
repository engine/solver/cache; no floating point.

Writes class2-lane-cost76b-independent-second-audit-20261115.json.
Exit code 0 iff every check passes.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CERTS = OUT / 'class2-lane-cost76b-certificates'
TMP = OUT / 'tmp-cost76b'
SCRIPTS = HERE / 'scripts'

CHILD_HEX = '00000000000000801302000000200000'
PARENT1_HEX = '00000000000000801202000000200000'
WIN_BITS = [72, 96]
ROOTS = {72: '00000000000001801302000000200000',
         96: '00000001000000801302000000200000'}
CHILD75D_HEX = '00000000000040801202000000200000'
WIN75D_BITS = [12, 40, 92, 111]
HEAD77_BLOB = '8d96b48273248073958b327ff91f7aecccd09944'
TOTAL_NODES = 107_961_863

N = 11
XR = [i % N for i in range(N * N)]
YR = [i // N for i in range(N * N)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(N * N)]


def det4(a, b, c, d):
    mm = [[QR[a], XR[a], YR[a], 1],
          [QR[b], XR[b], YR[b], 1],
          [QR[c], XR[c], YR[c], 1],
          [QR[d], XR[d], YR[d], 1]]
    prev = 1
    for k in range(3):
        if mm[k][k] == 0:
            for r in range(k + 1, 4):
                if mm[r][k] != 0:
                    mm[k], mm[r] = mm[r], mm[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                mm[i][j] = (mm[i][j] * mm[k][k] - mm[i][k] * mm[k][j]) // prev
        prev = mm[k][k]
    return mm[3][3]


def d4_canonical(pattern):
    stones = [i for i in range(N * N) if (pattern >> i) & 1]
    best = None
    for t in range(8):
        v = 0
        for i in stones:
            x, y = XR[i], YR[i]
            if t == 0:
                nx, ny = x, y
            elif t == 1:
                nx, ny = N - 1 - y, x
            elif t == 2:
                nx, ny = N - 1 - x, N - 1 - y
            elif t == 3:
                nx, ny = y, N - 1 - x
            elif t == 4:
                nx, ny = x, N - 1 - y
            elif t == 5:
                nx, ny = N - 1 - x, y
            elif t == 6:
                nx, ny = y, x
            else:
                nx, ny = N - 1 - y, N - 1 - x
            v |= 1 << (nx + N * ny)
        if best is None or v < best:
            best = v
    return best


def legal_cells(pattern):
    """Empty cells not collinear with any 3 placed stones (exact Bareiss 4x4)."""
    stones = [i for i in range(N * N) if (pattern >> i) & 1]
    forbidden = 0
    for i in range(len(stones)):
        for j in range(i + 1, len(stones)):
            for k in range(j + 1, len(stones)):
                for d in range(N * N):
                    if (pattern >> d) & 1:
                        continue
                    if det4(stones[i], stones[j], stones[k], d) == 0:
                        forbidden |= 1 << d
    return sorted(p for p in range(N * N)
                  if not (pattern >> p) & 1 and not (forbidden >> p) & 1)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def main():
    failures = []

    def check(name, ok, detail=''):
        status = 'PASS' if ok else 'FAIL'
        print(f'[{status}] {name}' + (f' - {detail}' if detail else ''))
        if not ok:
            failures.append(name)
        return ok

    child = int(CHILD_HEX, 16)
    parent1 = int(PARENT1_HEX, 16)

    # ---- claim-level assertions -------------------------------------------
    claim = json.loads((OUT / 'class2-lane-cost76b-inflight-20261115.json').read_text())
    check('claim status is completed (sweep + certificates + fold)',
          claim['status'] == 'completed (sweep + WIN7 certificates + receipts fold)',
          claim['status'])
    check('claim chain head at claim is 1277 with the baseline blob sha',
          claim['chain_head_at_claim'].startswith('1277/6570/518896/4840/382619')
          and HEAD77_BLOB in claim['chain_head_at_claim'])
    check('claim s6 child and stones match the audit constants',
          claim['s6_child'] == CHILD_HEX
          and sorted(claim['child_stones_bit_indices']) == [21, 49, 56, 57, 60, 71])
    check('claim demand is c1=0,c2=1,c4=0 at baseline 1277',
          claim['demand'] == {'c1': 0, 'c2': 1, 'c4': 0})

    # ---- geometry ----------------------------------------------------------
    stones = [i for i in range(121) if (child >> i) & 1]
    check('child decodes to exactly 6 stones [21,49,56,57,60,71]',
          sorted(stones) == [21, 49, 56, 57, 60, 71], f'{sorted(stones)}')
    check('child pattern is D4-canonical',
          format(d4_canonical(child), '032x') == CHILD_HEX)

    cand = legal_cells(child)
    check('independent legal-candidate enumeration is bit-exact with the '
          'claim (76 candidates, Bareiss 4x4)',
          cand == claim['legal_candidates'],
          f'independent {len(cand)} vs claim {len(claim["legal_candidates"])}')
    check('edge cost 76 equals the independent candidate count',
          claim['s6_s7_edge_cost'] == len(cand) == 76)

    # one-stone deletions
    orbits = {s: d4_canonical(child & ~(1 << s)) for s in stones}
    check('exactly one deletion orbit equals the open parent (the second '
          'coverable class-2 target S5)',
          sum(1 for v in orbits.values() if v == parent1) == 1,
          'del ' + str([s for s in stones if orbits[s] == parent1][0]))
    del_open = [s for s in stones if orbits[s] == parent1][0]
    check('the open lift deletion is bit 56 (claim prose)',
          del_open == 56, f'del {del_open}')
    check('del-56 is raw bit-exact the parent1 hex (not merely D4-canon)',
          (child & ~(1 << 56)) == parent1)
    check('the six deletion orbits are pairwise distinct',
          len(set(orbits.values())) == 6)

    # ---- head-1277 -> head-1280 bookkeeping --------------------------------
    head77 = json.loads((OUT / 'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json').read_text())
    fam77 = head77['frontier_after_merged']
    check('baseline head is 1277/6570/518896/4840/382619',
          [fam77['solved_s6_in_manifest'], fam77['unique_remaining_s6'],
           fam77['sum_remaining_cost'], fam77['s6_needed_by_open_classes'],
           fam77['cost_needed_by_open_classes']] == [1277, 6570, 518896, 4840, 382619])
    head77_bytes = (OUT / 'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json').read_bytes()
    check('baseline head JSON bytes reproduce the canonical blob sha '
          '8d96b482... (byte-identical fetch of main)',
          git_blob_sha(head77_bytes) == HEAD77_BLOB, f'{len(head77_bytes)} bytes')

    head80 = json.loads((OUT / 'class-frontier-cost76b-receipts-recompute-20261115.json').read_text())
    fam80 = head80['frontier_after_cost76b']
    check('post-fold head is 1280/6567/518678/4837/382401',
          [fam80['solved_s6_in_manifest'], fam80['unique_remaining_s6'],
           fam80['sum_remaining_cost'], fam80['s6_needed_by_open_classes'],
           fam80['cost_needed_by_open_classes']] == [1280, 6567, 518678, 4837, 382401])
    check('solved delta is +3 (equals the 2 receipts in-manifest marginal 3)',
          fam80['solved_s6_in_manifest'] - fam77['solved_s6_in_manifest'] == 3)
    check('unique-remaining delta is -3',
          fam77['unique_remaining_s6'] - fam80['unique_remaining_s6'] == 3)
    check('remaining-cost delta is -218 (= 76 + 69 + 73 child rows)',
          fam77['sum_remaining_cost'] - fam80['sum_remaining_cost'] == 218)
    check('remaining_s5_orbits unchanged at 174 (no S5 closed by this fold)',
          fam77['remaining_s5_orbits'] == fam80['remaining_s5_orbits'] == 174)

    # blob shas of the three published fold outputs vs the claim
    fold = claim['fold']
    for key, fname in [('head_json', 'class-frontier-cost76b-receipts-recompute-20261115.json'),
                       ('ranking_csv', 'class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv'),
                       ('top_candidates_csv', 'class-frontier-top-candidates-s6-after-cost76b-receipts-20261115.csv')]:
        data = (OUT / fname).read_bytes()
        check(f'fold output {key} bytes+git blob sha match the claim '
              f'({len(data)} bytes)',
              git_blob_sha(data) == fold['output_blob_shas'][key]
              and len(data) == fold[f'{key}_bytes'])
    check('head-1280 baseline_main references the reproduced head-1277 blob sha',
          HEAD77_BLOB in head80['baseline_main'])

    rank77 = {}
    for line in (OUT / 'class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv').read_text().strip().splitlines()[1:]:
        h, cls, rem, cost = line.split(',')
        rank77[h] = (int(cls), int(rem), int(cost))
    rank80 = {}
    for line in (OUT / 'class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv').read_text().strip().splitlines()[1:]:
        h, cls, rem, cost = line.split(',')
        rank80[h] = (int(cls), int(rem), int(cost))
    check('ranking 1277: parent1 open at 2/17/1325',
          rank77.get(PARENT1_HEX) == (2, 17, 1325), f'{rank77.get(PARENT1_HEX)}')
    check('ranking 1280: parent1 open at 2/16/1249 (child row cost 76 closed)',
          rank80.get(PARENT1_HEX) == (2, 16, 1249), f'{rank80.get(PARENT1_HEX)}')
    s5_b = '00000000000000801202000040000000'
    check('ranking: bit96 in-manifest parent ...8012020000400000 43/2984 -> '
          '42/2915 (row cost 69)',
          rank77.get(s5_b) == (2, 43, 2984) and rank80.get(s5_b) == (2, 42, 2915),
          f'{rank77.get(s5_b)} -> {rank80.get(s5_b)}')
    s5_c = '00000000000000403800000008000000'
    check('ranking: bit72 in-manifest parent ...403800000008000000 52/3742 -> '
          '51/3669 (row cost 73)',
          rank77.get(s5_c) == (2, 52, 3742) and rank80.get(s5_c) == (2, 51, 3669),
          f'{rank77.get(s5_c)} -> {rank80.get(s5_c)}')
    changed = {h for h in set(rank77) | set(rank80)
               if rank77.get(h) != rank80.get(h)}
    check('exactly three S5 rows changed between the 1277 and 1280 rankings',
          changed == {PARENT1_HEX, s5_b, s5_c}, f'{sorted(changed)}')
    absent = [format(orbits[s], '032x') for s in stones
              if orbits[s] != parent1
              and format(orbits[s], '032x') not in rank77
              and format(orbits[s], '032x') not in rank80]
    check('the other five deletion orbits are absent from both open rankings '
          '(already closed at 1277)', len(absent) == 5, f'{len(absent)}/5 absent')

    # ---- raw batches -------------------------------------------------------
    recs = {}
    total_nodes = 0
    batch_bits = {}
    for b in range(1, 11):
        path = OUT / f'class2-lane-cost76b-raw-batch{b}-20261115.jsonl'
        lines = [json.loads(x) for x in path.read_text().strip().splitlines()]
        pilot = lines[0]
        check(f'batch {b}: pilot is d6 control loss=false nodes=3402',
              pilot == {'control': 'pilot_d6', 'loss': False, 'nodes': 3402,
                        'capped': False})
        bits = []
        for r in lines[1:]:
            bits.append(r['bit'])
            if r['bit'] in recs:
                failures.append(f'bit {r["bit"]} duplicated across batches')
            recs[r['bit']] = r
            total_nodes += r['nodes']
        batch_bits[b] = bits
        check(f'batch {b}: {len(bits)} candidates (9x8 + 1x4 plan)',
              len(bits) == (8 if b < 10 else 4), f'{len(bits)}')
    check('all 76 candidates appear exactly once and equal the independent '
          'enumeration', sorted(recs) == cand and len(recs) == 76)
    win_bits = sorted(b for b, r in recs.items() if r['loss'])
    capped_bits = sorted(b for b, r in recs.items() if r['capped'])
    check('WIN7-D10 bits are exactly [72, 96]', win_bits == WIN_BITS, f'{win_bits}')
    check('capped bits: none', capped_bits == [], f'{capped_bits}')
    check('refuted-d10 count is 74 (76 - 2 WIN)', 76 - len(win_bits) == 74)
    ranges = {tuple(r['terminalStoneRange']) for r in recs.values()}
    check('all terminal stone ranges are [13, 17]', ranges == {(13, 17)})
    check('candidate node total equals the published 107,961,863',
          total_nodes == TOTAL_NODES, f'{total_nodes}')
    for bit in WIN_BITS:
        check(f'WIN bit {bit} root equals child XOR (1<<bit)',
              (child ^ (1 << bit)) == int(ROOTS[bit], 16))
    win_nodes = {b: recs[b]['nodes'] for b in WIN_BITS}
    check('head-1280 totals v16_sweep_win_nodes_sum equals the summed WIN '
          'batch nodes', head80['totals']['v16_sweep_win_nodes_sum']
          == sum(win_nodes.values()), f'{win_nodes}')

    rerun = [json.loads(x) for x in (OUT / 'class2-lane-cost76b-v16-determinism-rerun-20261115.jsonl').read_text().strip().splitlines()]
    batch5 = [json.loads(x) for x in (OUT / 'class2-lane-cost76b-raw-batch5-20261115.jsonl').read_text().strip().splitlines()]
    strip = lambda rs: [{k: v for k, v in r.items() if k != 'ms'} for r in rs]
    check('v16 determinism rerun (batch 5) node-exact ignoring ms',
          strip(rerun) == strip(batch5))

    v15 = [json.loads(x) for x in (OUT / 'class2-lane-cost76b-v15-crosscheck-20261115.jsonl').read_text().strip().splitlines()]
    v15_pilots = [r for r in v15 if r.get('control') == 'pilot_d6']
    check('v15 crosscheck: single pilot, nodes 5949',
          len(v15_pilots) == 1 and v15_pilots[0]['nodes'] == 5949)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    check('v15: both WIN bits loss=true (3,999,895 / 7,364,097 nodes)',
          all(v15_bits[b]['loss'] is True for b in WIN_BITS)
          and v15_bits[72]['nodes'] == 3_999_895
          and v15_bits[96]['nodes'] == 7_364_097)
    check('v15: refuted anchors bits 0/1/2 loss=false',
          all(v15_bits[b]['loss'] is False for b in (0, 1, 2)))
    check('v15: exactly the WIN bits + 3 anchors present (6 lines)',
          set(v15_bits) == set(WIN_BITS) | {0, 1, 2})
    check('head-1280 totals v15_crosscheck_nodes_sum equals 3,999,895 + '
          '7,364,097', head80['totals']['v15_crosscheck_nodes_sum'] == 11_363_992)

    # ---- certificates ------------------------------------------------------
    moves_all = json.loads((TMP / 'legal-moves.json').read_text())
    replay_results = {}
    for bit in WIN_BITS:
        root = ROOTS[bit]
        receipt = json.loads((TMP / f'bit{bit}.cert-receipt.json').read_text())
        bigint = json.loads((TMP / f'bit{bit}.bigint.json').read_text())
        parts = sorted(CERTS.glob(f'bit{bit}-root-{root}.cert.part*of2'))
        whole = (b''.join(p.read_bytes().replace(b'\r\n', b'\n') for p in parts)
                 if parts else (CERTS / f'bit{bit}-root-{root}.cert').read_bytes())
        check(f'bit{bit}: joined whole bytes/md5/sha256/blob-sha match the '
              'extraction receipt',
              len(whole) == receipt['bytes'] and md5(whole) == receipt['md5']
              and hashlib.sha256(whole).hexdigest() == receipt['sha256']
              and git_blob_sha(whole) == receipt['git_blob_sha'])
        lines_w = whole.splitlines()
        check(f'bit{bit}: header + root line + sorted-unique rows',
              lines_w[0] == b'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
              and lines_w[1] == b'root ' + root.encode()
              and receipt['rows_sorted_unique'] is True)
        rows = [ln.decode() for ln in lines_w[2:]]
        check(f'bit{bit}: published bigint json rows/mobility/union agree',
              bigint['root_hex'] == root and bigint['strategy_rows'] == len(rows)
              and bigint['union_missing'] == 0 and bigint['union_extra'] == 0
              and bigint['verdict'].startswith('WIN7 certificate'))
        mobility = bigint['root_mobility']
        ts_lines = (TMP / f'bit{bit}.tsverify.json').read_text().strip().splitlines()
        ts_head = json.loads(ts_lines[0])
        ts_rows = json.loads(ts_lines[1])
        check(f'bit{bit}: tsverify header loserMobility and rows count agree '
              'with bigint', ts_head == {'stones': 7, 'loserMobility': mobility}
              and ts_rows['rows'] == len(rows))

        # independent root-mobility enumeration vs legal-moves.json
        lm = moves_all[str(bit)]
        root_pat = int(root, 16)
        my_moves = legal_cells(root_pat)
        check(f'bit{bit}: independent legal-move enumeration of the 7-stone '
              'root is bit-exact with legal-moves.json and the mobility '
              'bookkeeping', lm['root'] == root
              and lm['stones'] == [21, 49, 56, 57, 60, 71, bit]
              and lm['moves'] == my_moves and len(my_moves) == mobility,
              f'{len(my_moves)} moves')

        # consumed dump: 76b convention = per-subroot visited multiset
        consumed = [x for x in (TMP / f'bit{bit}.consumed.txt').read_text().split() if x]
        check(f'bit{bit}: consumed dump distinct set == certificate rows '
              '(multiset-of-visits convention, unlike cost-75d sorted-unique)',
              len(set(consumed)) == len(rows)
              and set(consumed) == {r.split()[0] for r in rows},
              f'{len(consumed)} lines / {len(set(consumed))} distinct / '
              f'{len(rows)} rows')

        # re-run both replay verifiers concurrently on the joined whole
        whole_path = TMP / f'bit{bit}.whole-replay.cert'
        whole_path.write_bytes(whole)
        cons_b = TMP / f'bit{bit}.consumed_bareiss_replay.txt'
        cons_r = TMP / f'bit{bit}.consumed_rational_replay.txt'
        pb = subprocess.Popen(
            [sys.executable, str(SCRIPTS / 'verify_cost73h_win7_bareiss_independent.py'),
             str(whole_path), str(mobility), str(len(rows)), str(cons_b)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pr = subprocess.Popen(
            [sys.executable, str(SCRIPTS / 'verify_cost75d_win7_rational_independent.py'),
             str(whole_path), str(mobility), str(len(rows)), str(cons_r)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out_b, err_b = pb.communicate()
        out_r, err_r = pr.communicate()
        check(f'bit{bit}: published Bareiss replay verifier PASS on re-run '
              f'(rc={pb.returncode})', pb.returncode == 0,
              (out_b or err_b)[:120])
        check(f'bit{bit}: rational third-system verifier PASS on re-run '
              f'(rc={pr.returncode})', pr.returncode == 0,
              (out_r or err_r)[:120])
        res_b = json.loads(out_b)
        res_r = json.loads(out_r)
        check(f'bit{bit}: both replay verdicts agree on rows/mobility/'
              'terminals (terminal stone-count set identical, within 13..17)',
              res_b['strategy_rows'] == res_r['strategy_rows']
              == len(rows)
              and res_b['root_loser_mobility'] == res_r['root_loser_mobility']
              == mobility
              and res_b['union_missing'] == res_r['union_missing'] == 0
              and res_b['union_extra'] == res_r['union_extra'] == 0
              and res_b['terminal_stone_range']
              == res_r['terminal_stone_range']
              and res_b['terminal_stone_range'][0] == 13
              and res_b['terminal_stone_range'][-1] == 17)
        bareiss_set = set(cons_b.read_text().split())
        rational_set = set(cons_r.read_text().split())
        check(f'bit{bit}: Bareiss and rational consumed sets identical and '
              'equal to the published dump distinct set',
              bareiss_set == rational_set == set(consumed))
        replay_results[bit] = {
            'rows': len(rows), 'mobility': mobility,
            'subroots_passed': res_b['subroots_passed'],
            'bareiss': {'strategy_rows': res_b['strategy_rows'],
                        'consumed_rows': res_b['consumed_rows'],
                        'visited_winner_states': res_b['visited_winner_states'],
                        'terminal_range': sorted(res_b['terminal_stone_range'])},
            'rational': {'strategy_rows': res_r['strategy_rows'],
                         'consumed_rows': res_r['consumed_rows'],
                         'winner_state_visits': res_r['winner_state_visits'],
                         'loser_states': res_r['loser_states'],
                         'loser_reply_edges': res_r['loser_reply_edges'],
                         'terminal_range': sorted(res_r['terminal_stone_range'])},
            'consumed_dump_lines': len(consumed),
            'consumed_dump_distinct': len(set(consumed)),
        }
        whole_path.unlink()
        cons_b.unlink()
        cons_r.unlink()
    check('head-1280 totals certificate_rows/sub_roots equal 118,437 / 121',
          head80['totals']['certificate_rows'] == 50796 + 67641 == 118437
          and head80['totals']['certificate_sub_roots'] == 60 + 61 == 121)

    # bit96 two-part join matches the split manifest
    split = json.loads((TMP / 'bit96.split.json').read_text())
    check('bit96: split manifest whole bytes/md5/sha256/blob-sha agree with '
          'the receipt and the joined whole',
          split['whole_bytes'] == 2440105
          and split['whole_md5'] == receipt_96_md5()
          and len(parts96()) == 2)
    check('bit96: split manifest part list matches the joined part files '
          'byte counts',
          [p['bytes'] for p in split['parts']]
          == [p.stat().st_size for p in parts96()])

    # ---- fold marginal bookkeeping (published head JSON level) --------------
    add = head80['cost76b_addition']
    check('fold addition: 2 receipts, covers 7 each, marginals 6+5=11, '
          'in-manifest 2+1=3',
          len(add) == 2 and all(a['covers'] == 7 for a in add)
          and sum(a['marginal'] for a in add) == 11
          and sum(a['marginal_in_manifest'] for a in add) == 3)
    check('claim fold totals agree with the head-1280 addition block',
          fold['receipts_folded'] == 2 and fold['total_marginal'] == 11
          and fold['total_marginal_in_manifest'] == 3
          and fold['publication_order'] == [72, 96])
    check('child orbit closed by the bit-72 receipt (first in publication '
          'order)', head80['target']['child_orbit_closure']
          == 'closed by the bit-72 receipt of this fold'
          and fold['child_orbit_closed_by_bit'] == 72)
    check('claim fold parents_after/parents_lost_rows match the ranking '
          'deltas', fold['parents_after']['parent1'] == '16 rows / 1249'
          and fold['parents_lost_rows']['parent1'] == [CHILD_HEX])
    for a in add:
        rc = json.loads((TMP / f"bit{a['bit']}.cert-receipt.json").read_text())
        check(f"bit{a['bit']}: addition md5 matches the extraction receipt, "
              "rows match, d4-canon recomputes identically",
              a['md5'] == rc['md5'] and a['rows'] == rc['rows']
              and format(d4_canonical(int(a['root_hex'], 16)), '032x')
              == a['d4_canonical_hex'])
        check(f"bit{a['bit']}: marginal hex list lengths match "
              "marginal/marginal_in_manifest",
              len(a['marginal_manifest_hexes']) == a['marginal_in_manifest']
              and len(a['marginal_non_manifest_hexes'])
              == a['marginal'] - a['marginal_in_manifest'])
    # each in-manifest marginal hex is a genuine 6-stone child row of the S5
    # parent whose ranking changed
    a72, a96 = add
    row4038 = [h for h in a72['marginal_manifest_hexes'] if h != CHILD_HEX]
    check('bit72 in-manifest marginal hexes are genuine child rows: the '
          '76b child of parent1 and a row of ...403800000008000000',
          len(row4038) == 1
          and set(a72['marginal_manifest_hexes']) == {CHILD_HEX, row4038[0]}
          and (int(row4038[0], 16) & int(s5_c, 16)) == int(s5_c, 16)
          and bin(int(row4038[0], 16)).count('1') == 6)
    check('bit96 in-manifest marginal hex is a genuine 6-stone row of '
          '...80120200004000000',
          (int(a96['marginal_manifest_hexes'][0], 16) & int(s5_b, 16))
          == int(s5_b, 16)
          and bin(int(a96['marginal_manifest_hexes'][0], 16)).count('1') == 6)
    check('all marginal hexes (manifest + non-manifest) are D4-canonical '
          '6-stone patterns',
          all(bin(int(h, 16)).count('1') == 6
              and format(d4_canonical(int(h, 16)), '032x') == h
              for a in add for h in a['marginal_manifest_hexes']
              + a['marginal_non_manifest_hexes']))

    # root novelty vs the 16 head-1277 receipt roots and the 4 pending 75d roots
    sv = json.loads((OUT / 'class2-lane-merged-1277-certificates-second-verification-20261115.json').read_text())
    old_roots = [c['root_hex'] for c in sv['certificates']]
    child75d = int(CHILD75D_HEX, 16)
    pending75d = [format(child75d ^ (1 << b), '032x') for b in WIN75D_BITS]
    new_roots = [ROOTS[b] for b in WIN_BITS]
    canon = lambda h: format(d4_canonical(int(h, 16)), '032x')
    check('2 new roots are mutually raw/D4 distinct',
          len(set(new_roots)) == 2 and len({canon(r) for r in new_roots}) == 2)
    check('2 new roots are raw/D4 distinct from the 16 merged-1277 receipt '
          'roots', not (set(new_roots) & set(old_roots))
          and not ({canon(r) for r in new_roots} & {canon(r) for r in old_roots}))
    check('2 new roots are raw/D4 distinct from the 4 pending cost-75d '
          'roots', not (set(new_roots) & set(pending75d))
          and not ({canon(r) for r in new_roots} & {canon(r) for r in pending75d}))
    check('full 548-root disjointness and the set-equality chain control were '
          'asserted by the fold script from its runpy chain; recorded here as '
          'fold-covered, independent chain re-derivation scheduled',
          head80['controls']['root_disjointness_vs_548_roots'] is True
          and bool(head80['controls']['set_equality_after_2'])
          and head80['controls']['chain_head_1277_reproduced_byte_identical']
          is True)
    check('outstanding_not_folded lists the parallel cost-75d sweep and the '
          'new fold baseline', 'cost75d' in head80['outstanding_not_folded']
          and 'next_fold_baseline' in head80['outstanding_not_folded'])

    # ---- input hashes (exact bytes audited) --------------------------------
    inputs = {}
    input_files = [
        OUT / 'class2-lane-cost76b-inflight-20261115.json',
        OUT / 'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json',
        OUT / 'class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv',
        OUT / 'class-frontier-cost76b-receipts-recompute-20261115.json',
        OUT / 'class-frontier-s5-ranking-after-cost76b-receipts-20261115.csv',
        OUT / 'class-frontier-top-candidates-s6-after-cost76b-receipts-20261115.csv',
        OUT / 'class2-lane-merged-1277-certificates-second-verification-20261115.json',
        OUT / 'class2-lane-cost76b-v15-crosscheck-20261115.jsonl',
        OUT / 'class2-lane-cost76b-v16-determinism-rerun-20261115.jsonl',
        OUT / 'class2-lane-cost76b-certificates' / 'bit72-root-00000000000001801302000000200000.cert',
        OUT / 'class2-lane-cost76b-certificates' / 'bit96-root-00000001000000801302000000200000.cert.part1of2',
        OUT / 'class2-lane-cost76b-certificates' / 'bit96-root-00000001000000801302000000200000.cert.part2of2',
        OUT / 'tmp-cost76b' / 'legal-moves.json',
    ]
    for b in range(1, 11):
        input_files.append(OUT / f'class2-lane-cost76b-raw-batch{b}-20261115.jsonl')
    for bit in WIN_BITS:
        input_files += [TMP / f'bit{bit}.cert-receipt.json',
                        TMP / f'bit{bit}.bigint.json',
                        TMP / f'bit{bit}.tsverify.json',
                        TMP / f'bit{bit}.consumed.txt',
                        TMP / f'bit{bit}.rows.summary.json']
    input_files.append(TMP / 'bit96.split.json')
    for p in input_files:
        data = p.read_bytes()
        inputs[str(p.relative_to(OUT))] = {
            'bytes': len(data), 'md5': md5(data),
            'git_blob_sha': git_blob_sha(data)}

    # ---- summary ------------------------------------------------------------
    heavy = sorted(((r['nodes'], b) for b, r in recs.items()), reverse=True)[:6]
    audit = {
        'schema': 'n11-class2-lane-cost76b-independent-second-audit-20261115-v1',
        'date': '2026-11-15',
        'session': 'long-lane second-verification session (independent post-hoc '
                   'audit after the sweeping lane one-commit landing of sweep + '
                   'certificates + fold)',
        'independent_method': 'Python stdlib; exact-integer Bareiss 4x4 '
                              'determinants; independent 8-element D4 group; '
                              'published Bareiss verifier '
                              '(verify_cost73h_win7_bareiss_independent.py) and '
                              'rational third-system verifier '
                              '(verify_cost75d_win7_rational_independent.py) '
                              're-run on the joined certificate bytes; no repo '
                              'engine; no floating point',
        'target': {
            's5_parent_hex': PARENT1_HEX,
            's6_child_hex': CHILD_HEX,
            'edge_cost': 76,
            'child_stones': sorted(stones),
            'open_lift_deletion': del_open,
            'deletion_orbits': {str(s): format(orbits[s], '032x')
                                for s in sorted(orbits)},
            'legal_candidate_count': len(cand),
        },
        'sweep': {
            'batches': {str(b): len(v) for b, v in batch_bits.items()},
            'win7_d10_bits': win_bits,
            'refuted_d10': 74,
            'capped': [],
            'candidate_nodes': total_nodes,
            'determinism_rerun_batch5_node_exact': True,
            'v15': {'win_nodes': {str(b): v15_bits[b]['nodes']
                                  for b in WIN_BITS},
                    'anchors_loss_false': [0, 1, 2], 'pilot_nodes': 5949},
            'heaviest_bits_nodes': {str(b): n for n, b in heavy},
        },
        'certificates': {str(k): v for k, v in replay_results.items()},
        'fold_bookkeeping': {
            'head_1277': [1277, 6570, 518896, 4840, 382619],
            'head_1280': [1280, 6567, 518678, 4837, 382401],
            'solved_delta': 3, 'remaining_cost_delta': 218,
            'changed_s5_rows': sorted(changed),
            'receipts': [{'bit': a['bit'], 'covers': a['covers'],
                          'marginal': a['marginal'],
                          'marginal_in_manifest': a['marginal_in_manifest']}
                         for a in add],
            'consumed_dump_convention': 'cost-76b consumed.txt files hold the '
                                        'per-subroot visited winner-state '
                                        'multiset (69,250 / 90,622 lines for '
                                        'bits 72 / 96); the distinct level '
                                        'equals the certificate rows (50,796 / '
                                        '67,641) and both of my replay outputs; '
                                        'cost-75d dumps were sorted-unique - a '
                                        'cross-lane convention difference worth '
                                        'recording',
        },
        'checks_failed': failures,
        'inputs': inputs,
        'relation_to_prior_audits': 'complements '
          'class2-lane-cost76b-claim-independent-audit-20261115.json (the '
          'pre-sweep claim audit run while the sweep was in flight): that '
          'audit covered geometry/candidates/demand at head 1277; this audit '
          'covers the landed sweep, certificates, replay re-runs and the '
          'head-1277 -> head-1280 fold bookkeeping',
        'proof_boundary': 'REFUTED-D10 proves only absence of a WIN7-D10 '
                          'certificate, not a LOSS; WIN7 certificates prove a '
                          'first-player win within depth 10 from the individual '
                          '7-stone roots only; the fold is bookkeeping over '
                          'published receipts and solved counts measure '
                          'manifest coverage, not game-theoretic values; full '
                          '548-root disjointness and the set-equality control '
                          'were asserted by the fold script from its runpy '
                          'chain and are scheduled for independent chain '
                          're-derivation; 11x11 empty board / two-stone root '
                          '{49,60} / S2 {59,60} / class 1 / class 2 / class 4 '
                          'remain UNKNOWN',
    }
    outp = OUT / 'class2-lane-cost76b-independent-second-audit-20261115.json'
    outp.write_text(json.dumps(audit, indent=1, sort_keys=True) + '\n')
    print('ALL CHECKS PASS' if not failures else 'FAILURES: ' + repr(failures))
    print('wrote', outp)
    return 0 if not failures else 1


def parts96():
    root = ROOTS[96]
    return sorted(CERTS.glob(f'bit96-root-{root}.cert.part*of2'))


def receipt_96_md5():
    return json.loads((TMP / 'bit96.cert-receipt.json').read_text())['md5']


if __name__ == '__main__':
    sys.exit(main())
