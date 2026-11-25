#!/usr/bin/env python3
"""K0900 audit: cross-lane independent re-execution agreement check for the
K0898 three-branch REMO cap<=10 r=12 boundary, plus a committed-audit
reproducibility scan of the K0893/K0895/K0897/K0898 STASIS-series
experiment directories.

Background. K0898 was published by a concurrent lane (commits 746b17d9 /
24f1f873 / 0f4639c9 / d7bfeee9 / 41544af1, 2026-11-17). A second lane
session had independently started the same r=12 cap<=10 sweep before
seeing the publication; instead of duplicating the item, that independent
execution is repurposed here as a cross-lane agreement check:

  A. The independent lane re-executed the full 15863-profile r=12 sweep
     with the committed JS engine (mask_engine_fast_r12.js, byte-identical
     copy of the K0893 fixed engine; r given on the CLI) in a separate
     process tree and working directory. The packed records of that
     independent execution are committed in THIS directory as
     output/js_cap10_r12.independent.packed.jsonl. They are
     byte-identical to the committed K0898 packed records (C2), and the
     census / STASIS4 anchors re-derived from them reproduce the
     published K0898 values (C3 / C4). The full-format records of the
     independent run are not committed (same GitHub push transport size
     limit that motivated the packed format); locally they additionally
     reproduce the K0898 committed audit's sha256_uncompressed pin when
     fed through the committed K0898 verifier with a .gz copy present
     (see report.md).
  B. Reproducibility defect found and pinned: the committed audits of
     K0895 (r=10), K0897 (r=11) and K0898 (r=12) record sweep format
     "full", but only the packed records are committed in those
     directories, so a cold re-run from the committed repo state
     regenerates each audit with format "packed" and the verifier run()
     exits FATAL on the committed-audit byte comparison BEFORE the live
     checks. The committed audits pinned in those items were generated
     while the (unpublished) full-format records were locally present.
     The K0893 (r=9) audit is the control: it says "packed" and IS
     byte-reproducible from the committed state (C5/C7). The defect is a
     publication-reproducibility issue only: in every affected case the
     regenerated audit equals the committed audit except exactly the two
     "format" fields, and all machine checks pass (all_ok=true) in both
     versions (C5/C6). Consequence: the workflow audit steps for
     K0895/K0897/K0898 (refresh-knowledge-generated.yml) cannot pass from
     a fresh checkout until the owning lane either commits the
     full-format records (e.g. as output/js_cap10_rN.jsonl.gz, which
     load_jsonl prefers) or regenerates and re-pins the committed audit
     in the packed state. This checker accepts both the defect state and
     the post-fix state and records which one it observes.

Machine checks (all must pass; full details recorded in the audit JSON):

  C1  independent packed records integrity: 15863 records, index
      sequence 0..15862 complete, nonempty survivor masks and first-loser
      masks within r=12 bits, states > 0.
  C2  cross-lane byte agreement: the independent packed records are
      byte-identical to the committed K0898 packed records; both hash to
      the published pin sha256 0835a06fe3a2cc812b5434ef0d56146f72b2b01
      9b144ed62544d437472c05274.
  C3  independent census re-derivation from the independent packed
      records (atoms re-derived from the index via the canonical cap<=10
      enumeration): 715 keys, 98 uniformly determined, 583 uniformly
      non-determined, 34 mixed keys equal to the published 7-family
      boundary list, per-key partitions equal to the published table,
      max_states 666030.
  C4  STASIS4 independent re-derivation: det flags / survivor masks /
      first-loser masks of the independent records vs the committed
      K0897 r=11 packed records -> 0/0/0 differences (full-label
      fixpoint, r=11 <-> r=12).
  C5  audit reproducibility scan (fresh-checkout state): K0893 r=9
      regenerates its committed audit byte-identically (control); for
      K0895/K0897/K0898 the regenerated audit either is byte-identical
      (post-fix state) or differs from the committed audit (defect
      state); the observed state per directory is recorded.
  C6  defect pinning: in the defect state, the regenerated audit equals
      the committed audit after normalizing exactly the two "format"
      fields ("full" in the committed audits, "packed" in the
      fresh-checkout regeneration), and all_ok=true in both versions.
  C7  control pin: the committed K0893 r=9 verifier regenerates the
      committed r=9 audit byte-identically (sha256 f407faee7280a95d56741
      28fa4ba7c9fced8923d710a657eb16cfac0bae289d8).

Deterministic: stdlib only, no randomness, no wall clock, no network, no
JS execution. The K0898/K0897/K0895/K0893 verifier modules are imported
via importlib from their committed sibling directories (definitions and
audit assembly only; their live checks are NOT run here - the workflow
audit steps own those).

Usage:
    python3 check_k0898_cross_lane_agreement.py
"""

