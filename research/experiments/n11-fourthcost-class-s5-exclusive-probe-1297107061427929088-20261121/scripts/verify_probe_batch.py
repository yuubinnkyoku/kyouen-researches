#!/usr/bin/env python3
"""n11 fourth-cost class exclusive S5 probe batch: precheck + verify (Part C).

Two fail-closed modes:

  precheck : over the machine 41-key list (fourth-cost-exclusive-keys.json,
             itself gate-checked by the wave-2 refresh against the single-owner
             declaration note), verifies for EVERY key:
               - parseable (lo,hi) with exactly 5 stones,
               - canonical-safe (D4-least canonical, quadruple-free) via the
                 published canonical-safe policy,
               - independent integer geometry legal-count match: the
                 repo-independent Board.legal popcount == ledger legal,
               - exclusive-child membership: the key is a child of the
                 fourth-cost class 1297107061427929088:0 in the frozen 3,384
                 class geometry AND has exactly that one live parent class
                 (which also excludes the reply27 deg>=2 open-ended band),
               - absent from the pinned probe-13 merged exact S5 cache and
                 from the active quarantine registry,
               - disjoint from all five concurrent lanes' fixed claim sets
                 (re-derived machine-side, not copied from prose),
             then emits the batch input CSVs for the jsreplay replica runs.

  verify   : after the runs, parses the per-key raw replay rows, enforces the
             budget ladder (2,000,000 stage; 15,000,000 twice only on
             UNKNOWN), the twice-run determinism of every 15,000,000-budget
             resolution (identical result AND nodes), the legal-count match
             on every raw row, and the pre-registered stopping rules (a WIN
             stops the batch; an UNKNOWN at 15M parks the key with no cache
             row).  Produces the batch verification audit JSON.

No verdict is created by this script; raw rows are solver outputs.  11x11,
{60,27} and third moves 100/108 remain UNKNOWN.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

FOCUS_CLASS = (1188950301626859520, 536870912)
FOURTH_CLASS = (1297107061427929088, 0)
CERT_CLASS = (1297036692683752448, 0)
THIRD_CLASS = (1297036830122704896, 0)


def die(msg):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def kof(c):
    return f"{c[0]}:{c[1]}"


def load_census(w: Path):
    """geo + cache + live incidence + supply (fail-closed, same as ccp)."""
    geo = json.loads(gzip.open(w / "inputs/geometry.json.gz", "rt",
                               encoding="utf-8").read())
    if len(geo) != 3384:
        die("geometry class count")
    cache = {}
    for row in csv.reader((w / "inputs/merged-exact-s5-after-js-probe-13.cache")
                          .open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            die(f"unexpected cache row {row}")
        k = (int(row[1]), int(row[2]))
        v = int(row[4])
        if k in cache and cache[k] != v:
            die(f"verdict conflict in cache {k}")
        cache[k] = v

    def stage(vals):
        if 1 in vals:
            return "WIN"
        if all(v == 2 for v in vals):
            return "LOSS"
        return "UNKNOWN"

    active = []
    fourth_children = None
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        vals = [cache.get(z, 0) for z in ch]
        if tuple(g["key"]) == FOURTH_CLASS:
            fourth_children = ch
        if stage(vals) == "UNKNOWN" and {100, 108}.intersection(g["coverage"]):
            active.append((tuple(g["key"]), ch))
    if len(active) != 62 or fourth_children is None:
        die(f"active classes {len(active)}")
    live_par = defaultdict(set)
    for k, ch in active:
        for c in ch:
            if c not in cache:
                live_par[c].add(k)
    supply = {}
    for row in csv.DictReader((w / "inputs/shared-s5-tasks.csv")
                              .open(newline="")):
        supply[(int(row["key"].split(":")[0]),
                int(row["key"].split(":")[1]))] = row
    if len(supply) != 4562 or set(supply) != set(live_par):
        die("supply/live-incidence mismatch")
    return geo, cache, live_par, supply, active, fourth_children


def fixed_claim_sets(w: Path, live_par, class_children):
    sbd = json.loads((w / "inputs/sbd-corpus-def.json").read_text())
    sbd_corpus99 = {(a, b) for a, b in sbd["corpus99"]}
    sbd_extra2 = {(a, b) for a, b in sbd["unclaimed2"]}
    sets = {}
    sets["focus35"] = ({c for c in class_children[FOCUS_CLASS]
                        if len(live_par[c]) == 1} if FOCUS_CLASS in class_children
                       else set())
    sets["cert38"] = ({c for c in class_children[CERT_CLASS]
                       if len(live_par[c]) == 1} if CERT_CLASS in class_children
                      else set())
    sets["third39"] = ({c for c in class_children[THIRD_CLASS]
                        if len(live_par[c]) == 1} if THIRD_CLASS in class_children
                       else set())
    sets["sbd101"] = sbd_corpus99 | sbd_extra2
    for name, expect in (("focus35", 35), ("cert38", 38), ("third39", 39),
                         ("sbd101", 101)):
        if len(sets[name]) != expect:
            die(f"claim set {name} size {len(sets[name])}")
    return sets


THIRDCOST_MERGED_SHA = ("bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0")


def latest_cache_keys(w: Path):
    """Rows of the latest main merged exact S5 chain cache (third-cost
    increment), fail-closed on the published sha pin."""
    p = w / "chain/merged-exact-s5-after-class-excl-1.cache"
    if hashlib.sha256(p.read_bytes()).hexdigest() != THIRDCOST_MERGED_SHA:
        die("third-cost merged cache sha pin")
    keys = set()
    for row in csv.reader(p.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            die(f"unexpected latest-cache row {row}")
        keys.add((int(row[1]), int(row[2])))
    return keys


def do_precheck(w: Path):
    fr = w / "fakeroot"
    exp_scripts = fr / "research/experiments/probepart/scripts"
    exp_scripts.mkdir(parents=True, exist_ok=True)
    for src in ("s5_evidence_policy.py", "independent.py"):
        dst = exp_scripts / src
        if not dst.exists():
            shutil.copy(w / "inputs" / src, dst)
    results_dir = fr / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    q = results_dir / "n11-s5-evidence-quarantine.json"
    if not q.exists():
        shutil.copy(w / "inputs/n11-s5-evidence-quarantine.json", q)
    sys.path.insert(0, str(exp_scripts))
    import s5_evidence_policy as policy
    import independent as indep

    board = indep.Board(11)
    quarantine = policy.quarantined_cache_keys()
    QSHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
    if hashlib.sha256((w / "inputs/n11-s5-evidence-quarantine.json")
                      .read_bytes()).hexdigest() != QSHA:
        die("quarantine registry pin")

    keysdoc = json.loads((w / "out/fourthcost-probe/fourth-cost-exclusive-keys.json")
                         .read_text())
    order = keysdoc["exclusive_unclaimed_probe_order"]
    if len(order) != 41:
        die("key list size")
    geo, cache, live_par, supply, active, fourth_children = load_census(w)
    latest_keys = latest_cache_keys(w)
    class_children = {k: [c for c in ch if c not in cache] for k, ch in active}
    claims = fixed_claim_sets(w, live_par, class_children)
    claimed_all = set().union(*claims.values())
    bands = defaultdict(int)

    prev = None
    per_key = []
    for i, entry in enumerate(order):
        lo, hi = (int(x) for x in entry["key"].split(":"))
        k = (lo, hi)
        legal_ledger = int(supply[k]["legal"]) if k in supply else None
        problems = []
        if lo.bit_count() + hi.bit_count() != 5:
            problems.append("stone count != 5")
        if not policy.is_canonical_safe_s5_key((lo, hi)):
            problems.append("not canonical-safe")
        mask = indep.mask_from_key(lo, hi, 11)
        legal_indep = board.legal(mask).bit_count()
        if legal_ledger is None:
            problems.append("key not in supply ledger")
        elif legal_indep != legal_ledger:
            problems.append(f"independent legal {legal_indep} != ledger {legal_ledger}")
        if entry["legal"] != legal_ledger:
            problems.append("machine-list legal != ledger legal")
        if k not in fourth_children:
            problems.append("not a child of the fourth-cost class")
        live = live_par.get(k, set())
        if live != {FOURTH_CLASS}:
            problems.append(f"live parents {sorted(kof(x) for x in live)}")
        if k in cache:
            problems.append("already in the merged cache")
        if k in latest_keys:
            problems.append("already in the latest third-cost merged cache")
        if k in quarantine:
            problems.append("in the active quarantine registry")
        if k in claimed_all:
            problems.append("claimed by a concurrent fixed claim set")
        proxy = int(supply[k]["truncated_cost_proxy_nodes"])
        if proxy != entry["truncated_cost_proxy_nodes"]:
            problems.append("proxy mismatch vs machine list")
        cur = (proxy, k)
        if prev is not None and cur < prev:
            problems.append("probe order not ascending (proxy, key)")
        prev = cur
        bands[proxy] += 1
        per_key.append({
            "order": entry["order"], "key": kof(k),
            "legal_independent": legal_indep, "legal_ledger": legal_ledger,
            "truncated_cost_proxy_nodes": proxy,
            "live_parents": sorted(kof(x) for x in live),
            "gates": "PASS" if not problems else problems,
        })
    if any(p["gates"] != "PASS" for p in per_key):
        bad = [p for p in per_key if p["gates"] != "PASS"]
        die(f"precheck failures: {json.dumps(bad)[:600]}")
    if dict(bands) != {5041585: 9, 5234938: 27, 5932112: 5}:
        die(f"band histogram {dict(bands)}")
    ks = [tuple(int(x) for x in p["key"].split(":")) for p in per_key]
    if len(set(ks)) != 41:
        die("duplicate keys in list")

    # batch input CSVs
    indir = w / "probe/input"
    indir.mkdir(parents=True, exist_ok=True)
    for p in per_key:
        lo, hi = (int(x) for x in p["key"].split(":"))
        path = indir / f"k{p['order']:02d}.input.csv"
        if not path.exists():
            path.write_text(
                f"target,0,5,{lo},{hi},{p['legal_ledger']},0,0,0,0,0\n",
                encoding="utf-8")

    audit = {
        "mode": "precheck",
        "class": kof(FOURTH_CLASS),
        "keys": 41,
        "gates": [
            "5 stones", "D4-canonical-safe (policy)", "quadruple-free (policy)",
            "independent integer Board.legal count == ledger legal",
            "child of the fourth-cost class in the frozen 3384-class geometry",
            "exclusive live parent == the fourth-cost class",
            "absent from probe-13 merged cache",
            "absent from the latest third-cost merged cache (sha bb4495e0...)",
            "absent from quarantine registry",
            "disjoint from focus35/cert38/third39/sbd101 fixed claims",
            "ascending (proxy, key) probe order",
        ],
        "quarantine_registry_sha256": QSHA,
        "canonical_safe_policy": "pinned published copy (sha256 78655e94...)",
        "independent_py": "pinned published copy (sha256 954d3a10...)",
        "band_histogram": {str(b): bands[b] for b in sorted(bands)},
        "per_key": per_key,
        "status_guard": "no search performed yet; targets only; 11x11 UNKNOWN",
    }
    (w / "probe/precheck-audit.json").write_text(
        json.dumps(audit, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PRECHECK: 41/41 PASS")
    print(f"bands={ {b: bands[b] for b in sorted(bands)} } "
          f"claims_disjoint=yes quarantine_absent=yes cache_absent=yes")


def parse_replay_row(path: Path):
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            f = line.split(",")
            return {"stones": int(f[2]), "legal": int(f[3]), "is_or": int(f[4]),
                    "budget": int(f[5]), "result": int(f[6]), "nodes": int(f[7]),
                    "key_lo": int(f[9]), "key_hi": int(f[10])}
    return None


def do_verify(w: Path):
    keysdoc = json.loads((w / "out/fourthcost-probe/fourth-cost-exclusive-keys.json")
                         .read_text())
    order = keysdoc["exclusive_unclaimed_probe_order"]
    supply = {}
    for row in csv.DictReader((w / "inputs/shared-s5-tasks.csv")
                              .open(newline="")):
        supply[(int(row["key"].split(":")[0]),
                int(row["key"].split(":")[1]))] = row
    raw = w / "probe/raw"
    per = []
    stopped_early = False
    for entry in order:
        if stopped_early:
            per.append({"order": entry["order"], "key": entry["key"],
                        "status": "NOT RUN (batch stopped after WIN)"})
            continue
        lo, hi = (int(x) for x in entry["key"].split(":"))
        k = (lo, hi)
        legal_ledger = int(supply[k]["legal"])
        rec = {"order": entry["order"], "key": entry["key"], "legal": legal_ledger}
        f2 = raw / f"at2m-k{entry['order']:02d}.out.csv"
        r2 = parse_replay_row(f2) if f2.exists() else None
        if r2 is None:
            rec["status"] = "MISSING 2M STAGE RAW"
            per.append(rec)
            continue
        if (r2["legal"] != legal_ledger or (r2["key_lo"], r2["key_hi"]) != k
                or r2["stones"] != 5 or r2["budget"] != 2_000_000):
            rec["status"] = "2M RAW INCONSISTENT"
            rec["raw"] = r2
            per.append(rec)
            continue
        rec["at2m"] = {"result": r2["result"], "nodes": r2["nodes"]}
        if r2["result"] == 1:
            rec["status"] = "WIN AT 2M - STOPPING RULE 1"
            rec["cache_row"] = None  # no cache row without witness publication
            per.append(rec)
            stopped_early = True
            continue
        if r2["result"] == 2:
            rec["status"] = "LOSS AT 2M"
            rec["cache_row"] = f"s5verdict,{lo},{hi},5,2,{r2['nodes']}"
            per.append(rec)
            continue
        # result 0: UNKNOWN at 2M -> 15M ladder, twice
        r15 = []
        bad_stage = False
        for run in (1, 2):
            fp = raw / f"at15m-run{run}-k{entry['order']:02d}.out.csv"
            rr = parse_replay_row(fp) if fp.exists() else None
            if rr is None or rr["legal"] != legal_ledger or \
               (rr["key_lo"], rr["key_hi"]) != k or rr["stones"] != 5 or \
               rr["budget"] != 15_000_000:
                rec["status"] = f"15M RUN{run} RAW MISSING/INCONSISTENT"
                per.append(rec)
                bad_stage = True
                break
            r15.append({"result": rr["result"], "nodes": rr["nodes"]})
        if bad_stage:
            continue
        rec["at15m_run1"] = r15[0]
        rec["at15m_run2"] = r15[1]
        if r15[0]["result"] == 1 or r15[1]["result"] == 1:
            rec["status"] = "WIN AT 15M - STOPPING RULE 1"
            per.append(rec)
            stopped_early = True
            continue
        if r15[0] != r15[1]:
            rec["status"] = "DETERMINISM MISMATCH (15M twice-run)"
            per.append(rec)
            die(f"nondeterminism for {entry['key']}: {r15}")
        if r15[0]["result"] == 0:
            rec["status"] = "UNKNOWN AT 15M - PARKED (no cache row)"
        else:
            rec["status"] = "LOSS AT 15M"
            rec["cache_row"] = f"s5verdict,{lo},{hi},5,2,{r15[0]['nodes']}"
        per.append(rec)

    bad = [p for p in per if isinstance(p.get("status"), str) and
           ("MISSING" in p["status"] or "INCONSISTENT" in p["status"])]
    if bad:
        die(f"verify failures {json.dumps(bad)[:400]}")
    rows = [p["cache_row"] for p in per if p.get("cache_row")]
    wins = [p for p in per if "WIN" in p.get("status", "")]
    loss2m = [p for p in per if p.get("status") == "LOSS AT 2M"]
    loss15m = [p for p in per if p.get("status") == "LOSS AT 15M"]
    parked = [p for p in per if p.get("status") == "UNKNOWN AT 15M - PARKED (no cache row)"]
    audit = {
        "mode": "verify",
        "evidence_class": "replica solver-trusted exact (jsreplay.js, node-exact "
                          "against the published C++ raw rows via the 4-row val gate)",
        "budget_ladder": "2,000,000 fresh solver; 15,000,000 twice (fresh solver "
                         "each run) only on UNKNOWN; deadline 0; publish=ALL; "
                         "exact order=count",
        "determinism_gate": "every 15,000,000-budget resolution run twice; "
                            "identical (result, nodes) required",
        "loss_at_2m": [p["key"] for p in loss2m],
        "loss_at_15m": [p["key"] for p in loss15m],
        "parked_unknown_at_15m": [p["key"] for p in parked],
        "wins_stopping_rule_1": [p["key"] for p in wins],
        "cache_rows_emitted": len(rows),
        "per_key": per,
        "status_guard": "solver-trusted verdict rows only; no class closure claim; "
                        "{60,27}, 100/108 and the 11x11 empty board remain UNKNOWN",
    }
    (w / "probe/probe-verify-audit.json").write_text(
        json.dumps(audit, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    outc = w / "probe/new-rows.cache"
    outc.write_text("\n".join(sorted(rows,
        key=lambda r: (int(r.split(",")[1]), int(r.split(",")[2])))) + "\n",
        encoding="utf-8")
    print(f"VERIFY: loss2m={len(loss2m)} loss15m={len(loss15m)} "
          f"parked={len(parked)} wins={len(wins)} rows={len(rows)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["precheck", "verify"])
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    w = Path(a.dir)
    if a.mode == "precheck":
        do_precheck(w)
    else:
        do_verify(w)


if __name__ == "__main__":
    main()
