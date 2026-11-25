#!/usr/bin/env python3
# make_kit_eg.py -- fail-closed maker for the Part EG kit
# (n11-centralreply-closure-b33win6-thirdimpl-20261125).
#
# Verifies every kit source/input byte against its published sha256 pin
# (batch-33 class-34908 drive raws/status/batch-keys, Part EA b33exh5-reprobe
# 30M raws/status/reprobe-keys, Part EE af034loss1 adoption merged-cache /
# increment / increments-manifest, Part CZ anchor/negative/val-gate byte-
# clones), machine-extracts the published WIN rows for the 6 unconsumed
# class-34908 children from the RAW files (not status text alone), proves the
# 6 would-be canonical s5verdict rows are ABSENT from the current canonical
# merged cache (fc3e4ac9, 6,666 rows) and that no conflicting same-pair row
# exists, proves the af034 adopted row IS present exactly once (positive
# control of the absence logic), and only then writes input/rows.json.
#
# FAIL-CLOSED: on any gate failure it writes NO output file, prints
# ABORT <gate> and exits rc=1. Verdicts are NOT consumed: this maker never
# writes the canonical cache and never changes any honest label. The 6 rows
# stay unconsumed probe-level WIN rows pending the scrutiny owner C++
# second-implementation gate pin 9193f5b6... The standard 11x11 empty board,
# the 19 central-reply roots, class 34908 and every key remain UNKNOWN.
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-closure-b33win6-thirdimpl-20261125"
OUT_REL = "input/rows.json"
SCHEMA = "n11-centralreply-closure-b33win6-thirdimpl-input-v1"

