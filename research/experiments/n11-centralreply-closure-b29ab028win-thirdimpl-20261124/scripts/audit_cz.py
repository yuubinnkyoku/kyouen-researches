# audit_cz.py -- fail-closed gate battery for the Part CZ third-implementation
# cross-verification of the ONE published batch-29 (closure class 2251)
# Part CI takeover drive-2 WIN row ab028 (nodes 3,167,121) -- an UNCONSUMED
# honest label, including the declared this-host pinned-replica 2-pass
# reproductions. Every gate must PASS or the script exits rc=1 with the gate
# name. Reads only local artifacts under this experiment dir; writes
# output/audit-summary.json.
#
# Adapted from the published Part CW audit (audit_cw.py, sha256
# a7876a0a4232a144eebf396ff7b752f7324fdc4b937b030770aa8687654f3a8f,
# experiment n11-centralreply-closure-b28cqwin2-thirdimpl-20261124, itself
# from the published Part CR audit 2ab974c3.. / CM audit_cm.py 3f9a29fa.. /
# CL audit_ck.py edf0ae7c.. / CC audit.py b7cfb0ce.. / BY 7f7fa3d1 / BX
# 19351ab5 / BW 3a2ce7ef / BV 08bdebce). Declared deltas (all in the Part CZ
# declaration before execution): EXP/SCHEMA/rows-schema strings, the batch-29
# drive-2 WIN-row wording, the replica budget gate 20000000 -> 15000000 (the
# declared batch-29 probe condition), the pinned raw-out sha pins for
# ab028 p1/p2, the unadopted-corroboration source pins switched from the
# Part CO publications to the Part CU 16-LOSS adoption publications (merged
# canonical cache 30ddad9d.. 6,317 rows = CO base 854800f3 6,301 + 16
# adopted drive-1 LOSS rows; increment bab011e3..; increments-manifest
# f9f58ee1..), and the G6 id-list battery adapted for the CU-time fileless
# UNPROBED status of the target: ab028 LEGITIMATELY appears ONLY in the CU
# manifest's batches[0].fileless_unprobed_ids roster (38 keys) and must be
# absent from EVERY adopted/win/probed id list. Verdicts are NOT consumed:
# ab028 is an honest label pending the scrutiny owner C++ second-
# implementation gate pin 9193f5b6; nothing is adopted, freed, closed, or
# claimed. The standard 11x11 empty board, the central-reply roots, class
# 2251 and every batch-29 key stay UNKNOWN.
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-closure-b29ab028win-thirdimpl-20261124"
SCHEMA = "n11-centralreply-closure-b29ab028win-thirdimpl-audit-v1"
ROWS_SCHEMA = "n11-centralreply-closure-b29ab028win-thirdimpl-input-v1"

PIN_THIRD = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
PIN_VERIFYTBL = "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"
PIN_JSREPLAY = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
PIN_MERGED_CANONICAL = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"
PIN_INCREMENT = "bab011e376090f9f4732d63f0084f326ba72dada5cf699d5aabc7e014c29ae24"
PIN_INCR_MANIFEST = "f9f58ee101d53f0598ee01c5c54d5b277797a9e882cfb478ab7f7b3010e191e0"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
PIN_MERGED_BASE = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_STATUS_DRIVE1_PREFIX = "6b877344b9abea348a9b221f587a771857d3c4091f88fa460ef12595722183e2"
PIN_RAW_CZ = {
    # machine-pinned from the published batch-29 drive-2 final outputs (fetch-verified)
    "ab028.p1": "af6e6fe493762099a07d0a598471485e3ea1f9cc97f689fb194411192600b5f5",
    "ab028.p2": "77a4736424049fcedb630c53bd84a2e80d16c50aabd9263f444a2673797e5f02",
}
PIN_LOSS_IDS = [f"ab{i:03d}" for i in range(1, 17)]
PIN_ADOPTED_HEADER = "ADOPTED set = ab001..ab016"
PIN_STATUS_ROWS_JSON = "d8c53d294d5a95b1c5547da48c6197054f1819f22a5f2d5f3d18b6d19e3ee8d1"

VALGATE_KEYS = [("at2m-s5-1152921504606851072-536870946", 2000000),
                ("at2m-s5-1188950301626860544-536870912", 2000000),
                ("first-15m-s5-1152921504606851072-536870946", 15000000),
                ("second-15m-s5-1188950301626860544-536870912", 15000000)]

