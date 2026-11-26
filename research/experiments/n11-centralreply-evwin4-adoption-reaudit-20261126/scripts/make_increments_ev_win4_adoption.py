#!/usr/bin/env python3
"""Part EV maker: evwin4 canonical-adoption increment (2026-11-26).

Fork of the published Part EU maker
`make_increments_eu_win2_adoption.py` (sha256
f2ae97a135af1d7f14b376e5c9d41142025b6a2b4b161ce907cca9cb0356f498;
structural clone, disclosed diff: the adopted-rows table, the referenced
kits, the per-row gate set and the emitted header/manifest fields are
Part-EV specific).
PIN POLICY unchanged: no per-file sha of any kit member is hand-typed in
this script - every per-row pin is extracted from the byte-verified
published kit MANIFESTs and the byte-pinned SSOT registry and re-hashed
live (fail-closed; rc=1 on ANY drift).

(a) BATCH-SOURCE provenance: the four published 2026-11-22 closure-batch
    kits (class 16757 batch 1 / class 20421 batch 3 / class 16371
    batch 4 / class 12264 batch 5): the 15M two-pass fresh-cold
    node-exact jsreplay-replica probe raws of the four targets, each
    batch's batch-keys.json SSOT, input CSV and status.log (the single
    WIN row of each batch halted it: WIN-HALT discipline), re-verified
    here file-by-file against the pins recorded in the published Part EV
    gate SSOT registry input/gate-rows-ev.json.
(b) THIRD-IMPL provenance: the published third-implementation reverify
    kit n11-centralreply-closure-wins-thirdimpl-reverify-20261122
    (MANIFEST.sha256 file-by-file verified here): rows.json replica
    quadruples == batch raws and the a/b passes of every target agree
    verdict-level (WIN) with identical expansion counts.
(c) GATE provenance: the published Part EV C++ second-implementation
    scrutiny gate kit (closure-wins-b018d002e002f017-cppgate-20261125):
    MANIFEST-pinned file-by-file, audit 0327dad8..., 7/7 GATE-PASS
    (4 targets + 3 calibration anchors), audit re-runs 4/4
    byte-identical, gate source pin 9193f5b6... at 154f3b7a (registered
    in gate-rows-ev.json and re-checked here).
(d) FRESHNESS: every adopted (lo,hi) is absent from the canonical BASE
    (the Part EU head 3ba48608..., 6,767 rows WIN 188 / LOSS 6,579)
    and from the quarantine registry 81d23160...; the EU regression tie
    re-checks that both Part-EU adopted rows already sit WIN in the
    BASE cache (they must NOT be re-adopted here).

Adopted here: exactly the 4 Part EV gate-verified UNCONSUMED
closure-batch WIN rows b018 (class 16757 batch-1 dual-class, nodes
3,549,602), d002 (class 20421 batch-3, nodes 5,359,994), e002 (class
16371 batch-4, nodes 14,112,632), f017 (class 12264 batch-5, nodes
3,522,635); adopted node total 26,544,863. No verdict beyond these 4
adopted WIN rows is consumed anywhere; the standard 11x11 empty board
stays UNKNOWN; nodes are bookkeeping.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"

EU_KIT = ROOT / "research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125"
EV_KIT = ROOT / "research/experiments/n11-centralreply-closure-wins-b018d002e002f017-cppgate-20261125"
THIRD_KIT = ROOT / "research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122"
BATCH_KITS = {
    "b018": ROOT / "research/experiments/n11-centralreply-closure-class16757-batch-20261122",
    "d002": ROOT / "research/experiments/n11-centralreply-closure-class20421-batch-20261122",
    "e002": ROOT / "research/experiments/n11-centralreply-closure-class16371-batch4-20261122",
    "f017": ROOT / "research/experiments/n11-centralreply-closure-class12264-batch5-20261122",
}
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
EU_INCREMENT = EU_KIT / "output/increment-euwin2-20261125.cache"

MERGER = EXP / "scripts/s5_union_merge.py"

# ---------------- top-level pins (published bytes are the authority) ------
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA = "3ba486086703b9f44a0c685d7d5b45fab80f86760f2cd032a8dc18a2690233d6"
BASE_CACHE_ROWS = 6767
BASE_CACHE_WIN = 188
BASE_CACHE_LOSS = 6579
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
EU_INCREMENT_SHA = "d9365d80a90aff30cb451f8f2519ab2cc004c6d10ba4fb149a7ee340e0aa0b4f"
EU_ADOPTED_COUNT = 2

EV_MANIFEST_SHA = "34d7768bc68e0829ac725d33c91de0dea147dcc89239e3736dc4b1a06ddce9cb"
EV_REGISTRY_SHA = "3ba154f2f803a7a25de0133ac0fd0c3ed2df4c4ce7733bec4c8adc01e064659f"
EV_AUDIT_SHA = "0327dad83f7c33d475656d8d1f9ccd2e67c3b78f8f394b9a5daf74c2b96c91c4"
EV_AUDIT_SCHEMA = "n11-centralreply-cppgate-wins41164-audit-v1"
EV_REGISTRY_SCHEMA = "n11-centralreply-cppgate-wins41164-rows-v1"
EV_STATUS_PASS = 7
EV_GATE_SOURCE_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
EV_GATE_SOURCE_COMMIT = "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
EV_BUDGET = 15000000
EV_KEYS = 4
EV_ANCHORS = {
    "anchor-at2m": "98,2000000,0,2000000",
    "anchor-af039": "89,30000000,2,19234232",
    "anchor-aj001": "84,30000000,2,5156075",
}

THIRD_MANIFEST_SHA = "c5ed44146a1f4e1861b21831eded31b27c82824c9c5fe41a36491856b28a32d8"
THIRD_ROWS_SHA = None  # extracted from the verified thirdimpl MANIFEST, never hand-typed
THIRD_TELEMETRY = "# forbidden quadruples: 95670"

ADOPTED = {
    "b018": (528497, 1153204079095189504, 65536),
    "d002": (197253, 3461016313634230272, 131072),
    "e002": (183566, 1153765929805414400, 16),
    "f017": (415095, 1188950301625810945, 70368744177666),
}
ADOPTED_IDS = ["b018", "d002", "e002", "f017"]
ADOPTED_CLASS = {"b018": 16757, "d002": 20421, "e002": 16371, "f017": 12264}
ADOPTED_LEGAL = {"b018": 60, "d002": 73, "e002": 79, "f017": 82}
ADOPTED_NODES = {"b018": 3549602, "d002": 5359994, "e002": 14112632, "f017": 3522635}
ADOPTED_NODES_TOTAL = 26544863
MEMBERSHIP_CLASS_COUNT = {"b018": 3, "d002": 4, "e002": 4, "f017": 3}

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
THIRD = re.compile(r"^third,([a-z0-9]+)([ab]),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+),(clean),(.+)$")


def fail(msg):
    print(f"ABORT ev-max: {msg}", file=sys.stderr)
    raise SystemExit(1)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def parse_manifest(path: Path, kit_root: Path):
    out = {}
    kit_prefix = f"research/experiments/{kit_root.name}/"
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f = line.split()
        if len(f) < 2 or not HEX64.match(f[0]):
            fail(f"unexpected MANIFEST line in {path}: {line!r}")
        s = f[0]
        size = blob1 = None
        rel = f[-1]
        if len(f) >= 3:
            mid = f[1]
            if mid.isdigit():
                size = int(mid)
            elif HEX40.match(mid):
                blob1 = mid
            else:
                fail(f"unexpected MANIFEST middle field in {path}: {line!r}")
        if ".." in rel.split("/") or rel.startswith("/"):
            fail(f"unsafe MANIFEST path in {path}: {rel}")
        if rel.startswith(kit_prefix):
            key, local = rel[len(kit_prefix):], ROOT / rel
        elif rel.startswith("research/") or rel.startswith("results/"):
            key, local = rel, ROOT / rel
        else:
            key, local = rel, kit_root / rel
        if key in out and out[key]["sha256"] != s:
            fail(f"duplicate MANIFEST path with conflicting sha in {path}: {key}")
        out[key] = {"sha256": s, "size": size, "blob_sha1": blob1, "local": local}
    return out


def parse_raw(path: Path):
    rows = []
    text = path.read_text()
    seen_done = False
    for line in text.splitlines():
        if line.startswith("replay,"):
            m = REPLAY.match(line)
            if not m:
                fail(f"replay regex mismatch in {path}")
            rows.append({"id": int(m.group(1)), "stones": int(m.group(2)),
                         "legal": int(m.group(3)), "is_or": int(m.group(4)),
                         "budget": int(m.group(5)), "result": int(m.group(6)),
                         "nodes": int(m.group(7)), "lo": m.group(9), "hi": m.group(10)})
        if line.startswith("# replay_done") or " replay_done" in line:
            seen_done = True
    if len(rows) != 1 or not seen_done:
        fail(f"raw {path} must hold exactly one replay row plus the replay_done guard")
    return rows[0]


def check_two_pass(p1: Path, p2: Path, sha1: str, sha2: str):
    got1, got2 = sha(p1), sha(p2)
    if got1 != sha1 or got2 != sha2:
        fail(f"raw sha drift vs the manifest-pin pair: {p1} {got1}/{sha1} {p2} {got2}/{sha2}")
    r1 = parse_raw(p1)
    r2 = parse_raw(p2)
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    if tuple(r1[f] for f in fields) != tuple(r2[f] for f in fields):
        fail(f"two-pass raw disagreement (fresh-cold node-exact gate): {p1}")
    return r1


def verify_kit(kit: Path, man_sha: str, man_name: str, tag: str) -> dict:
    man = kit / man_name
    if sha(man) != man_sha:
        fail(f"kit MANIFEST sha drift ({tag})")
    entries = parse_manifest(man, kit)
    for rel, rec in entries.items():
        p = rec["local"]
        if not p.is_file():
            fail(f"kit file missing ({tag}): {rel}")
        if sha(p) != rec["sha256"]:
            fail(f"kit sha drift ({tag}): {rel}")
        if rec["size"] is not None and p.stat().st_size != rec["size"]:
            fail(f"kit size drift ({tag}): {rel}")
    return entries


def manifest_sha(entries: dict, kit_tag: str, rel: str) -> str:
    if rel not in entries:
        fail(f"pin absent from {kit_tag} MANIFEST: {rel}")
    return entries[rel]["sha256"]


def main() -> None:
    # G0: merger byte-clone + BASE identity + quarantine + EU regression basis
    if sha(MERGER) != MERGER_SHA:
        fail("union merger byte-clone sha drift (expected 90711961...)")
    base_cache = EU_KIT / "output/merged-exact-s5-chain-plus-euwin2-20261125.cache"
    if sha(base_cache) != BASE_CACHE_SHA:
        fail("BASE cache sha drift (expected 3ba48608...)")
    if sha(QUARANTINE) != QUARANTINE_SHA:
        fail("quarantine registry sha drift")
    if sha(EU_INCREMENT) != EU_INCREMENT_SHA:
        fail("EU increment sha drift (expected d9365d80...)")

    base_rows = {}
    for line in base_cache.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) != 6 or parts[0] != "s5verdict":
            fail(f"BASE cache malformed row: {line!r}")
        lo, hi, depth, verdict, nodes = (int(x) for x in parts[1:])
        if depth != 5 or verdict not in (1, 2):
            fail("BASE cache depth/verdict domain drift")
        base_rows[(lo, hi)] = (verdict, nodes)
    wins = sum(1 for v, _ in base_rows.values() if v == 1)
    if len(base_rows) != BASE_CACHE_ROWS or wins != BASE_CACHE_WIN or \
            len(base_rows) - wins != BASE_CACHE_LOSS:
        fail(f"BASE accounting drift: rows {len(base_rows)} win {wins}")

    # EU regression tie: both Part-EU adopted rows sit WIN in BASE, not re-adopted here
    eu_inc = {}
    for ln in EU_INCREMENT.read_text(encoding="utf-8-sig").splitlines():
        if ln.startswith("s5verdict,"):
            p = ln.split(",")
            eu_inc[(int(p[1]), int(p[2]))] = (int(p[4]), int(p[5]))
    if len(eu_inc) != EU_ADOPTED_COUNT:
        fail(f"EU increment row count drift: {len(eu_inc)}")
    for pair, (verdict, nodes) in eu_inc.items():
        if pair not in base_rows or base_rows[pair][0] != 1 or verdict != 1:
            fail(f"EU regression tie broken: {pair} not WIN in BASE")
        if base_rows[pair][1] != nodes:
            fail(f"EU regression nodes tie broken: {pair}")
    for kid in ADOPTED:
        if (ADOPTED[kid][1], ADOPTED[kid][2]) in eu_inc:
            fail(f"an adopted key equals a Part-EU adopted key: {kid}")

    quarantined = json.loads(QUARANTINE.read_text())
    qkeys = set()
    for entry in quarantined if isinstance(quarantined, list) else quarantined.get("keys", []):
        if isinstance(entry, dict) and "lo" in entry:
            qkeys.add((int(entry["lo"]), int(entry["hi"])))

    # G1: whole-kit file-by-file integrity of the two referenced published kits
    ev_mans = verify_kit(EV_KIT, EV_MANIFEST_SHA, "MANIFEST-sha256.txt", "ev")
    third_mans = verify_kit(THIRD_KIT, THIRD_MANIFEST_SHA, "MANIFEST.sha256", "thirdimpl")

    # G2: EV gate-kit machine audit + status honesty + audit determinism
    if sha(EV_KIT / "output/audit_gate.json") != EV_AUDIT_SHA:
        fail("EV gate-kit machine audit sha drift")
    audit = json.loads((EV_KIT / "output/audit_gate.json").read_text())
    if audit.get("overall") != "PASS" or audit.get("part") != "EV" or \
            audit.get("schema") != EV_AUDIT_SCHEMA:
        fail("EV gate-kit audit honesty drift")
    for rn in ("run1", "run2", "run3", "run4"):
        if sha(EV_KIT / f"output/audit_gate.{rn}.json") != EV_AUDIT_SHA:
            fail(f"EV audit re-run determinism drift ({rn})")
    if sha(EV_KIT / "input/gate-rows-ev.json") != EV_REGISTRY_SHA:
        fail("EV registry sha drift (expected 3ba154f2...)")
    registry = json.loads((EV_KIT / "input/gate-rows-ev.json").read_text())
    if registry.get("schema") != EV_REGISTRY_SCHEMA:
        fail("EV registry schema drift")
    gs = registry.get("gate_source", {})
    if gs.get("sha256") != EV_GATE_SOURCE_SHA or not gs.get("commit", "").startswith("154f3b7a"):
        fail("EV registry gate-source pin drift")
    bad_gates = [k for k, v in audit["gates"].items() if v.get("status") != "PASS"]
    if bad_gates:
        fail(f"EV audit has non-PASS gates: {bad_gates[:4]}")
    if audit["gates"].get("G4", {}).get("detail") != "passes=7/7 bad=0":
        fail("EV audit G4 aggregate drift")
    ok = 0
    bad = []
    for line in (EV_KIT / "output/gate-status.log").read_text().splitlines():
        if " GATE-PASS " in line:
            ok += 1
        elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line or "TRUNCATED" in line:
            bad.append(line)
    if ok != EV_STATUS_PASS or bad:
        fail(f"EV gate-status accounting drift: ok {ok} bad {bad}")
    if registry.get("anchors") != EV_ANCHORS:
        fail("EV registry anchor table drift")
    for ak, aexp in EV_ANCHORS.items():
        rec = audit["rows"].get(ak)
        if rec is None or rec.get("expected") != aexp or rec.get("observed_p1") != aexp:
            fail(f"EV anchor row drift: {ak} {rec}")
        for g in (f"G1:{ak}:p1", f"G1:{ak}:p2"):
            if audit["gates"].get(g, {}).get("status") != "PASS":
                fail(f"EV anchor gate not PASS: {ak} {g}")
    if sorted(registry.get("targets", {})) != sorted(ADOPTED_IDS):
        fail("EV registry target set drift")

    # G3+G4+G5: per-target batch raw + status + gate raw + third-impl + SSOT
    rows = []
    gate_pins = {}
    batch_pins = {}
    third_pins = {}
    third_rows = json.loads((THIRD_KIT / "input/rows.json").read_text())
    third_rows_sha = manifest_sha(third_mans, "thirdimpl", "input/rows.json")
    third_index = {t["key_id"]: t for t in third_rows["targets"]}

    for kid in ADOPTED_IDS:
        k = ADOPTED[kid]
        reg = registry["targets"][kid]
        lo, hi, legal, idx = k[1], k[2], ADOPTED_LEGAL[kid], k[0]
        if int(reg["s5_index"]) != idx or int(reg["lo"]) != lo or int(reg["hi"]) != hi:
            fail(f"EV registry SSOT quadruple drift: {kid}")
        if int(reg["class_index"]) != ADOPTED_CLASS[kid] or int(reg["budget"]) != EV_BUDGET:
            fail(f"EV registry class/budget drift: {kid}")
        if reg.get("result_label") != "WIN":
            fail(f"EV registry label drift: {kid}")
        # -- batch-source: registry pins, re-hashed live
        bsp = reg["batch_source_pins"]
        kit = BATCH_KITS[kid]
        bkeys = kit / "input/batch-keys.json"
        binput = kit / f"input/{kid}.input.csv"
        bp1 = kit / f"output/raw/{kid}.p1.out"
        bp2 = kit / f"output/raw/{kid}.p2.out"
        blog = kit / "output/status.log"
        if sha(bkeys) != bsp["batch_keys_sha256"]:
            fail(f"batch-keys sha drift vs registry pin: {kid}")
        if sha(binput) != bsp["input_sha256"]:
            fail(f"batch input csv sha drift vs registry pin: {kid}")
        if sha(bp1) != bsp["raw_p1_sha256"] or sha(bp2) != bsp["raw_p2_sha256"]:
            fail(f"batch raw sha drift vs registry pins: {kid}")
        if sha(blog) != bsp["status_log_sha256"]:
            fail(f"batch status.log sha drift vs registry pin: {kid}")
        # -- batch-keys SSOT row
        bk = json.loads(bkeys.read_text())
        rec = [e for e in bk["keys"] if e.get("key_id") == kid]
        if len(rec) != 1:
            fail(f"batch-keys SSOT target row missing: {kid}")
        rec = rec[0]
        if (int(rec["s5_index"]), int(rec["lo"]), int(rec["hi"])) != (idx, lo, hi):
            fail(f"batch-keys SSOT quadruple drift: {kid}")
        if int(rec["legal"]) != legal:
            fail(f"batch-keys legal count drift: {kid}")
        if int(rec.get("membership_class_count", -1)) != MEMBERSHIP_CLASS_COUNT[kid]:
            fail(f"batch-keys membership_class_count drift: {kid}")
        # -- input csv body == SSOT quadruple
        want_line = f"target,0,5,{lo},{hi},{legal},0,0,0,0,0"
        body = [l for l in binput.read_text().splitlines() if l.strip()]
        if body != [want_line]:
            fail(f"batch input csv body drift: {kid}: {body}")
        # -- batch raw pair: 15M two-pass fresh-cold node-exact WIN
        b = check_two_pass(bp1, bp2, bsp["raw_p1_sha256"], bsp["raw_p2_sha256"])
        if (b["stones"], b["is_or"], b["budget"]) != (5, 0, EV_BUDGET):
            fail(f"batch raw condition drift: {kid}")
        if (int(b["lo"]), int(b["hi"]), b["legal"]) != (lo, hi, legal):
            fail(f"batch raw key/legal drift vs SSOT: {kid}")
        if b["result"] != 1 or b["nodes"] != ADOPTED_NODES[kid]:
            fail(f"batch raw disposition drift (expected WIN {ADOPTED_NODES[kid]} nodes): {kid}")
        if THIRD_TELEMETRY not in bp1.read_text() or THIRD_TELEMETRY not in bp2.read_text():
            fail(f"batch raw telemetry drift: {kid}")
        # -- status.log: PASS triple + WIN-HALT discipline
        log_lines = blog.read_text().splitlines()
        triple = f"{EV_BUDGET},1,{ADOPTED_NODES[kid]}"
        pass_lines = [l for l in log_lines if f" {kid} PASS {triple}" in l]
        halt_lines = [l for l in log_lines if f"{kid} WIN-HALT" in l]
        if len(pass_lines) != 1 or not halt_lines:
            fail(f"batch status.log PASS/WIN-HALT discipline drift: {kid}")
        win_passes = [l for l in log_lines if " PASS " in l and ",1," in l]
        if win_passes != pass_lines:
            fail(f"batch held a second result-1 row besides the target: {kid}: {win_passes}")
        # -- EV gate raw pair: C++ second implementation, node-exact vs batch
        gp1 = manifest_sha(ev_mans, "ev", f"output/raw/{kid}.p1.out")
        gp2 = manifest_sha(ev_mans, "ev", f"output/raw/{kid}.p2.out")
        g = check_two_pass(EV_KIT / f"output/raw/{kid}.p1.out",
                           EV_KIT / f"output/raw/{kid}.p2.out", gp1, gp2)
        if (g["stones"], g["is_or"], g["budget"]) != (5, 0, EV_BUDGET):
            fail(f"EV gate raw condition drift: {kid}")
        if (int(g["lo"]), int(g["hi"]), g["legal"]) != (lo, hi, legal):
            fail(f"EV gate key/legal drift vs SSOT: {kid}")
        if (g["result"], g["nodes"]) != (b["result"], b["nodes"]):
            fail(f"EV gate != batch raw node-exact: {kid}")
        exp = reg["expected"]
        parts = exp.split(",")
        if (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])) != \
                (legal, EV_BUDGET, g["result"], g["nodes"]):
            fail(f"EV registry expected-quadruple drift: {kid}")
        # -- EV gate input csv triple-clone (batch == gate == registry pin)
        in_pin_ev = manifest_sha(ev_mans, "ev", f"input/{kid}.input.csv")
        if in_pin_ev != reg["input_pin"] or in_pin_ev != bsp["input_sha256"]:
            fail(f"input csv triple-clone pin drift: {kid}")
        # -- audit per-row
        rec2 = audit["rows"].get(kid)
        want = f"{legal},{EV_BUDGET},{g['result']},{g['nodes']}"
        if rec2 is None or rec2.get("budget") != str(EV_BUDGET) or \
                rec2.get("expected") != want or rec2.get("observed_p1") != want:
            fail(f"EV gate audit per-row drift: {kid} {rec2}")
        for gkey in (f"G1:{kid}:p1", f"G1:{kid}:p2"):
            if audit["gates"].get(gkey, {}).get("status") != "PASS":
                fail(f"EV gate audit per-pass gates not PASS: {kid} {gkey}")
        # -- third-impl cross-SSOT: rows.json + a/b target raws
        tr = third_index.get(kid)
        if tr is None:
            fail(f"thirdimpl rows.json target missing: {kid}")
        if (int(tr["lo"]), int(tr["hi"]), int(tr["legal"])) != (lo, hi, legal):
            fail(f"thirdimpl rows.json key drift: {kid}")
        if int(tr["replica_result"]) != 1 or int(tr["replica_nodes"]) != ADOPTED_NODES[kid] \
                or int(tr["expect_third"]) != 1:
            fail(f"thirdimpl rows.json replica quadruple drift: {kid}")
        expansions = {}
        for pass_id in ("a", "b"):
            out_rel = f"output/targets/{kid}.{pass_id}.out"
            out_pin = manifest_sha(third_mans, "thirdimpl", out_rel)
            out_path = THIRD_KIT / out_rel
            if sha(out_path) != out_pin:
                fail(f"thirdimpl target raw sha drift: {kid}.{pass_id}")
            m = THIRD.match(out_path.read_text().strip())
            if not m or m.group(1) != kid or m.group(2) != pass_id:
                fail(f"thirdimpl target raw format drift: {kid}.{pass_id}")
            _, _, stones, legal2, legal3, result, c1, c2, _, tlo, thi, clean, _t = m.groups()
            if (int(stones), int(legal2), int(legal3)) != (5, legal, legal) or \
                    int(result) != 1 or clean != "clean":
                fail(f"thirdimpl target raw condition drift: {kid}.{pass_id}")
            if (int(tlo), int(thi)) != (lo, hi):
                fail(f"thirdimpl target raw key drift: {kid}.{pass_id}")
            expansions[pass_id] = (int(c1), int(c2))
            third_pins[f"{kid}_{pass_id}_sha256"] = out_pin
        if expansions["a"] != expansions["b"]:
            fail(f"thirdimpl a/b expansion-count disagreement: {kid}")
        # -- freshness + quarantine
        if (lo, hi) in base_rows:
            fail(f"adopted key already in BASE (fresh gate): {kid}")
        if (lo, hi) in qkeys:
            fail(f"adopted key quarantined: {kid}")
        gate_pins[kid] = {"input": in_pin_ev, "p1": gp1, "p2": gp2}
        batch_pins[kid] = {"kit": BATCH_KITS[kid].name,
                           "batch_keys_sha256": bsp["batch_keys_sha256"],
                           "input_sha256": bsp["input_sha256"],
                           "status_log_sha256": bsp["status_log_sha256"],
                           "raw_p1_sha256": bsp["raw_p1_sha256"],
                           "raw_p2_sha256": bsp["raw_p2_sha256"],
                           "win_halted_at": pass_lines[0].split()[0],
                           "thirdimpl_rows_json_sha256": third_rows_sha,
                           "thirdimpl_out_a_sha256": third_pins[f"{kid}_a_sha256"],
                           "thirdimpl_out_b_sha256": third_pins[f"{kid}_b_sha256"],
                           "thirdimpl_expansion_counts": list(expansions["a"])}
        rows.append({"key_id": kid, "class": ADOPTED_CLASS[kid],
                     "s5_index": idx, "lo": lo, "hi": hi, "legal": legal,
                     "budget": EV_BUDGET, "nodes": ADOPTED_NODES[kid],
                     "label": "WIN"})

    # G6: adopted set accounting
    if sorted(r["key_id"] for r in rows) != sorted(ADOPTED_IDS):
        fail("adopted set drift")
    adopted_nodes = sum(r["nodes"] for r in rows)
    if adopted_nodes != ADOPTED_NODES_TOTAL:
        fail(f"adopted node total drift: {adopted_nodes}")

    # emission
    adopted = sorted(rows, key=lambda x: (x["lo"], x["hi"]))
    hdr = [
        "# n11 central-reply closure: evwin4 canonical-adoption increment (Part EV, 2026-11-26)",
        "#   The 4 Part EV gate-verified closure-batch WIN rows (b018 class 16757",
        "#   batch-1 dual-class, d002 class 20421 batch-3, e002 class 16371",
        "#   batch-4, f017 class 12264 batch-5; 2026-11-22 batch 15M two-pass",
        "#   fresh-cold node-exact replica raws re-verified live, third-impl",
        "#   verdict-level corroborated (a/b passes, identical expansion",
        "#   counts), C++ second-implementation scrutiny gate 9193f5b6...",
        "#   7/7 GATE-PASS, audit 0327dad8..., 4/4 byte-identical audit",
        "#   re-runs).  The 21 unconsumed closure-batch LOSS rows stay",
        "#   UNCONSUMED (EM-pattern territory); k04 untouched (sixth-cost",
        "#   lane); every other unconsumed probe-level WIN stays in NO cache.",
        "#   Every row is fresh to BASE 3ba48608... and not quarantined; the",
        "#   2 Part-EU adopted rows re-verified WIN in BASE (regression tie).",
        "#   Consuming WIN labels asserts NO root verdict and NO 11x11",
        "#   outcome; scheduling bookkeeping is re-audited fail-closed by",
        "#   the refresh.  11x11 stays UNKNOWN; nodes are bookkeeping.",
    ]
    lines = list(hdr)
    for r in adopted:
        lines.append(f"s5verdict,{r['lo']},{r['hi']},5,1,{r['nodes']}")
    incr_path = OUT / "increment-evwin4-20261126.cache"
    incr_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {
        "schema": "evwin4-increments-manifest-v1",
        "part": "EV",
        "date": "2026-11-26",
        "win_canonical_adoption": True,
        "base_cache_sha256": BASE_CACHE_SHA,
        "base_cache_path": "research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125/output/merged-exact-s5-chain-plus-euwin2-20261125.cache",
        "base_cache_rows": BASE_CACHE_ROWS,
        "merger_sha256": MERGER_SHA,
        "merger_note": "fail-closed union merger byte-clone 90711961...; WIN/LOSS conflict abort; first-occurrence nodes",
        "sha256": {"win_increment": sha(incr_path)},
        "adopted_win_rows": [
            {"key_id": r["key_id"], "class": r["class"], "s5_index": r["s5_index"],
             "lo": r["lo"], "hi": r["hi"], "legal": r["legal"], "budget": r["budget"],
             "result": 1, "nodes": r["nodes"],
             "gate_kit": "ev",
             "gate_input_sha256": gate_pins[r["key_id"]]["input"],
             "gate_raw_p1_sha256": gate_pins[r["key_id"]]["p1"],
             "gate_raw_p2_sha256": gate_pins[r["key_id"]]["p2"],
             "batch_basis": batch_pins[r["key_id"]],
             "expect_third": 1,
             "extra_provenance": None}
            for r in adopted
        ],
        "adopted_ids": sorted(r["key_id"] for r in adopted),
        "targets": sorted(r["key_id"] for r in rows),
        "row_counts": {"adopted_win_rows": len(adopted),
                       "exhausted_honest_unknown_rows": 0,
                       "prior_canonical_rows_base": BASE_CACHE_ROWS,
                       "loss_rows_this_pool": 0},
        "adopted_nodes_per_pool": adopted_nodes,
        "pool_derivation": {
            "selection": "the 4 Part EV gate-verified UNCONSUMED closure-batch WIN rows (b018/d002/e002/f017 from the 2026-11-22 closure batches 1/3/4/5; third-impl corroborated 2026-11-22; C++ scrutiny gate 2026-11-25)",
            "resolution": "batch 15M two-pass fresh-cold node-exact WIN raws re-verified live against the registry pins; EV C++ gate two-pass node-exact vs the batch raws; third-implementation a/b verdict-level corroboration re-verified live; no new solver pass was run by this Part",
            "targets_adopted_here": sorted(r["key_id"] for r in adopted),
            "registry_crosscheck": "the EV registry target quadruples equal the batch-keys SSOT, the batch raws, the gate raws, the rows.json replica quadruples and the ADOPTED table",
        },
        "eu_regression_tie": {
            "eu_increment_sha256": EU_INCREMENT_SHA,
            "adopted_rows_win_in_base": EU_ADOPTED_COUNT,
            "note": "both Part-EU rows re-verified WIN in BASE with identical nodes; NOT re-adopted here; the Part-ER 18-row tie is carried by the Part EU extractor proof against the same chain",
        },
        "verdicts_out_of_scope_unconsumed": {
            "closure_batch_loss_rows": "the 21 unconsumed closure-batch LOSS rows stay UNCONSUMED (EM-pattern loss-adoption territory at its own gate standard)",
            "k04_sixthcost_win": "owned by the sixth-cost lane; NOT adopted",
            "b018_dual_class": "b018 sits in the cost sets of classes 15640/16757/30345 (membership_class_count 3); adoption excludes only scheduling bookkeeping, no per-class verdict",
            "other_closure_wins": "every other unconsumed probe-level WIN row stays in NO cache",
            "no_reprobe": "no batch key was re-searched by this Part at any condition; honest labels of unprobed batch keys stay honest UNKNOWN",
        },
        "provenance": {
            "pin_policy": "no per-file kit sha is hand-typed; all per-row pins are extracted from the byte-verified published kit MANIFESTs and the byte-pinned EV registry SSOT, and re-hashed live at emission",
            "ev_kit_manifest_sha256": EV_MANIFEST_SHA,
            "ev_registry_sha256": EV_REGISTRY_SHA,
            "ev_audit_sha256": EV_AUDIT_SHA,
            "ev_audit_schema": EV_AUDIT_SCHEMA,
            "ev_audit_reruns_byte_identical": 4,
            "ev_gate_source_sha256": EV_GATE_SOURCE_SHA,
            "ev_gate_source_commit": EV_GATE_SOURCE_COMMIT,
            "ev_gate_status_pass": EV_STATUS_PASS,
            "thirdimpl_manifest_sha256": THIRD_MANIFEST_SHA,
            "thirdimpl_rows_json_sha256": third_rows_sha,
            "batch_kit_integrity": "the 4 closure-batch kits re-hashed file-by-file against the registry batch_source_pins (20 files); the batch-keys SSOT quadruples equal the ADOPTED table; each batch's single result-1 row is its target (WIN-HALT discipline); the EV gate kit (36/36) and the thirdimpl kit (96/96) verified file-by-file against their MANIFESTs",
        },
        "quarantine_hits": 0,
        "base_cache_absent_hits_for_emitted": len(adopted),
        "interpretation_guard": "nodes are bookkeeping, never verdicts; consuming a WIN label asserts no root verdict; the standard 11x11 empty board stays UNKNOWN",
    }
    manifest_path = OUT / "increments-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    print(f"EV increment OK: rows={len(adopted)} nodes={adopted_nodes} incr_sha={sha(incr_path)}")
    print(f"manifest sha={sha(manifest_path)}")


if __name__ == "__main__":
    main()
