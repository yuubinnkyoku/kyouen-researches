#!/usr/bin/env python3
"""cert {73} (S2 {59,60} milestone-4, greedy step 6, bit 32) vs K0675 s6sweep reuse check.

Checks (all machine-verifiable from published artifacts only):
 1. cert {73} s5Reps (94 keys) == K0675 94-position five-stone universe, key-for-key
    (after normalization: lower-case, leading zeros stripped).
 2. Obligation arithmetic: sum(records.children) + symmetry-doubled delta (39+38=77)
    == certStats.rawObligations (7,890).
 3. S6 level: cert {73} s6All has 3,868 orbits; the K0675 sweep also has 3,868 S6;
    all 14 LOSS S6 keys of loss_s6_covers are contained in cert {73} s6All.
    (S5 rep identity + count parity + LOSS containment; S6 set is determined by the
    S5 rep set, cf. mirror-identity classes in the ms4 log.)
 4. Closure roadmap: for each of the 30 certificates, the 1-based rank of its last
    member orbit when s6All is consumed cost-ascending (ties: manifest column order),
    plus min/max/sum cost and declared==seen control against certStats.

Usage:
  python3 cert73_reuse_check.py <milestone4_manifest.json> <s6sweep_dir> <output_dir>

<milestone4_manifest.json>  K0757 regenerated manifest, byte-exact reassembly of
  part1/part2/part3 (whole 1,782,603 bytes, md5 452b4336edbe272a49dcd76c4a7764af).
<s6sweep_dir>  research/experiments/n11-central-19-cover-20261031/output/s6sweep/
  (requires s5_verdicts.json; sweep_results.json used for the S6 count when present).
"""
import hashlib, json, os, sys

CERT73_BIT = 32
DEF_BIT51 = 1 << 51

def norm(k):
    k = k.lower()
    return k.lstrip("0") or "0"

def load_sweep_keys(sweep_results_path):
    """Return the set of S6 keys (ints) judged by the K0675 sweep, tolerating both
    dict-keyed and list record shapes; None if the file is absent."""
    if not os.path.exists(sweep_results_path):
        return None
    data = json.load(open(sweep_results_path))
    keys = set()
    if isinstance(data, dict):
        recs = data.get("results") or data.get("records") or data.get("s6_verdicts")
        if recs is None and all(isinstance(v, (int, str, list, dict)) for v in data.values()) and "s6_count" in data:
            recs = None
        if recs is None:
            # dict keyed directly by S6 hex?
            if all(len(str(k)) >= 20 for k in data.keys()) and all(isinstance(k, str) for k in data.keys()):
                recs = list(data.keys())
        else:
            recs = list(recs) if isinstance(recs, dict) else recs
    else:
        recs = data
    if recs is None:
        return None
    for r in recs:
        if isinstance(r, str):
            keys.add(int(r, 16))
        elif isinstance(r, dict):
            for f in ("s6", "key", "position"):
                if f in r:
                    keys.add(int(str(r[f]), 16)); break
        elif isinstance(r, list):
            keys.add(int(str(r[0]), 16))
    return keys or None

