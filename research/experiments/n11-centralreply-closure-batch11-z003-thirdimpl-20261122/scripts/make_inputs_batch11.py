# make_inputs_batch11.py -- machine-derive the batch-11 (class 8785, Part Z)
# third-impl input CSVs for the Part AA cross-verification rows from the
# published batch-11 raws (no hand transcription). Fail-closed: any unexpected
# field aborts.
#
# Sources (all fetched from repo main via the raw CDN, commit-pinned):
#  - sources/raw/<key>.p1.out / .p2.out  (declaring-host jsreplay replica
#    2-pass node-exact rows; z003 = WIN-HALT row, z001/z002/z004 = the three
#    in-flight LOSS rows of the same first wave)
#  - sources/raw/<key>.p1.takeover.out / .p2.takeover.out (takeover-host
#    fresh-cold cross-host reproduction rows, published alongside the
#    declaring-host rows; machine-compared field-for-field here)
#  - sources/batch-keys.json (published batch-11 input declaration, 51 keys,
#    sha256 8ef2206986a87f3859aa0a4b25f9936ffa82001d1fa3214013dc6351ecf8b08b,
#    scaffold commit 3cc96099)
#  - sources/status.log (published batch-11 declaring-host runner log;
#    every target row must match its `PASS 15000000,<result>,<nodes>` line)
#  - sources/status.takeover.log (published takeover-host reproduction log;
#    every (key, pass) PASS line must match the raw values)
#
# Anchors/negatives identical to Part G/K/O/P/T/W (same published third-impl
# values).
# NOTE: batch-11 rows (z001-z004) are NOT consumed into the canonical chain
# cache; this experiment is verdict-level corroboration literature only
# (verdicts not consumed). Batch-11 probed 4/51 keys (z005-z051 untouched).
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BATCH_KEYS_SHA = "8ef2206986a87f3859aa0a4b25f9936ffa82001d1fd3214013dc6351ecf8b08b"

# Part AA targets: the batch-11 WIN row + all three probed LOSS rows
# (batch-11 halted in its first wave at the pre-registered WIN-HALT rule;
# replica nodes 2.26M / 3.15M / 6.42M / 11.60M(WIN))
TARGETS = [("z003", "win"), ("z001", "loss"), ("z002", "loss"), ("z004", "loss")]

ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]

def sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_replay_csv(path):
    """Return the single `replay,...` row of a jsreplay raw, field-split."""
    got = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                got.append(line.strip())
    if len(got) != 1:
        sys.exit(f"ABORT raw parse {path}: {len(got)} replay rows")
    return got[0].split(",")

def status_pass_lines(path):
    """Map (key, pass) -> (budget, result, nodes) from a status log's PASS lines."""
    m = {}
    with open(path) as fh:
        for line in fh:
            toks = line.split()
            if len(toks) >= 4 and toks[2] == "PASS":
                stat = toks[3].split(",")
                if len(stat) == 3:
                    subject = toks[1]
                    if "." in subject:
                        key, pN = subject.split(".")
                        m[(key, pN)] = stat
                    else:
                        m[("host", subject)] = stat
    return m