import hashlib
import importlib.util
import json
import os
import sys

sys.setrecursionlimit(100000)

HERE = os.path.dirname(os.path.abspath(__file__))
K0898_DIR = os.path.join(HERE, "..", "remo-k-branch-cap10-r12-boundary-20261117")
K0897_DIR = os.path.join(HERE, "..", "remo-k-branch-cap10-r11-boundary-20261117")
K0895_DIR = os.path.join(HERE, "..", "remo-k-branch-cap10-r10-boundary-20261117")
K0893_DIR = os.path.join(HERE, "..", "remo-k-branch-cap10-r9-boundary-20261117")

INDEPENDENT_PACKED = os.path.join(
    HERE, "output", "js_cap10_r12.independent.packed.jsonl")
K0898_PACKED = os.path.join(K0898_DIR, "output", "js_cap10_r12.packed.jsonl")
K0897_PACKED = os.path.join(K0897_DIR, "output", "js_cap10_r11.packed.jsonl")

K0898_PACKED_SHA256 = ("0835a06fe3a2cc812b5434ef0d56146f"
                       "72b2b019b144ed62544d437472c05274")
K0893_AUDIT_SHA256 = ("f407faee7280a95d5674128fa4ba7c9f"
                      "ced8923d710a657eb16cfac0bae289d8")

R = 12
N_PROFILES = 15863
N_KEYS = 715
N_UNIFORM_DET = 98
N_UNIFORM_NDET = 583
N_MIXED = 34
MAX_STATES = 666030

# Published K0898 boundary (pinned from the K0898 item; re-derived from the
# independent records in C3 and asserted equal).
R12_FAILING_KEYS = [[[6, 6, 8], 0], [[6, 6, 8], 1], [[6, 6, 8], 2], [[6, 6, 8], 3], [[6, 6, 8], 4], [[6, 6, 9], 0], [[6, 6, 9], 1], [[6, 6, 9], 2], [[6, 6, 9], 3], [[6, 8, 8], 0], [[6, 8, 8], 1], [[6, 8, 8], 2], [[6, 8, 8], 3], [[6, 8, 8], 4], [[6, 8, 9], 0], [[6, 8, 9], 1], [[6, 8, 9], 2], [[6, 8, 9], 3], [[6, 9, 9], 0], [[6, 9, 9], 1], [[6, 9, 9], 2], [[6, 9, 9], 3], [[8, 8, 9], 0], [[8, 8, 9], 1], [[8, 8, 9], 2], [[8, 8, 9], 3], [[8, 8, 9], 4], [[8, 8, 9], 5], [[8, 9, 9], 0], [[8, 9, 9], 1], [[8, 9, 9], 2], [[8, 9, 9], 3], [[8, 9, 9], 4], [[8, 9, 9], 5]]
R12_PARTITIONS = {'6,6,8|0': {'n_det': 48, 'n_ndet': 3, 'profiles': 51}, '6,6,8|1': {'n_det': 30, 'n_ndet': 3, 'profiles': 33}, '6,6,8|2': {'n_det': 16, 'n_ndet': 3, 'profiles': 19}, '6,6,8|3': {'n_det': 7, 'n_ndet': 3, 'profiles': 10}, '6,6,8|4': {'n_det': 2, 'n_ndet': 2, 'profiles': 4}, '6,6,9|0': {'n_det': 40, 'n_ndet': 14, 'profiles': 54}, '6,6,9|1': {'n_det': 22, 'n_ndet': 12, 'profiles': 34}, '6,6,9|2': {'n_det': 10, 'n_ndet': 10, 'profiles': 20}, '6,6,9|3': {'n_det': 3, 'n_ndet': 7, 'profiles': 10}, '6,8,8|0': {'n_det': 63, 'n_ndet': 3, 'profiles': 66}, '6,8,8|1': {'n_det': 42, 'n_ndet': 3, 'profiles': 45}, '6,8,8|2': {'n_det': 24, 'n_ndet': 3, 'profiles': 27}, '6,8,8|3': {'n_det': 13, 'n_ndet': 3, 'profiles': 16}, '6,8,8|4': {'n_det': 4, 'n_ndet': 3, 'profiles': 7}, '6,8,9|0': {'n_det': 95, 'n_ndet': 25, 'profiles': 120}, '6,8,9|1': {'n_det': 53, 'n_ndet': 25, 'profiles': 78}, '6,8,9|2': {'n_det': 24, 'n_ndet': 23, 'profiles': 47}, '6,8,9|3': {'n_det': 6, 'n_ndet': 19, 'profiles': 25}, '6,9,9|0': {'n_det': 64, 'n_ndet': 14, 'profiles': 78}, '6,9,9|1': {'n_det': 40, 'n_ndet': 14, 'profiles': 54}, '6,9,9|2': {'n_det': 19, 'n_ndet': 14, 'profiles': 33}, '6,9,9|3': {'n_det': 6, 'n_ndet': 14, 'profiles': 20}, '8,8,9|0': {'n_det': 92, 'n_ndet': 8, 'profiles': 100}, '8,8,9|1': {'n_det': 62, 'n_ndet': 8, 'profiles': 70}, '8,8,9|2': {'n_det': 40, 'n_ndet': 8, 'profiles': 48}, '8,8,9|3': {'n_det': 22, 'n_ndet': 8, 'profiles': 30}, '8,8,9|4': {'n_det': 10, 'n_ndet': 8, 'profiles': 18}, '8,8,9|5': {'n_det': 3, 'n_ndet': 6, 'profiles': 9}, '8,9,9|0': {'n_det': 102, 'n_ndet': 8, 'profiles': 110}, '8,9,9|1': {'n_det': 72, 'n_ndet': 8, 'profiles': 80}, '8,9,9|2': {'n_det': 46, 'n_ndet': 8, 'profiles': 54}, '8,9,9|3': {'n_det': 28, 'n_ndet': 8, 'profiles': 36}, '8,9,9|4': {'n_det': 13, 'n_ndet': 8, 'profiles': 21}, '8,9,9|5': {'n_det': 4, 'n_ndet': 8, 'profiles': 12}}

