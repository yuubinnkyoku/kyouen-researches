# audit_dh.py -- fail-closed gate battery for the Part DH third-implementation
# cross-verification of the nine published batch-28 (closure class 5343)
# P4-package WIN rows of the b28-win46 third-impl queue registry:
# aa011 (nodes 12,424,953, drive4-15m) / aa054 (13,227,570, drive5-15m) /
# aa022 (14,044,375, drive4-15m) / aa034 (14,097,048, drive5-15m) / aa037
# (14,239,714, drive5-15m) / aa032 (20,312,294, cs-25m) / aa028 (21,563,925,
# cs-25m) / aa021 (22,942,323, cs-25m) / aa050 (25,541,199, ct-30m) -- all
# UNCONSUMED honest labels, including the declared this-host pinned-replica
# 2-pass reproductions at the PER-KEY decisive probe budgets (15M x5 /
# 25M x3 / 30M x1). Every gate must PASS or the script exits rc=1 with the
# gate name. Reads only local artifacts under this experiment dir; writes
# output/audit-summary.json.
#
# Byte-descended from the published Part DG audit (audit_dg.py, sha256
# e3a1c74f..., experiment n11-centralreply-closure-b28p3win8-thirdimpl-
# 20261124, itself a DE-audit adaptation). Declared deltas (all in the
# Part DH declaration before execution): EXP/SCHEMA/rows-schema strings,
# the batch-28 P4-package (drive4/drive5 15M-probe + cs-25m/ct-30m reprobe)
# wording, the target-count gate detail (9 P4-package WIN rows, all verdict
# kind WIN), the per-key replica budget gate (aa011/aa054/aa022/aa034/aa037
# = 15,000,000; aa032/aa028/aa021 = 25,000,000; aa050 = 30,000,000 -- the
# published decisive probe conditions), the pinned raw-out sha pins for
# aa011/aa022/aa054/aa034/aa037/aa032/aa028/aa021/aa050 p1/p2 (18 files;
# aa034 p1==p2 and aa050 p1==p2 byte-identical, a published fact), the
# pin-maker gate (make_inputs_dh.py sha256 8036d0e58180dcc1ab0d436ff9da0225
# 697bebaf36f581943b4c0af37e388cad), the val-gate host-run filename suffix
# (dg-host.out -> dh-host.out), and the G6 unadopted-corroboration SPLIT
# battery: the FIVE 15M-solved targets (aa011/aa054/aa022/aa034/aa037) are
# Part CO unadopted-WIN-roster members (node-exact unadopted_win_rows,
# present in the win roster and member bookkeeping, absent from every
# adopted/loss/fragment list and from exhausted_excluded_ids), while the
# FOUR reprobe-decisive targets (aa032/aa028/aa021/aa050) are CO-time
# exhausted_excluded members (they exhausted the base 15M probe before the
# 25M/30M reprobe runs solved them; they appear NOWHERE in the CO win
# roster / unadopted_win_ids / unadopted_win_rows, and their WIN labels
# come from the published reprobe decisive logs + queue registry rev3,
# not from Part CO). All nine remain absent from both merged caches and
# both increments and appear nowhere in the batch-29-scoped Part DB
# manifest. The G0-G5, G7 gate logic is otherwise unchanged from the
# published Part DG machine. Verdicts are NOT consumed: the nine targets
# are honest labels pending the scrutiny owner C++ second-implementation
# gate pin 9193f5b6; nothing is adopted, freed, closed, or claimed. The
# standard 11x11 empty board, the central-reply roots, class 5343 and
# every batch-28 key stay UNKNOWN.
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-closure-b28p4win9-thirdimpl-20261124"
SCHEMA = "n11-centralreply-closure-b28p4win9-thirdimpl-audit-v1"
ROWS_SCHEMA = "n11-centralreply-closure-b28p4win9-thirdimpl-input-v1"

