#!/usr/bin/env python3
"""Build the joint unconsumed-rows IF-ADOPTED increments, fail-closed (Part AJ).

Covers the nine WIN-HALT batch experiments of the n11 central-reply closure
grind whose probed rows are still unconsumed by the canonical chain cache:
batch 1 (class 16757), batch 3 (20421), batch 4 (16371), batch 5 (12264),
batch 6 (5473), batch 8 (2634), batch 9 (1518), batch 11 (8785) and
batch 12 (8106).  Batch 13 (16930) is EXCLUDED: its if-adopted decomposition
is owned by the in-flight Part AI declaration.  Batch 14 (23101, Part AF) is
untouched.  Clean batches 2 (23963), 7 (10324) and 10 (8784) are already
inside the canonical Part Y merged cache (BASE) and are therefore not part
of this packet.

Emits three what-if increment caches over the published raw replay rows:
  * JWIN10     - the 10 unconsumed closure WIN rows only
                 (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006)
  * JLOSS122   - the 122 probed exact-LOSS rows NOT already in BASE
  * JALL132    - all 132 resolved probed rows unique-new here (10 WIN + 122 LOSS)

HONEST CORRECTION published by Part AJ itself: the first run of this script
ABORTed fail-closed at "b001: key already in canonical BASE cache".  Precise
re-measurement of the batch keys against BASE found that exactly 19 batch-1
LOSS rows (b001..b017, b019, b020) are ALREADY inside the canonical BASE
cache with identical verdicts AND identical node counts (batches 2/7/10 of
the canonical chain reached their membership classes); batch-1's WIN b018
is NOT in BASE; batches 3,4,5,6,8,9,11,12 have ZERO BASE overlap; and NO
verdict conflicts exist anywhere.  Those 19 rows are therefore excluded
from every increment as pre-consumed duplicates, under a stricter gate
(verdict AND node count must match BASE exactly, else ABORT), bringing the
packet from 151 probed rows to 132 unique-new (10 WIN + 122 LOSS).
h002 (batch 8) exhausted its 15M budget with result 0 (honest UNKNOWN) and is
EXCLUDED from every increment by gate (its 15M re-search stays forbidden).

Fail-closed gates: every row must come from BOTH published raw passes with
identical (stones, legal, is_or, budget, result, nodes); batch-11 z-keys
additionally match their published takeover-host passes (4-way); legal and
(lo,hi) must match the published batch-keys.json for every key; every
declaring-host status.log PASS row must agree with the raws on
(budget, result, nodes); the WIN set must be exactly the 10 unconsumed
closure WINs; all (lo,hi) must be distinct across the packet, absent from the
canonical BASE cache (6,027 rows, sha256 95e868d6...) EXCEPT the exactly-19
pre-consumed batch-1 LOSS rows which must match BASE on verdict AND nodes
(the only permitted BASE overlap; any other overlap still ABORTs), and absent
from the quarantine registry.  Verdicts are byte-taken from the raws.
Read-only what-if analysis inputs; verdicts are NOT consumed. 11x11 stays
UNKNOWN; nodes are bookkeeping, never verdicts.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
BASE_CACHE = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

BATCHES = {
    1: ("n11-centralreply-closure-class16757-batch-20261122", "16757", None),
    3: ("n11-centralreply-closure-class20421-batch-20261122", "20421", None),
    4: ("n11-centralreply-closure-class16371-batch4-20261122", "16371", None),
    5: ("n11-centralreply-closure-class12264-batch5-20261122", "12264", None),
    6: ("n11-centralreply-closure-class5473-batch6-20261122", "5473", None),
    8: ("n11-centralreply-closure-class2634-batch8-20261122", "2634", None),
    9: ("n11-centralreply-closure-class1518-batch9-20261122", "1518", None),
    11: ("n11-centralreply-closure-class8785-batch11-20261122", "8785", 4),
    12: ("n11-centralreply-closure-class8106-batch12-20261122", "8106", None),
}
WIN_IDS = {
    1: ["b018"], 3: ["d002"], 4: ["e002"], 5: ["f017"], 6: ["g018"],
    8: ["h045"], 9: ["j033"], 11: ["z003"], 12: ["n005", "n006"],
}
EXHAUSTION = {(8, "h002")}
# the 19 batch-1 LOSS rows already consumed into canonical BASE (measured,
# verdict- and node-identical; found by this script's own first-run gate)
EXPECTED_CONSUMED = {(1, f"b{n:03d}") for n in
                     (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20)}
# resolved probed sets (from the published declaring-host status.log PASS rows)
RESOLVED = {
    1: [f"b{n:03d}" for n in (1, 2, 4, 3, 7, 5, 6, 8, 9, 11, 10, 12, 15, 13, 14, 16, 17, 19, 20, 18)],
    3: ["d001", "d003", "d002", "d004"],
    4: ["e001", "e002"],
    5: [f"f{n:03d}" for n in (1, 2, 3, 4, 6, 5, 8, 7, 9, 10, 11, 12, 14, 13, 16, 15, 17)] + ["f018"],
    6: [f"g{n:03d}" for n in range(1, 19)],
    8: [f"h{n:03d}" for n in range(1, 46) if n != 2],  # h002 = 15M exhaustion (result 0), excluded
    9: [f"j{n:03d}" for n in range(1, 34)],
    11: ["z001", "z002", "z004", "z003"],
    12: ["n002", "n004", "n003", "n001", "n007", "n008", "n006", "n005"],
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_replay(path: Path):
    row = None
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            if row is not None:
                sys.exit(f"ABORT multiple replay rows in {path}")
            row = {
                "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]),
                "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]), "wall_s": int(parts[8]),
                "lo": int(parts[9]), "hi": int(parts[10]),
            }
    if row is None:
        sys.exit(f"ABORT no replay row in {path}")
    return row


def parse_status(path: Path):
    got = {}
    for line in path.read_text().splitlines():
        m = re.match(r"^\S+ (\S+) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid, b, r, n = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            kid = kid.split(".")[0]
            if kid in got and got[kid] != (b, r, n):
                sys.exit(f"ABORT status disagreement for {kid}")
            got[kid] = (b, r, n)
    return got


def quorum(batch: int):
    return 4 if BATCHES[batch][2] == 4 else 3


def main() -> None:
    if sha(BASE_CACHE) != "95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326":
        sys.exit("ABORT base cache sha drift")
    OUT.mkdir(parents=True, exist_ok=True)
    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    q = json.loads(json.dumps(json.loads(QUARANTINE.read_text())))
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    rows = []  # (batch, class, kid, s5_index, lo, hi, result, nodes)
    consumed = []  # pre-consumed BASE duplicates (excluded from increments)
    all_lohi = {}
    for batch, (dirname, klass, _) in BATCHES.items():
        bdir = ROOT / "research/experiments" / dirname
        keys = json.loads((bdir / "input/batch-keys.json").read_text())["keys"]
        by_id = {k["key_id"]: k for k in keys}
        status = parse_status(bdir / "output/status.log")
        win_ids = WIN_IDS[batch]
        idseq = [k for k in RESOLVED[batch]]
        # exhaustive-check: every status PASS kid with a verdict row must be in idseq
        status_resolved = {k for k, v in status.items() if v[1] in (1, 2)}
        if status_resolved != set(idseq):
            sys.exit(f"ABORT batch {batch}: status resolved set != expected probed set: "
                     f"extra={sorted(status_resolved - set(idseq))} missing={sorted(set(idseq) - status_resolved)}")
        for kid in idseq:
            variants = {}
            for tag in ("p1", "p2"):
                p = bdir / f"output/raw/{kid}.{tag}.out"
                if not p.is_file():
                    sys.exit(f"ABORT missing raw {p}")
                variants[tag] = parse_replay(p)
            if BATCHES[batch][2] == 4:
                for tag in ("p1", "p2"):
                    p = bdir / f"output/raw/{kid}.{tag}.takeover.out"
                    if not p.is_file():
                        sys.exit(f"ABORT missing takeover raw {p}")
                    variants[tag + ".takeover"] = parse_replay(p)
            ref = variants["p1"]
            fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
            for tag, r in variants.items():
                if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
                    sys.exit(f"ABORT {kid}: pass mismatch {tag} {r} vs p1 {ref}")
            if ref["budget"] != 15000000 or ref["stones"] != 5 or ref["is_or"] != 0:
                sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
            bk = by_id.get(kid)
            if bk is None:
                sys.exit(f"ABORT batch-keys.json missing {kid}")
            if ref["legal"] != int(bk["legal"]):
                sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
            if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
                sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
            if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
                sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs {(ref['budget'], ref['result'], ref['nodes'])}")
            if ref["result"] not in (1, 2):
                sys.exit(f"ABORT {kid}: non-resolved result {ref['result']} in resolved set")
            key = (ref["lo"], ref["hi"])
            if key in all_lohi:
                sys.exit(f"ABORT duplicate key across packet {key}: {all_lohi[key]} and {kid}")
            all_lohi[key] = f"b{batch}:{kid}"
            if key in base_keys:
                bv, bn = base_keys[key]
                if ref["result"] != bv:
                    sys.exit(f"ABORT {kid}: BASE verdict conflict raw={ref['result']} base={bv} {key}")
                if ref["nodes"] != bn:
                    sys.exit(f"ABORT {kid}: BASE nodes mismatch raw={ref['nodes']} base={bn} {key}")
                consumed.append((batch, kid, key))
                continue  # pre-consumed duplicate: excluded from increments
            if key in quarantined:
                sys.exit(f"ABORT {kid}: quarantined key {key}")
            rows.append((batch, klass, kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    # exhaustion gate: h002 must be present in raws with result 0 and excluded
    hb = ROOT / "research/experiments/n11-centralreply-closure-class2634-batch8-20261122"
    ex_rows = []
    for tag in ("p1", "p2"):
        p = hb / f"output/raw/h002.{tag}.out"
        ex_rows.append(parse_replay(p))
    if any(r["result"] != 0 or r["nodes"] != 15000000 or r["budget"] != 15000000 for r in ex_rows):
        sys.exit(f"ABORT h002 exhaustion shape changed: {ex_rows}")
    if ex_rows[0]["result"] != ex_rows[1]["result"] or ex_rows[0]["nodes"] != ex_rows[1]["nodes"]:
        sys.exit("ABORT h002 pass mismatch")
    for (b, kid) in EXHAUSTION:
        if any(r[2] == "h002" for r in rows):
            sys.exit("ABORT exhaustion row leaked into a resolved increment")

    wins = [r for r in rows if r[6] == 1]
    losses = [r for r in rows if r[6] == 2]
    expected_wins = sorted(f"b{b}:{k}" for b, ks in WIN_IDS.items() for k in ks)
    got_wins = sorted(f"b{r[0]}:{r[2]}" for r in wins)
    if got_wins != expected_wins:
        sys.exit(f"ABORT WIN set mismatch: {got_wins}")
    if len(rows) != 132 or len(wins) != 10 or len(losses) != 122:
        sys.exit(f"ABORT row counts {len(rows)}/{len(wins)}/{len(losses)} != 132/10/122")
    got_consumed = sorted(f"b{b}:{k}" for b, k, _ in consumed)
    if got_consumed != sorted(f"b{b}:{k}" for b, k in EXPECTED_CONSUMED):
        sys.exit(f"ABORT consumed set mismatch: {got_consumed}")
    if len(consumed) != 19:
        sys.exit(f"ABORT consumed count {len(consumed)} != 19")

    hdr = [
        "# n11 central-reply closure JOINT unconsumed-rows IF-ADOPTED increment (Part AJ, 2026-11-22)",
        "# batches 1,3,4,5,6,8,9,11,12 (classes 16757/20421/16371/12264/5473/2634/1518/8785/8106)",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-11 z-keys also match their published takeover-host passes (4-way).",
        "# h002 (batch 8) exhausted 15M with result 0 (honest UNKNOWN) and is EXCLUDED from all",
        "#   increments; its 15M re-search stays forbidden. batch 13/14 are NOT part of this packet",
        "#   (Part AI / Part AF own them). Read-only what-if analysis only; verdicts are NOT consumed.",
        "# Methodology per Part H / H-bis / J / R / V / AB / AH: WIN-only vs LOSS-only vs full packet.",
        f"# gates: {quorum(11)}-way (batch-11) / 3-way (others) node-exact, status.log agreement,",
        "# HONEST CORRECTION (Part AJ): first run ABORTed at b001 already-in-BASE; re-measurement",
        "#   showed 19 batch-1 LOSS rows (b001..b017,b019,b020) pre-consumed into canonical BASE",
        "#   with identical verdicts AND nodes; they are excluded here (151 probed -> 132 unique-new).",
        "#   batch-keys legal/(lo,hi) agreement, 132 distinct keys, 19 pre-consumed BASE duplicates",
        "#   (verdict+node identical, the ONLY permitted overlap) excluded, quarantine 0.",
    ]
    tags = {
        "win": "# 10 rows: the unconsumed closure WINs b018/d002/e002/f017/g018/j033/h045/z003/n005/n006.",
        "loss": "# 122 rows: the probed exact-LOSS rows NOT already in BASE (19 pre-consumed excluded).",
        "all": "# 132 rows: all unique-new resolved probed rows (10 WIN + 122 LOSS), h002 excluded.",
    }
    names = {
        "win": "increment-joint-wins10-IFADOPTED-20261122.cache",
        "loss": "increment-joint-loss122-IFADOPTED-20261122.cache",
        "all": "increment-joint-all132-IFADOPTED-20261122.cache",
    }

    def write(tag, sel):
        lines = hdr + [tags[tag]]
        lines += [f"s5verdict,{r[4]},{r[5]},5,{r[6]},{r[7]}" for r in sorted(sel, key=lambda r: (r[4], r[5]))]
        p = OUT / names[tag]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{names[tag]}: {len(sel)} rows, sha256 {sha(p)}")

    write("win", wins)
    write("loss", losses)
    write("all", rows)

    manifest = {
        "schema": "joint10-unconsumed-increments-manifest-v1",
        "win_ids": {f"b{b}": ks for b, ks in WIN_IDS.items()},
        "row_counts": {"rows": len(rows), "wins": len(wins), "losses": len(losses)},
        "sha256": {tag: sha(OUT / names[tag]) for tag in names},
        "excluded_exhaustion": {"batch": 8, "kid": "h002", "result": 0, "budget": 15000000, "nodes": 15000000},
        "pre_consumed_base_duplicates": {
            "count": len(consumed),
            "ids": sorted(f"b{b}:{kid}" for b, kid, _k in consumed),
            "note": ("19 batch-1 LOSS rows already inside canonical BASE with "
                     "identical verdicts AND nodes (verdict+node-identity gate); "
                     "excluded from every increment; the first maker run ABORTed "
                     "fail-closed on this and the packet was corrected 151 -> 132 "),
        },
        "probed_total": 151,
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "interpretation_guard": "read-only what-if IF-ADOPTED analysis inputs; verdicts NOT consumed; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 151 probed rows -> 132 unique-new (122 LOSS + 10 WIN), 19 pre-consumed BASE duplicates excluded, "
          "h002 exhaustion excluded, all gates PASS")


if __name__ == "__main__":
    main()
