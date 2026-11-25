#!/usr/bin/env python3
"""resolve7: residual 72-row post-fold witness recheck (published records only).

Single-owner experiment declared in research/log/2026-11-20-n11-resolve7-single-owner-note.md.
Inputs are the five published record files, pinned by SHA-256:

  resolve6  : n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json
  fold9     : n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json
  fold10    : n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json
  sweep39   : n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json
  sv17      : n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json

This script does NOT rebuild the candidate universe (resolve6.py full re-run) and does not
judge any root. It re-derives, from the published records alone, (a) that the residual 72 rows
are exactly the 78-row one-cover witness plan minus the 6 rows closed by fold9/fold10,
(b) the post-retire assignment table of the 38 remaining witness roots, and (c) that under the
K1069 depth-10 sweep every assigned root of every residual row is REFUTED-D10, so this plan
supplies zero further depth-10 witnesses for the residual 72 rows.

Interpretation guard is invariant: REFUTED-D10 is not a LOSS proof; folds and coverage are
bookkeeping; the standard 11x11 empty board and the two-stone roots remain UNKNOWN.
"""
import hashlib
import json
import os
import sys

PINS = {
    "resolve6.json": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a",
    "fold9.json": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    "fold10.json": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    "sweep39.json": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "sv17.json": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
}

RETIRED_ROOT = "00004000000000821082000000000100"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pinned(input_dir):
    gates = []
    rec = {}
    for name in sorted(PINS):
        p = os.path.join(input_dir, name)
        got = sha256_file(p)
        ok = got == PINS[name]
        gates.append({"name": "pin-" + name, "pass": ok, "detail": got})
        if not ok:
            raise SystemExit("pin mismatch for " + name)
        with open(p) as f:
            rec[name] = json.load(f)
    return rec, gates