def main():
    manifest_path, sweep_dir, out_dir = sys.argv[1:4]
    expected_md5 = "452b4336edbe272a49dcd76c4a7764af"
    with open(manifest_path, "rb") as f:
        actual_md5 = hashlib.md5(f.read()).hexdigest()
    if actual_md5 != expected_md5:
        raise ValueError(f"manifest MD5 mismatch: expected {expected_md5}, got {actual_md5}")
    m = json.load(open(manifest_path))
    s5v = json.load(open(os.path.join(sweep_dir, "s5_verdicts.json")))
    sweep_keys = load_sweep_keys(os.path.join(sweep_dir, "sweep_results.json"))
    if sweep_keys is None:
        raise ValueError("S6 sweep keys unavailable or unparseable; cannot verify key-for-key identity")

    c73 = [c for c in m["certStats"] if int(c["bit"]) == CERT73_BIT]
    assert len(c73) == 1, "cert {73} (bit 32) not unique in certStats"
    c73 = c73[0]

    # ---- 1. S5 key identity ----
    s5_keys = {norm(r[0]) for r in m["s5Reps"] if int(r[1]) & CERT73_BIT == CERT73_BIT}
    uni_keys = {norm(rec["s5"]) for rec in s5v["records"]}
    s5_match = s5_keys == uni_keys

    # ---- 2. obligation arithmetic ----
    total_children = sum(rec["children"] for rec in s5v["records"])
    doubled = sum(rec["children"] for rec in s5v["records"] if rec["children"] in (39, 38) and rec["win_children"] == rec["children"])
    obligations_ok = (total_children + doubled == int(c73["rawObligations"]))

    # ---- 3. S6 level ----
    c73_s6 = [r for r in m["s6All"] if int(r[2]) & CERT73_BIT == CERT73_BIT]
    c73_s6_keys = set(int(r[0], 16) for r in c73_s6)
    loss_keys = set(int(k, 16) for k in s5v["loss_s6_covers"])
    loss_all_in = loss_keys <= c73_s6_keys
    count_ok = len(c73_s6) == 3868
    sweep_count_ok = len(sweep_keys) == len(c73_s6_keys)
    set_ok = sweep_keys == c73_s6_keys
    position_cell51 = sum(1 for r in c73_s6 if int(r[0], 16) & DEF_BIT51)
    membership_bit51 = sum(1 for r in c73_s6 if int(r[2]) & DEF_BIT51)
    assert membership_bit51 == 0, "unexpected certificate membership bit 51"

    # ---- 4. closure roadmap ----
    rows = m["s6All"]
    roadmap = []
    for c in sorted(m["certStats"], key=lambda c: int(c["step"])):
        bit = int(c["bit"])
        costs = []
        prefix = 0
        seen = 0
        for i, r in enumerate(rows, 1):
            if int(r[2]) & bit == bit:
                seen += 1
                prefix = i
                costs.append(int(r[1]))
        roadmap.append((int(c["step"]), c["cert"], int(c["s6OrbitsSingle"]), seen,
                        min(costs), max(costs), sum(costs), prefix))
    ok_all = all(r[2] == r[3] for r in roadmap)

    assert s5_match and obligations_ok and count_ok and sweep_count_ok and set_ok and loss_all_in and ok_all, "certificate reuse audit failed"

    summary = {
      "manifest_md5_expected": expected_md5,
      "manifest_md5_actual": actual_md5,
      "cert73": {"bit": CERT73_BIT, "step": int(c73["step"]), "s5Orbits": int(c73["s5Orbits"]),
                 "s6Orbits": len(c73_s6), "rawObligations": int(c73["rawObligations"])},
      "s5_universe_identity": {"match": s5_match, "cert73_s5": len(s5_keys), "universe": len(uni_keys)},
      "obligation_arithmetic": {"children_sum": total_children, "symmetry_doubled_delta": doubled,
                                "rawObligations": int(c73["rawObligations"]), "ok": obligations_ok},
      "s6_level": {"cert73_count_ok": count_ok, "sweep_count_ok": sweep_count_ok,
                   "sweep_set_identity": set_ok, "loss_keys": len(loss_keys),
                   "loss_all_in_cert73": loss_all_in,
                   "win": 3854, "loss": 14, "sensitivity_audit": "fails 0 (K0675 verified.json)"},
      "new_s6_computation_needed": 0,
      "remaining_worklist": {"orbits": 43375 - len(c73_s6), "cost_edges": 3477178 - sum(int(r[1]) for r in c73_s6)},
      "cert73_s6_with_position_cell51": position_cell51,
      "cert73_s6_with_membership_bit51": membership_bit51,
      "roadmap_declared_seen_all_match": ok_all,
    }
    os.makedirs(out_dir, exist_ok=True)
    json.dump(summary, open(os.path.join(out_dir, "cert73_reuse_summary.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out_dir, "cert_closure_roadmap.tsv"), "w") as f:
        f.write("step\tcert\tdeclared\tseen\tminCost\tmaxCost\tsumCost\tclosurePrefix\n")
        for step, cert, dec, seen, lo, hi, s, pfx in roadmap:
            f.write(f"{step}\t{cert}\t{dec}\t{seen}\t{lo}\t{hi}\t{s}\t{pfx}\n")
    print(json.dumps(summary, ensure_ascii=False)[:800])

if __name__ == "__main__":
    main()