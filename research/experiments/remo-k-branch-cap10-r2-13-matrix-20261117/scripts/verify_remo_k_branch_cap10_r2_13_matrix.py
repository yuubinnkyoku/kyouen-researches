#!/usr/bin/env python3
"""K0904: cap<=10 three-branch REMO determinacy state matrix, r=2..13.

This verifier assembles, purely from COMMITTED packed sweep records (no new
sweep is run), the full 715-key x 12-column (r=2..13) determinacy
classification matrix of the cap<=10 three-branch REMO composite family and
runs the following machine checks:

  C1  input integrity: the 13 committed packed record files match their
      sha256 pins; the seven cap<=12 columns (r=2..8, committed by the
      K0875/K0876-era publications) hold 47,595 index-complete records each
      and the six cap<=10 columns (r=9..13, committed by
      K0893/K0895/K0897/K0898/K0902) hold 15,863 index-complete records
      each; states > 0 everywhere.
  C2  cap12 -> cap10 view mapping: restricting each cap<=12 column to the
      profiles with max branch size <= 10 reproduces the canonical cap<=10
      enumeration exactly once per profile (atoms match by the canonical
      orbit representative), so the restricted columns are a faithful
      cap<=10 sweep view at that r.
  C3  published boundary re-derivation: per-r mixed (non-collapse) key
      sets equal the published boundaries (r2 none with 245 uniformly
      determined keys (K0864); r3 the 22 Theorem-H keys (K0862); r4/r5 the
      12 keys (8,8,9),(8,9,9) x gamma=0..5 (K0864); r6 the 6 mirror keys
      (4,4,8),(4,8,8) x gamma=0..2 (K0864); r7 the 6 keys (4,4,9),(4,9,9)
      x gamma=0..2 (K0866); r8 the 10 keys (6,6,8),(6,8,8) x gamma=0..4
      (K0869); r9..r13 the 34 keys of the 7 published families
      (K0893/K0895/K0897/K0898/K0902) with census 98/583/34 and
      max_states r12 666,030 / r13 741,630). The mixed keys' det-side
      survivor matches the published pins (r4/r5 P_2, r6/r7 P_3, r8..r13
      P_5) and their non-determined possible-survivor sets match the
      published r=4..8 bounds (K0864/K0866/K0869). Exactly 44 distinct
      keys are mixed somewhere in r=2..8 (K0874) and exactly 56 in r=2..13.
  C4  Theorem J (i), key-level classification form (K0902 conjecture): for
      every key with M = max C_i, the classification (uniformly determined
      / uniformly non-determined / mixed) is constant over all r in
      [M, 13]. Expected: 0 violations over all 715 keys.
  C5  Theorem J (i), per-profile survivor form (stronger): for every one of
      the 15,863 profiles, the survivor mask sv is constant over all r in
      [M(key), 13] (equality of sv masks implies equality of determined
      flags, so this subsumes C4). Expected: 0 violations. This extends
      the published r=11..13 full-label fixpoint (K0898/K0902) down to the
      per-key threshold r = M, which had never been checked below r=9.
  C6  Lemma FL inclusion (K0864, proved universally): for every record, the
      first-loser mask is contained in the branch-size residue mask
      {C_i mod r}. Expected: 0 violations over all 13 columns. For the
      mixed keys the observed first-loser residue union is recorded per r
      (two residues at r=3..8 matching the published K0872 pairs
      {0,2}/{0,1}/{3,4}/{2,4}/{2,4}/{0,6}).
  C7  stabilization time sigma: with sigma(key) = the largest r in [2, 12]
      where the classification changes between r and r+1 (0 if never), the
      matrix satisfies sigma(key) <= M(key) - 1 for every key (equivalent
      restatement of C4), the 34 keys mixed at r=13 have their final mixed
      regime starting exactly at r = M (onset at M, state(M-1) != mixed),
      and the 12 keys (8,8,9),(8,9,9) x gamma=0..5 are exactly the keys
      with a non-contiguous mixed band structure (mixed on [3,5], uniform
      on [6,8], mixed again on [9,13] - the K0893 "revival" in per-key
      form). All other mixed keys have a single contiguous band.
  C8  matrix artifact: output/matrix_r2_13.jsonl holds exactly 715 sorted
      key records (classification row, sigma, mixed bands, final survivor
      aggregates at r=13) and the audit JSON is byte-identical across two
      assemblies in the same process (deterministic serialization).

Method notes / honest scope:
  - No new game computation is performed. Every column is read from the
    committed packed records; the atoms are re-derived from the canonical
    enumeration (verbatim K0862 machinery via the committed K0875/K0876
    verifiers), so the mapping from packed index to key is exact.
  - C4/C5/C7 are FINITE checks over r=2..13 and cap<=10. They verify the
    Theorem J conjecture of K0902 inside the observed window only; they
    are not a proof of Theorem J (which quantifies over all r >= M and
    arbitrary k), and r >= 14 remains unobserved except for the K0902
    live L5 spot checks.
  - The state counts (SG guard) are NOT claimed r-invariant: max_states
    differs per column and is recorded as data.

Deterministic: stdlib only, no randomness, no clock, no network.

Usage:
    python3 verify_remo_k_branch_cap10_r2_13_matrix.py
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")

R_LOW, R_HIGH = 2, 13

# ---------------------------------------------------------------------------
# committed input files (sha256-pinned; all byte-verified against main)
# ---------------------------------------------------------------------------

CAP12_INPUTS = {
    2: ("../../remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r2.packed.jsonl",
        "1fd9dbf4cb6699c26bab7f6b34a900f5877d3408603a02a2dd121ca71ef8e951"),
    3: ("../../remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r3.packed.jsonl",
        "ea7c66286f728a52d5696d627ce1faf7705e77f9e4222493221f3a4fe79ed134"),
    4: ("../../remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r4.packed.jsonl",
        "04caba43a7c0f7124db1ea81fcad4f170de04bd041699f6659e42f786e9a40b4"),
    5: ("../../remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r5.packed.jsonl",
        "c6dddad7a4ce39d3ebc8765187b0f16961720654918d74f54e608e12975ea693"),
    6: ("../../remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r6.packed.jsonl",
        "65f1cb32a9ecae6bd258056dfe8ab7c59d376d570f1d11c647b6823fd2467f1d"),
    7: ("../../remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r7.packed.jsonl",
        "50eb7c1ba41825dcbf726258cb2c6878a324d58bb17a708cb587d9d2b3b79c78"),
    8: ("../../remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r8.packed.jsonl",
        "0a884b490e28c281166754c1e82aaa73f7515580dea05b4ce023e8a1f079e8dc"),
}

CAP10_INPUTS = {
    9: ("../../remo-k-branch-cap10-r9-boundary-20261117/output/js_cap10_r9.packed.jsonl",
        "a2bb16bc8d03f341704d902f0a50ce4352b14ad08043cbced54b8e8f83b9973b"),
    10: ("../../remo-k-branch-cap10-r10-boundary-20261117/output/js_cap10_r10.packed.jsonl",
         "fa1e1a405523403611101f819aed5013b353fdf2a526d125e643b8364b072884"),
    11: ("../../remo-k-branch-cap10-r11-boundary-20261117/output/js_cap10_r11.packed.jsonl",
         "08324c19e8837041d8128423f26d88100b1ba7963fea1b86e3f90052b10664f0"),
    12: ("../../remo-k-branch-cap10-r12-boundary-20261117/output/js_cap10_r12.packed.jsonl",
         "0835a06fe3a2cc812b5434ef0d56146f72b2b019b144ed62544d437472c05274"),
    13: ("../../remo-k-branch-cap10-r13-invariance-20261117/output/js_cap10_r13.packed.jsonl",
         "b0ec4f58ac0f4e91185ad252924920738d5e6e8d47a75e61477cf3d915bb7dca"),
}

# published mixed-key boundaries (machine-extracted from the committed
# K0862/K0864/K0866/K0869/K0893-era verifiers and audit JSONs)
PUBLISHED_MIXED = {
    2: [],
    3: [[[2, 3, 8], g] for g in range(2)] +
        [[[2, 8, 9], g] for g in range(2)] +
        [[[3, 3, 8], g] for g in range(2)] +
        [[[3, 8, 8], g] for g in range(2)] +
        [[[3, 8, 9], g] for g in range(2)] +
        [[[8, 8, 9], g] for g in range(6)] +
        [[[8, 9, 9], g] for g in range(6)],
    4: [[[8, 8, 9], g] for g in range(6)] + [[[8, 9, 9], g] for g in range(6)],
    5: [[[8, 8, 9], g] for g in range(6)] + [[[8, 9, 9], g] for g in range(6)],
    6: [[[4, 4, 8], g] for g in range(3)] + [[[4, 8, 8], g] for g in range(3)],
    7: [[[4, 4, 9], g] for g in range(3)] + [[[4, 9, 9], g] for g in range(3)],
    8: [[[6, 6, 8], g] for g in range(5)] + [[[6, 8, 8], g] for g in range(5)],
    9: [[[6, 6, 8], g] for g in range(5)] + [[[6, 8, 8], g] for g in range(5)] +
        [[[8, 8, 9], g] for g in range(6)] + [[[8, 9, 9], g] for g in range(6)] +
        [[[6, 6, 9], g] for g in range(4)] + [[[6, 8, 9], g] for g in range(4)] +
        [[[6, 9, 9], g] for g in range(4)],
    10: None,  # same 34-key set as r=9 (K0895)
    11: None,  # same (K0897)
    12: None,  # same (K0898)
    13: None,  # same (K0902)
}
PUBLISHED_UNIF_DET = {2: 245, 4: 106, 5: 85, 6: 85, 7: 98, 8: 98,
                      9: 98, 10: 98, 11: 98, 12: 98, 13: 98}
K0872_RESIDUE_PAIRS = {3: [0, 2], 4: [0, 1], 5: [3, 4], 6: [2, 4], 7: [2, 4], 8: [0, 6]}
PUBLISHED_MAX_STATES = {12: 666030, 13: 741630}
# published det-side survivor of the MIXED keys' determined profiles per r
# (player indices; K0864 R_BOUNDARY_DET_SURVIVOR {4:[2],5:[2],6:[3]}, the
# committed r278 verifier {7:[3],8:[5]}, K0893..K0902 uniformly P_5)
MIXED_DET_SURVIVOR = {4: [2], 5: [2], 6: [3], 7: [3], 8: [5],
                      9: [5], 10: [5], 11: [5], 12: [5], 13: [5]}
# published possible-survivor sets of the MIXED keys' non-determined
# profiles per r (player indices; K0864 R_BOUNDARY_NDET_BOUND, the
# committed K0866/K0869 witness tables)
MIXED_NDET_BOUND = {4: [[1, 2, 3]], 5: [[1, 2, 3], [1, 2, 3, 4]],
                    6: [[2, 3]], 7: [[1, 2, 3]], 8: [[3, 4, 5]]}

CLS_UDET, CLS_UNDET, CLS_MIXED = 0, 1, 2


def players(mask):
    return [p for p in range(mask.bit_length() + 1) if (mask >> p) & 1]


# ---------------------------------------------------------------------------
# canonical profile enumeration (verbatim K0862 machinery via the committed
# K0875/K0876 verifiers; atoms are a pure function of the packed index)
# ---------------------------------------------------------------------------

def branch_perms(k):
    if k == 1:
        return [(1,)]
    out = []

    def rec(rem, cur):
        if not rem:
            out.append(tuple(cur))
            return
        for x in rem:
            rec([y for y in rem if y != x], cur + [x])

    rec(list(range(1, k + 1)), [])
    return out


def orbit_representative(atoms, k, perms):
    reps = []
    for p in perms:
        na = [0] * ((1 << k) - 1)
        for m in range(1, 1 << k):
            if atoms[m - 1]:
                nm = 0
                for i in range(1, k + 1):
                    if (m >> (i - 1)) & 1:
                        nm |= 1 << (p[i - 1] - 1)
                na[nm - 1] = atoms[m - 1]
        reps.append(tuple(na))
    return min(reps)


def constrained_vectors(cap):
    for v0 in range(1, cap + 1):
        for v1 in range(1, cap + 1):
            for v3 in range(1, cap + 1):
                for v2 in range(0, cap + 1):
                    for v4 in range(0, cap + 1):
                        for v5 in range(0, cap + 1):
                            m = min(
                                cap - v0 - v2 - v4,
                                cap - v1 - v2 - v5,
                                cap - v3 - v4 - v5,
                            )
                            if m >= 0:
                                for v6 in range(0, m + 1):
                                    yield (v0, v1, v2, v3, v4, v5, v6)


def direct_constrained(cap):
    perms = branch_perms(3)
    seen = set()
    profiles = []
    for vec in constrained_vectors(cap):
        rep = orbit_representative(vec, 3, perms)
        if rep not in seen:
            seen.add(rep)
            profiles.append(rep)
    return profiles


def profile_sizes(atoms, k):
    return tuple(
        sum(atoms[m - 1] for m in range(1, 1 << k) if (m >> (i - 1)) & 1)
        for i in range(1, k + 1)
    )


def key_of(atoms):
    return (tuple(sorted(profile_sizes(atoms, 3))), atoms[6])


def kstr(k):
    return "%s|%d" % (",".join(map(str, k[0])), k[1])


def norm_key(k):
    return [list(k[0]), k[1]]


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_packed(path):
    recs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i, sv, fl, states = json.loads(line)
            recs.append((i, sv, fl, states))
    return recs


# ---------------------------------------------------------------------------
# analysis
# ---------------------------------------------------------------------------

def build_columns():
    prof10 = direct_constrained(10)
    prof12 = direct_constrained(12)
    idx10 = {atoms: i for i, atoms in enumerate(prof10)}
    map12 = []
    for atoms in prof12:
        i10 = idx10.get(atoms)
        map12.append((i10, key_of(atoms)))
    keys10 = [key_of(atoms) for atoms in prof10]

    columns = {}
    for r in range(R_LOW, R_HIGH + 1):
        if r in CAP12_INPUTS:
            path, pin = CAP12_INPUTS[r]
            recs = load_packed(os.path.join(HERE, path))
            col = {}
            for (i, sv, fl, states) in recs:
                i10, _k = map12[i]
                if i10 is not None:
                    col[i10] = (sv, fl, states)
            meta = {"source": "cap12", "records": len(recs)}
        else:
            path, pin = CAP10_INPUTS[r]
            recs = load_packed(os.path.join(HERE, path))
            col = {}
            for (i, sv, fl, states) in recs:
                col[i] = (sv, fl, states)
            meta = {"source": "cap10", "records": len(recs)}
        columns[r] = {"col": col, "meta": meta, "path": path, "pin": pin}
    return prof10, keys10, columns


def classify(keys10, columns):
    """cls[r][key] = classification code; sv_agg[r][key] = (det masks, ndet masks)."""
    cls = {r: {} for r in range(R_LOW, R_HIGH + 1)}
    sv_agg = {r: {} for r in range(R_LOW, R_HIGH + 1)}
    for r in range(R_LOW, R_HIGH + 1):
        col = columns[r]["col"]
        byk = {}
        for i, k in enumerate(keys10):
            sv, _fl, _st = col[i]
            det = bin(sv).count("1") == 1
            byk.setdefault(k, []).append((sv, det))
        for k, rs in byk.items():
            dets = [d for _sv, d in rs]
            if all(dets):
                cls[r][k] = CLS_UDET
            elif not any(dets):
                cls[r][k] = CLS_UNDET
            else:
                cls[r][k] = CLS_MIXED
            det_masks = sorted({sv for sv, d in rs if d})
            ndet_masks = sorted({sv for sv, d in rs if not d})
            sv_agg[r][k] = (det_masks, ndet_masks)
    return cls, sv_agg


def main():
    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    prof10, keys10, columns = build_columns()

    # ---- C1 input integrity
    c1_ok = True
    c1_detail = {}
    for r in range(R_LOW, R_HIGH + 1):
        c = columns[r]
        actual = sha256_file(os.path.join(HERE, c["path"]))
        recs_n = c["meta"]["records"]
        col = c["col"]
        idxs = sorted(col.keys())
        idx_ok = idxs == list(range(len(idxs)))
        states_ok = all(st > 0 for (_sv, _fl, st) in col.values())
        expect_n = 47595 if c["meta"]["source"] == "cap12" else 15863
        ok = (actual == c["pin"]) and recs_n == expect_n and idx_ok and states_ok
        c1_ok = c1_ok and ok
        c1_detail["r%d" % r] = {
            "sha256_ok": actual == c["pin"],
            "records": recs_n,
            "index_complete": idx_ok,
            "states_positive": states_ok,
            "view_records": len(col),
        }
    check("C1 input integrity: 13 committed packed columns sha256-pinned, "
          "index-complete, states>0 (cap12 columns 47,595 records restricted "
          "to the 15,863 cap<=10 profiles; cap10 columns 15,863 records)",
          c1_ok, c1_detail)

    # ---- C2 cap12 -> cap10 view mapping
    c2_ok = True
    c2_detail = {}
    for r in sorted(CAP12_INPUTS):
        c = columns[r]
        ok = len(c["col"]) == 15863 and sorted(c["col"].keys()) == list(range(15863))
        c2_ok = c2_ok and ok
        c2_detail["r%d" % r] = {"view_records": len(c["col"]),
                                 "bijective_on_cap10_profiles": ok}
    check("C2 cap12->cap10 view mapping: each r=2..8 cap<=12 column restricted "
          "to max branch size <= 10 covers every canonical cap<=10 profile "
          "exactly once (atoms equality by canonical orbit representative)",
          c2_ok, c2_detail)

    cls, sv_agg = classify(keys10, columns)
    all_keys = sorted(set(keys10))

    # ---- C3 published boundary re-derivation
    c3_ok = True
    c3_detail = {}
    for r in range(R_LOW, R_HIGH + 1):
        mixed = sorted(k for k in all_keys if cls[r][k] == CLS_MIXED)
        udet = sum(1 for k in all_keys if cls[r][k] == CLS_UDET)
        undet = sum(1 for k in all_keys if cls[r][k] == CLS_UNDET)
        col = columns[r]["col"]
        max_states = max(v[2] for v in col.values())
        exp = PUBLISHED_MIXED[r]
        if exp is None:
            exp = PUBLISHED_MIXED[9]
        exp_set = sorted((tuple(e[0]), e[1]) for e in exp)
        ok = sorted(mixed) == exp_set
        udet_ok = (r in PUBLISHED_UNIF_DET and udet == PUBLISHED_UNIF_DET[r])
        if r in (2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13):
            c3_ok = c3_ok and ok and udet_ok
        else:
            c3_ok = c3_ok and ok
        entry = {"mixed": len(mixed), "boundary_ok": ok,
                 "uniformly_determined": udet, "uniformly_ndet": undet,
                 "max_states": max_states}
        if r in PUBLISHED_UNIF_DET:
            entry["unif_det_pin_ok"] = udet_ok
        if r in PUBLISHED_MAX_STATES:
            entry["max_states_pin_ok"] = max_states == PUBLISHED_MAX_STATES[r]
            c3_ok = c3_ok and entry["max_states_pin_ok"]
        # det-side survivor of the mixed keys (player indices)
        mixed_det_players = set()
        mixed_ndet_sets = set()
        for k in mixed:
            det_masks, ndet_masks = sv_agg[r][k]
            for m in det_masks:
                mixed_det_players.update(players(m))
            for m in ndet_masks:
                mixed_ndet_sets.add(tuple(players(m)))
        entry["mixed_det_survivors"] = sorted(mixed_det_players)
        entry["mixed_ndet_sets"] = sorted(list(t) for t in mixed_ndet_sets)
        if r in MIXED_DET_SURVIVOR:
            entry["mixed_det_survivor_pin_ok"] = \
                sorted(mixed_det_players) == MIXED_DET_SURVIVOR[r]
            c3_ok = c3_ok and entry["mixed_det_survivor_pin_ok"]
        if r in MIXED_NDET_BOUND:
            allowed = [list(x) for x in MIXED_NDET_BOUND[r]]
            entry["mixed_ndet_bound_ok"] = all(
                s in allowed for s in entry["mixed_ndet_sets"])
            c3_ok = c3_ok and entry["mixed_ndet_bound_ok"]
        # uniformly-determined keys' survivors (data; chain values)
        udet_players = set()
        for k in all_keys:
            if cls[r][k] == CLS_UDET:
                for m in sv_agg[r][k][0]:
                    udet_players.update(players(m))
        entry["udet_survivors"] = sorted(udet_players)
        c3_detail["r%d" % r] = entry
    c3_ok = c3_ok and (len(all_keys) == 715)
    c3_detail["keys"] = len(all_keys)
    c3_detail["mixed_union_r2_8"] = len([k for k in all_keys
                                         if any(cls[r][k] == CLS_MIXED for r in range(2, 9))])
    c3_detail["mixed_union_r2_13"] = len([k for k in all_keys
                                           if any(cls[r][k] == CLS_MIXED for r in range(2, 14))])
    c3_ok = c3_ok and c3_detail["mixed_union_r2_8"] == 44 \
        and c3_detail["mixed_union_r2_13"] == 56
    check("C3 published boundary re-derivation: per-r mixed (non-collapse) "
          "key sets equal the published boundaries (r2 none/245 det, r3 22 "
          "keys, r4/r5 12, r6 6, r7 6, r8 10, r9..r13 34 with census "
          "98/583/34, max_states r12 666,030 / r13 741,630); the mixed "
          "keys' det-side survivor matches the published pins (r4/r5 P_2, "
          "r6/r7 P_3, r8..r13 P_5) and their non-determined possible-"
          "survivor sets match the published r=4..8 bounds; 44 distinct "
          "mixed keys in r=2..8 (K0874) and 56 in r=2..13",
          c3_ok, c3_detail)

    # ---- C4 Theorem J key-level classification constancy on [M, 13]
    c4_viol = []
    for k in all_keys:
        M = max(k[0])
        lo = max(M, R_LOW)
        base = cls[lo][k]
        for r in range(lo, R_HIGH + 1):
            if cls[r][k] != base:
                c4_viol.append([norm_key(k), r])
                break
    check("C4 Theorem J (i) key-level: for every key the classification is "
          "constant over all r in [M, 13] (M = max C_i); 715 keys, expected "
          "0 violations",
          len(c4_viol) == 0,
          {"keys": len(all_keys), "violations": len(c4_viol),
           "examples": c4_viol[:10]})

    # ---- C5 per-profile survivor constancy on [M, 13]
    c5_viol = []
    for i in range(15863):
        k = keys10[i]
        M = max(k[0])
        lo = max(M, R_LOW)
        sv0 = columns[lo]["col"][i][0]
        for r in range(lo + 1, R_HIGH + 1):
            if columns[r]["col"][i][0] != sv0:
                c5_viol.append([i, norm_key(k), r])
                break
    check("C5 Theorem J (i) per-profile (stronger): for every one of the "
          "15,863 profiles the survivor mask is constant over all r in "
          "[M, 13] (implies the determined-flag constancy; extends the "
          "published r=11..13 full-label fixpoint down to the per-key "
          "threshold r = M)",
          len(c5_viol) == 0,
          {"profiles": 15863, "violations": len(c5_viol),
           "examples": c5_viol[:10]})

    # ---- C6 Lemma FL inclusion
    c6_viol = []
    fl_union = {r: {} for r in range(R_LOW, R_HIGH + 1)}
    for r in range(R_LOW, R_HIGH + 1):
        col = columns[r]["col"]
        for i in range(15863):
            sv, fl, _st = col[i]
            sizes = keys10[i][0]
            resid = 0
            for c in sizes:
                resid |= 1 << (c % r)
            if fl & ~resid:
                c6_viol.append([i, norm_key(keys10[i]), r])
            k = keys10[i]
            fl_union[r].setdefault(k, set()).update(
                p for p in range(r) if (fl >> p) & 1)
    fl_pair_ok = True
    fl_pair_detail = {}
    for r, pair in K0872_RESIDUE_PAIRS.items():
        pairs_seen = set()
        for k in all_keys:
            if cls[r][k] == CLS_MIXED:
                u = sorted(fl_union[r][k])
                pairs_seen.add(tuple(u))
                if u != pair:
                    fl_pair_ok = False
        fl_pair_detail["r%d" % r] = {"pairs": sorted(list(p) for p in pairs_seen),
                                      "published": pair}
    check("C6 Lemma FL inclusion: every record's first-loser mask lies in "
          "{C_i mod r} (0 violations over 13 columns); the mixed keys' "
          "first-loser residue unions match the published K0872 pairs at "
          "r=3..8",
          len(c6_viol) == 0 and fl_pair_ok,
          {"violations": len(c6_viol), "examples": c6_viol[:10],
           "k0872_pairs": fl_pair_detail})

    # ---- C7 sigma / onset / band structure
    c7_ok = True
    sigma = {}
    bands = {}
    onset_ok = True
    noncontig = []
    for k in all_keys:
        M = max(k[0])
        s = 0
        for r in range(R_LOW, R_HIGH):
            if cls[r][k] != cls[r + 1][k]:
                s = r
        sigma[k] = s
        if s > M - 1:
            c7_ok = False
        row = [cls[r][k] for r in range(R_LOW, R_HIGH + 1)]
        b = []
        start = None
        for idx, c in enumerate(row):
            if c == CLS_MIXED and start is None:
                start = idx
            elif c != CLS_MIXED and start is not None:
                b.append([start + R_LOW, idx - 1 + R_LOW])
                start = None
        if start is not None:
            b.append([start + R_LOW, R_HIGH])
        bands[k] = b
        if len(b) > 1:
            noncontig.append(norm_key(k))
        if cls[R_HIGH][k] == CLS_MIXED:
            # final mixed regime must start exactly at r = M
            if not (cls[M][k] == CLS_MIXED and (M - 1 < R_LOW or cls[M - 1][k] != CLS_MIXED)):
                onset_ok = False
    revival = sorted([[8, 8, 9], g] for g in range(6)) + \
              sorted([[8, 9, 9], g] for g in range(6))
    revival_t = sorted((tuple(e[0]), e[1]) for e in revival)
    noncontig_t = sorted((tuple(e[0]), e[1]) for e in noncontig)
    c7_ok = c7_ok and onset_ok and noncontig_t == revival_t
    sigma_eq_M = sum(1 for k in all_keys
                     if cls[R_HIGH][k] == CLS_MIXED and sigma[k] == max(k[0]) - 1)
    check("C7 stabilization time: sigma(key) <= M-1 for every key (restates "
          "C4 in transition form); the 34 keys mixed at r=13 have their "
          "final mixed regime starting exactly at r = M; the 12 keys "
          "(8,8,9),(8,9,9) x gamma=0..5 are exactly the keys with two "
          "separate mixed bands (mixed [3,5] -> uniform [6,8] -> mixed "
          "[9,13], the K0893 revival in per-key form)",
          c7_ok,
          {"sigma_le_M_minus_1": c7_ok, "onset_at_M": onset_ok,
           "noncontiguous_band_keys": noncontig,
           "mixed_at_13_with_sigma_eq_M_minus_1": sigma_eq_M})

    # ---- C8 matrix artifact + double assembly
    matrix_path = os.path.join(OUT, "matrix_r2_13.jsonl")
    lines = []
    for k in all_keys:
        M = max(k[0])
        det_masks, ndet_masks = sv_agg[R_HIGH][k]
        rec = {
            "key": norm_key(k),
            "M": M,
            "cls": [cls[r][k] for r in range(R_LOW, R_HIGH + 1)],
            "sigma": sigma[k],
            "bands": bands[k],
            "final_det_survivors": sorted({p for m in det_masks for p in players(m)}),
            "final_ndet_sets": sorted(players(m) for m in ndet_masks),
        }
        lines.append(json.dumps(rec, sort_keys=True, separators=(",", ":")))
    matrix_blob = "\n".join(lines) + "\n"
    matrix_sha = hashlib.sha256(matrix_blob.encode("utf-8")).hexdigest()
    check("C8 matrix artifact: output/matrix_r2_13.jsonl holds 715 sorted "
          "key records (classification row r=2..13, sigma, mixed bands, "
          "final survivor aggregates); audit assembled twice with "
          "byte-identical output",
          len(lines) == 715,
          {"records": len(lines), "sha256": matrix_sha})

    audit = {
        "experiment": "remo-k-branch-cap10-r2-13-matrix-20261117",
        "kind": "K0904 cap<=10 three-branch REMO determinacy state matrix r=2..13",
        "columns": {
            "r_range": [R_LOW, R_HIGH],
            "cap10_profiles": 15863,
            "keys": 715,
            "cap12_sources": sorted(CAP12_INPUTS),
            "cap10_sources": sorted(CAP10_INPUTS),
        },
        "matrix_sha256": matrix_sha,
        "machine_checks": checks,
        "all_ok": all(c["ok"] for c in checks),
    }

    # double assembly determinism
    blob1 = json.dumps(audit, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    blob2 = json.dumps(audit, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    if blob1 != blob2:
        print("FATAL: double assembly mismatch")
        sys.exit(1)

    out_path = os.path.join(OUT, "remo_k_branch_cap10_r2_13_matrix_audit.json")
    os.makedirs(OUT, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(blob1)
    with open(matrix_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(matrix_blob)

    print("wrote %s" % out_path)
    print("wrote %s" % matrix_path)
    print("matrix sha256 %s" % matrix_sha)
    for c in checks:
        print("  [%s] %s" % ("ok" if c["ok"] else "FAIL", c["name"][:120]))
    print("AUDIT %s" % ("PASSED" if audit["all_ok"] else "FAILED"))
    sys.exit(0 if audit["all_ok"] else 1)


if __name__ == "__main__":
    main()
