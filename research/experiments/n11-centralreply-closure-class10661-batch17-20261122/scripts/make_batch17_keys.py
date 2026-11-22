#!/usr/bin/env python3
"""Batch-17 scaffold keys maker: closure class 10661 (Part AU, 2026-11-22).

Fail-closed, read-only generation of the batch-17 probe packet declared as
Part AU (note amendment, declaration push before this scaffold commit).
Target class: graph class index 10661, mask [1152921505697431552, 0],
the closure-candidate rank-14 class of the Part AS reaudit closure table
(first candidate row without refutation evidence: ranks 1-13 hold
in-flight or unconsumed-WIN-refuted classes), unknown_now 52, groups
served (24,30) and (24,90) (first-seen (24,30)).

Authoritative key source: the published Part AS reaudit probe-worklist
(sha-pinned), rows serving_class == 10661, exactly 52, probe_order
600..651 contiguous.  Every downstream fact is re-derived and gated here:

  * sha256 pins: graph, update8, Board, evidence policy, quarantine,
    canonical BASE cache (be9cb24e..., 6,120 rows), Part AS reaudit
    probe-worklist + closure-classes.csv, and the 16 published batch
    key packets (batches 1-16, fetched from the repo raw and sha-pinned);
  * the class mask/status come from the graph (mask match, graph status
    unknown(1), cost size 53 = 52 unknown + 1 known);
  * closure-table gate: the published rank-14 row IS class 10661 with
    unknown_now 52, groups_served_count 2, first group (24,30);
    re-derived group-best table must rank 10661 at 14 with exactly the
    groups {(24,30),(24,90)} and 809 candidate rows overall;
  * worklist gate: exactly 52 serving rows, class_unknown_now 52 on every
    row, probe_order 600..651 strictly increasing;
  * canonical-absence gate: 0/52 hits in the canonical 6,120-row cache
    (be9cb24e...); quarantine 0/52; canonical-safe key form 52/52;
    mask_to_index == worklist s5_index 52/52; every s5_index is a graph
    cost child of 10661; the unconsumed WIN child s5 745184 is NOT a key;
  * overlap gate: the 52 keys are disjoint from every published batch-1
    .. batch-16 key packet (16 sha-pinned files);
  * Board gate: independent.py Board recomputes every key's legal-move
    popcount and it must equal the published worklist legal 52/52.

Outputs: input/batch-keys.json (schema
n11-centralreply-closure-class10661-batch17-input-v1, key ids u001..u052
in probe_order) and input/u***.input.csv one-line solver targets
("target,0,5,lo,hi,legal,0,0,0,0,0").  Run 3x, byte-identical outputs.

Interpretation guard: this scaffold makes NO verdict claims.  The batch
itself (2-pass fresh-cold pinned replica, budget 15M, WIN-HALT rc=45 /
mismatch HARD-STOP rc=42 pre-registered) is executed by a later run
under the declared protocol.  The standard 11x11 empty board, the 19
central-reply roots, class 10661 and every key stay UNKNOWN; probe
counts and legal counts are bookkeeping, never verdicts.
"""
import csv
import gzip
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

_here = Path(__file__).resolve()
_CANDS = [q for q in _here.parents if (q / "research" / "experiments").is_dir()]
if not _CANDS:
    raise SystemExit("GATE FAILED: repo root not found above this script")
ROOT = _CANDS[0]
EXP = _here.parents[1]
OUTDIR = EXP / "input"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
AS_DIR = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/reaudit/output"

CLASS_INDEX = 10661
CLASS_MASK = [1152921505697431552, 0]
CLASS_RANK = 14
CLASS_GROUPS = [(24, 30), (24, 90)]
UNPROBED = 52
COST_SIZE = 53
KEY_PREFIX = "u"
WIN_S5_REFUTED_ABSENT = 745184
BUDGET = 15000000

PIN_SHA = {
    "graph": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
    "update8": "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719",
    "board": "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f",
    "policy": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "canonical_base_cache": "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685",
    "as_probe_worklist": "1c96df0533d69a57ec16943670e307480aba3511774460e8329f1a7198618c5a",
    "as_closure_classes": "3ee1dbb6db7a5fc8858f5bbdd5cae7ca754589f376ebb99727535806f917bc9e",
}