REPLICA_BUDGET = "15000000"

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
    # third,<row>,<stones>,<legalIn>,<legalDerived>,<result>,<expansion>,<ttHits>,<wallS>,<lo>,<hi>,<reason>,quads=...,ttOverwrites=...,memoPower=...
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
        # malformed winner/gate line: fail closed as a named condition, never a silent PASS
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
                # a GATE_FAIL/malformed line in a target/anchor run is NOT a
                # result: treat as absent so the present gate fails closed
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
    gate("pin-verify_tbl.js",
         sha256(os.path.join(ROOT, "scripts", "verify_tbl.js")) == PIN_VERIFYTBL,
         sha256(os.path.join(ROOT, "scripts", "verify_tbl.js")))
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
    gate("target-count", len(rows["targets"]) == 1,
         f"{len(rows['targets'])} (1 b29 drive-2 WIN row)")
    gate("target-verdict-kinds",
         sorted(t["expect_third"] for t in rows["targets"]) == [1],
         f"{sorted(t['expect_third'] for t in rows['targets'])}")

    # -- G2: rules-engine gate output (verify_tbl run, captured in output/rules-gate.txt)
    p = os.path.join(ROOT, "output", "rules-gate.txt")
    if not os.path.isfile(p):
        gate("rules-gate-present", False, "missing output/rules-gate.txt")
    txt = open(p).read()
    gate("rules-gate-quads", "replica quads 95670 mine quads 95670" in txt, txt.splitlines()[0] if txt else "")
    ok_mis = ("mismatches 0" in txt)
    gate("rules-gate-tbl-mismatch0", ok_mis, [l for l in txt.splitlines() if l.startswith("triples")])

    # -- G2b: declared this-host pinned-replica reproduction (fresh-cold 2-pass):
    #        determinism fields p1==p2 AND exact match with the published
    #        batch-29 drive-2 raw fields (result/nodes = replica_nodes).
    for t in rows["targets"]:
        k = t["key_id"]
        f1, d1, q1 = parse_replay_out(os.path.join(ROOT, "output", "replica", f"{k}.p1.out"))
        f2, d2, q2 = parse_replay_out(os.path.join(ROOT, "output", "replica", f"{k}.p2.out"))
        gate(f"replica-{k}-present", f1 is not None and f2 is not None, "p1/p2")
        if not (f1 and f2):
            continue
        gate(f"replica-{k}-done", d1 and d2, f"replay_done p1={d1} p2={d2}")
        gate(f"replica-{k}-quads", q1 and q2, f"quads-header p1={q1} p2={q2}")
        # determinism fields: legal,is_or,budget,result,nodes,key_lo,key_hi (wall_s excluded)
        det_ok = all(f1[i] == f2[i] for i in (3, 4, 5, 6, 7, 9, 10))
        gate(f"replica-{k}-det-pair", det_ok,
             f"p1={f1[3:8]} p2={f2[3:8]}")
        gate(f"replica-{k}-schema", f1[2] == "5" and f1[1] == "0" and f1[5] == REPLICA_BUDGET,
             f"schema {f1[:6]}")
        gate(f"replica-{k}-key", int(f1[9]) == t["lo"] and int(f1[10]) == t["hi"] and int(f1[3]) == t["legal"],
             f"{f1[9]},{f1[10]},{f1[3]} vs {t['lo']},{t['hi']},{t['legal']}")
        gate(f"replica-{k}-verdict-vs-published",
             int(f1[6]) == t["replica_result"] and int(f1[7]) == t["replica_nodes"],
             f"this-host result={f1[6]} nodes={f1[7]} vs published result={t['replica_result']} nodes={t['replica_nodes']}")

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
    gate("neg-ng1-failclosed", ng1 is not None and "gate_fail" in ng1 and "legal count mismatch" in ng1["gate_fail"],
         str(ng1))
    ng2 = read_run("negative", "ng2", "a")
    gate("neg-ng2-failclosed", ng2 is not None and "gate_fail" in ng2 and "stone count mismatch" in ng2["gate_fail"],
         str(ng2))

    # -- G5: target: 2-run determinism + verdict agreement with the published drive-2 row
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
            verdicts.append({"key_id": k, "source": t.get("source"), "replica_result": t["replica_result"],
                             "replica_nodes": t["replica_nodes"], "third_result": ra["result"],
                             "third_expansion": ra["expansion"], "third_ttHits": ra["ttHits"], "agree": True})
            exp_total += ra["expansion"]
            gate(f"target-{k}-verdict-agree", True, f"third={ra['result']} replica={t['replica_result']}")
        elif ra["reason"].startswith("runlimit"):
            # honest wall-inconclusive: recorded, NOT a verdict
            inconclusive.append({"key_id": k, "reason": ra["reason"]})
            gate(f"target-{k}-verdict-agree", False, f"WALL-INCONCLUSIVE {ra['reason']} (not a verdict)")
        else:
            # clean third-impl verdict differing from the replica expectation:
            # divergence evidence, fail the agree gate and record it
            verdicts.append({"key_id": k, "source": t.get("source"), "replica_result": t["replica_result"],
                             "replica_nodes": t["replica_nodes"], "third_result": ra["result"],
                             "third_expansion": ra["expansion"], "third_ttHits": ra["ttHits"], "agree": ra["result"] == t["replica_result"]})
            gate(f"target-{k}-verdict-agree", ra["result"] == t["replica_result"] and ra["reason"] == "clean",
                 f"DIVERGENCE third=({ra['result']},{ra['reason']}) replica={t['replica_result']}")

    # -- G6 (declared): unadopted-row corroboration. The row cross-verified
    #    above must be byte-identically the published batch-29 drive-2 raw row
    #    (pinned) and must NOT appear anywhere in the Part CU adopted
    #    canonical cache / increment, and in the increments-manifest ONLY in
    #    the batches[0].fileless_unprobed_ids roster (its CU-time UNPROBED
    #    status) -- never in any adopted/win/probed id list. Verdicts never
    #    consumed: canonical cache 30ddad9d unchanged (6,317 rows).
    for t in rows["targets"]:
        k = t["key_id"]
        gate(f"unadopted-pin-raw-{k}-p1", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")) == PIN_RAW_CZ[k + ".p1"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")))
        gate(f"unadopted-pin-raw-{k}-p2", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")) == PIN_RAW_CZ[k + ".p2"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")))
        row_would_be = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        merged_path = os.path.join(ROOT, "sources", "merged-cache-cu-b29loss16.cache")
        gate(f"unadopted-pin-merged-cache-{k}", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
        s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
        gate(f"unadopted-merged-cache-rowcount-{k}", len(s5rows) == 6317, f"{len(s5rows)} s5verdict rows")
        hits = [l for l in s5rows if l == row_would_be]
        gate(f"unadopted-merged-cache-row-absent-{k}", len(hits) == 0,
             f"{row_would_be} occurs {len(hits)} times (expect 0: the drive-2 WIN row was never adopted)")
        conflicts = [l for l in s5rows if l.startswith(f"s5verdict,{t['lo']},{t['hi']},")]
        gate(f"unadopted-merged-cache-no-key-row-{k}", not conflicts, str(conflicts))
    # shared Part CU source pins + battery (fail-closed)
    merged_path = os.path.join(ROOT, "sources", "merged-cache-cu-b29loss16.cache")
    inc_path = os.path.join(ROOT, "sources", "increment-b29loss16.cache")
    man_path = os.path.join(ROOT, "sources", "increments-manifest-cu.json")
    gate("unadopted-pin-merged-cache-shared", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
    gate("unadopted-pin-increment-shared", sha256(inc_path) == PIN_INCREMENT, sha256(inc_path))
    inc_rows = [l for l in open(inc_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("unadopted-increment-exact-16-rows", len(inc_rows) == 16, f"{len(inc_rows)} rows")
    gate("unadopted-increment-adopted-set-header",
         PIN_ADOPTED_HEADER in open(inc_path).read(),
         "Part CU increment ADOPTED set statement")
    im = json.load(open(man_path))
    gate("unadopted-pin-increments-manifest-shared", sha256(man_path) == PIN_INCR_MANIFEST, sha256(man_path))
    gate("unadopted-manifest-schema", im.get("schema") == "b29loss16-increments-manifest-v1", im.get("schema"))
    gate("unadopted-manifest-loss-ids", im.get("loss_ids") == PIN_LOSS_IDS, str(im.get("loss_ids"))[:80])
    gate("unadopted-manifest-flags",
         im.get("full_packet_eq_loss_only") is True
         and im.get("win_scenario_exists") is False
         and im.get("merger_sha256") == PIN_MERGER
         and im.get("base_cache_sha256") == PIN_MERGED_BASE
         and int(im.get("base_cache_rows", -1)) == 6301
         and int(im.get("base_cache_absent_hits_for_emitted", -1)) == 0
         and int(im.get("quarantine_hits", -1)) == 0,
         f"full_eq_loss={im.get('full_packet_eq_loss_only')} base={im.get('base_cache_rows')} quarantine={im.get('quarantine_hits')}")
    rcm = im.get("row_counts", {})
    gate("unadopted-manifest-row-counts",
         int(rcm.get("probed_rows", -1)) == 16 and int(rcm.get("adopted_loss_rows", -1)) == 16
         and int(rcm.get("wins", -1)) == 0 and int(rcm.get("exhausted_excluded", -1)) == 0
         and int(rcm.get("fragments_unprobed", -1)) == 0 and int(rcm.get("fileless_unprobed", -1)) == 38,
         f"row_counts={rcm}")
    b = im.get("batches", [{}])[0]
    gate("unadopted-manifest-status-prefix-pin",
         b.get("status_log_sha256") == PIN_STATUS_DRIVE1_PREFIX and int(b.get("status_log_lines", -1)) == 16,
         str(b.get("status_log_sha256"))[:24])
    # machine scan over every id LIST in the manifest (NOT raw text scan),
    # split into adopted/win/probed lists (must NOT contain the target) and
    # the CU-time fileless_unprobed_ids roster (MUST contain the target)
    adopted_ids = set()
    for fld in ("loss_ids", "win_ids", "unadopted_win_ids", "resolved_ids"):
        adopted_ids |= set(im.get(fld) or [])
    for bb in im.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "unadopted_win_ids", "fragment_ids", "probed_ids"):
            adopted_ids |= set(bb.get(fld) or [])
    for uwr in im.get("unadopted_win_rows") or []:
        if isinstance(uwr, dict) and "key_id" in uwr:
            adopted_ids.add(uwr["key_id"])
    fileless_ids = set(b.get("fileless_unprobed_ids") or [])
    gate("unadopted-manifest-fileless-roster",
         len(fileless_ids) == 38 and int(b.get("fileless_unprobed_count", -1)) == 38,
         f"fileless roster size {len(fileless_ids)}")
    for t in rows["targets"]:
        gate(f"unadopted-manifest-target-not-in-adopted-lists-{t['key_id']}", t["key_id"] not in adopted_ids,
             f"{t['key_id']} must not appear in any adopted/win/probed id list of the increments-manifest")
        gate(f"unadopted-manifest-target-in-fileless-roster-{t['key_id']}", t["key_id"] in fileless_ids,
             f"{t['key_id']} must appear in the CU-time fileless UNPROBED roster (batches[0].fileless_unprobed_ids)")

    # -- G7 (declared, as in Part CM/CR/CW): val-gate this-host 4/4 node-exact vs
    #    the published baselines (all replay fields except wall_s; replay_done +
    #    quads header presence both required)
    for vgkey, vgbudget in VALGATE_KEYS:
        base_path = os.path.join(ROOT, "val-gate", f"{vgkey}.published-baseline.out")
        host_path = os.path.join(ROOT, "val-gate", f"{vgkey}.cz-host.out")
        b, bd, _ = parse_replay_out(base_path)
        h, hd, hq = parse_replay_out(host_path)
        gate(f"valgate-{vgkey}-present", b is not None and h is not None and bd and hd and hq,
             f"baseline={b is not None} host={h is not None}")
        if not (b and h):
            continue
        ok = all(b[i] == h[i] for i in (1, 2, 3, 4, 5, 6, 7, 9, 10))
        gate(f"valgate-{vgkey}-node-exact", ok,
             f"host={h[5:8]} baseline={b[5:8]}")

    n_win = sum(1 for v in verdicts if v["replica_result"] == 1)
    n_loss = sum(1 for v in verdicts if v["replica_result"] == 2)
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
    # determinism of this audit: run multiple times, outputs must be byte-identical (no timestamps read)
    print(f"ALL {len(gates)} GATES PASS; verdict agreements {n_agree}/{len(verdicts)} "
          f"(WIN={n_win} LOSS={n_loss}); inconclusive={len(inconclusive)}; "
          f"total third-impl expansions pass-one={exp_total}")

if __name__ == "__main__":
    main()
