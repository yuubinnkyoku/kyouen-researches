#!/usr/bin/env python3
"""Pre-registered independent audit instrument for the seventh-cost exclusive S5
ladder (kit research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126).

Audits whatever raw checkpoint rows the single-owner lane has published in the
kit's output/raw/ directory, fail-closed, against:

  - the published selection JSON (pin below) and the canonical head cache
    (pin below);
  - the pre-registered seventh-cost stopping rules (declaration 8d8c3c5c):
    stage 1 = fresh cold 2M per key; resolved-at-2M keys get a second cold 2M
    run (determinism pair, identical (result, nodes)); keys UNKNOWN at 2M
    proceed to a 15M cold pair; LOSS/LOSS identical records resolved,
    UNKNOWN/UNKNOWN parks the key; any WIN stops further claimed-key starts.

The audit asserts NOTHING about verdicts or class status: it only checks raw
integrity, key provenance, budget/stage consistency, determinism pairs and
stopping-rule consistency of what is published. Partial checkpoints are
legal: the audit reports coverage and only fails when a published row is
inconsistent. The standard 11x11 board and every root/class stay UNKNOWN.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126"
SEL = KIT / "output/seventh-cost-exclusive-keys.json"
HEAD = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache"
RAW = KIT / "output/raw"

SEL_SHA = "c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627"
HEAD_SHA = "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4"

STAGES = {
    "at2m": 2000000,
    "at2m-run2": 2000000,
    "at2m-run3-verify": 2000000,
    "at15m-run1": 15000000,
    "at15m-run2": 15000000,
    "at15m-run3-verify": 15000000,
    "at50m-run1": 50000000,
    "at50m-run2": 50000000,
}


def fail(msg):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    gates = []
    gate = lambda name, ok, detail="": (
        fail(f"{name} {detail}") if not ok else gates.append(name))

    gate("pin_selection_json", sha(SEL) == SEL_SHA, str(SEL))
    gate("pin_head_cache", sha(HEAD) == HEAD_SHA, str(HEAD))
    gate("raw_dir", RAW.is_dir(), str(RAW))

    sel = json.loads(SEL.read_text(encoding="utf-8"))
    gate("sel_schema", sel["schema"] == "n11-seventhcost-exclusive-selection-v1")
    order = sel["exclusive_probe_order"]
    gate("sel_size", len(order) == 42)
    by_key = {r["key"]: (i + 1, r["legal"], r["proxy"]) for i, r in enumerate(order)}
    gate("sel_unique", len(by_key) == 42)

    head = set()
    for row in csv.reader(HEAD.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        gate("head_row", row[0] == "s5verdict" and int(row[3]) == 5, str(row))
        head.add((int(row[1]), int(row[2])))
    gate("head_absent_selection", not any(
        tuple(int(x) for x in k.split(":")) in head for k in by_key))

    files = sorted(p for p in RAW.glob("*.out.csv"))
    pat = re.compile(r"^(at2m|at2m-run2|at2m-run3-verify|at15m-run1|at15m-run2|at15m-run3-verify|at50m-run1|at50m-run2)-k(\d{2})\.out\.csv$")
    runs = {}
    for p in files:
        m = pat.match(p.name)
        gate(f"raw_name_{p.name}", m is not None, p.name)
        stage, kidx = m.group(1), int(m.group(2))
        gate(f"raw_kidx_{p.name}", 1 <= kidx <= 42, p.name)
        rows = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            cols = line.split(",")
            gate(f"raw_cols_{p.name}", len(cols) == 11, line)
            rows.append(cols)
        gate(f"raw_nonempty_{p.name}", len(rows) >= 1, p.name)
        gate(f"raw_single_{p.name}", len(rows) == 1, f"{len(rows)} rows")
        c = rows[0]
        gate(f"raw_kind_{p.name}", c[0] == "replay", c[0])
        gate(f"raw_stones_{p.name}", int(c[2]) == 5, c[2])
        legal = int(c[3])
        budget = int(c[5])
        result = int(c[6])
        nodes = int(c[7])
        lo, hi = int(c[9]), int(c[10])
        key = f"{lo}:{hi}"
        gate(f"raw_key_known_{p.name}", key in by_key, key)
        k_no, sel_legal, _ = by_key[key]
        gate(f"raw_kidx_match_{p.name}", k_no == kidx, f"file k{kidx:02d} but order k{k_no:02d}")
        gate(f"raw_legal_{p.name}", legal == sel_legal, f"{legal} vs selection {sel_legal}")
        gate(f"raw_budget_{p.name}", budget == STAGES[stage], f"{stage} budget {budget}")
        gate(f"raw_result_{p.name}", result in (0, 1, 2), str(result))
        gate(f"raw_nodes_le_budget_{p.name}", nodes <= budget, f"{nodes}>{budget}")
        gate(f"raw_unknown_full_{p.name}", result != 0 or nodes == budget,
             f"result {result} nodes {nodes}")
        runs.setdefault(kidx, {})[stage] = (result, nodes, p.name)

    # determinism pairs and stage policy
    resolved, parked, unknown_seen = {}, {}, {}
    for kidx in sorted(runs):
        r = runs[kidx]
        if "at2m" in r:
            res2m = r["at2m"]
            if "at2m-run2" in r:
                gate(f"pair_2m_{kidx:02d}", res2m[:2] == r["at2m-run2"][:2],
                     f"{res2m} vs {r['at2m-run2']}")
            if res2m[0] != 0:
                gate(f"pair_2m_required_{kidx:02d}", "at2m-run2" in r,
                     "resolved at 2M without determinism pair")
                resolved[kidx] = res2m
            else:
                unknown_seen[kidx] = True
        # 15M stage only after 2M UNKNOWN
        for st in ("at15m-run1", "at15m-run2", "at50m-run1", "at50m-run2"):
            if st in r:
                gate(f"stage_order_{kidx:02d}_{st}", "at2m" in r and r["at2m"][0] == 0,
                     f"{st} present without 2M UNKNOWN")
        if "at15m-run1" in r and "at15m-run2" in r:
            a, b = r["at15m-run1"], r["at15m-run2"]
            gate(f"pair_15m_{kidx:02d}", a[:2] == b[:2], f"{a} vs {b}")
            if a[0] == 2:
                resolved[kidx] = a
            elif a[0] == 0:
                parked[kidx] = a

    # WIN stopping rule: after the first WIN key (in ascending ladder order),
    # no later key may have any raw row
    win_keys = sorted(k for k, v in resolved.items() if v[0] == 1)
    if win_keys:
        first_win = win_keys[0]
        later = [k for k in runs if k > first_win]
        gate("win_stopping_rule", not later, f"raws beyond first WIN k{first_win:02d}: {later}")

    out = {
        "schema": "n11-seventhcost-ladder-preaudit-v1",
        "selection_json_sha256": SEL_SHA,
        "head_cache_sha256": HEAD_SHA,
        "raw_files_audited": len(files),
        "keys_with_raws": len(runs),
        "resolved_keys": sorted(resolved),
        "resolved_win_keys": win_keys,
        "parked_keys": sorted(parked),
        "determinism_pairs_present": sorted(
            k for k in runs
            if ("at2m" in runs[k] and "at2m-run2" in runs[k])
            or ("at15m-run1" in runs[k] and "at15m-run2" in runs[k])),
        "gates_passed": len(gates),
        "checkpoint": "partial" if len(runs) < 42 else "full",
        "status_guard": ("Audit of published raw rows only; no verdict is consumed or implied; "
                         "the standard 11x11 empty board, the two-stone root {60,27} and its "
                         "remaining third moves 100/108 remain UNKNOWN."),
    }
    dest = Path(__file__).resolve().parent.parent / "output" / "ladder-preaudit.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
