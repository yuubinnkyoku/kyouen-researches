"""Build the b3loss3 (batch-3 d001/d003/d004) canonical-adoption increment, fail-closed.

Part EB (2026-11-25).  BASE = the published Part DZ canonical merged cache
(6,660 rows, sha 4a30b88d...).  The single adopted pool is the published
batch-3 packet (class 20421, probed 2026-11-22): exactly the 3 fresh LOSS
rows d001/d003/d004; the probe-level WIN d002 is consumed NOWHERE (scrutiny
owner C++ second-implementation gate pin 9193f5b6...).  No WIN verdict is
consumed; no root verdict is asserted; 11x11 stays UNKNOWN.

Every gate is fail-closed: any drift aborts with rc=1 and no output is
written.  The published packet is verified byte-for-byte (batch keys
ad05073a..., honest-history status 7877f4a0..., all 8 raw replay files
sha-pinned), cross-checked against the published batch-36 kit pins
(manifest f4a6d53f..., batch3_batch_keys/batch3_status pins inside
batch-keys-b36.json, and the byte-clones in the kit sources/batch3-packet),
and the adopted rows are verified two-pass fresh-cold node-exact at the
decisive budget 15,000,000.
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
MERGER = EXP / "scripts/s5_union_merge.py"

DZ_EXP = "n11-centralreply-b4loss1-b36loss40-b37loss46-adoption-reaudit-20261125"
BASE_CACHE = ROOT / "research/experiments" / DZ_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-20261125.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
KIT36_DIR = ROOT / "research/experiments/n11-centralreply-closure-class20421-batch36-20261124"
B3_DIR = ROOT / "research/experiments/n11-centralreply-closure-class20421-batch-20261122"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9"
BASE_CACHE_ROWS_EXPECTED = 6660
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6502
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"

KIT36_MANIFEST_SHA = "f4a6d53f65694b1393767d562a14266d8bc91b3f255ba23c5d828414adcd0826"
KIT36_FILES = 160
KIT36_KEYS_SHA = "d59182030ce1ade5ad02c8db3836291e2feadfa84325fd4729001e80bfc0c815"
KIT36_STATUS_SHA = "dd8c180b9ad19937634d6ad7d0b0964a08f637d9d3d24dbbeabf198e6f6d74fb"

B3_KEYS_SHA = "ad05073a845e511669d28fde3691fe9f3bf9f08eef2021039c884f1411f6dd3f"
B3_STATUS_SHA = "7877f4a085b466289b7647a1d88b98b755afa2065efae8f59c01bb10dca4cbbb"
BUDGET = 15000000

# --- published batch-3 raw replay files (byte-pinned; direct publication) ----
B3_RAW_SHAS = {
    "d001.p1.out": "90c98d262c63d5905bdb9a8c38836d68e8512327584b355847d6a89b92f44911",
    "d001.p2.out": "90c98d262c63d5905bdb9a8c38836d68e8512327584b355847d6a89b92f44911",
    "d002.p1.out": "339cd483695f7d331dac828d6f6251758156911ce83afd4940fe85707ee69a26",
    "d002.p2.out": "503752d171bae178ac6e354ca1cb250c341a468f372a034d76e60ac8056beb90",
    "d003.p1.out": "e60646680b7d9afd10c6f646ab74ae126bd83505f472d799e329ac3f534f62a0",
    "d003.p2.out": "a26f7c2767542da45327b628cc54357202fccc597de19a87cd9233d8ac32bfe3",
    "d004.p1.out": "0c70397c8e3e42d6034c5ccfc47784a4fef31f847c29d488a77365f022e5d429",
    "d004.p2.out": "6717b2dde4b75198e848252de0bd584e3c55dc0dd72d7297abb2ea0cf02113ab",
}

# --- status.log honest-history pins (5 lines: 4 PASS + 1 WIN-HALT) ------------
B3_STATUS_LINES = 5
B3_STATUS_FIRST = "2026-11-22T03:14:35Z d001 PASS 15000000,2,879510"
B3_STATUS_FINAL = "2026-11-22T03:17:41Z d004 PASS 15000000,2,11969338"
B3_WIN_HALT_LINES = ["2026-11-22T03:16:25Z d002 WIN-HALT"]

# --- adopted packet ----------------------------------------------------------
B3_ADOPTED_IDS = ["d001", "d003", "d004"]
B3_WIN_IDS = ["d002"]
B3_PACKET_IDS = B3_ADOPTED_IDS + B3_WIN_IDS

B3_ADOPTED_NODES = 14962526
B3_PACKET_NODES = 20322520

# --- pinned per-key fields (frozen at packet build; kit-cross-checked) -------
B3_KEY_PINS = {
    "d001": {"lo": 1155173304554754048, "hi": 131072, "legal": 77,
             "s5_index": 38215, "membership_class_count": 4,
             "budget_result_nodes": "15000000,2,879510"},
    "d002": {"lo": 3461016313634230272, "hi": 131072, "legal": 73,
             "s5_index": 197253, "membership_class_count": 4,
             "budget_result_nodes": "15000000,1,5359994"},
    "d003": {"lo": 1155173579298443264, "hi": 131072, "legal": 86,
             "s5_index": 259023, "membership_class_count": 4,
             "budget_result_nodes": "15000000,2,2113678"},
    "d004": {"lo": 5766859322847924224, "hi": 131072, "legal": 86,
             "s5_index": 300778, "membership_class_count": 4,
             "budget_result_nodes": "15000000,2,11969338"},
}

ADOPTED_TABLE_DIGEST = "6c713953b96bb8f98d1a9146c53d90342395042a5aab1f0731273678d82b9036"
ADOPTED_INCREMENT_SHA = "94da84da8116bb89457b32b0b72cbcb667406b75ee1a0b4d76107b9b05df9859"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sys_exit(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_replay(path: Path):
    row = None
    rows_seen = 0
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            rows_seen += 1
            row = {
                "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]),
                "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]),
                "lo": parts[9], "hi": parts[10],
            }
    if rows_seen != 1 or row is None:
        sys_exit(f"expected exactly one replay row in {path}")
    return row


def two_pass(rawdir: Path, kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = rawdir / f"{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        psha = sha(p)
        if psha != B3_RAW_SHAS[p.name]:
            sys_exit(f"raw {p.name} sha drift vs the pinned published bytes")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} vs p1 (fresh two-pass node-exact gate)")
    return ref


def parse_status(path: Path, n_lines: int, first: str, final: str,
                  id_prefix: str, win_halt_lines: list):
    lines = path.read_text().splitlines()
    if len(lines) != n_lines:
        sys_exit(f"{path.name} status lines {len(lines)} != {n_lines}")
    if lines[0] != first or lines[-1] != final:
        sys_exit(f"{path.name} status first/final line drift")
    pat = re.compile(rf"^(\S+) ({id_prefix}\d{{3}}) PASS (\d+),(\d+),(\d+)$")
    hw = re.compile(rf"^(\S+) ({id_prefix}\d{{3}}) WIN-HALT$")
    got_pass, win_halt, others = {}, [], []
    for line in lines:
        m = pat.match(line)
        if m:
            kid = m.group(2)
            if kid in got_pass:
                sys_exit(f"{path.name} duplicate verdict row for {kid}")
            got_pass[kid] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        if hw.match(line):
            win_halt.append(line)
            continue
        others.append(line)
    if others:
        sys_exit(f"{path.name} status has EXHAUSTED/RETRY/MISMATCH rows: {others[:3]}")
    if win_halt != win_halt_lines:
        sys_exit(f"{path.name} status WIN-HALT lines != pinned halt history: {win_halt}")
    return got_pass


def _kit_candidates(kit_dir: Path, rel: str) -> list:
    cands = [kit_dir / rel, ROOT / rel]
    stripped = rel.split("research/experiments/", 1)[-1]
    stripped = stripped[stripped.index("/") + 1:] if stripped.startswith("n11") else stripped
    cands.append(kit_dir / stripped)
    cands.append(kit_dir / "output" / stripped)
    return cands


def verify_kit(dirp: Path, manifest_sha: str, kit_files: int):
    if not dirp.is_dir():
        sys_exit(f"kit dir missing {dirp}")
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        sys_exit(f"kit {dirp.name} MANIFEST sha drift")
    verified = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 4:  # batch-36 format: sha blobsha size relpath
            want, rel = fields[0], fields[3]
        else:                 # batch-37 format: sha relpath
            want, rel = fields[0], fields[1]
        p = None
        for cand in _kit_candidates(dirp, rel):
            if cand.is_file():
                p = cand
                break
        if p is None:
            sys_exit(f"kit {dirp.name} file missing: {rel} (resolved candidates tried)")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def main() -> None:
    # --- base cache, merger, quarantine anchors -------------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part DZ canonical) sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")
    if sha(QUARANTINE) != QUARANTINE_SHA_EXPECTED:
        sys_exit("quarantine registry sha drift")
    base_keys = {}
    wins = losss = 0
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
            if int(row[4]) == 1:
                wins += 1
            elif int(row[4]) == 2:
                losss += 1
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    if wins != BASE_CACHE_WIN_EXPECTED or losss != BASE_CACHE_LOSS_EXPECTED:
        sys_exit(f"base cache WIN/LOSS {wins}/{losss} != pinned")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    # --- kit36 integrity (pins the batch-3 packet through its selection kit) --
    k36 = verify_kit(KIT36_DIR, KIT36_MANIFEST_SHA, KIT36_FILES)
    if sha(KIT36_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("jsreplay.js sha drift in kit batch-36 (pinned solver image 8458...)")
    if sha(KIT36_DIR / "input/batch-keys-b36.json") != KIT36_KEYS_SHA:
        sys_exit("batch-36 keys sha drift")
    if sha(KIT36_DIR / "output/status.log") != KIT36_STATUS_SHA:
        sys_exit("batch-36 status.log sha drift")

    # --- published batch-3 packet integrity -----------------------------------
    if sha(B3_DIR / "input/batch-keys.json") != B3_KEYS_SHA:
        sys_exit("batch-3 packet keys sha drift")
    if sha(B3_DIR / "output/status.log") != B3_STATUS_SHA:
        sys_exit("batch-3 packet status sha drift")
    b3keys = json.loads((B3_DIR / "input/batch-keys.json").read_text())
    if len(b3keys["keys"]) != 49 or b3keys["schema"] != "n11-centralreply-closure-class20421-batch-input-v1":
        sys_exit("batch-3 packet keys schema/count drift")
    by_b3 = {e["key_id"]: e for e in b3keys["keys"]}
    for kid, pins in B3_KEY_PINS.items():
        e = by_b3.get(kid)
        if e is None:
            sys_exit(f"batch-3 packet keys missing {kid}")
        for f in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if int(e[f]) != int(pins[f]):
                sys_exit(f"batch-3 {kid}: {f} drift vs the pinned key fields")
    # kit cross-checks: the batch-36 kit frozen pins + byte-clones must agree
    bk36 = json.loads((KIT36_DIR / "input/batch-keys-b36.json").read_text())
    if bk36["pins"]["batch3_batch_keys"] != B3_KEYS_SHA or bk36["pins"]["batch3_status"] != B3_STATUS_SHA:
        sys_exit("batch-36 kit batch-3 packet pin drift")
    got36u = {e["key_id"]: e["budget_result_nodes"]
              for e in bk36["probed_unconsumed_same_class"]}
    if got36u != {kid: pins["budget_result_nodes"] for kid, pins in B3_KEY_PINS.items()}:
        sys_exit("batch-36 kit probed-unconsumed batch-3 honest label drift")
    clone_keys = KIT36_DIR / "sources/batch3-packet/batch-keys.json"
    clone_status = KIT36_DIR / "sources/batch3-packet/status.log"
    if not clone_keys.is_file() or not clone_status.is_file():
        sys_exit("batch-36 kit sources/batch3-packet byte-clones missing")
    if (clone_keys.read_bytes() != (B3_DIR / "input/batch-keys.json").read_bytes()
            or clone_status.read_bytes() != (B3_DIR / "output/status.log").read_bytes()):
        sys_exit("published batch-3 packet != batch-36 kit byte-clone")

    # --- status log (honest history) -------------------------------------------
    st3 = parse_status(B3_DIR / "output/status.log", B3_STATUS_LINES,
                       B3_STATUS_FIRST, B3_STATUS_FINAL, "d", B3_WIN_HALT_LINES)
    if set(st3) != {"d001", "d002", "d003", "d004"}:
        sys_exit("batch-3 status verdict keys != {d001..d004}")
    for kid in B3_PACKET_IDS:
        b, r, n = (int(x) for x in B3_KEY_PINS[kid]["budget_result_nodes"].split(","))
        if st3[kid] != (b, r, n):
            sys_exit(f"batch-3 {kid} status verdict vs pinned honest label drift")

    # --- two-pass raw verification (all 4 probed keys, adopted + WIN) ---------
    raws = {}
    for kid in B3_PACKET_IDS:
        ref = two_pass(B3_DIR / "output/raw", kid)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["budget"] != BUDGET:
            sys_exit(f"{kid}: budget drift (expected decisive 15M)")
        e = by_b3[kid]
        if (ref["legal"] != int(e["legal"])
                or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"])):
            sys_exit(f"{kid}: legal/key disagreement raw vs packet keys")
        if (ref["budget"], ref["result"], ref["nodes"]) != st3[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        raws[kid] = ref
    loss_set = sorted(k for k in B3_PACKET_IDS if raws[k]["result"] == 2)
    win_set = sorted(k for k in B3_PACKET_IDS if raws[k]["result"] == 1)
    exh_set = sorted(k for k in B3_PACKET_IDS if raws[k]["result"] == 0)
    if loss_set != sorted(B3_ADOPTED_IDS):
        sys_exit(f"batch-3 decisive LOSS set != the adopted candidates: {loss_set}")
    if win_set != sorted(B3_WIN_IDS):
        sys_exit(f"batch-3 probe-level WIN set != the pinned unconsumed WIN: {win_set}")
    if exh_set:
        sys_exit(f"batch-3 probe-level EXHAUSTED set non-empty: {exh_set}")
    n = sum(raws[k]["nodes"] for k in B3_ADOPTED_IDS)
    if n != B3_ADOPTED_NODES:
        sys_exit(f"batch-3 adopted node total drift {n} != {B3_ADOPTED_NODES}")
    p = sum(raws[k]["nodes"] for k in B3_PACKET_IDS)
    if p != B3_PACKET_NODES:
        sys_exit(f"batch-3 whole-packet node total drift {p} != {B3_PACKET_NODES}")

    adopted_rows = [(int(raws[k]["lo"]), int(raws[k]["hi"]), int(raws[k]["legal"]),
                     raws[k]["result"], raws[k]["nodes"]) for k in B3_ADOPTED_IDS]
    if len(adopted_rows) != 3:
        sys_exit(f"adopted rows {len(adopted_rows)} != 3")
    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes in sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- freshness: BASE / quarantine / distinct -------------------------------
    emitted = set()
    for kid in B3_PACKET_IDS:
        key = (int(raws[kid]["lo"]), int(raws[kid]["hi"]))
        if key in emitted:
            sys_exit(f"{kid}: duplicate key across the probed packet")
        emitted.add(key)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE {key}; fresh-increment gate")
    for kid in B3_WIN_IDS:
        if raws[kid]["result"] != 1:
            sys_exit(f"{kid}: unconsumed WIN row result drift")

    # --- emit increment + manifest ---------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure 3-LOSS (batch-3) canonical-adoption increment",
        "#   (Part EB, 2026-11-25) - single pool, loss-only, fresh increment:",
        "#   batch-3 (class 20421 packet, 2026-11-22, probed 4 keys) d001/d003/d004",
        "#     LOSS; d002 WIN unconsumed (scrutiny-owner C++ gate 9193f5b6...).",
        "# 2-pass fresh-cold node-exact exact-S5 verdicts at decisive budget 15M;",
        "#   packet raws published (8 files) with '# replay_done' on both passes;",
        "#   batch-36 kit pins (batch3_batch_keys ad05073a... / batch3_status",
        "#   7877f4a0...) cross-verified against the published packet bytes;",
        "#   adopted per-pass node total 14962526 (whole probed packet 20322520).",
        "# Loss-only adoption asserts no root verdict, frees no class,",
        "#   excludes no class; scheduling effects are derived only by the",
        "#   reaudit refresh (Board fail-closed child verification) and the",
        "#   delta extractor.  11x11 stays UNKNOWN; nodes are bookkeeping,",
        "#   never verdicts.",
    ]
    rows_for_sort = [(lo, hi, nodes) for lo, hi, legal, result, nodes in adopted_rows]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned {ADOPTED_INCREMENT_SHA}")
    incr_path = OUT / "increment-b3loss3-20261125.cache"
    incr_path.write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes}
        for lo, hi, legal, result, nodes in sorted(adopted_rows)]

    manifest = {
        "schema": "b3loss3-increments-manifest-v1",
        "batches": [
            {"pool": "b3",
             "adopted_loss_ids": list(B3_ADOPTED_IDS),
             "probed_ids": list(B3_PACKET_IDS),
             "unadopted_win_ids": list(B3_WIN_IDS),
             "exhausted_excluded_ids": [],
             "adopted_nodes_per_pool": B3_ADOPTED_NODES,
             "whole_packet_nodes": B3_PACKET_NODES,
             "input_sha256": B3_KEYS_SHA,
             "status_log_sha256": B3_STATUS_SHA,
             "status_log_lines": B3_STATUS_LINES,
             "status_log_first_line": B3_STATUS_FIRST,
             "status_log_final_line": B3_STATUS_FINAL,
             "status_log_win_halt_lines": list(B3_WIN_HALT_LINES),
             "kit_integrity": {
                 "kit_manifest_sha256": KIT36_MANIFEST_SHA,
                 "kit_files_verified": k36,
                 "raw_file_sha256_pins": B3_RAW_SHAS,
                 "note": "the batch-3 packet raws are PUBLISHED (8 files, "
                         "byte-pinned above; fetch-verified); integrity holds "
                         "via the published packet bytes plus the batch-36 kit "
                         "pins (batch3_batch_keys ad05073a... / batch3_status "
                         "7877f4a0...) and the kit sources byte-clone"}},
        ],
        "resolved_ids": list(B3_ADOPTED_IDS),
        "loss_ids": list(B3_ADOPTED_IDS),
        "win_ids": list(B3_WIN_IDS),
        "unadopted_win_ids": list(B3_WIN_IDS),
        "unadopted_win_rows": [
            {"pool": "b3", "key_id": kid,
             "lo": int(raws[kid]["lo"]), "hi": int(raws[kid]["hi"]),
             "verdict": "WIN", "nodes": raws[kid]["nodes"],
             "status": "probe-level WIN, consumed NOWHERE (scrutiny-owner C++ gate 9193f5b6...)"}
            for kid in B3_WIN_IDS],
        "exhausted_excluded_ids": [],
        "exhausted_rows": [],
        "row_counts": {
            "adopted_loss_rows": 3,
            "wins_unconsumed": 1,
            "exhausted_excluded": 0,
            "prior_adopted_loss_rows": 0,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note":
            "one probe-level WIN row (batch-3 d002, s5 197253) stays UNCONSUMED "
            "and belongs to the scrutiny-owner C++ second-implementation gate "
            "pin 9193f5b6...; loss-only adoption NEVER frees class 20421 "
            "(5 Part-DZ probe-level WIN children {d008,d009,d021,d026,d029} "
            "plus d002 remain) nor class 16371 (2 WIN children remain)",
        "full_packet_eq_loss_only_rationale":
            "the probed batch-3 packet is probe-complete at budget 15M but is "
            "NOT loss-only: the d002 probe-level WIN row stays UNCONSUMED and "
            "NOT adopted; the adopted packet is the 3 fresh LOSS rows plus "
            "nothing else; no packet row was adopted before (fresh-increment "
            "gate against BASE 4a30b88d...)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 3-LOSS adoption increment: only the 3 fresh batch-3 LOSS "
            "rows are consumed into the canonical cache via the fail-closed "
            "union merger; the d002 probe-level WIN is consumed NOWHERE (no "
            "verdict claim, no exclusion claim) and belongs to the scrutiny "
            "owner's C++ second-implementation gate; nodes are bookkeeping, "
            "never verdicts; the standard 11x11 empty board stays UNKNOWN; no "
            "class is freed or excluded by this Part",
        "provenance": {
            "batch36_kit_files": k36,
            "batch3_status_lines": B3_STATUS_LINES,
            "batch3_raws_published": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_total_nodes_per_pass": B3_ADOPTED_NODES,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
