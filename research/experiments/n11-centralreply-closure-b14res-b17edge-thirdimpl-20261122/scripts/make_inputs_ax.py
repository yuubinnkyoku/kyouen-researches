# make_inputs_ax.py -- machine-derive the Part AX third-impl input CSVs and
# rows.json for the batch-14 residual (class 23101, Part AW) 10 LOSS rows
# q043..q052 plus the batch-17 (class 10661, Part AU) budget-edge trio
# u031/u033/u038 on budget, from the published raws (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Sources (all fetched from the repo main raw CDN, commit-pinned):
#  - sources/raw/q043..q052.{p1,p2}.out + sources/status-aw.log +
#    sources/row-audit-aw.json (sha256 6b40b131.., schema
#    n11-centralreply-closure-class23101-batch14residual-rowaudit-v1) -- the
#    published Part AW batch-14-residual replica outputs, publication commit
#    cb94f808 (scaffold a5b514d7 / raw ecfe258d).
#  - sources/published-input/qXXX.input.csv -- the published per-key input
#    CSVs of Part AW (byte-equality asserted for all 10).
#  - sources/batch-keys-b14.json (published batch-14 input declaration, 52
#    keys, class 23101, sha256 dfde0e90.., publication commit 7b211d38).
#  - sources/raw/u031/u033/u038.{p1,p2}.out + sources/status-b17.log +
#    sources/row-audit-b17.json (sha256 c19e768f..) -- the published batch-17
#    (Part AU) replica outputs, publication commit ffc09de1.
#  - sources/published-input/uXXX.input.csv -- published batch-17 input CSVs
#    (byte-equality asserted for all 3).
#  - sources/batch-keys-b17.json (batch-17 input declaration, 52 keys, class
#    10661, sha256 db762175.., commit ffc09de1).
#  - sources/published-input-ar/{k02a,l1a,ng1,ng2}.input.csv -- published Part
#    AR third-impl anchor/negative input CSVs (byte-equality asserted).
#
# Anchors/negatives identical to Part G/K/O/P/T/W/AA/AD/AG/AL/AR (same
# published third-impl values).
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 23101, class 10661 and every key remain UNKNOWN.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BK_B14 = "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"
PIN_BK_B17 = "db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2"
PIN_RA_AW = "6b40b131c54302b61ad9c767f948b7fc4e9c1f6a67e42915faca9d457f709003"
PIN_RA_B17 = "c19e768f1ce4223de6736713a679028990ef5a884c9886affd62c951e307d5f9"

# Part AX targets: the 10 Part AW batch-14-residual LOSS rows (the batch-14
# key set of class 23101 is fully enumerated on this lane: 42 rows Part AQ +
# these 10) and the 3 batch-17 budget-edge rows from the Part AU execution
# (u031 = max-nodes row 14,967,263 directly under the 15M budget, u033 and
# u038 mid-range companions accepted as the Part AV adoption-declaration
# edge set). All 13 published replica rows are LOSS (result 2).
TARGETS_AW = ["q043", "q044", "q045", "q046", "q047", "q048", "q049", "q050", "q051", "q052"]
TARGETS_B17 = ["u031", "u033", "u038"]
EXPECT_PROBE_ORDER_AW = {  # from the published batch-14 batch-keys.json
    "q043": 580, "q044": 581, "q045": 582, "q046": 583, "q047": 584,
    "q048": 585, "q049": 586, "q050": 587, "q051": 588, "q052": 589,
}
EXPECT_PROBE_ORDER_B17 = {"u031": 630, "u033": 632, "u038": 637}

ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]
NEGATIVES = [
    {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
     "stones": 5, "why": "legal+1 vs derived 87"},
    {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
     "stones": 6, "why": "stones 6 vs actual 5"},
]

def sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_replay_csv(path):
    got = []
    done = False
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                got.append(line.strip())
            if line.startswith("# replay_done"):
                done = True
    if len(got) != 1 or not done:
        sys.exit(f"ABORT raw parse {path}: {len(got)} replay rows, replay_done={done}")
    return got[0].split(",")

