#!/usr/bin/env python3
"""Build the batch-18 dual-WIN (v001/v002) if-adopted increment (Part BA, 2026-11-22), fail-closed.

Executes the published single-owner Part BA declaration (note amendment,
pushed 2026-11-22 as commit 607c876a, observed HEAD-before-push f8cc6c9d
recorded in the declaration commit message).  All inputs are published main
bytes, re-verified on this host before use: the batch-18 published raws at
publication commit 938e34f2 (v001.p1/p2, v002.p1/p2, status.log, batch-keys.json
sha256 1bb3ed41...) and the current canonical exact-S5 verdict cache
6,120 rows sha256 be9cb24e... (the Part AS adoption output, published at
commit 8c42e44c).

This is an IF-ADOPTED increment for the scrutiny owner's adoption-decision
precomputation (Part V/R/AB/AH/AI/AN/AO/AT line; q042 / b018 / d002 / e002 /
p002p003 / r001r002 precedent).  The WIN rows v001 (s5_index 153671, key
[1154610354467115008, 64], result 1, 5,656,151 nodes) and v002 (s5_index
207534, key [3459890413727387648, 64], result 1, 7,898,204 nodes) are NOT
consumed anywhere by this Part: the canonical cache stays byte-identical, and
the merged if-adopted cache produced downstream is a PROJECTION, not the repo
canonical chain.  Adoption (and its C++ second-implementation gate 9193f5b6...)
stays the scrutiny owner's sole call; this Part neither recommends nor
rejects adoption.

Fail-closed gates: each WIN verdict is byte-taken from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes, lo, hi);
result must be 1 (WIN) and budget 15,000,000 and stones 5; legal and (lo,hi)
must match the published batch-keys.json rows for v001/v002 (key_id,
s5_index 153671/207534, legal 83/84); the status.log must carry the matching
`v001 PASS 15000000,1,5656151` / `v002 PASS 15000000,1,7898204` rows plus the
`v001 WIN-HALT` / `v002 WIN-HALT` rows, the WIN-ROW-DETAIL 2-pass lines for
both keys and the EXECUTION-HALTED stop line mentioning both keys with the
2/53 probed / 17 unconsumed-candidates bookkeeping (batch-18 status format;
the batch-14 WAVE-END row of the Part AT maker does not exist here, so the
WIN-ROW-DETAIL + EXECUTION-HALTED stop rows are gated instead); both keys must
be ABSENT from the canonical BASE cache (6,120 rows, sha256 be9cb24e...) and
absent from the quarantine registry; and both keys must be canonical-safe per
the published evidence policy.  Emission: 2-row increment cache + a manifest
JSON recording the BASE pins and the win-scenario bookkeeping.  11x11 stays
UNKNOWN; nodes are bookkeeping, never verdicts.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16131-batch18-20261122"
BATCH_KEYS_SHA_EXPECTED = "1bb3ed41b26af92491ed579a7c05471f271ed1394d8b5f817b5110794d926667"
STATUS_SHA_EXPECTED = "4b785add0f3e7dba7f689ec860458d0ead72e2cc77ef5f8b28026de36ef0bd21"
BASE_CACHE_SHA_EXPECTED = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
RAW_SHA_EXPECTED = {
    "v001.p1.out": "24b45c8a353a312cb0c6409592873b750e1ab8767257a9aca8c65a3894be3e25",
    "v001.p2.out": "1fc367bd99606a064557bbb6bc3f8246a2239bc34bb510ee92c213af4f65bd34",
    "v002.p1.out": "41c10ec220bc25abb7f9713e651229071096765b2a73f99951256d5710086a2e",
    "v002.p2.out": "e9f578fcbfa0a59a6f5746bbbb94ea5711eae5f7da57fd9af530ec0414da45de",
}
BUDGET = 15000000

WINS = [
    {"id": "v001", "s5_index": 153671, "lo": 1154610354467115008, "hi": 64,
     "nodes": 5656151, "legal": 83},
    {"id": "v002", "s5_index": 207534, "lo": 3459890413727387648, "hi": 64,
     "nodes": 7898204, "legal": 84},
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


def verify_one_win(w, status_lines):
    wid = w["id"]
    # --- two-pass WIN verification from the published raws -------------------
    variants = {}
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{wid}.{tag}.out"
        if not p.is_file():
            sys.exit(f"ABORT missing raw {p}")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys.exit(f"ABORT {wid}: pass mismatch {tag} {r} vs p1 {ref}")
    if (ref["result"] != 1 or ref["stones"] != 5 or ref["budget"] != BUDGET
            or ref["nodes"] != w["nodes"] or ref["lo"] != w["lo"]
            or ref["hi"] != w["hi"] or ref["legal"] != w["legal"]):
        sys.exit(f"ABORT {wid} raw is not the published WIN row: {ref}")

    # --- batch-keys agreement -------------------------------------------------
    bk_rows = bk[wid]
    if len(bk_rows) != 1:
        sys.exit(f"ABORT {wid} not unique in batch-keys")
    k = bk_rows[0]
    if (int(k["s5_index"]) != w["s5_index"] or int(k["lo"]) != w["lo"]
            or int(k["hi"]) != w["hi"] or int(k["legal"]) != ref["legal"]):
        sys.exit(f"ABORT {wid} batch-keys disagreement: {k} vs raw {ref}")

    # --- status.log agreement incl. the published WIN-HALT stop rows ----------
    pass_re = re.compile(rf"^\S+ {wid} PASS (\d+),(\d+),(\d+)$")
    hw_re = re.compile(rf"^\S+ {wid} WIN-HALT$")
    wrd_re = re.compile(
        rf"^\S+ WIN-ROW-DETAIL {wid} p1 nodes (\d+) == p2 nodes (\d+) "
        r"\(2-pass node-exact, compared fields identical, wall_s differs only\), "
        r"legal (\d+), budget (\d+), result (\d+), keys (\d+)/(\d+), # replay_done x2$")
    matched_pass = matched_halt = matched_detail = None
    for line in status_lines:
        m = pass_re.match(line)
        if m:
            mrow = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if matched_pass is not None and matched_pass != mrow:
                sys.exit(f"ABORT status PASS disagreement for {wid}")
            matched_pass = mrow
        if hw_re.match(line):
            matched_halt = True
        m = wrd_re.match(line)
        if m:
            drow = (int(m.group(1)), int(m.group(2)), int(m.group(3)),
                    int(m.group(4)), int(m.group(5)), int(m.group(6)), int(m.group(7)))
            if matched_detail is not None and matched_detail != drow:
                sys.exit(f"ABORT WIN-ROW-DETAIL disagreement for {wid}")
            matched_detail = drow
    if matched_pass != (BUDGET, 1, w["nodes"]):
        sys.exit(f"ABORT status PASS row for {wid} is {matched_pass}")
    if not matched_halt:
        sys.exit(f"ABORT WIN-HALT row missing for {wid}")
    if matched_detail != (w["nodes"], w["nodes"], w["legal"], BUDGET, 1,
                          w["lo"], w["hi"]):
        sys.exit(f"ABORT WIN-ROW-DETAIL row for {wid} is {matched_detail}")

    # --- BASE cache + quarantine absence --------------------------------------
    if (w["lo"], w["hi"]) in quarantined:
        sys.exit(f"ABORT {wid} key quarantined")
    if not is_canonical_safe_s5_key((w["lo"], w["hi"])):
        sys.exit(f"ABORT {wid} key noncanonical")
    if (w["lo"], w["hi"]) in base_index:
        sys.exit(f"ABORT {wid} key already present in the canonical BASE cache")
    return True


if __name__ == "__main__":
    for name, p, want in (("base cache", BASE_CACHE, BASE_CACHE_SHA_EXPECTED),
                          ("batch-keys", BATCH_DIR / "input/batch-keys.json", BATCH_KEYS_SHA_EXPECTED),
                          ("status.log", BATCH_DIR / "output/status.log", STATUS_SHA_EXPECTED)):
        got = sha(p)
        if got != want:
            sys.exit(f"ABORT {name} sha256 drift: {got} != {want}")
    for fname, want in RAW_SHA_EXPECTED.items():
        got = sha(BATCH_DIR / f"output/raw/{fname}")
        if got != want:
            sys.exit(f"ABORT raw {fname} sha256 drift: {got} != {want}")

    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key  # noqa: E402

    quarantined = quarantined_cache_keys()

    bk_json = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())
    if bk_json["class_index"] != 16131:
        sys.exit(f"ABORT batch-keys class_index {bk_json['class_index']} != 16131")
    if len(bk_json["keys"]) != 53:
        sys.exit(f"ABORT batch-keys {len(bk_json['keys'])} rows != 53")
    bk = {}
    for k in bk_json["keys"]:
        bk.setdefault(k["key_id"], []).append(k)

    base_rows = 0
    base_index = set()
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for line in stream:
            if not line.startswith("s5verdict,"):
                continue
            base_rows += 1
            parts = line.rstrip("\n").split(",")
            base_index.add((int(parts[1]), int(parts[2])))
    if base_rows != 6120:
        sys.exit(f"ABORT BASE cache rows {base_rows} != 6120")

    status_lines = (BATCH_DIR / "output/status.log").read_text().splitlines()
    for w in WINS:
        verify_one_win(w, status_lines)

    halt_re = re.compile(r"^\S+ EXECUTION-HALTED batch-18 stopped at first wave per "
                        r"pre-registered WIN-HALT rule \(rc=45 both workers\): v001 WIN and v002 WIN\.")
    if not any(halt_re.match(line) for line in status_lines):
        sys.exit("ABORT EXECUTION-HALTED stop row missing/not matching")
    if not any("Unconsumed closure WIN candidates now 17" in line for line in status_lines):
        sys.exit("ABORT 17-unconsumed-candidates bookkeeping row missing")

    # --- emission --------------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    incr_path = OUT / "increment-b18win-v001v002-ifadopted-20261122.cache"
    header = [
        "# n11 central-reply batch-18 dual-WIN (v001/v002) if-adopted increment (Part BA, 2026-11-22)",
        "# published Part BA declaration (note amendment 2026-11-22, commit 607c876a;",
        "#   observed HEAD-before-push f8cc6c9d recorded in the declaration commit message).",
        "# IF-ADOPTED PROJECTION ONLY - the WIN rows are NOT consumed by this Part; the",
        "#   canonical cache (be9cb24e..., 6,120 rows) is untouched; adoption of v001/v002",
        "#   stays the scrutiny owner's call (C++ second-implementation gate 9193f5b6...).",
        "# gates: per-key 2-pass (p1/p2) node-exact, status.log WIN-HALT / WIN-ROW-DETAIL /",
        "#   EXECUTION-HALTED stop-row agreement, batch-keys (sha256 1bb3ed41) legal/(lo,hi)/",
        "#   s5_index agreement, ZERO BASE-cache overlap, quarantine 0, canonical-safe keys.",
    ]
    lines = header + [f"s5verdict,{w['lo']},{w['hi']},5,1,{w['nodes']}" for w in WINS] + [""]
    incr_path.write_text("\n".join(lines), encoding="utf-8")
    incr_sha = sha(incr_path)

    manifest = {
        "schema": "batch18-win-v001v002-ifadopted-increment-manifest-v1",
        "part": "BA",
        "class_index": 16131,
        "win_ids": [w["id"] for w in WINS],
        "win_s5_index": [w["s5_index"] for w in WINS],
        "win_keys": [[w["lo"], w["hi"]] for w in WINS],
        "win_nodes": [w["nodes"] for w in WINS],
        "raw_publication_commit": "938e34f2",
        "row_counts": {"rows": 2, "wins": 2, "losses": 0},
        "ifadopted_only": True,
        "canonical_cache_untouched": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": base_rows,
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "sha256": {"win": incr_sha},
        "interpretation_guard": (
            "if-adopted projection increment for the scrutiny owner's adoption "
            "precomputation: the v001/v002 WIN verdicts are NOT consumed, the "
            "canonical cache stays byte-identical, this Part neither recommends "
            "nor rejects adoption; 11x11 stays UNKNOWN; nodes are bookkeeping, "
            "never verdicts"),
    }
    mpath = OUT / "increment-manifest.json"
    mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"OK 2 WIN rows -> increment sha256 {incr_sha}")
    print(f"manifest sha256 {sha(mpath)}")
