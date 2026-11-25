# audit_eg.py -- fail-closed gate battery for the Part EG third-implementation
# cross-verification of the SIX published class-34908 unconsumed honest-label
# WIN rows {af029, af047, af050, af053, af023, af048} (the COMPLETE remaining
# unknown-children set of closure class 34908 per the published Part EE wave F
# reaudit closure table), including the declared this-host pinned-replica
# 2-pass reproductions (batch-33 15M rows / Part EA 30M reprobe rows / the
# af029 double 15M+30M reproduction). Every gate must PASS or the script
# exits rc=1 with the gate name. Reads only local artifacts under this
# experiment dir; writes output/audit-summary.json.
#
# Adapted from the published Part CZ audit (audit_cz.py, sha256
# 3c95e32fcae03441e76e3e77765838d3ea195de5aaebba38fec32df92006a4a0, experiment
# n11-centralreply-closure-b29ab028win-thirdimpl-20261124, itself from the
# published Part CW audit / CM / CL / CC / BY / BX / BW / BV chain). Declared
# deltas (all recorded in the Part EG declaration before execution):
# EXP/SCHEMA/rows-schema strings; the per-target replica budget map
# (15000000 for af029/af047/af050/af053 batch-33 rows, 30000000 for the
# af023/af048 Part EA 30M reprobe rows -- their 15M b33 runs ended honest
# EXHAUSTED, so those 15M raws are provenance only and are NOT verdict
# comparison rows); the af029-30m double-reproduction gate (G2c: the same
# af029 key re-run at the 30M anchor condition must reproduce the published
# Part EA anchor pair node-exactly); the pinned raw-out sha pins for all six
# targets (12 files) plus the EA af029 anchor pair (2 files) and the EA af001
# anchor pair (2 files, adopted-row provenance); the unadopted-corroboration
# source pins switched from the Part CU publications to the Part EE
# af034loss1 adoption publications (merged canonical cache fc3e4ac9 6,666
# rows = EC base cecc1a0f 6,665 + the single adopted af034 60M LOSS row;
# increment cc9c4746; increments-manifest 0ad3469e schema
# af034loss1-increments-manifest-v1, whose win_scenario_note names all six
# pooled unconsumed WIN children); a POSITIVE control that the adopted af034
# row occurs exactly once in the merged cache (so the would-be-row absence
# gates cannot pass vacuously); target-absence is checked BOTH as the exact
# would-be s5verdict line AND as any same-(lo,hi) pair row; the G6 id-list
# battery adapted to the EE manifest shape (targets must appear in NO
# adopted/win/probed id list; af029 legitimately appears in batches[0].
# anchor_ids as Part EA anchor provenance -- declared, not an adoption list);
# and the EE manifest's fileless-unprobed roster concept does not exist for
# this adoption (full_packet_eq_loss_only=true, unadopted_win_ids=[]).
# Verdicts are NOT consumed: all six rows are honest labels pending the
# scrutiny owner C++ second-implementation gate pin 9193f5b6; nothing is
# adopted, freed, closed, or claimed. The standard 11x11 empty board, the
# central-reply roots, class 34908 and every key stay UNKNOWN.
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-closure-b33win6-thirdimpl-20261125"
SCHEMA = "n11-centralreply-closure-b33win6-thirdimpl-audit-v1"
ROWS_SCHEMA = "n11-centralreply-closure-b33win6-thirdimpl-input-v1"

