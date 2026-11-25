#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_verify_record_20261120: assemble the master record
(windfall4-cert-triple-verification-20261120.json) for the certificate
extraction and triple independent verification of the four resolve6 windfall
WIN7-D10 roots (class2-lane-cost65h child 00000000000000803202000000001000,
bits 40/43/99/118).

Fail-closed: any gate below raises SystemExit; the record is only written
when every gate passes.

Determinism: stdlib only, no wall clock in the record body (the fixed session
date 2026-11-20 is recorded once), sort_keys JSON; two runs byte-identical.

Interpretation guard: the certificates and their verifications prove the
game-theoretic fact "the original first player wins from the 7-stone root
(second player to move, loser stuck at terminals)" for these four roots.
They do NOT close any of the 78 residual five-parent target rows by
themselves: row-closure bookkeeping happens only in a receipt-fold record that
consumes these certificates. All n11 meta-status remains UNKNOWN.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPDIR = os.path.abspath(os.path.join(HERE, ".."))
OUTDIR = os.path.join(EXPDIR, "output")
OUTPATH = os.path.join(OUTDIR, "windfall4-cert-triple-verification-20261120.json")

SESSION_DATE = "2026-11-20"
CHILD_HEX = "00000000000000803202000000001000"
BITS = [40, 43, 99, 118]
PUBLISHED_RAW_NODES = {40: 1105860, 43: 3269824, 99: 1114855, 118: 2307338}
TERM_MIN, TERM_MAX = 13, 17

RESOLVE6 = {
    "path": ("research/experiments/n11-residual78-cache-join-resolve6-20261120/"
             "output/post-saturation-full-cache-join-resolve6-20261120.json"),
    "sha256": ("e85d4bfb867a193f2b3cdb23ec9e15679359c9f3"
               "37fcd97eb5c62473b90c281a"),
}
SESSION_STAMP = "20261120"
CERT_TEMPLATE = "certs/win7-root-%s-" + SESSION_STAMP + ".n11"


