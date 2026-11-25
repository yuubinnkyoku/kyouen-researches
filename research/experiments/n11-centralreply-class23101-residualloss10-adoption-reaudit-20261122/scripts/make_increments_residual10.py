#!/usr/bin/env python3
"""Build the batch-14 residual (class 23101) 10-LOSS canonical-adoption increment, fail-closed.

Prepared (read-only dry-run, BEFORE any declaration) for the Part BC
adoption: the residual packet published by Part AW
(n11-centralreply-closure-class23101-batch14-residual-20261122,
publication commit cb94f808) is a CLEAN all-LOSS batch: q043..q052, all
10 rows 2-pass fresh-cold node-exact result 2 at budget 15M, WIN 0,
exhaustion 0, mismatch 0 (published row-audit.json sha256 6b40b131...,
total 23,252,550 nodes/pass).  The adoption base is the canonical
6,172-row post-AV cache (sha256 a5540811...) once Part AV publishes it;
this maker pins that base by sha, so it ABORTS against anything else.

Emits the CANONICAL-ADOPTION increment cache over the published residual
raw replay rows:

  * all 10 resolved LOSS rows {q043..q052}

The residual packet is full == loss for the residual batch (zero WIN,
zero exhaustion).  NOTE (route context, never a verdict interpretation):
class 23101 also holds the unconsumed q042 WIN (s5 745184, Part AQ
WIN-HALT row, third-implementation cross-verified in Part AR); q042 is
NOT part of any adoption packet and stays unconsumed (scrutiny owner
C++ second-implementation gate pin 9193f5b6...).  A 10-LOSS adoption
can therefore NEVER free class 23101 (its WIN child remains): the class
keeps exactly one unknown child (745184) and this increment's scheduling
value is boundary 11 -> 1 plus any cross-class cost memberships.

Fail-closed gates: every increment row must come from BOTH published
raw passes with identical (stones, legal, is_or, budget, result, nodes);
legal and (lo,hi) must match the published batch-keys.json (sha256
d4fada68...) for every key; every status.log PASS row must agree with
the raws on (budget, result, nodes); the status.log PASS set must be
exactly {q043..q052} with zero result-1 and zero result-0 rows, the
VAL-GATE row and the WAVE-END all-10-done stop row present; the
published row-audit.json (schema ...batch14residual-rowaudit-v1, sha256
6b40b131...) must re-confirm all 10 rows 2-pass node-exact LOSS with
matching results/nodes for every key.  All keys distinct, ABSENT from
the canonical BASE cache (6,172 rows, sha256 a5540811...; ANY overlap
ABORTs), absent from the quarantine registry, s5-disjoint from the
batch-17 adopted pack (batch-17 batch-keys sha256 db762175... cross
gate) and from the unconsumed q042 WIN (s5 745184) explicit gate.
Verdicts are byte-taken from the raws.  The 10 LOSS rows ARE consumed
into the canonical cache by the Part BC fail-closed merger.  11x11
stays UNKNOWN; nodes are bookkeeping, never verdicts.
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class10661-loss52-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class23101-batch14-residual-20261122"
BATCH17_KEYS = ROOT / "research/experiments/n11-centralreply-closure-class10661-batch17-20261122/input/batch-keys.json"
BATCH_KEYS_SHA_EXPECTED = "d4fada6801173499750d1739bf7aee45cbd01eab316e11b210436f8bb1f94121"
BASE_CACHE_SHA_EXPECTED = "a554081156e2c2f940ecf2cc3c7af082dde6b760d6019e0a5113c4ddd5e12a3a"
ROW_AUDIT_SHA_EXPECTED = "6b40b131c54302b61ad9c767f948b7fc4e9c1f6a67e42915faca9d457f709003"
BATCH17_KEYS_SHA_EXPECTED = "db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2"
Q042_S5_EXPECTED = 745184

PROBED = [f"q{i:03d}" for i in range(43, 53)]  # the published residual probed set (10)
LOSS_IDS = list(PROBED)                        # residual batch: every probed row is LOSS
EXHAUSTED_IDS: list = []                       # residual batch has zero exhaustion rows (asserted)


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


def two_pass(kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{kid}.{tag}.out"
        if not p.is_file():
            sys.exit(f"ABORT missing raw {p}")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys.exit(f"ABORT {kid}: pass mismatch {tag} {r} vs p1 {ref}")
    if "# replay_done" not in (BATCH_DIR / f"output/raw/{kid}.p1.out").read_text():
        sys.exit(f"ABORT {kid}.p1 lacks '# replay_done'")
    if "# replay_done" not in (BATCH_DIR / f"output/raw/{kid}.p2.out").read_text():
        sys.exit(f"ABORT {kid}.p2 lacks '# replay_done'")
    return ref


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys.exit("ABORT base cache sha drift (expected the post-AV canonical 6,172 rows a5540811...)")
    if sha(BATCH_DIR / "input/batch-keys.json") != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT residual batch-keys.json sha drift")
    if sha(BATCH_DIR / "output/row-audit.json") != ROW_AUDIT_SHA_EXPECTED:
        sys.exit("ABORT residual row-audit.json sha drift")
    if sha(BATCH17_KEYS) != BATCH17_KEYS_SHA_EXPECTED:
        sys.exit("ABORT batch-17 batch-keys.json sha drift (s5-disjoint cross gate input)")
    OUT.mkdir(parents=True, exist_ok=True)
    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    if len(base_keys) != 6172:
        sys.exit(f"ABORT base cache row count {len(base_keys)} != 6172 (post-AV canonical)")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    keys = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())["keys"]
    by_id = {k["key_id"]: k for k in keys}
    if len(by_id) != 10:
        sys.exit(f"ABORT batch-keys key count {len(by_id)} != 10")
    b17 = json.loads(BATCH17_KEYS.read_text())
    if b17["class_index"] != 10661 or len(b17["keys"]) != 52:
        sys.exit("ABORT batch-17 batch-keys header disagreement")
    b17_s5 = {int(k["s5_index"]) for k in b17["keys"]}

    status = parse_status(BATCH_DIR / "output/status.log")
    status_probed = {k for k in status if k in PROBED}
    if status_probed != set(PROBED):
        sys.exit(f"ABORT status probed set != {{q043..q052}}: {sorted(status_probed)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(PROBED):
        sys.exit(f"ABORT status resolved set != full residual probed set: {sorted(status_resolved)}")
    status_wins = {k for k, v in status.items() if k in PROBED and v[1] == 1}
    if status_wins:
        sys.exit(f"ABORT residual batch is clean: no WIN rows allowed, got {sorted(status_wins)}")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted:
        sys.exit(f"ABORT residual batch must have zero exhaustion rows: {sorted(status_exhausted)}")
    status_text = (BATCH_DIR / "output/status.log").read_text()
    if re.search(r"\b[a-z]\d{3}\s+WIN-HALT\b", status_text):
        sys.exit("ABORT clean residual status.log must not contain any WIN-HALT row")
    if re.search(r"WIN-CONTINUE\s+[a-z]\d{3}", status_text):
        sys.exit("ABORT residual status.log must not contain any WIN-CONTINUE row (batch had no WIN)")
    if "VAL-GATE 4/4 node-exact" not in status_text:
        sys.exit("ABORT status.log lacks the published VAL-GATE 4/4 node-exact record")
    if re.search(r"WAVE-END q052 stop=0 all-10-done", status_text) is None:
        sys.exit("ABORT status.log lacks the published WAVE-END all-10-done stop row")

    # --- published row-audit.json cross-verification ------------------------
    audit = json.loads((BATCH_DIR / "output/row-audit.json").read_text())
    if audit["schema"] != "n11-centralreply-closure-class23101-batch14residual-rowaudit-v1":
        sys.exit(f"ABORT row-audit schema {audit['schema']}")
    if audit["class_index"] != 23101 or audit["budget"] != 15000000:
        sys.exit("ABORT row-audit header class/budget disagreement")
    if audit["probed_rows"] != 10 or audit["probed_ids"] != PROBED:
        sys.exit(f"ABORT row-audit probed set {audit['probed_rows']} {audit['probed_ids']}")
    if audit["wins"] != [] or audit["win_continues"] != [] or audit["exhausted_result0"] != []:
        sys.exit(f"ABORT row-audit win/exhaustion lists not empty: {audit}")
    if audit["mismatch"] != 0:
        sys.exit("ABORT row-audit mismatch nonzero")
    if audit["replay_done_complete_all_passes"] is not True:
        sys.exit("ABORT row-audit replay_done flag lost")
    if audit["all_result2_2pass_node_exact"] is not True:
        sys.exit("ABORT row-audit all-result2-2pass flag lost")
    if audit["status_pass_rows_cross_checked"] is not True:
        sys.exit("ABORT row-audit status cross-check flag lost")
    if audit["verdict_consumption"] != 0:
        sys.exit("ABORT row-audit verdict consumption nonzero")
    audit_rows = {r["key_id"]: r for r in audit["rows"]}
    if set(audit_rows) != set(PROBED):
        sys.exit("ABORT row-audit rows != residual probed set")
    node_sum = sum(int(r["nodes"]) for r in audit["rows"])
    if node_sum != int(audit["total_nodes_per_pass"]):
        sys.exit(f"ABORT row-audit node sum {node_sum} != total_nodes_per_pass "
                 f"{audit['total_nodes_per_pass']}")
    lohi_seen = set()

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - adopted LOSS rows
    for kid in LOSS_IDS:
        ref = two_pass(kid)
        if ref["budget"] != 15000000 or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["result"] != 2:
            sys.exit(f"ABORT {kid}: residual adopted rows must be result 2, got {ref['result']}")
        bk = by_id.get(kid)
        if bk is None:
            sys.exit(f"ABORT batch-keys.json missing {kid}")
        if ref["legal"] != int(bk["legal"]):
            sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
        if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs {(ref['budget'], ref['result'], ref['nodes'])}")
        ar = audit_rows.get(kid)
        if ar is None or ar["result"] != 2:
            sys.exit(f"ABORT {kid}: row-audit disagreement {ar}")
        if ar["nodes"] != ref["nodes"] or int(ar["budget"]) != ref["budget"]:
            sys.exit(f"ABORT {kid}: row-audit nodes/budget disagreement {ar}")
        if ar["s5_index"] != int(bk["s5_index"]) or ar["legal"] != int(bk["legal"]):
            sys.exit(f"ABORT {kid}: row-audit index/legal disagreement")
        s5i = int(bk["s5_index"])
        if s5i == Q042_S5_EXPECTED:
            sys.exit(f"ABORT {kid}: s5 {s5i} is the unconsumed q042 WIN - never adoptable in a LOSS packet")
        if s5i in b17_s5:
            sys.exit(f"ABORT {kid}: s5 {s5i} intersects the batch-17 adopted pack (disjointness gate)")
        key = (ref["lo"], ref["hi"])
        if key in lohi_seen:
            sys.exit(f"ABORT duplicate key within batch {key}")
        lohi_seen.add(key)
        if key in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {key}")
        if key in base_keys:
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        rows.append((kid, s5i, ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_losses = sorted(r[0] for r in losses)
    if got_losses != sorted(LOSS_IDS):
        sys.exit(f"ABORT LOSS set mismatch: {got_losses}")
    if len(rows) != 10 or wins or len(losses) != 10:
        sys.exit(f"ABORT resolved row counts {len(rows)}/{len(wins)}/{len(losses)} != 10/0/10")
    if {r[1] for r in rows} & {Q042_S5_EXPECTED}:
        sys.exit("ABORT q042 s5 leaked into the adopted pack")

    hdr = [
        "# n11 central-reply closure batch-14 residual (class 23101) 10-LOSS canonical-adoption increment (Part BC prep, 2026-11-22)",
        "# residual packet published by Part AW (dataset n11-centralreply-",
        "#   closure-class23101-batch14-residual-20261122, publication commit cb94f808):",
        "#   q043..q052, all 10 rows 2-pass fresh-cold node-exact result 2 at budget",
        "#   15M, WIN 0, exhaustion 0, mismatch 0 (row-audit 6b40b131, 23,252,550",
        "#   nodes/pass). Batch-14 residual class 23101 continuation of batch-14",
        "#   (Part AQ/AS) probed set {q001..q042}.",
        "# BASE = the post-AV canonical exact-S5 verdict cache 6,172 rows",
        "#   (sha256 a5540811...): Part AS 6,120 + batch-17 52-LOSS (Part AV).",
        "# gates: 3-way (p1/p2/status) node-exact, row-audit.json 10-row",
        "#   cross-verification, batch-keys (sha256 d4fada68) legal/(lo,hi)",
        "#   agreement, resolved keys distinct, s5 set disjoint from the batch-17",
        "#   adopted pack AND from the unconsumed q042 WIN (s5 745184), ZERO",
        "#   BASE-cache overlap (any overlap ABORTs), quarantine 0,",
        "#   WIN-CONTINUE/exhaustion absence gates.",
        "# ADOPTED set = exactly the 10 LOSS rows {q043..q052} = the full residual",
        "#   packet (clean all-LOSS residual, so full == loss here).",
        "# 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 10 rows: the adopted LOSS verdicts of class 23101's residual unknown S5 children.",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch14residual-loss10-20261122.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch14residual-loss10-increments-manifest-v1",
        "batch": "14r",
        "class_index": 23101,
        "loss_ids": LOSS_IDS,
        "resolved_ids": LOSS_IDS,
        "win_ids": [],
        "unadopted_win_ids": [],
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "row_counts": {"resolved_rows": len(rows), "wins": len(wins), "losses": len(losses),
                       "exhausted_excluded": 0, "probed_total": 10, "probed_resolved": 10},
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": True,
        "full_packet_eq_loss_only_rationale": ("the residual batch resolved all 10 probed "
                                                "keys as LOSS; the packet contains zero WIN "
                                                "rows and zero exhaustion rows, so the adopted "
                                                "packet is identical to the full resolved "
                                                "residual packet"),
        "win_scenario_exists": False,
        "win_scenario_note": ("class 23101's unconsumed q042 WIN (s5 745184, Part AQ "
                              "WIN-HALT row, Part AR third-implementation cross-verified) "
                              "is OUTSIDE this packet and stays unconsumed; the scrutiny "
                              "owner C++ gate (pin 9193f5b6...) is unchanged - a 10-LOSS "
                              "adoption can never free class 23101 and this Part must not "
                              "claim any class closure or root coverage"),
        "base_cache_absent_hits": 0,
        "base_cache_rows": len(base_keys),
        "quarantine_hits": 0,
        "row_audit_sha256": ROW_AUDIT_SHA_EXPECTED,
        "batch17_s5_disjoint": True,
        "q042_s5_excluded": Q042_S5_EXPECTED,
        "interpretation_guard": ("canonical adoption increment prep: the 10 LOSS rows are "
                                 "consumed into the canonical cache via the fail-closed "
                                 "union merger once declared (execution-before-declaration "
                                 "discipline); 11x11 stays UNKNOWN; nodes are bookkeeping, "
                                 "never verdicts"),
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 10 probed residual rows -> 10 adopted LOSS (q043..q052), zero WIN, zero "
          "exhaustion, zero BASE overlap, quarantine 0, s5 disjoint from batch-17 and from "
          "the unconsumed q042, clean residual packet full==loss, row-audit "
          "cross-verified, all gates PASS")


if __name__ == "__main__":
    main()
