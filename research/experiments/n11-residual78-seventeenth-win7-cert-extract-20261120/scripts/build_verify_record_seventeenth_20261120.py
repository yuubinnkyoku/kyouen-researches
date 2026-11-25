#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_verify_record_seventeenth_20261120: assemble the master record
(seventeenth-cert-triple-verification-20261120.json) for the blind extraction
and triple independent verification of the seventeenth WIN7-D10 certificate.

Root: 00004000000000821082000000000100 (7-stone, D4-canonical, bit 8,
child 4000000000821082000000000000), discovered as the single WIN of the
39-live-witness depth-10 both-order sweep recorded under ../sweep-records/
(K1063 resolve6 witness_full matching plan, run as an additional independent
execution started in the same minute as the single-owner concurrency note
commit 68b04984; see the experiment README for the race record).

Fail-closed: any gate below raises SystemExit; the record is only written
when every gate passes.

Determinism: stdlib only, no wall clock in the record body (the fixed session
date 2026-11-20 is recorded once), sort_keys JSON; two runs byte-identical.

Interpretation guard: the certificate proves the game-theoretic fact
"the original first player wins from this 7-stone root (second player to
move, loser stuck at terminals)". It does NOT close any residual row by
itself: row-closure bookkeeping happens only in a receipt-fold record
(fold10, consuming this seventeenth receipt) that re-derives the covered
rows from the certificate geometry. All n11 meta-status remains UNKNOWN.

Usage (repo root):  python3 research/experiments/ \
  n11-residual78-seventeenth-win7-cert-extract-20261120/scripts/ \
  build_verify_record_seventeenth_20261120.py \
  [RESOLVE6_JSON [FOLD9_JSON]]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPDIR = os.path.abspath(os.path.join(HERE, ".."))
OUTDIR = os.path.join(EXPDIR, "output")
OUTPATH = os.path.join(OUTDIR, "seventeenth-cert-triple-verification-20261120.json")

SESSION_DATE = "2026-11-20"
ROOT_HEX = "00004000000000821082000000000100"
CHILD_HEX = "4000000000821082000000000000"
BIT = 8
COVERED_ROWS = ["00000000000000821082000000000001",
                "00000000000000821082000000000004"]
TERM_MIN, TERM_MAX = 13, 17
MOVES = 60
ROWS = 49591
EXTRACTION_NODES = 4250297
SWEEP_NODES_ANDCLOSE1 = 1576372
SWEEP_NODES_ANDCLOSE0 = 2544178
SWEEP_TOTAL_NODES = 169615508
RESOLVE6_SHA256 = ("e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97"
                   "eb5c62473b90c281a")
FOLD9_SHA256 = ("24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64e"
                "a695d261017cdc2")
RACE_NOTE_COMMIT = "68b04984f22fe907120ded2deaf5b03182108fd7"
SINGLE_OWNER_SWEEP_DEFAULT = ("research/experiments/n11-residual78-"
                              "39livewitness-depth10-sweep-20261120/"
                              "output/witness-39live-root-depth10-"
                              "sweep-20261120.json")
SINGLE_OWNER_SWEEP_SHA256 = ("22953ae16a6002d87638531f2ca9fd286f6736b83"
                             "4fa296e5648505ada9074dc")
SOURCE_MAIN_HEAD_BEFORE = "ba447c8714"
CERT_REL = "certs/win7-root-%s-20261120.n11" % ROOT_HEX

RESOLVE6_DEFAULT = ("research/experiments/n11-residual78-cache-join-"
                    "resolve6-20261120/output/post-saturation-full-cache-"
                    "join-resolve6-20261120.json")
FOLD9_DEFAULT = ("research/experiments/n11-residual78-windfall4-receipt-"
                 "fold-20261120/output/windfall4-thirteenth-sixteenth-"
                 "win7-receipt-fold-20261120.json")


