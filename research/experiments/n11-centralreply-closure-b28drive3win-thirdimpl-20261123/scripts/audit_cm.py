# audit_cm.py -- fail-closed gate battery for the Part CM third-implementation
# cross-verification of the two published batch-28 (class 5343) drive-3 WIN-HALT
# rows aa008 and aa009 (unconsumed closure WIN candidates 34/35), including the
# declared this-host pinned-replica 2-pass reproductions. Every gate must PASS
# or the script exits rc=1 with the gate name. Reads only local artifacts under
# this experiment dir; writes output/audit-summary.json.
#
# Adapted from the published Part CL audit_ck.py (sha256
# edf0ae7c18e4d67d0fbd6734bfb56f5feb6e1793069c02ba17289afd0d8668d4,
# experiment n11-centralreply-closure-b28drive2loss-thirdimpl-20261123, itself
# from the published Part CC audit.py b7cfb0ce... / BY 7f7fa3d1... / BX
# 19351ab5... b25win / BW 3a2ce7ef... b24win / BV 08bdebce... b23win).
# Deltas (all declared in the Part CM declaration before execution):
# EXP/SCHEMA/rows-schema strings, the Part CJ drive-3 class-5343 wording, the
# target-count gate detail (2 b28 drive-3 WIN-HALT rows), the pinned raw-out
# sha pins for aa008/aa009 p1/p2, and the NEW gate block G6 (unadopted-WIN-row
# corroboration: the two cross-verified WIN rows must be byte-identically the
# published Part CJ drive-3 raw rows and must NOT appear anywhere in the
# Part CH adopted canonical cache / increment / increments-manifest; pinned
# merged-cache/increment/increments-manifest sources) and G7 (val-gate
# this-host 4/4 node-exact vs the published baselines, wall_s excluded).
# The G0-G5 gate logic is unchanged from the published Part CL/CC machine.
# Verdicts are NOT consumed: aa008/aa009 are honest WIN labels pending the
# scrutiny owner C++ second-implementation gate pin 9193f5b6; nothing is
# adopted, freed, closed, or claimed. The standard 11x11 empty board, the 19
# central-reply roots, class 5343 and every batch-28 key stay UNKNOWN.
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-closure-b28drive3win-thirdimpl-20261123"
SCHEMA = "n11-centralreply-closure-b28drive3win-thirdimpl-audit-v1"
ROWS_SCHEMA = "n11-centralreply-closure-b28drive3win-thirdimpl-input-v1"

PIN_THIRD = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
PIN_VERIFYTBL = "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"
PIN_JSREPLAY = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
PIN_MERGED_CANONICAL = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
PIN_INCREMENT = "dc857bfd2ecd00deaea3dbe214e0eec0e5b9d7704104a8721d046f262f170487"
PIN_INCR_MANIFEST = "017c7c3036927ddc8107258029d6a89318d04d5923103d7b8ae97952225aaa71"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
PIN_RAW_CM = {
    "aa008.p1": "f87c2ae9968b17b443b222921fbf2c0d57630792fe55675eeeb941e319759e84",
    "aa008.p2": "5546ed29d5af5dc499e107656f61c44ee73f3a924568dcbf3b04e9fe3572a9ba",
    "aa009.p1": "50c32fd5e354f2242119b8d034b50ca045f9d51b55b3dfff813fb49b1e83b3b8",
    "aa009.p2": "d79fc6d870ef6c561778854694b6f319d7f0c5985a920ecd3bc1b246d7399381",
}

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
    # third,<row>,<stones>,<legalIn>,<legalDerived>,<result>,<expansion>,<ttHits>,<wallS>,<lo>,<hi>,<reason>,quads=...,ttOverwrites=...,memoPower=...
    if not line.startswith("third,"):
        return None
    f = line.rstrip("\n").split(",")
    d = {"raw": line.rstrip("\n")}
    d["stub"] = f[0]
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
    return d