PIN_THIRD = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
PIN_JSREPLAY = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
PIN_MERGED_CANONICAL = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
PIN_MERGED_BASE = "cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626"
PIN_INCREMENT = "cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162"
PIN_INCR_MANIFEST = "0ad3469ede4bfbddaee21d12dbab97f7e0babdbe5cbaba8cc7a6f2f41d0d22c9"
PIN_STATUS_ROWS_JSON = "799d9faf191c5a7c1bfc164f4a2df46df91b4a01f02ce0e458718b7d2782c19b"
AF034_ADOPTED_ROW = "s5verdict,1152921504607911937,68719476736,5,2,32012059"
PIN_RAW = {
    # batch-33 published 15M drive rows (experiment n11-centralreply-closure-class34908-batch33-20261124)
    "af029.p1": "6bd7a2ac37cccd8a387d6b505112c1a93b712e8d41b43467fa0844ce64ec0036",
    "af029.p2": "b6abaa6384ee93c890cadd350f2f844889f3ee42110935a366af7893a2030e0b",
    "af047.p1": "8fd62fdd27d10235b4ba67c6f43cfeb4fe5f494559544119d4f0339223a7b8c6",
    "af047.p2": "ae4719e8c8a0a7abd72cec6f4e013c1e576c7627100de95b55ba34c364b694a4",
    "af050.p1": "3ea4f644ca19186f0a56ae25f79ef0ccc8b608b5ef64045bc052a488cae9b1d7",
    "af050.p2": "43a5b71ca57d2a2601f82b7ec35980b0761dc315e8093f3c9ae603cd8d4ca5a6",
    "af053.p1": "fce95ca8921357641f477a01483fbd4c35e6f183a25c8d741657dec645f78533",
    "af053.p2": "920b1029500e93532238d03d07e89fdf091ffecd2481cab56f7dd032b5f645b7",
    # Part EA published 30M reprobe rows (experiment n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125)
    "af023.p1": "fe118851a927944328a62387d0410a596713c87f1360dda662c97f87913c1dbe",
    "af023.p2": "af02e38b07a7f1da9af28c0af7985eaa0cdd97ec2884298ede3a831b19c9198b",
    "af048.p1": "ae8df6ad6f922669f285f1c2a20d7fa09453c2ef38f64f1b4b878c3034e9d07a",
    "af048.p2": "e2056ca26533124e20d3538eebc5e6c4b752be21b92e9e3780c5a0040f0bb620",
    # Part EA af029 30M anchor pair (double-reproduction comparison)
    "af029-30m.p1": "1726ecb6d8199d612130d3c2cae12b176102fef0468263cbc1397f525eb0aa66",
    "af029-30m.p2": "c937f8964385b2e4c74c1f1d417cdb113b2548dca33c3e0604facea7d9c905a6",
    # Part EA af001 30M anchor pair (EE adopted-row provenance control)
    "af001.p1": "c2bc73f6a5d88720e33fc3fb498ab16f2d541d7cad62248ef8d04b5f9351381d",
    "af001.p2": "e4614f6bd7d4f20cfdd7dba3362e6db52328827a120b9d379fdd2accbdbf1681",
}
# raw sources dir per target key (b33 = the 15M comparison family,
# ea = the 30M comparison family)
SRC_DIR = {"af029": "b33-raw", "af047": "b33-raw", "af050": "b33-raw", "af053": "b33-raw",
           "af023": "ea-raw", "af048": "ea-raw", "af029-30m": "ea-raw", "af001": "ea-raw"}
RAW_SRC_NAME = {"af029-30m": "af029"}

VALGATE_KEYS = [("at2m-s5-1152921504606851072-536870946", 2000000),
                ("at2m-s5-1188950301626860544-536870912", 2000000),
                ("first-15m-s5-1152921504606851072-536870946", 15000000),
                ("second-15m-s5-1188950301626860544-536870912", 15000000)]

gates = []
def gate(name, ok, detail=""):
    gates.append({"gate": name, "pass": bool(ok), "detail": str(detail)})
    if not ok:
        summary = {"schema": SCHEMA, "experiment": EXP, "all_pass": False, "gates": gates}
        with open(os.path.join(ROOT, "output", "audit-summary.json"), "w") as fh:
            json.dump(summary, fh, indent=1); fh.write("\n")
        print("GATE FAILED:", name, detail)
        sys.exit(1)
    print("PASS", name, detail)

def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_third_line(line):
    if not line.startswith("third,"):
        return None
    raw = line.rstrip("\n")
    f = raw.split(",")
    d = {"raw": raw, "stub": "third"}
    try:
        if f[5] == "GATE_FAIL" or (len(f) > 5 and f[5].startswith('"')):
            d["gate_fail"] = ",".join(f[5:]).strip('"')
            return d
        d["row"], d["legalIn"], d["legalDerived"] = f[1], int(f[3]), int(f[4])
        d["result"], d["expansion"], d["ttHits"], d["wall"] = int(f[5]), int(f[6]), int(f[7]), float(f[8])
        d["lo"], d["hi"] = int(f[9]), int(f[10])
        d["reason"] = f[11]
        for tail in f[12:]:
            if tail.startswith("quads="): d["quads"] = int(tail[6:])
            elif tail.startswith("ttOverwrites="): d["overwrites"] = int(tail[13:])
            elif tail.startswith("memoPower="): d["memoPower"] = int(tail[10:])
    except (ValueError, IndexError):
        d = {"raw": raw, "stub": "third", "gate_fail": "malformed third line: " + raw[:80]}
    return d

