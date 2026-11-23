#!/usr/bin/env python3
"""Build the batch-26 (class 1849) 52-LOSS canonical-adoption increment, fail-closed.

Prepared (read-only dry-run, BEFORE the Part BU declaration push) for the
Part BU adoption: the published batch-26 packet (Part BQ drive-1 commits
... + Part BT continuation a79c2a6f/d69c3a38; kit MANIFEST af6da4ce 204
files all sha256-verified here; raws 123 = 106 complete (l001-l053 p1/p2)
+ 17 host-event truncated fragments that never produced a verdict row;
status.log afc92e03; row-audit.json (full-row schema v2) cb4158d9;
batch-keys.json f1ea43ae) is a COMPLETE enumeration book of the 53 unknown
cost children of class 1849: 52 LOSS rows (l001..l053 minus l028) plus ONE
WIN row (l028, honest label, 4系統 cross-verified in Part BS), 0
exhaustion, 0 mismatch, 2-pass fresh-cold node-exact at budget 15M.

The adoption base is the canonical exact-S5 verdict cache BASE = 6,235 rows
sha256 f6649fe3... (Part BI adoption output), byte-pinned here; this maker
ABORTS against anything else.

Emits the CANONICAL-ADOPTION increment cache over the published batch-26 raw
replay rows:

  * the 52 resolved LOSS rows {l001..l053} \\ {l028}

batch-26 resolved all 53 probed keys (52 LOSS + 1 WIN).  The WIN row l028
(key (1153485622925590528,0), s5 81011) is an HONEST LABEL ONLY and is NOT
adopted: it stays unconsumed (scrutiny owner C++ second-implementation gate
pin 9193f5b6...), like the batch-14residual q042 precedent (loss-only
adoption with an in-class WIN left unconsumed).  full != loss here
(machine-stated): the adopted packet is the 52-LOSS packet.

Fail-closed gates: every adopted increment row must come from BOTH published
raw passes with identical (stones, legal, is_or, budget, result, nodes) and
a completed "# replay_done" line; legal and (lo,hi) must match the
published batch-keys.json (sha256 f1ea43ae...) for every key; the
unadopted WIN row l028 is likewise two-pass re-verified (result 1) and its
key is asserted ABSENT from the BASE cache and the quarantine registry and
NOT emitted into the increment; every status.log PASS row must agree with
the raws on (budget, result, nodes); the status.log probed set must be
exactly {l001..l053} each-once (53 dated PASS rows), the WIN set must be
exactly {l028} (equals UNADOPTED_WIN_IDS), the exhaustion set EMPTY
(absence gate), the published WIN-HALT row of the Part BQ drive-1 stop must
be exactly the recorded l028 2-line pair (PASS row directly followed by
the dated WIN-HALT row) and no other stop row may exist (the Part BT
continuation after WIN-HALT is the published honest 29-row suffix); the
published final row 'l053 PASS 15000000,2,5352593' must be the last line
(the enumeration completed fresh, no EXHAUSTED/'EXECUTION-COMPLETE' rows
anywhere); the published row-audit summary (schema
n11-centralreply-closure-class1849-batch26-rowaudit-full-v2) must agree
(class 1849, batch 26, keys_total/probed 53, pass_rows 52, win_rows
['l028'], exhausted_rows [], mismatches 0, input_sha256 f1ea43ae); all 204
kit files must verify against the published MANIFEST af6da4ce (kit
integrity gate); the 17 truncated fragments must exist and carry NO verdict
row nor completion guard, and every one of their base keys must have a
later dated PASS row (host-event retries, fresh-cold re-run); adopted-row
pass node totals must agree on both passes (208,202,177); all adopted keys
distinct, ABSENT from the canonical BASE cache (6,235 rows; ANY overlap
ABORTs - batch-26 post-dates the Part BI merge), and absent from the
quarantine registry.  Verdicts are byte-taken from the raws.  The 52 LOSS
rows ARE consumed into the canonical cache by the Part BU fail-closed
merger; no WIN verdict is consumed anywhere.  11x11 stays UNKNOWN; nodes
are bookkeeping, never verdicts.
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-20261123.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class1849-batch26-20261123"
BATCH_KEYS_SHA_EXPECTED = "f1ea43aef6ee06c918885a9007ad3f347d96aa198180e87bf3eb14d783304cdd"
ROW_AUDIT_SHA_EXPECTED = "cb4158d9ecfa6143c20a8fddb59f03815e385cf90f6389cf032aa7e15779edb7"
STATUS_LOG_SHA_EXPECTED = "afc92e03dc4009854e698aa794ae4eae33f635c09986bd74287f5f07981eda05"
KIT_MANIFEST_SHA_EXPECTED = "af6da4ce6e5dabd7a6e32fe3c565db3f75a848134537c29f68821eed0394d760"
KIT_FILES_EXPECTED = 204
BASE_CACHE_SHA_EXPECTED = "f6649fe36425f9a4e959b058392746b73e655cda0fcfa223befafd8905d67d26"
BASE_CACHE_ROWS_EXPECTED = 6235

LOSS_IDS = [f"l{i:03d}" for i in range(1, 54) if i != 28]  # adopted LOSS rows (52)
UNADOPTED_WIN_IDS = ["l028"]                                # honest-label WIN, NOT adopted
PROBED = [f"l{i:03d}" for i in range(1, 54)]               # the published probed set (53)
EXHAUSTED_IDS: list = []                                    # batch-26 has zero exhaustion rows (asserted)
BUDGET = 15_000_000
TOTAL_NODES_PER_PASS_EXPECTED = 208_202_177                 # over the 52 adopted LOSS rows only
FINAL_ROW_EXPECTED = "2026-11-23T09:42:23Z l053 PASS 15000000,2,5352593"
WIN_HALT_ROW_EXPECTED = "2026-11-23T08:21:45Z l028 WIN-HALT"
WIN_PASS_ROW_EXPECTED = "2026-11-23T08:21:45Z l028 PASS 15000000,1,4893014"
TRUNCATED_FRAGMENTS_EXPECTED = [
    "l006.p2.truncated.080016.out", "l007.p1.truncated.080016.out",
    "l009.p1.truncated.080438.out", "l012.p1.truncated.080709.out",
    "l014.p1.truncated.080901.out", "l017.p1.truncated.081007.out",
    "l020.p1.truncated.081323.out", "l021.p2.truncated.081323.out",
    "l022.p2.truncated.081746.out", "l027.p2.truncated.081837.out",
    "l035.p1.truncated.092554.out", "l036.p2.truncated.092942.out",
    "l041.p1.truncated.093015.out", "l045.p1.truncated.093411.out",
    "l046.p2.truncated.093411.out", "l049.p1.truncated.093843.out",
    "l050.p1.truncated.093843.out",
]


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
        m = re.match(r"^(\S+) (\S+) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid, b, r, n = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
            if kid in got:
                sys.exit(f"ABORT status key {kid} appears more than once (each-once gate)")
            got[kid] = (b, r, n)
    return got


def two_pass(kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{kid}.{tag}.out"
        if not p.is_file():
            sys.exit(f"ABORT missing raw {p}")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys.exit(f"ABORT raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys.exit(f"ABORT {kid}: pass mismatch {tag} {r} vs p1 {ref}")
    return ref


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys.exit("ABORT base cache sha drift")
    if sha(BATCH_DIR / "input/batch-keys.json") != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT batch-26 batch-keys.json sha drift")
    if sha(BATCH_DIR / "output/row-audit.json") != ROW_AUDIT_SHA_EXPECTED:
        sys.exit("ABORT batch-26 row-audit.json sha drift")
    if sha(BATCH_DIR / "output/status.log") != STATUS_LOG_SHA_EXPECTED:
        sys.exit("ABORT batch-26 status.log sha drift")
    if sha(BATCH_DIR / "MANIFEST-sha256.txt") != KIT_MANIFEST_SHA_EXPECTED:
        sys.exit("ABORT batch-26 kit MANIFEST sha drift")
    OUT.mkdir(parents=True, exist_ok=True)

    # --- kit integrity gate: all 204 published files must verify ------------
    kit_verified = 0
    for line in (BATCH_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split(None, 1)
        p = BATCH_DIR / rel
        if not p.is_file():
            sys.exit(f"ABORT kit file missing: {rel}")
        if sha(p) != want:
            sys.exit(f"ABORT kit file sha drift: {rel}")
        kit_verified += 1
    if kit_verified != KIT_FILES_EXPECTED:
        sys.exit(f"ABORT kit files verified {kit_verified} != {KIT_FILES_EXPECTED}")

    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys.exit(f"ABORT base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    keys = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())["keys"]
    bk_all = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())
    if bk_all["class_index"] != 1849 or bk_all["budget"] != BUDGET:
        sys.exit("ABORT batch-keys class/budget drift")
    if bk_all["published_base_canonical_rows"] != BASE_CACHE_ROWS_EXPECTED:
        sys.exit("ABORT batch-keys published_base_canonical_rows drift")
    by_id = {k["key_id"]: k for k in keys}
    if len(by_id) != 53:
        sys.exit(f"ABORT batch-keys key count {len(by_id)} != 53")

    # --- status.log: whole picture -----------------------------------------
    status = parse_status(BATCH_DIR / "output/status.log")
    status_probed = {k for k in status if k in PROBED}
    if status_probed != set(PROBED):
        sys.exit(f"ABORT status probed set != {{l001..l053}}: {sorted(status_probed)}")
    extra_status = set(status) - set(PROBED)
    if extra_status:
        sys.exit(f"ABORT status.log PASS rows outside the probed set: {sorted(extra_status)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(PROBED):
        sys.exit(f"ABORT status resolved set != full probed set: {sorted(status_resolved)}")
    status_wins = {k for k, v in status.items() if k in PROBED and v[1] == 1}
    if status_wins != set(UNADOPTED_WIN_IDS):
        sys.exit(f"ABORT batch-26 WIN set {sorted(status_wins)} != {{'l028'}} (unadopted WIN gate)")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted != set(EXHAUSTED_IDS):
        sys.exit(f"ABORT batch-26 must have zero exhaustion rows: {sorted(status_exhausted)}")
    lines = (BATCH_DIR / "output/status.log").read_text().strip().splitlines()
    if lines[-1] != FINAL_ROW_EXPECTED:
        sys.exit(f"ABORT status.log final line is not the published l053 PASS row: {lines[-1]}")
    if WIN_PASS_ROW_EXPECTED not in lines:
        sys.exit("ABORT status.log lacks the published l028 WIN PASS row pair head")
    if lines.count(WIN_PASS_ROW_EXPECTED) != 1:
        sys.exit("ABORT status.log l028 PASS row not exactly once")
    idx = lines.index(WIN_PASS_ROW_EXPECTED)
    if idx + 1 >= len(lines) or lines[idx + 1] != WIN_HALT_ROW_EXPECTED:
        sys.exit("ABORT status.log l028 PASS row not directly followed by its dated WIN-HALT row "
                 "(the published Part BQ drive-1 stop is the recorded 2-line pair)")
    halt_rows = [ln for ln in lines if re.match(r"^\S+ \S+ (WIN-HALT|HARD-STOP)( |$)", ln)]
    if halt_rows != [WIN_HALT_ROW_EXPECTED]:
        sys.exit(f"ABORT stop rows must be exactly the recorded l028 WIN-HALT row: {halt_rows}")
    if "EXECUTION-COMPLETE" in "\n".join(lines):
        sys.exit("ABORT unexpected EXECUTION-COMPLETE stop record in batch-26 status.log")
    if status.get("l028") != (15_000_000, 1, 4_893_014):
        sys.exit(f"ABORT status.log l028 disagreement: {status.get('l028')}")

    # --- row-audit.json: summary agreement -----------------------------------
    ra = json.loads((BATCH_DIR / "output/row-audit.json").read_text())
    if ra["schema"] != "n11-centralreply-closure-class1849-batch26-rowaudit-full-v2":
        sys.exit(f"ABORT row-audit schema drift: {ra['schema']}")
    if ra["class_index"] != 1849 or ra["batch"] != 26:
        sys.exit("ABORT row-audit whole-picture header drift")
    if ra["keys_total"] != 53 or ra["probed"] != 53 or ra["pass_rows"] != 52:
        sys.exit("ABORT row-audit keys_total/probed/pass_rows drift")
    if ra["win_rows"] != ["l028"] or ra["exhausted_rows"] != [] or ra["mismatches"] != 0:
        sys.exit(f"ABORT row-audit results not the published 52-LOSS + l028-WIN picture: "
                 f"{ra['win_rows']}/{ra['exhausted_rows']}/{ra['mismatches']}")
    if ra["input_sha256"] != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT row-audit input_sha256 drift")

    # --- host-event truncated fragments -------------------------------------
    present_frags = sorted(p.name for p in (BATCH_DIR / "output/raw").glob("*.truncated.*.out"))
    if present_frags != sorted(TRUNCATED_FRAGMENTS_EXPECTED):
        sys.exit(f"ABORT truncated fragment set drift: {present_frags}")
    for name in present_frags:
        p = BATCH_DIR / "output/raw" / name
        txt = p.read_text()
        if re.search(r"^replay,", txt, re.M):
            sys.exit(f"ABORT hostevent fragment carries a verdict row: {p}")
        if "# replay_done" in txt:
            sys.exit(f"ABORT hostevent fragment carries a completion guard: {p}")
        base_kid = name.split(".")[0]
        if base_kid not in status:
            sys.exit(f"ABORT truncated fragment {name} base key {base_kid} has no dated PASS row")

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - adopted LOSS rows
    total_nodes = {"p1": 0, "p2": 0}
    for kid in LOSS_IDS:
        ref = two_pass(kid)
        if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["result"] != 2:
            sys.exit(f"ABORT {kid}: adopted rows must be result 2, got {ref['result']}")
        total_nodes["p1"] += ref["nodes"]
        bk = by_id.get(kid)
        if bk is None:
            sys.exit(f"ABORT batch-keys.json missing {kid}")
        if ref["legal"] != int(bk["legal"]):
            sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
        if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs {(ref['budget'], ref['result'], ref['nodes'])}")
        key = (ref["lo"], ref["hi"])
        if key in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {key}")
        if key in base_keys:
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        if any(r[3] == key[0] and r[4] == key[1] for r in rows):
            sys.exit(f"ABORT duplicate key within batch {key}")
        rows.append((kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    # --- the unadopted WIN row l028: two-pass re-verification, NOT adopted ---
    winref = two_pass("l028")
    winbk = by_id["l028"]
    if winref["result"] != 1 or winref["budget"] != BUDGET or winref["stones"] != 5 or winref["is_or"] != 0:
        sys.exit(f"ABORT l028: WIN row not the published honest label: {winref}")
    if (winref["lo"], winref["hi"]) != (int(winbk["lo"]), int(winbk["hi"])):
        sys.exit("ABORT l028: key mismatch raw vs batch-keys")
    if winref["legal"] != int(winbk["legal"]):
        sys.exit(f"ABORT l028: legal mismatch raw={winref['legal']} keys={winbk['legal']}")
    if status.get("l028") != (winref["budget"], winref["result"], winref["nodes"]):
        sys.exit("ABORT l028: status.log disagreement")
    winkey = (winref["lo"], winref["hi"])
    if winkey in base_keys:
        sys.exit(f"ABORT l028: unadopted WIN key already in BASE cache {winkey}")
    if winkey in quarantined:
        sys.exit(f"ABORT l028: quarantined key {winkey}")
    if any(r[3] == winkey[0] and r[4] == winkey[1] for r in rows):
        sys.exit("ABORT l028 WIN key leaked into the adopted rows")

    # second-pass node totals cross-check (independent of parse)
    for tag in ("p1", "p2"):
        s = 0
        for kid in LOSS_IDS:
            for line in (BATCH_DIR / f"output/raw/{kid}.{tag}.out").read_text().splitlines():
                if line.startswith("replay,"):
                    s += int(line.split(",")[7])
        total_nodes[tag] = s
    if total_nodes["p1"] != total_nodes["p2"] or total_nodes["p1"] != TOTAL_NODES_PER_PASS_EXPECTED:
        sys.exit(f"ABORT adopted-row pass node totals drift: {total_nodes} != {TOTAL_NODES_PER_PASS_EXPECTED}")

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_losses = sorted(r[0] for r in losses)
    if got_losses != sorted(LOSS_IDS):
        sys.exit(f"ABORT LOSS set mismatch: {got_losses}")
    if len(rows) != 52 or wins or len(losses) != 52:
        sys.exit(f"ABORT adopted row counts {len(rows)}/{len(wins)}/{len(losses)} != 52/0/52")

    hdr = [
        "# n11 central-reply closure batch-26 (class 1849) 52-LOSS canonical-adoption increment (Part BU, 2026-11-23)",
        "# published Part BU declaration (note amendment 2026-11-23; single-owner: batch-26 52-LOSS",
        "#   adoption; the in-batch WIN row l028 is an honest label only and is NOT adopted).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-26 was executed by the Part BQ drive-1 host (WIN-HALT at l028, pre-registered)",
        "#   and completed by the Part BT continuation host (WIN-CONTINUE pre-registration; the",
        "#   29-row status.log suffix is the honest continuation record); class 1849's 53 unknown",
        "#   cost children are fully enumerated: 52 LOSS + 1 WIN (l028, 4-systems cross-verified",
        "#   in Part BS), 0 exhaustion, 0 mismatch; row-audit cb4158d9 (full-row schema v2)",
        "#   agrees; status.log afc92e03: 53 dated each-once PASS rows, exactly one stop row",
        "#   (the l028 WIN-HALT 2-line pair of Part BQ drive-1), final row 'l053 PASS",
        "#   15000000,2,5352593'.",
        "# gates: kit MANIFEST af6da4ce 204/204 file sha verification, 2-way (p1/p2) node-exact",
        "#   + '# replay_done' completeness, status.log each-once agreement (b,r,n) per key,",
        "#   WIN set == {l028} == unadopted, exhaustion absence gate, WIN-HALT 2-line pair pin,",
        "#   row-audit.json full-v2 summary agreement, batch-keys f1ea43ae legal/(lo,hi)",
        "#   agreement, adopted-row pass node totals 208,202,177 x2, adopted keys distinct,",
        "#   ZERO BASE-cache overlap (structural gate: batch-26 post-dates the Part BI merge;)",
        "#   any overlap ABORTs), quarantine 0, l028 two-pass WIN re-verification + presence",
        "#   bookkeeping (asserted NOT adopted).",
        "# ADOPTED set = {l001..l053}\\{l028} = exactly the 52 LOSS rows.  full != loss here",
        "#   (machine-stated): the resolved packet additionally holds the l028 WIN row, which",
        "#   stays UNCONSUMED (scrutiny owner C++ second-implementation gate pin 9193f5b6...;",
        "#   batch-14residual q042 precedent); no WIN verdict is consumed anywhere by this",
        "#   Part; the 28 unconsumed closure WIN candidates (l028 included) are untouched.",
        "# The 52 LOSS rows ARE consumed into the canonical cache by the Part BU merger;",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 52 rows: the adopted LOSS verdicts of class 1849's unknown S5 children (26th batch).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch26-loss52-20261123.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch26-loss52-increments-manifest-v1",
        "batch": 26,
        "class_index": 1849,
        "loss_ids": LOSS_IDS,
        "resolved_ids": PROBED,
        "win_ids": UNADOPTED_WIN_IDS,
        "unadopted_win_ids": UNADOPTED_WIN_IDS,
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "row_counts": {"resolved_rows": len(rows) + 1, "wins": len(UNADOPTED_WIN_IDS),
                       "losses": len(losses),
                       "exhausted_excluded": 0, "probed_total": 53, "probed_resolved": 53},
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale": ("batch-26 resolved all 53 probed keys as 52 LOSS + "
                                               "1 WIN (l028); the WIN row is an honest label only, "
                                               "NOT adopted (unconsumed), so the adopted packet "
                                               "(the 52 LOSS rows) != the full resolved packet"),
        "win_scenario_exists": True,
        "win_scenario_note": ("batch-26 contains exactly one WIN row (l028, key "
                              "(1153485622925590528,0), s5 81011, nodes 4893014 x2, "
                              "two-pass node-exact, 4-systems cross-verified in Part BS); "
                              "it is NOT adopted by this Part and stays unconsumed "
                              "(scrutiny owner C++ second-implementation gate pin "
                              "9193f5b6...; batch-14residual q042 precedent); loss-only "
                              "adoption can NEVER free class 1849 while l028 stays "
                              "unconsumed (its WIN child remains unknown in canonical)"),
        "unadopted_win_rows": [{"key_id": "l028", "s5_index": int(winbk["s5_index"]),
                                "lo": winref["lo"], "hi": winref["hi"],
                                "legal": winref["legal"], "result": winref["result"],
                                "nodes": winref["nodes"],
                                "two_pass_node_exact": True,
                                "systems_backing": 4,
                                "note": "Part BQ drive-1 + Part BS pinned-replica + third "
                                        "implementation a/b (k02a/l1a anchors) - honest "
                                        "label only, never adopted in this Part"}],
        "row_audit_agreement_rows": 53,
        "row_audit_sha256": ROW_AUDIT_SHA_EXPECTED,
        "status_log_stop_record": {"key_id": "l028", "row": WIN_HALT_ROW_EXPECTED},
        "status_log_stop_record_note": ("the single stop row is the Part BQ drive-1 l028 "
                                        "WIN-HALT (rc=45, pre-registered); the published "
                                        "Part BT continuation (WIN-CONTINUE pre-registration) "
                                        "restarted the drive and completed the enumeration "
                                        "(status.log 29-row suffix, final row the l053 PASS row)"),
        "status_log_final_row": FINAL_ROW_EXPECTED,
        "status_log_sha256": STATUS_LOG_SHA_EXPECTED,
        "total_nodes_pass_one": total_nodes["p1"],
        "total_nodes_pass_two": total_nodes["p2"],
        "truncated_fragments": TRUNCATED_FRAGMENTS_EXPECTED,
        "truncated_fragments_carries_verdict": False,
        "kit_integrity": {"manifest_sha256": KIT_MANIFEST_SHA_EXPECTED,
                          "files_verified": kit_verified},
        "base_cache_absent_hits": 0,
        "base_cache_rows": len(base_keys),
        "quarantine_hits": 0,
        "interpretation_guard": ("canonical adoption increment: only the 52 LOSS rows are "
                                 "consumed into the canonical cache via the fail-closed "
                                 "union merger; the l028 WIN verdict is NOT consumed "
                                 "(unconsumed closure WIN candidate); 11x11 stays UNKNOWN; "
                                 "nodes are bookkeeping, never verdicts"),
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 53 probed rows -> 52 adopted LOSS ({l001..l053}\\l028), 1 unadopted WIN (l028, "
          "honest label, stays unconsumed), zero exhaustion, zero BASE overlap, quarantine 0, "
          "kit 204/204 verified, full != loss packet, row-audit full-v2 summary agreement, "
          "all gates PASS")


if __name__ == "__main__":
    main()