def read_run(kind, key, tag):
    p = os.path.join(ROOT, "output", kind, f"{key}.{tag}.out")
    if not os.path.isfile(p):
        return None
    with open(p) as fh:
        for line in fh:
            if line.startswith("third,"):
                return parse_third_line(line)
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
         and rows.get("canonical_cache_sha256_unchanged") == PIN_MERGED_CANONICAL,
         rows.get("schema"))
    gate("target-count", len(rows["targets"]) == 2,
         f"{len(rows['targets'])} (2 b28 drive-3 WIN-HALT rows)")

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
    #        Part CJ drive-3 raw fields (result 1 nodes = replica_nodes).
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
        gate(f"replica-{k}-schema", f1[2] == "5" and f1[1] == "0" and f1[5] == "15000000",
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

    # -- G5: targets: 2-run determinism + verdict agreement with the published WIN-HALT rows
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

    # -- G6 (NEW, declared): unadopted-WIN-row corroboration. The two rows
    #    cross-verified above must be byte-identically the published Part CJ
    #    drive-3 raw rows (pinned) and must NOT appear anywhere in the Part CH
    #    adopted canonical cache / increment / increments-manifest. Verdicts
    #    never consumed: canonical cache 3124461b unchanged.
    for t_idx, t in enumerate(rows["targets"]):
        k = t["key_id"]
        gate(f"unadopted-pin-raw-{k}-p1", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")) == PIN_RAW_CM[k + ".p1"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")))
        gate(f"unadopted-pin-raw-{k}-p2", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")) == PIN_RAW_CM[k + ".p2"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")))
        win_row = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        merged_path = os.path.join(ROOT, "sources", "canonical-cache-ch-merged-b28loss1.cache")
        gate(f"unadopted-pin-merged-cache-{k}", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
        inc_path = os.path.join(ROOT, "sources", "increment-b28loss1.cache")
        gate(f"unadopted-pin-increment-{k}", sha256(inc_path) == PIN_INCREMENT, sha256(inc_path))
        man_path = os.path.join(ROOT, "sources", "increments-manifest-ch.json")
        gate(f"unadopted-pin-increments-manifest-{k}", sha256(man_path) == PIN_INCR_MANIFEST, sha256(man_path))
        s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
        gate(f"unadopted-merged-cache-rowcount-{k}", len(s5rows) == 6294, f"{len(s5rows)} s5verdict rows")
        hits = [l for l in s5rows if l == win_row]
        gate(f"unadopted-merged-cache-row-absent-{k}", len(hits) == 0,
             f"{win_row} occurs {len(hits)} times (expect 0: WIN row never adopted)")
        conflicts = [l for l in s5rows if l.startswith(f"s5verdict,{t['lo']},{t['hi']},")]
        gate(f"unadopted-merged-cache-no-key-row-{k}", not conflicts, str(conflicts))
        inc_rows = [l for l in open(inc_path).read().splitlines() if l.startswith("s5verdict,")]
        gate(f"unadopted-increment-single-aa003-row-{k}",
             inc_rows == ["s5verdict,1152921504741064704,4228,5,2,4070373"], str(inc_rows))
        im = json.load(open(man_path))
        gate(f"unadopted-manifest-loss-ids-{k}", im.get("loss_ids") == ["aa003"], str(im.get("loss_ids")))
        gate(f"unadopted-manifest-flags-{k}",
             im.get("full_packet_eq_loss_only") is False
             and im.get("merger_sha256") == PIN_MERGER
             and int(im.get("base_cache_rows", -1)) == 6293
             and int(im.get("base_cache_absent_hits", -1)) == 0
             and int(im.get("quarantine_hits", -1)) == 0,
             f"full_eq_loss={im.get('full_packet_eq_loss_only')} base={im.get('base_cache_rows')} quarantine={im.get('quarantine_hits')}")
        gate(f"unadopted-manifest-wins-untouched-{k}",
             im.get("batches", [{}])[0].get("unadopted_win_ids") == ["aa001", "aa002", "aa006", "aa007"]
             and int(im.get("row_counts", {}).get("wins", -1)) == 4
             and int(im.get("row_counts", {}).get("fileless_unprobed", -1)) == 47,
             "Part CH manifest pre-dates drive-3: aa008/aa009 untouched")
        # machine scan over every id LIST in the manifest (NOT raw text scan:
        # the manifest prose legitimately mentions the pre-drive-3 fileless
        # range "aa008..aa054" in fragment_rows_note, no id-list entry)
        man_ids = set()
        for fld in ("loss_ids", "win_ids", "unadopted_win_ids", "exhausted_excluded_ids", "resolved_ids"):
            v = im.get(fld) or []
            man_ids |= set(v)
        for b in im.get("batches", []):
            for fld in ("adopted_loss_ids", "unadopted_win_ids", "exhausted_excluded_ids", "fragment_ids", "probed_ids"):
                v = b.get(fld) or []
                man_ids |= set(v)
        for uwr in im.get("unadopted_win_rows") or []:
            if isinstance(uwr, dict) and "key_id" in uwr:
                man_ids.add(uwr["key_id"])
        gate(f"unadopted-manifest-target-absent-{k}", k not in man_ids,
             f"{k} must not appear in any id list of the increments-manifest")

    # -- G7 (declared, as in Part CL): val-gate this-host 4/4 node-exact vs the
    #    published baselines (all replay fields except wall_s; replay_done +
    #    quads header presence both required)
    for vgkey, vgbudget in VALGATE_KEYS:
        base_path = os.path.join(ROOT, "val-gate", f"{vgkey}.published-baseline.out")
        host_path = os.path.join(ROOT, "val-gate", f"{vgkey}.cm-host.out")
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