def main():
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "input"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output/residual72-postfold-witness-recheck-20261120.json"
    rec, gates = load_pinned(input_dir)

    r6 = rec["resolve6.json"]
    f9 = rec["fold9.json"]
    f10 = rec["fold10.json"]
    sw = rec["sweep39.json"]
    sv = rec["sv17.json"]

    rows78 = r6["base_state"]["residual_row_hex"]
    wf = r6["witness_full"]
    closed9 = [r["row_hex"] for r in f9["new_receipt_coverage"]["rows"]]
    cov10 = f10["new_receipt_coverage"]["rows"]
    closed10_all = [r["row_hex"] for r in cov10]
    set78_pre = set(rows78)
    # target rows are the closed rows inside the five-parent residual 78-row plan;
    # the extra row is the closed row outside that plan (fold10 closes 2 + 1).
    closed10_target = [h for h in closed10_all if h in set78_pre]
    closed10_extra = [h for h in closed10_all if h not in set78_pre]
    residual72 = f10["five_parent_target_after"]["residual_row_hex_after"]
    retired_root = f10["witness_plan_impact"]["retired_witness_root"]
    cls = sw["classification"]

    def gate(name, ok, detail=""):
        gates.append({"name": name, "pass": bool(ok), "detail": detail})
        return bool(ok)

    # --- structural gates on the published records -------------------------
    set78 = set(rows78)
    gate("rows78-unique", len(rows78) == len(set78), str(len(rows78)))
    union = set()
    dup_in_plan = []
    for w in wf:
        for c in w["covered"]:
            if c in union:
                dup_in_plan.append(c)
            union.add(c)
    gate("witness-39-roots", len(wf) == 39, str(len(wf)))
    gate("witness-one-cover-no-dup", not dup_in_plan, "dups=" + str(dup_in_plan))
    gate("witness-union-eq-rows78", union == set78,
         "union=%d rows78=%d" % (len(union), len(set78)))
    gate("fold9-closes-4-in-78", set(closed9) <= set78 and len(closed9) == 4,
         "closed9=%d in78=%s" % (len(closed9), set(closed9) <= set78))
    gate("fold10-closes-3-rows", len(closed10_all) == 3, str(len(closed10_all)))
    gate("fold10-target-closes-2-in-78", set(closed10_target) <= set78 and len(closed10_target) == 2,
         "closed=" + ",".join(sorted(set(closed10_target))))
    gate("closed6-disjoint", not (set(closed9) & set(closed10_target)), "")
    gate("sv17-claim-eq-fold10-target",
         sorted(sv["coverage_claim_pending_fold"]["covered_rows_per_resolve6_matching"]) == sorted(closed10_target),
         "")
    gate("retired-root-eq-seventeenth", retired_root == RETIRED_ROOT, retired_root)
    gate("rows78-minus-closed6-eq-residual72",
         set78 - set(closed9) - set(closed10_target) == set(residual72) and len(residual72) == 72,
         "|78-4-2|=%d residual=%d" % (len(set78 - set(closed9) - set(closed10_target)), len(residual72)))
    gate("extra-row-outside-78",
         set(closed10_extra).isdisjoint(set78) and len(closed10_extra) == 1,
         ",".join(closed10_extra))
    gate("k1069-classification-39-roots", len(cls) == 39, str(len(cls)))
    gate("k1069-roots-eq-witness-roots",
         set(cls.keys()) == set(w["root"] for w in wf), "")
    win_roots = [r for r, v in cls.items() if v == "WIN7-D10" or v == "WIN"]
    gate("k1069-single-win-root", len(win_roots) == 1 and win_roots[0] == RETIRED_ROOT,
         str(win_roots))
    gate("k1069-summary-win1-refuted38",
         sw["summary"]["win"] == 1 and sw["summary"]["refuted"] == 38 and sw["summary"]["capped"] == 0,
         json.dumps({k: sw["summary"][k] for k in ("win", "refuted", "capped", "order_conflicts")}, sort_keys=True))

    # --- post-retire assignment table --------------------------------------
    closed_all6 = set(closed9) | set(closed10_target)
    live_assign = {}
    assign_rows = {}
    for w in wf:
        root = w["root"]
        if root == RETIRED_ROOT:
            continue
        keep = [c for c in w["covered"] if c not in closed_all6]
        live_assign[root] = keep
        for c in keep:
            assign_rows.setdefault(c, []).append(root)
    two_row_roots = sorted(r for r, v in live_assign.items() if len(v) == 2)
    one_row_roots = sorted(r for r, v in live_assign.items() if len(v) == 1)
    zero_row_roots = sorted(r for r, v in live_assign.items() if len(v) == 0)
    assigned_rows = set(assign_rows.keys())
    gate("post-retire-38-roots", len(live_assign) == 38, str(len(live_assign)))
    gate("post-retire-34x2-plus-4x1",
         len(two_row_roots) == 34 and len(one_row_roots) == 4 and zero_row_roots == [],
         "2row=%d 1row=%d 0row=%d" % (len(two_row_roots), len(one_row_roots), len(zero_row_roots)))
    gate("post-retire-assignment-covers-residual72-exactly",
         assigned_rows == set(residual72) and sum(len(v) for v in live_assign.values()) == 72,
         "assigned=%d residual=%d edges=%d" % (len(assigned_rows), len(residual72),
                                              sum(len(v) for v in live_assign.values())))
    # one-cover property is preserved: every residual row has exactly one live assigned root
    multi = sorted(r for r, roots in assign_rows.items() if len(roots) > 1)
    gate("post-retire-one-cover-per-row", not multi, "multi=" + str(multi))

    # which witness roots provided the four fold9-closed rows (their remaining coverage)
    lost9 = sorted(r for r, v in live_assign.items() if set(w_c := wfor(wf, r)["covered"]) & set(closed9))
    row9_owner = {}
    for w in wf:
        for c in w["covered"]:
            if c in set(closed9):
                row9_owner[c] = w["root"]

    # verdicts of live assigned roots under the K1069 sweep
    refuted_live = sorted(r for r in live_assign if cls.get(r) == "REFUTED-D10")
    other_live = sorted(r for r in live_assign if cls.get(r) != "REFUTED-D10")
    gate("live-38-all-refuted-d10", len(refuted_live) == 38 and other_live == [],
         "refuted=%d other=%s" % (len(refuted_live), other_live))
    dead_rows = sorted(r for r, roots in assign_rows.items()
                       if all(cls.get(x) == "REFUTED-D10" for x in roots))
    gate("residual72-all-rows-assigned-to-dead10-only", len(dead_rows) == 72,
         "dead_rows=%d" % len(dead_rows))

    result = {
        "date": "2026-11-20",
        "schema": "resolve7-postfold-witness-recheck/1",
        "status": "published-records-only recheck; no universe rebuild, no new judging",
        "single_owner_note": "research/log/2026-11-20-n11-resolve7-single-owner-note.md",
        "input_pins": PINS,
        "retired_witness_root": RETIRED_ROOT,
        "gates": gates,
        "gates_total": len(gates),
        "gates_all_pass": all(g["pass"] for g in gates),
        "recheck": {
            "residual_78_plan": {
                "rows": rows78,
                "witness_roots": [w["root"] for w in wf],
                "one_cover": "39 roots x 2 rows = 78 rows, each row covered exactly once",
                "closed_by_fold9": closed9,
                "closed_by_fold10_target": closed10_target,
                "closed_by_fold10_extra_outside_plan": closed10_extra,
            },
            "residual_72_after": {
                "rows": residual72,
                "exactly_plan_minus_closed6": True,
            },
            "post_retire_assignment": {
                "live_roots": len(live_assign),
                "two_row_roots": two_row_roots,
                "one_row_roots": one_row_roots,
                "fold9_row_owners_lost": row9_owner,
                "one_cover_preserved": True,
                "rows_per_root": {r: v for r, v in sorted(live_assign.items())},
            },
            "k1069_cross": {
                "win_root": win_roots[0] if len(win_roots) == 1 else None,
                "live_refuted_roots": len(refuted_live),
                "residual_rows_with_only_refuted_d10_assignment": len(dead_rows),
                "depth10_witness_supply_from_39root_plan_for_residual72": 0,
                "note": ("Under the K1069 depth-10 sweep every one of the 38 live assigned roots is "
                         "REFUTED-D10, so the 39-root plan supplies zero further depth-10 witnesses "
                         "for the residual 72 rows. Closing them needs fresh candidates from the "
                         "resolve6 universe rebuild, add-two-stones expansion, depth>10 search, or "
                         "other certificate sources. REFUTED-D10 is not a LOSS proof."),
            },
        },
        "interpretation_guard": [
            "REFUTED-D10 is NOT a LOSS proof; it certifies no first-player win within depth 10 from that root only.",
            "Folds and coverage are row bookkeeping and say nothing about the game-theoretic value of any row.",
            "The residual 72 rows are a conditional depth-10 sweep/accounting state, not certificates.",
            "This recheck judges no root and closes no row.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("gates", result["gates_total"], "all_pass", result["gates_all_pass"])


def wfor(wf, root):
    for w in wf:
        if w["root"] == root:
            return w
    raise KeyError(root)


if __name__ == "__main__":
    main()
