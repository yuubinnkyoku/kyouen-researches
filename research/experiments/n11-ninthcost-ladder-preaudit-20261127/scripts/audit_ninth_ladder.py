#!/usr/bin/env python3
"""Pre-registered-independent audit instrument for the ninth-cost exclusive
S5 ladder (kit research/experiments/n11-ninthcost-class-s5-exclusive-probe-
1297036692683751424-20261127), covering the stage-1 2M sweep, the stage-2
15M escalation (8 LOSS + k12 WIN + 3 parked + k13 overreach) and the
stage-3 50M parked escalation (k02/k04/k07).

Fresh implementation structurally modeled on the published eighth-cost
pre-audit instrument (audit_eighth_ladder.py, sha256 91d98fe2..., disclosed)
and the seventh-cost revision 2 (5b47ac7f..., disclosed) - NOT a byte
transform: the pin set, the multi-stage modeling and the parked/overreach
gates are new because the ninth-cost batch structure differs:

  - stage-1: 45 keys x 2 cold passes at 2M, all UNKNOWN (90 raws);
  - stage-2 15M: 13 keys escalated in ascending batch order (26 raws):
    8 exact LOSS, k12 WIN(1) 14521862 (WIN stopping rule FIRED there;
    k14..k45 escalation suppressed - no 15M raws may exist for them),
    k02/k04/k07 parked UNKNOWN@15M, and k13 executed post-determination
    inside the same batch command: its 15M raw pair IS published but the
    ledger marks it overreach - official status of k13 = 2M UNKNOWN pair,
    escalation suppressed;
  - stage-3 50M: the three ledger-parked keys escalated (6 raws), declared
    in research/log/2026-11-27-n11-ninthcost-parked3-l50m-escalation-single-owner.md
    (publish-then-execute, commit 59db0d52);
  - the batch-summary-15m ledger was git-published in the SAME commit
    (7332d958) as the 15M raws, so it is NOT a proven-preceding temporal
    anchor: the instrument checks the CONTENT invariant that embodies the
    stop rule (15M raws exist only for k01..k13; k13 is overreach-only in
    the ledger; no 15M raws for k14..k45) instead of git ordering.

The instrument asserts NOTHING about verdicts or class status: it only
checks raw integrity, key provenance, budget/stage consistency,
determinism pairs, ledger cross-consistency, WIN-stop content
consistency, overreach disclosure consistency and 50M-stage consistency.
Nodes are bookkeeping. The standard 11x11 board and every root/class stay
UNKNOWN.

Fail-closed: any gate failure -> rc=1.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SEL_SHA = "772c9235fe226e9b52a36a6860ef2096a099a3be374daf0b80de21ee81bd4568"
BS15_SHA = "f1a1d803c69f37ee05f1ac82000a9e5945671616c9cfe12119ace82597321b15"
BS50_SHA = "e0b27ffd2b931a802569db533b2c43eaa0fcec7d3fb690e9ac881de60ba5ecba"
HEAD_SHA = "0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4"
HEAD_ROWS, HEAD_WIN, HEAD_LOSS = 6875, 203, 6672
CLASS = "1297036692683751424:134217728"
N_KEYS = 45
N_15M_KEYS = 13
WIN_KEY_POS, WIN_NODES = 12, 14521862
K13_NODES = 4217733
PARKED = ["k02", "k04", "k07"]
LOSS_15M = {1: 2163556, 3: 7753840, 5: 8687533, 6: 8130387,
            8: 3306768, 9: 4711230, 10: 5542083, 11: 5931960}
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def replay_row(p: Path):
    m = None
    for line in p.read_text().splitlines():
        if line.startswith("replay,"):
            if m is not None:
                return None  # more than one replay row
            m = REPLAY.match(line)
    return m.groups() if m else None


def main() -> int:
    kit = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    head = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    gates = {}

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
        return bool(ok)

    ok = True

    sel_path = kit / "output" / "ninth-cost-exclusive-keys.json"
    bs15_path = kit / "output" / "batch-summary-15m.json"
    bs50_path = kit / "output" / "batch-summary-l50m.json"
    raw = kit / "output" / "raw"
    man_path = kit / "MANIFEST-raw-sha256.txt"

    # P0: pins
    ok &= g("P0:selection-sha", sha256(sel_path) == SEL_SHA, sha256(sel_path))
    sel = json.loads(sel_path.read_text())
    ok &= g("P0:selection-schema", sel.get("schema") == "n11-ninthcost-exclusive-selection-v1", sel.get("schema"))
    ok &= g("P0:selection-class", sel.get("class") == CLASS, sel.get("class"))
    hb = sel.get("head_basis", {})
    ok &= g("P0:selection-head-basis", hb.get("sha256") == HEAD_SHA and hb.get("rows") == HEAD_ROWS
            and hb.get("win") == HEAD_WIN and hb.get("loss") == HEAD_LOSS, "")
    epo = sel.get("exclusive_probe_order", [])
    ok &= g("P0:selection-order-len", len(epo) == N_KEYS, len(epo))
    keys = [e.get("key") for e in epo]
    ok &= g("P0:selection-order-unique", len(set(keys)) == N_KEYS, "")
    ok &= g("P0:selection-unknown-exclusive", sel.get("unknown_exclusive_head") == N_KEYS, sel.get("unknown_exclusive_head"))

    ok &= g("P0:batch-summary-15m-sha", sha256(bs15_path) == BS15_SHA, sha256(bs15_path))
    bs15 = json.loads(bs15_path.read_text())
    ok &= g("P0:batch-summary-15m-schema", bs15.get("schema") == "n11-ninthcost-batch-checkpoint-summary-v1", bs15.get("schema"))
    ok &= g("P0:batch-summary-15m-class", bs15.get("class") == CLASS, bs15.get("class"))
    ok &= g("P0:batch-summary-15m-head-basis", bs15.get("head_basis") == HEAD_SHA[:8], bs15.get("head_basis"))
    ok &= g("P0:batch-summary-15m-counters", bs15.get("keys_total") == N_KEYS
            and bs15.get("stage1_2m", {}).get("rows") == 90
            and bs15.get("stage1_2m", {}).get("all_unknown") is True
            and bs15.get("stage1_2m", {}).get("pairs_node_identical") == 45
            and bs15.get("pairs_node_identical") == 13
            and bs15.get("jsreplay_sha256") == JSREPLAY_SHA, "")
    led_loss = bs15.get("stage2_15m_resolved_loss", [])
    ok &= g("P0:ledger-loss-list", sorted(l.split()[0] for l in led_loss) == sorted("k%02d" % p for p in LOSS_15M), led_loss)
    ok &= g("P0:ledger-loss-nodes", all(int(l.split()[1]) == LOSS_15M[int(l.split()[0][1:])] for l in led_loss), "")
    led_win = bs15.get("stage2_15m_resolved_win", [])
    ok &= g("P0:ledger-win-list", len(led_win) == 1 and led_win[0].split()[0] == "k12"
            and int(led_win[0].split()[1]) == WIN_NODES, led_win)
    ok &= g("P0:ledger-parked-list", bs15.get("stage2_15m_parked_unknown_at15m") == PARKED, bs15.get("stage2_15m_parked_unknown_at15m"))
    wsr = bs15.get("win_stopping_rule", "")
    ok &= g("P0:ledger-win-stop-text", isinstance(wsr, str) and "FIRED" in wsr and "k12" in wsr
            and str(WIN_NODES) in wsr and "k13..k45" in wsr, wsr[:80])
    ovd = bs15.get("overreach_disclosure", "")
    ok &= g("P0:ledger-overreach-text", isinstance(ovd, str) and "k13" in ovd and str(K13_NODES) in ovd
            and "LOSS 2" in ovd and "2M UNKNOWN pair" in ovd, ovd[:80])

    # P0b: head cache freshness (ALL 45 key pairs absent)
    ok &= g("P0:head-sha", head is not None and sha256(head) == HEAD_SHA, "" if head else "head arg missing")
    if head is not None:
        data = [l for l in head.read_text().splitlines() if l.startswith("s5verdict,")]
        wins = sum(1 for l in data if l.split(",")[4] == "1")
        losses = sum(1 for l in data if l.split(",")[4] == "2")
        ok &= g("P0:head-census", len(data) == HEAD_ROWS and wins == HEAD_WIN and losses == HEAD_LOSS,
                "rows=%d WIN=%d LOSS=%d" % (len(data), wins, losses))
        present = [k for k in keys if any(l.split(",")[1] == k.split(":")[0] and l.split(",")[2] == k.split(":")[1] for l in data)]
        ok &= g("P0:freshness-all-45-keys-absent", not present, "present=%s" % present[:3])

    # P1: raw manifest
    man = [l.split() for l in man_path.read_text().splitlines() if l.strip()]
    ok &= g("P1:manifest-count", len(man) == 90 + 2 * N_15M_KEYS + 2 * len(PARKED), len(man))
    ok &= g("P1:manifest-sha-all", all(sha256(kit / r[2]) == r[0] for r in man), "")
    at2m = [r for r in man if "/at2m-" in r[2]]
    at15m = [r for r in man if "/at15m-" in r[2]]
    at50m = [r for r in man if "/at50m-" in r[2]]
    ok &= g("P1:manifest-at2m-90", len(at2m) == 90, len(at2m))
    ok &= g("P1:manifest-at15m-26", len(at15m) == 26, len(at15m))
    ok &= g("P1:manifest-at50m-6", len(at50m) == 6, len(at50m))
    ok &= g("P1:at15m-keys-k01-k13-only",
            sorted({r[2].split("/")[-1] for r in at15m}) == sorted("k%02d.out.csv" % p for p in range(1, 14)),
            "%s" % sorted({r[2].split("/")[-1] for r in at15m}))
    ok &= g("P1:at50m-keys-parked-only", sorted({r[2].split("/")[-1] for r in at50m}) == sorted("%s.out.csv" % k for k in PARKED),
            "%s" % sorted({r[2].split("/")[-1] for r in at50m}))
    tree = sorted(str(p.relative_to(kit)) for p in raw.rglob("*.csv"))
    ok &= g("P1:raw-tree==manifest", tree == sorted(r[2] for r in man), "")

    # P2/P3: raw rows, provenance, determinism (2M stage: all 45)
    for pos, e in enumerate(epo, 1):
        kidx = "k%02d" % pos
        key, legal = e["key"], e["legal"]
        lo, hi = key.split(":")
        r1 = raw / ("at2m-run1/%s.out.csv" % kidx)
        r2 = raw / ("at2m-run2/%s.out.csv" % kidx)
        f1, f2 = replay_row(r1), replay_row(r2)
        good = f1 and f2
        ok &= g("P2:%s:2m-row" % kidx, bool(good), "")
        if good:
            for f, tag in ((f1, "run1"), (f2, "run2")):
                ok &= g("P2:%s:%s:provenance" % (kidx, tag),
                        f[8] == lo and f[9] == hi and f[2] == str(legal),
                        "key=%s:%s legal=%s exp=%s:%s/%s" % (f[8], f[9], f[2], lo, hi, legal))
                ok &= g("P2:%s:%s:budget" % (kidx, tag), f[4] == "2000000", f[4])
                ok &= g("P2:%s:%s:unknown-2m" % (kidx, tag), f[5] == "0" and f[6] == "2000000",
                        "result=%s nodes=%s" % (f[5], f[6]))
            ok &= g("P3:%s:2m-pair-identity" % kidx, f1[:7] == f2[:7] and f1[8:] == f2[8:], "")

    # 15M stage: k01..k13
    for pos in range(1, 14):
        kidx = "k%02d" % pos
        e = epo[pos - 1]
        lo, hi = e["key"].split(":")
        f1 = replay_row(raw / ("at15m-run1/%s.out.csv" % kidx))
        f2 = replay_row(raw / ("at15m-run2/%s.out.csv" % kidx))
        ok &= g("P2:%s:15m-rows" % kidx, bool(f1 and f2), "")
        if f1 and f2:
            for f, tag in ((f1, "run1"), (f2, "run2")):
                ok &= g("P2:%s:%s:15m-provenance" % (kidx, tag),
                        f[8] == lo and f[9] == hi and f[2] == str(e["legal"]),
                        "key=%s:%s exp=%s:%s" % (f[8], f[9], lo, hi))
                ok &= g("P2:%s:%s:15m-budget" % (kidx, tag), f[4] == "15000000", f[4])
            ok &= g("P3:%s:15m-pair-identity" % kidx, f1[:7] == f2[:7] and f1[8:] == f2[8:], "")
            if pos in LOSS_15M:
                ok &= g("P2:%s:15m-loss" % kidx, f1[5] == "2" and f1[6] == str(LOSS_15M[pos]),
                        "result=%s nodes=%s exp=%d" % (f1[5], f1[6], LOSS_15M[pos]))
                ok &= g("P2:%s:loss-inside-budget" % kidx, int(f1[6]) <= int(f1[4]), "")
            elif pos == WIN_KEY_POS:
                ok &= g("P2:k12:15m-win", f1[5] == "1" and f1[6] == str(WIN_NODES),
                        "result=%s nodes=%s" % (f1[5], f1[6]))
                ok &= g("P2:k12:win-inside-budget", int(f1[6]) <= int(f1[4]), "")
            elif kidx in PARKED:
                ok &= g("P2:%s:15m-parked-unknown" % kidx, f1[5] == "0" and f1[6] == "15000000",
                        "result=%s nodes=%s" % (f1[5], f1[6]))
            else:  # k13 overreach: raw published, status 2M UNKNOWN
                ok &= g("P2:k13:15m-overreach-loss-observed",
                        pos == 13 and f1[5] == "2" and f1[6] == str(K13_NODES),
                        "pos=%d result=%s nodes=%s" % (pos, f1[5], f1[6]))

    # no 15M raws for k14..k45 (WIN stopping rule content invariant)
    stray = [kidx for pos in range(14, 46) for kidx in ("k%02d" % pos,)
             if (raw / ("at15m-run1/%s.out.csv" % kidx)).exists() or (raw / ("at15m-run2/%s.out.csv" % kidx)).exists()]
    ok &= g("P5:no-15m-raws-k14-k45", not stray, "%s" % stray)

    # P4: 50M stage vs its ledger
    if not bs50_path.exists():
        ok &= g("P4:bs50-present", False, "batch-summary-l50m.json missing")
        bs50 = {}
    else:
        ok &= g("P4:bs50-sha", sha256(bs50_path) == BS50_SHA, sha256(bs50_path))
        bs50 = json.loads(bs50_path.read_text())
        ok &= g("P4:bs50-schema", bs50.get("schema") == "n11-ninthcost-parked3-l50m-summary-v1", bs50.get("schema"))
        ok &= g("P4:bs50-class", bs50.get("class") == CLASS, bs50.get("class"))
        ok &= g("P4:bs50-head-basis", bs50.get("head_basis") == HEAD_SHA[:8], bs50.get("head_basis"))
        ok &= g("P4:bs50-declaration-pin", isinstance(bs50.get("declaration_log"), str)
                and "2026-11-27-n11-ninthcost-parked3-l50m-escalation-single-owner.md" in bs50.get("declaration_log", ""), "")
        ok &= g("P4:bs50-jsreplay", bs50.get("jsreplay_sha256") == JSREPLAY_SHA, "")
        ok &= g("P4:bs50-targets", bs50.get("targets") == PARKED, bs50.get("targets"))
    pk50 = bs50.get("per_key", {})
    ok &= g("P4:bs50-per-key-len", len(pk50) == len(PARKED), len(pk50))
    for kidx in PARKED if bs50 else []:
        pos = int(kidx[1:])
        e = epo[pos - 1]
        lo, hi = e["key"].split(":")
        row = pk50.get(kidx, {})
        f1 = replay_row(raw / ("at50m-run1/%s.out.csv" % kidx))
        f2 = replay_row(raw / ("at50m-run2/%s.out.csv" % kidx))
        ok &= g("P4:%s:50m-rows" % kidx, bool(f1 and f2), "")
        if f1 and f2:
            for f, tag in ((f1, "run1"), (f2, "run2")):
                ok &= g("P2:%s:%s:50m-provenance" % (kidx, tag),
                        f[8] == lo and f[9] == hi and f[2] == str(e["legal"]),
                        "key=%s:%s exp=%s:%s" % (f[8], f[9], lo, hi))
                ok &= g("P2:%s:%s:50m-budget" % (kidx, tag), f[4] == "50000000", f[4])
            ok &= g("P3:%s:50m-pair-identity" % kidx, f1[:7] == f2[:7] and f1[8:] == f2[8:], "")
            ok &= g("P4:%s:50m-ledger==raw" % kidx,
                    row.get("result") == int(f1[5]) and row.get("nodes") == int(f1[6])
                    and row.get("pair") == "identical",
                    "ledger=%s raw=%s,%s" % (row, f1[5], f1[6]))
            ok &= g("P4:%s:50m-result-domain" % kidx, f1[5] in ("0", "1", "2"), f1[5])
            if f1[5] == "0":
                ok &= g("P4:%s:50m-unknown-full-budget" % kidx, f1[6] == "50000000", f1[6])
            else:
                ok &= g("P4:%s:50m-resolved-inside-budget" % kidx, int(f1[6]) <= int(f1[4]), "")

    # P5: no 50M raws for non-parked keys
    stray50 = [kidx for pos in range(1, 46) for kidx in ("k%02d" % pos,)
               if kidx not in PARKED and ((raw / ("at50m-run1/%s.out.csv" % kidx)).exists()
                                          or (raw / ("at50m-run2/%s.out.csv" % kidx)).exists())]
    ok &= g("P5:no-50m-raws-non-parked", not stray50, "%s" % stray50)

    # P6: guards
    ok &= g("P6:status-guard", "UNKNOWN" in json.dumps(bs15.get("guards", "")) and "UNKNOWN" in json.dumps(bs50.get("guards", "")), "")

    out = {
        "schema": "n11-ninthcost-ladder-preaudit-v1",
        "kit": "research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127",
        "selection_sha256": SEL_SHA, "batch_summary_15m_sha256": BS15_SHA,
        "batch_summary_50m_sha256": BS50_SHA, "head_sha256": HEAD_SHA,
        "raws": len(man), "keys": N_KEYS,
        "stages": {"2m_unknown": 45, "15m_loss": 8, "15m_win": 1, "15m_parked": 3,
                   "15m_overreach_disclosed": 1, "50m_targets": len(PARKED)},
        "overreach_disclosed": True,
        "temporal_anchor_disclosure": ("batch-summary-15m ledger git-published in the SAME commit as the 15M raws "
                                       "(7332d958): content-level WIN-stop invariant checked (15M raws only for "
                                       "k01..k13; k13 pair published as overreach observation with official status "
                                       "2M UNKNOWN; no 15M raws for k14..k45; 50M raws only for the 3 ledger-parked keys "
                                       "per the wave-A declaration 59db0d52); no git-preceding ledger anchor exists "
                                       "for the 15M batch"),
        "gates": gates, "overall": "PASS" if ok else "FAIL",
    }
    print(json.dumps({"overall": out["overall"], "gates": len(gates)}))
    fails = [k for k, v in sorted(gates.items()) if v["status"] == "FAIL"]
    for k in fails:
        print("FAIL", k, gates[k]["detail"][:120])
    if out_path is not None:
        out_path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