PIN_THIRD = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
PIN_VERIFYTBL = "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"
PIN_JSREPLAY = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
PIN_MERGED_CANONICAL_DB = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"
PIN_MERGED_CANONICAL_CO = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_INCREMENT_CO = "bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382"
PIN_INCREMENT_DB = "85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc"
PIN_INCR_MANIFEST_CO = "b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192"
PIN_INCR_MANIFEST_DB = "1b51f30dabed6f4df435a3a034e1b5b9c2f405c75ebdcd918c0e256f2812d25a"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
PIN_MERGED_BASE_CH = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
PIN_MERGED_BASE_CU = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"
PIN_MAKER = "8036d0e58180dcc1ab0d436ff9da0225697bebaf36f581943b4c0af37e388cad"
PIN_RAW_DH = {
    "aa011.p1": "171d63813822c074ccfea28b55818191f789cb39b19fbeda0cb5125266ca01f0",
    "aa011.p2": "9864d2b0f3487ff7ee84587cbc0c46ea1642b57e261fd492fd4c274695dcfe7f",
    "aa022.p1": "5feb035316488b9ff9f353d11ab146d52832cafa99cc316480e86442f3b0afda",
    "aa022.p2": "da703e37eff3de00e9e19d0451eca25f278323bd634bb99b04fbc89456582a7c",
    "aa054.p1": "d79d24f7763df06dfed33ef24e92ae43830ef97ef035f8a623ff825a89a3b53c",
    "aa054.p2": "997a0aae3a886f9227eae99b671f212e05ba75a87212670bb3d18ee764208a17",
    "aa034.p1": "42580df2c86f7b602880d0fe453c8fb0af3c315e2cc989a1e3df6bf2fa2d82e9",
    "aa034.p2": "42580df2c86f7b602880d0fe453c8fb0af3c315e2cc989a1e3df6bf2fa2d82e9",
    "aa037.p1": "4defd77a37554eba0692cc2ff15cf363970fdfa830dfb29871296b58bed6a045",
    "aa037.p2": "5bc188380b8d89c0dc3ca304622d21264c24a0bccc130628cdc590e2f3f89712",
    "aa021.p1": "0082e9d0621fb96ab21ebf0965d7d9fc2289601490ebb908d53b0d34deb6ecec",
    "aa021.p2": "35a98fda2355d6c83317fd49573ecbac22cfd3329109605e40d63c5096607bb3",
    "aa028.p1": "d57f3c0715a9d585853a0010f73c6c4e9504f65c5b7b7c68ddc8799f8cdf4539",
    "aa028.p2": "c41b5ab452ce85aa827d04a8d4055369f965cae553632810f6e41b92be9d8b18",
    "aa032.p1": "85a787a9d814b0e1277498af3abc65450315125cc1d4c26d3c4ed349b4560dbf",
    "aa032.p2": "312271645e1014cc5eefbc685e1eb613600c1433f31bc73e373e7dc6a0651e61",
    "aa050.p1": "aada66cf31f2f99a04433d04c237cac3e3b22a02cd5a6514c75a440073d099c8",
    "aa050.p2": "aada66cf31f2f99a04433d04c237cac3e3b22a02cd5a6514c75a440073d099c8",
}
# the exact 7 adopted batch-28 LOSS rows of the pinned Part CO increment
# (machine-pinned; battery below requires byte-exact equality)
PIN_INCREMENT_CO_ROWS = [
    "s5verdict,1152921504606912512,4228,5,2,955659",
    "s5verdict,1171516445255794688,16,5,2,10010789",
    "s5verdict,1171516445255827456,0,5,2,6152494",
    "s5verdict,1171516445259988992,0,5,2,11446358",
    "s5verdict,1171516445264183296,0,5,2,214968",
    "s5verdict,1171516513975271424,0,5,2,5000770",
    "s5verdict,1171516582694748160,0,5,2,5003631",
]
PIN_ADOPTED_SET = "aa015, aa017, aa018, aa023, aa024, aa029, aa036"
PIN_LOSS_IDS = ["aa015", "aa017", "aa018", "aa023", "aa024", "aa029", "aa036"]
PIN_EXHAUSTED_IDS = ["aa004", "aa005", "aa021", "aa028", "aa030", "aa031",
                     "aa032", "aa035", "aa047", "aa050", "aa053"]

VALGATE_KEYS = [("at2m-s5-1152921504606851072-536870946", 2000000),
                ("at2m-s5-1188950301626860544-536870912", 2000000),
                ("first-15m-s5-1152921504606851072-536870946", 15000000),
                ("second-15m-s5-1188950301626860544-536870912", 15000000)]