AUDIT_NAME = "check_k0898_cross_lane_agreement_audit.json"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def popcount(x):
    return bin(x).count("1")


def load_packed(path):
    """Packed records -> list of (i, sv_mask, fl_mask, states)."""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i, sv, fl, states = json.loads(line)
            out.append((i, sv, fl, states))
    return out


def normalize_format(obj):
    """Deep-copy with every 'format' string field value normalized, so a
    'full' vs 'packed' label difference disappears. Returns (copy, hits)."""
    hits = []

    def walk(x):
        if isinstance(x, dict):
            o = {}
            for kk, v in x.items():
                if kk == "format" and isinstance(v, str):
                    hits.append(v)
                    o[kk] = "<format>"
                else:
                    o[kk] = walk(v)
            return o
        if isinstance(x, list):
            return [walk(v) for v in x]
        return x

    return walk(obj), hits


# ---------------------------------------------------------------------------
# audit assembly
# ---------------------------------------------------------------------------


def assemble_audit():
    machine_checks = []

    def record(name, ok, detail=None):
        machine_checks.append({"name": name, "ok": bool(ok),
                               "detail": detail or {}})

    # ---- shared definitions from the committed K0898 verifier
    k0898 = load_module("k0898_verifier", os.path.join(
        K0898_DIR, "verify_remo_k_branch_cap10_r12_boundary.py"))
    profiles = k0898.direct_constrained(10)

    # ---- C1: independent packed records integrity
    recs = load_packed(INDEPENDENT_PACKED)
    ok_c1 = (
        len(recs) == N_PROFILES
        and [rec[0] for rec in recs] == list(range(N_PROFILES))
        and all(
            0 < rec[1] < (1 << R) and rec[2] < (1 << R) and rec[3] > 0
            for rec in recs)
    )
    record(
        "C1 independent packed records: 15863 records, index-complete, "
        "nonempty survivor masks within r=12 bits, first-loser masks "
        "within r=12 bits, states>0",
        ok_c1,
        {"records": len(recs),
         "sha256": sha256_file(INDEPENDENT_PACKED),
         "max_states": max(rec[3] for rec in recs)},
    )

    # ---- C2: cross-lane byte agreement with the committed K0898 packed
    ind_text = open(INDEPENDENT_PACKED, "r", encoding="utf-8").read()
    pub_text = open(K0898_PACKED, "r", encoding="utf-8").read()
    ind_digest = sha256_text(ind_text)
    pub_digest = sha256_text(pub_text)
    record(
        "C2 cross-lane byte agreement: the independent packed records are "
        "byte-identical to the committed K0898 packed records (published "
        "pin)",
        ind_text == pub_text and ind_digest == K0898_PACKED_SHA256,
        {"sha256_independent": ind_digest,
         "sha256_committed": pub_digest},
    )

    # ---- C3: independent census re-derivation
    determined = {rec[0]: popcount(rec[1]) == 1 for rec in recs}
    byk = {}
    for i, atoms in enumerate(profiles):
        kk = (tuple(sorted(k0898.profile_sizes(atoms, 3))), atoms[6])
        byk.setdefault(kk, []).append(determined[i])
    failing = sorted(kk for kk, flags in byk.items()
                     if len(set(flags)) > 1)
    part = {}
    for kk in failing:
        flags = byk[kk]
        part["%s|%d" % (",".join(map(str, kk[0])), kk[1])] = {
            "n_det": sum(1 for f in flags if f),
            "n_ndet": sum(1 for f in flags if not f),
            "profiles": len(flags)}
    uni_det = sum(1 for kk, flags in byk.items()
                  if len(set(flags)) == 1 and flags[0])
    uni_ndet = sum(1 for kk, flags in byk.items()
                   if len(set(flags)) == 1 and not flags[0])
    failing_list = sorted([list(kk[0]), kk[1]] for kk in failing)
    record(
        "C3 independent census: 715 keys / 98 uniformly determined / 583 "
        "uniformly non-determined / 34 mixed == the published 7-family "
        "boundary with identical per-key partitions, max_states 666030",
        len(byk) == N_KEYS
        and uni_det == N_UNIFORM_DET
        and uni_ndet == N_UNIFORM_NDET
        and len(failing) == N_MIXED
        and failing_list == sorted(R12_FAILING_KEYS)
        and part == R12_PARTITIONS
        and max(rec[3] for rec in recs) == MAX_STATES,
        {"keys": len(byk), "uniformly_determined": uni_det,
         "uniformly_ndet": uni_ndet, "mixed": len(failing),
         "max_states": max(rec[3] for rec in recs)},
    )

    # ---- C4: STASIS4 independent re-derivation vs committed r=11 packed
    r11 = {rec[0]: (rec[1], rec[2]) for rec in load_packed(K0897_PACKED)}
    det_diff = 0
    sv_diff = 0
    fl_diff = 0
    for i, sv, fl, _st in recs:
        sv11, fl11 = r11[i]
        if (popcount(sv) == 1) != (popcount(sv11) == 1):
            det_diff += 1
        if sv != sv11:
            sv_diff += 1
        if fl != fl11:
            fl_diff += 1
    record(
        "C4 STASIS4 independent re-derivation: det flags / survivor masks "
        "/ first-loser masks of the independent records vs the committed "
        "K0897 r=11 packed records -> 0/0/0 differences (full-label "
        "fixpoint)",
        det_diff == 0 and sv_diff == 0 and fl_diff == 0
        and len(r11) == N_PROFILES,
        {"det_flag_differences": det_diff,
         "survivor_mask_differences": sv_diff,
         "first_loser_mask_differences": fl_diff},
    )

    # ---- C5/C6: committed-audit reproducibility scan (fresh-checkout
    # state: no .gz full records committed in any of the four directories)
    scan = {}
    scan_ok = True
    for label, dirname, vername, audname, control in [
        ("r9", K0893_DIR, "verify_remo_k_branch_cap10_r9_boundary.py",
         "remo_k_branch_cap10_r9_boundary_audit.json", True),
        ("r10", K0895_DIR, "verify_remo_k_branch_cap10_r10_boundary.py",
         "remo_k_branch_cap10_r10_boundary_audit.json", False),
        ("r11", K0897_DIR, "verify_remo_k_branch_cap10_r11_boundary.py",
         "remo_k_branch_cap10_r11_boundary_audit.json", False),
        ("r12", K0898_DIR, "verify_remo_k_branch_cap10_r12_boundary.py",
         "remo_k_branch_cap10_r12_boundary_audit.json", False),
    ]:
        mod = load_module("k_verifier_" + label,
                          os.path.join(dirname, vername))
        audit_r = mod.assemble_audit()
        blob_r = mod.serialize(audit_r)
        committed = open(os.path.join(dirname, "output", audname),
                         "r", encoding="utf-8").read()
        entry = {
            "regenerated_sha256": sha256_text(blob_r),
            "committed_sha256": sha256_text(committed),
            "regenerated_all_ok": audit_r["summary"]["all_ok"],
        }
        if blob_r == committed:
            entry["state"] = "byte_identical"
            ok_dir = audit_r["summary"]["all_ok"]
            if control:
                ok_dir = ok_dir and sha256_text(blob_r) == K0893_AUDIT_SHA256
        else:
            reg_norm, reg_hits = normalize_format(json.loads(blob_r))
            com_norm, com_hits = normalize_format(json.loads(committed))
            entry["state"] = "format_only_difference"
            entry["committed_format_fields"] = sorted(com_hits)
            entry["regenerated_format_fields"] = sorted(reg_hits)
            ok_dir = (
                reg_norm == com_norm
                and sorted(reg_hits) == ["packed", "packed"]
                and sorted(com_hits) == ["full", "full"]
                and audit_r["summary"]["all_ok"]
            )
            if control:
                ok_dir = False
        scan[label] = entry
        entry["check_ok"] = bool(ok_dir)
        scan_ok = scan_ok and ok_dir
    record(
        "C5 committed-audit reproducibility scan (fresh-checkout state): "
        "K0893 r=9 control regenerates its committed audit "
        "byte-identically; K0895/K0897/K0898 are either byte-identical "
        "(post-fix state) or in the pinned defect state (recorded)",
        scan_ok,
        scan,
    )
    defect_ok = all(
        (v["state"] == "byte_identical")
        or (v["state"] == "format_only_difference"
            and v.get("committed_format_fields") == ["full", "full"]
            and v.get("regenerated_format_fields") == ["packed", "packed"]
            and v["regenerated_all_ok"])
        for v in scan.values())
    record(
        "C6 defect pinning: in the defect state the regenerated audit "
        "equals the committed audit except exactly the two 'format' "
        "fields (committed 'full' from the pre-publication local state "
        "vs fresh-checkout 'packed'), all_ok=true in both versions",
        defect_ok,
        {k: v.get("state") for k, v in scan.items()},
    )

    # ---- C7: control pin (folded out of C5 for explicit reporting)
    record(
        "C7 control pin: the committed K0893 r=9 verifier regenerates the "
        "committed r=9 audit byte-identically (sha256 f407faee...)",
        scan["r9"]["state"] == "byte_identical"
        and scan["r9"]["committed_sha256"] == K0893_AUDIT_SHA256,
        {"sha256": scan["r9"]["committed_sha256"]},
    )

    audit = {
        "machine_checks": machine_checks,
        "summary": {
            "all_ok": all(c["ok"] for c in machine_checks),
            "checks": len(machine_checks),
        },
    }
    return audit


def serialize(audit):
    return json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=1) \
        + "\n"


def run():
    audit1 = assemble_audit()
    blob1 = serialize(audit1)
    audit2 = assemble_audit()
    blob2 = serialize(audit2)
    d1 = sha256_text(blob1)
    d2 = sha256_text(blob2)
    if d1 != d2:
        sys.stderr.write("FATAL: two runs differ (nondeterminism)\n")
        sys.exit(1)
    all_ok = audit1["summary"]["all_ok"]
    out_path = os.path.join(HERE, "output", AUDIT_NAME)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            committed = f.read()
        if committed != blob1:
            sys.stderr.write(
                "FATAL: regenerated audit differs from committed file "
                "(sha256 %s)\n" % d1)
            sys.exit(1)
        print("OK: audit byte-identical (sha256 %s)" % d1)
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(blob1)
        print("wrote %s (sha256 %s)" % (out_path, d1))
    print("AUDIT PASSED" if all_ok else "AUDIT FAILED")
    for c in audit1["machine_checks"]:
        print("  [%s] %s" % ("ok" if c["ok"] else "NG", c["name"]))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    run()