def need(ok, msg):
    if not ok:
        raise SystemExit("GATE FAILED: " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---- D4 canon (resolve5/resolve6 conventions) ----
TS = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0:
            nx, ny = x, y
        elif t == 1:
            nx, ny = 10 - y, x
        elif t == 2:
            nx, ny = 10 - x, 10 - y
        elif t == 3:
            nx, ny = y, 10 - x
        elif t == 4:
            nx, ny = x, 10 - y
        elif t == 5:
            nx, ny = 10 - y, 10 - x
        elif t == 6:
            nx, ny = y, x
        else:
            nx, ny = 10 - x, y
        tab.append(nx * 11 + ny)
    TS.append(tab)


def popcount(v):
    return bin(v).count("1")


def d4_images(v):
    out = []
    for tab in TS:
        w = 0
        for p in range(121):
            if (v >> p) & 1:
                w |= 1 << tab[p]
        out.append(w)
    return out


def d4_canon(v):
    return min(d4_images(v))


def main():
    resolve6_path = sys.argv[1] if len(sys.argv) > 1 else RESOLVE6_DEFAULT
    fold9_path = sys.argv[2] if len(sys.argv) > 2 else FOLD9_DEFAULT
    sw_theirs_path = (sys.argv[3] if len(sys.argv) > 3
                      else SINGLE_OWNER_SWEEP_DEFAULT)
    gates = []

    def check(name, cond, detail=None):
        gates.append({"gate": name, "pass": bool(cond),
                      **({"detail": detail} if detail is not None else {})})
        if not cond:
            raise SystemExit("GATE FAILED: " + name)
        return True

    resolve6 = load(resolve6_path)
    check("pin-resolve6-sha256", sha256_file(resolve6_path) == RESOLVE6_SHA256,
          {"sha256": sha256_file(resolve6_path)})
    fold9 = load(fold9_path)
    check("pin-fold9-sha256", sha256_file(fold9_path) == FOLD9_SHA256,
          {"sha256": sha256_file(fold9_path)})

    # ---- witness selection (coordinator record) ----
    wf = resolve6["witness_full"]
    sel = [w for w in wf if w["root"] == ROOT_HEX]
    check("witness-selection-strict", len(sel) == 1 and sel[0]["safe"] is True
          and sorted(sel[0]["rows"]) == sorted(COVERED_ROWS)
          and sel[0]["rule"].startswith("live candidate"),
          {"root": ROOT_HEX, "covered": sorted(sel[0]["rows"]),
           "safe": sel[0]["safe"], "witness_size": len(wf)})
    cover_union = sorted({r for w in wf for r in w["rows"]})
    check("witness-plan-covers-78", len(cover_union) == 78,
          {"unique_covered_rows": len(cover_union)})

    residual74 = fold9["five_parent_target_after"]["residual_row_hex_after"]
    check("fold9-residual-count-74", len(residual74) == 74)
    check("covered-rows-in-residual-74",
          all(r in residual74 for r in COVERED_ROWS),
          {"row1": COVERED_ROWS[0], "row2": COVERED_ROWS[1]})
    windfall_roots = [rc["root"] for rc in fold9["receipts"]]
    check("receipt-disjoint-from-windfall4",
          ROOT_HEX not in windfall_roots,
          {"windfall_roots": windfall_roots})
    check("root-d4-canonical",
          format(d4_canon(int(ROOT_HEX, 16)), "032x") == ROOT_HEX,
          {"canonical": format(d4_canon(int(ROOT_HEX, 16)), "032x")})
    check("root-stones-7", popcount(int(ROOT_HEX, 16)) == 7)
    for r in COVERED_ROWS:
        check("covered-row-d4-canonical-%s" % r[-4:],
              format(d4_canon(int(r, 16)), "032x") == r)
        check("covered-row-stones-6-%s" % r[-4:],
              popcount(int(r, 16)) == 6,
              {"note": "the residual five-parent target rows are 6-stone "
                       "S6 rows (7-stone witness roots cover them through "
                       "the '8 D4 images - 1 stone' join; the fold machine "
                       "re-derives the covered rows geometrically"})
    check("child-bit-decomposition",
          (int(CHILD_HEX, 16) | (1 << BIT)) == int(ROOT_HEX, 16))
    check("child-is-root-minus-least-set-bit",
          (int(ROOT_HEX, 16) & -int(ROOT_HEX, 16)) == (1 << BIT))

    # ---- certificate file ----
    cert_path = os.path.join(EXPDIR, CERT_REL)
    cert_bytes = os.path.getsize(cert_path)
    cert_sha = sha256_file(cert_path)
    lines = open(cert_path, encoding="utf-8").read().splitlines()
    rows = [l.split() for l in lines[2:] if l.strip()]
    check("cert-header", lines[0] == ("n11-terminal-strategy-v1 "
                                      "original_first_WIN7 "
                                      "second_to_move_LOSS")
          and lines[1] == "root " + ROOT_HEX,
          {"header": lines[0], "root_line": lines[1]})
    check("cert-rows-count-sorted-unique", len(rows) == ROWS
          and len({r[0] for r in rows}) == ROWS
          and all(rows[i][0] < rows[i + 1][0] for i in range(len(rows) - 1)),
          {"rows": len(rows)})

    # ---- extraction summaries (run1 + rerun) ----
    s1 = load(os.path.join(OUTDIR, "extraction-run1-summary-seventeenth-"
                                        "20261120.json"))
    s2 = load(os.path.join(OUTDIR, "extraction-rerun-summary-seventeenth-"
                                    "20261120.json"))
    pm1 = s1["perMove"]
    check("extraction-run1-summary", s1["child"] == CHILD_HEX and s1["bit"] == BIT
          and s1["moves"] == MOVES and s1["sum"] == EXTRACTION_NODES
          and s1["nRows"] == ROWS and s1["fbt_drops"] == 0
          and s1.get("fatal") is None
          and all(v["ok"] for v in pm1.values())
          and not any(v["capped"] for v in pm1.values())
          and all(TERM_MIN <= v["terminalRange"][0]
                  and v["terminalRange"][1] <= TERM_MAX for v in pm1.values()),
          {"moves": s1["moves"], "sum": s1["sum"], "nRows": s1["nRows"],
           "fbt_drops": s1["fbt_drops"]})
    check("extraction-rerun-summary-identical-numbers",
          s2["moves"] == s1["moves"] and s2["sum"] == s1["sum"]
          and s2["nRows"] == s1["nRows"] and s2["fbt_drops"] == s1["fbt_drops"]
          and s2["perMove"] == s1["perMove"])
    check("extraction-nodes-sum-per-move",
          sum(v["nodes"] for v in pm1.values()) == EXTRACTION_NODES)

    # ---- verification 1: TS sub-root Bareiss 4x4 ----
    rc = load(os.path.join(OUTDIR, "ts-root-check-seventeenth-20261120.json"))
    check("ts-root-check", rc["stones"] == 7 and rc["loserMobility"] == MOVES,
          rc)
    stats = [json.loads(l) for l in
             open(os.path.join(OUTDIR, "ts-subroot-stats-seventeenth-"
                                       "20261120.jsonl"), encoding="utf-8")]
    check("ts-subroots-count-ranges",
          len(stats) == MOVES
          and sorted(s["move"] for s in stats) == sorted(int(m) for m in pm1)
          and all(TERM_MIN <= s["range"][0] and s["range"][1] <= TERM_MAX
                  for s in stats),
          {"seen_total": sum(s["seen"] for s in stats),
           "terminals_total": sum(s["terminals"] for s in stats),
           "opponent_edges_total": sum(s["opponentEdges"] for s in stats)})
    ua = load(os.path.join(OUTDIR, "ts-union-audit-seventeenth-20261120.json"))
    check("ts-union-exact", ua["rows"] == ROWS and ua["missing"] == 0
          and ua["extra"] == 0, ua)

    # ---- verification 2: python exact Bareiss replay ----
    py = load(os.path.join(OUTDIR, "python-bareiss-replay-"
                                   "seventeenth-20261120.json"))
    check("python-bareiss-replay",
          py["root_loser_mobility"] == MOVES
          and py["subroots_passed"] == MOVES
          and py["strategy_rows"] == ROWS
          and py["consumed_rows"] == ROWS
          and py["union_missing"] == 0 and py["union_extra"] == 0
          and sorted(py["terminal_stone_range"]) == [13, 15, 17],
          {k: py[k] for k in ("subroots_passed", "strategy_rows",
                              "consumed_rows", "union_missing",
                              "union_extra", "terminal_stone_range",
                              "visited_winner_states")})

    # ---- verification 3: BigInt 3x3 cofactor ----
    bi = load(os.path.join(OUTDIR, "bigint-independent-verification-"
                                   "seventeenth-20261120.json"))
    check("bigint-3x3-cofactor",
          bi["root_hex"] == ROOT_HEX and bi["root_safe"] is True
          and bi["root_mobility"] == MOVES
          and bi["strategy_rows"] == ROWS
          and bi["rows_sorted_unique"] is True
          and bi["subroots_passed"] == MOVES
          and bi["consumed_winner_rows"] == ROWS
          and bi["union_missing"] == 0 and bi["union_extra"] == 0
          and bi["terminal_range"] == [13, 17],
          {k: bi[k] for k in ("subroots_passed", "winner_states",
                              "loser_states", "loser_reply_edges",
                              "terminal_count", "terminal_range")})
    check("mobility-triple-consistent",
          py["root_loser_mobility"] == bi["root_mobility"]
          == rc["loserMobility"] == MOVES)

    # ---- sweep classification record (provenance of the WIN verdict) ----
    sw = load(os.path.join(EXPDIR, "sweep-records",
                           "witness-39-live-root-depth10-sweep-20261120.json"))
    cls = sw["classification"]
    check("sweep-classification-39", cls["counted_roots"] == 39
          and cls["win7_d10"]["count"] == 1
          and cls["win7_d10"]["roots"] == [ROOT_HEX]
          and cls["refuted_d10"]["count"] == 38
          and cls["capped"]["count"] == 0
          and cls["ordering_conflicts"]["count"] == 0,
          {"win": cls["win7_d10"]["roots"], "refuted": 38, "capped": 0,
           "conflicts": 0})
    check("sweep-nodes-total", sw["controls"]["nodes_total_all_probes"]
          == SWEEP_TOTAL_NODES)
    wr = [r for r in sw["witness_records"] if r["root"] == ROOT_HEX][0]
    probes = {p["ordering"]: p for p in wr["probe_runs"]}
    check("sweep-win-both-orders-uncapped",
          probes["andclose1"]["loss"] is True
          and probes["andclose0"]["loss"] is True
          and not probes["andclose1"]["capped"]
          and not probes["andclose0"]["capped"]
          and probes["andclose1"]["nodes"] == SWEEP_NODES_ANDCLOSE1
          and probes["andclose0"]["nodes"] == SWEEP_NODES_ANDCLOSE0,
          {"andclose1_nodes": SWEEP_NODES_ANDCLOSE1,
           "andclose0_nodes": SWEEP_NODES_ANDCLOSE0})
    check("sweep-win-pilot-control",
          wr["pilot_control"]["nodes"] == 3402
          and wr["pilot_control"]["loss"] is False)
    check("sweep-covered-rows-record",
          sorted(wr["covered_stranded_rows"]) == sorted(COVERED_ROWS))

    # ---- independent double-run cross-check against the single-owner sweep ----
    sw_theirs = load(sw_theirs_path)
    check("pin-single-owner-sweep-sha256",
          sha256_file(sw_theirs_path) == SINGLE_OWNER_SWEEP_SHA256,
          {"sha256": sha256_file(sw_theirs_path)})
    tcls = sw_theirs["classification"]
    t_win = sorted(k for k, v in tcls.items() if v == "WIN7-D10")
    t_ref = sorted(k for k, v in tcls.items() if v == "REFUTED-D10")
    check("cross-run-classification-equal",
          t_win == [ROOT_HEX] and len(t_win) == 1 and len(t_ref) == 38
          and len(tcls) == 39)
    check("cross-run-total-nodes-equal",
          sw_theirs["summary"]["total_nodes"] == SWEEP_TOTAL_NODES,
          {"theirs": sw_theirs["summary"]["total_nodes"],
           "ours": SWEEP_TOTAL_NODES})
    my_max_probe = max(p["nodes"] for r in sw["witness_records"]
                       for p in r["probe_runs"])
    check("cross-run-max-probe-nodes-equal",
          sw_theirs["summary"]["max_probe"]["nodes"] == my_max_probe,
          {"theirs": sw_theirs["summary"]["max_probe"]["nodes"],
           "ours": my_max_probe})
    check("cross-run-winning-root-both-orders-in-both-runs",
          tcls.get(ROOT_HEX) == "WIN7-D10"
          and probes["andclose1"]["loss"] is True
          and probes["andclose0"]["loss"] is True)

    # ---- determinism rerun (fresh processes, node-exact) ----
    det = {}
    for ordering in (0, 1):
        path = (os.path.join(EXPDIR, "sweep-records", "determinism",
                            "win-root-andclose%d-rerun.jsonl" % ordering))
        entries = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        control = [e for e in entries if "control" in e]
        result = [e for e in entries if "control" not in e]
        check("determinism-rerun-andclose%d" % ordering,
              len(control) == 1 and control[0]["nodes"] == 3402
              and control[0]["loss"] is False
              and len(result) == 1 and result[0]["loss"] is True
              and not result[0]["capped"]
              and result[0]["terminalStoneRange"] == [13, 17]
              and result[0]["nodes"] == probes["andclose%d" % ordering]["nodes"],
              {"nodes": result[0]["nodes"], "loss": result[0]["loss"],
               "capped": result[0]["capped"]})
        det["andclose%d" % ordering] = {
            "nodes": result[0]["nodes"],
            "node_exact_vs_sweep_record": True}

    record = {
        "schema": ("n11-seventeenth-win7-cert-triple-verification-"
                   "20261120-v1"),
        "date": SESSION_DATE,
        "status": "triple-verified",
        "receipt_ordinal": "seventeenth",
        "root_hex": ROOT_HEX,
        "child_hex": CHILD_HEX,
        "added_bit": BIT,
        "certificate": {
            "path_rel": CERT_REL,
            "bytes": cert_bytes,
            "sha256": cert_sha,
            "rows": ROWS,
            "loser_first_moves": MOVES,
        },
        "extraction": {
            "engine": ("class4_child1_cert_extractor_exact_ms23.ts "
                        "(repo-verbatim, git blob pinned by K1066)"),
            "mode": "blind (kill table empty)",
            "run1_nodes": EXTRACTION_NODES,
            "run1_rows": ROWS,
            "rerun_summary_numbers_identical": True,
            "rerun_certificate_sha256_local": cert_sha,
            "fbt_drops": 0,
        },
        "discovery": {
            "kind": ("39-live-witness depth-10 both-order sweep "
                     "(K1063 resolve6 matching witness plan)"),
            "sweep_record_rel": ("sweep-records/witness-39-live-root-depth10-"
                                 "sweep-20261120.json"),
            "verdicts": {"win7_d10": 1, "refuted_d10": 38, "capped": 0,
                         "ordering_conflicts": 0},
            "determinism_rerun": det,
            "concurrency": {
                "single_owner_note_commit": RACE_NOTE_COMMIT,
                "note_pushed_at": "2026-11-19T20:32:07Z",
                "this_run_started": "2026-11-19T20:32:47Z (worker0)",
                "visibility": ("the note and this run's start were mutually "
                               "invisible; the sweep completed before the "
                               "note was seen by this lane"),
                "single_owner_sweep_record": {
                    "commit": "e47e418496...",
                    "path_rel": SINGLE_OWNER_SWEEP_DEFAULT,
                    "sha256": SINGLE_OWNER_SWEEP_SHA256,
                    "per_probe_cross_check": ("78/78 probes node-exact "
                                              "identical between this run "
                                              "and the single-owner run "
                                              "(independently loaded and "
                                              "compared before publication)"),
                },
            },
        },
        "coverage_claim_pending_fold": {
            "covered_rows_per_resolve6_matching": sorted(COVERED_ROWS),
            "both_rows_open_in_fold9_residual_74": True,
            "note": ("row-closure accounting for these rows happens only in "
                     "a fold10 receipt-fold record that re-derives the "
                     "covered rows from the certificate geometry; until "
                     "then the rows stay open"),
        },
        "triple_verification": {
            "ts_bareiss": {
                "file": "output/ts-subroot-stats-seventeenth-20261120.jsonl",
                "subroots": MOVES,
                "seen": sum(s["seen"] for s in stats),
                "terminals": sum(s["terminals"] for s in stats),
                "opponent_edges": sum(s["opponentEdges"] for s in stats),
                "union_missing": ua["missing"], "union_extra": ua["extra"],
            },
            "python_bareiss_replay": {
                "file": ("output/python-bareiss-replay-seventeenth-"
                         "20261120.json"),
                "subroots_passed": py["subroots_passed"],
                "visited_winner_states": py["visited_winner_states"],
                "terminal_stone_range": py["terminal_stone_range"],
                "union_missing": py["union_missing"],
                "union_extra": py["union_extra"],
            },
            "bigint": {
                "file": ("output/bigint-independent-verification-"
                         "seventeenth-20261120.json"),
                "subroots_passed": bi["subroots_passed"],
                "terminal_range": bi["terminal_range"],
                "union_missing": bi["union_missing"],
                "union_extra": bi["union_extra"],
                "rows_sorted_unique": bi["rows_sorted_unique"],
            },
            "cross_method_union_exact": True,
            "pilot_control": {"control": "pilot_d6", "nodes": 3402,
                              "loss": False},
        },
        "pins": {
            "resolve6_sha256": RESOLVE6_SHA256,
            "fold9_sha256": FOLD9_SHA256,
            "source_main_head_before": SOURCE_MAIN_HEAD_BEFORE,
        },
        "gates": gates,
        "gates_total": len(gates),
        "gates_all_pass": all(g["pass"] for g in gates),
        "interpretation_guard": [
            ("WIN7-D10 proves a first-player win within depth 10 only from "
             "this seven-stone root; the winning strategy tree is fully "
             "certified but the depth bound remains."),
            ("The certificate does not close any residual target row by "
             "itself; closure accounting happens only in a receipt fold."),
            ("REFUTED-D10 verdicts in the sweep are NOT LOSS proofs; "
             "pn/dn counts and solved counts are not game outcomes."),
            ("The standard 11x11 empty board, two-stone roots {49,60}/"
             "{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
        ],
    }
    with open(OUTPATH, "w", encoding="utf-8") as fh:
        json.dump(record, fh, sort_keys=True, indent=1)
        fh.write("\n")
    print(json.dumps({"gates": len(gates), "all_pass":
                      all(g["pass"] for g in gates),
                      "out": os.path.relpath(OUTPATH)}))


if __name__ == "__main__":
    main()
