#!/usr/bin/env python3
"""Finite-complete target test of K0866's r=8 three-branch REMO extrapolation.

Scope: only (4,4,10) and (4,10,10), gamma=0..3, under branch-size cap 10.
This is not a full r=8 cap<=10 boundary sweep.
Python 3.11+, standard library only; deterministic and network-free.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_DIR = HERE.parent / "remo-k-branch-r7-extension-20261116"
sys.path.insert(0, str(BASE_DIR))
import verify_remo_k_branch_r7_extension as base  # noqa: E402

BASE_GIT_BLOB_SHA = "8c8ea051dc0e2be51133e5f10be2968b17336176"
REGION_BUDGET = 1_500_000
ALT_BUDGET = 2_000_000
TARGET_FAMILIES = ((4, 4, 10), (4, 10, 10))
TARGET_COUNTS = {
    (4, 4, 10): (20, 10, 4, 1),
    (4, 10, 10): (51, 32, 15, 7),
}
R7_CONTROLS = {
    (4, 4, 9): ((20, 16), (10, 7), (4, 2), (1, 0)),
    (4, 9, 9): ((45, 39), (28, 22), (13, 7), (6, 0)),
}


class BudgetExceeded(Exception):
    pass


def git_blob_sha(path):
    raw = Path(path).read_bytes()
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(header + raw).hexdigest()


def permutations3():
    return (
        (1, 2, 3), (1, 3, 2), (2, 1, 3),
        (2, 3, 1), (3, 1, 2), (3, 2, 1),
    )


def transform_atoms(atoms, permutation):
    out = [0] * 7
    for mask in range(1, 8):
        new_mask = 0
        for old_branch in range(1, 4):
            if (mask >> (old_branch - 1)) & 1:
                new_mask |= 1 << (permutation[old_branch - 1] - 1)
        out[new_mask - 1] = atoms[mask - 1]
    return tuple(out)


def canonical_atoms(atoms):
    return min(transform_atoms(atoms, p) for p in permutations3())


def profile_sizes(atoms):
    return tuple(
        sum(atoms[mask - 1] for mask in range(1, 8)
            if (mask >> (branch - 1)) & 1)
        for branch in range(1, 4)
    )


def profiles_for_key(sizes, gamma):
    """Complete S3-orbit representatives for fixed sorted sizes and core."""
    c1, c2, c3 = sizes
    representatives = set()
    # Pair-only atom sizes are free; the three singleton sizes are forced.
    for a12 in range(min(c1, c2) + 1):
        for a13 in range(min(c1 - a12, c3) + 1):
            for a23 in range(min(c2 - a12, c3 - a13) + 1):
                s1 = c1 - gamma - a12 - a13
                s2 = c2 - gamma - a12 - a23
                s3 = c3 - gamma - a13 - a23
                if min(s1, s2, s3) < 1:
                    continue
                atoms = (s1, s2, a12, s3, a13, a23, gamma)
                if tuple(sorted(profile_sizes(atoms))) != tuple(sorted(sizes)):
                    raise AssertionError("profile-size construction failed")
                representatives.add(canonical_atoms(atoms))
    return sorted(representatives)


def chain_profile(sizes, gamma):
    atoms = [0] * 7
    atoms[6] = gamma
    for branch, size in enumerate(sizes, start=1):
        atoms[(1 << (branch - 1)) - 1] = size - gamma
    return tuple(atoms)


def next_player(player, r, active):
    return next(
        (player + distance) % r
        for distance in range(1, r + 1)
        if active & (1 << ((player + distance) % r))
    )


def survivor_mask_alt(atoms, r, budget=ALT_BUDGET):
    """Independent engine: survivor bitmasks, not elimination-order tuples."""
    sizes = profile_sizes(atoms)
    branch_atoms = []
    for branch in range(3):
        mask = 0
        for atom_mask in range(1, 8):
            if (atom_mask >> branch) & 1:
                mask |= 1 << (atom_mask - 1)
        branch_atoms.append(mask)

    zero = tuple((0,) * r for _ in range(7))
    memo = {}
    nodes = [0]
    all_players = (1 << r) - 1

    def solve(counts, mover, active):
        key = (counts, mover, active)
        cached = memo.get(key)
        if cached is not None:
            return cached
        nodes[0] += 1
        if nodes[0] > budget:
            raise BudgetExceeded

        occupied = 0
        totals = []
        for atom_index, row in enumerate(counts):
            total = sum(row)
            totals.append(total)
            if total:
                occupied |= 1 << atom_index

        terminal = False
        for branch, atom_mask in enumerate(branch_atoms):
            if (occupied & ~atom_mask) == 0:
                used = sum(
                    totals[atom_index]
                    for atom_index in range(7)
                    if (atom_mask >> atom_index) & 1
                )
                if used == sizes[branch]:
                    terminal = True
                    break

        if terminal:
            remaining = active & ~(1 << mover)
            if remaining.bit_count() == 1:
                result = remaining
            else:
                following = next_player(mover, r, remaining)
                cleared = tuple(
                    tuple(0 if player == mover else count
                          for player, count in enumerate(row))
                    for row in counts
                )
                result = solve(cleared, following, remaining)
            memo[key] = result
            return result

        following = next_player(mover, r, active)
        result = 0
        for atom_index, row in enumerate(counts):
            if totals[atom_index] >= atoms[atom_index]:
                continue
            if not any(
                (occupied & ~atom_mask) == 0
                and ((atom_mask >> atom_index) & 1)
                for atom_mask in branch_atoms
            ):
                continue
            new_row = row[:mover] + (row[mover] + 1,) + row[mover + 1:]
            new_counts = counts[:atom_index] + (new_row,) + counts[atom_index + 1:]
            result |= solve(new_counts, following, active)

        memo[key] = result
        return result

    try:
        result = solve(zero, 0, all_players)
        return result, nodes[0], False
    except BudgetExceeded:
        return None, nodes[0], True


def bit_indices(mask):
    return [player for player in range(mask.bit_length())
            if (mask >> player) & 1]


def checked_survivors(atoms, r):
    verdict, states_a = base.region_verdict_cached(
        atoms, 3, r, budget=REGION_BUDGET
    )
    mask_b, states_b, skipped_b = survivor_mask_alt(atoms, r)
    if verdict is None or skipped_b:
        raise AssertionError("budget skip at r=%d for %s" % (r, atoms))
    survivors_a = verdict["survivors"]
    survivors_b = bit_indices(mask_b)
    if survivors_a != survivors_b:
        raise AssertionError("engine disagreement: %s vs %s" %
                             (survivors_a, survivors_b))
    return survivors_a, states_a, states_b


def audit_r8():
    rows = {}
    total_profiles = 0
    total_states_a = 0
    total_states_b = 0
    total_chain_a = 0
    total_chain_b = 0
    max_single = 0

    for sizes in TARGET_FAMILIES:
        family_key = ",".join(map(str, sizes))
        family_rows = {}
        for gamma, expected_count in enumerate(TARGET_COUNTS[sizes]):
            profiles = profiles_for_key(sizes, gamma)
            if len(profiles) != expected_count:
                raise AssertionError("profile count mismatch: %s gamma=%d" %
                                     (family_key, gamma))
            histogram = Counter()
            states_a_total = 0
            states_b_total = 0
            max_states = 0
            determined = 0
            for atoms in profiles:
                survivors, states_a, states_b = checked_survivors(atoms, 8)
                histogram[tuple(survivors)] += 1
                determined += (len(survivors) == 1)
                states_a_total += states_a
                states_b_total += states_b
                max_states = max(max_states, states_a, states_b)
                if survivors != [3, 7]:
                    raise AssertionError("unexpected r=8 survivor set")
            chain = chain_profile(sizes, gamma)
            chain_survivors, chain_a, chain_b = checked_survivors(chain, 8)
            if chain_survivors != [3, 7] or determined != 0:
                raise AssertionError("candidate key did not collapse to uniform ndet")

            family_rows[str(gamma)] = {
                "profiles": len(profiles),
                "determined_profiles": determined,
                "survivor_sets": {
                    ",".join(map(str, key)): value
                    for key, value in sorted(histogram.items())
                },
                "chain_survivors": chain_survivors,
                "profile_states_engine_a": states_a_total,
                "profile_states_engine_b": states_b_total,
                "max_states_single_profile": max_states,
                "chain_states_engine_a": chain_a,
                "chain_states_engine_b": chain_b,
            }
            total_profiles += len(profiles)
            total_states_a += states_a_total
            total_states_b += states_b_total
            total_chain_a += chain_a
            total_chain_b += chain_b
            max_single = max(max_single, max_states)

        rows[family_key] = family_rows

    if total_profiles != 140 or total_states_a != total_states_b:
        raise AssertionError("r=8 target aggregate mismatch")
    if (total_states_a, total_chain_a, max_single) != (1465293, 4767, 57739):
        raise AssertionError("r=8 state-count regression")

    return {
        "profiles": total_profiles,
        "chain_profiles": 8,
        "profile_states_engine_a": total_states_a,
        "profile_states_engine_b": total_states_b,
        "chain_states_engine_a": total_chain_a,
        "chain_states_engine_b": total_chain_b,
        "max_states_single_profile": max_single,
        "families": rows,
    }


def audit_r7_positive_control():
    rows = {}
    total_profiles = 0
    for sizes, expected in (
        ((4, 4, 9), ((20, 16), (10, 7), (4, 2), (1, 0))),
        ((4, 9, 9), ((45, 39), (28, 22), (13, 7), (6, 0))),
    ):
        family_key = ",".join(map(str, sizes))
        family_rows = {}
        for gamma, (expected_count, expected_determined) in enumerate(expected):
            profiles = profiles_for_key(sizes, gamma)
            if len(profiles) != expected_count:
                raise AssertionError("r=7 control profile count mismatch")
            histogram = Counter()
            determined = 0
            for atoms in profiles:
                survivors, _, _ = checked_survivors(atoms, 7)
                histogram[tuple(survivors)] += 1
                determined += (len(survivors) == 1)
            chain_survivors, _, _ = checked_survivors(
                chain_profile(sizes, gamma), 7
            )
            expected_chain = [3] if gamma <= 2 else [1, 2, 3]
            if determined != expected_determined or chain_survivors != expected_chain:
                raise AssertionError("r=7 positive-control mismatch")
            family_rows[str(gamma)] = {
                "profiles": len(profiles),
                "determined_profiles": determined,
                "survivor_sets": {
                    ",".join(map(str, key)): value
                    for key, value in sorted(histogram.items())
                },
                "chain_survivors": chain_survivors,
            }
            total_profiles += len(profiles)
        rows[family_key] = family_rows

    if total_profiles != 127:
        raise AssertionError("r=7 positive-control total mismatch")
    return {"profiles": total_profiles, "families": rows}


def audit():
    if git_blob_sha(base.__file__) != BASE_GIT_BLOB_SHA:
        raise AssertionError("pinned K0866 engine changed; inspect before reuse")
    base._VERDICT_CACHE.clear()
    r8 = audit_r8()
    r7 = audit_r7_positive_control()
    return {
        "target": "K0866 r=8 extrapolation: (4,4,10)/(4,10,10), gamma=0..2",
        "status": "finite-complete-targeted-refutation",
        "scope": {
            "game": "three-branch REMO region game",
            "branch_size_cap": 10,
            "r": 8,
            "target_families": ["4,4,10", "4,10,10"],
            "gamma_checked": [0, 1, 2, 3],
            "claim_scope": (
                "Complete only for these two size families and gamma values; "
                "not a full r=8 cap<=10 boundary sweep."
            ),
        },
        "r8_target_sweep": r8,
        "r7_positive_control": r7,
        "checks": [
            "all 140 r=8 profiles were enumerated from the three pair-only atom counts",
            "K0866 region engine and independent survivor-mask engine agree on every profile and chain",
            "every r=8 target profile and chain has survivor set {3,7}",
            "the predicted gamma=0..2 keys are uniformly non-determined, not non-collapse keys",
            "r=7 positive control reproduces the published determined-profile splits",
            "no budget skips",
        ],
        "all_checks_pass": True,
        "base_verifier_git_blob_sha": BASE_GIT_BLOB_SHA,
    }


def serialize(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def run():
    first = serialize(audit())
    second = serialize(audit())
    if first != second:
        raise SystemExit("FATAL: repeated audit output differs")
    blob = first
    output = HERE / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.read_text(encoding="utf-8") != blob:
        raise SystemExit("FATAL: regenerated audit differs from committed JSON")
    output.write_text(blob, encoding="utf-8")
    print("AUDIT PASSED")
    print("r=8: 140 profiles + 8 chains; every survivor set is {3,7}")
    print("r=7 positive control: 127 profiles; published split reproduced")
    print("two independent engines agree; repeated output is byte-identical")


if __name__ == "__main__":
    run()
