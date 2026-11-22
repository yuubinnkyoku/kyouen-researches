#!/usr/bin/env python3
"""Joint 17 unconsumed-closure-WIN if-adopted increment maker (Part BB, 2026-11-22).

Fail-closed builder of the single 17-row WIN increment for the Part BB
joint if-adopted projection (declaration: note amendment commit dafe9651,
observed HEAD-before-push 53e7fae9).  Part BB adopts, IN ONE PROJECTION,
every unconsumed closure WIN row of the repo history:

  b018 d002 e002 f017 g018 h045 j033 z003 n005 n006   (Part AJ wins10)
  p002 p003                                          (batch-13, Part AI)
  r001 r002                                          (batch-15, Part AN)
  q042                                               (batch-14, Part AT)
  v001 v002                                          (batch-18, Part BA)

The rows are NOT re-derived from raws here: each row was already
machine-verified against its 2-pass raw passes, status logs, batch-keys
and quarantine registry at its own publication.  This maker re-verifies
the published increment bytes by sha256 and cross-checks the published
manifests, then asserts the joint packet against the CURRENT canonical
BASE (6,120 rows, be9cb24e..., Part AS) and the pinned graph/evidence
infrastructure.  IF-ADOPTED projection only: no verdict is consumed
anywhere, the canonical cache stays byte-identical, and this Part
neither recommends nor rejects adoption.  11x11 stays UNKNOWN; nodes
are bookkeeping, never verdicts.
"""
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

_here = Path(__file__).resolve()
_CANDS = [q for q in _here.parents if (q / "research" / "experiments").is_dir()]
if not _CANDS:
    raise SystemExit("GATE FAILED: repo root (research/experiments) not found above this script")
ROOT = _CANDS[0]
EXP = _here.parents[1]

INPUT = EXP / "input"
OUT_CACHE = EXP / "output/increment-17win-joint-IFADOPTED-20261122.cache"
OUT_MANIFEST = EXP / "output/increment-manifest.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"

# --- published pins (byte chains to the published machine verifications) ---
SOURCES = [
    {"name": "part-aj-wins10", "incr": "incr-aj-wins10.cache", "manifest": "manifest-aj.json",
     "incr_sha": "fe2c6f68f49195b44e21c8d43998fccd965c868e08e49d8a1b3233f5daa4c15e",
     "manifest_sha": "74fb877dba862bb8d8ecaa28d4741fbc97f533087e1779fe49a3062af2600b88",
     "rows": 10, "win_ids": ["b018", "d002", "e002", "f017", "g018", "h045", "j033",
                             "z003", "n005", "n006"]},
    {"name": "batch13-wins2", "incr": "incr-b13-wins2.cache", "manifest": "manifest-b13.json",
     "incr_sha": "bb238f67dbfcc3b9a05ac5542f783107366777f17149f7a5a5af64d4864b0f7c",
     "manifest_sha": "43143fd51bb02ddf65d912018f063e631a70517d607c2a73a626b76bd8e5957c",
     "rows": 2, "win_ids": ["p002", "p003"]},
    {"name": "batch15-wins2", "incr": "incr-b15-wins2.cache", "manifest": "manifest-b15.json",
     "incr_sha": "05c10e1ff17c2601b1fb4a0782af2543d302187ce6344df97d3c763947262b7d",
     "manifest_sha": "d6ed7b931fb3418ceb8879073b2668b184e3dfcc7a2d24230267fdb7da67777e",
     "rows": 2, "win_ids": ["r001", "r002"]},
    {"name": "batch14-q042", "incr": "incr-q042.cache", "manifest": "manifest-q042.json",
     "incr_sha": "b4958328270f11b24d3a638e1099a0c6047dbebb242e3116217b0473ef63f9b6",
     "manifest_sha": "894e9420b043e12543920bb63c49f00530e45ad5b29c95c65e3dadf3047fc02e",
     "rows": 1, "win_ids": ["q042"]},
    {"name": "batch18-v001v002", "incr": "incr-b18-wins2.cache", "manifest": "manifest-b18.json",
     "incr_sha": "4f8fc29bfd00492aa9a983f20a121737d395b8f80d53e2b04c271fec068bc1ee",
     "manifest_sha": "13736030ea484a0496da7f929b9c6892a2e9ebf6522f96d1c87d2c21000945f1",
     "rows": 2, "win_ids": ["v001", "v002"]},
]