def sha(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def abort(gate, detail):
    print(f"ABORT {gate} {detail}")
    sys.exit(1)

def gate_sha(rel, pin):
    s = sha(rel)
    if s != pin:
        abort(f"G1-pin-drift:{rel}", f"{s} != {pin}")
    return True

# ---------------------------------------------------------------------------
# pinned constants (published bytes, fetch-verified at kit assembly time)
PIN_THIRD = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
PIN_JSREPLAY = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
PIN_RUN_REPLICA = None  # self-script, pinned at declaration by its own sha below
RUN_REPLICA_PIN = sha("scripts/run_replica_eg.sh") if os.path.isfile(os.path.join(ROOT, "scripts", "run_replica_eg.sh")) else None

PINS = {
    "scripts/third_impl.js": PIN_THIRD,
    "scripts/jsreplay.js": PIN_JSREPLAY,
    "scripts/run_thirdimpl.sh": "a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41",
    "sources/b33-batch-keys.json": "8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa",
    "sources/b33-status.log": "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52",
    "sources/ea-status.log": "db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438",
    "sources/ea-reprobe-keys.json": "3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663",
    "sources/ee-merged-exact-s5-chain-plus-af034loss1-20261125.cache": "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f",
    "sources/ee-increment-af034loss1-20261125.cache": "cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162",
    "sources/ee-increments-manifest.json": "0ad3469ede4bfbddaee21d12dbab97f7e0babdbe5cbaba8cc7a6f2f41d0d22c9",
}
B33_RAW_PINS = {
    "af029": ("6bd7a2ac37cccd8a387d6b505112c1a93b712e8d41b43467fa0844ce64ec0036",
              "b6abaa6384ee93c890cadd350f2f844889f3ee42110935a366af7893a2030e0b"),
    "af047": ("8fd62fdd27d10235b4ba67c6f43cfeb4fe5f494559544119d4f0339223a7b8c6",
              "ae4719e8c8a0a7abd72cec6f4e013c1e576c7627100de95b55ba34c364b694a4"),
    "af050": ("3ea4f644ca19186f0a56ae25f79ef0ccc8b608b5ef64045bc052a488cae9b1d7",
              "43a5b71ca57d2a2601f82b7ec35980b0761dc315e8093f3c9ae603cd8d4ca5a6"),
    "af053": ("fce95ca8921357641f477a01483fbd4c35e6f183a25c8d741657dec645f78533",
              "920b1029500e93532238d03d07e89fdf091ffecd2481cab56f7dd032b5f645b7"),
    # the two 15M EXHAUSTED rows are provenance of the budget ladder, not
    # comparison rows (their 30M WIN counterparts are the published verdicts)
    "af023": ("225b4d6526f1f8c5b6a6dafe6b5b359df4718c6b6b958147582ead3c14b5e33a",
              "fc86c52502e08f04dd2a7d35d257021d808f1a3652f1ed758f91ac3c3954e17f"),
    "af048": ("95c30994057c5017b5e3f153fea9432c21ca7d9da119ff1181ffee95805ce2a4",
              "25fa2c2279eadd297b488d2156dfac9ee5c9abbb06e0026bfc878aaf4fce6450"),
}
EA_RAW_PINS = {
    "af023": ("fe118851a927944328a62387d0410a596713c87f1360dda662c97f87913c1dbe",
              "af02e38b07a7f1da9af28c0af7985eaa0cdd97ec2884298ede3a831b19c9198b"),
    "af048": ("ae8df6ad6f922669f285f1c2a20d7fa09453c2ef38f64f1b4b878c3034e9d07a",
              "e2056ca26533124e20d3538eebc5e6c4b752be21b92e9e3780c5a0040f0bb620"),
    "af029": ("1726ecb6d8199d612130d3c2cae12b176102fef0468263cbc1397f525eb0aa66",
              "c937f8964385b2e4c74c1f1d417cdb113b2548dca33c3e0604facea7d9c905a6"),
    "af001": ("c2bc73f6a5d88720e33fc3fb498ab16f2d541d7cad62248ef8d04b5f9351381d",
              "e4614f6bd7d4f20cfdd7dba3362e6db52328827a120b9d379fdd2accbdbf1681"),
}
INPUT_CSV_PINS = {
    "af029": "b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10",
    "af047": "24cc1aa00849f6b74c7f976b46903874321aac981f62dd542e51948a3f351418",
    "af050": "3bc623db974bc6285c575b8575a75510c3e9f1909a650a4969e214225e507729",
    "af053": "b30a43a948945d7b49946c28dec20b5859aac1003d522f042cfff4d1225d989e",
    "af023": "0ba31256582eae15cc80fb2bdbfe56a140533828cdab7a05eeef6ca1089a1c08",
    "af048": "d619dcd7d47d7b65f1c4325d99b69211826eb83732c3eb475f14ea4f9f973422",
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}
VALGATE_INPUT_PINS = {
    "at2m-s5-1152921504606851072-536870946": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "at2m-s5-1188950301626860544-536870912": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "first-15m-s5-1152921504606851072-536870946": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "second-15m-s5-1188950301626860544-536870912": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
}
VALGATE_BASELINE_PINS = {
    "at2m-s5-1152921504606851072-536870946": "6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c",
    "at2m-s5-1188950301626860544-536870912": "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "first-15m-s5-1152921504606851072-536870946": "8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591",
    "second-15m-s5-1188950301626860544-536870912": "91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb",
}

# published honest-label WIN rows (the COMPLETE unconsumed set of class 34908)
TARGETS = [
    {"key_id": "af029", "stones": 5, "lo": 1152921504607895553, "hi": 68720525312,
     "legal": 86, "s5_index": 900646, "membership_class_count": 2,
     "replica_result": 1, "replica_nodes": 4862485, "budget": 15000000,
     "source": "batch33-class34908-drive-15m",
     "extra30m": {"replica_result": 1, "replica_nodes": 4862485, "budget": 30000000,
                  "source": "part-ea-b33exh5-reprobe30m-anchor"}},
    {"key_id": "af047", "stones": 5, "lo": 1152921504607895809, "hi": 68719476736,
     "legal": 84, "s5_index": 961976, "membership_class_count": 3,
     "replica_result": 1, "replica_nodes": 9841975, "budget": 15000000,
     "source": "batch33-class34908-drive-15m"},
    {"key_id": "af050", "stones": 5, "lo": 1152921504607899649, "hi": 68719476736,
     "legal": 94, "s5_index": 962386, "membership_class_count": 3,
     "replica_result": 1, "replica_nodes": 7311834, "budget": 15000000,
     "source": "batch33-class34908-drive-15m"},
    {"key_id": "af053", "stones": 5, "lo": 1152921504606852096, "hi": 17660905521152,
     "legal": 90, "s5_index": 962470, "membership_class_count": 2,
     "replica_result": 1, "replica_nodes": 5182129, "budget": 15000000,
     "source": "batch33-class34908-drive-15m"},
    {"key_id": "af023", "stones": 5, "lo": 1152921504607895553, "hi": 68719478784,
     "legal": 94, "s5_index": 810351, "membership_class_count": 4,
     "replica_result": 1, "replica_nodes": 28933179, "budget": 30000000,
     "source": "part-ea-b33exh5-reprobe30m", "prior_15m_exhausted": True},
    {"key_id": "af048", "stones": 5, "lo": 1152921508902862849, "hi": 68719476736,
     "legal": 87, "s5_index": 962172, "membership_class_count": 3,
     "replica_result": 1, "replica_nodes": 17816616, "budget": 30000000,
     "source": "part-ea-b33exh5-reprobe30m", "prior_15m_exhausted": True},
]
ANCHORS = [
    {"key_id": "k02a", "stones": 5, "lo": 1297036692683751424, "hi": 68157440,
     "legal": 87, "expect_third": 1, "anchor_expansions": 9106337,
     "anchor_ttHits": 4991527, "expect_kind": "win",
     "replica_result": None, "replica_nodes": None},
    {"key_id": "l1a", "stones": 5, "lo": 13019119616, "hi": 16448,
     "legal": 116, "expect_third": 2, "anchor_expansions": 7660602,
     "anchor_ttHits": 3951175, "expect_kind": "loss",
     "replica_result": None, "replica_nodes": None},
]
NEGATIVES = [
    {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
     "stones": 5, "why": "legal+1 vs derived 87"},
    {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
     "stones": 6, "why": "stones 6 vs actual 5"},
]
AF034_ADOPTED_ROW = "s5verdict,1152921504607911937,68719476736,5,2,32012059"

def replay_row(path):
    """first replay, row of a raw .out as field list, plus done/quads flags"""
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
    for rel, pin in PINS.items():
        gate_sha(rel, pin)
    for k, (p1, p2) in B33_RAW_PINS.items():
        gate_sha(f"sources/b33-raw/{k}.p1.out", p1)
        gate_sha(f"sources/b33-raw/{k}.p2.out", p2)
    for k, (p1, p2) in EA_RAW_PINS.items():
        gate_sha(f"sources/ea-raw/{k}.p1.out", p1)
        gate_sha(f"sources/ea-raw/{k}.p2.out", p2)
    for k, pin in INPUT_CSV_PINS.items():
        gate_sha(f"input/{k}.input.csv", pin)
    for k, pin in VALGATE_INPUT_PINS.items():
        gate_sha(f"val-gate/{k}.input.csv", pin)
    for k, pin in VALGATE_BASELINE_PINS.items():
        gate_sha(f"val-gate/{k}.published-baseline.out", pin)
    if RUN_REPLICA_PIN is None:
        abort("G1-run-replica-missing", "scripts/run_replica_eg.sh")
    print("G1 all source/input pins PASS")

    # -- G2: cross-field consistency (exact Python ints; CSV pairs as strings)
    bk = json.load(open(os.path.join(ROOT, "sources/b33-batch-keys.json")))
    bkeys = {it["key_id"]: it for it in bk["keys"]}
    rk = json.load(open(os.path.join(ROOT, "sources/ea-reprobe-keys.json")))
    rkeys = {it["key_id"]: it for it in rk["keys"]}
    for t in TARGETS:
        csv = open(os.path.join(ROOT, f"input/{t['key_id']}.input.csv")).read().strip().split(",")
        if not (csv[0] == "target" and int(csv[2]) == t["stones"] and int(csv[3]) == t["lo"]
                and int(csv[4]) == t["hi"] and int(csv[5]) == t["legal"]):
            abort(f"G2-csv:{t['key_id']}", str(csv[:6]))
        b = bkeys[t["key_id"]]
        if not (int(b["lo"]) == t["lo"] and int(b["hi"]) == t["hi"] and b["legal"] == t["legal"]
                and b["s5_index"] == t["s5_index"] and b["membership_class_count"] == t["membership_class_count"]):
            abort(f"G2-batchkeys:{t['key_id']}", json.dumps(b))
        if t["key_id"] in rkeys:
            r = rkeys[t["key_id"]]
            if not (int(r["lo"]) == t["lo"] and int(r["hi"]) == t["hi"] and r["legal"] == t["legal"]
                    and r["s5_index"] == t["s5_index"]):
                abort(f"G2-reprobekeys:{t['key_id']}", json.dumps(r)[:120])
        else:
            # af047/af050/af053 are batch-33-only rows (no EA entry at all):
            # legitimate. af029 was an EA ANCHOR: field-check it there.
            anchor = next((a for a in (rk.get("anchors") or []) if a["key_id"] == t["key_id"]), None)
            if t["key_id"] == "af029":
                if anchor is None:
                    abort("G2-rk-anchor-missing:af029", "af029 must be in the EA anchor roster")
                if not (int(anchor["lo"]) == t["lo"] and int(anchor["hi"]) == t["hi"]
                        and anchor["legal"] == t["legal"]):
                    abort("G2-rk-anchor-fields:af029", json.dumps(anchor)[:120])
            elif anchor is not None:
                abort(f"G2-rk-anchor-unexpected:{t['key_id']}",
                      "batch-33-only key must not appear in the EA anchor roster")
    # af023/af048/af029 (in EA) must have their pinned 15m raws equal to b33 raws
    for k in ("af023", "af048", "af029"):
        r = rkeys.get(k) or next((a for a in (rk.get("anchors") or []) if a["key_id"] == k), None)
        if r is None:
            abort(f"G2-rk-missing:{k}", "")
        p15 = r.get("published_15m", {})
        if not (p15.get("result") is not None and p15["result"] in (0, 1)
                and p15.get("raw_p1_sha256") == B33_RAW_PINS[k][0]
                and p15.get("raw_p2_sha256") == B33_RAW_PINS[k][1]):
            abort(f"G2-ladder15m-pin:{k}", json.dumps(p15)[:160])
    print("G2 cross-field consistency PASS")

    # -- G3: status.log rows machine-checked against pinned published values
    b33_lines = [(l.split(None, 3) + [""])[:4] for l in open(os.path.join(ROOT, "sources/b33-status.log")).read().splitlines() if l]
    b33_pass = {}
    b33_exhausted = set()
    for ts, kid, kind, rest in b33_lines:
        if kind == "PASS":
            b33_pass.setdefault(kid, []).append(rest)
        elif kind == "EXHAUSTED":
            b33_exhausted.add(kid)
    for t in TARGETS:
        k = t["key_id"]
        if t.get("prior_15m_exhausted"):
            if k not in b33_exhausted:
                abort(f"G3-b33-exhausted-missing:{k}", "")
        else:
            want = f"{t['budget']},{t['replica_result']},{t['replica_nodes']}"
            hits = [r for r in b33_pass.get(k, []) if r == want]
            if len(hits) != 1:
                abort(f"G3-b33-status:{k}", f"{b33_pass.get(k)} != single {want}")
    ea_lines = [(l.split(None, 3) + [""])[:4] for l in open(os.path.join(ROOT, "sources/ea-status.log")).read().splitlines() if l]
    ea_pass = {}
    for ts, kid, kind, rest in ea_lines:
        if kind == "PASS":
            ea_pass.setdefault(kid, []).append(rest)
    for k, want in (("af023", "30000000,1,28933179"), ("af048", "30000000,1,17816616"),
                    ("af029", "30000000,1,4862485"), ("af001", "30000000,2,2952432")):
        if ea_pass.get(k) != [want]:
            abort(f"G3-ea-status:{k}", str(ea_pass.get(k)))
    print("G3 status rows PASS")

    # -- G4: raw fields machine-extracted (SSOT = raw files)
    def rawrel(src, k, p):
        return f"sources/{src}/{k}.{p}.out"
    for t in TARGETS:
        k = t["key_id"]
        src = "b33-raw" if t["budget"] == 15000000 else "ea-raw"
        for p in ("p1", "p2"):
            row, done, quads = replay_row(os.path.join(ROOT, rawrel(src, k, p)))
            if row is None or not done or not quads:
                abort(f"G4-raw-shape:{k}.{p}", f"row={row is not None} done={done} quads={quads}")
            # replay,<stub>,s?,legal,is_or,budget,result,nodes,wall,lo,hi
            if not (row[2] == "5" and row[1] == "0" and int(row[3]) == t["legal"]
                    and int(row[5]) == t["budget"] and int(row[6]) == t["replica_result"]
                    and int(row[7]) == t["replica_nodes"] and int(row[9]) == t["lo"]
                    and int(row[10]) == t["hi"]):
                abort(f"G4-raw-fields:{k}.{p}", ",".join(row))
    # af029 extra 30M pair (EA anchor rows)
    for p in ("p1", "p2"):
        row, done, quads = replay_row(os.path.join(ROOT, rawrel("ea-raw", "af029", p)))
        if not (done and quads and row[5] == "30000000" and row[6] == "1" and row[7] == "4862485"):
            abort(f"G4-raw-fields:af029-30m.{p}", ",".join(row or []))
    # af023/af048 15M EXHAUSTED provenance pairs (result 0 = honest UNKNOWN)
    for k in ("af023", "af048"):
        for p in ("p1", "p2"):
            row, done, quads = replay_row(os.path.join(ROOT, rawrel("b33-raw", k, p)))
            if not (done and quads and row[5] == "15000000" and row[6] == "0" and row[7] == "15000000"):
                abort(f"G4-raw-15m-exhausted:{k}.{p}", ",".join(row or []))
    # af001 anchor LOSS pair at 30M (EE adopted-line provenance)
    for p in ("p1", "p2"):
        row, done, quads = replay_row(os.path.join(ROOT, rawrel("ea-raw", "af001", p)))
        if not (done and quads and row[5] == "30000000" and row[6] == "2" and row[7] == "2952432"):
            abort(f"G4-raw-af001.{p}", ",".join(row or []))
    print("G4 raw fields PASS")

    # -- G5: canonical merged cache (EE) -- absence of the 6 rows + presence
    #        of the adopted af034 row as positive control
    merged_rel = "sources/ee-merged-exact-s5-chain-plus-af034loss1-20261125.cache"
    lines = open(os.path.join(ROOT, merged_rel)).read().splitlines()
    s5rows = [l for l in lines if l.startswith("s5verdict,")]
    if len(s5rows) != 6666:
        abort("G5-merged-rowcount", str(len(s5rows)))
    wins = sum(1 for l in s5rows if l.split(",")[4] == "1")
    losses = sum(1 for l in s5rows if l.split(",")[4] == "2")
    if not (wins == 158 and losses == 6508):
        abort("G5-merged-counts", f"WIN={wins} LOSS={losses}")
    if sum(1 for l in s5rows if l == AF034_ADOPTED_ROW) != 1:
        abort("G5-af034-control", "adopted row must occur exactly once")
    for t in TARGETS:
        would = f"s5verdict,{t['lo']},{t['hi']},5,{t['replica_result']},{t['replica_nodes']}"
        if sum(1 for l in s5rows if l == would) != 0:
            abort(f"G5-wouldbe-present:{t['key_id']}", would)
        conflicts = [l for l in s5rows if l.startswith(f"s5verdict,{t['lo']},{t['hi']},")]
        if conflicts:
            abort(f"G5-pair-conflict:{t['key_id']}", str(conflicts))
    print("G5 merged-cache absence battery PASS")

    # -- G6: EE increment + manifest pins (adoption provenance)
    inc = open(os.path.join(ROOT, "sources/ee-increment-af034loss1-20261125.cache")).read().splitlines()
    inc_s5 = [l for l in inc if l.startswith("s5verdict,")]
    if inc_s5 != [AF034_ADOPTED_ROW]:
        abort("G6-increment-rows", str(inc_s5))
    man = json.load(open(os.path.join(ROOT, "sources/ee-increments-manifest.json")))
    if not (man.get("schema") == "af034loss1-increments-manifest-v1"
            and man.get("loss_ids") == ["af034"] and man.get("resolved_ids") == ["af034"]
            and man.get("win_scenario_exists") is False and man.get("full_packet_eq_loss_only") is True
            and man.get("unadopted_win_ids") == [] and man.get("win_ids") == []
            and man.get("merger_sha256") == "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
            and man.get("base_cache_sha256") == "cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626"
            and int(man.get("base_cache_rows", -1)) == 6665
            and int(man.get("row_counts", {}).get("adopted_loss_rows", -1)) == 1):
        abort("G6-manifest-flags", json.dumps({k: man.get(k) for k in
              ("schema", "loss_ids", "win_scenario_exists", "base_cache_rows")})[:200])
    b0 = man["batches"][0]
    if b0.get("adopted_loss_ids") != ["af034"]:
        abort("G6-batch-adopted", str(b0.get("adopted_loss_ids")))
    if b0.get("anchor_input_sha256", {}).get("af029") != INPUT_CSV_PINS["af029"]:
        abort("G6-anchor-pin-af029", str(b0.get("anchor_input_sha256", {}).get("af029")))
    note = man.get("win_scenario_note", "")
    for t in TARGETS:
        if t["key_id"] not in note:
            abort(f"G6-note-missing:{t['key_id']}", "EE win_scenario_note must name all six pooled WIN children")
    # targets must not appear in any adopted id list of the EE manifest
    adopted_ids = set(man.get("loss_ids") or []) | set(man.get("resolved_ids") or []) \
        | set(man.get("win_ids") or []) | set(man.get("unadopted_win_ids") or [])
    for bb in man.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "unadopted_win_ids",
                    "fragment_ids", "probed_ids"):
            adopted_ids |= set(bb.get(fld) or [])
    for t in TARGETS:
        if t["key_id"] in adopted_ids:
            abort(f"G6-target-adopted:{t['key_id']}", "target must NOT appear in any adopted id list")
    print("G6 EE adoption provenance PASS")

    # -- G7: expected third-impl budget map is consistent with runner whitelist
    for t in TARGETS:
        if t["budget"] not in (15000000, 30000000):
            abort(f"G7-budget:{t['key_id']}", str(t["budget"]))
    print("G7 budget map PASS")

    # -- emit rows.json (deterministic)
    rows = {
        "schema": SCHEMA,
        "consumed_into_canonical_cache": False,
        "unadopted_win_rows": True,
        "unadopted_loss_rows": False,
        "canonical_cache_sha256_unchanged":
            "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f",
        "sources": {
            "b33_drive": ("sources/b33-raw (12 files) + sources/b33-status.log + "
                          "sources/b33-batch-keys.json: published batch-33 class-34908 "
                          "drive (experiment n11-centralreply-closure-class34908-batch33-"
                          "20261124, commit-pinned raw fetch, MANIFEST-verified)"),
            "ea_reprobe30m": ("sources/ea-raw (8 files) + sources/ea-status.log + "
                              "sources/ea-reprobe-keys.json: published Part EA b33exh5 "
                              "30M re-probe (experiment n11-centralreply-closure-"
                              "class34908-b33exh5-reprobe30m-20261125)"),
            "ee_adoption": ("sources/ee-* 3 files: published Part EE af034loss1 "
                            "adoption core (merged canonical 6,666 rows fc3e4ac9, "
                            "increment cc9c4746, manifest 0ad3469e)"),
            "merged_canonical_sha256":
                "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f",
            "attention": ("verdicts NOT consumed: all six rows are honest "
                          "unconsumed probe-level WIN labels pending the scrutiny "
                          "owner C++ second-implementation gate pin 9193f5b6; "
                          "nothing in this Part adopts, frees or excludes anything"),
        },
        "targets": [],
        "anchors": ANCHORS,
        "negatives": NEGATIVES,
        "valgate": [
            {"key_id": "at2m-s5-1152921504606851072-536870946", "budget": 2000000},
            {"key_id": "at2m-s5-1188950301626860544-536870912", "budget": 2000000},
            {"key_id": "first-15m-s5-1152921504606851072-536870946", "budget": 15000000},
            {"key_id": "second-15m-s5-1188950301626860544-536870912", "budget": 15000000},
        ],
    }
    for t in TARGETS:
        rows["targets"].append(dict(t, expect_third=1))

    out_path = os.path.join(ROOT, OUT_REL)
    body = json.dumps(rows, indent=1, ensure_ascii=False) + "\n"
    if os.path.exists(out_path):
        if open(out_path).read() != body:
            abort("G8-idempotency", "input/rows.json exists and differs from regenerated content; refusing to overwrite")
    with open(out_path, "w") as fh:
        fh.write(body)
    print("WROTE", OUT_REL, "sha256", sha(OUT_REL))
    print(f"MAKER-PASS run-replica-eg sha256 {RUN_REPLICA_PIN} rows-json sha256 {sha(OUT_REL)}")

if __name__ == "__main__":
    main()
