#!/usr/bin/env python3
"""Pre-registered independent audit instrument for the seventh-cost exclusive S5
ladder (kit research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126).

REVISION 2 (2026-11-27): models the 50M escalation stage. The original revision 1
(sha256 89e816dcc9ea8f201e902a8cd46e721b8739551e66acf7368d658bc0f36b72af) audited
2M/15M raws only: it had no pair_50m determinism gate, did not resolve or park
keys at the 50M stage, and its WIN stopping rule compared ladder key order, which
would false-fail once a 50M WIN row is integrated (the 50M escalation of k05 was
published after the 15M raws of k06..k42, so key order is not the temporal order).

Revision 2 replaces the key-order WIN rule with a ledger-anchored temporal rule:
the published batch-summary checkpoint (pin below; git-published in wave C3
commit 24f40b8b, before any 50M escalation raws existed) is the temporal anchor.
Every key-start and 15M escalation recorded in that ledger provably precedes
any 50M raw row (git publication order). Concretely the instrument now asserts,
fail-closed:

  - the batch-summary pin, schema, class, head basis and counters;
  - ledger vs raw cross-consistency: every ledger stage1_2m row equals the
    published at2m raw; every ledger resolution (2M or 15M) matches the raw
    pair rows; every ledger park matches raw 15M UNKNOWN pairs;
  - every raw 15M start is accounted for by the ledger (a 15M raw for a key the
    ledger does not account for is a post-anchor start and fails);
  - 50M rows only for keys the ledger parked UNKNOWN at 15M, only after the
    15M raw pair exists, with a mandatory determinism pair (pair_50m,
    identical (result, nodes)); result 1 resolves WIN, 2 resolves LOSS,
    0 parks at 50M (nodes == budget is already gated);
  - temporal WIN stopping rule: if any WIN is resolved at any stage, then
    (a) every key with any raw must be covered by the ledger (its stage-1
    start predates the anchor), (b) every 15M raw row must be ledger-accounted
    (its 15M start predates the anchor), and (c) every 50M escalation must be
    of a ledger-parked key. No key-order comparison is made.

The audit still asserts NOTHING about verdicts or class status: it only checks
raw integrity, key provenance, budget/stage consistency, determinism pairs and
stopping-rule consistency of what is published. Partial checkpoints are legal.
The standard 11x11 board and every root/class stay UNKNOWN.
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
BS = KIT / "output/batch-summary.json"
HEAD = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache"
RAW = KIT / "output/raw"

SEL_SHA = "c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627"
HEAD_SHA = "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4"
# batch-summary checkpoint, git-published at wave C3 (commit 24f40b8b) BEFORE any
# 50M escalation raw existed: the temporal anchor of the ledger (see docstring).
BS_SHA = "6881eaaf48e900c96d8816017a5d052054d5ebbf4f0b3dc9e621df732ce01c2b"

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
    gate("pin_batch_summary", sha(BS) == BS_SHA, str(BS))
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

    bs = json.loads(BS.read_text(encoding="utf-8"))
    gate("bs_schema", bs["schema"] == "n11-seventhcost-batch-checkpoint-summary-v1",
         str(bs.get("schema")))
    gate("bs_class", bs["class"] == sel.get("class"), f"{bs.get('class')} vs {sel.get('class')}")
    gate("bs_head_basis_sha", bs["head_basis"]["sha256"] == HEAD_SHA,
         str(bs["head_basis"].get("sha256")))
    gate("bs_batch_keys", bs["batch_keys"] == 42, str(bs["batch_keys"]))
    per_key = bs["per_key"]
    gate("bs_per_key_len", len(per_key) == 42, str(len(per_key)))

    # ledger: position, key, stage-1 result, stage-2 status
    ledger = {}
    for e in per_key:
        pos, key = e["pos"], e["key"]
        gate("bs_key_known", key in by_key, key)
        k_no, _, _ = by_key[key]
        gate("bs_pos_match", k_no == pos, f"ledger pos {pos} but selection k{k_no:02d}")
        st1 = e["stage1_2m"]
        gate("bs_stage1_domain", set(st1) == {"result", "nodes"}, str(st1))
        if "resolved" in e:
            r = e["resolved"]
            gate("bs_resolved_domain", set(r) == {"stage", "result", "nodes", "pair"},
                 str(r))
            gate("bs_resolved_stage", r["stage"] in ("2m", "15m"), str(r["stage"]))
            gate("bs_resolved_pair", r["pair"] == "identical", str(r.get("pair")))
            status = ("resolved", r["stage"], r["result"], r["nodes"])
        elif e.get("parked_unknown_15m"):
            gate("bs_parked_flags", "stage2_15m_pair" in e, str(sorted(e)))
            status = ("parked15m",)
        else:
            gate("bs_entry_status", False, f"pos {pos} neither resolved nor parked")
            status = None
        ledger[pos] = (key, st1, status)
    gate("bs_ledger_unique", len(ledger) == 42, str(len(ledger)))
    n_res = sum(1 for v in ledger.values() if v[2][0] == "resolved")
    n_park = sum(1 for v in ledger.values() if v[2][0] == "parked15m")
    gate("bs_counter_loss", bs["resolved_exact_loss"] == n_res,
         f"{bs['resolved_exact_loss']} vs {n_res}")
    gate("bs_counter_parked", bs["parked_unknown_15m"] == n_park,
         f"{bs['parked_unknown_15m']} vs {n_park}")
    gate("bs_counter_win", bs["resolved_exact_win"] == 0,
         str(bs["resolved_exact_win"]))
    gate("bs_parked_keys_list",
         sorted(ledger[p][0] for p in ledger if ledger[p][2][0] == "parked15m")
         == sorted(bs["parked_keys"]), str(bs["parked_keys"]))
    sum15 = sum(v[2][3] for v in ledger.values()
                if v[2][0] == "resolved" and v[2][1] == "15m")
    sum2 = sum(v[2][3] for v in ledger.values()
               if v[2][0] == "resolved" and v[2][1] == "2m")
    gate("bs_nodes_bookkeeping",
         bs["nodes_bookkeeping"]["resolved_15m_nodes_sum"] == sum15
         and bs["nodes_bookkeeping"]["resolved_2m_nodes_sum"] == sum2,
         f"15m {bs['nodes_bookkeeping']['resolved_15m_nodes_sum']} vs {sum15}; "
         f"2m {bs['nodes_bookkeeping']['resolved_2m_nodes_sum']} vs {sum2}")

    files = sorted(p for p in RAW.glob("*.out.csv"))
    pat = re.compile(r"^(at2m|at2m-run2|at2m-run3-verify|at15m-run1|at15m-run2|at15m-run3-verify|at50m-run1|at50m-run2)-k(\d{2})\.out\.csv$")
    runs = {}
    raw_keys = {}
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
        raw_keys[kidx] = key
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

    # ledger vs raw cross-consistency (fail-closed, unconditional)
    ledger15_started, ledger_parked = set(), set()
    for kidx, (key, st1, status) in sorted(ledger.items()):
        r = runs.get(kidx, {})
        gate(f"ledger_at2m_raw_present_{kidx:02d}", "at2m" in r, f"k{kidx:02d}")
        if "at2m" in r:
            gate(f"ledger_stage1_match_{kidx:02d}",
                 (st1["result"], st1["nodes"]) == r["at2m"][:2],
                 f"ledger {st1} vs raw {r['at2m']}")
        if status[0] == "resolved":
            stage_name = {"2m": "at2m", "15m": "at15m-run1"}[status[1]]
            gate(f"ledger_resolution_raw_present_{kidx:02d}", stage_name in r,
                 f"k{kidx:02d} resolved at {status[1]} without raw")
            if stage_name in r:
                gate(f"ledger_resolution_match_{kidx:02d}",
                     (status[2], status[3]) == r[stage_name][:2],
                     f"ledger {(status[2], status[3])} vs raw {r[stage_name]}")
            if status[1] == "2m":
                gate(f"ledger_resolved2m_pair_present_{kidx:02d}", "at2m-run2" in r,
                     f"k{kidx:02d}")
            else:
                ledger15_started.add(kidx)
        else:  # parked15m
            gate(f"ledger_parked15m_pair_present_{kidx:02d}",
                 "at15m-run1" in r and "at15m-run2" in r, f"k{kidx:02d}")
            if "at15m-run1" in r:
                gate(f"ledger_parked15m_match_{kidx:02d}",
                     (0, 15000000) == r["at15m-run1"][:2],
                     f"raw {r['at15m-run1']}")
            ledger15_started.add(kidx)
            ledger_parked.add(kidx)

    # every raw 15M start must be ledger-accounted (temporal anchor)
    for kidx in sorted(runs):
        has15 = any(s in runs[kidx] for s in ("at15m-run1", "at15m-run2", "at15m-run3-verify"))
        gate(f"stage2_15m_ledger_accounted_{kidx:02d}",
             (not has15) or kidx in ledger15_started,
             f"k{kidx:02d} has 15M raws but ledger does not account a 15M start")

    # determinism pairs and stage policy
    resolved, parked, parked50 = {}, {}, {}
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
                pass
        # 15M/50M stage only after 2M UNKNOWN
        for st in ("at15m-run1", "at15m-run2", "at50m-run1", "at50m-run2"):
            if st in r:
                gate(f"stage_order_{kidx:02d}_{st}", "at2m" in r and r["at2m"][0] == 0,
                     f"{st} present without 2M UNKNOWN")
        if "at15m-run1" in r and "at15m-run2" in r:
            a, b = r["at15m-run1"], r["at15m-run2"]
            gate(f"pair_15m_{kidx:02d}", a[:2] == b[:2], f"{a} vs {b}")
            if a[0] == 2:
                resolved[kidx] = a
            elif a[0] == 1:
                resolved[kidx] = a
            else:
                parked[kidx] = a
        # 50M escalation: only ledger-parked keys, after a 15M UNKNOWN pair
        if "at50m-run1" in r or "at50m-run2" in r:
            gate(f"at50m_ledger_parked_{kidx:02d}", kidx in ledger_parked,
                 f"k{kidx:02d} escalated to 50M but ledger does not park it")
            gate(f"at50m_after_parked15m_{kidx:02d}",
                 "at15m-run1" in r and r["at15m-run1"][0] == 0,
                 f"k{kidx:02d} 50M without 15M UNKNOWN raw")
            gate(f"pair_50m_required_{kidx:02d}",
                 "at50m-run1" in r and "at50m-run2" in r,
                 f"k{kidx:02d} 50M without determinism pair")
            if "at50m-run1" in r and "at50m-run2" in r:
                a, b = r["at50m-run1"], r["at50m-run2"]
                gate(f"pair_50m_{kidx:02d}", a[:2] == b[:2], f"{a} vs {b}")
                if a[0] in (1, 2):
                    resolved[kidx] = a
                    parked.pop(kidx, None)
                elif a[0] == 0:
                    parked50[kidx] = a

    # ledger-covered key set (temporal anchor: all 42 selection keys)
    ledger_keys = set(ledger)

    # temporal WIN stopping rule (ledger-anchored; no key-order comparison)
    win_keys = sorted(k for k, v in resolved.items() if v[0] == 1)
    if win_keys:
        gate("win_all_raws_predate_anchor",
             set(runs) <= ledger_keys,
             f"raw keys outside ledger: {sorted(set(runs) - ledger_keys)}")
        gate("win_15m_starts_predate_anchor",
             all(k in ledger15_started for k in runs
                 if any(s in runs[k] for s in ("at15m-run1", "at15m-run2", "at15m-run3-verify"))),
             "15M start not accounted by ledger")
        gate("win_50m_escalations_from_parked",
             all(k in ledger_parked for k in runs
                 if any(s in runs[k] for s in ("at50m-run1", "at50m-run2"))),
             "50M escalation of a non-parked key")
        gate("win_ledger_consistent_pre_win",
             bs["win_stopping_rule_fired"] is False
             and bs["resolved_exact_win"] == 0,
             "ledger already recorded a WIN or fired stopping rule")

    out = {
        "schema": "n11-seventhcost-ladder-preaudit-v2",
        "revision": 2,
        "selection_json_sha256": SEL_SHA,
        "head_cache_sha256": HEAD_SHA,
        "batch_summary_sha256": BS_SHA,
        "raw_files_audited": len(files),
        "keys_with_raws": len(runs),
        "resolved_keys": sorted(resolved),
        "resolved_win_keys": win_keys,
        "parked_keys": sorted(parked),
        "parked_50m_keys": sorted(parked50),
        "escalated_50m_keys": sorted(
            k for k in runs if "at50m-run1" in runs[k] or "at50m-run2" in runs[k]),
        "determinism_pairs_present": sorted(
            k for k in runs
            if ("at2m" in runs[k] and "at2m-run2" in runs[k])
            or ("at15m-run1" in runs[k] and "at15m-run2" in runs[k])
            or ("at50m-run1" in runs[k] and "at50m-run2" in runs[k])),
        "win_stopping_rule_model": "temporal-ledger-anchored",
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
