# make_inputs_az.py -- machine-derive the Part AZ third-impl input CSVs and
# rows.json for the batch-18 (class 16131, Part AY) WIN rows v001/v002 from
# the published batch-18 artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Sources (all fetched from the repo main raw CDN, commit-pinned to the
# published batch-18 publication commit 938e34f2... MANIFEST 73 rows):
#  - sources/raw/v001.{p1,p2}.out + raw/v002.{p1,p2}.out --
#    the published batch-18 replica WIN outputs (raws commit 3c07f51a).
#  - sources/status-b18.log -- the published batch-18 runner status.log
#    (sha256 4b785add... per the published MANIFEST).
#  - sources/batch-keys-b18.json -- published batch-18 input declaration
#    (53 keys, class 16131, sha256 1bb3ed41...).
#  - sources/README-b18.md -- published batch-18 README (results section).
#  - sources/published-input/{v001,v002}.input.csv -- published batch-18
#    per-key input CSVs (byte-equality asserted for both targets).
#  - sources/published-input-ar/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part AR third-impl anchor/negative input CSVs (byte-equality asserted).
#
# Anchors/negatives identical to Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX (same
# published third-impl values).
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 16131 and every key remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BK_B18 = "1bb3ed41b26af92491ed579a7c05471f271ed1394d8b5f817b5110794d926667"
PIN_STATUS_B18 = "4b785add0f3e7dba7f689ec860458d0ead72e2cc77ef5f8b28026de36ef0bd21"
PIN_README_B18 = "8b6a85b34f0dcd9206ff03d660bed16277bd3a78b0499ffaef24f1cd08a0d3d1"
PIN_RAW = {
    "v001.p1": "24b45c8a353a312cb0c6409592873b750e1ab8767257a9aca8c65a3894be3e25",
    "v001.p2": "1fc367bd99606a064557bbb6bc3f8246a2239bc34bb510ee92c213af4f65bd34",
    "v002.p1": "41c10ec220bc25abb7f9713e651229071096765b2a73f99951256d5710086a2e",
    "v002.p2": "e9f578fcbfa0a59a6f5746bbbb94ea5711eae5f7da57fd9af530ec0414da45de",
}
PIN_PUB_INPUT = {
    "v001": "edee9be8fdbd5fe49449b4e78f63ef656d61c17489b978929e267499bbaf5a73",
    "v002": "e8bbbaedc9c3a0c1d504ca81756937d84357639fc54a718e327d6d80eb8b627b",
}

TARGETS = ["v001", "v002"]
EXPECT_S5 = {"v001": 153671, "v002": 207534}
EXPECT_REPLICA = {"v001": 5656151, "v002": 7898204}  # published 2-pass node-exact WIN rows

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

def parse_raw(key, kmap, status_text):
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
    if f1[1] != "0":
        sys.exit(f"ABORT {key}: unexpected replay id {f1[1]}")
    lo, hi, legal = int(f1[9]), int(f1[10]), int(f1[3])
    bk = kmap[key]
    if int(bk["lo"]) != lo or int(bk["hi"]) != hi or int(bk["legal"]) != legal:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    result, nodes = int(f1[6]), int(f1[7])
    if result != 1:
        sys.exit(f"ABORT {key}: expected in-budget WIN (result 1) row, got result={result}")
    if nodes >= 15000000:
        sys.exit(f"ABORT {key}: WIN row at/near budget: nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    # status.log cross-verification: PASS line + WIN-HALT + WIN-ROW-DETAIL
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
    if f"{key} WIN-HALT" not in status_text:
        sys.exit(f"ABORT {key}: no WIN-HALT line in status log")
    m = re.search(rf"WIN-ROW-DETAIL {key} .*nodes (\d+) == p2 nodes \d+ .*legal (\d+), budget (\d+), result (\d+), keys (\d+)/(\d+)", status_text)
    if m is None:
        sys.exit(f"ABORT {key}: no WIN-ROW-DETAIL line in status log")
    if (int(m.group(1)) != nodes or int(m.group(2)) != legal or int(m.group(3)) != 15000000
            or int(m.group(4)) != result or int(m.group(5)) != lo or int(m.group(6)) != hi):
        sys.exit(f"ABORT {key}: WIN-ROW-DETAIL {m.groups()} != raw ({nodes},{legal},{lo},{hi})")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b18.json", PIN_BK_B18), ("status-b18.log", PIN_STATUS_B18),
                       ("README-b18.md", PIN_README_B18)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk18 = json.load(open(os.path.join(SRC, "batch-keys-b18.json")))
    if int(bk18["class_index"]) != 16131:
        sys.exit(f"ABORT class_index {bk18.get('class_index')}")
    k18 = {k["key_id"]: k for k in bk18["keys"]}
    if len(k18) != 53:
        sys.exit(f"ABORT batch keys count {len(k18)} != 53")
    # -- status log battery gates (published batch-18 runner log)
    slog = open(os.path.join(SRC, "status-b18.log")).read()
    if "VAL-GATE 4/4 node-exact this-host re-verified" not in slog:
        sys.exit("ABORT status-b18.log lacks the AY VAL-GATE 4/4 line")
    if "EXECUTION-HALTED batch-18 stopped at first wave" not in slog:
        sys.exit("ABORT status-b18.log lacks the EXECUTION-HALTED line")
    if "2/53 keys probed, 51 keys UNPROBED" not in slog:
        sys.exit("ABORT status-b18.log lacks the 51-unprobed honesty line")
    if "Unconsumed closure WIN candidates now 17" not in slog:
        sys.exit("ABORT status-b18.log lacks the 17-candidates line")
    # 3 total WIN-HALT mentions: v001 + v002 runner lines + the EXECUTION-HALTED prose
    if len([l for l in slog.splitlines() if l.endswith(" WIN-HALT")]) != 2:
        sys.exit("ABORT status-b18.log WIN-HALT runner lines != 2")
    # -- README results battery gates (published batch-18 README)
    rd = open(os.path.join(SRC, "README-b18.md")).read()
    for key in TARGETS:
        if f"**v{key[1:]}: WIN (result 1)**" not in rd:
            sys.exit(f"ABORT README lacks the {key} WIN results line")
        nn = f"{EXPECT_REPLICA[key]:,}"
        if nn not in rd:
            sys.exit(f"ABORT README lacks the {key} node count {nn}")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k18.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-18 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k18, slog)
        r["source"] = "part-ay-batch18-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR-identical)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b18win-thirdimpl-input-v1",
                 "sources": {
                     "b18": ("sources/raw v001/v002 4 files + sources/status-b18.log + batch-keys-b18.json + "
                             "published batch-18 (Part AY) outputs, publication commit 938e34f2, "
                             "commit-pinned raw fetch; batch-18 batch-keys sha256 1bb3ed41.."),
                     "b18_batch_keys_sha256": PIN_BK_B18,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part AR experiment")},
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
        if sha256(os.path.join(SRC, "published-input", f"{r['key_id']}.input.csv")) != PIN_PUB_INPUT[r["key_id"]]:
            sys.exit(f"ABORT {r['key_id']}: published input CSV sha mismatch")
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
    print("AZ-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
