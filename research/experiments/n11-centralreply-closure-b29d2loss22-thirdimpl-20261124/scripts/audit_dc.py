# audit_dc.py -- fail-closed gate battery for the Part DC third-implementation
# cross-verification of the TWENTY-TWO published batch-29 (closure class 2251)
# Part CI takeover drive-2 ckpt-3/3 LOSS rows (ab033..ab054,
# result 2, budget 15M) -- UNCONSUMED honest labels, including the declared
# this-host pinned-replica 2-pass reproductions. Every gate must PASS or the
# script exits rc=1 with the gate name. Reads only local artifacts under this
# experiment dir; writes output/audit-summary.json.
#
# Adapted from the published Part DA audit (audit_da.py, sha256
# ca24423d2278c205b9a37fd08dd15ad01f9dbb3f49cf216b944a1df0712df686 (declared
# Part DA kit pin), itself adapted from the published Part CZ audit (audit_cz.py,
# sha256
# 3c95e32fc1b069c5a8ccf60f82e59846e8889ebfa53f2a607c76e5b50a48f289,
# experiment n11-centralreply-closure-b29ab028win-thirdimpl-20261124, itself
# from the published Part CW audit a7876a0a.. / CR 2ab974c3.. / CM 3f9a29fa..
# / CL edf0ae7c.. / CC b7cfb0ce.. / BY 7f7fa3d1 / BX 19351ab5 / BW 3a2ce7ef
# / BV 08bdebce). Declared deltas (all in the Part DC declaration before
# execution): EXP/SCHEMA/rows-schema strings, the batch-29 drive-2
# ckpt-3/3 LOSS-rows wording (targets = 22 LOSS rows, NOT the WIN row ab028),
# the rows.json pin switched to the Part DC maker output, the pinned raw-out
# sha pins for the 22 targets p1/p2 (44), target-count 22, target-verdict-
# kinds [2]*22, rows-schema flags unadopted_win_rows False /
# unadopted_loss_rows True, the val-gate host suffix .dc-host.out, and the
# G6 id-list battery adapted for the CU-time fileless UNPROBED status of
# EACH target: all 22 targets LEGITIMATELY appear ONLY in the CU manifest's
# batches[0].fileless_unprobed_ids roster (38 keys) and must be absent from
# EVERY adopted/win/probed id list. Verdicts are NOT consumed: the 22 LOSS
# rows are honest labels pending canonical adoption Parts; nothing is
# adopted, freed, closed, or claimed. The standard 11x11 empty board, the
# central-reply roots, class 2251 and every batch-29 key stay UNKNOWN.
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-closure-b29d2loss22-thirdimpl-20261124"
SCHEMA = "n11-centralreply-closure-b29d2loss22-thirdimpl-audit-v1"
ROWS_SCHEMA = "n11-centralreply-closure-b29d2loss22-thirdimpl-input-v1"

