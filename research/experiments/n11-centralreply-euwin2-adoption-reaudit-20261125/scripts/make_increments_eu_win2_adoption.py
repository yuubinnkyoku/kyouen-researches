#!/usr/bin/env python3
"""Part EU maker: euwin2 canonical-adoption increment (2026-11-25).

Fork of the published Part ER maker
`make_increments_er_win18_adoption.py` (sha256 39f6c86a...; structural
clone, disclosed diff: the adopted-rows table, the referenced kits, the
resolution condition and the per-row gate set are Part-EU specific).
PIN POLICY unchanged: no per-file sha of any kit member is hand-typed in
this script - every per-row pin is extracted from the byte-verified
published kit MANIFESTs and re-hashed live (fail-closed; rc=1 on ANY
drift).

(a) SOURCE-RAW provenance: the published Part ES re-probe-6 kit
    (closure-class30345-reprobe30m-20261125): the 30M two-pass
    fresh-cold node-exact raw pairs that resolved the 6 batch-38
    honest-EXHAUSTED keys at the DIFFERENT 30M condition (the 15M
    same-condition re-probe ban untouched; the 15M b38 raws stay
    honest-EXHAUSTED and are only used as the selection basis).
(b) GATE provenance: the published Part ET C++ second-implementation
    scrutiny gate kit (closure-class30345-es6-cppgate-20261125):
    9/9 GATE-PASS (6 targets + 3 anchors), audit 2c6d7441..., gate
    source pin 9193f5b6... at 154f3b7a (registered in gate-rows-et.json
    and re-checked here), audit re-run 4/4 byte-identical in-kit.
(c) SSOT: batch-keys-b38.json (29807104...) - per-key (lo, hi, legal,
    s5_index, serving_class=30345) quadruples; the maker re-derives
    the 6-key honest-EXHAUSTED selection from the published b38 raws
    (result 0, nodes == 15M budget, two-pass fresh-cold node-exact at
    15M) and the 30M WIN disposition from the ES raws, failing closed
    on any deviation.
(d) FRESHNESS: every adopted (lo,hi) is absent from the canonical BASE
    (the Part ER head 9c4dd94e..., 6,765 rows WIN 186 / LOSS 6,579)
    and from the quarantine registry 81d23160...; the ER regression tie
    re-checks that all 18 Part-ER adopted rows already sit WIN in the
    BASE cache (they must NOT be re-adopted here).

Adopted here: exactly the 2 ES-30M-resolved WIN rows ai007 (nodes
16,090,493) and ai040 (nodes 20,711,023); adopted node total 36,801,516.
No verdict beyond these 2 adopted WIN rows is consumed anywhere; the
standard 11x11 empty board stays UNKNOWN; nodes are bookkeeping.
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

ER_KIT = ROOT / "research/experiments/n11-centralreply-erwin18-adoption-reaudit-20261125"
ES_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-reprobe30m-20261125"
ET_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-es6-cppgate-20261125"
B38_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-batch38-20261125"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
ER_INCREMENT = ER_KIT / "output/increment-erwin18-20261125.cache"
ER_MANIFEST = ER_KIT / "output/increments-manifest.json"

MERGER = EXP / "scripts/s5_union_merge.py"

# ---------------- top-level pins (published bytes are the authority) ------
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA = "9c4dd94e61b6ee724a966ecc9552e527ba5a7107de732f0e9c5ced33bdad4a5a"
BASE_CACHE_ROWS = 6765
BASE_CACHE_WIN = 186
BASE_CACHE_LOSS = 6579
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
ER_INCREMENT_SHA = "4f6b7797df3bb950703f95e7ec72f288a447434da5b4ccf3d6d94ee8d8d6ffc1"
ER_MANIFEST_SHA = "48b71d6af77306a94bd561f625838cff70cd94f12d702bcda0e945b67237450a"
ER_ADOPTED_COUNT = 18

ES_MANIFEST_SHA = "cc9877399ab18dddad1250a359d13d834849aceb4ff6d54612a79bf72a615819"
ET_MANIFEST_SHA = "f0c1c27a830448dca3cd9c17cfb0f225293bc19f402e7c16710bd32572b449c8"
ET_REGISTRY_SHA = "6cf057ba2320a9d7be55e53edd9be2b65e41f552af206010899793a5b6a659c5"
ET_AUDIT_SHA = "2c6d7441d6f752f160efbe7e275b807ff174d8cd70ece3c85aed135ead11c0d0"
ET_AUDIT_SCHEMA = "n11-centralreply-cppgate-30345es6-audit-v1"
ET_STATUS_PASS = 9
ET_GATE_SOURCE_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
ET_BUDGET = 30000000
ET_KEYS = 6

B38_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"
B38_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
B38_BUDGET = 15000000
B38_KEYS_TOTAL = 49
EXPECTED_POOL = ["ai007", "ai024", "ai030", "ai038", "ai040", "ai041"]
EXPECTED_ADOPTED = ["ai007", "ai040"]
EXPECTED_ADOPTED_NODES = 36801516
EXPECTED_NODES = {"ai007": 16090493, "ai040": 20711023}

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def fail(msg):
    print(f"ABORT eu-max: {msg}", file=sys.stderr)
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


def verify_kit(kit: Path, man_sha: str, tag: str) -> dict:
    man = kit / "MANIFEST-sha256.txt"
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
    # G0: merger byte-clone + BASE identity + quarantine + ER regression basis
    if sha(MERGER) != MERGER_SHA:
        fail("union merger byte-clone sha drift (expected 90711961...)")
    base_cache = ER_KIT / "output/merged-exact-s5-chain-plus-erwin18-20261125.cache"
    if sha(base_cache) != BASE_CACHE_SHA:
        fail("BASE cache sha drift (expected 9c4dd94e...)")
    if sha(QUARANTINE) != QUARANTINE_SHA:
        fail("quarantine registry sha drift")
    if sha(ER_INCREMENT) != ER_INCREMENT_SHA:
        fail("ER increment sha drift (expected 4f6b7797...)")
    if sha(ER_MANIFEST) != ER_MANIFEST_SHA:
        fail("ER increments-manifest sha drift (expected 48b71d6a...)")

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

    # ER regression tie: all 18 ER-adopted rows sit WIN in BASE, not re-adopted here
    er_inc = {}
    for ln in ER_INCREMENT.read_text(encoding="utf-8-sig").splitlines():
        if ln.startswith("s5verdict,"):
            p = ln.split(",")
            er_inc[(int(p[1]), int(p[2]))] = (int(p[4]), int(p[5]))
    if len(er_inc) != ER_ADOPTED_COUNT:
        fail(f"ER increment row count drift: {len(er_inc)}")
    for pair, (verdict, nodes) in er_inc.items():
        if pair not in base_rows or base_rows[pair][0] != 1 or verdict != 1:
            fail(f"ER regression tie broken: {pair} not WIN in BASE")
        if base_rows[pair][1] != nodes:
            fail(f"ER regression nodes tie broken: {pair}")

    quarantined = json.loads(QUARANTINE.read_text())
    qkeys = set()
    for entry in quarantined if isinstance(quarantined, list) else quarantined.get("keys", []):
        if isinstance(entry, dict) and "lo" in entry:
            qkeys.add((int(entry["lo"]), int(entry["hi"])))

    # G1: whole-kit file-by-file integrity of the three referenced published kits
    es_mans = verify_kit(ES_KIT, ES_MANIFEST_SHA, "es")
    et_mans = verify_kit(ET_KIT, ET_MANIFEST_SHA, "et")
    b38_mans = verify_kit(B38_KIT, B38_MANIFEST_SHA, "b38")

    # G2: ET gate-kit machine audit + status honesty + audit determinism
    if sha(ET_KIT / "output/audit_gate.json") != ET_AUDIT_SHA:
        fail("ET gate-kit machine audit sha drift")
    audit = json.loads((ET_KIT / "output/audit_gate.json").read_text())
    if audit.get("overall") != "PASS" or audit.get("part") != "ET" or \
            audit.get("schema") != ET_AUDIT_SCHEMA:
        fail("ET gate-kit audit honesty drift")
    for rn in ("run1", "run2", "run3"):
        if sha(ET_KIT / f"output/audit_gate.{rn}.json") != ET_AUDIT_SHA:
            fail(f"ET audit re-run determinism drift ({rn})")
    if sha(ET_KIT / "input/gate-rows-et.json") != ET_REGISTRY_SHA:
        fail("ET registry sha drift (expected 6cf057ba...)")
    registry = json.loads((ET_KIT / "input/gate-rows-et.json").read_text())
    if registry.get("schema") != "n11-centralreply-cppgate-30345es6-rows-v1":
        fail("ET registry schema drift")
    gs = registry.get("gate_source", {})
    if gs.get("sha256") != ET_GATE_SOURCE_SHA or not gs.get("commit", "").startswith("154f3b7a"):
        fail("ET registry gate-source pin drift")
    bad_gates = [k for k, v in audit["gates"].items() if v.get("status") != "PASS"]
    if bad_gates:
        fail(f"ET audit has non-PASS gates: {bad_gates[:4]}")
    if audit["gates"].get("G4", {}).get("detail") != "passes=9/9 bad=0":
        fail("ET audit G4 aggregate drift")
    ok = 0
    bad = []
    for line in (ET_KIT / "output/gate-status.log").read_text().splitlines():
        if " GATE-PASS " in line:
            ok += 1
        elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line or "TRUNCATED" in line:
            bad.append(line)
    if ok != ET_STATUS_PASS or bad:
        fail(f"ET gate-status accounting drift: ok {ok} bad {bad}")
    # anchor calibration rows (3) present and PASS in the audit
    anchors_expected = {"anchor-at2m": "98,2000000,0,2000000",
                        "anchor-af039": "89,30000000,2,19234232",
                        "anchor-aj001": "84,30000000,2,5156075"}
    reg_anchors = registry.get("anchors", {})
    if reg_anchors != anchors_expected:
        fail("ET registry anchor table drift")
    for ak, aexp in anchors_expected.items():
        rec = audit["rows"].get(ak)
        if rec is None or rec.get("expected") != aexp or rec.get("observed_p1") != aexp:
            fail(f"ET anchor row drift: {ak} {rec}")
        for g in (f"G1:{ak}:p1", f"G1:{ak}:p2"):
            if audit["gates"].get(g, {}).get("status") != "PASS":
                fail(f"ET anchor gate not PASS: {ak} {g}")

    # G3: SSOT + honest-EXHAUSTED selection re-derivation from the b38 raws
    if sha(B38_KIT / "input/batch-keys-b38.json") != B38_KEYS_SHA:
        fail("b38 batch-keys SSOT sha drift (expected 29807104...)")
    ssot = json.loads((B38_KIT / "input/batch-keys-b38.json").read_text())
    keys = ssot["keys"]
    if len(keys) != B38_KEYS_TOTAL:
        fail(f"b38 SSOT key count drift: {len(keys)}")
    ssot_by_id = {}
    for k in keys:
        if k.get("serving_class") != 30345:
            fail(f"b38 SSOT serving_class drift for {k.get('key_id')}")
        ssot_by_id[k["key_id"]] = k

    exhausted = []
    for kid in sorted(ssot_by_id):
        p1 = B38_KIT / f"output/raw/{kid}.p1.out"
        p2 = B38_KIT / f"output/raw/{kid}.p2.out"
        pin1 = manifest_sha(b38_mans, "b38", f"output/raw/{kid}.p1.out")
        pin2 = manifest_sha(b38_mans, "b38", f"output/raw/{kid}.p2.out")
        r = check_two_pass(p1, p2, pin1, pin2)
        if (r["stones"], r["is_or"], r["budget"]) != (5, 0, B38_BUDGET):
            fail(f"b38 raw condition drift: {kid}")
        lo, hi = int(ssot_by_id[kid]["lo"]), int(ssot_by_id[kid]["hi"])
        if (int(r["lo"]), int(r["hi"])) != (lo, hi):
            fail(f"b38 raw key drift vs SSOT: {kid}")
        if r["result"] == 0 and r["nodes"] == B38_BUDGET:
            exhausted.append(kid)
        elif r["result"] not in (1, 2):
            fail(f"b38 raw unclassifiable disposition: {kid}")
    if sorted(exhausted) != EXPECTED_POOL:
        fail(f"b38 honest-EXHAUSTED pool drift: {sorted(exhausted)}")
    reg_targets = sorted(registry.get("targets", {}))
    if reg_targets != EXPECTED_POOL:
        fail(f"ET registry target pool != re-derived honest-EXHAUSTED pool: {reg_targets}")

    # G4: per-row source (ES 30M) + gate (ET C++) provenance, node-exact across
    rows = []
    gate_pins = {}
    src_pins = {}
    b38_basis_pins = {}
    input_pins = {}
    es_nodes = {}
    for kid in EXPECTED_POOL:
        k = ssot_by_id[kid]
        lo, hi, legal = int(k["lo"]), int(k["hi"]), int(k["legal"])
        reg = registry["targets"][kid]
        if int(reg["s5_index"]) != int(k["s5_index"]) or int(reg["serving_class"]) != 30345:
            fail(f"ET registry SSOT quadruple drift: {kid}")
        if int(reg["budget"]) != ET_BUDGET:
            fail(f"ET registry budget drift: {kid}")
        # input csv triple clone: ES pin == ET pin == b38 pin, body == SSOT quadruple
        in_pin_es = manifest_sha(es_mans, "es", f"input/{kid}.input.csv")
        in_pin_et = manifest_sha(et_mans, "et", f"input/{kid}.input.csv")
        in_pin_b38 = manifest_sha(b38_mans, "b38", f"input/{kid}.input.csv")
        if not (in_pin_es == in_pin_et == in_pin_b38 == reg["input_pin"]):
            fail(f"input triple-clone pin drift: {kid}")
        want_line = f"target,0,5,{lo},{hi},{legal},0,0,0,0,0"
        body = [l for l in (ES_KIT / f"input/{kid}.input.csv").read_text().splitlines() if l.strip()]
        if body != [want_line]:
            fail(f"input csv body drift: {kid}: {body}")
        # ES source raw pair (30M two-pass fresh-cold)
        sp1 = manifest_sha(es_mans, "es", f"output/raw/{kid}.p1.out")
        sp2 = manifest_sha(es_mans, "es", f"output/raw/{kid}.p2.out")
        s = check_two_pass(ES_KIT / f"output/raw/{kid}.p1.out",
                           ES_KIT / f"output/raw/{kid}.p2.out", sp1, sp2)
        if (s["stones"], s["is_or"], s["budget"]) != (5, 0, ET_BUDGET):
            fail(f"ES raw condition drift (30M): {kid}")
        if (int(s["lo"]), int(s["hi"])) != (lo, hi) or s["legal"] != legal:
            fail(f"ES raw key/legal drift vs SSOT: {kid}")
        es_nodes[kid] = (s["result"], s["nodes"])
        # b38 15M honest-EXHAUSTED basis pair re-verified live (selection basis)
        bp1 = manifest_sha(b38_mans, "b38", f"output/raw/{kid}.p1.out")
        bp2 = manifest_sha(b38_mans, "b38", f"output/raw/{kid}.p2.out")
        b = check_two_pass(B38_KIT / f"output/raw/{kid}.p1.out",
                           B38_KIT / f"output/raw/{kid}.p2.out", bp1, bp2)
        if (b["result"], b["nodes"], b["budget"]) != (0, B38_BUDGET, B38_BUDGET):
            fail(f"b38 honest-EXHAUSTED basis drift: {kid}")
        # ET gate raw pair (C++ second implementation, 30M two-pass fresh-cold)
        gp1 = manifest_sha(et_mans, "et", f"output/raw/{kid}.p1.out")
        gp2 = manifest_sha(et_mans, "et", f"output/raw/{kid}.p2.out")
        g = check_two_pass(ET_KIT / f"output/raw/{kid}.p1.out",
                           ET_KIT / f"output/raw/{kid}.p2.out", gp1, gp2)
        if (g["stones"], g["is_or"], g["budget"]) != (5, 0, ET_BUDGET):
            fail(f"ET gate raw condition drift: {kid}")
        if (int(g["lo"]), int(g["hi"]), g["legal"]) != (lo, hi, legal):
            fail(f"ET gate key/legal drift vs SSOT: {kid}")
        if (g["result"], g["nodes"]) != (s["result"], s["nodes"]):
            fail(f"ET gate != ES source node-exact: {kid}")
        # registry quadruple + label agreement
        exp = reg["expected"]
        parts = exp.split(",")
        if (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])) != (legal, ET_BUDGET, s["result"], s["nodes"]):
            fail(f"ET registry expected-quadruple drift: {kid}")
        label = "WIN" if s["result"] == 1 else ("LOSS" if s["result"] == 2 else "?")
        if reg["result_label"] != label:
            fail(f"ET registry label drift: {kid}")
        # audit per-key
        rec = audit["rows"].get(kid)
        want = f"{legal},{ET_BUDGET},{s['result']},{s['nodes']}"
        if rec is None or rec.get("budget") != str(ET_BUDGET) or \
                rec.get("expected") != want or rec.get("observed_p1") != want:
            fail(f"ET gate audit per-row drift: {kid} {rec}")
        for gkey in (f"G1:{kid}:p1", f"G1:{kid}:p2"):
            if audit["gates"].get(gkey, {}).get("status") != "PASS":
                fail(f"ET gate audit per-pass gates not PASS: {kid} {gkey}")
        # freshness + quarantine
        if (lo, hi) in base_rows:
            fail(f"adopted key already in BASE (fresh gate): {kid}")
        if (lo, hi) in qkeys:
            fail(f"adopted key quarantined: {kid}")
        gate_pins[kid] = {"input": in_pin_et, "p1": gp1, "p2": gp2}
        src_pins[kid] = {"input": in_pin_es, "p1": sp1, "p2": sp2}
        b38_basis_pins[kid] = {"p1": bp1, "p2": bp2}
        input_pins[kid] = in_pin_es
        rows.append({"key_id": kid, "class": 30345, "s5_index": int(k["s5_index"]),
                     "lo": lo, "hi": hi, "legal": legal,
                     "budget": ET_BUDGET, "nodes": s["nodes"], "label": label})

    # G5: adopted set = the ES-30M raw-derived WIN disposition of the pool, exactly
    derived_win = sorted(r["key_id"] for r in rows if r["label"] == "WIN")
    derived_loss = sorted(r["key_id"] for r in rows if r["label"] == "LOSS")
    if derived_win != EXPECTED_ADOPTED:
        fail(f"ES 30M WIN disposition drift: {derived_win}")
    if derived_loss != ["ai024", "ai030", "ai038", "ai041"]:
        fail(f"ES 30M LOSS disposition drift: {derived_loss}")
    adopted_nodes = sum(EXPECTED_NODES[k] for k in derived_win)
    for r in rows:
        if r["key_id"] in EXPECTED_NODES and r["nodes"] != EXPECTED_NODES[r["key_id"]]:
            fail(f"adopted node count drift: {r['key_id']}")
    if adopted_nodes != EXPECTED_ADOPTED_NODES:
        fail(f"adopted node total drift: {adopted_nodes}")

    # emission
    adopted = sorted((r for r in rows if r["label"] == "WIN"), key=lambda x: (x["lo"], x["hi"]))
    hdr = [
        "# n11 central-reply closure: euwin2 canonical-adoption increment (Part EU, 2026-11-25)",
        "#   The 2 scrutinized closure-class-30345 WIN rows resolved by the Part ES",
        "#   exhausted-6 re-probe at the DIFFERENT 30M condition (ai007 + ai040;",
        "#   b38 15M honest-EXHAUSTED selection, ES 30M two-pass fresh-cold node-exact",
        "#   resolution, the Part ET C++ second-implementation gate 9193f5b6...",
        "#   9/9 GATE-PASS, audit 2c6d7441..., re-run 4/4 byte-identical).",
        "#   The 4 ES-30M-resolved LOSS rows stay UNCONSUMED (EM-pattern territory);",
        "#   b018 untouched (dual-class, scrutiny-owner pending); the same-condition",
        "#   15M re-probe ban untouched.  Every row is fresh to BASE 9c4dd94e... and",
        "#   not quarantined; all 18 Part-ER adopted rows re-verified WIN in BASE.",
        "#   Consuming WIN labels asserts NO root verdict and NO 11x11 outcome;",
        "#   scheduling bookkeeping is re-audited fail-closed by the refresh.",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping.",
    ]
    lines = list(hdr)
    for r in adopted:
        lines.append(f"s5verdict,{r['lo']},{r['hi']},5,1,{r['nodes']}")
    incr_path = OUT / "increment-euwin2-20261125.cache"
    incr_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {
        "schema": "euwin2-increments-manifest-v1",
        "part": "EU",
        "date": "2026-11-25",
        "win_canonical_adoption": True,
        "base_cache_sha256": BASE_CACHE_SHA,
        "base_cache_path": "research/experiments/n11-centralreply-erwin18-adoption-reaudit-20261125/output/merged-exact-s5-chain-plus-erwin18-20261125.cache",
        "base_cache_rows": BASE_CACHE_ROWS,
        "merger_sha256": MERGER_SHA,
        "merger_note": "fail-closed union merger byte-clone 90711961...; WIN/LOSS conflict abort; first-occurrence nodes",
        "sha256": {"win_increment": sha(incr_path)},
        "adopted_win_rows": [
            {"key_id": r["key_id"], "class": r["class"], "s5_index": r["s5_index"],
             "lo": r["lo"], "hi": r["hi"], "legal": r["legal"], "budget": r["budget"],
             "result": 1, "nodes": r["nodes"],
             "gate_kit": "et",
             "gate_input_sha256": gate_pins[r["key_id"]]["input"],
             "gate_raw_p1_sha256": gate_pins[r["key_id"]]["p1"],
             "gate_raw_p2_sha256": gate_pins[r["key_id"]]["p2"],
             "source_kit": "es", "source_dir": "output/raw",
             "source_input_sha256": input_pins[r["key_id"]],
             "source_raw_p1_sha256": src_pins[r["key_id"]]["p1"],
             "source_raw_p2_sha256": src_pins[r["key_id"]]["p2"],
             "b38_basis": {"kit": "b38", "condition_budget": B38_BUDGET,
                           "honest_disposition": "EXHAUSTED (honest UNKNOWN, never re-probed at 15M)",
                           "raw_p1_sha256": b38_basis_pins[r["key_id"]]["p1"],
                           "raw_p2_sha256": b38_basis_pins[r["key_id"]]["p2"]},
             "extra_provenance": None}
            for r in adopted
        ],
        "adopted_ids": sorted(r["key_id"] for r in adopted),
        "resolved_ids": sorted(r["key_id"] for r in rows),
        "row_counts": {"adopted_win_rows": len(adopted),
                       "exhausted_honest_unknown_rows": 0,
                       "prior_canonical_rows_base": BASE_CACHE_ROWS,
                       "loss_rows_this_pool": 4},
        "adopted_nodes_per_pool": adopted_nodes,
        "pool_derivation": {
            "selection": "the 6 batch-38 honest-EXHAUSTED keys of closure class 30345, re-derived from the published b38 raws (15M result==nodes==budget, two-pass fresh-cold node-exact)",
            "resolution": "Part ES 30M re-probe (two-pass fresh-cold node-exact raws), the DIFFERENT condition; same-condition ban untouched",
            "win_derived": derived_win,
            "loss_derived": derived_loss,
            "targets_adopted_here": sorted(r["key_id"] for r in adopted),
            "registry_crosscheck": "the ET registry target pool (gate-rows-et.json) equals the re-derived pool; the ET G4 audit aggregated 9/9 PASS",
        },
        "er_regression_tie": {"er_increment_sha256": ER_INCREMENT_SHA,
                               "er_manifest_sha256": ER_MANIFEST_SHA,
                               "adopted_rows_win_in_base": ER_ADOPTED_COUNT,
                               "note": "all 18 Part-ER rows re-verified WIN in BASE with identical nodes; NOT re-adopted here"},
        "verdicts_out_of_scope_unconsumed": {
            "es6_30m_resolved_loss_rows": "ai024/ai030/ai038/ai041 resolved LOSS at the 30M condition, unconsumed here (EM-pattern loss-adoption territory at its own gate standard)",
            "b38_15m_exhausted_labels": "the 15M honest-EXHAUSTED label of every pool key remains honest UNKNOWN at 15M; nothing overwrote it",
            "b018": "batch-1 dual-class probe-level WIN, scrutiny-owner pending, same-condition re-probe prohibited - consumed nowhere",
            "k04_sixthcost_win": "owned by the sixth-cost lane; NOT adopted",
            "other_closure_wins": "every other unconsumed probe-level WIN row stays in NO cache",
        },
        "provenance": {
            "pin_policy": "no per-file kit sha is hand-typed; all per-row pins are extracted from the byte-verified published kit MANIFESTs and re-hashed live at emission",
            "es_kit_manifest_sha256": ES_MANIFEST_SHA,
            "et_kit_manifest_sha256": ET_MANIFEST_SHA,
            "et_registry_sha256": ET_REGISTRY_SHA,
            "et_audit_sha256": ET_AUDIT_SHA,
            "et_audit_schema": ET_AUDIT_SCHEMA,
            "et_audit_reruns_byte_identical": 3,
            "et_gate_source_sha256": ET_GATE_SOURCE_SHA,
            "et_gate_source_commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
            "et_gate_status_pass": ET_STATUS_PASS,
            "b38_manifest_sha256": B38_MANIFEST_SHA,
            "b38_keys_sha256": B38_KEYS_SHA,
            "kit_integrity": "all three referenced kits (es/et/b38) verified file-by-file against their pinned MANIFESTs (38 + 38 + 181 entries)",
        },
        "quarantine_hits": 0,
        "base_cache_absent_hits_for_emitted": len(adopted),
        "interpretation_guard": "nodes are bookkeeping, never verdicts; consuming a WIN label asserts no root verdict; the standard 11x11 empty board stays UNKNOWN",
    }
    manifest_path = OUT / "increments-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    print(f"EU increment OK: rows={len(adopted)} nodes={adopted_nodes} incr_sha={sha(incr_path)}")
    print(f"manifest sha={sha(manifest_path)}")


if __name__ == "__main__":
    main()
