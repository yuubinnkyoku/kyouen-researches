#!/usr/bin/env python3
"""Pre-registered independent audit instrument for the twelfth-cost exclusive
S5 ladder (selection kit research/experiments/n11-twelfthcost-class-s5-exclusive-probe-20261127,
commit e588de1e; cross-checked independently at commit 5745ede1f).

Two stages:

  Stage S (selection-side) - RUNNABLE NOW, before the batch raws exist:
    - byte pins: selection json 1119d01b..., selector ea2b8331...,
      jsreplay 84585617..., kit README 74131df1..., head of record
      1e2eeda2... (6,890 rows WIN 208 / LOSS 6,682), wave-A declaration
      log 395cbeac...;
    - selection content: schema, class 10376293541461626880:16777216,
      51 exclusive keys, unique, first/last key pinned, bands
      5,041,585 x1 / 5,069,670 x 1 / 5,234,938 x 11 / 5,932,112 x 38,
      proxy_exclusive_sum_head 293,115,829 (recomputed from entries);
    - all 51 input CSVs: MANIFEST sha256 gate + order fidelity
      (CSV i target key == exclusive_probe_order[i-1]) + legal fidelity
      (CSV legal == entry legal) + stones == 5;
    - head census (6,890/208/6,682) + 51-key freshness (all absent).

  Stage B (batch-side) - PRE-REGISTERED, auto-runs when the batch raws
    are present under <selkit>/output/raw/ (wave B of declaration
    f6d29d16).  Until then the instrument reports stage_batch: "absent"
    and lists the pre-registered gates as PREREGISTERED (not FAIL).
    When raws appear it enforces, fail-closed:
      B1 every replay row targets one of the 51 selected keys;
      B2 stage-1: exactly two rows per key at budget 2,000,000 and the
         pair is node-identical (wall may differ);
      B3 result semantics: result==0 requires nodes==budget; result
         in {1,2} requires nodes<=budget (WIN=1 / exact LOSS=2);
      B4 escalation discipline: rows at budget 15,000,000 (or 50,000,000)
         exist only for keys whose stage-1 pair is UNKNOWN;
      B5 WIN-stop content rule: after the first escalating key that
         resolves result==1, no further escalated rows may exist unless
         the ledger marks them overreach (batch-summary json field
         overreach_disclosure, ninth/eighth precedent);
      B6 cold-pair determinism: every pair of rows with the same
         (key, budget) is node-identical.

This instrument asserts NOTHING about verdicts, class status, or the
11x11 game value. Nodes are bookkeeping. The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.

Fail-closed: any gate failure -> rc=1.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SEL_SHA = "1119d01bb2a4c0a02222414ae0506aa61a307334b263e619fdfed9b3eddc0878"
SEL_SCHEMA = "n11-twelfthcost-exclusive-selection-v1"
CLASS = "10376293541461626880:16777216"
HEAD_SHA = "1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17"
HEAD_ROWS, HEAD_WIN, HEAD_LOSS = 6890, 208, 6682
N_KEYS = 51
FIRST_KEY = "1152921504607895556:603979776"
LAST_KEY = "14987979559889014784:16777216"
BANDS = {5041585: 1, 5069670: 1, 5234938: 11, 5932112: 38}
PROXY_SUM = 293115829
UNK_BEFORE, UNK_EXCL, UNK_SHARED = 100, 51, 49
SELECTOR_SHA = "ea2b8331db3ba9be99b2880230c7a2f70c9576ddbbff6fd16e6e7686feb81024"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
README_SHA = "74131df13a62ad3b17ac55997a91731fcea91ea6327aa03e5fa66fa79a5cd948"
DECL_SHA = "395cbeac81a709938b5303a83d8f4426c1bf9f8f39ed7422f168c1b5c6632385"
CSV_PREFIX = "input/"
CSV_SUFFIX = ".input.csv"
REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    kit = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    head = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    decl = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    out_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None
    gates = {}

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
        return bool(ok)

    ok = True

    # ---------- Stage S: selection-side ----------
    sel_path = kit / "output" / "twelfth-cost-exclusive-keys.json"
    ok &= g("S0:selection-sha", sel_path.exists() and sha256(sel_path) == SEL_SHA,
            sha256(sel_path) if sel_path.exists() else "missing")
    sel = json.loads(sel_path.read_text())
    ok &= g("S0:selection-schema", sel.get("schema") == SEL_SCHEMA, sel.get("schema"))
    ok &= g("S0:selection-class", sel.get("class") == CLASS, sel.get("class"))
    hb = sel.get("head_basis", {})
    ok &= g("S0:selection-head-basis",
            hb.get("sha256") == HEAD_SHA and hb.get("rows") == HEAD_ROWS
            and hb.get("win") == HEAD_WIN and hb.get("loss") == HEAD_LOSS, "")
    ok &= g("S0:selection-unknown-counters",
            sel.get("s5_unknown_before_head") == UNK_BEFORE
            and sel.get("unknown_exclusive_head") == UNK_EXCL
            and sel.get("unknown_shared_head") == UNK_SHARED, "")
    epo = sel.get("exclusive_probe_order", [])
    ok &= g("S0:selection-order-len", len(epo) == N_KEYS, len(epo))
    keys = [e.get("key") for e in epo]
    ok &= g("S0:selection-order-unique", len(set(keys)) == N_KEYS, "")
    ok &= g("S0:selection-first-key", keys and keys[0] == FIRST_KEY, keys[0] if keys else "")
    ok &= g("S0:selection-last-key", keys and keys[-1] == LAST_KEY, keys[-1] if keys else "")
    bands = sel.get("bands_proxy_to_count", {})
    ok &= g("S0:selection-bands",
            {int(k): v for k, v in bands.items()} == BANDS, json.dumps(bands, sort_keys=True))
    psum = sum(int(e.get("proxy", 0)) for e in epo)
    ok &= g("S0:selection-proxy-sum-recomputed", psum == sel.get("proxy_exclusive_sum_head") == PROXY_SUM,
            f"{psum} vs {sel.get('proxy_exclusive_sum_head')}")
    ok &= g("S0:selection-status-guard", sel.get("status_guard") is not None and sel.get("gates_passed") is not None, "")

    ok &= g("S0:selector-sha", sha256(kit / "scripts" / "select_twelfth_exclusive.py") == SELECTOR_SHA, "")
    ok &= g("S0:jsreplay-sha", sha256(kit / "scripts" / "jsreplay.js") == JSREPLAY_SHA, "")
    ok &= g("S0:kit-readme-sha", sha256(kit / "README.md") == README_SHA, "")

    if decl is not None:
        ok &= g("S0:declaration-sha", sha256(decl) == DECL_SHA, sha256(decl))
        dt = " ".join(decl.read_text().split())
        ok &= g("S0:declaration-class", CLASS in dt, "")
        ok &= g("S0:declaration-head-pin", "1e2eeda2" in dt, "")
        ok &= g("S0:declaration-win-stop-rule",
                 "WIN stopping rule" in dt or "WIN-stopping rule" in dt, "")
        ok &= g("S0:declaration-single-owner", "single-owner declaration" in dt, "")

    # manifest + input CSVs
    man = {}
    for line in (kit / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip():
            continue
        sha, _, name = line.partition(" ")
        name = name.strip()
        man[name] = sha
    ok &= g("S1:manifest-len", len(man) == 55, len(man))
    bad = [n for n, s in man.items() if not (kit / n).exists() or sha256(kit / n) != s]
    ok &= g("S1:manifest-all-sha", not bad, str(bad))
    csv_ok, csv_detail = True, []
    for i in range(1, N_KEYS + 1):
        name = f"{CSV_PREFIX}k{i:02d}{CSV_SUFFIX}"
        if name not in man:
            csv_ok = False
            csv_detail.append(f"{name}:not-in-manifest")
            continue
        f = (kit / name).read_text().strip().split(",")
        entry = epo[i - 1]
        lohi = entry.get("key", "")
        lo, _, hi = lohi.partition(":")
        if (len(f) >= 11 and f[0] == "target" and f[2] == "5"
                and f[3] == lo and f[4] == hi and f[5] == str(entry.get("legal"))):
            continue
        csv_ok = False
        csv_detail.append(f"{name}:mismatch({','.join(f[:6])} vs {lohi}/{entry.get('legal')})")
    ok &= g("S1:csv-order-legal-fidelity-51", csv_ok, "; ".join(csv_detail[:4]))

    # head census + freshness
    if head is not None:
        ok &= g("S2:head-sha", sha256(head) == HEAD_SHA, sha256(head))
        rows, win, loss, seen, dup = 0, 0, 0, set(), 0
        first = head.read_text().splitlines()
        ok &= g("S2:head-first-line-comment", bool(first) and first[0].startswith("#"), "")
        for line in first:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            f = line.split(",")
            if len(f) != 6 or f[0] != "s5verdict":
                ok = False
                continue
            rows += 1
            k = (f[1], f[2])
            if k in seen:
                dup += 1
            seen.add(k)
            if f[4] == "1":
                win += 1
            elif f[4] == "2":
                loss += 1
        ok &= g("S2:head-census", rows == HEAD_ROWS and win == HEAD_WIN and loss == HEAD_LOSS,
                f"{rows}/{win}/{loss}")
        ok &= g("S2:head-no-duplicate-keys", dup == 0, dup)
        absent = sum(1 for e in epo if (e["key"].split(":")[0], e["key"].split(":")[1]) not in seen)
        ok &= g("S2:head-freshness-51-absent", absent == N_KEYS, absent)

    # ---------- Stage B: batch-side (pre-registered) ----------
    raw_dir = kit / "output" / "raw"
    stage = {}
    if not raw_dir.exists() or not any(raw_dir.iterdir()):
        stage["status"] = "absent"
        stage["note"] = ("wave B raws of declaration f6d29d16 are not yet published; "
                         "the B-gates below are PRE-REGISTERED here before the raws exist "
                         "and activate on the next run once <kit>/output/raw/ is populated")
        for name in ("B1:raw-keys-subset-of-51", "B2:stage1-two-rows-per-key-2M",
                     "B3:result-semantics", "B4:escalation-only-for-unknown",
                     "B5:win-stop-content-rule", "B6:cold-pair-node-identity"):
            gates[name] = {"status": "PREREGISTERED", "detail": "batch raws absent"}
    else:
        rows = []
        for p in sorted(raw_dir.rglob("*")):
            if not p.is_file():
                continue
            for line in p.read_text().splitlines():
                m = REPLAY.match(line.strip())
                if m:
                    rows.append({
                        "file": str(p.relative_to(kit)), "stones": int(m.group(2)),
                        "legal": int(m.group(3)), "budget": int(m.group(5)),
                        "result": int(m.group(6)), "nodes": int(m.group(7)),
                        "lo": m.group(9), "hi": m.group(10)})
        keyset = set(keys)
        ok &= g("B1:raw-keys-subset-of-51",
                all(f"{r['lo']}:{r['hi']}" in keyset for r in rows), "")
        per = {}
        for r in rows:
            per.setdefault((r["lo"], r["hi"]), []).append(r)
        ok &= g("B2:stage1-two-rows-per-key-2M",
                all(len([r for r in v if r["budget"] == 2_000_000]) == 2 for v in per.values())
                and len(per) <= N_KEYS, f"{len(per)} keys")
        ok &= g("B3:result-semantics",
                all((r["result"] == 0 and r["nodes"] == r["budget"])
                    or (r["result"] in (1, 2) and r["nodes"] <= r["budget"]) for r in rows), "")
        esc_ok = True
        for k, v in per.items():
            s1 = [r for r in v if r["budget"] == 2_000_000]
            if not s1 or any(r["result"] == 0 for r in s1):
                continue
            if any(r["budget"] != 2_000_000 for r in v):
                esc_ok = False
        ok &= g("B4:escalation-only-for-unknown", esc_ok, "")
        order = {(k.split(":")[0], k.split(":")[1]): i for i, k in enumerate(keys)}
        esc_keys = [k for k, v in per.items() if any(r["budget"] != 2_000_000 for r in v)]
        esc_keys.sort(key=lambda k: order[k])
        win_pos = None
        for k in esc_keys:
            if any(r["result"] == 1 for r in per[k] if r["budget"] != 2_000_000):
                win_pos = order[k]
                break
        ok &= g("B5:win-stop-content-rule",
                win_pos is None or all(order[k] <= win_pos for k in esc_keys),
                f"win at {win_pos}, escalated {len(esc_keys)}")
        det = True
        for k, v in per.items():
            byb = {}
            for r in v:
                byb.setdefault(r["budget"], []).append(r["nodes"])
            for b, ns in byb.items():
                if len(set(ns)) != 1:
                    det = False
        ok &= g("B6:cold-pair-node-identity", det, "")
        stage["status"] = "present"
        stage["raw_rows"] = len(rows)

    out = {
        "schema": "n11-twelfthcost-ladder-preaudit-v1",
        "instrument": "audit_twelfth_ladder.py (pre-registered before wave-B raws)",
        "selection_kit": "research/experiments/n11-twelfthcost-class-s5-exclusive-probe-20261127",
        "stage_selection": "complete",
        "stage_batch": stage,
        "gates": gates,
        "overall": "PASS" if ok else "FAIL",
        "meaning": ("audit bookkeeping only; no verdict is claimed or consumed; the standard "
                    "11x11 empty board, all 19 central-reply roots, the two-stone root "
                    "{60,27} and third moves 100/108 remain UNKNOWN; nodes are bookkeeping"),
    }
    js = json.dumps(out, sort_keys=True, indent=1) + "\n"
    if out_path is not None:
        out_path.write_text(js)
    sys.stdout.write(js)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