def parse_raw(key, kmap, audit_row, status_text):
    per_pass = []
    for p in ("p1", "p2"):
        path = os.path.join(SRC, "raw", f"{key}.{p}.out")
        if not os.path.isfile(path):
            sys.exit(f"ABORT missing raw {path}")
        per_pass.append(parse_replay_csv(path))
    f1, f2 = per_pass
    # raw field layout: [0]='replay', [1]=id, [2]=stones, [3]=legal, [4]=is_or,
    # [5]=budget, [6]=result, [7]=nodes, [8]=wall_s, [9]=key_lo, [10]=key_hi
    for i in (3, 6, 7, 9, 10):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {key}: source raw passes differ at field {i}: {f1[i]} vs {f2[i]}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT {key}: unexpected source schema {f1[:6]}")
    lo, hi, legal = int(f1[9]), int(f1[10]), int(f1[3])
    bk = kmap[key]
    if lo != int(bk["lo"]) or hi != int(bk["hi"]) or legal != bk["legal"]:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    if audit_row is not None:
        if (lo != audit_row["lo"] or hi != audit_row["hi"] or legal != audit_row["legal"]
                or int(f1[6]) != audit_row["result"] or int(f1[7]) != audit_row["nodes"]
                or audit_row.get("node_exact", True) is not True or audit_row["budget"] != 15000000):
            sys.exit(f"ABORT {key}: raw vs published row-audit mismatch {audit_row}")
    result, nodes = int(f1[6]), int(f1[7])
    stat = None
    for line in status_text.splitlines():
        toks = line.split()
        if len(toks) >= 4 and toks[1] == key and toks[2] == "PASS":
            if stat is not None:
                sys.exit(f"ABORT {key}: multiple PASS lines in status log")
            stat = toks[3].split(",")
    if stat is None:
        sys.exit(f"ABORT {key}: no PASS line in status log")
    if stat[0] != "15000000" or int(stat[1]) != result or int(stat[2]) != nodes:
        sys.exit(f"ABORT {key}: status.log {stat} != raw ({result},{nodes})")
    if result != 2 or nodes >= 15000000:
        sys.exit(f"ABORT {key}: expected in-budget LOSS row, got result={result} nodes={nodes}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b14.json", PIN_BK_B14), ("batch-keys-b17.json", PIN_BK_B17),
                        ("row-audit-aw.json", PIN_RA_AW), ("row-audit-b17.json", PIN_RA_B17)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    bk14 = json.load(open(os.path.join(SRC, "batch-keys-b14.json")))
    bk17 = json.load(open(os.path.join(SRC, "batch-keys-b17.json")))
    if int(bk14["class_index"]) != 23101 or int(bk17["class_index"]) != 10661:
        sys.exit(f"ABORT class_index {bk14.get('class_index')}/{bk17.get('class_index')}")
    k14 = {k["key_id"]: k for k in bk14["keys"]}
    k17 = {k["key_id"]: k for k in bk17["keys"]}
    if len(k14) != 52 or len(k17) != 52:
        sys.exit(f"ABORT batch keys count {len(k14)}/{len(k17)} != 52/52")
    ra_aw = json.load(open(os.path.join(SRC, "row-audit-aw.json")))
    ra_b17 = json.load(open(os.path.join(SRC, "row-audit-b17.json")))
    # -- published row-audit battery gates
    if ra_aw["probed_rows"] != 10 or ra_aw["mismatch"] != 0 or ra_aw["budget"] != 15000000:
        sys.exit(f"ABORT row-audit-aw header {ra_aw['probed_rows']},{ra_aw['mismatch']},{ra_aw['budget']}")
    if ra_aw["wins"] or ra_aw["win_continues"] or ra_aw["exhausted_result0"]:
        sys.exit("ABORT row-audit-aw has WIN/exhaustion rows")
    if ra_aw["all_result2_2pass_node_exact"] is not True or ra_aw["status_pass_rows_cross_checked"] is not True \
            or ra_aw["replay_done_complete_all_passes"] is not True:
        sys.exit("ABORT row-audit-aw honesty flags not all true")
    if ra_aw["total_nodes_per_pass"] != 23252550:
        sys.exit(f"ABORT row-audit-aw total nodes {ra_aw['total_nodes_per_pass']}")
    if sorted(ra_aw["probed_ids"]) != sorted(TARGETS_AW):
        sys.exit(f"ABORT row-audit-aw probed set != Part AX AW target set")
    if ra_b17["probed"] != 52 or ra_b17["budget"] != 15000000 or ra_b17["two_pass_node_exact"] != 52:
        sys.exit(f"ABORT row-audit-b17 header {ra_b17.get('probed')},{ra_b17.get('two_pass_node_exact')}")
    if ra_b17["total_nodes_pass_one"] != 196536452 or ra_b17["nodes_range"] != [1651860, 14967263]:
        sys.exit(f"ABORT row-audit-b17 totals {ra_b17.get('total_nodes_pass_one')},{ra_b17.get('nodes_range')}")
    # u031/u033 published p2 passes are fresh-cold retries after host resets
    for frag in ra_b17["host_event_truncated_fragments"]:
        if frag["carries_verdict"] is not False:
            sys.exit(f"ABORT truncated fragment carries verdict: {frag}")
    audit_rows_aw = {r["key_id"]: r for r in ra_aw["rows"]}
    audit_rows_b17 = {r["key_id"]: r for r in ra_b17["rows"]}
    # -- status log battery gates (Part AW runner log)
    aw_slog = open(os.path.join(SRC, "status-aw.log")).read()
    if "PART-AW SCAFFOLD maker gates PASS" not in aw_slog:
        sys.exit("ABORT status-aw.log lacks its SCAFFOLD maker gates line")
    if "VAL-GATE 4/4 node-exact this-host" not in aw_slog:
        sys.exit("ABORT status-aw.log lacks its VAL-GATE 4/4 line")
    if "WAVE-END q052 stop=0 all-10-done" not in aw_slog:
        sys.exit("ABORT status-aw.log lacks the WAVE-END stop=0 all-10-done line")
    if "RUNNER-NOTE" not in aw_slog:
        sys.exit("ABORT status-aw.log lacks its RUNNER-NOTE line")
    import re
    for line in aw_slog.splitlines():
        if re.match(r"^\S+ \S+ PASS ", line):
            toks = line.split()
            if toks[3].split(",")[1] != "2":
                sys.exit(f"ABORT status-aw.log non-LOSS PASS line: {line}")
    if len(re.findall(r"^\S+ q0\d\d PASS ", aw_slog, re.M)) != 10:
        sys.exit("ABORT status-aw.log PASS line count != 10")
    # -- status log battery gates (batch-17 runner log, honesty records)
    b17_slog = open(os.path.join(SRC, "status-b17.log")).read()
    if "EXECUTION-COMPLETE: 52/52 probed = 52 LOSS" not in b17_slog:
        sys.exit("ABORT status-b17.log lacks the EXECUTION-COMPLETE 52/52 LOSS line")
    if "u031 P2-TRUNCATED-RETRY" not in b17_slog or "u033 P2-TRUNCATED-RETRY" not in b17_slog:
        sys.exit("ABORT status-b17.log lacks the u031/u033 P2-TRUNCATED-RETRY honesty lines")
    # 5 fragments across the whole 52-key batch (u017/u018/u027/u031/u033);
    # the Part AX edge rows u031/u033 must be among the retried keys
    if b17_slog.count("P2-TRUNCATED-RETRY") != 5:
        sys.exit("ABORT status-b17.log P2-TRUNCATED-RETRY count != 2")
    # HARD-STOP appears only in the pre-registered stop-rules prose (line 58);
    # no fired HARD-STOP event line (timestamped runner line) may exist
    for line in b17_slog.splitlines():
        if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z ", line) and "HARD-STOP" in line:
            sys.exit(f"ABORT status-b17.log fired HARD-STOP line: {line}")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS_AW:
        if key not in k14 or k14[key]["probe_order"] != EXPECT_PROBE_ORDER_AW[key]:
            sys.exit(f"ABORT {key}: batch-14 probe_order {k14.get(key, {}).get('probe_order')}")
        r = parse_raw(key, k14, audit_rows_aw.get(key), aw_slog)
        r["source"] = "part-aw-b14residual"
        r["probe_order"] = EXPECT_PROBE_ORDER_AW[key]
        r["s5_index"] = k14[key]["s5_index"]
        rows.append(r)
    for key in TARGETS_B17:
        if key not in k17 or k17[key]["probe_order"] != EXPECT_PROBE_ORDER_B17[key]:
            sys.exit(f"ABORT {key}: batch-17 probe_order {k17.get(key, {}).get('probe_order')}")
        r = parse_raw(key, k17, audit_rows_b17.get(key), b17_slog)
        r["source"] = "part-au-b17-edge"
        r["probe_order"] = EXPECT_PROBE_ORDER_B17[key]
        r["s5_index"] = k17[key]["s5_index"]
        rows.append(r)
    for r in rows:
        r["expect_third"] = 2
    # -- anchors/negatives (published constants, AR-identical)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b14res-b17edge-thirdimpl-input-v1",
                 "sources": {
                     "aw": "sources/raw q043..q052 20 files + status-aw.log + row-audit-aw.json (published Part AW batch-14-residual outputs, publication commit cb94f808, fetched from the repo raw CDN, commit-pinned; row-audit sha256 6b40b131..)",
                     "aw_batch_keys_sha256": PIN_BK_B14,
                     "b17": "sources/raw u031/u033/u038 6 files + status-b17.log + row-audit-b17.json (published batch-17 Part AU outputs, publication commit ffc09de1, commit-pinned; row-audit sha256 c19e768f..)",
                     "b17_batch_keys_sha256": PIN_BK_B17,
                     "anchors": "published Part G/K/O/P/T/W/AA/AD/AG/AL/AR anchor/negative values, input CSVs byte-equality-checked against the published Part AR experiment"},
                 "consumed_into_canonical_cache": False,
                 "targets": rows, "anchors": anchor_rows, "negatives": NEGATIVES}
    with open(os.path.join(OUT, "rows.json"), "w") as fh:
        json.dump(rows_json, fh, indent=1)
        fh.write("\n")
    # -- derived-vs-published input CSV byte-equality gates + input emission
    for r in rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT {r['key_id']}: derived CSV {csv!r} != published {pub!r}")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in anchor_rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-ar", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT anchor {r['key_id']}: derived CSV {csv!r} != published Part AR {pub!r}")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in NEGATIVES:
        csv = f"target,0,{r['stones']},{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-ar", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT negative {r['key_id']}: derived CSV {csv!r} != published Part AR {pub!r}")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"],
              r["source"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
