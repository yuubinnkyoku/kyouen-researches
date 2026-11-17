#!/usr/bin/env python3
"""Full regeneration + independent verification of the two deferred WIN7-D10
certificates of the class2-lane cost-63c (bit 46) and cost-63d (bit 70) bands.

Background: the 2026-11-14 sweep records (class2-lane-cost63{c,d}-sweep-20261114.json)
document one WIN7-D10 certificate each (md5s 01bcaabc... / 63a3cb44...), but the
certificate files themselves were never pushed ("push deferred to next run";
1.4-1.6MB through the connector) and the bytes existed only as per-entry records.
The head-1452 census v3 therefore carried them as receiptcert-only records with
bytes absent from main. This script closes that gap:

 1. re-enumerates the loser first-moves on the RAW root with an inlined,
    independent Python Bareiss 4x4 enumeration (mirrors legal_candidates.py),
 2. regenerates each certificate per-move via node cert_driver63cd.ts
    (repo-verbatim class4_child1_cert_extractor_exact.ts, FBS=1<<20, probe 96,
    CLI-default KILL_BIT7 preference table; see the driver's reconstruction
    note: blind extraction does NOT reproduce the 2026-11-14 bytes),
 3. asserts the assembled whole certificate is byte-identical to the 2026-11-14
    records: md5, row count, sub-root count, loser mobility, terminal range
    (a cross-environment, cross-time determinism check, 2026-11-14 -> 2026-11-17),
 4. verifies the regenerated certificate with BOTH engine-free verifiers:
    the repo Bareiss verifier (verify_bit7_win7_cert.ts, per-sub-root batches
    with --consumed-out; consumed union == row set 0/0 both directions) and the
    third-implementation BigInt independent verifier
    (verify_win7_certificate_bigint_independent.mjs), with full field
    cross-agreement (seen/terminals/opponentEdges sums),
 5. asserts the published parts (part1of2+part2of2) are byte-exact halves of
    the regenerated whole and the sidecar records agree field-by-field.

Run from the experiment scripts directory (node v22+ with
--experimental-strip-types required). Output JSON is deterministic: no
timestamps, no wall times; running twice must produce byte-identical output.

11x11 empty board remains UNKNOWN; a WIN7-D10 certificate proves only that its
individual 7-stone root is a first-player win within depth 10. REFUTED-D10 is
not a LOSS proof. The 62 REFUTED bits of each band are not touched here.
"""
import concurrent.futures, hashlib, itertools, json, os, subprocess, sys

NODE = os.environ.get("NODE", "node")
EXTRACTOR = "class4_child1_cert_extractor_exact.ts"
DRIVER = "cert_driver63cd.ts"
BAREISS = "verify_bit7_win7_cert.ts"
BIGINT = "verify_win7_certificate_bigint_independent.mjs"
WORK = os.environ.get("REGEN_WORK", "/tmp/regen63cd")
OUT = ("../output/class2-lane-cost63cd-certificates-"
       "regeneration-verification-20261117.json")

# ---- pins (git blob shas of the repo-verbatim inputs, asserted at start) ----
PIN = {
    EXTRACTOR: "52bcaf509ea12fad4c936501d30d26b5b66c0085",
    DRIVER: "6cc1be810c774ea473ceec7299641afcec839f62",
    BAREISS: "2960afabdf7c1a7012d223974b65f1423e6890da",
    BIGINT: "62b5d9413daafb172f6e10249976ee6808f7b454",
}

# ---- the 2026-11-14 sweep-record expectations (pinned bytes) ----
SWEEP_RECORDS = {
    "63c": {
        "file": "class2-lane-cost63c-sweep-20261114.json",
        "blob_sha": "5770b951ecf5529c748964ea59de3e063bf2fcbc",
        "child": "000000000000008090a2000000000000",
        "bit": 46,
        "root": "000000000000008090a2400000000000",
        "rows": 45337,
        "extraction_nodes": 14524021,   # per-move partition node sum
        "mobility": 52,
        "md5": "01bcaabc9d20d20e6215826e22c01181",
        "sub_roots": 52,
        "terminal": [13, 17],
    },
    "63d": {
        "file": "class2-lane-cost63d-sweep-20261114.json",
        "blob_sha": "91dbb822aa906def5ef118963bfc53a24d1e32d4",
        "child": "00000000000000809082000000080000",
        "bit": 70,
        "root": "00000000000000c09082000000080000",
        "rows": 39213,
        "extraction_nodes": 9616344,    # original batch partition (memo cache shared across moves)
        "mobility": 49,
        "md5": "63a3cb44f1cfc7262509214a9f24d3ca",
        "sub_roots": 49,
        "terminal": [13, 17],
    },
}
# the per-move regeneration node sum of 63d differs from the recorded
# extraction_nodes: the original ran moves in batches inside single processes
# (shared memo table), the regeneration runs one process per move. The row set
# (and hence the certificate bytes and md5) is partition-invariant.
PERMOVE_NODE_SUMS = {"63c": 14524021, "63d": 14424015}


def blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# ---- independent legal-move enumeration (Bareiss 4x4, inlined) ----
def det4(m):
    a = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if a[k][k] == 0:
            for r in range(k + 1, 4):
                if a[r][k] != 0:
                    a[k], a[r] = a[r], a[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return a[3][3]


def legal_moves(hexstr):
    st = [i for i in range(121) if int(hexstr, 16) >> i & 1]
    rows = [[i % 11 * (i % 11) + i // 11 * (i // 11), i % 11, i // 11, 1] for i in st]
    out = []
    for p in range(121):
        if p in st:
            continue
        prow = [p % 11 * (p % 11) + p // 11 * (p // 11), p % 11, p // 11, 1]
        ok = True
        for (i, j, k) in itertools.combinations(range(len(st)), 3):
            if det4([rows[i], rows[j], rows[k], prow]) == 0:
                ok = False
                break
        if ok:
            out.append(p)
    return st, out


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    assert p.returncode == 0, (cmd, p.returncode, p.stderr[-400:])
    return p.stdout


def extract_move(tag, rec, m, outdir):
    pref = f"{outdir}/m{m}"
    p = subprocess.run([NODE, "--experimental-strip-types", DRIVER,
                        rec["child"], str(rec["bit"]), str(m), pref],
                       capture_output=True, text=True)
    assert p.returncode == 0, ("extraction failed", tag, m, p.stderr[-300:])
    d = json.loads(open(pref + ".summary.json").read())
    assert d["fbt_drops"] == 0 and not d.get("fatal"), ("fbt/fatal", tag, m, d)
    return m, d["sum"], d["nRows"], open(pref + ".rows").read()


def assert_sweep_record(tag, rec):
    """When run inside the repo (scripts dir), the pinned sweep record file
    must exist in ../output/ and agree with every inlined expectation."""
    p = f"../output/{rec['file']}"
    if not os.path.exists(p):
        return False  # out-of-repo run: inlined constants only
    b = open(p, "rb").read()
    assert blob_sha(b) == rec["blob_sha"], ("sweep record blob sha", tag)
    d = json.loads(b)
    c = d["win7_certificates"][0]
    assert c["root"] == rec["root"] and c["bit"] == rec["bit"]
    assert c["rows"] == rec["rows"] and c["extraction_nodes"] == rec["extraction_nodes"]
    assert c["sub_roots_pass"] == rec["sub_roots"]
    assert c["root_check"]["loser_mobility"] == rec["mobility"]
    assert c["root_check"]["loser_mobility_matches_independent_enumeration"] is True
    assert c["consumed_union_minus_cert"] == 0 and c["cert_minus_consumed_union"] == 0
    assert c["terminal_stone_range"] == rec["terminal"]
    assert c["fbt_drops"] == 0 and c["md5"] == rec["md5"]
    return True


def verify_one(tag, rec):
    outdir = f"{WORK}/{tag}"
    os.makedirs(outdir, exist_ok=True)
    st, moves = legal_moves(rec["root"])
    assert len(st) == 7, ("root stones", tag)
    assert len(moves) == rec["mobility"], ("mobility", tag, len(moves))
    sweep_record_in_repo = assert_sweep_record(tag, rec)

    per_move = {}
    rowset = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(extract_move, tag, rec, m, outdir) for m in moves]
        for f in futs:
            m, nodes, nrows, rows_txt = f.result()
            per_move[str(m)] = {"nodes": nodes, "rows": nrows}
            for ln in rows_txt.splitlines():
                if ln:
                    rowset.add(ln)
    node_sum = sum(v["nodes"] for v in per_move.values())
    assert node_sum == PERMOVE_NODE_SUMS[tag], ("per-move node sum", tag, node_sum)
    assert PERMOVE_NODE_SUMS[tag] == rec["extraction_nodes"] or tag == "63d", \
        ("63c per-move node sum must equal the record", tag)

    whole = ("n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS\n"
             f"root {rec['root']}\n"
             + "\n".join(sorted(rowset)) + "\n").encode()
    assert len(rowset) == rec["rows"], ("rows", tag, len(rowset))
    assert md5(whole) == rec["md5"], ("2026-11-14 md5 mismatch", tag)
    wpath = f"{outdir}/whole.cert"
    open(wpath, "wb").write(whole)

    # repo Bareiss verifier: root-check + per-sub-root batches with consumed-out
    rc = json.loads(run([NODE, "--experimental-strip-types", BAREISS,
                         "--cert", wpath, "--root", rec["root"], "--root-check"]
                        ).splitlines()[0])
    assert rc == {"stones": 7, "loserMobility": rec["mobility"]}, ("rootcheck", tag, rc)
    consumed = set()
    stats = {}
    for i in range(0, len(moves), 8):
        batch = ",".join(str(m) for m in moves[i:i + 8])
        out = run([NODE, "--experimental-strip-types", BAREISS,
                   "--cert", wpath, "--root", rec["root"],
                   "--subroots", batch, "--consumed-out", f"{outdir}/consumed.txt"])
        d = json.loads(out.splitlines()[-1])
        assert d["rows"] == rec["rows"], ("verifier rows", tag)
        for m in moves[i:i + 8]:
            stats["m%d" % m] = d["stats"]["m%d" % m]
    for ln in open(f"{outdir}/consumed.txt"):
        if ln.strip():
            consumed.add(ln.strip())
    assert len(consumed) == rec["rows"], ("consumed union size", tag, len(consumed))
    assert not (consumed - rowset_keys(whole)) and not (rowset_keys(whole) - consumed), \
        ("union mismatch", tag)
    tmin = min(s["range"][0] for s in stats.values())
    tmax = max(s["range"][1] for s in stats.values())
    assert [tmin, tmax] == rec["terminal"], ("terminal range", tag)
    assert len(stats) == rec["sub_roots"], ("subroots", tag)

    # third-implementation BigInt verifier
    out = run([NODE, BIGINT, wpath, str(rec["mobility"])])
    v = json.loads(out)
    assert v["verdict"] == "WIN7 certificate independently verified", ("bigint verdict", tag)
    assert v["root_hex"] == rec["root"] and v["root_stones"] == 7 and v["root_safe"] is True
    assert v["rows_sorted_unique"] is True
    assert v["strategy_rows"] == rec["rows"] and v["consumed_winner_rows"] == rec["rows"]
    assert v["union_missing"] == 0 and v["union_extra"] == 0
    assert v["subroots_passed"] == rec["sub_roots"]
    assert v["root_mobility"] == rec["mobility"]
    assert list(v["terminal_range"]) == rec["terminal"]
    # Bareiss vs BigInt cross-agreement
    assert sum(s["seen"] for s in stats.values()) == v["visited_states_across_subroots"], ("seen", tag)
    assert sum(s["terminals"] for s in stats.values()) == v["terminal_count"], ("terminals", tag)
    assert sum(s["opponentEdges"] for s in stats.values()) == v["loser_reply_edges"], ("edges", tag)

    # published parts must be byte-exact halves of the regenerated whole
    band = "../output/class2-lane-cost63cd-certificates"
    fn = f"n11_s7_{rec['root']}.cert"
    p1 = open(f"{band}/{fn}.part1of2", "rb").read()
    p2 = open(f"{band}/{fn}.part2of2", "rb").read()
    assert p1.endswith(b"\n") and p2.endswith(b"\n"), ("parts line boundary", tag)
    assert p1 + p2 == whole, ("parts joined != regenerated whole", tag)

    # sidecars agree field-by-field
    side = json.loads(open(f"{band}/bit{rec['bit']}-subroots.json").read().splitlines()[0])
    assert side["rows"] == rec["rows"] and side["stats"] == stats, ("sidecar", tag)
    rcs = json.loads(open(f"{band}/bit{rec['bit']}-rootcheck.json").read().splitlines()[0])
    assert rcs == {"stones": 7, "loserMobility": rec["mobility"]}, ("sidecar rootcheck", tag)

    return {
        "band": tag, "bit": rec["bit"], "root_hex": rec["root"],
        "sweep_record": f"../output/{rec['file']}",
        "sweep_record_blob_sha": rec["blob_sha"],
        "sweep_record_field_agreement_asserted": sweep_record_in_repo,
        "regeneration": {
            "method": ("repo-verbatim extractor CLI engine via cert_driver63cd.ts "
                       "(class4_child1_cert_extractor_exact.ts, FBS=1<<20, probe96, "
                       "CLI-default KILL_BIT7 pref table), one process per move, "
                       "4 workers, sort -u merge, header+root prepend"),
            "per_move_processes": len(moves),
            "per_move_node_sum": node_sum,
            "per_move_fbt_drops": 0,
            "per_move_fatal": 0,
            "per_move": {k: per_move[k] for k in sorted(per_move, key=int)},
        },
        "byte_identical_to_20261114_record": True,
        "whole_bytes": len(whole), "whole_md5": md5(whole),
        "whole_sha256": sha256(whole), "whole_git_blob_sha": blob_sha(whole),
        "rows": rec["rows"], "sub_roots_pass": rec["sub_roots"],
        "loser_mobility": rec["mobility"],
        "terminal_stone_range": rec["terminal"],
        "bareiss_verifier": {
            "rootcheck": rc, "subroots_all_pass": True,
            "consumed_union_minus_cert": 0, "cert_minus_consumed_union": 0,
            "per_subroot_stats": stats,
            "sum_seen": sum(s["seen"] for s in stats.values()),
            "sum_terminals": sum(s["terminals"] for s in stats.values()),
            "sum_opponent_edges": sum(s["opponentEdges"] for s in stats.values()),
        },
        "bigint_verifier": {
            "verdict": v["verdict"], "strategy_rows": v["strategy_rows"],
            "subroots_passed": v["subroots_passed"],
            "root_mobility": v["root_mobility"],
            "terminal_range": list(v["terminal_range"]),
            "terminal_count": v["terminal_count"],
            "visited_states_across_subroots": v["visited_states_across_subroots"],
            "loser_reply_edges": v["loser_reply_edges"],
            "winner_states": v["winner_states"], "loser_states": v["loser_states"],
            "union_missing": v["union_missing"], "union_extra": v["union_extra"],
        },
        "published_parts": {
            "part1of2_bytes": len(p1), "part2of2_bytes": len(p2),
            "part1of2_md5": md5(p1), "part2of2_md5": md5(p2),
            "joined_equals_regenerated_whole": True,
        },
        "sidecar_agreement": True,
    }


def rowset_keys(whole):
    return set(l.split(" ")[0] for l in whole.decode().splitlines()[2:])


def main():
    for f, pin in PIN.items():
        b = open(f, "rb").read()
        assert blob_sha(b) == pin, ("pin mismatch", f)
    entries = [verify_one("63c", SWEEP_RECORDS["63c"]),
               verify_one("63d", SWEEP_RECORDS["63d"])]
    doc = {
        "schema": "n11-class2-lane-cost63cd-certificates-regeneration-verification-20261117-v1",
        "date": "2026-11-17",
        "method": {
            "gap_closed": "the two WIN7-D10 certificates documented by the 2026-11-14 cost-63c/63d sweep records were never pushed (push_note: deferred; bytes existed only as per-entry records); this run regenerates both from the repo-verbatim extractor and publishes the bytes",
            "reconstruction": "the 2026-11-14 extraction used the extractor CLI whose default KILL_BIT7 session-6 preference table was active; a blind (empty kill table) extraction was tested first and does NOT reproduce the bytes (63c bit46 blind union 43,473 rows vs recorded 45,337); the KILL_BIT7-pref per-move reconstruction reproduces both certificates byte-identically (md5, rows) and node-exactly for 63c (per-move node sum 14,524,021 = recorded extraction_nodes)",
            "partition_note": "63d recorded extraction_nodes 9,616,344 came from the original batch partition (memo table shared across moves inside one process); the per-move regeneration sums to 14,424,015 nodes; the row set and certificate bytes are partition-invariant (observed previously and re-confirmed here by md5)",
            "verifiers": "both engine-free verifiers: repo Bareiss verify_bit7_win7_cert.ts (per-sub-root batches, --consumed-out, consumed union == row set 0/0 both directions, terminal range [13,17]) and the third-implementation BigInt verify_win7_certificate_bigint_independent.mjs; full cross-agreement of the per-sub-root stat sums",
            "pins": "all five repo inputs (extractor, driver, both verifiers, sweep records) asserted by git blob sha before use; sweep-record expectations inlined and asserted against the pinned sweep record bytes",
        },
        "entries": entries,
        "summary": {
            "certificates": 2, "regeneration_byte_identical": 2, "regeneration_mismatch": 0,
            "bareiss_pass": 2, "bigint_pass": 2, "sidecar_agreement_fail": 0,
            "total_rows": sum(e["rows"] for e in entries),
            "total_sub_roots": sum(e["sub_roots_pass"] for e in entries),
            "total_bytes": sum(e["whole_bytes"] for e in entries),
            "total_regeneration_nodes": sum(e["regeneration"]["per_move_node_sum"] for e in entries),
        },
        "interpretation_guard": [
            "the head-1452 census v3 carried these two records as receiptcert-only with bytes absent from main; after this publication the bytes are on main and independently re-verified (both verifiers) - a bookkeeping/evidence upgrade only, no frontier number changes and no manifest row closes",
            "the 62 REFUTED-D10 bits of each of the two bands are not LOSS proofs and are untouched by this run",
            "a WIN7-D10 certificate proves only that its individual 7-stone root is a first-player win within depth 10",
            "11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN",
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    print(json.dumps(doc["summary"]))


if __name__ == "__main__":
    main()
