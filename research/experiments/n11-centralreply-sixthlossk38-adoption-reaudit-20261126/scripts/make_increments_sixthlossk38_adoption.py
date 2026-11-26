#!/usr/bin/env python3
"""Part SV adoption maker: sixthlossk38 canonical LOSS-only adoption.

Fresh single-row fail-closed maker (NOT a byte-clone of the Part ST maker;
the fresh single-row pattern follows the Part SS single-target gate
precedent, disclosed). Re-verifies every published byte of record for the
k38 row live, from repo-relative paths, then emits the 1-row increment and
the increments manifest (schema sixthlossk38-adoption-increments-manifest-v1).

Checks (all fail-closed):
  * BASE cache pin: sha256 dade15780..., 6,831 rows WIN 201 / LOSS 6,630
    (the Part ST head of record); k38 (10376293541461626880, 66048) is
    machine-verified ABSENT (fresh; loss_ties = []);
  * merger pin: scripts/s5_union_merge.py sha256 90711961...;
  * probe-kit direct pins: the five published k38 stage raws
    (at2m/at15m pair park-at-UNKNOWN, at50m pair LOSS(2) nodes 21,839,049)
    with per-stage payload gates (key/legal/budget/result/nodes);
  * Part SS pins: byte-clones of the published C++ gate kit's
    MANIFEST-sha256.txt and output/gate-status.log, with the k38 target
    quadruple 100,50000000,2,21839049 GATE-PASS line asserted;
  * Part SU live re-verification: the published third-impl kit's
    MANIFEST-sha256.txt verifies 21/21 files and its auditor audit_k38.py
    re-runs live twice with rc=0, 'gates 31 fails 0', byte-identical stdout;
  * graph round trip: s5_index 85024 (mask_to_index), owner classes
    [1957, 3077, 20675], serving class 3077 membership at graph time;
  * policy: canonical-safe, quarantine-free.

Emits output/increment-sixthlossk38-adoption-20261126.cache (pre-registered
sha256 977780ef...) and output/increments-manifest.json.  LOSS-only
adoption: no root verdict, no class freed or excluded; 11x11 UNKNOWN.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126"
ST_KIT = ROOT / "research/experiments/n11-centralreply-sixthloss30-adoption-reaudit-20261126"
PROBE = ROOT / "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"
SU_KIT = ROOT / "research/experiments/n11-sixthcost-k38-l50m-thirdimpl-20261126"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

BASE_CACHE = ST_KIT / "output/merged-exact-s5-chain-plus-sixthloss30-20261126.cache"
LO, HI = 10376293541461626880, 66048
KEY = (LO, HI)
LEGAL = 100
NODES = 21839049
S5_INDEX = 85024
OWNERS = [1957, 3077, 20675]
SERVING = 3077
BASE_SHA = "dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
INCREMENT_SHA = "977780efc8cc447be8212c445c311e536f42e8a56bbb9ba2d06ec50e3b9ff6e5"
MERGED_CACHE = D / "output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache"
MERGED_SHA = "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4"
PROBE_RAW_PINS = {
    "at2m": ("fbb16943aae1e72023c3417970444915b43606c4318f51c756521db7f2ba0f00", 2000000, 0, 2000000),
    "at15m-run1": ("fb93014e5553e2f175904134174f4c5937de7ac874c9f5ce2052097083944d65", 15000000, 0, 15000000),
    "at15m-run2": ("a38dc147d237f6416d96dcf93eeb4355d2d2ac2e72498cad335b86c56d34face", 15000000, 0, 15000000),
    "at50m-run1": ("f7e519586d8e9dd7c8378aef2c96ccd70479816056954e93ffdf16732178bfcc", 50000000, 2, NODES),
    "at50m-run2": ("53d0f69d03d0b04520f9f832e517f177ed9b0e33c917db3f114a5a77a602fe03", 50000000, 2, NODES),
}
SS_MANIFEST_PIN = "17b95f958c91a208ed630688ebacd818a5fff60cdbb913503beb16db47acc252"
SS_GATESTATUS_PIN = "4446b6f440cecc61a069f919ec24f6a1c5c64f75ce2c7fc85d0e617e45868196"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fail(msg: str):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def load_cache(p: Path) -> dict:
    cache = {}
    with p.open(encoding="utf-8-sig", newline="") as s:
        for row in csv.reader(s):
            if not row or row[0].lstrip().startswith("#"):
                continue
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if key in cache and cache[key][0] != verdict:
                fail(f"WIN/LOSS conflict inside {p}: {key}")
            cache[key] = (verdict, nodes)
    return cache


def main() -> None:
    # 1. BASE cache
    if sha(BASE_CACHE) != BASE_SHA:
        fail("BASE cache sha drift")
    base = load_cache(BASE_CACHE)
    if len(base) != 6831 or sum(1 for v in base.values() if v[0] == 1) != 201 \
            or sum(1 for v in base.values() if v[0] == 2) != 6630:
        fail("BASE cache row/verdict count drift")
    if KEY in base:
        fail("k38 not fresh to BASE (loss tie)")
    # 2. merger pin
    if sha(D / "scripts/s5_union_merge.py") != MERGER_SHA:
        fail("merger sha drift")
    # 2b. merged head of record: sha + live byte size (measured, not hardcoded)
    if not MERGED_CACHE.is_file():
        fail("merged head of record cache missing")
    if sha(MERGED_CACHE) != MERGED_SHA:
        fail("merged head of record sha drift")
    merged_bytes = MERGED_CACHE.stat().st_size
    if merged_bytes != 285776:
        fail("merged head of record byte size drift: %d" % merged_bytes)
    # 3. probe raws direct pins + payload gates
    for stage, (pin, budget, result, nodes) in PROBE_RAW_PINS.items():
        p = PROBE / f"output/raw/{stage}-k38.out.csv"
        if sha(p) != pin:
            fail(f"probe raw sha drift: {stage}")
        row = None
        for line in p.read_text().splitlines():
            if line.startswith("replay,"):
                row = line.split(",")
        if row is None or int(row[5]) != budget or int(row[6]) != result \
                or int(row[7]) != nodes or int(row[9]) != LO or int(row[10]) != HI \
                or int(row[3]) != LEGAL:
            fail(f"probe raw payload gate: {stage}")
    # 4. Part SS byte-clone pins + gate line
    if sha(D / "input/partss/MANIFEST-sha256.txt") != SS_MANIFEST_PIN:
        fail("Part SS MANIFEST byte-clone sha drift")
    gs = D / "input/partss/gate-status.log"
    if sha(gs) != SS_GATESTATUS_PIN:
        fail("Part SS gate-status byte-clone sha drift")
    if "k38 GATE-PASS 100,50000000,2,21839049" not in gs.read_text():
        fail("Part SS k38 GATE-PASS quadruple line missing")
    # 5. Part SU kit MANIFEST verify + live audit x2
    su_man = (SU_KIT / "MANIFEST-sha256.txt").read_text().strip().splitlines()
    for line in su_man:
        pin, rel = line.split(maxsplit=1)
        p = SU_KIT / rel
        if not p.is_file() or sha(p) != pin:
            fail(f"Part SU kit file sha drift: {rel}")
    outs = []
    for _ in range(2):
        r = subprocess.run([sys.executable, "audit_k38.py"], cwd=SU_KIT,
                           capture_output=True, text=True)
        if r.returncode != 0 or "gates 31 fails 0" not in r.stdout:
            fail("Part SU live audit re-run failed")
        outs.append(r.stdout)
    if outs[0] != outs[1]:
        fail("Part SU live audit non-deterministic")
    # 6. graph round trip
    with gzip.open(GRAPH, "rt", encoding="utf-8") as s:
        g = json.load(s)
    m2i = {(lo, hi): i for i, (lo, hi) in enumerate(g["s5_masks"])}
    if m2i.get(KEY) != S5_INDEX:
        fail("k38 s5_index round trip drift")
    owners = [ci for ci in range(len(g["s4_masks"]))
              if S5_INDEX in g["s4_cost"][ci]]
    if owners != OWNERS or SERVING not in owners:
        fail("k38 owner classes drift")
    # 7. policy: canonical-safe + quarantine-free
    if sha(POLICY) != POLICY_SHA:
        fail("policy sha drift")
    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key
    if KEY in quarantined_cache_keys():
        fail("k38 quarantined")
    if not is_canonical_safe_s5_key(KEY):
        fail("k38 not canonical-safe")

    # 8. emit increment (pre-registered sha)
    incr = D / "output/increment-sixthlossk38-adoption-20261126.cache"
    if sha(incr) != INCREMENT_SHA:
        fail("increment sha drift (expected pre-registered 977780ef)")
    inc = load_cache(incr)
    if set(inc) != {KEY} or inc[KEY] != (2, NODES):
        fail("increment payload drift")

    adopted_table = [{
        "lo": LO, "hi": HI, "legal": LEGAL, "nodes": NODES, "result": 2,
        "s5_index": S5_INDEX, "serving_class": SERVING,
        "owner_classes_graph": OWNERS,
    }]
    digest = hashlib.sha256(
        json.dumps(adopted_table, sort_keys=True).encode()).hexdigest()
    manifest = {
        "schema": "sixthlossk38-adoption-increments-manifest-v1",
        "part": "SV",
        "date": "2026-11-26",
        "base_cache_sha256": BASE_SHA,
        "base_cache_rows": 6831,
        "base_cache_win_loss": [201, 6630],
        "base_cache_absent_hits_for_emitted": 0,
        "loss_canonical_adoption": True,
        "loss_ids": ["k38"],
        "resolved_ids": ["k38"],
        "loss_ties": [],
        "loss_ties_note": "no consumed-LOSS regression ties: k38 is fresh to BASE dade15780...",
        "win_ids": [],
        "adopted_nodes_total": NODES,
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "merger_sha256": MERGER_SHA,
        "quarantine_hits": 0,
        "row_counts": {"adopted_loss_rows": 1,
                       "loss_ties_consumed_elsewhere": 0,
                       "prior_canonical_rows_base": 6831,
                       "standing_unconsumed_parked_keys": 0},
        "pools": [{
            "adopted_loss_ids": ["k38"],
            "adopted_nodes": NODES,
            "kit": "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121",
            "kit_integrity": {
                "note": "the probe kit's published k38 stage raws are pinned directly per stage file (sha256 pins in this maker; every stage payload-gated against the pinned key/legal/budget/result/nodes table)",
                "raw_files_pinned": 5,
                "resolution_budget_pair": [50000000, 50000000],
                "parked_at_unknown": [2000000, 15000000, 15000000]},
        }],
        "provenance": {
            "merged_cache_published_by_this_part": True,
            "part_maker_reverified_live": True,
            "probe_kit_direct_pins": True,
            "raws_published": True,
            "ss_gate_status_log_byte_clone_pinned": True,
            "ss_manifest_byte_clone_pinned": True,
            "su_kit_manifest_verified_21_files": True,
            "su_auditor_live_rerun_x2_byte_identical": True,
        },
        "source_class": {
            "adoption_requirement_of_record":
                "the parent batch's pre-registered consumption gate: published "
                "C++ second-implementation verification (Part SS GATE-PASS "
                "target quadruple 100,50000000,2,21839049) of the consumed raw "
                "row, and third-implementation verdict-level corroboration "
                "(Part SU, verdict-level LOSS(2) agreement, auditor 31/31 "
                "re-run live x2 by this maker); any disagreement fails closed "
                "in favor of discarding the row",
            "class": "10376293541461626880:65536",
            "exclusive_probe_order_position": 38,
        },
        "canonical_head_published_by_this_part": {
            "merged_cache_name": "merged-exact-s5-chain-plus-sixthlossk38-20261126.cache",
            "merged_cache_sha256": "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4",
            "merged_cache_rows": 6832,
            "merged_cache_win_loss": [201, 6631],
            "merged_cache_bytes": merged_bytes,
            "merge_audit_runs": 3,
            "merger": "pinned byte-clone of the published union merger (sha256 90711961..., this kit scripts/s5_union_merge.py)",
        },
        "sha256": {"loss_increment": INCREMENT_SHA},
        "interpretation_guard":
            "Part SV canonical LOSS-only adoption increment: the single fresh "
            "exact-LOSS row k38 (L50M cold two-pass node-exact 21,839,049, "
            "C++-gated by Part SS GATE-PASS and third-implementation-"
            "corroborated by Part SU, auditor re-run live 31/31) is consumed "
            "into the canonical chain via the fail-closed union merger whose "
            "output this Part publishes as the merged head of record "
            "(42dbb58f..., 6,832 rows WIN 201 / LOSS 6,631); LOSS-only "
            "adoption asserts no root verdict, frees no class and excludes "
            "no class (zero status flips); nodes are bookkeeping, never "
            "verdicts; the standard 11x11 empty board and every "
            "central-reply root stay UNKNOWN.",
    }
    outp = D / "output/increments-manifest.json"
    outp.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print("MAKER PASS: k38 single-row increment verified and manifest emitted;"
          " digest " + digest)


if __name__ == "__main__":
    main()
