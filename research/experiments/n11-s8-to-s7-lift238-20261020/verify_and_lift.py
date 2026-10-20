#!/usr/bin/env python3
"""Terminal-only S8 LOSS verification and sound S7 reverse propagation.

The 35 S8 roots and 385 S10 leaves are the sole outcome evidence.
The older 2232 S7 labels are used only for a *conditional* coverage audit,
never to establish the new S7 LOSS labels.
"""
import argparse
import zipfile
import hashlib
import json
from pathlib import Path

from terminal_geometry import canonical, children, next_player_wins_at_s10, safe

HERE = Path(__file__).resolve().parent
OLDER = HERE.parent / 'n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt'
S6_TARGET = int('00000000041000001000401000100000', 16)
LEAVES_SHA256 = 'ca487f8075c4a03a404f5d1a98e2c0c847701192d0ce37a30542fd73ea1f3f22'


def fail_unless(cond, message):
    if not cond:
        raise AssertionError(message)


def load_canonical(path, count, stones):
    entries = path.read_text().split()
    fail_unless(len(entries) == count and len(set(entries)) == count, 'duplicate or wrong count: ' + str(path))
    for h in entries:
        fail_unless(len(h) == 32 and h == h.lower(), 'nonstandard hex')
        b = int(h, 16)
        fail_unless(b.bit_count() == stones and canonical(b) == b and safe(b), 'unsafe/noncanonical: ' + h)
    return {int(h, 16) for h in entries}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True,
                        help='full n11-s8-compact385-pruned1946-20261020.zip archive')
    parser.add_argument('--terminal-only', action='store_true')
    args = parser.parse_args()
    archive_bytes = args.archive.read_bytes()
    fail_unless(hashlib.sha256(archive_bytes).hexdigest() ==
                '2ff704ef0a1805556d1cad0b6502add91f68629ac4ba82879801714546aeeb63',
                'archive SHA mismatch')
    with zipfile.ZipFile(args.archive) as z:
        prefix = 'n11-s8-compact385-pruned1946-20261020/'
        plain = z.read(prefix + 'selected385.txt')
        fail_unless(z.read(prefix + 'loss_roots35.txt') == (HERE / 'roots35.txt').read_bytes(),
                    'archive root list differs from repository')
    roots = load_canonical(HERE / 'roots35.txt', 35, 8)
    fail_unless(hashlib.sha256(plain).hexdigest() == LEAVES_SHA256, 'leaf archive SHA mismatch')
    leaves_text = plain.decode('ascii').split()
    fail_unless(len(leaves_text) == len(set(leaves_text)) == 385, 'leaf count/duplicates')
    leaves = set()
    states = 0
    for h in leaves_text:
        fail_unless(len(h) == 32, 'leaf width')
        b = int(h, 16)
        fail_unless(b.bit_count() == 10 and canonical(b) == b and safe(b), 'invalid leaf')
        win, count = next_player_wins_at_s10(b)
        fail_unless(not win, 'selected S10 is WIN: ' + h)
        states += count
        leaves.add(b)
    fail_unless(states == 34709, 'terminal-state regression')

    # Every canonical S9 parent of a verified S10 LOSS leaf is LOSS:
    # at odd ply one LOSS reply suffices. Recompute the relation from scratch.
    s9_loss = set()
    for leaf in leaves:
        for i in range(121):
            if leaf >> i & 1:
                s9_loss.add(canonical(leaf ^ (1 << i)))
    fail_unless(len(s9_loss) == 3757, 'S9 reverse-closure count')
    obligations = set()
    for root in roots:
        obligations.update(children(root))
    fail_unless(len(obligations) == 782, 'S9 obligation count')
    fail_unless(obligations <= s9_loss, 'S8 root with uncovered S9 child')
    # All 35 S8 roots are now proved LOSS by exhaustive S9 boundary checking.

    # An S7 parent of any verified S8 LOSS is LOSS (odd-ply existential reply).
    s7 = set()
    for root in roots:
        for i in range(121):
            if root >> i & 1:
                p = canonical(root ^ (1 << i))
                fail_unless(safe(p), 'unsafe S7 parent')
                s7.add(p)
    fail_unless(len(s7) == 246, 'S7 parent count')
    # Every S7 parent has a *legal* S8 LOSS child; verify the edge independently.
    for p in s7:
        fail_unless(bool(children(p) & roots), 'S7 LOSS has no certified S8 child')

    if args.terminal_only:
        print('PASS 385 S10 terminal LOSS, 35 S8 LOSS, 246 S7 LOSS; older-cache comparison skipped')
        return

    older = load_canonical(OLDER, 2232, 7)
    new = s7 - older
    fail_unless(len(new) == 238 and len(s7 & older) == 8, 'S7 novelty regression')
    target_children = children(S6_TARGET)
    fail_unless(safe(S6_TARGET) and S6_TARGET.bit_count() == 6 and canonical(S6_TARGET) == S6_TARGET, 'invalid S6 target')
    covered = target_children & (older | s7)
    missing = sorted(target_children - (older | s7))
    expected_missing = [
        '00000000041000001000401080100000',
        '00000000041000001000501000100000',
        '00000000041000021000401000100000',
        '00000000041002001000401000100000',
    ]
    fail_unless(len(target_children) == 49 and len(covered) == 45, 'S6 coverage regression')
    fail_unless([f'{x:032x}' for x in missing] == expected_missing, 'S6 gap changed')

    report = {
        'rule': '11x11 standard q=4 complete call normal play, fixed original-first-player perspective',
        'outcome_empty': 'UNKNOWN',
        'terminal_s10_loss_leaves_verified': len(leaves),
        'terminal_memo_states': states,
        'certified_s8_loss_roots': len(roots),
        's9_obligations': len(obligations),
        's9_loss_reverse_closure': len(s9_loss),
        's7_loss_parents_of_s8_roots': len(s7),
        's7_loss_new_vs_20261015_2232': len(new),
        's7_loss_older_overlap': len(s7 & older),
        's6_target': f'{S6_TARGET:032x}',
        's6_target_s7_covered_conditioned_on_old_cache': len(covered),
        's6_target_s7_total': len(target_children),
        's6_target_missing_s7': expected_missing,
        's6_target_verdict': 'UNKNOWN',
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    # To regenerate the list, use the s7_lift.py helper or adapt this set.
    print('new S7 LOSS (hex):')
    print('\n'.join(f'{x:032x}' for x in sorted(new)))


if __name__ == '__main__':
    main()