def read_run(kind, key, tag):
    p = os.path.join(ROOT, "output", kind, f"{key}.{tag}.out")
    if not os.path.isfile(p):
        return None
    with open(p) as fh:
        for line in fh:
            if line.startswith("third,"):
                d = parse_third_line(line)
                if d is not None and "gate_fail" in d and kind != "negative":
                    return None
                return d
    return None

def parse_replay_out(path):
    if not os.path.isfile(path):
        return None, False, False
    row, done, quads = None, False, False
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                row = line.strip().split(",")
            if line.startswith("# replay_done"):
                done = True
            if line.startswith("# forbidden quadruples: 95670"):
                quads = True
    return row, done, quads

def main():
    rows = json.load(open(os.path.join(ROOT, "input", "rows.json")))
    gate("rows-json-pin", sha256(os.path.join(ROOT, "input", "rows.json")) == PIN_STATUS_ROWS_JSON,
         sha256(os.path.join(ROOT, "input", "rows.json")))

    # -- G0: input CSVs carry exactly the rows.json keys (exact Python ints;
    #        guards against any transport rounding of 61-bit keys)
    for grp in ("targets", "anchors", "negatives"):
        for r in rows.get(grp, []):
            p = os.path.join(ROOT, "input", f"{r['key_id']}.input.csv")
            if not os.path.isfile(p):
                gate(f"input-{r['key_id']}-present", False, p)
                continue
            f = open(p).read().strip().split(",")
            ok = (f[0] == "target" and int(f[2]) == r["stones"] and int(f[3]) == r["lo"]
                  and int(f[4]) == r["hi"] and int(f[5]) == r["legal"])
            gate(f"input-{r['key_id']}-matches-rows", ok,
                 f"{f[2]},{f[3]},{f[4]},{f[5]} vs {r['stones']},{r['lo']},{r['hi']},{r['legal']}")

    # -- G1: pinned script bytes
    gate("pin-third_impl.js",
         sha256(os.path.join(ROOT, "scripts", "third_impl.js")) == PIN_THIRD,
         sha256(os.path.join(ROOT, "scripts", "third_impl.js")))
    gate("pin-jsreplay.js",
         sha256(os.path.join(ROOT, "scripts", "jsreplay.js")) == PIN_JSREPLAY,
         sha256(os.path.join(ROOT, "scripts", "jsreplay.js")))
    gate("rows-schema",
         rows["schema"] == ROWS_SCHEMA
         and rows.get("consumed_into_canonical_cache") is False
         and rows.get("unadopted_win_rows") is True
         and rows.get("unadopted_loss_rows") is False
         and rows.get("canonical_cache_sha256_unchanged") == PIN_MERGED_CANONICAL,
         rows.get("schema"))
    gate("target-count", len(rows["targets"]) == 6,
         f"{len(rows['targets'])} (6 class-34908 unconsumed WIN rows: af029/af047/af050/af053 @15M, af023/af048 @30M)")
    gate("target-verdict-kinds",
         sorted(t["expect_third"] for t in rows["targets"]) == [1] * 6,
         f"{sorted(t['expect_third'] for t in rows['targets'])}")
    gate("target-budget-map",
         all(t["budget"] in (15000000, 30000000) for t in rows["targets"])
         and sorted(t["key_id"] for t in rows["targets"] if t["budget"] == 15000000) == ["af029", "af047", "af050", "af053"]
         and sorted(t["key_id"] for t in rows["targets"] if t["budget"] == 30000000) == ["af023", "af048"],
         str([(t["key_id"], t["budget"]) for t in rows["targets"]]))

    # -- G2: rules-engine gate output (verify_tbl_eg run, captured in output/rules-gate.txt)
    p = os.path.join(ROOT, "output", "rules-gate.txt")
    if not os.path.isfile(p):
        gate("rules-gate-present", False, "missing output/rules-gate.txt")
    txt = open(p).read()
    gate("rules-gate-quads", "replica quads 95670 mine quads 95670" in txt, txt.splitlines()[0] if txt else "")
    ok_mis = ("mismatches 0" in txt)
    gate("rules-gate-tbl-mismatch0", ok_mis, [l for l in txt.splitlines() if l.startswith("triples")])

    # -- G2b: declared this-host pinned-replica reproduction (fresh-cold 2-pass):
    #        determinism fields p1==p2 AND exact match with the published
    #        honest-label WIN rows (result/nodes), at the per-target budget.
    for t in rows["targets"]:
        k = t["key_id"]
        f1, d1, q1 = parse_replay_out(os.path.join(ROOT, "output", "replica", f"{k}.p1.out"))
        f2, d2, q2 = parse_replay_out(os.path.join(ROOT, "output", "replica", f"{k}.p2.out"))
        gate(f"replica-{k}-present", f1 is not None and f2 is not None, "p1/p2")
        if not (f1 and f2):
            continue
        gate(f"replica-{k}-done", d1 and d2, f"replay_done p1={d1} p2={d2}")
        gate(f"replica-{k}-quads", q1 and q2, f"quads-header p1={q1} p2={q2}")
        det_ok = all(f1[i] == f2[i] for i in (3, 4, 5, 6, 7, 9, 10))
        gate(f"replica-{k}-det-pair", det_ok, f"p1={f1[3:8]} p2={f2[3:8]}")
        gate(f"replica-{k}-schema", f1[2] == "5" and f1[1] == "0" and int(f1[5]) == t["budget"],
             f"schema {f1[:6]} (budget {t['budget']})")
        gate(f"replica-{k}-key", int(f1[9]) == t["lo"] and int(f1[10]) == t["hi"] and int(f1[3]) == t["legal"],
             f"{f1[9]},{f1[10]},{f1[3]} vs {t['lo']},{t['hi']},{t['legal']}")
        gate(f"replica-{k}-verdict-vs-published",
             int(f1[6]) == t["replica_result"] and int(f1[7]) == t["replica_nodes"],
             f"this-host result={f1[6]} nodes={f1[7]} vs published result={t['replica_result']} nodes={t['replica_nodes']}")

    # -- G2c: af029 double reproduction at the 30M anchor condition (the
    #   same key family also published as the Part EA anchor pair: budget
    #   30M, result 1, nodes 4862485 -- identical to the 15M row).
    f1, d1, q1 = parse_replay_out(os.path.join(ROOT, "output", "replica", "af029-30m.p1.out"))
    f2, d2, q2 = parse_replay_out(os.path.join(ROOT, "output", "replica", "af029-30m.p2.out"))
    gate("replica-af029-30m-present", f1 is not None and f2 is not None, "p1/p2")
    if f1 and f2:
        gate("replica-af029-30m-done", d1 and d2, f"replay_done p1={d1} p2={d2}")
        gate("replica-af029-30m-det-pair", all(f1[i] == f2[i] for i in (3, 4, 5, 6, 7, 9, 10)),
             f"p1={f1[3:8]} p2={f2[3:8]}")
        gate("replica-af029-30m-schema", f1[2] == "5" and f1[1] == "0" and int(f1[5]) == 30000000,
             f"schema {f1[:6]}")
        gate("replica-af029-30m-verdict-vs-published",
             int(f1[6]) == 1 and int(f1[7]) == 4862485 and int(f1[9]) == 1152921504607895553
             and int(f1[10]) == 68720525312 and int(f1[3]) == 86,
             f"this-host 30M result={f1[6]} nodes={f1[7]} vs published 30M anchor result=1 nodes=4862485")

    # -- G3: anchors reproduce published deterministic counts
    for a_instance, tagA, tagB in [(rows["anchors"][0], "a", "b"), (rows["anchors"][1], "a", "b")]:
        ka = a_instance["key_id"]
        ra, rb = read_run("anchors", ka, tagA), read_run("anchors", ka, tagB)
        gate(f"anchor-{ka}-present", ra is not None and rb is not None, f"{tagA}/{tagB}")
        if not (ra and rb):
            continue
        for r, t in ((ra, tagA), (rb, tagB)):
            gate(f"anchor-{ka}-{t}-clean", r["result"] == a_instance["expect_third"] and r["reason"] == "clean" and r["quads"] == 95670,
                 f"result={r['result']} reason={r['reason']}")
            gate(f"anchor-{ka}-{t}-expansions", r["expansion"] == a_instance["anchor_expansions"] and r["ttHits"] == a_instance["anchor_ttHits"],
                 f"exp={r['expansion']} vs {a_instance['anchor_expansions']}, ttH={r['ttHits']} vs {a_instance['anchor_ttHits']}")
            gate(f"anchor-{ka}-{t}-legal", r["legalDerived"] == a_instance["legal"], f"{r['legalDerived']} vs {a_instance['legal']}")
            gate(f"anchor-{ka}-{t}-key", r["lo"] == a_instance["lo"] and r["hi"] == a_instance["hi"], f"{r['lo']}:{r['hi']}")
        gate(f"anchor-{ka}-det-pair",
             ra["expansion"] == rb["expansion"] and ra["ttHits"] == rb["ttHits"] and ra["result"] == rb["result"],
             f"{ra['expansion']} vs {rb['expansion']}")

    # -- G4: negative gates fail closed as designed
    ng1 = read_run("negative", "ng1", "a")
    gate("neg-ng1-failclosed", ng1 is not None and "gate_fail" in ng1 and "legal count mismatch" in ng1["gate_fail"], str(ng1))
    ng2 = read_run("negative", "ng2", "a")
    gate("neg-ng2-failclosed", ng2 is not None and "gate_fail" in ng2 and "stone count mismatch" in ng2["gate_fail"], str(ng2))

    # -- G5: targets: 2-run determinism + verdict agreement per row
    verdicts = []
    inconclusive = []
    exp_total = 0
    for t in rows["targets"]:
        k = t["key_id"]
        ra, rb = read_run("targets", k, "a"), read_run("targets", k, "b")
        gate(f"target-{k}-present", ra is not None and rb is not None, "a/b")
        if not (ra and rb):
            continue
        for r, tg in ((ra, "a"), (rb, "b")):
            gate(f"target-{k}-{tg}-key", r["lo"] == t["lo"] and r["hi"] == t["hi"], f"{r['lo']}:{r['hi']}")
            gate(f"target-{k}-{tg}-legal", r["legalDerived"] == t["legal"], f"{r['legalDerived']} vs {t['legal']}")
            gate(f"target-{k}-{tg}-quads", r.get("quads") == 95670, r.get("quads"))
        gate(f"target-{k}-det-pair",
             ra["result"] == rb["result"] and ra["expansion"] == rb["expansion"] and ra["ttHits"] == rb["ttHits"]
             and ra["reason"] == rb["reason"],
             f"a=({ra['result']},{ra['expansion']},{ra['reason']}) b=({rb['result']},{rb['expansion']},{rb['reason']})")
        if ra["reason"] == "clean" and ra["result"] == t["expect_third"]:
            verdicts.append({"key_id": k, "source": t.get("source"), "budget": t["budget"],
                             "replica_result": t["replica_result"], "replica_nodes": t["replica_nodes"],
                             "third_result": ra["result"], "third_expansion": ra["expansion"],
                             "third_ttHits": ra["ttHits"], "agree": True})
            exp_total += ra["expansion"]
            gate(f"target-{k}-verdict-agree", True, f"third={ra['result']} replica={t['replica_result']}")
        elif ra["reason"].startswith("runlimit"):
            inconclusive.append({"key_id": k, "reason": ra["reason"]})
            gate(f"target-{k}-verdict-agree", False, f"WALL-INCONCLUSIVE {ra['reason']} (not a verdict)")
        else:
            verdicts.append({"key_id": k, "source": t.get("source"), "budget": t["budget"],
                             "replica_result": t["replica_result"], "replica_nodes": t["replica_nodes"],
                             "third_result": ra["result"], "third_expansion": ra["expansion"],
                             "third_ttHits": ra["ttHits"], "agree": ra["result"] == t["replica_result"]})
            gate(f"target-{k}-verdict-agree", ra["result"] == t["replica_result"] and ra["reason"] == "clean",
                 f"DIVERGENCE third=({ra['result']},{ra['reason']}) replica={t['replica_result']}")

    # -- G6 (declared): unadopted-row corroboration against the Part EE
    #    publications. Each target row cross-verified above must be
    #    byte-identically the published raw row (pinned), and its exact
    #    would-be canonical s5verdict row must be ABSENT from the current
    #    canonical merged cache (fc3e4ac9, 6,666 rows) with NO conflicting
    #    same-(lo,hi) row; the adopted af034 row must occur EXACTLY ONCE
    #    (positive control); the target key ids must appear in NO adopted /
    #    win / probed id list of the EE increments-manifest (af029 is
    #    DECLARED to legitimately appear in batches[0].anchor_ids as Part EA
    #    anchor provenance, which is not an adoption list).
    for t in rows["targets"]:
        k = t["key_id"]
        for p in ("p1", "p2"):
            sp = os.path.join(ROOT, "sources", SRC_DIR[k], f"{k}.{p}.out")
            gate(f"unadopted-pin-raw-{k}-{p}", sha256(sp) == PIN_RAW[k + "." + p], sha256(sp))
        row_would_be = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        merged_path = os.path.join(ROOT, "sources", "ee-merged-exact-s5-chain-plus-af034loss1-20261125.cache")
        gate(f"unadopted-pin-merged-cache-{k}", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
        s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
        gate(f"unadopted-merged-cache-rowcount-{k}", len(s5rows) == 6666, f"{len(s5rows)} s5verdict rows")
        hits = [l for l in s5rows if l == row_would_be]
        gate(f"unadopted-merged-cache-row-absent-{k}", len(hits) == 0,
             f"{row_would_be} occurs {len(hits)} times (expect 0: the WIN row was never adopted)")
        conflicts = [l for l in s5rows if l.startswith(f"s5verdict,{t['lo']},{t['hi']},")]
        gate(f"unadopted-merged-cache-no-key-row-{k}", not conflicts, str(conflicts))
    # af029 30M anchor-pair raw pins + af001 anchor provenance pins
    for k in ("af029-30m", "af001"):
        srcname = RAW_SRC_NAME.get(k, k)
        for p in ("p1", "p2"):
            sp = os.path.join(ROOT, "sources", SRC_DIR[k], f"{srcname}.{p}.out")
            gate(f"extra-pin-raw-{k}-{p}", sha256(sp) == PIN_RAW[k + "." + p], sha256(sp))
    # shared Part EE source pins + battery (fail-closed)
    merged_path = os.path.join(ROOT, "sources", "ee-merged-exact-s5-chain-plus-af034loss1-20261125.cache")
    inc_path = os.path.join(ROOT, "sources", "ee-increment-af034loss1-20261125.cache")
    man_path = os.path.join(ROOT, "sources", "ee-increments-manifest.json")
    gate("unadopted-pin-merged-cache-shared", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
    gate("unadopted-pin-increment-shared", sha256(inc_path) == PIN_INCREMENT, sha256(inc_path))
    s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
    wins = sum(1 for l in s5rows if l.split(",")[4] == "1")
    losses = sum(1 for l in s5rows if l.split(",")[4] == "2")
    gate("unadopted-merged-cache-counts", len(s5rows) == 6666 and wins == 158 and losses == 6508,
         f"rows={len(s5rows)} WIN={wins} LOSS={losses}")
    gate("unadopted-merged-cache-af034-positive-control",
         sum(1 for l in s5rows if l == AF034_ADOPTED_ROW) == 1,
         "the adopted af034 60M LOSS row must occur exactly once (absence gates cannot pass vacuously)")
    inc_rows = [l for l in open(inc_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("unadopted-increment-exact-1-row", inc_rows == [AF034_ADOPTED_ROW], str(inc_rows))
    im = json.load(open(man_path))
    gate("unadopted-pin-increments-manifest-shared", sha256(man_path) == PIN_INCR_MANIFEST, sha256(man_path))
    gate("unadopted-manifest-schema", im.get("schema") == "af034loss1-increments-manifest-v1", im.get("schema"))
    gate("unadopted-manifest-ids", im.get("loss_ids") == ["af034"] and im.get("resolved_ids") == ["af034"],
         str(im.get("loss_ids")))
    gate("unadopted-manifest-flags",
         im.get("full_packet_eq_loss_only") is True
         and im.get("win_scenario_exists") is False
         and im.get("unadopted_win_ids") == [] and im.get("win_ids") == []
         and im.get("merger_sha256") == PIN_MERGER
         and im.get("base_cache_sha256") == PIN_MERGED_BASE
         and int(im.get("base_cache_rows", -1)) == 6665
         and int(im.get("quarantine_hits", -1)) == 0,
         f"full_eq_loss={im.get('full_packet_eq_loss_only')} base={im.get('base_cache_rows')} quarantine={im.get('quarantine_hits')}")
    rcm = im.get("row_counts", {})
    gate("unadopted-manifest-row-counts",
         int(rcm.get("adopted_loss_rows", -1)) == 1 and int(rcm.get("wins_unconsumed", -1)) == 0
         and int(rcm.get("exhausted_excluded", -1)) == 0 and int(rcm.get("prior_adopted_loss_rows_base", -1)) == 2,
         f"row_counts={rcm}")
    note = im.get("win_scenario_note", "")
    for t in rows["targets"]:
        gate(f"unadopted-manifest-note-names-{t['key_id']}", t["key_id"] in note,
             "the EE manifest win_scenario_note must name the pooled unconsumed WIN child")
    b = im.get("batches", [{}])[0]
    gate("unadopted-manifest-batch-adopted", b.get("adopted_loss_ids") == ["af034"], str(b.get("adopted_loss_ids")))
    # machine scan over every id LIST in the manifest; af029's DECLARED
    # presence in anchor_ids is provenance, not adoption
    adopted_ids = set()
    for fld in ("loss_ids", "win_ids", "unadopted_win_ids", "resolved_ids"):
        adopted_ids |= set(im.get(fld) or [])
    for bb in im.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "unadopted_win_ids", "fragment_ids", "probed_ids"):
            adopted_ids |= set(bb.get(fld) or [])
    for t in rows["targets"]:
        gate(f"unadopted-manifest-target-not-in-adopted-lists-{t['key_id']}", t["key_id"] not in adopted_ids,
             f"{t['key_id']} must not appear in any adopted/win/probed id list of the increments-manifest")

    # -- G7 (declared, as in Part CZ/CM/CR/CW): val-gate this-host 4/4 node-exact vs
    #    the published baselines (all replay fields except wall_s; replay_done +
    #    quads header presence both required)
    for vgkey, vgbudget in VALGATE_KEYS:
        base_path = os.path.join(ROOT, "val-gate", f"{vgkey}.published-baseline.out")
        host_path = os.path.join(ROOT, "val-gate", f"{vgkey}.eg-host.out")
        b, bd, _ = parse_replay_out(base_path)
        h, hd, hq = parse_replay_out(host_path)
        gate(f"valgate-{vgkey}-present", b is not None and h is not None and bd and hd and hq,
             f"baseline={b is not None} host={h is not None}")
        if not (b and h):
            continue
        ok = all(b[i] == h[i] for i in (1, 2, 3, 4, 5, 6, 7, 9, 10))
        gate(f"valgate-{vgkey}-node-exact", ok, f"host={h[5:8]} baseline={b[5:8]}")

    n_win = sum(1 for v in verdicts if v["replica_result"] == 1)
    n_agree = sum(1 for v in verdicts if v["agree"])
    summary = {"schema": SCHEMA,
               "experiment": EXP,
               "all_pass": all(g["pass"] for g in gates),
               "gate_count": len(gates),
               "targets_pass_one_total_third_expansions": exp_total,
               "verdict_agreements": verdicts,
               "wall_inconclusive": inconclusive,
               "gates": gates}
    with open(os.path.join(ROOT, "output", "audit-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1); fh.write("\n")
    print(f"ALL {len(gates)} GATES PASS; verdict agreements {n_agree}/{len(verdicts)} "
          f"(WIN={n_win}); inconclusive={len(inconclusive)}; total third-impl expansions pass-one={exp_total}")

if __name__ == "__main__":
    main()
