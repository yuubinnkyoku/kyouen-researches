#!/usr/bin/env python3
"""Pre-registered independent audit instrument for the eighth-cost exclusive
S5 ladder (kit research/experiments/n11-eighthcost-class-s5-exclusive-probe-
1297036692750860288-20261127).

Fresh implementation for the eighth-cost batch, structurally modeled on the
published seventh-cost pre-audit instrument revision 2
(audit_seventh_ladder.py, sha256 5b47ac7f..., disclosed) - NOT a byte
transform: the pin set, the WIN-stop modeling and the overreach gates are new
because the eighth-cost batch structure differs:

  - the batch resolved at the 15M stage with ONE WIN (k01
    1297036692750860288:64) and 42 keys SUPPRESSED by the pre-registered WIN
    stopping rule (no LOSS, no parked, no 50M stage);
  - the batch-summary ledger was git-published in the SAME commit (0005e5b1)
    as the raws, so it is NOT a proven-preceding temporal anchor (unlike the
    seventh-cost 50M case). The instrument therefore checks the CONTENT
    invariant that embodies the stop rule: the official raw set contains 15M
    rows ONLY for the WIN key, every other key has exactly its 2M UNKNOWN
    pair, and the single post-anchor host execution (k02 15M pair) lives only
    in the ledger's overreach_disclosure with its observed values and must
    NOT appear as an official raw;
  - freshness is stronger here than the seventh-cost instrument: ALL 43
    selection key pairs must be ABSENT from the canonical head 5b6e77f7.

The instrument asserts NOTHING about verdicts or class status: it only
checks raw integrity, key provenance, budget/stage consistency,
determinism pairs, ledger cross-consistency, WIN-stop content consistency
and overreach disclosure consistency. Nodes are bookkeeping. The standard
11x11 board and every root/class stay UNKNOWN.

Fail-closed: any gate failure -> rc=1 and no output rewrite of a PASS.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SEL_SHA = "691dcd807d52b9b9dbe0118f2347db9a613565377350246fda53a6c518aeef33"
BS_SHA = "2379dbe031c59b368407a41a65c5366d5209234045c149d0ec2d40136698ba08"
HEAD_SHA = "5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2"
HEAD_ROWS, HEAD_WIN, HEAD_LOSS = 6874, 202, 6672
CLASS = "1297036692750860288:0"
WIN_KEY = "1297036692750860288:64"
WIN_NODES = 8514427
N_KEYS = 43
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

    sel_path = kit / "output" / "eighth-cost-exclusive-keys.json"
    bs_path = kit / "output" / "batch-summary.json"
    raw = kit / "output" / "raw"
    man_path = kit / "MANIFEST-raw-sha256.txt"

    # P0: pins
    ok &= g("P0:selection-sha", sha256(sel_path) == SEL_SHA, sha256(sel_path))
    sel = json.loads(sel_path.read_text())
    ok &= g("P0:selection-schema", sel.get("schema") == "n11-eighthcost-exclusive-selection-v1", sel.get("schema"))
    ok &= g("P0:selection-class", sel.get("class") == CLASS, sel.get("class"))
    hb = sel.get("head_basis", {})
    ok &= g("P0:selection-head-basis", hb.get("sha256") == HEAD_SHA and hb.get("rows") == HEAD_ROWS
            and hb.get("win") == HEAD_WIN and hb.get("loss") == HEAD_LOSS, "")
    epo = sel.get("exclusive_probe_order", [])
    ok &= g("P0:selection-order-len", len(epo) == N_KEYS, len(epo))
    keys = [e.get("key") for e in epo]
    ok &= g("P0:selection-order-unique", len(set(keys)) == N_KEYS, "")
    ok &= g("P0:selection-unknown-exclusive", sel.get("unknown_exclusive_head") == N_KEYS, sel.get("unknown_exclusive_head"))

    ok &= g("P0:batch-summary-sha", sha256(bs_path) == BS_SHA, sha256(bs_path))
    bs = json.loads(bs_path.read_text())
    ok &= g("P0:batch-summary-schema", bs.get("schema") == "n11-eighthcost-batch-checkpoint-summary-v1", bs.get("schema"))
    ok &= g("P0:batch-summary-class", bs.get("class") == CLASS, bs.get("class"))
    ok &= g("P0:batch-summary-head-basis", bs.get("head_basis", {}).get("sha256") == HEAD_SHA, "")
    ok &= g("P0:batch-summary-counters", bs.get("batch_keys") == N_KEYS
            and bs.get("resolved_exact_loss") == 0 and bs.get("resolved_exact_win") == 1
            and bs.get("win_resolved_keys") == [WIN_KEY]
            and bs.get("parked_unknown_15m") == 0 and bs.get("parked_keys") == []
            and bs.get("win_stopping_rule_fired") is True, "")

    # P0b: head cache freshness (ALL keys absent)
    ok &= g("P0:head-sha", head is not None and sha256(head) == HEAD_SHA, "" if head else "head arg missing")
    if head is not None:
        data = [l for l in head.read_text().splitlines() if l.startswith("s5verdict,")]
        wins = sum(1 for l in data if l.split(",")[4] == "1")
        losses = sum(1 for l in data if l.split(",")[4] == "2")
        ok &= g("P0:head-census", len(data) == HEAD_ROWS and wins == HEAD_WIN and losses == HEAD_LOSS,
                "rows=%d WIN=%d LOSS=%d" % (len(data), wins, losses))
        present = [k for k in keys if any(l.split(",")[1] == k.split(":")[0] and l.split(",")[2] == k.split(":")[1] for l in data)]
        ok &= g("P0:freshness-all-43-keys-absent", not present, "present=%s" % present[:3])

    # P1: raw manifest
    man = [l.split() for l in man_path.read_text().splitlines() if l.strip()]
    ok &= g("P1:manifest-count", len(man) == 86 + 2, len(man))
    ok &= g("P1:manifest-sha-all", all(sha256(kit / r[2]) == r[0] for r in man), "")
    at2m = [r for r in man if "/at2m-" in r[2]]
    at15m = [r for r in man if "/at15m-" in r[2]]
    ok &= g("P1:manifest-at2m-86", len(at2m) == 86, len(at2m))
    ok &= g("P1:manifest-at15m-only-k01", len(at15m) == 2 and all("/k01.out.csv" in r[2] for r in at15m),
            "%s" % [r[2] for r in at15m])
    tree = sorted(str(p.relative_to(kit)) for p in raw.rglob("*.csv"))
    ok &= g("P1:raw-tree==manifest", tree == sorted(r[2] for r in man), "")

    # P2/P3: raw rows, provenance, determinism
    pairs = {}
    for pos, e in enumerate(epo, 1):
        kidx = "k%02d" % pos
        key, legal = e["key"], e["legal"]
        lo, hi = key.split(":")
        r1 = raw / ("at2m-run1/%s.out.csv" % kidx)
        r2 = raw / ("at2m-run2/%s.out.csv" % kidx)
        f1, f2 = replay_row(r1), replay_row(r2)
        good = f1 and f2
        ok &= g("P2:%s:row" % kidx, bool(good), "")
        if good:
            for f, tag in ((f1, "run1"), (f2, "run2")):
                ok &= g("P2:%s:%s:provenance" % (kidx, tag),
                        f[8] == lo and f[9] == hi and f[2] == str(legal),
                        "key=%s:%s legal=%s exp=%s:%s/%s" % (f[8], f[9], f[2], lo, hi, legal))
                ok &= g("P2:%s:%s:budget" % (kidx, tag), f[4] == "2000000", f[4])
                ok &= g("P2:%s:%s:unknown-2m" % (kidx, tag), f[5] == "0" and f[6] == "2000000",
                        "result=%s nodes=%s" % (f[5], f[6]))
            ok &= g("P3:%s:pair-identity" % kidx, f1[:7] == f2[:7] and f1[8:] == f2[8:], "")
            pairs[kidx] = (f1, f2)
    f1, f2 = replay_row(raw / "at15m-run1/k01.out.csv"), replay_row(raw / "at15m-run2/k01.out.csv")
    ok &= g("P2:k01:at15m-rows", bool(f1 and f2), "")
    if f1 and f2:
        ok &= g("P2:k01:at15m-provenance", f1[8] == WIN_KEY.split(":")[0] and f1[9] == "64" and f1[2] == "84", "")
        ok &= g("P2:k01:at15m-budget", f1[4] == "15000000" and f2[4] == "15000000", "")
        ok &= g("P2:k01:at15m-win", f1[5] == "1" and f1[6] == str(WIN_NODES), "result=%s nodes=%s" % (f1[5], f1[6]))
        ok &= g("P3:k01:at15m-pair-identity", f1[:7] == f2[:7] and f1[8:] == f2[8:], "")
        ok &= g("P2:k01:win-inside-budget", int(f1[6]) <= int(f1[4]), "")

    # P4: ledger cross-consistency
    pk = bs.get("per_key", [])
    ok &= g("P4:per-key-len", len(pk) == N_KEYS, len(pk))
    for i, row in enumerate(pk):
        pos = i + 1
        kidx = "k%02d" % pos
        ok &= g("P4:%s:pos" % kidx, row.get("pos") == pos, row.get("pos"))
        ok &= g("P4:%s:key==selection" % kidx, row.get("key") == epo[i]["key"], "")
        s12 = row.get("stage1_2m_pair", {})
        ok &= g("P4:%s:ledger-2m==raw" % kidx, kidx in pairs and s12.get("result") == 0
                and s12.get("nodes") == 2000000 and s12.get("pair") == "identical", "")
        if pos == 1:
            s215 = row.get("stage2_15m_pair", {})
            ok &= g("P4:k01:ledger-15m==raw", s215.get("result") == 1 and s215.get("nodes") == WIN_NODES
                    and s215.get("pair") == "identical", "")
            res = row.get("resolved", {})
            ok &= g("P4:k01:ledger-resolved-win", res.get("stage") == "15m" and res.get("result") == 1
                    and res.get("nodes") == WIN_NODES, "")
        else:
            ok &= g("P4:%s:ledger-suppressed" % kidx, row.get("stage2_15m") == "suppressed_by_win_stopping_rule",
                    row.get("stage2_15m"))
            ok &= g("P4:%s:no-15m-raw" % kidx, not (raw / ("at15m-run1/%s.out.csv" % kidx)).exists()
                    and not (raw / ("at15m-run2/%s.out.csv" % kidx)).exists(), "")

    # P5: WIN stop anchor + overreach disclosure
    anchor = bs.get("win_stopping_rule_anchor", "")
    ok &= g("P5:win-anchor-text", isinstance(anchor, str) and "k01" in anchor and "8514427" in anchor
            and "WIN(1)" in anchor, anchor[:80])
    ov = bs.get("overreach_disclosure", {})
    obs = ov.get("observed_values_not_official", {}).get("stage2_15m_pair", {})
    ok &= g("P5:overreach-present", isinstance(ov.get("event"), str) and "k02" in ov["event"], "")
    ok &= g("P5:overreach-values", obs.get("result") == 0 and obs.get("nodes") == 15000000
            and obs.get("pair") == "identical", "%s" % obs)
    ok &= g("P5:overreach-not-official", "NOT an official" in ov.get("event", "") and "not published" in ov.get("event", ""), "")
    k02_15m_exists = any("/at15m-" in r[2] and "/k02.out.csv" in r[2] for r in man)
    ok &= g("P5:k02-15m-raw-absent-from-manifest", not k02_15m_exists, "")
    # every raw file not part of the 88 is absent from the tree (already P1) and no 50M stage exists
    ok &= g("P5:no-50m-stage", not any("at50m" in r[2] for r in man) and not any(p.name.startswith("at50m") for p in raw.rglob("*")),
            "")
    ok &= g("P5:no-post-win-15m-starts", sorted(r[2].split("/")[-1] for r in at15m) == ["k01.out.csv", "k01.out.csv"], "")

    # P6: guards
    ok &= g("P6:status-guard", isinstance(bs.get("status_guard"), (str, dict)) and "UNKNOWN" in json.dumps(bs.get("status_guard")), "")
    ok &= g("P6:single-implementation-note", isinstance(bs.get("single_implementation_note"), str), "")
    nb = bs.get("nodes_bookkeeping", {})
    ok &= g("P6:nodes-bookkeeping", nb.get("stage1_2m_nodes_sum_all_43_keys_two_passes") == 172000000
            and nb.get("win_15m_nodes_each_pass") == WIN_NODES, "")

    out = {
        "schema": "n11-eighthcost-ladder-preaudit-v1",
        "kit": "research/experiments/n11-eighthcost-class-s5-exclusive-probe-1297036692750860288-20261127",
        "selection_sha256": SEL_SHA, "batch_summary_sha256": BS_SHA, "head_sha256": HEAD_SHA,
        "raws": len(man), "keys": N_KEYS,
        "resolved": {"win": 1, "loss": 0, "parked": 0, "suppressed": N_KEYS - 1},
        "overreach_disclosed": True,
        "temporal_anchor_disclosure": ("batch-summary ledger git-published in the SAME commit as the raws "
                                       "(0005e5b1): content-level WIN-stop invariant checked (15M raws only "
                                       "for the WIN key; k02 post-anchor 15M pair only in overreach_disclosure); "
                                       "no git-preceding ledger anchor exists for this batch"),
        "gates": gates, "overall": "PASS" if ok else "FAIL",
    }
    print(json.dumps({"overall": out["overall"], "gates": len(gates)}, ))
    fails = [k for k, v in sorted(gates.items()) if v["status"] == "FAIL"]
    for k in fails:
        print("FAIL", k, gates[k]["detail"][:120])
    if out_path is not None and ok:
        out_path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    elif out_path is not None:
        # fail-closed: never overwrite a PASS with a FAIL silently
        out_path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