REPLICA_BUDGET = {
    "aa011": 15000000, "aa054": 15000000, "aa022": 15000000,
    "aa034": 15000000, "aa037": 15000000,
    "aa032": 25000000, "aa028": 25000000, "aa021": 25000000,
    "aa050": 30000000,
}
# five 15M-solved targets (Part CO win-roster members node-exact)
TIER15_KEYS = ["aa011", "aa054", "aa022", "aa034", "aa037"]
# four reprobe-decisive targets (CO-time exhausted_excluded members)
REPROBE_KEYS = ["aa032", "aa028", "aa021", "aa050"]

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
    gate("pin-maker",
         sha256(os.path.join(ROOT, "scripts", "make_inputs_dh.py")) == PIN_MAKER,
         sha256(os.path.join(ROOT, "scripts", "make_inputs_dh.py")))
    gate("rows-schema",
         rows["schema"] == ROWS_SCHEMA
         and rows.get("consumed_into_canonical_cache") is False
         and rows.get("unadopted_win_rows") is True
         and rows.get("unadopted_loss_rows") is False
         and rows.get("canonical_cache_sha256_unchanged") == PIN_MERGED_CANONICAL_DB
         and rows.get("canonical_cache_sha256_unchanged_co") == PIN_MERGED_CANONICAL_CO,
         rows.get("schema"))
    gate("target-count", len(rows["targets"]) == 9,
         f"{len(rows['targets'])} (9 b28 P4-package WIN rows)")
    gate("target-verdict-kinds",
         sorted(t["expect_third"] for t in rows["targets"]) == [1] * 9,
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
    #        decisive raw fields (result/nodes = replica_nodes) at the
    #        PER-KEY published decisive probe budget.
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
        gate(f"replica-{k}-schema", f1[2] == "5" and f1[1] == "0" and f1[5] == str(REPLICA_BUDGET[k]),
             f"schema {f1[:6]} (per-key decisive budget {REPLICA_BUDGET[k]})")
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

    # -- G5: targets: 2-run determinism + verdict agreement with the published decisive rows
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

    # -- G6 (declared): unadopted-row corroboration. The nine rows
    #    cross-verified above must be byte-identically the published
    #    decisive-probe raw rows (pinned) and must NOT appear anywhere in
    #    the current canonical chain head (Part DB merged cache, 6,354 rows)
    #    nor in the Part CO merged cache (6,301 rows), nor in either
    #    increment. In the Part CO increments-manifest the battery SPLITS
    #    (DECLARED DH adaptation): the FIVE 15M-solved targets (TIER15_KEYS)
    #    are unadopted-WIN-roster members (win_ids / unadopted_win_ids /
    #    node-exact unadopted_win_rows + member bookkeeping probed_ids /
    #    resolved_ids), while the FOUR reprobe-decisive targets
    #    (REPROBE_KEYS) are CO-time exhausted_excluded members: they appear
    #    in exhausted_excluded_ids and the member books but NOWHERE in the
    #    win roster or unadopted_win_rows (their CO-time baseline was the
    #    base 15M probe they exhausted; their WIN labels come from the
    #    published cs-25m / ct-30m reprobe decisive logs + registry rev3).
    #    No target may appear in any loss/adopted fragment list nor in the
    #    batch-29-scoped Part DB manifest text. Verdicts never consumed.
    for t in rows["targets"]:
        k = t["key_id"]
        gate(f"unadopted-pin-raw-{k}-p1", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")) == PIN_RAW_DH[k + ".p1"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")))
        gate(f"unadopted-pin-raw-{k}-p2", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")) == PIN_RAW_DH[k + ".p2"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")))
        row_would_be = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        for cache_file, pin, nrows, label in (
                ("canonical-cache-co-merged-b28loss7.cache", PIN_MERGED_CANONICAL_CO, 6301, "co"),
                ("canonical-cache-db-merged-b29loss37.cache", PIN_MERGED_CANONICAL_DB, 6354, "db")):
            merged_path = os.path.join(ROOT, "sources", cache_file)
            gate(f"unadopted-pin-merged-cache-{label}-{k}", sha256(merged_path) == pin, sha256(merged_path))
            s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
            gate(f"unadopted-merged-cache-{label}-rowcount-{k}", len(s5rows) == nrows, f"{len(s5rows)} s5verdict rows")
            hits = [l for l in s5rows if l == row_would_be]
            gate(f"unadopted-merged-cache-{label}-row-absent-{k}", len(hits) == 0,
                 f"{row_would_be} occurs {len(hits)} times (expect 0: P4 WIN rows never adopted)")
            conflicts = [l for l in s5rows if l.startswith(f"s5verdict,{t['lo']},{t['hi']},")]
            gate(f"unadopted-merged-cache-{label}-no-key-row-{k}", not conflicts, str(conflicts))
    # shared source pins + batteries (fail-closed)
    inc_path = os.path.join(ROOT, "sources", "increment-b28loss7.cache")
    incdb_path = os.path.join(ROOT, "sources", "increment-b29loss37.cache")
    man_path = os.path.join(ROOT, "sources", "increments-manifest-co.json")
    mandb_path = os.path.join(ROOT, "sources", "increments-manifest-db.json")
    gate("unadopted-pin-increment-shared", sha256(inc_path) == PIN_INCREMENT_CO, sha256(inc_path))
    inc_rows = [l for l in open(inc_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("unadopted-increment-exact-7-rows", inc_rows == PIN_INCREMENT_CO_ROWS, str(inc_rows[:2]))
    gate("unadopted-pin-increment-db-shared", sha256(incdb_path) == PIN_INCREMENT_DB, sha256(incdb_path))
    incdb_rows = [l for l in open(incdb_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("unadopted-increment-db-37-rows", len(incdb_rows) == 37, f"{len(incdb_rows)}")
    gate("unadopted-increment-adopted-set-header",
         f"ADOPTED set = {{{PIN_ADOPTED_SET}}}" in open(inc_path).read(),
         "Part CO increment ADOPTED set statement")
    im = json.load(open(man_path))
    gate("unadopted-pin-increments-manifest-shared", sha256(man_path) == PIN_INCR_MANIFEST_CO, sha256(man_path))
    gate("unadopted-manifest-schema", im.get("schema") == "b28loss7-increments-manifest-v1", im.get("schema"))
    gate("unadopted-manifest-loss-ids", im.get("loss_ids") == PIN_LOSS_IDS, str(im.get("loss_ids")))
    gate("unadopted-manifest-flags",
         im.get("full_packet_eq_loss_only") is False
         and im.get("win_scenario_exists") is True
         and im.get("merger_sha256") == PIN_MERGER
         and im.get("base_cache_sha256") == PIN_MERGED_BASE_CH
         and int(im.get("base_cache_rows", -1)) == 6294
         and int(im.get("base_cache_absent_hits_for_emitted", -1)) == 0
         and int(im.get("quarantine_hits", -1)) == 0,
         f"full_eq_loss={im.get('full_packet_eq_loss_only')} base={im.get('base_cache_rows')} quarantine={im.get('quarantine_hits')}")
    rcm = im.get("row_counts", {})
    gate("unadopted-manifest-row-counts",
         int(rcm.get("probed_rows", -1)) == 54 and int(rcm.get("adopted_loss_rows", -1)) == 7
         and int(rcm.get("wins", -1)) == 35 and int(rcm.get("exhausted_excluded", -1)) == 11
         and int(rcm.get("fragments_unprobed", -1)) == 0 and int(rcm.get("fileless_unprobed", -1)) == 0,
         f"row_counts={rcm}")
    gate("unadopted-manifest-aa003-not-reemitted",
         im.get("aa003_base_consistency", {}).get("re_emitted") is False,
         str(im.get("aa003_base_consistency", {}).get("re_emitted")))
    # machine scan over the id LISTS in the CO manifest, split into
    # adopted/loss/fragment lists (must NOT contain the targets), the win
    # roster + member-bookkeeping lists, and the CO-time exhausted roster
    # (DECLARED DH adaptation: the four reprobe-decisive targets ARE the
    # CO-time exhausted members; the five 15M-solved targets are win-roster
    # members; see the G6 header above)
    adopted_ids = set()
    for fld in ("loss_ids",):
        v = im.get(fld) or []
        adopted_ids |= set(v)
    for b in im.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "fragment_ids"):
            v = b.get(fld) or []
            adopted_ids |= set(v)
    win_roster_ids = set()
    for fld in ("win_ids", "unadopted_win_ids"):
        v = im.get(fld) or []
        win_roster_ids |= set(v)
    uwr_rows = {u.get("key_id"): u for u in (im.get("unadopted_win_rows") or []) if isinstance(u, dict)}
    member_ids = set()
    for fld in ("probed_ids", "resolved_ids"):
        v = im.get(fld) or []
        member_ids |= set(v)
    for b in im.get("batches", []):
        for fld in ("unadopted_win_ids", "probed_ids"):
            v = b.get(fld) or []
            win_roster_ids |= set(v) if fld == "unadopted_win_ids" else set()
            member_ids |= set(v) if fld == "probed_ids" else set()
    gate("unadopted-manifest-exhausted-roster",
         (im.get("exhausted_excluded_ids") or []) == PIN_EXHAUSTED_IDS and
         (im.get("batches", [{}])[0].get("exhausted_excluded_ids") or []) == PIN_EXHAUSTED_IDS,
         "CO-time exhausted_excluded_ids roster (11)")
    for t in rows["targets"]:
        gate(f"unadopted-manifest-target-not-in-adopted-lists-{t['key_id']}", t["key_id"] not in adopted_ids,
             f"{t['key_id']} must not appear in any adopted/loss/fragment id list of the CO increments-manifest")
        gate(f"unadopted-manifest-target-in-member-books-{t['key_id']}", t["key_id"] in member_ids,
             f"{t['key_id']} must appear in probed_ids/resolved_ids member bookkeeping (batch-28 member)")
    by_key = {t["key_id"]: t for t in rows["targets"]}
    for k in TIER15_KEYS:
        gate(f"unadopted-manifest-tier15-not-in-exhausted-{k}",
             k not in set(im.get("exhausted_excluded_ids") or []),
             f"{k} was 15M-solved at CO time, not exhausted")
        gate(f"unadopted-manifest-tier15-in-win-roster-{k}", k in win_roster_ids,
             f"{k} must appear in the CO unadopted-win roster")
        u = uwr_rows.get(k)
        gate(f"unadopted-manifest-tier15-uwr-node-exact-{k}",
             u is not None and int(u.get("result")) == 1 and int(u.get("nodes")) == by_key[k]["replica_nodes"]
             and u.get("two_pass_node_exact") is True,
             str(u))
    for k in REPROBE_KEYS:
        gate(f"unadopted-manifest-reprobe-in-exhausted-{k}",
             k in set(im.get("exhausted_excluded_ids") or []),
             f"{k} was a CO-time exhausted_excluded member (base 15M probe exhausted; WIN label from the reprobe publications)")
        gate(f"unadopted-manifest-reprobe-not-in-win-roster-{k}", k not in win_roster_ids,
             f"{k} must NOT appear in the CO unadopted-win roster (CO-time honest label was exhausted, not win)")
        gate(f"unadopted-manifest-reprobe-not-in-uwr-{k}", k not in uwr_rows,
             f"{k} must NOT carry a CO unadopted_win_rows entry")
    # Part DB manifest battery (current canonical chain head; batch-29 scope)
    imd = json.load(open(mandb_path))
    gate("unadopted-pin-increments-manifest-db", sha256(mandb_path) == PIN_INCR_MANIFEST_DB, sha256(mandb_path))
    gate("unadopted-manifest-db-schema", imd.get("schema") == "b29loss37-increments-manifest-v1", imd.get("schema"))
    gate("unadopted-manifest-db-base", imd.get("base_cache_sha256") == PIN_MERGED_BASE_CU
         and int(imd.get("base_cache_rows", -1)) == 6317,
         f"{imd.get('base_cache_sha256')},{imd.get('base_cache_rows')}")
    gate("unadopted-manifest-db-loss37", len(imd.get("loss_ids") or []) == 37
         and all(str(x).startswith("ab") for x in imd.get("loss_ids") or []),
         f"{len(imd.get('loss_ids') or [])} batch-29 LOSS ids")
    db_text = open(mandb_path).read()
    for t in rows["targets"]:
        gate(f"unadopted-manifest-db-absent-text-{t['key_id']}", t["key_id"] not in db_text,
             f"{t['key_id']} must not appear anywhere in the batch-29-scoped DB manifest")

    # -- G7 (declared, as in Part CM/CR/CX/DG): val-gate this-host 4/4 node-exact vs
    #    the published baselines (all replay fields except wall_s; replay_done +
    #    quads header presence both required)
    for vgkey, vgbudget in VALGATE_KEYS:
        base_path = os.path.join(ROOT, "val-gate", f"{vgkey}.published-baseline.out")
        host_path = os.path.join(ROOT, "val-gate", f"{vgkey}.dh-host.out")
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
