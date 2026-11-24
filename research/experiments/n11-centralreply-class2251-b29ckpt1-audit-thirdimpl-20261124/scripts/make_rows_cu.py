# make_rows_cu.py -- machine-generate input/rows.json for the Part CU
# (batch-29 class 2251 checkpoint-1/3) third-implementation cross-verification.
#
# Every value is derived strictly from pinned local bytes under sources/ and
# val-gate/ (published Part CI takeover checkpoint-1/3 outputs, published
# batch-keys.json, published Part CR anchor/negative third-impl outputs).
# NO hand transcription of keys or node counts appears in this script: the
# 61-bit lo keys are read as exact Python ints from the published raw replay
# rows and the published input CSVs, and cross-checked against each other and
# against published batch-keys.json before a row is emitted. fails closed on
# any inconsistency (exit rc=1, no rows.json written).
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-class2251-b29ckpt1-audit-thirdimpl-20261124"
ROWS_SCHEMA = "n11-centralreply-class2251-b29ckpt1-thirdimpl-input-v1"
PIN_MERGED_CANONICAL = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def parse_replay_out(path):
    row = done = quads = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                row = line.strip().split(",")
            if line.startswith("# replay_done"):
                done = True
            if line.startswith("# forbidden quadruples: 95670"):
                quads = True
    return row, done, quads


def parse_third_out(path):
    with open(path) as fh:
        for line in fh:
            if line.startswith("third,"):
                f = line.rstrip("\n").split(",")
                if f[5] == "GATE_FAIL" or (len(f) > 5 and f[5].startswith('"')):
                    return {"gate_fail": ",".join(f[5:]).strip('"')}
                return {"row": f[1], "result": int(f[5]), "expansion": int(f[6]),
                        "ttHits": int(f[7]), "reason": f[11]}
    return None


def main():
    bk = json.load(open(os.path.join(ROOT, "sources", "batch-keys-b29.json")))
    assert bk["schema"] == "n11-centralreply-closure-class2251-batch29-input-v1", bk["schema"]

    targets = []
    for k in bk["keys"]:
        key = k["key_id"]
        if not (key.startswith("ab") and int(key[2:]) <= 16):
            continue  # only checkpoint-1/3 rows; ab017+ are the Part CI owner's lane
        p1, d1, q1 = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{key}.p1.out"))
        p2, d2, q2 = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{key}.p2.out"))
        csv = open(os.path.join(ROOT, "input", f"{key}.input.csv")).read().strip().split(",")
        # replay: id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
        problems = []
        if not (p1 and p2 and d1 and d2 and q1 and q2):
            problems.append("raw shape")
        if [p1[2], p1[3], p1[4], p1[5], p1[6], p1[7], p1[9], p1[10]] != \
           [p2[2], p2[3], p2[4], p2[5], p2[6], p2[7], p2[9], p2[10]]:
            problems.append("p1/p2 determinism fields")
        if int(csv[2]) != 5 or int(csv[5]) != k["legal"] or int(csv[3]) != int(k["lo"]) or int(csv[4]) != 0:
            problems.append("input csv vs batch-keys")
        if [p1[2], p1[3], p1[9], p1[10]] != ["5", str(k["legal"]), str(k["lo"]), "0"]:
            problems.append("raw vs batch-keys (stones/legal/lo)")
        if p1[5] != "15000000":
            problems.append("budget")
        if problems:
            print("MAKE ROWS FAIL", key, problems)
            sys.exit(1)
        targets.append({
            "key_id": key,
            "s5_index": k["s5_index"],
            "membership_class_count": k["membership_class_count"],
            "stones": 5,
            "lo": int(p1[9]),
            "hi": int(p1[10]),
            "legal": int(p1[3]),
            "replica_result": int(p1[6]),
            "replica_nodes": int(p1[7]),
            "published_raw_sha256_p1": sha256(os.path.join(ROOT, "sources", "raw", f"{key}.p1.out")),
            "published_raw_sha256_p2": sha256(os.path.join(ROOT, "sources", "raw", f"{key}.p2.out")),
            "expect_third": int(p1[6]),
            "source": "published Part CI takeover checkpoint-1/3 raw (commit a5a159d7 dir)",
        })
    assert len(targets) == 16 and all(t["replica_result"] == 2 for t in targets), "expected 16 LOSS rows"

    anchors = []
    for key, legal, exp in (("k02a", 87, 1), ("l1a", 116, 2)):
        csv = open(os.path.join(ROOT, "input", f"{key}.input.csv")).read().strip().split(",")
        if int(csv[2]) != 5 or int(csv[5]) != legal:
            print("MAKE ROWS FAIL anchor", key, csv)
            sys.exit(1)
        ra = parse_third_out(os.path.join(ROOT, "sources", "anchor-third-published", f"{key}.a.out"))
        rb = parse_third_out(os.path.join(ROOT, "sources", "anchor-third-published", f"{key}.b.out"))
        if not (ra and rb and "expansion" in ra and "expansion" in rb):
            print("MAKE ROWS FAIL anchor shape", key, ra, rb)
            sys.exit(1)
        if ra["expansion"] != rb["expansion"] or ra["ttHits"] != rb["ttHits"] or ra["result"] != rb["result"]:
            print("MAKE ROWS FAIL anchor det-pair", key, ra, rb)
            sys.exit(1)
        anchors.append({
            "key_id": key, "stones": 5, "lo": int(csv[3]), "hi": int(csv[4]), "legal": legal,
            "expect_third": exp,
            "anchor_expansions": ra["expansion"], "anchor_ttHits": ra["ttHits"],
            "source": "published Part CR anchor rows (byte-copy)",
        })

    negatives = []
    for key in ("ng1", "ng2"):
        r = parse_third_out(os.path.join(ROOT, "sources", "negative-third-published", f"{key}.a.out"))
        if not r or "gate_fail" not in r:
            print("MAKE ROWS FAIL negative", key, r)
            sys.exit(1)
        negatives.append({"key_id": key, "expect_gate_fail_text": r["gate_fail"],
                         "source": "published Part CR negative rows (byte-copy)"})

    rows = {
        "schema": ROWS_SCHEMA,
        "experiment": EXP,
        "sources": {
            "b29_ckpt1": "sources/raw ab001..ab016 p1+p2 + sources/status-ckpt13.log (published Part CI takeover checkpoint 1/3, commit a5a159d7, machine-fetched commit-pinned d06c4d92)",
            "b29_batch_keys_sha256": sha256(os.path.join(ROOT, "sources", "batch-keys-b29.json")),
            "b29_ckpt1_status_sha256": sha256(os.path.join(ROOT, "sources", "status-ckpt13.log")),
            "canonical_cache_sha256_unchanged": PIN_MERGED_CANONICAL,
        },
        "consumed_into_canonical_cache": False,
        "unadopted_loss_rows": True,
        "unadopted_win_rows": True,
        "canonical_cache_sha256_unchanged": PIN_MERGED_CANONICAL,
        "verdict_semantics": {"0": "budget exhaustion (honest UNKNOWN)", "1": "WIN", "2": "LOSS"},
        "targets": targets,
        "anchors": anchors,
        "negatives": negatives,
    }
    out = os.path.join(ROOT, "input", "rows.json")
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1); fh.write("\n")
    print(f"rows.json written: {len(targets)} targets (all expect_third=2, replica LOSS honest labels), "
          f"{len(anchors)} anchors, {len(negatives)} negatives")
    print("rows.json sha256:", sha256(out))


if __name__ == "__main__":
    main()
