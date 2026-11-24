#!/usr/bin/env python3
"""Part CT audit: verify the batch-28 last-remaining-EXHAUSTED-1-row (aa050)
30M reprobe publication kit.

Gates (fail-closed; any violation -> GATE FAILED + rc=1, no audit.json written):
  A. registry: input/reprobe-keys.json parses, budget == 30000000, key id set ==
     the pinned remaining-EXHAUSTED id set (aa050), anchors == aa036/aa004.
  B. per key with a complete pair: replay_done in both pass files; p1/p2 rows
     identical except wall_s (field 8); budget field == 30000000; key lo/hi ==
     registry; legal == registry; result in {0,1,2}; result 0 -> nodes ==
     30000000; result 1/2 -> nodes <= 30000000; forbidden-quadruples header ==
     95670 in both pass files; status.log corroboration (PASS line with
     "30000000,<result>,<nodes>" for completable rows; WIN rows additionally
     require the WIN-HALT line; exhausted rows additionally require the
     EXHAUSTED line - the pinned runner writes both PASS and EXHAUSTED lines).
     Registry published prior-condition facts (15M, CQ 20M, CS 25M) must all be
     exhaustion rows (result 0 at their own budgets).
  C. anchors (aa036/aa004): complete pairs under the derived 30M runner,
     replay_done, budget field == 30000000, and node-exact match vs the pinned
     published 20M baselines (result and nodes unchanged: the deterministic
     search resolves before the budget; only wall and budget-flag fields may
     differ). aa004 WIN rows also require the PASS + WIN-HALT status pair.
  D. val-gate fresh: 4 sanctioned keys, `.ct-host.out` present with
     replay_done, node-exact vs published baselines (all fields except
     wall_s; the sanctioned budgets 2000000/15000000 are re-run as pinned).
  E. rules gate: every out file in output/raw plus val-gate/*.ct-host.out
     carries `# forbidden quadruples: 95670`.
  F. bookkeeping: keys with neither a complete pair nor window-exceeded
     cause list as `unprobed`; keys skipped by the pre-registered >=2
     truncated-retry window rule list as `window_exceeded` (honest
     unresolved, NOT a gate failure).

Interpretation guard: node counts are bookkeeping, never verdicts. WIN/LOSS
rows are honest labels only (verdict not consumed); adoption stays with a
separate declared adoption Part through the pinned fail-closed merger, WIN
rows further gated by the scrutiny owner's C++ second implementation. The
standard 11x11 empty board, class 5343 and every key stay UNKNOWN here.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
EXP = HERE.parents[1]
SCHEMA = "n11-centralreply-c5343-b28aa050-reprobe30m-audit-v1"
PIN_IDS = ["aa050"]
PIN_ANCHORS = {"aa036": {"result": 2, "nodes": 955659},
               "aa004": {"result": 1, "nodes": 15616012}}
VAL_KEYS = [("at2m-s5-1152921504606851072-536870946", 2000000, 0, 2000000),
            ("at2m-s5-1188950301626860544-536870912", 2000000, 0, 2000000),
            ("first-15m-s5-1152921504606851072-536870946", 15000000, 2, 3651923),
            ("second-15m-s5-1188950301626860544-536870912", 15000000, 2, 5040200)]
BUDGET = 30000000


def fail(msg):
    print("GATE FAILED: " + msg)
    raise SystemExit(1)


def sha(p):
    d = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for b in iter(lambda: fh.read(1024 * 1024), b""):
            d.update(b)
    return d.hexdigest()


def parse_raw(path):
    txt = Path(path).read_text(encoding="utf-8")
    row, quads, done = None, None, False
    for ln in txt.splitlines():
        if ln.startswith("# replay_done"):
            done = True
        elif ln.startswith("replay,"):
            row = ln.split(",")
        elif ln.startswith("# forbidden quadruples:"):
            quads = int(ln.split(":")[1].strip())
    if not done:
        fail(f"{Path(path).name}: missing # replay_done (truncated fragment)")
    if row is None:
        fail(f"{Path(path).name}: missing replay row")
    return {"row": row, "quads": quads}


def pair(kid):
    p1p, p2p = EXP / f"output/raw/{kid}.p1.out", EXP / f"output/raw/{kid}.p2.out"
    if not (p1p.exists() and p2p.exists()):
        return None
    p1, p2 = parse_raw(p1p), parse_raw(p2p)
    r1, r2 = p1["row"], p2["row"]
    if r1[:8] + r1[9:] != r2[:8] + r2[9:]:
        fail(f"{kid}: p1/p2 row mismatch {r1} vs {r2}")
    return {"r": r1, "quads": (p1["quads"], p2["quads"])}


def main():
    regp = EXP / "input/reprobe-keys.json"
    reg = json.loads(regp.read_text(encoding="utf-8"))
    if reg.get("reprobe_condition", {}).get("budget") != BUDGET:
        fail(f"A registry budget != {BUDGET}")
    ids = [k["key_id"] for k in reg["keys"]]
    if sorted(ids) != sorted(PIN_IDS):
        fail("A registry key set != pinned EXHAUSTED set")
    rmap = {k["key_id"]: k for k in reg["keys"]}
    a_ids = sorted(a["key_id"] for a in reg["anchors"])
    if a_ids != sorted(PIN_ANCHORS):
        fail("A anchors != aa036/aa004")

    status = (EXP / "output/status.log").read_text(encoding="utf-8").splitlines()
    lines = {kid: [l for l in status if len(l.split()) > 1 and l.split()[1] == kid]
             for kid in ids + list(PIN_ANCHORS)}
    trunc = {}
    for l in status:
        parts = l.split()
        for i in range(1, len(parts)):
            if parts[i] in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY"):
                trunc[(parts[i-1], parts[i][:2])] = trunc.get((parts[i-1], parts[i][:2]), 0) + 1

    results = {}
    for kid in ids:
        pr = pair(kid)
        if pr is None:
            continue
        r = pr["r"]
        k = rmap[kid]
        if int(r[2]) != 5 or int(r[5]) != BUDGET:
            fail(f"{kid}: stones/budget mismatch {r}")
        if int(r[9]) != int(k["lo"]) or int(r[10]) != int(k["hi"]):
            fail(f"{kid}: raw key does not match registry row")
        if int(r[3]) != int(k["legal"]):
            fail(f"{kid}: raw legal mismatch vs registry")
        if int(r[6]) not in (0, 1, 2):
            fail(f"{kid}: invalid result {r[6]}")
        nodes = int(r[7])
        if int(r[6]) == 0 and nodes != BUDGET:
            fail(f"{kid}: exhausted without full budget nodes")
        if int(r[6]) != 0 and nodes > BUDGET:
            fail(f"{kid}: nodes exceed budget")
        if pr["quads"] != (95670, 95670):
            fail(f"{kid}: forbidden quadruples header mismatch")
        kl = lines[kid]
        has_pass = any(len(l.split()) > 3 and l.split()[2] == "PASS"
                       and l.split()[3] == f"{BUDGET},{r[6]},{nodes}" for l in kl)
        if not has_pass:
            fail(f"{kid}: no PASS field line in status.log")
        if int(r[6]) == 1 and not any("WIN-HALT" in l for l in kl):
            fail(f"{kid}: no WIN-HALT line in status.log")
        if int(r[6]) == 0 and not any("EXHAUSTED" in l for l in kl):
            fail(f"{kid}: no EXHAUSTED line in status.log")
        for pk, pb in (("published_15m", 15000000),
                       ("published_cq20m", 20000000),
                       ("published_cs25m", 25000000)):
            pf = k.get(pk, {})
            if int(pf.get("result", -1)) != 0 or int(pf.get("nodes", -1)) != pb:
                fail(f"{kid}: registry {pk} fact is not an exhaustion row at {pb}")
        results[kid] = {"result": int(r[6]), "nodes": nodes, "legal": int(r[3]),
                        "two_pass_exact": True, "truncated_retries":
                         max(trunc.get((kid, "P1"), 0), trunc.get((kid, "P2"), 0))}

    window_exceeded = [kid for kid in ids if kid not in results
                       and (trunc.get((kid, "P1"), 0) >= 2 or trunc.get((kid, "P2"), 0) >= 2)]
    unprobed = [kid for kid in ids if kid not in results and kid not in window_exceeded]

    anchors = {}
    for kid, exp in PIN_ANCHORS.items():
        pr = pair(kid)
        if pr is None:
            fail(f"anchor {kid}: pass pair missing")
        r = pr["r"]
        if int(r[5]) != BUDGET:
            fail(f"anchor {kid}: budget field != {BUDGET}")
        if int(r[6]) != exp["result"] or int(r[7]) != exp["nodes"]:
            fail(f"anchor {kid}: not node-exact vs published baseline: {r}")
        if pr["quads"] != (95670, 95670):
            fail(f"anchor {kid}: quads header mismatch")
        kl = lines[kid]
        nodes = int(r[7])
        has_pass = any(len(l.split()) > 3 and l.split()[2] == "PASS"
                       and l.split()[3] == f"{BUDGET},{r[6]},{nodes}" for l in kl)
        if not has_pass:
            fail(f"anchor {kid}: no PASS line in status.log")
        if exp["result"] == 1 and not any("WIN-HALT" in l for l in kl):
            fail(f"anchor {kid}: no WIN-HALT line in status.log")
        anchors[kid] = {"result": int(r[6]), "nodes": nodes, "node_exact_vs_published": True}

    val = {}
    for vk, vbudget, vresult, vnodes in VAL_KEYS:
        outp = EXP / f"val-gate/{vk}.ct-host.out"
        if not outp.exists():
            fail(f"val-gate {vk}: fresh output missing")
        pr = parse_raw(outp)
        r = pr["row"]
        base = parse_raw(EXP / f"val-gate/{vk}.published-baseline.out")["row"]
        if int(r[5]) != vbudget or int(r[6]) != vresult or int(r[7]) != vnodes:
            fail(f"val-gate {vk}: fresh row != pinned expectation: {r}")
        if r[:8] + r[9:] != base[:8] + base[9:]:
            fail(f"val-gate {vk}: not node-exact vs published baseline: {r} vs {base}")
        if int(base[7]) != vnodes:
            fail(f"val-gate {vk}: published baseline drift: {base}")
        val[vk] = {"result": int(r[6]), "nodes": int(r[7]), "node_exact": True}

    for f in sorted((EXP / "output/raw").glob("*.out")):
        txt = f.read_text(encoding="utf-8")
        if "# forbidden quadruples: 95670" not in txt:
            fail(f"rules gate: {f.name} missing quads header")

    resolved_win = sorted(k for k, v in results.items() if v["result"] == 1)
    resolved_loss = sorted(k for k, v in results.items() if v["result"] == 2)
    still_exhausted = sorted(k for k, v in results.items() if v["result"] == 0)
    audit = {
        "schema": SCHEMA,
        "class_index": 5343,
        "batch": 28,
        "reprobe_budget": BUDGET,
        "keys_total": len(ids),
        "probed": len(results),
        "resolved_win_rows": resolved_win,
        "resolved_loss_rows": resolved_loss,
        "loss_rows_are_adoption_candidates_only": True,
        "still_exhausted_rows": still_exhausted,
        "window_exceeded_rows": window_exceeded,
        "unprobed_rows": unprobed,
        "mismatches": 0,
        "anchors": anchors,
        "val_gate_fresh": val,
        "input_sha256": sha(regp),
        "note": ("all complete pairs two-pass node-exact at budget 30000000; resolved "
                 "rows are honest labels (verdict NOT consumed; adoption via a separate "
                 "declared adoption Part with the pinned fail-closed merger only; WIN "
                 "rows additionally gated by the scrutiny owner C++ second "
                 "implementation); still-exhausted rows are honest UNKNOWN at the 30M "
                 "condition (no same-condition re-probe); window-exceeded rows are "
                 "honest unresolved-in-window; the standard 11x11 empty board and "
                 "every key stay UNKNOWN at this point"),
    }
    with (EXP / "output/audit.json").open("w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print(f"audit PASS: probed {len(results)}/{len(ids)}, win {len(resolved_win)}, "
          f"loss {len(resolved_loss)}, exhausted @30M {len(still_exhausted)}, "
          f"window-exceeded {len(window_exceeded)}, unprobed {len(unprobed)}, "
          f"anchors {len(anchors)}, val-gate {len(val)}")


if __name__ == "__main__":
    main()