PIN_THIRD = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
PIN_VERIFYTBL = "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"
PIN_JSREPLAY = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
PIN_MERGED_CANONICAL = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"
PIN_INCREMENT = "bab011e376090f9f4732d63f0084f326ba72dada5cf699d5aabc7e014c29ae24"
PIN_INCR_MANIFEST = "f9f58ee101d53f0598ee01c5c54d5b277797a9e882cfb478ab7f7b3010e191e0"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
PIN_INCREMENT_DB = "85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc"
PIN_MERGED_DB = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"
PIN_MERGED_BASE = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_STATUS_DRIVE1_PREFIX = "6b877344b9abea348a9b221f587a771857d3c4091f88fa460ef12595722183e2"
PIN_RAW_DC = {
    "ab033.p1": "1fb2b25017e6d899b105652fd104316628ec66aaa5e35ef91e3ee5876396e260",
    "ab033.p2": "b4545d3682aafb11701f344a82e38f4f817b713e6e5a6936e6f89f68faabd39c",
    "ab034.p1": "02cc6aac705e6ebe788486f8ef5e5aa835d9238d076dadc5706ba14b92118b33",
    "ab034.p2": "1276f66702e70de460e612c5b0a26e6f083e3c471080ac10699a32db43f32a4a",
    "ab035.p1": "a64a66c342c01a798b707111b6e1959a373d6784c23a231626cbb54bf51e07c1",
    "ab035.p2": "cac28df0e7bc55707c762e4db490694f66148d4e2e1ac68725e5497a521d3f04",
    "ab036.p1": "fb66e6ba9f93c02cc63821a432e94aa98485adbe501cb7d2969ab913849043ba",
    "ab036.p2": "612cf8697ac4f05a351205e665c779a6a9643f1cad4ce7f7f0e19e8806a06c66",
    "ab037.p1": "ccf3bdc3912be63d0236cfcf1ef98ed1de5fbbb7a1a7f6fad26068fb9f67cd10",
    "ab037.p2": "ec56ba4c8081c1a57170012304a9af6429743d235dc0321c967a4b47e0eba730",
    "ab038.p1": "1faabe063bdf0e11895fe569896e780c86e596015110928b77b9c2ace11858c9",
    "ab038.p2": "b1c8bbf46d84600126765480133328830e80fab29f2e68f2b813a01ae5a04f2e",
    "ab039.p1": "6010281e79aca63c1017b3dae72fe3559482e4d5ffeec0e0fba16e8988830769",
    "ab039.p2": "6e66a85edc3b0fcaa9da92fd58630586266527fb299ac329162d081bfb3a8d36",
    "ab040.p1": "d5458452c343f7f82e6f278e9760f7675ae6aa8d7ea107344a798cb59d0df335",
    "ab040.p2": "5f49c18615e2278cf872ea7afb9a7fa0b0679f04322cfbf9679742a60a9ab99e",
    "ab041.p1": "b2aec1abca8019fbc4f7496f5c89dfe0ce4eb0150e3af946f04676501b0c47bb",
    "ab041.p2": "0a24ebf4a96207c4c1df0d68a482f0875ca61a97da5d2c8b9f55beab6b9fd666",
    "ab042.p1": "714daf54f12b742dc80ba5140c5626d639f9cd9cbce1b15749efcf202725a6e0",
    "ab042.p2": "e7042cd71c8407c3f2b48eda39f6a26de3e1303fdc3afd43d21f206cd5093c65",
    "ab043.p1": "a0d6c3a07d922ed3abda4f7fecb562ad6747acd9ff93c89b0c9ef57cdaecced5",
    "ab043.p2": "430ff6e191f49e71d60d81ff60c7c44fe09638431673d9b1886effed801f9fd9",
    "ab044.p1": "18128ecb2bf8fc74f0bab09a6b57ceabfdae66a47eefbe8830cfa76d826944b6",
    "ab044.p2": "6c391e4d32fdcd85f6744d23fafef6c23e75f46c5937d105a24fa5578258f4bb",
    "ab045.p1": "4f4cb428c31e26ca537aa1bbde092a333141d9dd6edb494afadf1fce1bf2e39c",
    "ab045.p2": "acb756456316f34959332292dc6f125242c40b973e8ef7d2b2e1ad3b50a5c4f8",
    "ab046.p1": "d0aa5b31e90fae9e2eba9f8cff0eff7cc5d41fb28b174fd1f5165bc03169676a",
    "ab046.p2": "6b2b38ef1900d6a150a2f0b36d6f5125bea2d408b83eac2e82b48e21d1a6b9ea",
    "ab047.p1": "2e9f7cf2b19a1896933e9201a7245b218c89895325aee2c8720448e64af03850",
    "ab047.p2": "f53697178e1f6aa8b6561a26c043a00729963c6e15c806599c0c2e912cecdb03",
    "ab048.p1": "30b633c167824c84fb32e117c164aacf026aafeaa4f35cfcaa051d3ddaa2c087",
    "ab048.p2": "d71f73ccad93b58f6dffe09faf0d3eea8bc97007a794a13814bf5047a51d4fc9",
    "ab049.p1": "44b431f5941d5f35138c63eacf1ac6e662431f06c87d06ce39d103bb60065071",
    "ab049.p2": "6c3aac130f498985e993bb78cc4c80b364a3e7b15293048ee69f93dd6bd0098e",
    "ab050.p1": "b027f4d91a95f954049d1d8313e2b9a7c07f6b719d22a7edcf7829adae371d9e",
    "ab050.p2": "b027f4d91a95f954049d1d8313e2b9a7c07f6b719d22a7edcf7829adae371d9e",
    "ab051.p1": "198af4f083bf59dd971b6e4dd775a6d7120d1b315dc8d18164e0b18bed65a91c",
    "ab051.p2": "3898a79281f3ff8f3e884fa1e1f3dfa4c962b023cece5787c88786b17ea937f1",
    "ab052.p1": "28b105794acb36705102755a39d3a64d1a718bc5b900f5d0f758c8ebcd7cd74e",
    "ab052.p2": "eae0d933fc275933fdad3d46ff0cf53625f371f48d11d46ca0502688a1c243b7",
    "ab053.p1": "a92b7c0a78ea5eb66c0e0ef9b82410507faf1e8047ce417c77598a7a406ef533",
    "ab053.p2": "a92b7c0a78ea5eb66c0e0ef9b82410507faf1e8047ce417c77598a7a406ef533",
    "ab054.p1": "22a825e42af6ab1cdd7b83390c9831a69a9a1841aee6f979136decdf266bb6a3",
    "ab054.p2": "2e4c5e1dbcc379f1f50f64fb83e4aa0a5d73b1fb20a17152353205b835fbbeab",
}
PIN_LOSS_IDS = [f"ab{i:03d}" for i in range(1, 17)]
PIN_ADOPTED_HEADER = "ADOPTED set = ab001..ab016"
PIN_STATUS_ROWS_JSON = "64bc4b78711dbe1e3798116a670d669bcdd71865768bf9a0998bd50550dc13b6"

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
         and rows.get("unadopted_win_rows") is False
         and rows.get("unadopted_loss_rows") is True
         and rows.get("canonical_cache_sha256_unchanged") == PIN_MERGED_CANONICAL,
         rows.get("schema"))
    gate("target-count", len(rows["targets"]) == 22,
         f"{len(rows['targets'])} (22 b29 drive-2 ckpt-3/3 LOSS rows)")
    gate("target-verdict-kinds",
         sorted(t["expect_third"] for t in rows["targets"]) == [2] * 22,
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

    # -- G6 (declared): unadopted-row corroboration. EACH row cross-verified
    #    above must be byte-identically the published batch-29 drive-2 raw row
    #    (pinned) and must NOT appear anywhere in the Part CU adopted
    #    canonical cache / increment, and in the increments-manifest ONLY in
    #    the batches[0].fileless_unprobed_ids roster (its CU-time UNPROBED
    #    status) -- never in any adopted/win/probed id list. Verdicts never
    #    consumed: canonical cache 30ddad9d unchanged (6,317 rows).
    for t in rows["targets"]:
        k = t["key_id"]
        gate(f"unadopted-pin-raw-{k}-p1", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")) == PIN_RAW_DC[k + ".p1"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out")))
        gate(f"unadopted-pin-raw-{k}-p2", sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")) == PIN_RAW_DC[k + ".p2"],
             sha256(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out")))
        row_would_be = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        merged_path = os.path.join(ROOT, "sources", "merged-cache-cu-b29loss16.cache")
        gate(f"unadopted-pin-merged-cache-{k}", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
        s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
        gate(f"unadopted-merged-cache-rowcount-{k}", len(s5rows) == 6317, f"{len(s5rows)} s5verdict rows")
        hits = [l for l in s5rows if l == row_would_be]
        gate(f"unadopted-merged-cache-row-absent-{k}", len(hits) == 0,
             f"{row_would_be} occurs {len(hits)} times (expect 0: the drive-2 LOSS row was never adopted)")
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

    # -- G6b (declared, Part DC adaptation): post-DB canonical corroboration.
    #    The Part DB 37-LOSS adoption (published 2026-11-24 02:38Z) adopted the
    #    same drive-2 LOSS rows into the canonical chain. Each target row must
    #    be byte-identically present in the pinned DB increment (37 rows) and
    #    in the pinned post-adoption canonical cache (6,354 rows) with the
    #    exact (result, nodes) pair -- an independent cross-artifact
    #    consistency check, NOT a new verdict and NOT any claim.
    db_inc_path = os.path.join(ROOT, "sources", "increment-b29loss37.cache")
    db_merg_path = os.path.join(ROOT, "sources", "merged-cache-db-b29loss37.cache")
    gate("db-pin-increment-shared", sha256(db_inc_path) == PIN_INCREMENT_DB, sha256(db_inc_path))
    gate("db-pin-merged-shared", sha256(db_merg_path) == PIN_MERGED_DB, sha256(db_merg_path))
    db_inc_rows = [l for l in open(db_inc_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("db-increment-37-rows", len(db_inc_rows) == 37, f"{len(db_inc_rows)} rows")
    db_s5rows = [l for l in open(db_merg_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("db-merged-6354-rows", len(db_s5rows) == 6354, f"{len(db_s5rows)} rows")
    for t in rows["targets"]:
        row_expected = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        gate(f"db-increment-row-{t['key_id']}", sum(1 for l in db_inc_rows if l == row_expected) == 1, row_expected)
        gate(f"db-merged-row-{t['key_id']}", sum(1 for l in db_s5rows if l == row_expected) == 1, row_expected)

    # -- G7 (declared, as in Part CM/CR/CW): val-gate this-host 4/4 node-exact vs
    #    the published baselines (all replay fields except wall_s; replay_done +
    #    quads header presence both required)
    for vgkey, vgbudget in VALGATE_KEYS:
        base_path = os.path.join(ROOT, "val-gate", f"{vgkey}.published-baseline.out")
        host_path = os.path.join(ROOT, "val-gate", f"{vgkey}.dc-host.out")
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
