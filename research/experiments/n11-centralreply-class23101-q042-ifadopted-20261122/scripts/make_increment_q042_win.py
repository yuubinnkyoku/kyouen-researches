#!/usr/bin/env python3
"""Build the q042 single-WIN if-adopted increment (Part AT, 2026-11-22), fail-closed.

Executes the published single-owner Part AT declaration (note amendment,
pushed 2026-11-22 as commit 58938933).  All inputs are published main bytes,
re-verified on this host before use: the batch-14 published raws at
publication commit 7b211d38 (q042.p1/q042.p2, status.log, batch-keys.json
sha256 dfde0e90...) and the current canonical exact-S5 verdict cache
6,120 rows sha256 be9cb24e... (the Part AS adoption output, published at
commit 8c42e44c).

This is an IF-ADOPTED increment for the scrutiny owner's adoption-decision
precomputation (k04 / b018 / d002 / e002 / r001 / r002 precedent).  The WIN
row q042 (s5_index 745184, key [1152921505747697664, 1032], result 1,
9,149,084 nodes) is NOT consumed anywhere by this Part: the canonical cache
stays byte-identical, and the merged if-adopted cache produced downstream is
a PROJECTION, not the repo canonical chain.  Adoption (and its C++
second-implementation gate 9193f5b6...) stays the scrutiny owner's sole
call; this Part neither recommends nor rejects adoption.

Fail-closed gates: the q042 verdict is byte-taken from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes, lo, hi);
result must be 1 (WIN) and budget 15,000,000 and stones 5; legal and (lo,hi)
must match the published batch-keys.json row for q042 (key_id, s5_index
745184, legal 85); the status.log must carry the matching
`q042 PASS 15000000,1,9149084` row plus the `q042 WIN-HALT` and
WAVE-END stop=1 stop rows; the key must be ABSENT from the canonical BASE
cache (6,120 rows, sha256 be9cb24e...) and absent from the quarantine
registry; and the key must be canonical-safe per the published evidence
policy.  Emission: 1-row increment cache + a manifest JSON recording the
BASE pins and the win-scenario bookkeeping.  11x11 stays UNKNOWN; nodes are
bookkeeping, never verdicts.
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
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class23101-batch14-20261122"
BATCH_KEYS_SHA_EXPECTED = "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"
BASE_CACHE_SHA_EXPECTED = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
WIN_ID = "q042"
WIN_S5_INDEX = 745184
WIN_LO = 1152921505747697664
WIN_HI = 1032
WIN_NODES = 9149084
BUDGET = 15000000


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


def main():
    for name, p, want in (("base cache", BASE_CACHE, BASE_CACHE_SHA_EXPECTED),
                          ("batch-keys", BATCH_DIR / "input/batch-keys.json", BATCH_KEYS_SHA_EXPECTED)):
        got = sha(p)
        if got != want:
            sys.exit(f"ABORT {name} sha256 drift: {got} != {want}")

    # --- two-pass WIN verification from the published raws --------------------
    variants = {}
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{WIN_ID}.{tag}.out"
        if not p.is_file():
            sys.exit(f"ABORT missing raw {p}")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys.exit(f"ABORT {WIN_ID}: pass mismatch {tag} {r} vs p1 {ref}")
    if (ref["result"] != 1 or ref["stones"] != 5 or ref["budget"] != BUDGET
            or ref["nodes"] != WIN_NODES or ref["lo"] != WIN_LO or ref["hi"] != WIN_HI):
        sys.exit(f"ABORT {WIN_ID} raw is not the published WIN row: {ref}")

    # --- batch-keys agreement -------------------------------------------------
    bk = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())
    if bk["class_index"] != 23101:
        sys.exit(f"ABORT batch-keys class_index {bk['class_index']} != 23101")
    rows = [k for k in bk["keys"] if k["key_id"] == WIN_ID]
    if len(rows) != 1:
        sys.exit(f"ABORT {WIN_ID} not unique in batch-keys")
    k = rows[0]
    if (int(k["s5_index"]) != WIN_S5_INDEX or int(k["lo"]) != WIN_LO
            or int(k["hi"]) != WIN_HI or int(k["legal"]) != ref["legal"]):
        sys.exit(f"ABORT {WIN_ID} batch-keys disagreement: {k} vs raw {ref}")

    # --- status.log agreement incl. the published WIN-HALT stop rows ----------
    status_lines = (BATCH_DIR / "output/status.log").read_text().splitlines()
    pass_re = re.compile(rf"^\S+ {WIN_ID} PASS (\d+),(\d+),(\d+)$")
    hw_re = re.compile(rf"^\S+ {WIN_ID} WIN-HALT$")
    we_re = re.compile(r"^\S+ WAVE-END (.+) stop=1$")
    matched_pass = matched_halt = matched_wave = None
    for line in status_lines:
        m = pass_re.match(line)
        if m:
            mrow = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if matched_pass is not None and matched_pass != mrow:
                sys.exit(f"ABORT status PASS disagreement for {WIN_ID}")
            matched_pass = mrow
        if hw_re.match(line):
            matched_halt = True
        m = we_re.match(line)
        if m and WIN_ID in m.group(1).split():
            matched_wave = True
    if matched_pass != (BUDGET, 1, WIN_NODES):
        sys.exit(f"ABORT status PASS row for {WIN_ID} is {matched_pass}")
    if not (matched_halt and matched_wave):
        sys.exit("ABORT WIN-HALT / WAVE-END stop=1 rows missing")

    # --- BASE cache + quarantine absence --------------------------------------
    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    if (WIN_LO, WIN_HI) in quarantined_cache_keys():
        sys.exit("ABORT q042 key quarantined")
    if not is_canonical_safe_s5_key((WIN_LO, WIN_HI)):
        sys.exit("ABORT q042 key noncanonical")
    base_rows = 0
    base_hit = False
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for line in stream:
            if not line.startswith("s5verdict,"):
                continue
            base_rows += 1
            parts = line.rstrip("\n").split(",")
            if int(parts[1]) == WIN_LO and int(parts[2]) == WIN_HI:
                base_hit = True
    if base_hit:
        sys.exit("ABORT q042 key already present in the canonical BASE cache")
    if base_rows != 6120:
        sys.exit(f"ABORT BASE cache rows {base_rows} != 6120")

    # --- emission --------------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    incr_path = OUT / "increment-q042-win-ifadopted-20261122.cache"
    header = [
        "# n11 central-reply batch-14 q042 single-WIN if-adopted increment (Part AT, 2026-11-22)",
        "# published Part AT declaration (note amendment 2026-11-22, commit 58938933;",
        "#   observed HEAD-before-push 2f88a495 recorded in the declaration commit message).",
        "# IF-ADOPTED PROJECTION ONLY - the WIN row is NOT consumed by this Part; the",
        "#   canonical cache (be9cb24e..., 6,120 rows) is untouched; adoption of q042",
        "#   stays the scrutiny owner's call (C++ second-implementation gate 9193f5b6...).",
        "# gates: 2-pass (p1/p2) node-exact, status.log WIN-HALT stop-row agreement,",
        "#   batch-keys (sha256 dfde0e90) legal/(lo,hi)/s5_index agreement,",
        "#   ZERO BASE-cache overlap, quarantine 0, canonical-safe key.",
    ]
    lines = header + [f"s5verdict,{WIN_LO},{WIN_HI},5,1,{WIN_NODES}", ""]
    incr_path.write_text("\n".join(lines), encoding="utf-8")
    incr_sha = sha(incr_path)

    manifest = {
        "schema": "batch14-q042-win-ifadopted-increment-manifest-v1",
        "part": "AT",
        "class_index": 23101,
        "win_ids": [WIN_ID],
        "win_s5_index": WIN_S5_INDEX,
        "win_key": [WIN_LO, WIN_HI],
        "win_nodes": WIN_NODES,
        "raw_publication_commit": "7b211d38",
        "row_counts": {"rows": 1, "wins": 1, "losses": 0},
        "ifadopted_only": True,
        "canonical_cache_untouched": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": base_rows,
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "sha256": {"win": incr_sha},
        "interpretation_guard": (
            "if-adopted projection increment for the scrutiny owner's adoption "
            "precomputation: the q042 WIN verdict is NOT consumed, the canonical "
            "cache stays byte-identical, this Part neither recommends nor rejects "
            "adoption; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts"),
    }
    mpath = OUT / "increment-manifest.json"
    mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"OK 1 WIN row -> increment sha256 {incr_sha}")
    print(f"manifest sha256 {sha(mpath)}")


if __name__ == "__main__":
    main()
