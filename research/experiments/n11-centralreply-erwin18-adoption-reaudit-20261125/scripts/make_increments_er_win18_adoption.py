#!/usr/bin/env python3
"""Part ER maker: erwin18 canonical-adoption increment (2026-11-25).

Fork of the published Part EP maker
`make_increments_ep_win10_adoption.py` (sha256 efc40a0b...; structural
clone, disclosed diff: the adopted-rows table, the referenced kits, and
the per-row gate set are Part-ER specific).  PIN POLICY unchanged: no
per-file sha of any kit member is hand-typed in this script - every
per-row pin is extracted from the byte-verified published kit MANIFESTs
and re-hashed live (fail-closed; rc=1 on ANY drift).

(a) SOURCE-RAW provenance: the published batch-38 original drive pairs
    in the Part EF b38 kit output/raw (two-pass fresh-cold node-exact at
    the single 15M condition; the WIN label of every adopted row).
(b) GATE provenance: the published Part EQ C++ second-implementation
    scrutiny gate kit (closure-class30345-cppgate-20261125): 21/21
    GATE-PASS (18 targets + 3 anchors), audit c2ff2232..., gate source
    pin 9193f5b6... at 154f3b7a (the same gate revision as EN/EO/EP);
    the gate kit's input csvs are byte-clones of the b38 kit pins.
(c) SSOT: batch-keys-b38.json (29807104...) - per-key (lo, hi, legal,
    s5_index, serving_class=30345) quadruples; the maker re-derives the
    whole 49-key batch disposition from the published b38 raws (24 LOSS /
    6 honest-EXHAUSTED / 19 WIN) and the target pool as (WIN minus the
    EP-consumed ai048), failing closed on any deviation.
(d) FRESHNESS: every adopted (lo,hi) is absent from the canonical BASE
    (the Part EP head fd29a337..., 6,747 rows WIN 168 / LOSS 6,579) and
    from the quarantine registry 81d23160....

Honest pre-disclosed item: the Part EQ declaration prose total
"136,539,338" is a 65,000 mis-sum; the per-row registry/audit/raws all
agree on single-pass node total 136,604,338 (verified per row below).
No verdict beyond the 18 adopted WIN rows is consumed anywhere; the
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

EP_KIT = ROOT / "research/experiments/n11-centralreply-epwin10-adoption-reaudit-20261125"
EQ_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-cppgate-20261125"
B38_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-batch38-20261125"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
EP_INCREMENT = EP_KIT / "output/increment-epwin10-20261125.cache"

MERGER = EXP / "scripts/s5_union_merge.py"

# ---------------- top-level pins (published bytes are the authority) ------
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA = "fd29a33726e2e083998c67d83bf90822f84beebac30728ea79ea713e880cd1af"
BASE_CACHE_ROWS = 6747
BASE_CACHE_WIN = 168
BASE_CACHE_LOSS = 6579
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
EP_INCREMENT_SHA = "c245bc4c63fdd116f5d707736a4b06925c7e0c48df92993a21363a910e7de1f2"
EP_CONSUMED_KEY = "ai048"
EP_CONSUMED_NODES = 2232854

EQ_MANIFEST_SHA = "786315f35e73cc322f0746c68e5cb7d93369628933e46d45ff77f4f247cd304d"
EQ_AUDIT_SHA = "c2ff2232271d87459fd6954b5076e3a6462c849a15cd891fe51f343c931f0174"
EQ_REGISTRY_SHA = "85736edf3a1b049afc3476c7cb78d1980415888a42c10037e632d393c79cb09c"
EQ_AUDIT_SCHEMA = "n11-centralreply-cppgate-30345win18-audit-v1"
EQ_STATUS_PASS = 21
EQ_GATE_SOURCE_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
EQ_REGISTRY_BUDGET = 15000000

B38_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"
B38_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
B38_BUDGET = 15000000
B38_KEYS_TOTAL = 49
EXPECTED_DISPOSITION = {"WIN": 19, "LOSS": 24, "EXHAUSTED": 6}
EXPECTED_ADOPTED = 18
EXPECTED_ADOPTED_NODES = 136604338  # EQ declaration prose says 136539338 (mis-sum, disclosed)

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def fail(msg):
    print(f"ABORT er-max: {msg}", file=sys.stderr)
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
    for line in path.read_text().splitlines():
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
        if rec["blob_sha1"] is not None:
            data = p.read_bytes()
            h = hashlib.sha1()
            h.update(b"blob %d\0" % len(data))
            h.update(data)
            if h.hexdigest() != rec["blob_sha1"]:
                fail(f"kit git-blob sha1 drift ({tag}): {rel}")
    return entries


def manifest_sha(entries: dict, kit_tag: str, rel: str) -> str:
    if rel not in entries:
        fail(f"pin absent from {kit_tag} MANIFEST: {rel}")
    return entries[rel]["sha256"]


def classify(result: int, nodes: int) -> str:
    if result == 1:
        return "WIN"
    if result == 2:
        return "LOSS"
    if result == 0 and nodes == B38_BUDGET:
        return "EXHAUSTED"
    fail(f"unclassifiable published raw disposition (result {result}, nodes {nodes})")


def main() -> None:
    # G0: merger byte-clone + BASE identity + quarantine pin
    if sha(MERGER) != MERGER_SHA:
        fail("union merger byte-clone sha drift (expected 90711961...)")
    base_cache = EP_KIT / "output/merged-exact-s5-chain-plus-epwin10-20261125.cache"
    if sha(base_cache) != BASE_CACHE_SHA:
        fail("BASE cache sha drift (expected fd29a337...)")
    if sha(QUARANTINE) != QUARANTINE_SHA:
        fail("quarantine registry sha drift")
    if sha(EP_INCREMENT) != EP_INCREMENT_SHA:
        fail("EP increment sha drift (expected c245bc4c...)")

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

    quarantined = json.loads(QUARANTINE.read_text())
    qkeys = set()
    for entry in quarantined if isinstance(quarantined, list) else quarantined.get("keys", []):
        if isinstance(entry, dict) and "lo" in entry:
            qkeys.add((int(entry["lo"]), int(entry["hi"])))

    # G1: whole-kit file-by-file integrity of both referenced published kits
    eq_mans = verify_kit(EQ_KIT, EQ_MANIFEST_SHA, "eq")
    b38_mans = verify_kit(B38_KIT, B38_MANIFEST_SHA, "b38")

    # G2: EQ gate-kit machine audit + status honesty
    if sha(EQ_KIT / "output/audit_gate.json") != EQ_AUDIT_SHA:
        fail("EQ gate-kit machine audit sha drift")
    audit = json.loads((EQ_KIT / "output/audit_gate.json").read_text())
    if audit.get("overall") != "PASS" or audit.get("part") != "EQ" or \
            audit.get("schema") != EQ_AUDIT_SCHEMA:
        fail("EQ gate-kit audit honesty drift")
    if sha(EQ_KIT / "input/gate-rows-eq.json") != EQ_REGISTRY_SHA:
        fail("EQ registry sha drift (expected 85736edf...)")
    registry = json.loads((EQ_KIT / "input/gate-rows-eq.json").read_text())
    if registry.get("gate_source", {}).get("sha256", "").startswith("9193f5b6") is False or \
            registry["gate_source"]["sha256"] != EQ_GATE_SOURCE_SHA:
        fail("EQ registry gate-source pin drift")
    bad_gates = [k for k, v in audit["gates"].items() if v.get("status") != "PASS"]
    if bad_gates:
        fail(f"EQ audit has non-PASS gates: {bad_gates[:4]}")
    ok = 0
    bad = []
    for line in (EQ_KIT / "output/gate-status.log").read_text().splitlines():
        if " GATE-PASS " in line:
            ok += 1
        elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
            bad.append(line)
    if ok != EQ_STATUS_PASS or bad:
        fail(f"EQ gate-status accounting drift: ok {ok} bad {bad}")
    # anchor calibration rows (3) present and PASS in the audit rows
    anchors_expected = {"anchor-at2m": "98,2000000,0,2000000",
                        "anchor-af039": "89,30000000,2,19234232",
                        "anchor-aj001": "84,30000000,2,5156075"}
    for ak, aexp in anchors_expected.items():
        rec = audit["rows"].get(ak)
        if rec is None or rec.get("expected") != aexp or rec.get("observed_p1") != aexp:
            fail(f"EQ anchor row drift: {ak} {rec}")
        for g in (f"G1:{ak}:p1", f"G1:{ak}:p2"):
            if audit["gates"].get(g, {}).get("status") != "PASS":
                fail(f"EQ anchor gate not PASS: {ak} {g}")

    # G3: SSOT + published-batch disposition + target-pool derivation
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

    disposition = {"WIN": [], "LOSS": [], "EXHAUSTED": []}
    published_disp = {}
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
        if r["legal"] != int(ssot_by_id[kid]["legal"]):
            fail(f"b38 raw legal drift vs SSOT: {kid}")
        d = classify(r["result"], r["nodes"])
        disposition[d].append(kid)
        published_disp[kid] = d
    for d, n in EXPECTED_DISPOSITION.items():
        if len(disposition[d]) != n:
            fail(f"b38 published disposition drift for {d}: {len(disposition[d])} != {n}")

    # target pool = WIN minus the EP-consumed ai048 (exactly the EQ registry)
    ep_inc_rows = [ln for ln in EP_INCREMENT.read_text().splitlines()
                   if ln.startswith("s5verdict,")]
    ep_inc = {}
    for ln in ep_inc_rows:
        p = ln.split(",")
        ep_inc[(int(p[1]), int(p[2]))] = (int(p[4]), int(p[5]))
    epk = ssot_by_id[EP_CONSUMED_KEY]
    epk_pair = (int(epk["lo"]), int(epk["hi"]))
    if epk_pair not in ep_inc or ep_inc[epk_pair] != (1, EP_CONSUMED_NODES):
        fail("EP increment does not contain the consumed ai048 WIN quadruple")
    if epk_pair not in base_rows or base_rows[epk_pair][0] != 1:
        fail("BASE cache does not hold the EP-consumed ai048 WIN row")
    targets = [k for k in disposition["WIN"] if (int(ssot_by_id[k]["lo"]), int(ssot_by_id[k]["hi"])) not in ep_inc]
    if len(targets) != EXPECTED_ADOPTED:
        fail(f"derived target pool drift: {len(targets)}")
    reg_targets = sorted(registry["targets"])
    if sorted(targets) != reg_targets:
        fail("derived target pool != EQ registry targets")

    # G4: per-row gate + source provenance (EQ gate pair = b38 source pair,
    # two-pass fresh-cold node-exact, audit per-key PASS)
    rows = []
    gate_pins = {}
    src_pins = {}
    adopted_nodes = 0
    for kid in targets:
        k = ssot_by_id[kid]
        lo, hi, legal = int(k["lo"]), int(k["hi"]), int(k["legal"])
        # gate input csv clone: EQ pin == b38 pin, body == the SSOT quadruple
        in_pin_eq = manifest_sha(eq_mans, "eq", f"input/{kid}.input.csv")
        in_pin_b38 = manifest_sha(b38_mans, "b38", f"input/{kid}.input.csv")
        if in_pin_eq != in_pin_b38:
            fail(f"EQ-vs-b38 gate input clone drift: {kid}")
        want_line = f"target,0,5,{lo},{hi},{legal},0,0,0,0,0"
        body = [l for l in (EQ_KIT / f"input/{kid}.input.csv").read_text().splitlines() if l.strip()]
        if body != [want_line]:
            fail(f"gate input csv body drift: {kid}: {body}")
        # gate raw pair
        gp1 = manifest_sha(eq_mans, "eq", f"output/raw/{kid}.p1.out")
        gp2 = manifest_sha(eq_mans, "eq", f"output/raw/{kid}.p2.out")
        g = check_two_pass(EQ_KIT / f"output/raw/{kid}.p1.out",
                           EQ_KIT / f"output/raw/{kid}.p2.out", gp1, gp2)
        # registry quadruple + label agreement
        exp = registry["targets"][kid]["expected"]
        parts = exp.split(",")
        if (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])) != (legal, EQ_REGISTRY_BUDGET, 1, g["nodes"]):
            fail(f"EQ registry expected-quadruple drift: {kid}")
        if (g["stones"], g["is_or"], g["budget"], g["result"]) != (5, 0, EQ_REGISTRY_BUDGET, 1):
            fail(f"EQ gate raw label drift: {kid}")
        # audit per-key
        rec = audit["rows"].get(kid)
        want = f"{legal},{EQ_REGISTRY_BUDGET},1,{g['nodes']}"
        if rec is None or rec.get("budget") != str(EQ_REGISTRY_BUDGET) or \
                rec.get("expected") != want or rec.get("observed_p1") != want:
            fail(f"EQ gate audit per-row drift: {kid} {rec}")
        for gkey in (f"G1:{kid}:p1", f"G1:{kid}:p2"):
            if audit["gates"].get(gkey, {}).get("status") != "PASS":
                fail(f"EQ gate audit per-pass gates not PASS: {kid} {gkey}")
        # b38 source raw pair (same single 15M condition)
        sp1 = manifest_sha(b38_mans, "b38", f"output/raw/{kid}.p1.out")
        sp2 = manifest_sha(b38_mans, "b38", f"output/raw/{kid}.p2.out")
        s = check_two_pass(B38_KIT / f"output/raw/{kid}.p1.out",
                           B38_KIT / f"output/raw/{kid}.p2.out", sp1, sp2)
        if (s["legal"], s["is_or"], s["budget"], s["result"], s["nodes"]) != \
                (legal, 0, B38_BUDGET, 1, g["nodes"]):
            fail(f"b38 source raw != EQ gate raw core fields: {kid}")
        # freshness + quarantine
        if (lo, hi) in base_rows:
            fail(f"adopted key already in BASE (fresh gate): {kid}")
        if (lo, hi) in qkeys:
            fail(f"adopted key quarantined: {kid}")
        rows.append({"key_id": kid, "class": 30345, "s5_index": k["s5_index"],
                     "lo": lo, "hi": hi, "legal": legal,
                     "budget": EQ_REGISTRY_BUDGET, "nodes": g["nodes"]})
        gate_pins[kid] = {"input": in_pin_eq, "p1": gp1, "p2": gp2}
        src_pins[kid] = {"p1": sp1, "p2": sp2}
        adopted_nodes += g["nodes"]

    if adopted_nodes != EXPECTED_ADOPTED_NODES:
        fail(f"adopted node total drift: {adopted_nodes} (expected {EXPECTED_ADOPTED_NODES})")

    # emission
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure: erwin18 canonical-adoption increment (Part ER, 2026-11-25)",
        "#   The 18 scrutinized batch-38 probe-level WIN rows of closure class 30345",
        "#   (ai002/ai003/ai005/ai006/ai010/ai013/ai014/ai017/ai023/ai028/ai034/ai035/",
        "#   ai036/ai039/ai043/ai046/ai047/ai049) consumed as WIN verdicts, the second",
        "#   WIN canonical adoption of this chain.",
        "#   WIN label eligibility: published b38 two-pass fresh-cold node-exact",
        "#   source raws (original probes), the Part EQ C++ second-implementation",
        "#   gate 9193f5b6... executed two-pass fresh-cold (21/21 GATE-PASS, audit",
        "#   c2ff2232...), gate inputs = byte-clones of the b38 kit pins, per-key",
        "#   quadruples vs the batch-keys-b38.json SSOT, disposition re-derived from",
        "#   the published batch (24 LOSS / 6 honest-EXHAUSTED / 19 WIN; ai048 already",
        "#   consumed by Part EP).  Every row is fresh to BASE fd29a337... and not",
        "#   quarantined.  Consuming WIN labels asserts NO root verdict and NO 11x11",
        "#   outcome; scheduling bookkeeping is re-audited fail-closed by the refresh.",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping.",
    ]
    lines = list(hdr)
    for r in sorted(rows, key=lambda x: (x["lo"], x["hi"])):
        lines.append(f"s5verdict,{r['lo']},{r['hi']},5,1,{r['nodes']}")
    incr_path = OUT / "increment-erwin18-20261125.cache"
    incr_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {
        "schema": "erwin18-increments-manifest-v1",
        "part": "ER",
        "date": "2026-11-25",
        "win_canonical_adoption": True,
        "base_cache_sha256": BASE_CACHE_SHA,
        "base_cache_path": "research/experiments/n11-centralreply-epwin10-adoption-reaudit-20261125/output/merged-exact-s5-chain-plus-epwin10-20261125.cache",
        "base_cache_rows": BASE_CACHE_ROWS,
        "merger_sha256": MERGER_SHA,
        "merger_note": "fail-closed union merger byte-clone 90711961...; WIN/LOSS conflict abort; first-occurrence nodes",
        "sha256": {"win_increment": sha(incr_path)},
        "adopted_win_rows": [
            {"key_id": r["key_id"], "class": r["class"], "s5_index": r["s5_index"],
             "lo": r["lo"], "hi": r["hi"], "legal": r["legal"], "budget": r["budget"],
             "result": 1, "nodes": r["nodes"],
             "gate_kit": "eq",
             "gate_input_sha256": gate_pins[r["key_id"]]["input"],
             "gate_raw_p1_sha256": gate_pins[r["key_id"]]["p1"],
             "gate_raw_p2_sha256": gate_pins[r["key_id"]]["p2"],
             "source_kit": "b38", "source_dir": "output/raw",
             "source_raw_p1_sha256": src_pins[r["key_id"]]["p1"],
             "source_raw_p2_sha256": src_pins[r["key_id"]]["p2"],
             "extra_provenance": None}
            for r in sorted(rows, key=lambda x: (x["lo"], x["hi"]))
        ],
        "adopted_ids": sorted(r["key_id"] for r in rows),
        "resolved_ids": sorted(r["key_id"] for r in rows),
        "row_counts": {"adopted_win_rows": len(rows),
                       "exhausted_honest_unknown_rows": 0,
                       "prior_canonical_rows_base": BASE_CACHE_ROWS,
                       "loss_rows_this_pool": 0},
        "adopted_nodes_per_pool": adopted_nodes,
        "adopted_nodes_declared_in_eq_prose": {"value": 136539338,
                                               "note": "Part EQ declaration prose mis-sum, disclosed; per-row registry/audit/raws agree on 136,604,338 (machine-verified per row here)"},
        "batch38_disposition_derivation": {
            "published_raw_derived": {d: sorted(disposition[d]) for d in disposition},
            "counts": {d: len(disposition[d]) for d in disposition},
            "consumed_by_ep": [EP_CONSUMED_KEY],
            "targets_adopted_here": sorted(r["key_id"] for r in rows),
        },
        "full_packet_eq_win_only": True,
        "loss_scenario_exists": False,
        "verdicts_out_of_scope_unconsumed": {
            "batch38_6_exhausted": "honest UNKNOWN at the 15M condition (ai007/ai024/ai030/ai038/ai040/ai041, budget ceiling holds)",
            "batch38_loss_rows": "the 24 b38 LOSS rows were consumed by the Part EM loss-only adoption territory",
            "ai048": "consumed by Part EP (first-ever WIN adoption); verified present in the EP increment c245bc4c... and BASE fd29a337...",
            "ai044": "LOSS row, EM adoption territory, unconsumed by WIN parts",
            "b018": "batch-1 dual-class probe-level WIN, scrutiny-owner pending, same-condition re-probe prohibited - consumed nowhere",
            "k04_sixthcost_win": "owned by the sixth-cost lane; NOT adopted",
            "other_closure_wins": "every other unconsumed probe-level WIN row stays in NO cache",
        },
        "provenance": {
            "pin_policy": "no per-file kit sha is hand-typed; all per-row pins are extracted from the byte-verified published kit MANIFESTs and re-hashed live at emission",
            "eq_kit_manifest_sha256": EQ_MANIFEST_SHA,
            "eq_registry_sha256": EQ_REGISTRY_SHA,
            "eq_audit_sha256": EQ_AUDIT_SHA,
            "eq_audit_schema": EQ_AUDIT_SCHEMA,
            "eq_gate_status_pass": EQ_STATUS_PASS,
            "eq_gate_source_sha256": EQ_GATE_SOURCE_SHA,
            "b38_manifest_sha256": B38_MANIFEST_SHA,
            "b38_keys_sha256": B38_KEYS_SHA,
            "ep_increment_sha256": EP_INCREMENT_SHA,
            "kit_integrity": "both referenced kits (eq/b38) verified file-by-file against their pinned MANIFESTs (74 + 181 entries)",
        },
        "quarantine_hits": 0,
        "base_cache_absent_hits_for_emitted": len(rows),
        "interpretation_guard": "nodes are bookkeeping, never verdicts; consuming a WIN label asserts no root verdict; the standard 11x11 empty board stays UNKNOWN",
    }
    manifest_path = OUT / "increments-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    print(f"ER increment OK: rows={len(rows)} nodes={adopted_nodes} incr_sha={sha(incr_path)}")
    print(f"manifest sha={sha(manifest_path)}")


if __name__ == "__main__":
    main()
