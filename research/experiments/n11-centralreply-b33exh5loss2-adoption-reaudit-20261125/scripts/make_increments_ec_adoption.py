"""Build the b33exh5loss2 (Part EA af003/af039 30M-resolved) canonical-adoption
increment, fail-closed.

Part EC (2026-11-25).  BASE = the published Part EB canonical merged cache
(6,663 rows, sha c3026468...; WIN 158 / LOSS 6,505).  The single adopted pool
is the published Part EA b33exh5 30M reprobe (class 34908, 2026-11-25): exactly
the 2 fresh LOSS rows af003 (s5 153030) / af039 (s5 950512), resolved at the
pre-declared higher budget condition 30,000,000 where both keys were published
EXHAUSTED (honest UNKNOWN) at 15M in the batch-33 packet; the probe-level WIN
rows af023 / af048 are consumed NOWHERE (scrutiny-owner C++ second-
implementation gate pin 9193f5b6...); af034 stays EXHAUSTED at the 30M
condition and is excluded from adoption (same-condition re-probe forbidden).
No WIN verdict is consumed; no root verdict is asserted; 11x11 stays UNKNOWN.

Every gate is fail-closed: any drift aborts with rc=1 and no output is
written.  The published Part EA kit (61 files, MANIFEST 42ba81bc...) is
verified file-by-file, the adopted rows are verified two-pass fresh-cold
node-exact at budget 30M against the published raw replay files and the
honest-history status log (13 lines), the published 15M EXHAUSTED source raws
of both keys are pinned (budget-condition upgrade, previously unresolved), and
both keys are proven absent from BASE (fresh-increment gate) and from the
quarantine registry.
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

EB_EXP = "n11-centralreply-b3loss3-adoption-reaudit-20261125"
EA_EXP = "n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125"
BASE_CACHE = ROOT / "research/experiments" / EB_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-20261125.cache"
EA_DIR = ROOT / "research/experiments" / EA_EXP
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "c3026468c74b56e71f3a9e0cd45c13e4a8cba147d137c25703c5be62b9c4c94e"
BASE_CACHE_ROWS_EXPECTED = 6663
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6505
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

EA_MANIFEST_SHA = "42ba81bc79dd887074dbc9514b87f0c9d1a656d53a98ff3dfef29b9c4666601e"
EA_KIT_FILES = 61
EA_REPROBE_KEYS_SHA = "3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663"
EA_STATUS_SHA = "db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438"
EA_AUDIT_SHA = "5b83d166e0fb7842a0cad949404c572ba666b71a4cd87dd9e704ce97e543cff3"
EA_BATCH_KEYS_SHA = "8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa"
EA_BATCH_KEYS_SCHEMA = "n11-centralreply-closure-class34908-batch33-input-v1"
EA_BATCH_KEYS_COUNT = 54
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNBATCH_SHA_EXPECTED = "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84"
RUNNER30M_SHA_EXPECTED = "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4"
B33_STATUS_SHA = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"
BUDGET = 30000000
BUDGET_15M = 15000000

# --- published Part EA 30M re-probe raw replay files (byte-pinned) ----------
EA_RAW_SHAS = {
    "af003.p1.out": "5fd8731437146e310992441aa16eb473920cb5cffc87cbf6d758eaba8adb7123",
    "af003.p2.out": "cda10962c1ee55efb58de00742c727df14ee99a5c96e9d8da5c4a7ef9c103cf6",
    "af023.p1.out": "fe118851a927944328a62387d0410a596713c87f1360dda662c97f87913c1dbe",
    "af023.p2.out": "af02e38b07a7f1da9af28c0af7985eaa0cdd97ec2884298ede3a831b19c9198b",
    "af029.p1.out": "1726ecb6d8199d612130d3c2cae12b176102fef0468263cbc1397f525eb0aa66",
    "af029.p2.out": "c937f8964385b2e4c74c1f1d417cdb113b2548dca33c3e0604facea7d9c905a6",
    "af034.p1.out": "9ecfdc770c0b8a6eab027c097051ae2731ee15f1ede0babbc619e38acf2fca74",
    "af034.p2.out": "3978990d5821850476e7b38d1de98fbe7a56738cfd48a8b03cf8ed3350d1b290",
    "af039.p1.out": "9325c7c555823b9a7479442c66cd0b174b3e45cc8b6621b5dc4f45af21de8286",
    "af039.p2.out": "9325c7c555823b9a7479442c66cd0b174b3e45cc8b6621b5dc4f45af21de8286",
    "af048.p1.out": "ae8df6ad6f922669f285f1c2a20d7fa09453c2ef38f64f1b4b878c3034e9d07a",
    "af048.p2.out": "e2056ca26533124e20d3538eebc5e6c4b752be21b92e9e3780c5a0040f0bb620",
    "af001.p1.out": "c2bc73f6a5d88720e33fc3fb498ab16f2d541d7cad62248ef8d04b5f9351381d",
    "af001.p2.out": "e4614f6bd7d4f20cfdd7dba3362e6db52328827a120b9d379fdd2accbdbf1681",
}

# --- published batch-33 15M EXHAUSTED source raws of the 2 adopted keys ------
EA_EXH15M_SHAS = {
    "af003.p1.out": "fdd1e84dc9b5a4e9cd49c6d26c33d208ac9f3f89125594426606f5fba15d597a",
    "af003.p2.out": "4ef154cba92ba078bd31f68ba1643c22518057243bdeb00e53894b5840e41225",
    "af039.p1.out": "a04e23ea9bd1914c997dfb26b820ce793572d2c96e9aebbae7ce283a59281331",
    "af039.p2.out": "aaaaef87ff9406f8f49ea395a9d6513379636e5c2491ce9d4b95fbc7d5ef3abe",
}

# --- status.log honest-history pins (13 lines) ------------------------------
EA_STATUS_LINES = 13
EA_STATUS_FIRST = "2026-11-25T02:33:51Z af001 PASS 30000000,2,2952432"
EA_STATUS_FINAL = "2026-11-25T03:00:04Z af048 WIN-HALT"
EA_STATUS_WIN_HALT_LINES = [
    "2026-11-25T02:34:39Z af029 WIN-HALT",
    "2026-11-25T02:46:09Z af023 WIN-HALT",
    "2026-11-25T03:00:04Z af048 WIN-HALT",
]
EA_STATUS_RETRY_LINES = [
    "2026-11-25T02:43:31Z af023 P2-TRUNCATED-RETRY",
    "2026-11-25T02:50:34Z af034 P2-TRUNCATED-RETRY",
]
EA_STATUS_EXHAUSTED_LINES = [
    "2026-11-25T02:53:19Z af034 EXHAUSTED 30000000,0,30000000",
]

# --- adopted packet ----------------------------------------------------------
ADOPTED_IDS = ["af003", "af039"]
WIN_IDS_UNCONSUMED = ["af023", "af048"]
EXHAUSTED_EXCLUDED_IDS = ["af034"]
PACKET_IDS = ["af003", "af023", "af034", "af039", "af048"]
ANCHOR_IDS = ["af001", "af029"]

ADOPTED_NODES = 42360304
PACKET_NODES = 119110099

# --- pinned per-key fields (frozen at Part EA packet build; kit-crosschecked) -
KEY_PINS = {
    "af001": {"lo": 1152921504742113281, "hi": 68719476736, "legal": 91,
              "s5_index": 1176, "membership_class_count": 2},
    "af003": {"lo": 3458764513821589505, "hi": 68719476736, "legal": 93,
              "s5_index": 153030, "membership_class_count": 3},
    "af023": {"lo": 1152921504607895553, "hi": 68719478784, "legal": 94,
              "s5_index": 810351, "membership_class_count": 4},
    "af029": {"lo": 1152921504607895553, "hi": 68720525312, "legal": 86,
              "s5_index": 900646, "membership_class_count": 2},
    "af034": {"lo": 1152921504607911937, "hi": 68719476736, "legal": 95,
              "s5_index": 930660, "membership_class_count": 4},
    "af039": {"lo": 1152921504607895681, "hi": 68719476736, "legal": 89,
              "s5_index": 950512, "membership_class_count": 4},
    "af048": {"lo": 1152921508902862849, "hi": 68719476736, "legal": 87,
              "s5_index": 962172, "membership_class_count": 3},
}
LABEL_PINS = {
    "af001": (2, 2952432),      # 30M re-run anchor, node-exact vs published 15M
    "af003": (2, 23126072),    # ADOPTED
    "af023": (1, 28933179),    # probe-level WIN, unconsumed
    "af029": (1, 4862485),     # 30M re-run anchor, node-exact vs published 15M
    "af034": (0, 30000000),    # EXHAUSTED at 30M, honest UNKNOWN, excluded
    "af039": (2, 19234232),    # ADOPTED
    "af048": (1, 17816616),    # probe-level WIN, unconsumed
}
PUBLISHED_15M_EXHAUSTED = {
    "af003": (0, 15000000),
    "af039": (0, 15000000),
}

ADOPTED_TABLE_DIGEST = "7c74832f57c9b54a6b5606880ee8c40b7d563ad518cc04e96ef257b543172182"
ADOPTED_INCREMENT_SHA = "8f45a202af94faa448ac5f39f061100e3370ce9397c475c98f75cc9ea30d04a1"


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


def two_pass(rawdir: Path, kid: str, shas: dict):
    variants = {}
    for tag in ("p1", "p2"):
        p = rawdir / f"{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        psha = sha(p)
        if psha != shas[p.name]:
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
        if len(fields) >= 4:  # 4-column format: sha blobsha size relpath
            want, rel = fields[0], fields[3]
        else:                 # Part EA format: sha blobsha relpath
            want, rel = fields[0], fields[2]
        p = dirp / rel
        if not p.is_file():
            sys_exit(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def parse_status(path: Path):
    lines = path.read_text().splitlines()
    if len(lines) != EA_STATUS_LINES:
        sys_exit(f"{path.name} status lines {len(lines)} != {EA_STATUS_LINES}")
    if lines[0] != EA_STATUS_FIRST or lines[-1] != EA_STATUS_FINAL:
        sys_exit(f"{path.name} status first/final line drift")
    pat = re.compile(r"^(\S+) (af\d{3}) PASS (\d+),(\d+),(\d+)$")
    hw = re.compile(r"^(\S+) (af\d{3}) WIN-HALT$")
    rt = re.compile(r"^(\S+) (af\d{3}) P2-TRUNCATED-RETRY$")
    ex = re.compile(r"^(\S+) (af\d{3}) EXHAUSTED (\d+),(\d+),(\d+)$")
    got_pass, win_halt, retry, exh, others = {}, [], [], [], []
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
        if rt.match(line):
            retry.append(line)
            continue
        if ex.match(line):
            exh.append(line)
            continue
        others.append(line)
    if others:
        sys_exit(f"{path.name} status has UNEXPECTED rows: {others[:3]}")
    if win_halt != EA_STATUS_WIN_HALT_LINES:
        sys_exit(f"{path.name} status WIN-HALT lines != pinned halt history: {win_halt}")
    if retry != EA_STATUS_RETRY_LINES:
        sys_exit(f"{path.name} status P2-TRUNCATED-RETRY lines != pinned retry history: {retry}")
    if exh != EA_STATUS_EXHAUSTED_LINES:
        sys_exit(f"{path.name} status EXHAUSTED lines != pinned exhaustion history: {exh}")
    if sorted(re.match(r"^(\S+) (af\d{3})", l).group(2) for l in exh) != EXHAUSTED_EXCLUDED_IDS:
        sys_exit(f"{path.name} EXHAUSTED key set != the pinned excluded set")
    return got_pass


def main() -> None:
    # --- base cache, merger, quarantine anchors -------------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EB canonical) sha drift")
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

    # --- Part EA kit integrity (the published b33exh5 re-probe kit) -----------
    ea_files = verify_kit(EA_DIR, EA_MANIFEST_SHA, EA_KIT_FILES)
    if sha(EA_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("jsreplay.js sha drift in the Part EA kit (pinned solver image 8458...)")
    if sha(EA_DIR / "scripts/runbatch.sh") != RUNBATCH_SHA_EXPECTED:
        sys_exit("runbatch.sh sha drift in the Part EA kit (pinned 15M runner f591...)")
    if sha(EA_DIR / "scripts/runbatch_afexh5-30m.sh") != RUNNER30M_SHA_EXPECTED:
        sys_exit("derived 30M runner sha drift in the Part EA kit (pinned 3b50...)")
    if sha(EA_DIR / "input/reprobe-keys.json") != EA_REPROBE_KEYS_SHA:
        sys_exit("Part EA reprobe-keys sha drift")
    if sha(EA_DIR / "output/status.log") != EA_STATUS_SHA:
        sys_exit("Part EA status.log sha drift")
    if sha(EA_DIR / "output/audit.json") != EA_AUDIT_SHA:
        sys_exit("Part EA audit.json sha drift")
    if sha(EA_DIR / "input/batch-keys.json") != EA_BATCH_KEYS_SHA:
        sys_exit("batch-33 packet keys sha drift")
    if sha(EA_DIR / "sources/b33-status.log") != B33_STATUS_SHA:
        sys_exit("published batch-33 honest-history status sha drift (source 1f66...)")

    # --- reprobe-keys + batch-keys structure ----------------------------------
    rk = json.loads((EA_DIR / "input/reprobe-keys.json").read_text())
    if rk["schema"] != "n11-centralreply-c34908-b33exh5-reprobe30m-input-v1" \
            or int(rk["class_index"]) != 34908 or int(rk["batch"]) != 33:
        sys_exit("reprobe-keys schema/class/batch drift")
    if rk["reprobe_condition"]["budget"] != BUDGET \
            or rk["reprobe_condition"]["derived_runner_sha256"] != RUNNER30M_SHA_EXPECTED:
        sys_exit("reprobe-condition budget/runner pin drift")
    if rk["source_condition"]["budget"] != BUDGET_15M \
            or sorted(rk["source_condition"]["published_b33_status"]
                      ["target_remaining_exhausted_set"]) != sorted(PACKET_IDS) \
            or rk["source_condition"]["published_b33_status"]["lines"] != 66:
        sys_exit("source-condition 15M honest-history pin drift (5 EXHAUSTED targets / 66 lines)")
    rk_by = {e["key_id"]: e for e in rk["keys"]}
    if sorted(rk_by) != sorted(PACKET_IDS):
        sys_exit("reprobe-keys target set != the 5 EXHAUSTED re-probe targets")
    for kid in PACKET_IDS:
        e = rk_by[kid]
        pins = KEY_PINS[kid]
        for f in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if int(e[f]) != int(pins[f]):
                sys_exit(f"reprobe-keys {kid}: {f} drift vs the pinned key fields")
        if kid in ("af003", "af039"):
            if e["published_15m"]["raw_p1_sha256"] != EA_EXH15M_SHAS[f"{kid}.p1.out"] \
                    or e["published_15m"]["raw_p2_sha256"] != EA_EXH15M_SHAS[f"{kid}.p2.out"]:
                sys_exit(f"reprobe-keys {kid} 15M raw pin drift")
        if (int(e["published_15m"]["result"]), int(e["published_15m"]["nodes"])) \
                != PUBLISHED_15M_EXHAUSTED.get(kid, (0, 15000000)):
            sys_exit(f"reprobe-keys {kid} published-15M exhaustion label drift")
    bk = json.loads((EA_DIR / "input/batch-keys.json").read_text())
    if bk["schema"] != EA_BATCH_KEYS_SCHEMA or len(bk["keys"]) != EA_BATCH_KEYS_COUNT \
            or int(bk["class_index"]) != 34908:
        sys_exit("batch-33 packet keys schema/class/count drift")
    bk_by = {e["key_id"]: e for e in bk["keys"]}
    for kid, pins in KEY_PINS.items():
        e = bk_by.get(kid)
        if e is None:
            sys_exit(f"batch-33 packet keys missing {kid}")
        for f in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if int(e[f]) != int(pins[f]):
                sys_exit(f"batch-33 {kid}: {f} drift vs the pinned key fields")

    # --- audit.json honesty pins ----------------------------------------------
    audit = json.loads((EA_DIR / "output/audit.json").read_text())
    if audit["schema"] != "n11-centralreply-c34908-b33exh5-reprobe30m-audit-v1" \
            or int(audit["class_index"]) != 34908 or int(audit["batch"]) != 33 \
            or audit["reprobe_budget"] != BUDGET or audit["keys_total"] != 5 \
            or audit["probed"] != 5 or audit["mismatches"] != 0:
        sys_exit("audit.json header pin drift")
    if sorted(audit["resolved_loss_rows"]) != sorted(ADOPTED_IDS):
        sys_exit("audit resolved_loss_rows != the adopted 2-set")
    if sorted(audit["resolved_win_rows"]) != sorted(WIN_IDS_UNCONSUMED):
        sys_exit("audit resolved_win_rows != the unconsumed WIN 2-set")
    if audit["still_exhausted_rows"] != EXHAUSTED_EXCLUDED_IDS \
            or audit["window_exceeded_rows"] or audit["unprobed_rows"]:
        sys_exit("audit still-exhausted/window-unprobed rows drift")
    if not audit["loss_rows_are_adoption_candidates_only"]:
        sys_exit("audit adoption-candidate-only flag must be true")
    for kid in ANCHOR_IDS:
        a = audit["anchors"].get(kid)
        if a is None or not a["node_exact_vs_published"]:
            sys_exit(f"audit anchor {kid} node-exact flag drift")
        if (a["result"], a["nodes"]) != LABEL_PINS[kid]:
            sys_exit(f"audit anchor {kid} label drift")
    for name, v in audit["val_gate_fresh"].items():
        if not v["node_exact"]:
            sys_exit(f"audit val-gate {name} node-exact flag drift")
    if audit["input_sha256"] != EA_REPROBE_KEYS_SHA:
        sys_exit("audit input_sha256 pin drift")

    # --- status log (honest history, 13 lines) --------------------------------
    st = parse_status(EA_DIR / "output/status.log")
    if sorted(st) != sorted(PACKET_IDS + ANCHOR_IDS):
        sys_exit("Part EA status verdict keys != the 5 targets + 2 anchors")
    for kid, (r, n) in LABEL_PINS.items():
        if st[kid] != (BUDGET, r, n):
            sys_exit(f"{kid} status verdict vs pinned honest label drift")

    # --- two-pass raw verification (all 5 targets + 2 anchors) -----------------
    raws = {}
    for kid in PACKET_IDS + ANCHOR_IDS:
        ref = two_pass(EA_DIR / "output/raw", kid, EA_RAW_SHAS)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["budget"] != BUDGET:
            sys_exit(f"{kid}: budget drift (expected pre-declared 30M)")
        e = KEY_PINS[kid]
        if (ref["legal"] != int(e["legal"])
                or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"])):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != st[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        raws[kid] = ref
    loss_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 2)
    win_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 1)
    exh_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 0)
    if loss_set != sorted(ADOPTED_IDS):
        sys_exit(f"30M decisive LOSS set != the adopted candidates: {loss_set}")
    if win_set != sorted(WIN_IDS_UNCONSUMED):
        sys_exit(f"30M probe-level WIN set != the pinned unconsumed WINs: {win_set}")
    if exh_set != sorted(EXHAUSTED_EXCLUDED_IDS):
        sys_exit(f"30M still-EXHAUSTED set != the pinned excluded key: {exh_set}")
    n = sum(raws[k]["nodes"] for k in ADOPTED_IDS)
    if n != ADOPTED_NODES:
        sys_exit(f"adopted node total drift {n} != {ADOPTED_NODES}")
    p = sum(raws[k]["nodes"] for k in PACKET_IDS)
    if p != PACKET_NODES:
        sys_exit(f"whole-packet node total drift {p} != {PACKET_NODES}")

    # --- 15M EXHAUSTED source raws of the 2 adopted keys (condition upgrade) --
    for kid in ADOPTED_IDS:
        ref15 = two_pass(EA_DIR / "sources/exh15m", kid, EA_EXH15M_SHAS)
        if ref15["budget"] != BUDGET_15M or ref15["result"] != 0 \
                or ref15["nodes"] != BUDGET_15M:
            sys_exit(f"{kid}: 15M source raw must be the published EXHAUSTED honest-UNKNOWN run")
        if (ref15["lo"], ref15["hi"], ref15["legal"]) != (raws[kid]["lo"], raws[kid]["hi"], raws[kid]["legal"]):
            sys_exit(f"{kid}: 15M source raw key/legal disagreement vs the 30M raw")

    # --- b33-status.log honest history (66 lines; 5 EXHAUSTED pairs pinned) ---
    b33_lines = (EA_DIR / "sources/b33-status.log").read_text().splitlines()
    if len(b33_lines) != 66:
        sys_exit(f"b33-status lines {len(b33_lines)} != 66")
    for kid in PACKET_IDS:
        pair = [l for l in b33_lines
                if (f" {kid} PASS {BUDGET_15M},0,{BUDGET_15M}" in l)
                or (f" {kid} EXHAUSTED {BUDGET_15M},0,{BUDGET_15M}" in l)]
        if len(pair) != 2:
            sys_exit(f"b33-status EXHAUSTED pair for {kid} not found (15M honest history)")

    adopted_rows = [(int(raws[k]["lo"]), int(raws[k]["hi"]), int(raws[k]["legal"]),
                     raws[k]["result"], raws[k]["nodes"]) for k in ADOPTED_IDS]
    if len(adopted_rows) != 2 or any(r[3] != 2 for r in adopted_rows):
        sys_exit("adopted rows must be exactly the 2 fresh exact-LOSS rows")
    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes in sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- freshness: BASE / quarantine / distinct -------------------------------
    emitted = set()
    for kid in PACKET_IDS:
        key = (int(raws[kid]["lo"]), int(raws[kid]["hi"]))
        if key in emitted:
            sys_exit(f"{kid}: duplicate key across the probed packet")
        emitted.add(key)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE {key}; fresh-increment gate")
    for kid in ANCHOR_IDS:
        key = (int(raws[kid]["lo"]), int(raws[kid]["hi"]))
        if key in quarantined:
            sys_exit(f"{kid}: quarantined anchor key {key}")
    # anchor identity gates: af001 is the published batch-33 exact-LOSS row
    # already adopted into BASE (node-exact reproduction expected); af029 is
    # the unconsumed batch-33 probe-level WIN (must sit in NO cache).
    key_af001 = (int(raws["af001"]["lo"]), int(raws["af001"]["hi"]))
    if base_keys.get(key_af001) != (2, 2952432):
        sys_exit(f"af001 anchor must reproduce the published BASE row verbatim: {base_keys.get(key_af001)}")
    key_af029 = (int(raws["af029"]["lo"]), int(raws["af029"]["hi"]))
    if key_af029 in base_keys:
        sys_exit("af029 anchor is an unconsumed probe-level WIN: must sit in NO cache")
    for kid in WIN_IDS_UNCONSUMED:
        if raws[kid]["result"] != 1:
            sys_exit(f"{kid}: unconsumed WIN row result drift")
    for kid in EXHAUSTED_EXCLUDED_IDS:
        if raws[kid]["result"] != 0:
            sys_exit(f"{kid}: excluded EXHAUSTED row result drift")

    # --- emit increment + manifest ---------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure 2-LOSS (batch-33 EXHAUSTED-resolved 30M reprobe)",
        "#   canonical-adoption increment (Part EC, 2026-11-25) - single pool,",
        "#   loss-only, fresh increment: class-34908 EXHAUSTED-reprobe targets",
        "#   af003 (s5 153030) and af039 (s5 950512) resolved exact LOSS at the",
        "#   pre-declared 30M budget condition (Part EA b33exh5, 2026-11-25); the",
        "#   same packet's probe-level WIN rows af023/af048 stay UNCONSUMED",
        "#   (scrutiny-owner C++ gate 9193f5b6...); af034 stays EXHAUSTED at 30M",
        "#   (honest UNKNOWN, excluded here, same-condition re-probe forbidden).",
        "# 2-pass fresh-cold node-exact exact-S5 verdicts at budget 30M;",
        "#   published raws with '# replay_done' on both passes; the Part EA kit",
        "#   (61 files, MANIFEST 42ba81bc...) verified byte-for-byte; the 15M",
        "#   EXHAUSTED source raws of both keys pinned (budget-condition upgrade,",
        "#   previously unresolved);",
        "#   adopted per-pass node total 42360304 (whole probed 5-target packet",
        "#   119110099).",
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
    incr_path = OUT / "increment-b33exh5loss2-20261125.cache"
    incr_path.write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes}
        for lo, hi, legal, result, nodes in sorted(adopted_rows)]

    manifest = {
        "schema": "b33exh5loss2-increments-manifest-v1",
        "batches": [
            {"pool": "b33exh5",
             "adopted_loss_ids": list(ADOPTED_IDS),
             "probed_ids": list(PACKET_IDS),
             "anchor_ids": list(ANCHOR_IDS),
             "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
             "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
             "adopted_nodes_per_pool": ADOPTED_NODES,
             "whole_packet_nodes": PACKET_NODES,
             "input_sha256": EA_REPROBE_KEYS_SHA,
             "batch_keys_sha256": EA_BATCH_KEYS_SHA,
             "status_log_sha256": EA_STATUS_SHA,
             "status_log_lines": EA_STATUS_LINES,
             "status_log_first_line": EA_STATUS_FIRST,
             "status_log_final_line": EA_STATUS_FINAL,
             "status_log_win_halt_lines": list(EA_STATUS_WIN_HALT_LINES),
             "status_log_retry_lines": list(EA_STATUS_RETRY_LINES),
             "status_log_exhausted_lines": list(EA_STATUS_EXHAUSTED_LINES),
             "reprobe_budget": BUDGET,
             "source_budget": BUDGET_15M,
             "kit_integrity": {
                 "kit_manifest_sha256": EA_MANIFEST_SHA,
                 "kit_files_verified": ea_files,
                 "raw_file_sha256_pins": EA_RAW_SHAS,
                 "exh15m_source_sha256_pins": EA_EXH15M_SHAS,
                 "note": "the Part EA b33exh5 kit raws are PUBLISHED (61 files, "
                         "byte-pinned above; fetch-verified against the kit "
                         "MANIFEST 42ba81bc...); the 2 adopted keys are fresh "
                         "at BASE (EXHAUSTED honest-UNKNOWN at 15M in the "
                         "batch-33 packet, resolved exact LOSS only at the "
                         "pre-declared 30M condition)"}},
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_rows": [
            {"pool": "b33exh5", "key_id": kid,
             "lo": int(raws[kid]["lo"]), "hi": int(raws[kid]["hi"]),
             "verdict": "WIN", "nodes": raws[kid]["nodes"],
             "status": "probe-level WIN, consumed NOWHERE (scrutiny-owner C++ gate 9193f5b6...)"}
            for kid in WIN_IDS_UNCONSUMED],
        "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
        "exhausted_rows": [
            {"pool": "b33exh5", "key_id": kid,
             "lo": int(raws[kid]["lo"]), "hi": int(raws[kid]["hi"]),
             "verdict": "EXHAUSTED", "nodes": raws[kid]["nodes"],
             "status": "still EXHAUSTED at the pre-declared 30M condition; honest "
                       "UNKNOWN, excluded from adoption; same-condition re-probe "
                       "forbidden (a higher-budget re-probe needs a NEW declaration)"}
            for kid in EXHAUSTED_EXCLUDED_IDS],
        "row_counts": {
            "adopted_loss_rows": 2,
            "wins_unconsumed": 2,
            "exhausted_excluded": 1,
            "prior_adopted_loss_rows": 0,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note":
            "two probe-level WIN rows (af023 s5 810351 / af048 s5 962172) stay "
            "UNCONSUMED and belong to the scrutiny-owner C++ second-implementation "
            "gate pin 9193f5b6...; loss-only adoption NEVER frees class 34908 "
            "(6 unconsumed WIN children {af029, af047, af050, af053} plus af023/af048 "
            "remain, plus 1 still-EXHAUSTED af034)",
        "full_packet_eq_loss_only_rationale":
            "the re-probed Part EA packet is probe-complete at the pre-declared "
            "30M condition but is NOT loss-only: 2 probe-level WIN rows and 1 "
            "still-EXHAUSTED row stay UNCONSUMED / excluded; the adopted packet "
            "is the 2 fresh LOSS rows plus nothing else; no packet row was "
            "adopted before (fresh-increment gate against BASE c3026468...)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 2-LOSS adoption increment: only the 2 fresh af003/af039 "
            "exact-LOSS rows are consumed into the canonical cache via the "
            "fail-closed union merger; the af023/af048 probe-level WINs are "
            "consumed NOWHERE (no verdict claim, no exclusion claim) and belong "
            "to the scrutiny owner's C++ second-implementation gate; af034 is "
            "honest UNKNOWN at the 30M condition (excluded); nodes are "
            "bookkeeping, never verdicts; the standard 11x11 empty board stays "
            "UNKNOWN; no class is freed or excluded by this Part",
        "provenance": {
            "ea_kit_files": ea_files,
            "b33_status_lines": 66,
            "b33exh5_status_lines": EA_STATUS_LINES,
            "raws_published": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_total_nodes_per_pass": ADOPTED_NODES,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