# batches 1..16 published key packets (raw main, sha256-pinned)
PRIOR_BATCHES = [
    ("n11-centralreply-closure-class16757-batch-20261122", 48,
     "2aaccc941d7aec35c416b27d5cdd10f7fbb82c9801bcf560b61e20be88c331f8"),
    ("n11-centralreply-closure-class23963-batch-20261122", 48,
     "3b37c92387336407d6399a689befb2fad99e01520a390294a2370daa11e631e3"),
    ("n11-centralreply-closure-class20421-batch-20261122", 49,
     "ad05073a845e511669d28fde3691fe9f3bf9f08eef2021039c884f1411f6dd3f"),
    ("n11-centralreply-closure-class16371-batch4-20261122", 50,
     "70b8a4c89f7cea454bfd2b52f720245b6d9c5d7311878bf8aac637940825ecdf"),
    ("n11-centralreply-closure-class12264-batch5-20261122", 51,
     "57da4702161ab781350ebf4236791266b31bdcd78b017eaa6e4a9391ecf5451d"),
    ("n11-centralreply-closure-class5473-batch6-20261122", 51,
     "c16d36e041da855ab654841f25d2bf5a64fb9ce4a2c1fde75e1217c7b082c59e"),
    ("n11-centralreply-closure-class10324-batch7-20261122", 51,
     "91d0f49254652cbc282cb8869b50d918ae16084c1bba1dcfcb725e15d7a3d434"),
    ("n11-centralreply-closure-class2634-batch8-20261122", 51,
     "5c42a950c687bbd1b8a9e25b1fdd5cffb4b7a19565a3d4372173a2001fcccc02"),
    ("n11-centralreply-closure-class1518-batch9-20261122", 51,
     "8f2035d17b3c987c8e5c848b23b6849ad5f3508a51d64002c1fef0e8c5ed7e9e"),
    ("n11-centralreply-closure-class8784-batch10-20261122", 52,
     "a1401ee2769f3943f993527dd4934ce82e99c6d55ee27a13cf74b1b417148ebf"),
    ("n11-centralreply-closure-class8785-batch11-20261122", 51,
     "8ef2206986a87f3859aa0a4b25f9936ffa82001d1fd3214013dc6351ecf8b08b"),
    ("n11-centralreply-closure-class8106-batch12-20261122", 52,
     "de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2"),
    ("n11-centralreply-closure-class16930-batch13-20261122", 52,
     "c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7"),
    ("n11-centralreply-closure-class23101-batch14-20261122", 52,
     "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"),
    ("n11-centralreply-closure-class5830-batch15-20261122", 52,
     "af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727"),
    ("n11-centralreply-closure-class10687-batch16-20261122", 52,
     "465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e"),
]
RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/research/experiments/"


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    for name, p, want in (("graph", GRAPH, PIN_SHA["graph"]),
                          ("update8", UPDATE8, PIN_SHA["update8"]),
                          ("board", BOARD_SOURCE, PIN_SHA["board"]),
                          ("policy", POLICY, PIN_SHA["policy"]),
                          ("quarantine", QUARANTINE, PIN_SHA["quarantine"]),
                          ("canonical cache", BASE_CACHE, PIN_SHA["canonical_base_cache"]),
                          ("probe-worklist", AS_DIR / "probe-worklist.csv", PIN_SHA["as_probe_worklist"]),
                          ("closure-classes", AS_DIR / "closure-classes.csv", PIN_SHA["as_closure_classes"])):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    board = Board(11)
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks, s4_status, s4_cost, s5_masks = g["s4_masks"], g["s4_status"], g["s4_cost"], g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    # class sanity
    if list(s4_masks[CLASS_INDEX]) != CLASS_MASK:
        fail(f"graph mask {s4_masks[CLASS_INDEX]} != declared class mask")
    if s4_status[CLASS_INDEX] != 1:
        fail(f"graph status of class {CLASS_INDEX} is {s4_status[CLASS_INDEX]}, not unknown(1)")
    cost_set = set(s4_cost[CLASS_INDEX])
    if len(cost_set) != COST_SIZE:
        fail(f"class cost size {len(cost_set)} != {COST_SIZE}")

    # closure-table gate (published row)
    with (AS_DIR / "closure-classes.csv").open() as fh:
        cc = list(csv.DictReader(fh))
    row = next((r for r in cc if int(r["class_rank"]) == CLASS_RANK), None)
    if row is None or int(row["class_index"]) != CLASS_INDEX:
        fail(f"published closure rank-{CLASS_RANK} row is not class {CLASS_INDEX}")
    if (int(row["unknown_now"]) != UNPROBED or int(row["groups_served_count"]) != len(CLASS_GROUPS)
            or (int(row["first_group_first"]), int(row["first_group_third"])) != CLASS_GROUPS[0]
            or [int(row["class_lo"]), int(row["class_hi"])] != CLASS_MASK):
        fail(f"published closure row content mismatch: {row}")

    # canonical cache + receipts -> re-derive the group-best closure view
    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        fail("update8 schema drift")
    receipts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    cache = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for lineno, r in enumerate(csv.reader(stream), 1):
            if not r or r[0].lstrip().startswith("#"):
                continue
            lo, hi, stones, verdict = int(r[1]), int(r[2]), int(r[3]), int(r[4])
            if r[0] != "s5verdict" or stones != 5 or verdict not in (1, 2):
                fail(f"invalid canonical row {lineno}")
            cache[(lo, hi)] = verdict
    if len(cache) != 6120:
        fail(f"canonical cache {len(cache)} rows != 6,120")
    iv = {}
    for (lo, hi), v in cache.items():
        i = mask_to_index.get((lo, hi))
        if i is not None:
            iv[i] = v
    for i, v in receipts.items():
        iv[i] = v
    LOSS, UNKNOWN, EXCLUDED = 0, 1, -1
    unknown_now = {}
    for i in range(len(s4_masks)):
        base = s4_status[i]
        if base == EXCLUDED:
            unknown_now[i] = set()
            continue
        if base not in (LOSS, UNKNOWN):
            fail(f"unexpected graph status {base} at class {i}")
        unknown_now[i] = {j for j in s4_cost[i] if iv.get(j) is None}
    best_class_groups = {}
    for r in g["roots"]:
        if r["role"] != "central":
            continue
        for t in r["thirds"]:
            best_o, best_r = None, None
            for o in t["options"]:
                base = s4_status[o]
                if base == UNKNOWN:
                    rr = len(unknown_now[o])
                elif base == LOSS:
                    rr = 0
                else:
                    continue
                if rr == 0:
                    best_o, best_r = o, 0
                    break
                if best_r is None or rr < best_r:
                    best_o, best_r = o, rr
            if best_r:
                best_class_groups.setdefault(best_o, []).append((r["origin_first"], t["third"]))
    if len(best_class_groups) != len(cc):
        fail(f"re-derived closure candidate count {len(best_class_groups)} != published {len(cc)}")
    groups = sorted(best_class_groups.get(CLASS_INDEX, []))
    if groups != sorted(CLASS_GROUPS):
        fail(f"re-derived groups for class {CLASS_INDEX} {groups} != declared {sorted(CLASS_GROUPS)}")
    ranked = sorted(best_class_groups.items(),
                    key=lambda kv: (len(unknown_now[kv[0]]), -len(kv[1])))
    if [ci for ci, _ in ranked].index(CLASS_INDEX) != CLASS_RANK - 1:
        fail("re-derived rank of class 10661 is not 14")

    # worklist gate + keys
    with (AS_DIR / "probe-worklist.csv").open() as fh:
        wl = list(csv.DictReader(fh))
    rows = [r for r in wl if r["serving_class"] == str(CLASS_INDEX)]
    if len(rows) != UNPROBED:
        fail(f"serving rows {len(rows)} != {UNPROBED}")
    orders = [int(r["probe_order"]) for r in rows]
    if orders != list(range(600, 600 + UNPROBED)):
        fail(f"probe_order not contiguous 600..{600 + UNPROBED - 1}: {orders[:5]}")
    quarantined = quarantined_cache_keys()
    keys = []
    for r in rows:
        lo, hi = int(r["lo"]), int(r["hi"])
        s5i, legal, mem = int(r["s5_index"]), int(r["legal"]), int(r["membership_class_count"])
        if int(r["class_unknown_now"]) != UNPROBED:
            fail(f"worklist class_unknown_now {r['class_unknown_now']} != {UNPROBED}")
        if (lo, hi) in cache:
            fail(f"key ({lo},{hi}) already in the canonical cache")
        if (lo, hi) in quarantined:
            fail(f"key ({lo},{hi}) quarantined")
        if not is_canonical_safe_s5_key((lo, hi)):
            fail(f"key ({lo},{hi}) noncanonical")
        if mask_to_index.get((lo, hi)) != s5i:
            fail(f"key ({lo},{hi}) s5_index mismatch")
        if s5i not in cost_set:
            fail(f"s5 {s5i} not a cost child of class {CLASS_INDEX}")
        if bin(board.legal(lo | (hi << 64))).count("1") != legal:
            fail(f"key ({lo},{hi}) Board legal recount mismatch")
        keys.append({
            "key_id": f"{KEY_PREFIX}{len(keys)+1:03d}",
            "s5_index": s5i,
            "lo": str(lo),
            "hi": str(hi),
            "legal": legal,
            "membership_class_count": mem,
            "probe_order": int(r["probe_order"]),
        })
    if any(k["s5_index"] == WIN_S5_REFUTED_ABSENT for k in keys):
        fail("unconsumed WIN child s5 745184 must not be a batch key")
    keyset = {(int(k["lo"]), int(k["hi"])) for k in keys}
    if len(keyset) != UNPROBED:
        fail("duplicate keys within the batch")

    # overlap gate vs batches 1..16
    prior_total = 0
    for dirname, nkeys, want in PRIOR_BATCHES:
        url = RAW + dirname + "/input/batch-keys.json"
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = resp.read()
        except Exception as e:
            fail(f"fetch {dirname}: {e}")
        if hashlib.sha256(data).hexdigest() != want:
            fail(f"batch-keys sha drift for {dirname}")
        pkt = json.loads(data)
        if len(pkt["keys"]) != nkeys:
            fail(f"batch {dirname} key count drift")
        prior = {(int(k["lo"]), int(k["hi"])) for k in pkt["keys"]}
        prior_total += len(prior)
        overlap = keyset & prior
        if overlap:
            fail(f"overlap with {dirname}: {sorted(overlap)}")
    if prior_total != 813:
        fail(f"prior key total {prior_total} != expected 813")

    batch_keys = {
        "schema": "n11-centralreply-closure-class10661-batch17-input-v1",
        "class_index": CLASS_INDEX,
        "class_mask": [str(CLASS_MASK[0]), str(CLASS_MASK[1])],
        "closure_class_rank_in_partas_reaudit": CLASS_RANK,
        "groups_served_count": len(CLASS_GROUPS),
        "groups_served_first_seen": {"first": CLASS_GROUPS[0][0], "third": CLASS_GROUPS[0][1]},
        "groups_served_full": [{"first": a, "third": b} for a, b in CLASS_GROUPS],
        "class_groups_total_in_closure_classes": 2,
        "budget": BUDGET,
        "keys": keys,
    }
    OUTDIR.mkdir(parents=True, exist_ok=True)
    bk_path = OUTDIR / "batch-keys.json"
    bk_path.write_text(json.dumps(batch_keys, indent=1) + "\n", encoding="utf-8")
    for k in keys:
        csv_path = OUTDIR / f"{k['key_id']}.input.csv"
        csv_path.write_text(
            "target,0,5," + k["lo"] + "," + k["hi"] + "," + str(k["legal"]) + ",0,0,0,0,0\n",
            encoding="utf-8")
    print(f"OK batch-17 keys: {len(keys)} keys class {CLASS_INDEX} rank {CLASS_RANK} "
          f"groups {CLASS_GROUPS} probe_order 600..{orders[-1]} "
          f"legal {min(k['legal'] for k in keys)}..{max(k['legal'] for k in keys)} "
          f"canonical_hits 0 quarantine_hits 0 overlap 0 prior_batches 16/{prior_total} keys")


if __name__ == "__main__":
    main()