def parse_raw(key, kmap, tk_status):
    """Parse the declaring-host jsreplay replica rows for a batch-11 key;
    cross-check the p2 twin, the takeover-host twins, the published
    batch-keys.json declaration and both published status logs."""
    per_pass = []
    takeover = {}
    for p in ("p1", "p2"):
        path = os.path.join(SRC, "raw", f"{key}.{p}.out")
        if not os.path.isfile(path):
            sys.exit(f"ABORT missing raw {path}")
        per_pass.append(parse_replay_csv(path))
        tpath = os.path.join(SRC, "raw", f"{key}.{p}.takeover.out")
        if not os.path.isfile(tpath):
            sys.exit(f"ABORT missing takeover raw {tpath}")
        takeover[p] = parse_replay_csv(tpath)
    f1, f2 = per_pass
    # raw field layout: [0]='replay', [1]=id, [2]=stones, [3]=legal, [4]=is_or,
    # [5]=budget, [6]=result, [7]=nodes, [8]=wall_s, [9]=key_lo, [10]=key_hi
    for i in (3, 6, 7, 9, 10):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {key}: source raw passes differ at field {i}: {f1[i]} vs {f2[i]}")
    # cross-host: takeover twin must agree on every semantic field
    for p, tt in (("p1", "p1"), ("p2", "p2")):
        tw = takeover[tt]
        for i in (2, 3, 5, 6, 7, 9, 10):
            if tw[i] != per_pass[0 if tt == "p1" else 1][i]:
                sys.exit(f"ABORT {key}.{tt}: takeover raw {tw[i]} != declaring {per_pass[0 if tt=='p1' else 1][i]} at field {i}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT {key}: unexpected source schema {f1[:6]}")
    lo, hi, legal = int(f1[9]), int(f1[10]), int(f1[3])
    bk = kmap[key]
    # batch-11 batch-keys.json stores lo/hi as decimal STRINGS (121-bit keys
    # cannot round-trip JSON numbers); compare digit-for-digit in exact ints
    if lo != int(bk["lo"]) or hi != int(bk["hi"]) or legal != bk["legal"]:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    result, nodes = int(f1[6]), int(f1[7])
    # declaring-host status.log cross-check: `DATE <key> PASS 15000000,<result>,<nodes>`
    stat = None
    with open(os.path.join(SRC, "status.log")) as fh:
        for line in fh:
            toks = line.split()
            if len(toks) >= 4 and toks[1] == key and toks[2] == "PASS":
                stat = toks[3].split(",")
    if stat is None:
        sys.exit(f"ABORT {key}: no PASS line in status.log")
    if stat[0] != "15000000" or int(stat[1]) != result or int(stat[2]) != nodes:
        sys.exit(f"ABORT {key}: status.log {stat} != raw ({result},{nodes})")
    # takeover-host status.takeover.log cross-check (both passes):
    # `<key>.<pN> PASS 15000000,<result>,<nodes> (repro...)`
    for p in ("p1", "p2"):
        t = tk_status.get((key, p))
        if t is None:
            sys.exit(f"ABORT {key}.{p}: no PASS line in status.takeover.log")
        if t[0] != "15000000" or int(t[1]) != result or int(t[2]) != nodes:
            sys.exit(f"ABORT {key}.{p}: takeover status {t} != raw ({result},{nodes})")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    bk_sha = sha256(os.path.join(SRC, "batch-keys.json"))
    if bk_sha != PIN_BATCH_KEYS_SHA:
        sys.exit(f"ABORT batch-keys.json sha {bk_sha} != pin {PIN_BATCH_KEYS_SHA}")
    keys_json = json.load(open(os.path.join(SRC, "batch-keys.json")))
    kmap = {k["key_id"]: k for k in keys_json["keys"]}
    if len(kmap) != 51:
        sys.exit(f"ABORT batch-keys.json keys {len(kmap)} != 51")
    tk_status = status_pass_lines(os.path.join(SRC, "status.takeover.log"))
    rows = []
    for key, kind in TARGETS:
        r = parse_raw(key, kmap, tk_status)
        expect = 1 if kind == "win" else 2
        if r["replica_result"] != expect:
            sys.exit(f"ABORT {key}: replica result {r['replica_result']} != expected {expect}")
        r["expect_third"] = expect
        rows.append(r)
    # z003 must additionally be the published WIN-HALT row; batch-11 status.log
    # (unlike batch-8's) DOES carry RUNNER-STOP / RUNNER-EXIT lines - asserted
    # present here for schema honesty
    with open(os.path.join(SRC, "status.log")) as fh:
        slog = fh.read()
    if "z003 WIN-HALT" not in slog:
        sys.exit("ABORT status.log lacks the z003 WIN-HALT stop line")
    if "RUNNER-STOP" not in slog or "RUNNER-EXIT" not in slog:
        sys.exit("ABORT batch-11 status.log lacks its RUNNER-STOP/RUNNER-EXIT lines")
    if int(keys_json["class_index"]) != 8785:
        sys.exit(f"ABORT batch-keys class_index {keys_json['class_index']} != 8785")
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    negatives = [
        {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
         "stones": 5, "why": "legal+1 vs derived 87"},
        {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
         "stones": 6, "why": "stones 6 vs actual 5"},
    ]
    rows_json = {"schema": "n11-centralreply-closure-batch11-z003-thirdimpl-input-v1",
                 "sources": {
                     "batch_keys_sha256": PIN_BATCH_KEYS_SHA,
                     "raws": "sources/raw (published batch-11 raws 16 files: declaring-host 8 + takeover-host 8, commits 12be47c7/40e02623, fetched from the repo raw CDN, commit-pinned)",
                     "status_log": "sources/status.log (published batch-11 declaring-host runner log) + sources/status.takeover.log (takeover-host reproduction log)"},
                 "consumed_into_canonical_cache": False,
                 "targets": rows, "anchors": anchor_rows, "negatives": negatives}
    with open(os.path.join(OUT, "rows.json"), "w") as fh:
        json.dump(rows_json, fh, indent=1)
        fh.write("\n")
    for r in rows + anchor_rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in negatives:
        csv = f"target,0,{r['stones']},{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(negatives))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"],
              "replica_result", r["replica_result"], "replica_nodes", r["replica_nodes"],
              "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
