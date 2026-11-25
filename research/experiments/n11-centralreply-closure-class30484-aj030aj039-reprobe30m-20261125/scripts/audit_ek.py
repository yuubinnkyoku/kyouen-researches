#!/usr/bin/env python3
"""Part EK fail-closed audit: aj030/aj039 (class 30484) 30M reprobe kit + outputs.

Verifies, against pins declared in research/log/2026-11-25-part-ek-aj030aj039-reprobe30m-declaration.md:
  * kit bytes (jsreplay byte-clone, the 30M runner = ED 60M runner published bytes
    with the BUDGET line only changed (60000000 -> 30000000), which incidentally
    equals the published Part EA 30M runner bytes exactly, input clones,
    val-gate clones, source pins),
  * fresh-increment gate: aj030/aj039 absent from the Part EI canonical merged
    cache (73482be0...) and from the quarantine registry,
  * honest 15M exhaustion history for aj030/aj039 (published batch-39 bytes),
  * val-gate: 4 fresh host runs match the published baselines on every replay
    column except wall_s,
  * anchors: aj001/aj049/af039 fresh two-pass runs node-exact against the
    published b39/EA condition values under the 30M EK cap,
  * the main probes: aj030/aj039 p1/p2 two-pass node-exact under the 30M cap,
    honest label classification (LOSS: nodes>15M; WIN: runner WIN-HALT;
    EXHAUSTED: nodes==30M exactly), and,
  * nothing else: no verdict consumption, no cache write, no coverage claim.

Exit 0 only if every gate passes; writes output/audit_ek.json.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

EK = Path(__file__).resolve().parents[1]

JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNNER_SHA = "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4"
RUNNER_ED60M_REFERENCE = "b0c5f714"
INPUT_AJ030_SHA = "520ee52abefaec80b800245dd1913489cd511923732e14d3315f4806aec83595"
INPUT_AJ039_SHA = "82f8dff3136ce54e33203f69f3589b72891a41129b11f7b0811b4053e9858394"
INPUT_AJ001_SHA = "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c"
INPUT_AJ049_SHA = "46349391b3aa212cf7ffffbeae94d01b5202f25ca24a6c5294b75ced6184951a"
INPUT_AF039_SHA = "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691"
B39_STATUS_SHA = "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea"
AJ030_P1_15M_SHA = "843a0a0c976699d937391377455504797f5bece24222eef74d4452f20e20178c"
AJ030_P2_15M_SHA = "661c8e410f8e3f93227ac635233556fec5069ccf115117255a38b3b19f551757"
AJ039_P1_15M_SHA = "60ae21db0e099b22403b8ce64ba97e15de3987acfafb218d79c11aae6c3b4906"
AJ039_P2_15M_SHA = "c51899d50649444c3ee8cbb43f3318392131cc3add8b54cbe77d3f600a59dfbb"
CANONICAL_CACHE_SHA = "73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70"
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
TARGETS = {
    "aj030": {"lo": 1152922604135251976, "hi": 65536, "legal": 83},
    "aj039": {"lo": 1152922606282735616, "hi": 65536, "legal": 88},
}
ANCHORS = {
    "aj001": {"result": 2, "nodes": 5156075, "budget": 30000000,
              "published": "b39 15M anchor aj001 PASS 15000000,2,5156075"},
    "aj049": {"result": 1, "nodes": 4998452, "budget": 30000000,
              "published": "b39 15M WIN anchor aj049 PASS 15000000,1,4998452"},
    "af039": {"result": 2, "nodes": 19234232, "budget": 30000000,
              "published": "Part EA 30M af039 PASS 30000000,2,19234232"},
}
EK_BUDGET = 30000000
PREV_EXHAUSTED_BUDGET = 15000000

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
        "scripts/runbatch_ek-30m.sh": RUNNER_SHA,
        "input/aj030.input.csv": INPUT_AJ030_SHA,
        "input/aj039.input.csv": INPUT_AJ039_SHA,
        "input/aj001.input.csv": INPUT_AJ001_SHA,
        "input/aj049.input.csv": INPUT_AJ049_SHA,
        "input/af039.input.csv": INPUT_AF039_SHA,
        "sources/b39-status.log": B39_STATUS_SHA,
        "sources/exh15m/aj030.p1.out": AJ030_P1_15M_SHA,
        "sources/exh15m/aj030.p2.out": AJ030_P2_15M_SHA,
        "sources/exh15m/aj039.p1.out": AJ039_P1_15M_SHA,
        "sources/exh15m/aj039.p2.out": AJ039_P2_15M_SHA,
        "sources/canonical-cache-ei-merged-73482be0-20261125.cache": CANONICAL_CACHE_SHA,
        "sources/n11-s5-evidence-quarantine.json": QUARANTINE_SHA,
    }
    for rel, want in pins.items():
        p = EK / rel
        have = sha256(p) if p.is_file() else "MISSING"
        ok_all &= check(f"pin:{rel}", have == want, have[:16])

    for rel, want in VALGATE_FILE_SHAS.items():
        p = EK / rel
        have = sha256(p) if p.is_file() else "MISSING"
        ok_all &= check(f"pin:{rel}", have == want, have[:16])

    # runner delta rule: the published ED 60M runner bytes with the BUDGET line
    # only changed (60000000 -> 30000000); byte-equal to the published Part EA
    # 30M runner bytes (pin 3b5083b4...).
    runner_text = (EK / "scripts/runbatch_ek-30m.sh").read_text(encoding="utf-8")
    ok_all &= check("runner:budget-line", re.search(r"^BUDGET=30000000$", runner_text, re.M) is not None, "BUDGET line")
    ok_all &= check("runner:no-60m-remnant", "60000000" not in runner_text, "60M string absent")
    ok_all &= check("runner:replay-done-guard", "# replay_done" in runner_text, "guard present")
    ok_all &= check("runner:jsreplay-clone", "node scripts/jsreplay.js" in runner_text, "invocation")

    # --- target key hygiene -------------------------------------------------
    for key, meta in TARGETS.items():
        in_row = (EK / f"input/{key}.input.csv").read_text(encoding="utf-8").strip()
        want_row = f"target,0,5,{meta['lo']},{meta['hi']},{meta['legal']},0,0,0,0,0"
        ok_all &= check(f"{key}:input-row", in_row == want_row, in_row)

    # fresh-increment gate: absent from canonical cache and quarantine
    cache_keys = set()
    with (EK / "sources/canonical-cache-ei-merged-73482be0-20261125.cache").open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"bad cache row: {row}")
            lo, hi = int(row[1]), int(row[2])
            cache_keys.add((lo, hi))
    ok_all &= check("fresh:cache-rows", len(cache_keys) == 6712, f"cache rows={len(cache_keys)}")
    for key, meta in TARGETS.items():
        ok_all &= check(f"fresh:{key}-not-in-canonical", (meta["lo"], meta["hi"]) not in cache_keys, f"cache rows={len(cache_keys)}")
    q = json.loads((EK / "sources/n11-s5-evidence-quarantine.json").read_text(encoding="utf-8"))
    qtext = json.dumps(q)
    for key, meta in TARGETS.items():
        ok_all &= check(f"fresh:{key}-not-in-quarantine", str(meta["lo"]) not in qtext, "quarantine scan")

    # honest 15M exhaustion history (published bytes)
    b39 = (EK / "sources/b39-status.log").read_text(encoding="utf-8")
    for key in TARGETS:
        ok_all &= check(f"history:{key}-15m-pass", re.search(rf"^.* {key} PASS 15000000,0,15000000$", b39, re.M) is not None, "b39 15M PASS line")
        ok_all &= check(f"history:{key}-15m-exh", re.search(rf"^.* {key} EXHAUSTED 15000000,0,15000000$", b39, re.M) is not None, "b39 15M EXH line")
        for p in ("p1", "p2"):
            r = replay_row(EK / f"sources/exh15m/{key}.{p}.out")
            ok_all &= check(f"history:{key}-{p}:row",
                            (r["budget"], r["result"], r["nodes"]) == (PREV_EXHAUSTED_BUDGET, 0, PREV_EXHAUSTED_BUDGET),
                            f"{r['budget']},{r['result']},{r['nodes']}")

    # --- val-gate -----------------------------------------------------------
    valgate_results = {}
    for stem, (_ipin, _bpin, expect) in VALGATE_PINS.items():
        base = EK / f"val-gate/{stem}.published-baseline.out"
        host = EK / f"val-gate/{stem}.ek-host.out"
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
        p1 = EK / f"output/raw/{key}.p1.out"
        p2 = EK / f"output/raw/{key}.p2.out"
        if not (p1.is_file() and p2.is_file()):
            ok_all &= check(f"anchor:{key}:raws", False, "missing raw")
            continue
        r1, r2 = replay_row(p1), replay_row(p2)
        exact = (r1["budget"], r1["result"], r1["nodes"]) == (r2["budget"], r2["result"], r2["nodes"])
        ok_all &= check(f"anchor:{key}:two-pass-exact", exact, f"p1={r1['nodes']} p2={r2['nodes']}")
        ok_all &= check(f"anchor:{key}:node-exact", (r1["budget"], r1["result"], r1["nodes"]) == (want["budget"], want["result"], want["nodes"]),
                        f"got=({r1['budget']},{r1['result']},{r1['nodes']}) want=({want['budget']},{want['result']},{want['nodes']}) from {want['published']}")
        anchor_results[key] = {"budget": r1["budget"], "result": r1["result"], "nodes": r1["nodes"]}

    # --- main probes: aj030 and aj039 @30M ----------------------------------
    main_gate = {}
    for key, meta in TARGETS.items():
        p1 = EK / f"output/raw/{key}.p1.out"
        p2 = EK / f"output/raw/{key}.p2.out"
        if not (p1.is_file() and p2.is_file()):
            ok_all &= check(f"{key}:raws", False, "missing raws")
            continue
        r1, r2 = replay_row(p1), replay_row(p2)
        ok_all &= check(f"{key}:key", (r1["key_lo"], r1["key_hi"]) == (meta["lo"], meta["hi"]) and (r2["key_lo"], r2["key_hi"]) == (meta["lo"], meta["hi"]), str((meta["lo"], meta["hi"])))
        ok_all &= check(f"{key}:legal", r1["legal"] == meta["legal"] and r2["legal"] == meta["legal"], r1["legal"])
        ok_all &= check(f"{key}:stones5", r1["stones"] == 5 and r2["stones"] == 5, r1["stones"])
        ok_all &= check(f"{key}:forb95670", r1["forbidden_quads"] == 95670 and r2["forbidden_quads"] == 95670, r1["forbidden_quads"])
        ok_all &= check(f"{key}:is_or0", r1["is_or"] == 0 and r2["is_or"] == 0, r1["is_or"])
        ok_all &= check(f"{key}:budget-30m", r1["budget"] == EK_BUDGET and r2["budget"] == EK_BUDGET, f"{r1['budget']}/{r2['budget']}")
        exact = (r1["result"], r1["nodes"]) == (r2["result"], r2["nodes"])
        ok_all &= check(f"{key}:two-pass-node-exact", exact, f"{r1['result']},{r1['nodes']} vs {r2['result']},{r2['nodes']}")
        label = {0: "EXHAUSTED", 1: "WIN", 2: "LOSS"}[r1["result"]]
        if r1["result"] == 0:
            ok_all &= check(f"{key}:exh-exact-budget", r1["nodes"] == EK_BUDGET, r1["nodes"])
        elif r1["result"] == 2:
            ok_all &= check(f"{key}:loss-fresh-floor", r1["nodes"] > PREV_EXHAUSTED_BUDGET, r1["nodes"])
        main_gate[key] = {"label": label, "result": r1["result"], "nodes": r1["nodes"],
                          "p1_wall_s": r1.get("wall_s"), "p2_wall_s": r2.get("wall_s")}

    # --- status.log ---------------------------------------------------------
    status = EK / "output/status.log"
    if status.is_file():
        st = status.read_text(encoding="utf-8")
        for key in TARGETS:
            m = re.search(rf"^(\S+) {key} PASS (30000000,(\d),(\d+))$", st, re.M)
            ok_all &= check(f"status:{key}-pass", m is not None, f"{key} PASS 30M line")
            if m:
                if int(m.group(3)) == 0:
                    ok_all &= check(f"status:{key}-exh-line", re.search(rf"{key} EXHAUSTED 30000000,0,30000000", st) is not None, "EXH line")
                if int(m.group(3)) == 1:
                    ok_all &= check(f"status:{key}-win-line", f"{key} WIN-HALT" in st, "WIN-HALT line")
        ok_all &= check("status:aj001", re.search(r"aj001 PASS 30000000,2,5156075", st) is not None, "aj001 anchor line")
        ok_all &= check("status:aj049", re.search(r"aj049 PASS 30000000,1,4998452", st) is not None, "aj049 anchor line")
        ok_all &= check("status:aj049-halt", "aj049 WIN-HALT" in st, "aj049 WIN-HALT")
        ok_all &= check("status:af039", re.search(r"af039 PASS 30000000,2,19234232", st) is not None, "af039 anchor line")
        ok_all &= check("status:no-mismatch", "MISMATCH" not in st, "no MISMATCH")
    else:
        ok_all &= check("status:exists", False, "missing status.log")

    result = {
        "schema": "n11-ek-aj030aj039-reprobe30m-audit-v1",
        "all_gates_pass": ok_all,
        "gates": CHECKS,
        "gates_total": len(CHECKS),
        "gates_failed": [c["gate"] for c in CHECKS if not c["passed"]],
        "main_probes": main_gate,
        "anchors": anchor_results,
        "valgate": valgate_results,
        "verdict_consumed": False,
        "claims": {
            "targets": "aj030 (1152922604135251976, 65536), aj039 (1152922606282735616, 65536)",
            "condition": "EK 30M two-pass fresh-cold",
            "labels": {k: v.get("label") for k, v in main_gate.items()},
            "note": "probe-level honest labels only; NOT consumed into any canonical "
                    "cache; class 30484 and the 11x11 empty board remain UNKNOWN",
        },
    }
    (EK / "output/audit_ek.json").write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({"all_gates_pass": ok_all, "gates_total": len(CHECKS),
                      "failed": result["gates_failed"], "probes": main_gate}, indent=1))
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