GRAPH_SHA = "54f9c364"
UPDATE8_SHA = "b658290a"
BOARD_SHA = "954d3a10"
POLICY_SHA = "78655e94"
QUARANTINE_SHA = "81d23160"
BASE_CACHE_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_cache_rows(path):
    rows = []
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        for lineno, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                fail(f"invalid cache row {lineno} in {path}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                fail(f"invalid cache verdict at row {lineno} in {path}: {row}")
            rows.append((lo, hi, verdict, nodes))
    return rows


def main():
    # --- infrastructure pins ---------------------------------------------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    if sha(BOARD_SOURCE).startswith(BOARD_SHA) is False:
        fail("Board source pin drift")
    if not sha(POLICY).startswith(POLICY_SHA):
        fail("policy pin drift")
    if not sha(QUARANTINE).startswith(QUARANTINE_SHA):
        fail("quarantine pin drift")
    if not sha(GRAPH).startswith(GRAPH_SHA):
        fail("graph pin drift")
    if not sha(UPDATE8).startswith(UPDATE8_SHA):
        fail("update8 pin drift")

    quarantined = quarantined_cache_keys()

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        fail("update8 schema drift")
    baseline_req = set(update8["required_new_s5"])
    if update8["union_size"] != len(baseline_req) or update8["union_size"] != 31859:
        fail("update8 baseline drift")

    # --- source increments and manifests ---------------------------------------
    all_rows = []
    for src in SOURCES:
        inc_path = INPUT / src["incr"]
        man_path = INPUT / src["manifest"]
        got = sha(inc_path)
        if got != src["incr_sha"]:
            fail(f"{src['name']} increment sha drift: {got} != {src['incr_sha']}")
        gots = sha(man_path)
        if gots != src["manifest_sha"]:
            fail(f"{src['name']} manifest sha drift: {gots} != {src['manifest_sha']}")
        manifest = json.loads(man_path.read_text())
        rows = read_cache_rows(inc_path)
        wins = [r for r in rows if r[2] == 1]
        losses = [r for r in rows if r[2] == 2]
        if len(rows) != src["rows"] or len(wins) != src["rows"] or losses:
            fail(f"{src['name']}: expected {src['rows']} WIN rows, got "
                 f"{len(wins)} WIN / {len(losses)} LOSS of {len(rows)}")
        # manifest cross-agreement (per-source published bookkeeping)
        for key, want in (("base_cache_absent_hits", 0), ("quarantine_hits", 0)):
            if manifest.get(key) != want:
                fail(f"{src['name']} manifest {key} != {want}")
        m_sha_win = manifest.get("sha256", {}).get("win")
        if m_sha_win != src["incr_sha"]:
            fail(f"{src['name']} manifest sha256.win does not chain to the increment")
        for wid in src["win_ids"]:
            flat = json.dumps(manifest.get("win_ids", "")).replace(" ", "")
            if wid not in flat:
                fail(f"{src['name']} manifest win bookkeeping lacks {wid}")
        all_rows.extend((src["name"],) + r for r in wins)

    # --- joint packet gates -----------------------------------------------------
    if len(all_rows) != 17:
        fail(f"joint packet holds {len(all_rows)} rows, expected 17")
    by_key = {}
    for src, lo, hi, verdict, nodes in all_rows:
        key = (lo, hi)
        if key in by_key:
            fail(f"duplicate WIN key across sources: {key}")
        by_key[key] = {"source": src, "lo": lo, "hi": hi,
                       "verdict": verdict, "nodes": nodes}
    if len(by_key) != 17:
        fail("joint key set is not 17 unique keys")

    # q042 / b18 manifests pin exact keys, s5 indices and nodes (machine chain)
    q_man = json.loads((INPUT / "manifest-q042.json").read_text())
    q_key = tuple(q_man["win_key"])
    if by_key.get(q_key) is None or by_key[q_key]["nodes"] != q_man["win_nodes"]:
        fail("q042 manifest key/nodes not present verbatim in the packet")
    if q_man["win_s5_index"] != mask_to_index.get(q_key):
        fail("q042 manifest s5 index != graph mapping of its key")
    b_man = json.loads((INPUT / "manifest-b18.json").read_text())
    for k, n, s5 in zip(b_man["win_keys"], b_man["win_nodes"], b_man["win_s5_index"]):
        key = tuple(k)
        if by_key.get(key) is None or by_key[key]["nodes"] != n:
            fail("b18 manifest key/nodes not present verbatim in the packet")
        if mask_to_index.get(key) != s5:
            fail("b18 manifest s5 index != graph mapping of its key")

    # --- BASE / quarantine / canonical-safety / universe -----------------------
    base_rows = read_cache_rows(BASE_CACHE)
    if sha(BASE_CACHE) != BASE_CACHE_SHA:
        fail("canonical BASE cache sha drift")
    base_keys = {(lo, hi) for lo, hi, _v, _n in base_rows}
    if len(base_rows) != 6120 or len(base_keys) != 6120:
        fail(f"BASE cache is not 6,120 unique rows: {len(base_rows)}")
    in_baseline_req = 0
    for key, meta in by_key.items():
        if key in base_keys:
            fail(f"WIN row already inside canonical BASE (would NOT be if-adopted): {key}")
        if key in quarantined:
            fail(f"WIN row is quarantined: {key}")
        if not is_canonical_safe_s5_key(key):
            fail(f"WIN row is not canonical-safe: {key}")
        idx = mask_to_index.get(key)
        if idx is None:
            fail(f"WIN key outside the pinned s5 universe: {key}")
        meta["s5_index"] = idx
        if idx in baseline_req:
            in_baseline_req += 1

    # --- write the 17-row joint increment (sorted by (lo,hi)) ------------------
    OUT_CACHE.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(by_key.items(), key=lambda kv: (kv[1]["lo"], kv[1]["hi"]))
    header = [
        "# n11 central-reply closure JOINT 17 unconsumed-WIN if-adopted increment (Part BB, 2026-11-22)",
        "# sources (published sha-pinned increments; raw 2-pass verification chain per source):",
        "#   part-aj-wins10  fe2c6f68... (b018 d002 e002 f017 g018 h045 j033 z003 n005 n006)",
        "#   batch13-wins2   bb238f67... (p002 p003)   batch15-wins2 05c10e1f... (r001 r002)",
        "#   batch14-q042    b4958328... (q042)        batch18-v001v002 4f8fc29b... (v001 v002)",
        "# IF-ADOPTED PROJECTION ONLY - no verdict is consumed; the canonical cache",
        "#   (be9cb24e..., 6,120 rows) is byte-identical (machine-reverified); adoption stays",
        "#   the scrutiny owner's call (C++ second-implementation gate 9193f5b6...).",
        "# gates: 5 source increments sha-pinned + manifest-chained, 17 unique WIN keys,",
        "#   ZERO BASE-cache overlap, quarantine 0, canonical-safe keys, s5 universe mapping",
        "#   machine-verified; q042/b18 manifest key/s5/nodes cross-checks machine-passed.",
        "# 17 rows: every unconsumed closure WIN of the repo, adopted TOGETHER in one projection.",
    ]
    body = [f"s5verdict,{lo},{hi},5,1,{meta['nodes']}"
            for (lo, hi), meta in ((k, m) for k, m in ordered)]
    OUT_CACHE.write_text("\n".join(header + body) + "\n", encoding="utf-8")

    incr_sha = sha(OUT_CACHE)
    manifest = {
        "schema": "joint17win-ifadopted-increment-manifest-v1",
        "part": "BB",
        "row_counts": {"rows": 17, "wins": 17, "losses": 0},
        "ifadopted_only": True,
        "canonical_cache_untouched": BASE_CACHE_SHA,
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "win_ids": [wid for src in SOURCES for wid in src["win_ids"]],
        "win_keys": [[lo, hi] for (lo, hi), _meta in ordered],
        "win_nodes": [meta["nodes"] for _key, meta in ordered],
        "win_s5_index": [meta["s5_index"] for _key, meta in ordered],
        "win_s5_in_update8_baseline_requirement": in_baseline_req,
        "sources": [
            {"name": src["name"], "increment_sha256": src["incr_sha"],
             "manifest_sha256": src["manifest_sha"], "rows": src["rows"],
             "win_ids": src["win_ids"]}
            for src in SOURCES
        ],
        "sha256": {"win": incr_sha},
        "interpretation_guard": (
            "joint if-adopted projection increment for the scrutiny owner's "
            "adoption precomputation: NO verdict is consumed, the canonical "
            "cache stays byte-identical, this Part neither recommends nor "
            "rejects adoption; 11x11 stays UNKNOWN; nodes are bookkeeping, "
            "never verdicts"),
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n",
                            encoding="utf-8")
    print("OK 17-WIN joint increment: rows=17 wins=17 losses=0 "
          f"in_baseline_req={in_baseline_req} "
          f"increment_sha256={incr_sha}")


if __name__ == "__main__":
    main()
