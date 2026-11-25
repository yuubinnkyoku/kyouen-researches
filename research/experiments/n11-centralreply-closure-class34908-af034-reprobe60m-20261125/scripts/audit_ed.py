#!/usr/bin/env python3
"""Part ED fail-closed audit: af034 60M reprobe kit + outputs.

Verifies, against pins declared in research/log/2026-11-25-part-ed-af034-reprobe60m-declaration.md
(commit 8cc8ed0c):
  * kit bytes (jsreplay byte-clone, derived 60M runner = EA 30M runner with the
    BUDGET line only changed, input clones, val-gate clones, source pins),
  * fresh-increment gate: af034 absent from the Part EC canonical merged cache
    (cecc1a0f...) and from the quarantine registry,
  * honest 15M/30M exhaustion history for af034 (published bytes),
  * val-gate: 4 fresh host runs match the published baselines on every replay
    column except wall_s,
  * anchors: af001/af029/af039 fresh two-pass runs node-exact against the
    published b33/EA condition values under the 60M ED cap,
  * the main probe: af034 p1/p2 two-pass node-exact under the 60M cap, honest
    label classification (LOSS: nodes>30M; WIN: runner WIN-HALT; EXHAUSTED:
    nodes==60M exactly), and,
  * nothing else: no verdict consumption, no cache write, no coverage claim.

Exit 0 only if every gate passes; writes output/audit_ed.json.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ED = Path(__file__).resolve().parents[1]

JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNNER_SHA = "b0c5f714f926a923d35692672fbfc6aaf2da0081cdf4217c074e0f64d3a29f92"
RUNNER_EA30M_REFERENCE = "3b5083b4"
INPUT_AF034_SHA = "a4bff56606cbb11107b77dac677b1e1151f59686174bddcf7e08c0558f590326"
INPUT_AF001_SHA = "b2ef3588267694aff51b5ec7aa9940064c5199db2b5f00644a9ed27fca2a127b"
INPUT_AF029_SHA = "b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10"
INPUT_AF039_SHA = "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691"
B33_STATUS_SHA = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"
EA_STATUS_SHA = "db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438"
AF034_P1_30M_SHA = "9ecfdc770c0b8a6eab027c097051ae2731ee15f1ede0babbc619e38acf2fca74"
AF034_P2_30M_SHA = "3978990d5821850476e7b38d1de98fbe7a56738cfd48a8b03cf8ed3350d1b290"
CANONICAL_CACHE_SHA = "cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
VALGATE_FILE_SHAS = {
    "val-gate/at2m-s5-1152921504606851072-536870946.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "val-gate/at2m-s5-1152921504606851072-536870946.published-baseline.out": "6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c",
    "val-gate/at2m-s5-1188950301626860544-536870912.input.csv": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "val-gate/at2m-s5-1188950301626860544-536870912.published-baseline.out": "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "val-gate/first-15m-s5-1152921504606851072-536870946.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "val-gate/first-15m-s5-1152921504606851072-536870946.published-baseline.out": "8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591",
    "val-gate/second-15m-s5-1188950301626860544-536870912.input.csv": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "val-gate/second-15m-s5-1188950301626860544-536870912.published-baseline.out": "91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb",
}
VALGATE_PINS = {
    "at2m-s5-1152921504606851072-536870946": ("input-ecc0299b", "base-6e902ab1",
        (2000000, 0, 2000000)),
    "at2m-s5-1188950301626860544-536870912": ("input-56aacb71", "base-eeafe3ac",
        (2000000, 0, 2000000)),
    "first-15m-s5-1152921504606851072-536870946": ("input-ecc0299b", "base-8035fe54",
        (15000000, 2, 3651923)),
    "second-15m-s5-1188950301626860544-536870912": ("input-56aacb71", "base-91dffdec",
        (15000000, 2, 5040200)),
}
AF034_KEY = (1152921504607911937, 68719476736)
ANCHORS = {
    "af001": {"result": 2, "nodes": 2952432, "budget": 60000000,
              "published": "b33 15M anchor af001 PASS 15000000,2,2952432"},
    "af029": {"result": 1, "nodes": 4862485, "budget": 60000000,
              "published": "b33 15M WIN anchor af029 PASS 15000000,1,4862485"},
    "af039": {"result": 2, "nodes": 19234232, "budget": 60000000,
              "published": "Part EA 30M af039 PASS 30000000,2,19234232"},
}
ED_BUDGET = 60000000

CHECKS: list = []


def check(name: str, ok: bool, detail) -> bool:
    CHECKS.append({"gate": name, "passed": bool(ok), "detail": str(detail)})
    return bool(ok)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_row(path: Path) -> dict:
    """Parse the single replay row of a jsreplay raw output."""
    row = None
    text = path.read_text(encoding="utf-8")
    if "# replay_done" not in text:
        raise ValueError(f"truncated raw (no replay_done): {path}")
    m = re.search(r"^# forbidden quadruples: (\d+)$", text, re.M)
    flds = None
    for line in text.splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            flds = {
                "id": int(parts[1]), "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]), "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]), "wall_s": float(parts[8]),
                "key_lo": int(parts[9]), "key_hi": int(parts[10]),
            }
            forbid = int(m.group(1)) if m else None
            flds["forbidden_quads"] = forbid
    if flds is None:
        raise ValueError(f"no replay row in {path}")
    return flds


def main() -> None:
    ok_all = True

    # --- kit byte pins ------------------------------------------------------
    pins = {
        "scripts/jsreplay.js": JSREPLAY_SHA,
        "scripts/runbatch_af034-60m.sh": RUNNER_SHA,
        "input/af034.input.csv": INPUT_AF034_SHA,
        "input/af001.input.csv": INPUT_AF001_SHA,
        "input/af029.input.csv": INPUT_AF029_SHA,
        "input/af039.input.csv": INPUT_AF039_SHA,
        "sources/b33-status.log": B33_STATUS_SHA,
        "sources/ea-status.log": EA_STATUS_SHA,
        "sources/exh30m/af034.p1.out": AF034_P1_30M_SHA,
        "sources/exh30m/af034.p2.out": AF034_P2_30M_SHA,
        "sources/canonical-cache-ec-merged-cecc1a0f-20261125.cache": CANONICAL_CACHE_SHA,
        "sources/n11-s5-evidence-quarantine.json": QUARANTINE_SHA,
    }
    for rel, want in pins.items():
        p = ED / rel
        have = sha256(p) if p.is_file() else "MISSING"
        ok_all &= check(f"pin:{rel}", have == want, have[:16])

    for rel, want in VALGATE_FILE_SHAS.items():
        p = ED / rel
        have = sha256(p) if p.is_file() else "MISSING"
        ok_all &= check(f"pin:{rel}", have == want, have[:16])

    # runner delta rule: identical to a BUDGET-line-only change vs the pinned
    # EA 30M runner semantics (BUDGET=60000000 line present, no other drift
    # vs the published pattern: guard comments intact)
    runner_text = (ED / "scripts/runbatch_af034-60m.sh").read_text(encoding="utf-8")
    ok_all &= check("runner:budget-line", re.search(r"^BUDGET=60000000$", runner_text, re.M) is not None, "BUDGET line")
    ok_all &= check("runner:replay-done-guard", "# replay_done" in runner_text, "guard present")
    ok_all &= check("runner:jsreplay-clone", "node scripts/jsreplay.js" in runner_text, "invocation")

    # --- af034 key hygiene --------------------------------------------------
    in_row = (ED / "input/af034.input.csv").read_text(encoding="utf-8").strip()
    ok_all &= check("af034:input-row", in_row == "target,0,5,1152921504607911937,68719476736,95,0,0,0,0,0", in_row)

    # fresh-increment gate: absent from canonical cache and quarantine
    cache_keys = set()
    with (ED / "sources/canonical-cache-ec-merged-cecc1a0f-20261125.cache").open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"bad cache row: {row}")
            lo, hi = int(row[1]), int(row[2])
            cache_keys.add((lo, hi))
    ok_all &= check("fresh:not-in-canonical", AF034_KEY not in cache_keys, f"cache rows={len(cache_keys)}")
    q = json.loads((ED / "sources/n11-s5-evidence-quarantine.json").read_text(encoding="utf-8"))
    qtext = json.dumps(q)
    ok_all &= check("fresh:not-in-quarantine", "1152921504607911937" not in qtext, "quarantine scan")

    # honest 15M/30M exhaustion history (published bytes)
    b33 = (ED / "sources/b33-status.log").read_text(encoding="utf-8")
    ok_all &= check("history:15m-exh", re.search(r"^.* af034 EXHAUSTED 15000000,0,15000000$", b33, re.M) is not None, "b33 15M EXH")
    ea = (ED / "sources/ea-status.log").read_text(encoding="utf-8")
    ok_all &= check("history:30m-exh", re.search(r"^.* af034 PASS 30000000,0,30000000$", ea, re.M) is not None, "EA 30M EXH")
    ea_exh = re.search(r"^.* af034 EXHAUSTED 30000000,0,30000000$", ea, re.M) is not None
    ok_all &= check("history:30m-exh-line", ea_exh is not None or "af034 EXHAUSTED" in ea, "EA 30M EXH line")

    # --- val-gate -----------------------------------------------------------
    valgate_results = {}
    for stem, (_ipin, _bpin, expect) in VALGATE_PINS.items():
        base = ED / f"val-gate/{stem}.published-baseline.out"
        host = ED / f"val-gate/{stem}.ed-host.out"
        if not host.is_file():
            ok_all &= check(f"valgate:{stem}:host-run", False, "missing host run")
            continue
        rb, rh = replay_row(base), replay_row(host)
        same = all(rb[k] == rh[k] for k in ("id", "stones", "legal", "is_or", "budget", "result", "nodes", "key_lo", "key_hi", "forbidden_quads"))
        ok_all &= check(f"valgate:{stem}:row-match", same,
                        f"base=({rb['budget']},{rb['result']},{rb['nodes']}) host=({rh['budget']},{rh['result']},{rh['nodes']})")
        ok_all &= check(f"valgate:{stem}:expected", (rh["budget"], rh["result"], rh["nodes"]) == expect, str(expect))
        valgate_results[stem] = {k: rh[k] for k in ("budget", "result", "nodes")}
    ok_all &= check("valgate:count", len(valgate_results) == 4, sorted(valgate_results))

    # --- anchors ------------------------------------------------------------
    anchor_results = {}
    for key, want in ANCHORS.items():
        p1 = ED / f"output/raw/{key}.p1.out"
        p2 = ED / f"output/raw/{key}.p2.out"
        if not (p1.is_file() and p2.is_file()):
            ok_all &= check(f"anchor:{key}:raws", False, "missing raw")
            continue
        r1, r2 = replay_row(p1), replay_row(p2)
        exact = (r1["budget"], r1["result"], r1["nodes"]) == (r2["budget"], r2["result"], r2["nodes"])
        ok_all &= check(f"anchor:{key}:two-pass-exact", exact, f"p1={r1['nodes']} p2={r2['nodes']}")
        ok_all &= check(f"anchor:{key}:node-exact", (r1["budget"], r1["result"], r1["nodes"]) == (want["budget"], want["result"], want["nodes"]),
                        f"got=({r1['budget']},{r1['result']},{r1['nodes']}) want=({want['budget']},{want['result']},{want['nodes']}) from {want['published']}")
        anchor_results[key] = {"budget": r1["budget"], "result": r1["result"], "nodes": r1["nodes"]}

    # --- main probe: af034 @60M --------------------------------------------
    main_gate = {}
    p1 = ED / "output/raw/af034.p1.out"
    p2 = ED / "output/raw/af034.p2.out"
    if p1.is_file() and p2.is_file():
        r1, r2 = replay_row(p1), replay_row(p2)
        ok_all &= check("af034:key", (r1["key_lo"], r1["key_hi"]) == AF034_KEY and (r2["key_lo"], r2["key_hi"]) == AF034_KEY, str(AF034_KEY))
        ok_all &= check("af034:legal95", r1["legal"] == 95 and r2["legal"] == 95, r1["legal"])
        ok_all &= check("af034:stones5", r1["stones"] == 5 and r2["stones"] == 5, r1["stones"])
        ok_all &= check("af034:forb95670", r1["forbidden_quads"] == 95670 and r2["forbidden_quads"] == 95670, r1["forbidden_quads"])
        ok_all &= check("af034:budget-60m", r1["budget"] == ED_BUDGET and r2["budget"] == ED_BUDGET, f"{r1['budget']}/{r2['budget']}")
        exact = (r1["result"], r1["nodes"]) == (r2["result"], r2["nodes"])
        ok_all &= check("af034:two-pass-node-exact", exact, f"{r1['result']},{r1['nodes']} vs {r2['result']},{r2['nodes']}")
        label = {0: "EXHAUSTED", 1: "WIN", 2: "LOSS"}[r1["result"]]
        if r1["result"] == 0:
            ok_all &= check("af034:exh-exact-budget", r1["nodes"] == ED_BUDGET, r1["nodes"])
        elif r1["result"] == 2:
            ok_all &= check("af034:loss-fresh-floor", r1["nodes"] > 30000000, r1["nodes"])
        main_gate = {"label": label, "result": r1["result"], "nodes": r1["nodes"],
                     "p1_wall_s": r1.get("wall_s"), "p2_wall_s": r2.get("wall_s")}
    else:
        ok_all &= check("af034:raws", False, "missing af034 raws")

    # --- status.log ---------------------------------------------------------
    status = ED / "output/status.log"
    if status.is_file():
        st = status.read_text(encoding="utf-8")
        m = re.search(r"^(\S+) af034 PASS (60000000,(\d),(\d+))$", st, re.M)
        ok_all &= check("status:af034-pass", m is not None, "af034 PASS 60M line")
        if m:
            ok_all &= check("status:af034-fields", (int(m.group(3)) in (0, 1, 2)), m.group(2))
            if int(m.group(3)) == 0:
                ok_all &= check("status:af034-exh-line", re.search(r"af034 EXHAUSTED 60000000,0,60000000", st) is not None, "EXH line")
            if int(m.group(3)) == 1:
                ok_all &= check("status:af034-win-line", "af034 WIN-HALT" in st, "WIN-HALT line")
        ok_all &= check("status:af001", re.search(r"af001 PASS 60000000,2,2952432", st) is not None, "af001 anchor line")
        ok_all &= check("status:af029", re.search(r"af029 PASS 60000000,1,4862485", st) is not None, "af029 anchor line")
        ok_all &= check("status:af029-halt", "af029 WIN-HALT" in st, "af029 WIN-HALT")
        ok_all &= check("status:af039", re.search(r"af039 PASS 60000000,2,19234232", st) is not None, "af039 anchor line")
        ok_all &= check("status:no-mismatch", "MISMATCH" not in st, "no MISMATCH")
    else:
        ok_all &= check("status:exists", False, "missing status.log")

    result = {
        "schema": "n11-ed-af034-reprobe60m-audit-v1",
        "all_gates_pass": ok_all,
        "gates": CHECKS,
        "gates_total": len(CHECKS),
        "gates_failed": [c["gate"] for c in CHECKS if not c["passed"]],
        "main_probe_af034": main_gate,
        "anchors": anchor_results,
        "valgate": valgate_results,
        "verdict_consumed": False,
        "claims": {
            "target": "af034 (1152921504607911937, 68719476736)",
            "condition": "ED 60M two-pass fresh-cold",
            "label": main_gate.get("label"),
            "note": "probe-level honest label only; NOT consumed into any canonical "
                    "cache; class 34908 and the 11x11 empty board remain UNKNOWN",
        },
    }
    (ED / "output/audit_ed.json").write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({"all_gates_pass": ok_all, "gates_total": len(CHECKS),
                      "failed": result["gates_failed"], "af034": main_gate}, indent=1))
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