def need(ok, msg):
    if not ok:
        raise SystemExit("GATE FAILED: " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---- D4 canon (resolve5/resolve6 conventions) ----
TF = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0:
            X, Y = x, y
        elif t == 1:
            X, Y = 10 - y, x
        elif t == 2:
            X, Y = 10 - x, 10 - y
        elif t == 3:
            X, Y = y, 10 - x
        elif t == 4:
            X, Y = 10 - x, y
        elif t == 5:
            X, Y = x, 10 - y
        elif t == 6:
            X, Y = y, x
        else:
            X, Y = 10 - y, 10 - x
        tab.append(11 * Y + X)
    TF.append(tab)


def popcount(v):
    return bin(v).count("1")


def d4_canon(v):
    best = None
    for tab in TF:
        w = 0
        for i in range(121):
            if (v >> i) & 1:
                w |= 1 << tab[i]
        if best is None or w < best:
            best = w
    return best


def main():
    resolve6_path = sys.argv[1] if len(sys.argv) > 1 else RESOLVE6["path"]
    need(sha256_file(resolve6_path) == RESOLVE6["sha256"],
         "resolve6 record sha256 pin")
    resolve6 = load(resolve6_path)
    evidence = {e["root"]: e for e in
                resolve6["checks"][11]["detail"]["evidence"]}
    win_cover = resolve6["resolve"]["win_cover_detail"]

    # map (child, bit) -> canonical evidence root
    canon_key = {}
    for e in evidence.values():
        for m in e["engine_entries"]:
            if m["child_hex"] == CHILD_HEX:
                canon_key[m["bit"]] = e
    need(sorted(canon_key) == BITS,
         "resolve6 evidence child/bit set = 40/43/99/118")

    checks = []

    def check(name, cond, detail=None):
        checks.append({"name": name, "pass": bool(cond), "detail": detail})
        need(cond, name)
        return True

    runner_lines = []
    with open(os.path.join(OUTDIR,
             "runner-v16-node-exact-crosscheck-20261120.jsonl"),
             "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                runner_lines.append(json.loads(line))
    pilot = [r for r in runner_lines if "control" in r]
    runner_bits = {r["bit"]: r for r in runner_lines if "bit" in r}
    check("runner-v16-pilot-d6-control",
          len(pilot) == 1 and pilot[0]["loss"] is False
          and pilot[0]["nodes"] == 3402 and pilot[0]["capped"] is False,
          pilot[0])
    check("runner-v16-bits", sorted(runner_bits) == BITS,
          {"bits": sorted(runner_bits)})

    roots = []
    for bit in BITS:
        raw_root = format(int(CHILD_HEX, 16) | (1 << bit), "032x")
        canon_hex = format(d4_canon(int(raw_root, 16)), "032x")
        ev = canon_key[bit]
        check("canonical-mapping-bit%d" % bit, canon_hex == ev["root"],
              {"raw_root_hex": raw_root, "canonical_root_hex": canon_hex,
               "resolve6_evidence_root": ev["root"]})

        cert_name = CERT_TEMPLATE % raw_root
        cert_path = os.path.join(EXPDIR, cert_name)
        cert_sha = sha256_file(cert_path)
        cert_md5 = md5_file(cert_path)
        cert_bytes = os.path.getsize(cert_path)
        lines = [l for l in open(cert_path, encoding="utf-8").read().
                 splitlines() if l.strip()]
        check("cert-header-root-bit%d" % bit,
              lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                           "second_to_move_LOSS")
              and lines[1] == "root " + raw_root
              and popcount(int(raw_root, 16)) == 7,
              {"header": lines[0], "root_line": lines[1]})
        rows = lines[2:]
        need(len(rows) == len(set(r.split()[0] for r in rows)),
             "duplicate row bit%d" % bit)
        need(all(r > rows[i - 1] for i, r in enumerate(rows) if i > 0),
             "unsorted rows bit%d" % bit)

        run1 = load(os.path.join(
            OUTDIR, "extraction-run1-summary-bit%d-%s.json" % (bit, SESSION_STAMP)))
        rr = load(os.path.join(
            OUTDIR, "extraction-rerun-summary-bit%d-%s.json" % (bit, SESSION_STAMP)))
        check("extraction-determinism-bit%d" % bit,
              run1["sum"] == rr["sum"] and run1["nRows"] == rr["nRows"]
              and run1["fbt_drops"] == 0 and rr["fbt_drops"] == 0
              and "fatal" not in run1 and "fatal" not in rr
              and run1["nRows"] == len(rows) and run1["bit"] == bit
              and run1["child"] == CHILD_HEX,
              {"run1_nodes": run1["sum"], "rerun_nodes": rr["sum"],
               "rows": run1["nRows"], "moves": run1["moves"],
               "cert_sha256_run1_and_rerun_byte_identical": cert_sha})
        terms = [pm["terminalRange"]
                 for pm in run1["perMove"].values() if pm["terminalRange"]]
        tmin = min(t[0] for t in terms)
        tmax = max(t[1] for t in terms)
        check("extraction-terminal-range-bit%d" % bit,
              TERM_MIN <= tmin and tmax <= TERM_MAX
              and all(pm["ok"] and not pm["capped"]
                      for pm in run1["perMove"].values()),
              [tmin, tmax])
        check("extraction-moves-bit%d" % bit,
              run1["moves"] == len(run1["perMove"])
              and run1["moves"] == len(rr["perMove"]),
              run1["moves"])

        rc = load(os.path.join(
            OUTDIR, "ts-root-check-bit%d-%s.json" % (bit, SESSION_STAMP)))
        check("ts-root-check-bit%d" % bit,
              rc["stones"] == 7 and rc["loserMobility"] == run1["moves"],
              rc)

        sub_count = 0
        for ln in open(os.path.join(
                OUTDIR, "ts-subroot-stats-bit%d-%s.jsonl" % (bit, SESSION_STAMP)),
                encoding="utf-8"):
            if not ln.strip():
                continue
            stats = json.loads(ln)["stats"]
            sub_count += len(stats)
            for k, st in stats.items():
                need(st["range"][0] >= TERM_MIN and st["range"][1] <= TERM_MAX,
                     "terminal range violation %s %s" % (k, st))
        check("ts-subroots-bit%d" % bit, sub_count == run1["moves"],
              {"subroots_verified": sub_count, "moves": run1["moves"]})

        audit = load(os.path.join(
            OUTDIR, "ts-union-audit-bit%d-%s.json" % (bit, SESSION_STAMP)))
        check("ts-union-exact-bit%d" % bit,
              audit["exact_union"] and audit["missing"] == 0
              and audit["extra"] == 0
              and audit["consumed_unique"] == len(rows)
              and audit["certificate_rows"] == len(rows),
              audit)

        py = load(os.path.join(
            OUTDIR, "python-bareiss-replay-bit%d-%s.json" % (bit, SESSION_STAMP)))
        check("python-bareiss-replay-bit%d" % bit,
              py["root_stones"] == 7
              and py["root_loser_mobility"] == run1["moves"]
              and py["subroots_passed"] == run1["moves"]
              and py["strategy_rows"] == len(rows)
              and py["consumed_rows"] == len(rows)
              and py["union_missing"] == 0 and py["union_extra"] == 0
              and all(TERM_MIN <= x <= TERM_MAX
                      for x in py["terminal_stone_range"])
              and "independently verified" in py["verdict"],
              {k: py[k] for k in ("root_loser_mobility", "subroots_passed",
                                  "strategy_rows", "union_missing",
                                  "union_extra", "terminal_stone_range",
                                  "visited_winner_states")})

        big = load(os.path.join(
            OUTDIR, "bigint-independent-verification-bit%d-%s.json"
            % (bit, SESSION_STAMP)))
        check("bigint-independent-bit%d" % bit,
              big["root_stones"] == 7 and big["root_safe"]
              and big["rows_sorted_unique"]
              and big["root_mobility"] == run1["moves"]
              and big["subroots_passed"] == run1["moves"]
              and big["strategy_rows"] == len(rows)
              and big["consumed_winner_rows"] == len(rows)
              and big["union_missing"] == 0 and big["union_extra"] == 0
              and big["terminal_range"][0] >= TERM_MIN
              and big["terminal_range"][1] <= TERM_MAX,
              {k: big[k] for k in ("root_mobility", "subroots_passed",
                                   "strategy_rows", "union_missing",
                                   "union_extra", "terminal_range",
                                   "visited_states_across_subroots",
                                   "winner_states", "loser_states",
                                   "terminal_count")})

        rb = runner_bits[bit]
        pub_ev = ev["engine_entries"][0]["raw_provenance"][0]
        check("runner-v16-node-exact-bit%d" % bit,
              rb["loss"] is True and rb["capped"] is False
              and rb["bit"] == bit
              and rb["nodes"] == PUBLISHED_RAW_NODES[bit]
              and rb["nodes"] == pub_ev["bit_line"]["nodes"]
              and rb["terminalStoneRange"] == [TERM_MIN, TERM_MAX]
              and pub_ev["bit_line"]["loss"] is True
              and TERM_MIN <= pub_ev["bit_line"]["terminalStoneRange"][0]
              and pub_ev["bit_line"]["terminalStoneRange"][1] <= TERM_MAX,
              {"fresh_nodes": rb["nodes"],
               "published_raw_bit_line_nodes": pub_ev["bit_line"]["nodes"],
               "raw_batch_file": pub_ev["file"]})
        check("covered-rows-match-resolve6-bit%d" % bit,
              ev["covered_residual_rows"] is not None
              and ev["unsafe_quadruples"] == 0 and ev["d4_canonical"],
              ev["covered_residual_rows"])

        roots.append({
            "bit": bit,
            "child_hex": CHILD_HEX,
            "raw_root_hex": raw_root,
            "canonical_root_hex": canon_hex,
            "resolve6_evidence_root": ev["root"],
            "covered_residual_rows": ev["covered_residual_rows"],
            "raw_batch_provenance": {
                "file": pub_ev["file"],
                "published_bit_line": pub_ev["bit_line"],
                "pilot_control_line": pub_ev["pilot_control_line"],
                "lane_context": ev["engine_entries"][0]["lane_context"],
            },
            "extraction": {
                "driver": "scripts/cert_driver_windfall.ts",
                "extractor": ("scripts/class4_child1_cert_extractor_exact_ms23.ts "
                              "(repo-verbatim; FBS=1<<20 forbidden-bit table, "
                              "MS=1<<23 memo, CAP=1e9)"),
                "kill_table": "empty (blind, pref=null)",
                "moves": run1["moves"],
                "nodes_run1": run1["sum"],
                "nodes_rerun": rr["sum"],
                "rows": run1["nRows"],
                "fbt_drops": run1["fbt_drops"],
                "fatal": None,
                "terminal_range": [tmin, tmax],
                "rerun_byte_identical": True,
            },
            "certificate": {
                "file": cert_name,
                "bytes": cert_bytes,
                "md5": cert_md5,
                "sha256": cert_sha,
            },
            "ts_verify_bit7_win7_cert": {
                "root_check": rc,
                "subroots_verified": sub_count,
                "union_audit": audit,
            },
            "python_bareiss_replay": py,
            "bigint_independent_verification": big,
            "runner_v16_fresh_crosscheck": rb,
        })

    # driver-run1 summaries must also record no fatal and correct child/bit
    record = {
        "schema": ("n11-windfall4-win7-cert-extract-triple-verify-v1 "
                   "(2026-11-20)"),
        "date": SESSION_DATE,
        "status": ("windfall-4-WIN7-roots-certificate-backed-pending-fold"),
        "source_main": "bd092b8df2ea24723d0497dd400066360f902314",
        "inputs": {
            "resolve6_record": RESOLVE6,
            "child_hex": CHILD_HEX,
            "bits": BITS,
            "session_tooling": {
                "node": "v22.20.0 (--experimental-strip-types)",
                "python": "3.12.14 (stdlib only)",
            },
        },
        "what": ("Certificate extraction (blind, empty kill table) of the four "
                 "resolve6 windfall WIN7-D10 roots -- the class2-lane-cost65h "
                 "child 00000000000000803202000000001000 at bits 40/43/99/118 "
                 "-- followed by three independent exact verifications: "
                 "(1) TS number-arithmetic Bareiss 4x4 sub-root decomposition "
                 "with exact consumed-union audit, (2) pure-python exact "
                 "Bareiss full replay expanding every loser reply, "
                 "(3) BigInt 3x3 cofactor independent verifier. Plus a fresh "
                 "repo-verbatim runner v16 (depth 10, andclose=1, cap 1e9) "
                 "node-exact re-solve of all four raw bit lines and the "
                 "extraction rerun (byte-identical certificates)."),
        "roots": roots,
        "checks": checks,
        "interpretation_guard": [
            "These certificates prove the game-theoretic statement for each "
            "7-stone root: with the second mover to move, the original first "
            "mover forces a win with the loser stuck at every terminal "
            "(13-17 stones).",
            "No residual five-parent target row is CLOSED by this record. "
            "Closure by receipts happens only in a subsequent receipt-fold "
            "record that consumes these certificates (the row-bookkeeping "
            "machine of K1057/K1063 lineage). Until that fold exists, the "
            "four covered rows stay pending-win, and the 39-root live witness "
            "plan of resolve6 still independently covers all 78 residual "
            "rows.",
            "A WIN7 receipt root is not a statement about the value of the "
            "covered 6-stone row itself; REFUTED-D10 is not a LOSS proof; no "
            "pn/dn or solved-count is read as a verdict.",
        ],
        "unknown_status": ("11x11 empty board, two-stone root {49,60}/{59,60}, "
                           "S2 {59,60}, class 1/2/4: UNKNOWN"),
    }
    with open(OUTPATH, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"out": OUTPATH, "checks": len(checks),
                      "all_pass": all(c["pass"] for c in checks),
                      "sha256": sha256_file(OUTPATH)}))


if __name__ == "__main__":
    main()
