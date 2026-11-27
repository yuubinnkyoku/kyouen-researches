#!/usr/bin/env python3
"""Build the epwin10 (Part EP 10-scrutinized-WIN-row) canonical-adoption
increment, fail-closed.

Part EP (2026-11-25).  BASE = the published Part EM canonical merged chain
head merged-exact-s5-chain-plus-b38loss24-20261125.cache (6,737 rows, sha256
b5be64e6b96af435ab589caced29273bab765085ba13c3033e897de13fab636c, WIN 158 /
LOSS 6,579).  The adopted pool is the FIRST-EVER WIN canonical adoption in
this chain: the 10 probe-level WIN rows that have now passed the
scrutiny-owner C++ second-implementation gate `kyouen_dfpn_root.cpp` at
commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19 (source byte pin 9193f5b6...),
executed two-pass fresh-cold by Part EN (class 30484 rows aj030/aj049/aj050/
ai048) and Part EO (class 34908 rows af029/af047/af050/af053/af023/af048),
and corroborated for the six class-34908 rows by the Part EG JS
third-implementation replication (third_impl 08ea958f..., audit-summary
73af060a... all gates PASS).

PIN POLICY (this revision, 2026-11-25 EP rebuild): no per-file sha of any kit
member is hand-typed in this script.  Every kit's MANIFEST-sha256.txt is
itself byte-pinned by a constant below; the maker verifies EVERY manifest
entry file-by-file first, then extracts each per-row pin (gate input csv,
gate raw pair, source raw pair, EG clones) from those verified MANIFESTs and
re-asserts live recomputed sha256 equality.  This eliminates the
transcription-error class found in the earlier draft (63/64-char sha
typos) by construction.

Every adopted row satisfies ALL of, machine-verified below:

(a) SOURCE-RAW provenance: a published original probe pair in its own kit,
    two-pass fresh-cold node-exact at the row's own single condition --
    b33 kit 15M raws for af029/af047/af050/af053; Part EA 30M reprobe raws
    for af023/af048; Part EK 30M reprobe raws for aj030 (and the EK 30M
    anchor for aj049); b39 kit 15M raws for aj049/aj050; Part EF b38 kit
    15M raws for ai048.  No row is re-probed here; the same-condition
    re-probe ban is untouched.  The 15M EXHAUSTED labels of af023/af048 in
    b33 are honest UNKNOWN remnants of a different (superseded) condition
    and are NOT adopted; the 30M labels are the adopted condition.
(b) GATE provenance: the published Part EN / Part EO gate kits
    (MANIFEST-sha256.txt 384cad61... / b6e2663a...), verified file-by-file
    (34 / 37 entries; the Part EN kit's declaration.md mirror lives at
    research/log/2026-11-25-part-en-cppgate-30484win4-declaration.md with
    byte pin b606b27d...), the gate input csvs byte-pinned as published,
    the gate C++ raw pairs p1/p2 with
    (stones, legal, is_or, budget, result, nodes, lo, hi) field-equal across
    the two passes and equal to the source raws, the machine audits
    audit_gate.json (Part EN f35cddd2..., Part EO b46f2130..., both overall
    PASS, schema n11-centralreply-cppgate-30484win4-audit-v1 /
    n11-centralreply-cppgate-34908win6-audit-v1) re-pinned byte-exact, per
    key budget/expected/observed equality, and the run statuses
    (8/8 and 9/9 GATE-PASS, zero MISMATCH/GATE-FAIL/GATE-CRASH).
(c) FRESHNESS: every adopted (lo,hi) is absent from BASE and absent from
    the quarantine registry 81d23160...; the merges are conflict-free by
    construction (the fail-closed union merger 90711961... re-checks
    WIN/LOSS conflicts independently).
(d) KEY-SSOT cross-check: the (lo,hi,legal,s5_index) quadruples match the
    published batch-keys SSOTs -- b33 input/batch-keys.json
    (8a863381...), Part EA sources/ea-reprobe-keys.json (3744b522...),
    b39 input/batch-keys-b39.json (5e25b550...), Part EF b38
    input/batch-keys-b38.json (29807104...), and Part EK
    output/audit_ek.json (d9aa8aab...) provenance; AND the gate input csvs
    are byte-identical clones (EG kit pins == EO gate-kit pins for the six
    class-34908 rows; EK kit pins == EN gate-kit pins for aj030/aj049).
(e) EG byte-clone depth: the Part EG kit's sources/b33-raw clones of
    af029/af047/af050/af053 and sources/ea-raw clones of af023/af048 (and
    the af029 30M pair) equal the original kit MANIFEST shas, all
    recorded below.  The EG sources/b33-raw clones of af023/af048 are the
    superseded 15M EXH condition on purpose (clone == EA sources/exh15m
    byte clone is verified for bookkeeping only) and are NOT adoption
    provenance.  EG sources/b33-batch-keys.json == b33 batch-keys (SSOT
    clone), EK sources/n11-s5-evidence-quarantine.json == the quarantine
    registry clone.

verdict semantics: adopting a WIN row into the canonical cache consumes the
row's honest WIN label as a canonical S5 child verdict of the chain cache.
It asserts NO root verdict and NO 11x11 outcome: the closure class becomes
excluded (a known WIN cost child can no longer serve as free all-LOSS
coverage), which is scheduling bookkeeping derived only by the reaudit
refresh (Board fail-closed child verification).  The standard 11x11 empty
board stays UNKNOWN.  nodes are bookkeeping, never verdicts.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"

EM_KIT = ROOT / "research/experiments/n11-centralreply-b38loss24-adoption-reaudit-20261125"
BASE_CACHE = EM_KIT / "output/merged-exact-s5-chain-plus-b38loss24-20261125.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
EN_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30484-cppgate-20261125"
EO_KIT = ROOT / "research/experiments/n11-centralreply-closure-class34908-cppgate-20261125"
B33_KIT = ROOT / "research/experiments/n11-centralreply-closure-class34908-batch33-20261124"
EA_KIT = ROOT / "research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125"
EK_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125"
B39_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30484-batch39-20261125"
B38_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-batch38-20261125"
EG_KIT = ROOT / "research/experiments/n11-centralreply-closure-b33win6-thirdimpl-20261125"
EN_DECLARATION = ROOT / "research/log/2026-11-25-part-en-cppgate-30484win4-declaration.md"

MERGER = EXP / "scripts/s5_union_merge.py"

# ---------------- top-level pins (each re-derived from the pinned-commit ----
# fetch 28822eb0b3d9948e97bdbb524f4e9745ba87b1b1 local clone; the published
# bytes at raw.githubusercontent are the authority and were byte-verified
# during this rebuild) -------------------------------------------------------
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA = "b5be64e6b96af435ab589caced29273bab765085ba13c3033e897de13fab636c"
BASE_CACHE_ROWS = 6737
BASE_CACHE_WIN = 158
BASE_CACHE_LOSS = 6579
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

EN_MANIFEST_SHA = "384cad6143aac8e05cc0ca7ec7a97e42f2dec600d9acb521a541b8e8996c5401"
EO_MANIFEST_SHA = "b6e2663abf6917ad2999637dcc929c9ba3991a58bf1109d6d2cc78d46e8adadd"
EN_DECLARATION_SHA = "b606b27d0993a8e8b997d295b7e34fa566760bf2b5cc0e8224505cd5ead4787d"
EN_AUDIT_SHA = "f35cddd24f7062c1e0861563fbce737edabd2620ae3028d3c2d42fd937c407af"
EO_AUDIT_SHA = "b46f2130e9855204b5d3a12c07833083af1e96fc4dd9013893f6be7ed0bfa057"
EN_STATUS_PASS = 8
EO_STATUS_PASS = 9
EN_AUDIT_SCHEMA = "n11-centralreply-cppgate-30484win4-audit-v1"
EO_AUDIT_SCHEMA = "n11-centralreply-cppgate-34908win6-audit-v1"

B33_MANIFEST_SHA = "f2603e3a12d291579f02b81b7c388b5c952b90125df53756c91812368f16dbcb"
B33_KEYS_SHA = "8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa"
EA_MANIFEST_SHA = "42ba81bc79dd887074dbc9514b87f0c9d1a656d53a98ff3dfef29b9c4666601e"
EA_KEYS_SHA = "3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663"
EK_MANIFEST_SHA = "97574401309964806a8eed4968496dcd222aecaf029aa9b1115dcaaa2ec78a68"
EK_AUDIT_SHA = "d9aa8aab971ca0975caea7e52156bea86b3c183d843a40a8cea44a8dcf54691b"
EK_STATUS_SHA = "868bfbff196343d074c909b0290739a0111f2b3dcfc04967f459528dbab6c01c"
B39_MANIFEST_SHA = "52b69c0404c9f78451249c6decc65f70b908e44a98bebac0b827d8eb8aa5bf41"
B39_KEYS_SHA = "5e25b550ef42c1f56dc9d4b69d61d33304664ad839ed7f8d19f45fe50f5e63a9"
B38_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"
B38_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
EG_MANIFEST_SHA = "ed568fc7733cba14af901b35a31ff4e8ae15b9a3315b03934afe56e0107641be"
EG_AUDIT_SUMMARY_SHA = "73af060a4c139818e0e4625ed511945394169afca6ad704eec8c4c6b4bcfc7bf"
EG_THIRD_IMPL_SHA = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
EG_AUDIT_SCHEMA = "n11-centralreply-closure-b33win6-thirdimpl-audit-v1"

# ---------------- adopted rows (semantic pins only) --------------------------
# (key_id, class, s5_index, lo, hi, legal, budget, nodes,
#  gate kit tag, source kit tag, source rel dir, extra (kit tag, rel dir) or None)
ROWS = [
    ("af029", 34908, 900646, 1152921504607895553, 68720525312, 86, 15000000, 4862485,
     "eo", "b33", "output/raw", ("ea", "output/raw")),
    ("af047", 34908, 961976, 1152921504607895809, 68719476736, 84, 15000000, 9841975,
     "eo", "b33", "output/raw", None),
    ("af050", 34908, 962386, 1152921504607899649, 68719476736, 94, 15000000, 7311834,
     "eo", "b33", "output/raw", None),
    ("af053", 34908, 962470, 1152921504606852096, 17660905521152, 90, 15000000, 5182129,
     "eo", "b33", "output/raw", None),
    ("af023", 34908, 810351, 1152921504607895553, 68719478784, 94, 30000000, 28933179,
     "eo", "ea", "output/raw", None),
    ("af048", 34908, 962172, 1152921508902862849, 68719476736, 87, 30000000, 17816616,
     "eo", "ea", "output/raw", None),
    ("aj030", 30484, 892576, 1152922604135251976, 65536, 83, 30000000, 15284699,
     "en", "ek", "output/raw", None),
    ("aj049", 30484, 902511, 1152921574400065536, 1114112, 80, 30000000, 4998452,
     "en", "ek", "output/raw", ("b39", "output/raw")),
    ("aj050", 30484, 902512, 1152921574400065536, 68157440, 80, 15000000, 1871594,
     "en", "b39", "output/raw", None),
    ("ai048", 30484, 900718, 1152921573327372288, 68157440, 68, 15000000, 2232854,
     "en", "b38", "output/raw", None),
]
ADOPTED_IDS = [r[0] for r in ROWS]
ADOPTED_NODES = sum(r[7] for r in ROWS)

# SSOT key_id -> (json path, kit) used in the G4 quadruple cross-check
KEY_SSOTS = [
    (B33_KIT / "input/batch-keys.json", (B33_KEYS_SHA, "b33")),
    (EG_KIT / "sources/ea-reprobe-keys.json", (EA_KEYS_SHA, "ea")),
    (B39_KIT / "input/batch-keys-b39.json", (B39_KEYS_SHA, "b39")),
    (B38_KIT / "input/batch-keys-b38.json", (B38_KEYS_SHA, "b38")),
]

# raw format: replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def fail(msg):
    print(f"ABORT ep-max: {msg}", file=sys.stderr)
    raise SystemExit(1)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    import hashlib as _h
    h = _h.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def kit_dir(tag: str) -> Path:
    tags = {"b33": B33_KIT, "ea": EA_KIT, "ek": EK_KIT, "b39": B39_KIT, "b38": B38_KIT,
            "en": EN_KIT, "eo": EO_KIT, "eg": EG_KIT, "em": EM_KIT}
    try:
        return tags[tag]
    except KeyError:
        fail(f"unknown kit tag {tag}")


def parse_manifest(path: Path, kit_root: Path):
    """Parse a MANIFEST-sha256.txt.

    Returns dict keyed by the KIT-RELATIVE path -> {"sha256": str, "size":
    int|None, "blob_sha1": str|None, "local": Path}.  Handles the three
    published line formats: `<sha256>  <path>`, `<sha256>  <size>  <path>`
    and `<sha256>  <git-blob-sha1>  <path>`.  Paths that start with
    `research/` or `results/` are repo-root relative (normalized to a
    kit-relative key when they live inside the kit); others are already
    kit-relative.
    """
    out = {}
    kit_prefix = f"research/experiments/{kit_root.name}/"
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f = line.split()
        if len(f) < 2 or not HEX64.match(f[0]):
            fail(f"unexpected MANIFEST line in {path}: {line!r}")
        sha256 = f[0]
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
        if key in out and out[key]["sha256"] != sha256:
            fail(f"duplicate MANIFEST path with conflicting sha in {path}: {key}")
        out[key] = {"sha256": sha256, "size": size, "blob_sha1": blob1,
                    "local": local}
    return out


def parse_raw(path: Path):
    """Return the single replay row dict of a two-pass raw output."""
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
        if line.startswith("# replay_done"):
            seen_done = True
    if len(rows) != 1 or not seen_done:
        fail(f"raw {path} must hold exactly one replay row plus the # replay_done guard")
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


def verify_kit(tag: str, man_sha: str) -> dict:
    """Byte-verify a whole kit against its pinned MANIFEST; return the parsed
    manifest dict.  EN's declaration.md is a published log mirror special
    case; em/b39/repo-relative paths resolve against ROOT."""
    kit = kit_dir(tag)
    man = kit / "MANIFEST-sha256.txt"
    if sha(man) != man_sha:
        fail(f"kit MANIFEST sha drift ({tag})")
    entries = parse_manifest(man, kit)
    for rel, rec in entries.items():
        p = rec["local"]
        if not p.is_file():
            if tag == "en" and rel == "declaration.md":
                if sha(EN_DECLARATION) != rec["sha256"]:
                    fail("EN declaration mirror sha drift (log mirror)")
                continue
            fail(f"kit file missing ({tag}): {rel}")
        if sha(p) != rec["sha256"]:
            fail(f"kit sha drift ({tag}): {rel}")
        if rec["size"] is not None and p.stat().st_size != rec["size"]:
            fail(f"kit size drift ({tag}): {rel}")
        if rec["blob_sha1"] is not None and git_blob_sha1(p) != rec["blob_sha1"]:
            fail(f"kit git-blob sha1 drift ({tag}): {rel}")
    return entries


def manifest_sha(entries: dict, kit_tag: str, rel: str) -> str:
    if rel not in entries:
        fail(f"pin absent from {kit_tag} MANIFEST: {rel}")
    return entries[rel]["sha256"]


def main() -> None:
    # G0: merger byte-clone + BASE identity + quarantine pin
    if sha(MERGER) != MERGER_SHA:
        fail("union merger byte-clone sha drift (expected 90711961...)")
    if sha(BASE_CACHE) != BASE_CACHE_SHA:
        fail("BASE cache sha drift (expected b5be64e6...)")
    if sha(QUARANTINE) != QUARANTINE_SHA:
        fail("quarantine registry sha drift")

    base_rows = {}
    for line in BASE_CACHE.read_text(encoding="utf-8-sig").splitlines():
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
    for r in ROWS:
        if (r[3], r[4]) in base_rows:
            fail(f"adopted key already in BASE (fresh gate): {r[0]}")
    quarantined = json.loads(QUARANTINE.read_text())
    qkeys = set()
    for entry in quarantined if isinstance(quarantined, list) else quarantined.get("keys", []):
        if isinstance(entry, dict) and "lo" in entry:
            qkeys.add((int(entry["lo"]), int(entry["hi"])))
    for r in ROWS:
        if (r[3], r[4]) in qkeys:
            fail(f"adopted key quarantined: {r[0]}")

    # G1: whole-kit file-by-file integrity of every referenced published kit
    kit_mans = {
        "en": verify_kit("en", EN_MANIFEST_SHA),
        "eo": verify_kit("eo", EO_MANIFEST_SHA),
        "b33": verify_kit("b33", B33_MANIFEST_SHA),
        "ea": verify_kit("ea", EA_MANIFEST_SHA),
        "ek": verify_kit("ek", EK_MANIFEST_SHA),
        "b39": verify_kit("b39", B39_MANIFEST_SHA),
        "b38": verify_kit("b38", B38_MANIFEST_SHA),
        "eg": verify_kit("eg", EG_MANIFEST_SHA),
    }
    en_kit_n = len(kit_mans["en"])
    eo_kit_n = len(kit_mans["eo"])
    if en_kit_n != 34 or eo_kit_n != 37:
        fail(f"gate-kit manifest entry count drift: en {en_kit_n} eo {eo_kit_n}")

    # gate-kit machine audit + run-status honesty
    for tag, kit, audit_sha, status_n, schema in (
            ("en", EN_KIT, EN_AUDIT_SHA, EN_STATUS_PASS, EN_AUDIT_SCHEMA),
            ("eo", EO_KIT, EO_AUDIT_SHA, EO_STATUS_PASS, EO_AUDIT_SCHEMA)):
        audit_path = kit / "output/audit_gate.json"
        if sha(audit_path) != audit_sha:
            fail(f"gate-kit machine audit sha drift ({tag})")
        audit = json.loads(audit_path.read_text())
        if audit.get("overall") != "PASS" or audit.get("part") != tag.upper() or \
                audit.get("schema") != schema:
            fail(f"gate-kit audit honesty drift ({tag})")
        ok = 0
        bad = []
        for line in (kit / "output/gate-status.log").read_text().splitlines():
            if " GATE-PASS " in line:
                ok += 1
            elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
                bad.append(line)
        if ok != status_n or bad:
            fail(f"gate-kit status accounting drift ({tag}): ok {ok} bad {bad}")

    # G2: per-row gate provenance (inputs, raw pairs, audit per-key PASS)
    gate_pins = {}
    for r in ROWS:
        rid, cls, s5, lo, hi, legal, budget, nodes, gk = r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]
        kit = kit_dir(gk)
        man = kit_mans[gk]
        in_pin = manifest_sha(man, gk, f"input/{rid}.input.csv")
        ipath = kit / f"input/{rid}.input.csv"
        if sha(ipath) != in_pin:
            fail(f"gate input csv sha drift: {rid}")
        want_line = f"target,0,5,{lo},{hi},{legal},0,0,0,0,0"
        rows_in = [l for l in ipath.read_text().splitlines() if l.strip()]
        if rows_in != [want_line]:
            fail(f"gate input csv body drift: {rid}: {rows_in}")
        p1_pin = manifest_sha(man, gk, f"output/raw/{rid}.p1.out")
        p2_pin = manifest_sha(man, gk, f"output/raw/{rid}.p2.out")
        g = check_two_pass(kit / f"output/raw/{rid}.p1.out",
                           kit / f"output/raw/{rid}.p2.out", p1_pin, p2_pin)
        if (g["stones"], g["legal"], g["is_or"], g["budget"], g["result"], g["nodes"]) != \
                (5, legal, 0, budget, 1, nodes) or int(g["lo"]) != lo or int(g["hi"]) != hi:
            fail(f"gate raw field disagreement vs the adoption pin: {rid}")
        audit = json.loads((kit / "output/audit_gate.json").read_text())
        rec = audit["rows"].get(rid)
        expect = f"{legal},{budget},1,{nodes}"
        if rec is None or rec.get("budget") != str(budget) or \
                rec.get("expected") != expect or rec.get("observed_p1") != expect:
            fail(f"gate audit per-row drift: {rid} {rec}")
        gkey = f"G1:{rid}:p1"
        if audit["gates"].get(gkey, {}).get("status") != "PASS" or \
                audit["gates"].get(f"G1:{rid}:p2", {}).get("status") != "PASS":
            fail(f"gate audit per-pass gates not PASS: {rid}")
        gate_pins[rid] = {"input": in_pin, "p1": p1_pin, "p2": p2_pin, "kit": gk}

    # gate input csvs are byte-identical clones across kits where published:
    # EG kit pins == EO gate-kit pins (six class-34908 rows); EK kit pins ==
    # EN gate-kit pins (aj030/aj049).
    for rid in ("af029", "af047", "af050", "af053", "af023", "af048"):
        if manifest_sha(kit_mans["eg"], "eg", f"input/{rid}.input.csv") != gate_pins[rid]["input"]:
            fail(f"EG-vs-EO gate input clone drift: {rid}")
    for rid in ("aj030", "aj049"):
        if manifest_sha(kit_mans["ek"], "ek", f"input/{rid}.input.csv") != gate_pins[rid]["input"]:
            fail(f"EK-vs-EN gate input clone drift: {rid}")

    # G3: source-raw provenance (original kit pairs; manifest-extracted pins)
    src_pins = {}
    for r in ROWS:
        rid, cls, s5, lo, hi, legal, budget, nodes, gk, sk, sdir, extra = r
        s_p1 = manifest_sha(kit_mans[sk], sk, f"{sdir}/{rid}.p1.out")
        s_p2 = manifest_sha(kit_mans[sk], sk, f"{sdir}/{rid}.p2.out")
        s = check_two_pass(kit_dir(sk) / f"{sdir}/{rid}.p1.out",
                           kit_dir(sk) / f"{sdir}/{rid}.p2.out", s_p1, s_p2)
        if (s["stones"], s["legal"], s["is_or"], s["budget"], s["result"], s["nodes"]) != \
                (5, legal, 0, budget, 1, nodes) or int(s["lo"]) != lo or int(s["hi"]) != hi:
            fail(f"source raw field disagreement vs the adoption pin: {rid}")
        e_pins = None
        if extra is not None:
            ek_tag, edir = extra
            e_p1 = manifest_sha(kit_mans[ek_tag], ek_tag, f"{edir}/{rid}.p1.out")
            e_p2 = manifest_sha(kit_mans[ek_tag], ek_tag, f"{edir}/{rid}.p2.out")
            e = check_two_pass(kit_dir(ek_tag) / f"{edir}/{rid}.p1.out",
                               kit_dir(ek_tag) / f"{edir}/{rid}.p2.out", e_p1, e_p2)
            # budget-INDEPENDENCE witness: the extra pair is the same WIN at a
            # different budget with the same nodes; only the budget field may
            # differ (that is the point of the witness).  The row's own
            # adopted condition is fixed by the primary source pair.
            if (e["stones"], e["legal"], e["is_or"], e["result"], e["nodes"]) != \
                    (5, legal, 0, 1, nodes) or int(e["lo"]) != lo or int(e["hi"]) != hi:
                fail(f"extra provenance pair field disagreement (budget-independence witness): {rid}")
            if e["budget"] == budget:
                fail(f"extra provenance pair must exercise a different budget: {rid}")
            e_pins = {"kit": ek_tag, "p1": e_p1, "p2": e_p2,
                      "budget": e["budget"], "nodes": e["nodes"]}
        src_pins[rid] = {"kit": sk, "dir": sdir, "p1": s_p1, "p2": s_p2, "extra": e_pins}
        # the gate raw pair must be byte-distinct-from-source but field-equal;
        # field equality source-vs-gate is already forced by both matching the
        # adoption pin quadruple.

    # G4: key-SSOT quadruple cross-check (lo, hi, legal, s5_index)
    ssots = {}
    for path, (want_sha, tag) in KEY_SSOTS:
        if sha(path) != want_sha:
            fail(f"key SSOT sha drift ({tag})")
        for k in json.loads(path.read_text())["keys"]:
            if isinstance(k, dict) and "key_id" in k and "lo" in k:
                ssots.setdefault(k["key_id"], (int(k["lo"]), int(k["hi"]),
                                               int(k["legal"]), int(k["s5_index"])))
    for r in ROWS:
        rid, cls, s5, lo, hi, legal = r[0], r[1], r[2], r[3], r[4], r[5]
        if rid not in ssots:
            fail(f"key absent from every SSOT: {rid}")
        if ssots[rid] != (lo, hi, legal, s5):
            fail(f"key SSOT disagreement: {rid} {ssots[rid]} != {(lo, hi, legal, s5)}")
    if sha(EK_KIT / "output/audit_ek.json") != EK_AUDIT_SHA:
        fail("EK audit sha drift")
    if sha(EK_KIT / "output/status.log") != EK_STATUS_SHA:
        fail("EK status sha drift")
    # cross-kit SSOT clones: EG batch-keys clone == b33 keys; EK quarantine
    # clone == the registry
    if manifest_sha(kit_mans["eg"], "eg", "sources/b33-batch-keys.json") != B33_KEYS_SHA:
        fail("EG b33-batch-keys clone drift")
    if sha(B33_KIT / "input/batch-keys.json") != B33_KEYS_SHA:
        fail("b33 batch-keys SSOT sha drift")
    if manifest_sha(kit_mans["ek"], "ek", "sources/n11-s5-evidence-quarantine.json") != QUARANTINE_SHA:
        fail("EK quarantine registry clone drift")

    # G5: EG byte-clone equality (explicit mapping of clones to original pins)
    # adopted-source clones:
    for rid in ("af029", "af047", "af050", "af053"):
        for p in ("p1", "p2"):
            if manifest_sha(kit_mans["eg"], "eg", f"sources/b33-raw/{rid}.{p}.out") != \
                    src_pins[rid][p]:
                fail(f"EG b33-raw clone sha != original kit pin: {rid}.{p}")
    for rid in ("af023", "af048"):
        for p in ("p1", "p2"):
            if manifest_sha(kit_mans["eg"], "eg", f"sources/ea-raw/{rid}.{p}.out") != \
                    src_pins[rid][p]:
                fail(f"EG ea-raw clone sha != original kit pin: {rid}.{p}")
    # af029 30M extra-provenance clone (EA reprobe pair):
    for p in ("p1", "p2"):
        if manifest_sha(kit_mans["eg"], "eg", f"sources/ea-raw/af029.{p}.out") != \
                src_pins["af029"]["extra"][p]:
            fail(f"EG ea-raw clone sha != EA extra-provenance pin: af029.{p}")
    # superseded-condition bookkeeping (NOT adoption provenance): the EG
    # b33-raw clones of af023/af048 are the 15M EXH pair and must equal the
    # EA kit's sources/exh15m clones byte-for-byte.
    superseded = {}
    for rid in ("af023", "af048"):
        pair = {}
        for p in ("p1", "p2"):
            clone = manifest_sha(kit_mans["eg"], "eg", f"sources/b33-raw/{rid}.{p}.out")
            orig = manifest_sha(kit_mans["ea"], "ea", f"sources/exh15m/{rid}.{p}.out")
            if clone != orig:
                fail(f"superseded-condition clone drift EG-vs-EA exh15m: {rid}.{p}")
            pair[p] = clone
        superseded[rid] = pair

    # G6: third-implementation corroboration (class-34908 rows)
    if sha(EG_KIT / "output/audit-summary.json") != EG_AUDIT_SUMMARY_SHA:
        fail("EG audit-summary sha drift")
    if sha(EG_KIT / "scripts/third_impl.js") != EG_THIRD_IMPL_SHA:
        fail("EG third_impl.js sha drift")
    eg_audit = json.loads((EG_KIT / "output/audit-summary.json").read_text())
    if eg_audit.get("all_pass") is not True or eg_audit.get("schema") != EG_AUDIT_SCHEMA:
        fail("EG third-implementation audit-summary honesty drift")

    # emission
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure: epwin10 canonical-adoption increment (Part EP, 2026-11-25)",
        "#   The 10 scrutinized probe-level WIN rows consumed by the FIRST-EVER WIN canonical",
        "#   adoption in this chain: class 34908 {af029, af047, af050, af053, af023, af048} and",
        "#   class 30484 {aj030, aj049, aj050, ai048}.",
        "#   WIN label eligibility: published original two-pass fresh-cold node-exact raw pairs",
        "#   in the source kits (b33/EA/EK/b39/b38), the C++ second-implementation gate 9193f5b6...",
        "#   executed two-pass by Part EN (30484 rows) / Part EO (34908 rows) with audit rc=0, and",
        "#   the Part EG JS third-implementation replication for the class-34908 rows.",
        "#   Every row is absent from BASE (b5be64e6...) and from the quarantine registry.",
        "#   Consuming a WIN label asserts no root verdict and no 11x11 outcome; the closure",
        "#   classes 30484/34908 become excluded (a known WIN child ends all-LOSS coverage),",
        "#   derived only by the reaudit refresh.  11x11 stays UNKNOWN; nodes are bookkeeping.",
    ]
    lines = list(hdr)
    for r in sorted(ROWS, key=lambda x: (x[3], x[4])):
        lines.append(f"s5verdict,{r[3]},{r[4]},5,1,{r[7]}")
    incr_path = OUT / "increment-epwin10-20261125.cache"
    incr_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # live-recompute the emitted per-row pins one last time (sha == manifest
    # pin == recomputed) so the manifest below never carries a stale value.
    for rid, gp in gate_pins.items():
        kit = kit_dir(gp["kit"])
        for rel, pin in ((f"input/{rid}.input.csv", gp["input"]),
                         (f"output/raw/{rid}.p1.out", gp["p1"]),
                         (f"output/raw/{rid}.p2.out", gp["p2"])):
            if sha(kit / rel) != pin:
                fail(f"emission-time rehash drift {gp['kit']} {rel}")

    manifest = {
        "schema": "epwin10-increments-manifest-v1",
        "part": "EP",
        "date": "2026-11-25",
        "win_canonical_adoption": True,
        "base_cache_sha256": BASE_CACHE_SHA,
        "base_cache_path": "research/experiments/n11-centralreply-b38loss24-adoption-reaudit-20261125/output/merged-exact-s5-chain-plus-b38loss24-20261125.cache",
        "base_cache_rows": BASE_CACHE_ROWS,
        "merger_sha256": MERGER_SHA,
        "merger_note": "fail-closed union merger byte-clone 90711961...; WIN/LOSS conflict abort; first-occurrence nodes",
        "sha256": {"win_increment": sha(incr_path)},
        "adopted_win_rows": [
            {"key_id": r[0], "class": r[1], "s5_index": r[2], "lo": r[3], "hi": r[4],
             "legal": r[5], "budget": r[6], "result": 1, "nodes": r[7],
             "gate_kit": r[8],
             "gate_input_sha256": gate_pins[r[0]]["input"],
             "gate_raw_p1_sha256": gate_pins[r[0]]["p1"],
             "gate_raw_p2_sha256": gate_pins[r[0]]["p2"],
             "source_kit": r[9], "source_dir": r[10],
             "source_raw_p1_sha256": src_pins[r[0]]["p1"],
             "source_raw_p2_sha256": src_pins[r[0]]["p2"],
             "extra_provenance": ({"kit": src_pins[r[0]]["extra"]["kit"],
                                   "raw_p1_sha256": src_pins[r[0]]["extra"]["p1"],
                                   "raw_p2_sha256": src_pins[r[0]]["extra"]["p2"]}
                                  if src_pins[r[0]]["extra"] else None)}
            for r in ROWS
        ],
        "adopted_ids": ADOPTED_IDS,
        "resolved_ids": ADOPTED_IDS,
        "row_counts": {"adopted_win_rows": len(ROWS),
                       "exhausted_honest_unknown_rows": 0,
                       "prior_canonical_rows_base": BASE_CACHE_ROWS,
                       "loss_rows_this_pool": 0},
        "adopted_nodes_per_pool": ADOPTED_NODES,
        "full_packet_eq_win_only": True,
        "loss_scenario_exists": False,
        "superseded_condition_clone_bookkeeping": {
            "note": "EG sources/b33-raw clones of af023/af048 are the 15M EXH "
                    "superseded condition; verified byte-equal to the EA kit "
                    "sources/exh15m pairs for bookkeeping only; NOT adoption provenance",
            "af023": superseded["af023"], "af048": superseded["af048"],
        },
        "verdicts_out_of_scope_unconsumed": {
            "k04_sixthcost_win": "verified WIN by the Part EN gate but owned by the sixth-cost lane; NOT adopted",
            "batch38_19_win": "remaining batch-38 probe-level WIN rows still unconsumed (no C++ gate execution yet)",
            "batch38_6_exhausted": "honest UNKNOWN at the 15M condition",
            "other_closure_wins": "every other unconsumed probe-level WIN row stays in NO cache",
            "af023_af048_15m_exhausted_b33_rows": "the b33 15M EXHAUSTED labels are superseded conditions, NOT adopted; the adopted rows are the EA 30M labels",
        },
        "provenance": {
            "pin_policy": "no per-file kit sha is hand-typed; all per-row pins are extracted from the byte-verified published kit MANIFESTs and re-hashed live at emission",
            "en_kit_manifest_sha256": EN_MANIFEST_SHA,
            "eo_kit_manifest_sha256": EO_MANIFEST_SHA,
            "en_kit_manifest_entries": en_kit_n,
            "eo_kit_manifest_entries": eo_kit_n,
            "en_declaration_log_mirror_sha256": EN_DECLARATION_SHA,
            "en_audit_sha256": EN_AUDIT_SHA,
            "eo_audit_sha256": EO_AUDIT_SHA,
            "en_gate_status_pass": EN_STATUS_PASS,
            "eo_gate_status_pass": EO_STATUS_PASS,
            "gate_source_sha256": "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e",
            "b33_manifest_sha256": B33_MANIFEST_SHA,
            "ea_manifest_sha256": EA_MANIFEST_SHA,
            "ek_manifest_sha256": EK_MANIFEST_SHA,
            "b39_manifest_sha256": B39_MANIFEST_SHA,
            "b38_manifest_sha256": B38_MANIFEST_SHA,
            "eg_manifest_sha256": EG_MANIFEST_SHA,
            "eg_audit_summary_sha256": EG_AUDIT_SUMMARY_SHA,
            "eg_third_impl_sha256": EG_THIRD_IMPL_SHA,
            "ek_audit_sha256": EK_AUDIT_SHA,
            "b33_keys_sha256": B33_KEYS_SHA,
            "ea_reprobe_keys_sha256": EA_KEYS_SHA,
            "b39_keys_sha256": B39_KEYS_SHA,
            "b38_keys_sha256": B38_KEYS_SHA,
            "kit_integrity": "all 9 referenced kits (en/eo/b33/ea/ek/b39/b38/eg) verified file-by-file against their pinned MANIFESTs (EN declaration.md via its research/log mirror)",
        },
        "quarantine_hits": 0,
        "base_cache_absent_hits_for_emitted": 0,
        "interpretation_guard": "nodes are bookkeeping, never verdicts; consuming a WIN label asserts no root verdict; the standard 11x11 empty board stays UNKNOWN",
    }
    manifest_path = OUT / "increments-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    print(f"EP increment OK: rows={len(ROWS)} nodes={ADOPTED_NODES} incr_sha={sha(incr_path)}")
    print(f"manifest sha={sha(manifest_path)}")


if __name__ == "__main__":
    main()
