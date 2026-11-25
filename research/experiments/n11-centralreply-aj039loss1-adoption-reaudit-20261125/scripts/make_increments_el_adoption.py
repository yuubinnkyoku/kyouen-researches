"""Build the ek-aj039loss1 (Part EL single-row loss-only) canonical-adoption
increment, fail-closed.

Part EL (2026-11-25).  BASE = the published Part EI canonical merged cache
(6,712 rows, sha 73482be0...; WIN 158 / LOSS 6,554; the b39loss46 canonical
adoption of Part EI).  The adopted pool is the published Part EK aj030/aj039
30M re-probe kit (closure class 30484 honest-EXHAUSTED pair, 42 files,
MANIFEST-sha256 rev2 97574401...): exactly the ONE honest-label exact-LOSS
row aj039 (key (1152922606282735616, 65536), legal 88, s5_index 897668,
nodes 16,549,916), two-pass fresh-cold node-exact at budget 30,000,000
order 0 (pass walls 96 s / 98 s, identical passes, MISMATCH 0), resolved in
(15M, 30M] beyond the honest EXHAUSTED 15M history of batch-39 (NOT a
same-condition re-probe).  The probe-level WIN row aj030 (result 1, nodes
15,284,699, WIN-HALT) is UNCONSUMED everywhere: adoption of WIN verdicts is
scrutiny-owner C++ second-implementation gate 9193f5b6... exclusive and the
aj030 key must sit in NO cache.  The 2 claim-reserved dual-class batch-38
keys (ai044/ai048, Part EF in-flight single-owner) are excluded at pair
level and untouched, as are the batch-39 probe-level WIN rows aj049/aj050
(anchors aside, they sit in NO cache too).  Loss-only canonical adoption:
no WIN verdict is consumed; no root verdict is asserted; 11x11 stays
UNKNOWN.

Every gate is fail-closed: any drift aborts with rc=1 and no output is
written.  The published Part EK kit is verified file-by-file (byte pins
against the published MANIFEST-sha256 rev2), the 10 published raw replay
pairs (two-pass fresh-cold node-exact: aj039, aj030 and the 3 anchors
aj001/aj049/af039), the 7-line honest-history status.log, the machine audit
audit_ek.json (d9aa8aab..., 79/79 gates PASS), the 5 byte-pinned input
rows, the exh15m honest-exhaustion sources and the b39-status honest
history are pinned, the adopted key is proven absent from BASE
(fresh-increment gate) and from the quarantine registry, and every
unconsumed key (WIN aj030, WIN aj049, WIN aj050, claim-reserved ai044/
ai048) is proven absent from BASE and never emitted.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
MERGER = EXP / "scripts/s5_union_merge.py"

EI_EXP = "n11-centralreply-b39loss46-adoption-reaudit-20261125"
EK_EXP = "n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125"
BASE_CACHE = ROOT / "research/experiments" / EI_EXP / (
    "output/merged-exact-s5-chain-plus-b39loss46-20261125.cache")
EK_DIR = ROOT / "research/experiments" / EK_EXP
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70"
BASE_CACHE_ROWS_EXPECTED = 6712
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6554
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

EK_MANIFEST_SHA = "97574401309964806a8eed4968496dcd222aecaf029aa9b1115dcaaa2ec78a68"
EK_KIT_FILES = 42
EK_STATUS_SHA = "868bfbff196343d074c909b0290739a0111f2b3dcfc04967f459528dbab6c01c"
EK_AUDIT_SHA = "d9aa8aab971ca0975caea7e52156bea86b3c183d843a40a8cea44a8dcf54691b"
EK_AUDIT_PY_SHA = "7636def1cc7ca87171a0716e8eb76386ea9965485f28a942a53137439ac4bcfb"
BUDGET = 30000000
EXH_BUDGET = 15000000
STATUS_LINES = 7
STATUS_ALL_LINES = [
    "2026-11-25T14:06:22Z aj049 PASS 30000000,1,4998452",
    "2026-11-25T14:06:22Z aj049 WIN-HALT",
    "2026-11-25T14:06:25Z aj001 PASS 30000000,2,5156075",
    "2026-11-25T14:12:54Z aj030 PASS 30000000,1,15284699",
    "2026-11-25T14:12:54Z aj030 WIN-HALT",
    "2026-11-25T14:13:33Z af039 PASS 30000000,2,19234232",
    "2026-11-25T14:17:28Z aj039 PASS 30000000,2,16549916",
]
STATUS_WIN_HALT_LINES = [
    "2026-11-25T14:06:22Z aj049 WIN-HALT",
    "2026-11-25T14:12:54Z aj030 WIN-HALT",
]
B39_STATUS_SHA = "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea"
B39_EXHAUSTED_LINES = [
    "2026-11-25T09:56:39Z aj030 EXHAUSTED 15000000,0,15000000",
    "2026-11-25T10:06:11Z aj039 EXHAUSTED 15000000,0,15000000",
]

SOURCE_PINS = {
    "b39_status": "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea",
    "canonical_cache_src": "73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70",
    "exh15m_aj030_p1": "843a0a0c976699d937391377455504797f5bece24222eef74d4452f20e20178c",
    "exh15m_aj030_p2": "661c8e410f8e3f93227ac635233556fec5069ccf115117255a38b3b19f551757",
    "exh15m_aj039_p1": "60ae21db0e099b22403b8ce64ba97e15de3987acfafb218d79c11aae6c3b4906",
    "exh15m_aj039_p2": "c51899d50649444c3ee8cbb43f3318392131cc3add8b54cbe77d3f600a59dfbb",
    "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "runbatch_ek_30m": "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4",
    "audit_ek_py": "7636def1cc7ca87171a0716e8eb76386ea9965485f28a942a53137439ac4bcfb",
    "valgate_at2m_first_input": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "valgate_at2m_first_baseline": "6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c",
    "valgate_second_input": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "valgate_at2m_second_baseline": "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "valgate_first15m_baseline": "8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591",
    "valgate_second15m_baseline": "91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb",
    "valgate_at2m_first_host": "2e940c8f5bd1e595827f7958b5094a461f8e137e64062346154c144501a8bdad",
    "valgate_at2m_second_host": "878cbb5c5f08eed0913163ac0a8329e0d9a65fa22a51bc8666c2b7c686a3f1a6",
    "valgate_first15m_host": "d654674d72cf26292af993bd6b9bb745b17902cc047212804c89b589b4f495b5",
    "valgate_second15m_host": "b2aee5684906582f02cefb70ea24f1a9cab5112b945aa59d6d2a31fb0ac19729",
}

ADOPTED_IDS = ["aj039"]
WIN_IDS_UNCONSUMED = ["aj030"]
ANCHOR_IDS = ["aj001", "aj049", "af039"]
PROBED_IDS = ["aj030", "aj039"]
CLAIM_RESERVED_IDS = ["ai044", "ai048"]
CLAIM_RESERVED_PAIRS = {
    "ai044": (1152922604135256064, 65536),
    "ai048": (1152921573327372288, 68157440),
}
# batch-39 probe-level WIN rows, unconsumed, must sit in NO cache
UNCONSUMED_WIN_NO_CACHE = {
    "aj049": (1152921574400065536, 1114112),
    "aj050": (1152921574400065536, 68157440),
}

ADOPTED_NODES_PER_PASS = 16549916
WHOLE_PACKET_NODES_PER_PASS = 31834615  # aj039 16,549,916 + aj030 15,284,699

KEY_PINS = {
    "aj039": {"lo": 1152922606282735616, "hi": 65536, "legal": 88,
              "s5_index": 897668, "probe_order": 578,
              "membership_class_count": 4},
    "aj030": {"lo": 1152922604135251976, "hi": 65536, "legal": 83,
              "s5_index": 892576, "probe_order": 569,
              "membership_class_count": 4},
    "aj001": {"lo": 1152922604269469696, "hi": 65536, "legal": 84,
              "s5_index": 63021},
    "aj049": {"lo": 1152921574400065536, "hi": 1114112, "legal": 80,
              "s5_index": 902511},
    "af039": {"lo": 1152921504607895681, "hi": 68719476736, "legal": 89},
}

LABEL_PINS = {
    "aj039": (2, 16549916),
    "aj030": (1, 15284699),
    "aj001": (2, 5156075),
    "aj049": (1, 4998452),
    "af039": (2, 19234232),
}
EXH_LABEL_PINS = {
    "aj030": (0, 15000000),
    "aj039": (0, 15000000),
}

RAW_SHAS = {
    "aj039.p1.out": "529b3efeefd4c3d2c12988c9254b4a39931405708b707dece56dc9a508863238",
    "aj039.p2.out": "930d0b48063c1b0f18381beaa16d038c1129406539da579b68a8224fa9274dd8",
    "aj030.p1.out": "a0c88b3511d551fec1efa3069a7df59b1291bce2ae4bcb24cdb2bcda70573c7b",
    "aj030.p2.out": "f0eb149af394f79f795186bf714d7da23a22c0df07d7bc2f1e35d6d661613062",
    "aj001.p1.out": "41a6b129005bd360741d89b48be2b3e35bba38d26fa9c08228e4519f2747ade1",
    "aj001.p2.out": "0348aa062d7a488f8d802fcaec18c43dd87faa41089c63f0f78ee9a9922dd5ab",
    "aj049.p1.out": "741f62f999d6944dc5d6151850f9f1960051b56c476ee53fd5b611dae8c49af5",
    "aj049.p2.out": "850df2ae34a0f3e437a83f557e57b8ccca59ab418de54c64fd06beea212b9257",
    "af039.p1.out": "2ba27ad40d2b344491f52e6efc724312ee3f597b9a9d7a8d194c60c6740a2fb4",
    "af039.p2.out": "93b3a25d25b96af4cc27eb6994ece201be6befa1b40722d61b5cf18303019a7e",
}

INPUT_CSV_SHAS = {
    "aj039": "82f8dff3136ce54e33203f69f3589b72891a41129b11f7b0811b4053e9858394",
    "aj030": "520ee52abefaec80b800245dd1913489cd511923732e14d3315f4806aec83595",
    "aj001": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "aj049": "46349391b3aa212cf7ffffbeae94d01b5202f25ca24a6c5294b75ced6184951a",
    "af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
}

ADOPTED_TABLE_DIGEST = "cd77a0d107b99ef7515b3e1f95a0913cfc514a4c2240a8e003743d8db06ebc52"
ADOPTED_INCREMENT_SHA = "7838b08131c5ee5bd8a2819ee8e3bcb4fb9733034f495e7da24b2758890ad36a"

INCREMENT_NAME = "increment-aj039loss1-20261125.cache"
EL_SCHEMA = "ek-aj039loss1-increments-manifest-v1"

HDR_LINES = [
 "# n11 central-reply closure class 30484 aj039loss1",
 "#   canonical-adoption increment (Part EL, 2026-11-25) - loss-only,",
 "#   fresh single-row increment.  The one honest-label exact-LOSS row",
 "#   aj039 (key 1152922606282735616,65536, legal 88, nodes 16,549,916)",
 "#   of the published Part EK 30M re-probe kit (42 published files,",
 "#   MANIFEST-sha256 rev2 97574401...), two-pass fresh-cold node-exact",
 "#   at the pre-declared 30M budget, order 0 (pass walls 96 s / 98 s,",
 "#   MISMATCH 0), resolved in (15M,30M] beyond the honest EXHAUSTED",
 "#   15M history (same-condition re-probe prohibited and NOT performed).",
 "#   The probe-level WIN row aj030 (nodes 15,284,699, WIN-HALT) is",
 "#   consumed NOWHERE (scrutiny-owner C++ second-implementation gate",
 "#   9193f5b6... exclusive); the 2 claim-reserved dual-class batch-38",
 "#   keys (ai044/ai048, Part EF in-flight) untouched; aj049/aj050",
 "#   probe-level WIN rows (batch-39) stay unconsumed.",
 "# Loss-only adoption asserts no root verdict, frees no class,",
 "#   excludes no class; scheduling effects are derived only by the",
 "#   reaudit refresh (Board fail-closed child verification) and the",
 "#   delta extractor.  11x11 stays UNKNOWN; nodes are bookkeeping,",
 "#   never verdicts.",
]


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


def two_pass(raw_dir: Path, kid: str, shas: dict, budget: int):
    variants = {}
    for tag in ("p1", "p2"):
        p = raw_dir / f"{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        psha = sha(p)
        if psha != shas[f"{kid}.{tag}.out"]:
            sys_exit(f"raw {kid}.{tag}.out sha drift vs the pinned published bytes")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {kid}.{tag}.out lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} vs p1 (fresh two-pass node-exact gate)")
    if ref["budget"] != budget:
        sys_exit(f"{kid}: budget drift (expected {budget})")
    return ref


def verify_ek_kit():
    if not EK_DIR.is_dir():
        sys_exit(f"kit dir missing {EK_DIR}")
    if sha(EK_DIR / "MANIFEST-sha256.txt") != EK_MANIFEST_SHA:
        sys_exit("Part EK kit MANIFEST rev2 sha drift")
    verified = 0
    for line in (EK_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        want, rel = fields[0], fields[1]
        if rel.startswith("/") or ".." in rel.split("/"):
            sys_exit(f"Part EK MANIFEST unsafe path: {rel}")
        p = EK_DIR / rel
        if not p.is_file():
            sys_exit(f"Part EK kit file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"Part EK kit file sha drift: {rel}")
        verified += 1
    if verified != EK_KIT_FILES:
        sys_exit(f"Part EK kit files verified {verified} != {EK_KIT_FILES}")
    return verified


def main() -> None:
    # --- anchors: base cache, merger, quarantine ----------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EI canonical) sha drift")
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

    # --- G-kit: the published Part EK kit is verified file-by-file ---------
    kit_files = verify_ek_kit()
    for name, want in SOURCE_PINS.items():
        p = {
            "b39_status": "sources/b39-status.log",
            "canonical_cache_src": "sources/canonical-cache-ei-merged-73482be0-20261125.cache",
            "exh15m_aj030_p1": "sources/exh15m/aj030.p1.out",
            "exh15m_aj030_p2": "sources/exh15m/aj030.p2.out",
            "exh15m_aj039_p1": "sources/exh15m/aj039.p1.out",
            "exh15m_aj039_p2": "sources/exh15m/aj039.p2.out",
            "jsreplay": "scripts/jsreplay.js",
            "quarantine": "sources/n11-s5-evidence-quarantine.json",
            "runbatch_ek_30m": "scripts/runbatch_ek-30m.sh",
            "audit_ek_py": "scripts/audit_ek.py",
            "valgate_at2m_first_input": "val-gate/at2m-s5-1152921504606851072-536870946.input.csv",
            "valgate_at2m_first_baseline": "val-gate/at2m-s5-1152921504606851072-536870946.published-baseline.out",
            "valgate_second_input": "val-gate/at2m-s5-1188950301626860544-536870912.input.csv",
            "valgate_at2m_second_baseline": "val-gate/at2m-s5-1188950301626860544-536870912.published-baseline.out",
            "valgate_first15m_baseline": "val-gate/first-15m-s5-1152921504606851072-536870946.published-baseline.out",
            "valgate_second15m_baseline": "val-gate/second-15m-s5-1188950301626860544-536870912.published-baseline.out",
            "valgate_at2m_first_host": "val-gate/at2m-s5-1152921504606851072-536870946.ek-host.out",
            "valgate_at2m_second_host": "val-gate/at2m-s5-1188950301626860544-536870912.ek-host.out",
            "valgate_first15m_host": "val-gate/first-15m-s5-1152921504606851072-536870946.ek-host.out",
            "valgate_second15m_host": "val-gate/second-15m-s5-1188950301626860544-536870912.ek-host.out",
        }[name]
        if sha(EK_DIR / p) != want:
            sys_exit(f"Part EK source pin drift: {name}")
    if SOURCE_PINS["canonical_cache_src"] != BASE_CACHE_SHA_EXPECTED:
        sys_exit("the EK kit source cache copy and the EI chain head disagree")
    if sha(EK_DIR / "output/status.log") != EK_STATUS_SHA:
        sys_exit("Part EK status.log sha drift")
    if sha(EK_DIR / "output/audit_ek.json") != EK_AUDIT_SHA:
        sys_exit("Part EK audit_ek.json sha drift")

    # --- G-SSOT: audit_ek.json honesty pins ---------------------------------
    audit = json.loads((EK_DIR / "output/audit_ek.json").read_text())
    if audit["schema"] != "n11-ek-aj030aj039-reprobe30m-audit-v1":
        sys_exit("Part EK audit schema drift")
    if audit["gates_total"] != 79 or audit["gates_failed"] != []:
        sys_exit("Part EK audit gates 79/79 accounting drift")
    if audit["all_gates_pass"] is not True:
        sys_exit("Part EK audit all_gates_pass must be true")
    if audit["verdict_consumed"] is not False:
        sys_exit("Part EK audit verdict_consumed must be false (probe-time honesty)")
    if audit["claims"]["labels"] != {"aj030": "WIN", "aj039": "LOSS"}:
        sys_exit("Part EK audit honest-label drift")
    if audit["main_probes"] != {
            "aj030": {"label": "WIN", "nodes": 15284699,
                      "p1_wall_s": 181.0, "p2_wall_s": 190.0, "result": 1},
            "aj039": {"label": "LOSS", "nodes": 16549916,
                      "p1_wall_s": 96.0, "p2_wall_s": 98.0, "result": 2}}:
        sys_exit("Part EK audit main_probes drift")
    if audit["anchors"] != {
            "af039": {"budget": 30000000, "nodes": 19234232, "result": 2},
            "aj001": {"budget": 30000000, "nodes": 5156075, "result": 2},
            "aj049": {"budget": 30000000, "nodes": 4998452, "result": 1}}:
        sys_exit("Part EK audit anchors drift")
    if audit["valgate"] != {
            "at2m-s5-1152921504606851072-536870946": {"budget": 2000000, "nodes": 2000000, "result": 0},
            "at2m-s5-1188950301626860544-536870912": {"budget": 2000000, "nodes": 2000000, "result": 0},
            "first-15m-s5-1152921504606851072-536870946": {"budget": 15000000, "nodes": 3651923, "result": 2},
            "second-15m-s5-1188950301626860544-536870912": {"budget": 15000000, "nodes": 5040200, "result": 2}}:
        sys_exit("Part EK audit valgate drift")

    # --- G-status: the 7-line honest history --------------------------------
    lines = (EK_DIR / "output/status.log").read_text().splitlines()
    if lines != STATUS_ALL_LINES:
        sys_exit("status.log != the pinned 7-line honest history")
    if [l for l in lines if "WIN-HALT" in l] != STATUS_WIN_HALT_LINES:
        sys_exit("status WIN-HALT lines != the pinned honest halt history")
    got_pass = {}
    for line in lines:
        parts = line.split()
        if parts[2] == "PASS":
            kid = parts[1]
            if kid in got_pass:
                sys_exit(f"duplicate status verdict row for {kid}")
            b, r, n = parts[3].split(",")
            got_pass[kid] = (int(b), int(r), int(n))
    if sorted(got_pass) != sorted(ADOPTED_IDS + WIN_IDS_UNCONSUMED + ANCHOR_IDS):
        sys_exit("status PASS keys != the 5 probed/anchor targets")
    for kid, (r, n) in LABEL_PINS.items():
        if got_pass[kid] != (BUDGET, r, n):
            sys_exit(f"{kid} status verdict vs pinned honest label drift")

    # --- G-drive: the published drive.out one-liners ------------------------
    for kid in ["aj030", "aj039", "af039"]:  # the published drive.out one-liners
        d = (EK_DIR / f"output/{kid}.drive.out").read_text().splitlines()
        r, n = LABEL_PINS[kid]
        want = [f"{kid} PASS {BUDGET},{r},{n}"]
        if LABEL_PINS[kid][0] == 1:
            want = want + [f"WIN-HALT {kid}"]
        if d != want:
            sys_exit(f"{kid} drive.out drift: {d}")

    # --- G-SSOT: the published raws (two-pass fresh-cold node-exact) --------
    raws = {}
    for kid in PROBED_IDS + ANCHOR_IDS:
        e = KEY_PINS[kid]
        ref = two_pass(EK_DIR / "output/raw", kid, RAW_SHAS, BUDGET)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["legal"] != e["legal"] or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != got_pass[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        if (ref["result"], ref["nodes"]) != LABEL_PINS[kid]:
            sys_exit(f"{kid}: raw honest-label drift vs the pinned audit label")
        raws[kid] = ref
    loss_set = sorted(k for k in raws if raws[k]["result"] == 2)
    win_set = sorted(k for k in raws if raws[k]["result"] == 1)
    if loss_set != sorted(ADOPTED_IDS + [k for k in ANCHOR_IDS if LABEL_PINS[k][0] == 2]):
        sys_exit(f"30M decisive LOSS set drift: {loss_set}")
    if win_set != sorted(WIN_IDS_UNCONSUMED + [k for k in ANCHOR_IDS if LABEL_PINS[k][0] == 1]):
        sys_exit(f"30M probe-level WIN set drift: {win_set}")
    n = sum(raws[k]["nodes"] for k in ADOPTED_IDS)
    if n != ADOPTED_NODES_PER_PASS:
        sys_exit(f"adopted node total drift {n} != {ADOPTED_NODES_PER_PASS}")
    p = sum(raws[k]["nodes"] for k in PROBED_IDS)
    if p != WHOLE_PACKET_NODES_PER_PASS:
        sys_exit(f"whole-packet node total drift {p} != {WHOLE_PACKET_NODES_PER_PASS}")

    # --- G-input: byte-pinned 1-line input rows -----------------------------
    for kid in PROBED_IDS + ANCHOR_IDS:
        p_in = EK_DIR / f"input/{kid}.input.csv"
        if sha(p_in) != INPUT_CSV_SHAS[kid]:
            sys_exit(f"input csv {kid} sha drift vs the pinned published bytes")
        e = KEY_PINS[kid]
        want_line = f"target,0,5,{e['lo']},{e['hi']},{e['legal']},0,0,0,0,0"
        rows_in = [l for l in p_in.read_text().splitlines() if l.strip()]
        if rows_in != [want_line]:
            sys_exit(f"input csv {kid} body drift: {rows_in}")

    # --- G-exh15m: the honest exhaustion history (no same-condition re-probe)
    if BUDGET <= EXH_BUDGET:
        sys_exit("the adopted condition must EXCEED the exhausted 15M condition")
    for kid in ("aj030", "aj039"):
        e = KEY_PINS[kid]
        ref = two_pass(EK_DIR / "sources/exh15m", kid,
                       {f"aj030.p1.out": SOURCE_PINS["exh15m_aj030_p1"],
                        "aj030.p2.out": SOURCE_PINS["exh15m_aj030_p2"],
                        "aj039.p1.out": SOURCE_PINS["exh15m_aj039_p1"],
                        "aj039.p2.out": SOURCE_PINS["exh15m_aj039_p2"]},
                       EXH_BUDGET)
        if (ref["result"], ref["nodes"]) != EXH_LABEL_PINS[kid]:
            sys_exit(f"{kid}: exh15m honest-history label drift")
        if ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
            sys_exit(f"{kid}: exh15m key disagreement vs the pinned key fields")
    b39_lines = (EK_DIR / "sources/b39-status.log").read_text().splitlines()
    exhausted_now = [l for l in b39_lines if " EXHAUSTED " in l and
                     ("aj030" in l or "aj039" in l)]
    if exhausted_now != B39_EXHAUSTED_LINES:
        sys_exit("b39-status honest EXHAUSTED history lines drift")

    # --- freshness: BASE / quarantine / WIN exclusion ------------------------
    for kid in PROBED_IDS:
        e = KEY_PINS[kid]
        key = (e["lo"], e["hi"])
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE; fresh-increment gate")
    for kid, key in UNCONSUMED_WIN_NO_CACHE.items():
        if key in base_keys:
            sys_exit(f"unconsumed batch-39 WIN key {kid} must sit in NO cache (BASE)")
        if key in quarantined:
            sys_exit(f"unconsumed batch-39 WIN key {kid} is quarantined")
    for cid, key in CLAIM_RESERVED_PAIRS.items():
        if key in base_keys:
            sys_exit(f"claim-reserved {cid} must sit in NO cache (Part EF owner)")
        if key in quarantined:
            sys_exit(f"claim-reserved {cid} is quarantined")
    for cid, key in CLAIM_RESERVED_PAIRS.items():
        if key == (KEY_PINS["aj039"]["lo"], KEY_PINS["aj039"]["hi"]):
            sys_exit(f"claim-reserved {cid} pair must not be adopted here (Part EF owner)")

    adopted_rows = [(KEY_PINS[k]["lo"], KEY_PINS[k]["hi"], KEY_PINS[k]["legal"],
                     LABEL_PINS[k][0], LABEL_PINS[k][1]) for k in ADOPTED_IDS]
    if len(adopted_rows) != 1 or any(r[3] != 2 for r in adopted_rows):
        sys_exit("adopted rows must be exactly the 1 fresh exact-LOSS row")
    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes in sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- emit increment + manifest -------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    rowlines = [f"s5verdict,{r[0]},{r[1]},5,2,{r[2]}"
                for r in sorted((lo, hi, nodes)
                                 for lo, hi, legal, result, nodes in adopted_rows)]
    blob = ("\n".join(HDR_LINES + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned {ADOPTED_INCREMENT_SHA}")
    (OUT / INCREMENT_NAME).write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes}
        for lo, hi, legal, result, nodes in sorted(adopted_rows)]

    manifest = {
        "schema": EL_SCHEMA,
        "batches": [
            {"pool": "ek-aj039loss1",
             "adopted_loss_ids": list(ADOPTED_IDS),
             "probed_ids": list(PROBED_IDS),
             "anchor_ids": list(ANCHOR_IDS),
             "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
             "adopted_nodes_per_pool": ADOPTED_NODES_PER_PASS,
             "whole_packet_nodes": WHOLE_PACKET_NODES_PER_PASS,
             "status_log_sha256": EK_STATUS_SHA,
             "status_log_lines": STATUS_LINES,
             "status_log_first_line": STATUS_ALL_LINES[0],
             "status_log_final_line": STATUS_ALL_LINES[-1],
             "status_log_win_halt_lines": list(STATUS_WIN_HALT_LINES),
             "b39_exhausted_history_lines": list(B39_EXHAUSTED_LINES),
             "probed_budget": BUDGET,
             "exhausted_history_budget": EXH_BUDGET,
             "claim_reserved_excluded_ids": list(CLAIM_RESERVED_IDS),
             "claim_reserved_pairs": {k: list(v) for k, v in CLAIM_RESERVED_PAIRS.items()},
             "unconsumed_win_no_cache_pairs": {k: list(v) for k, v in UNCONSUMED_WIN_NO_CACHE.items()},
             "kit_integrity": {
                 "kit_manifest_sha256": EK_MANIFEST_SHA,
                 "kit_files_verified": kit_files,
                 "raw_file_sha256_pins": RAW_SHAS,
                 "input_csv_sha256_pins": INPUT_CSV_SHAS,
                 "audit_ek_json_sha256": EK_AUDIT_SHA,
                 "audit_ek_py_sha256": EK_AUDIT_PY_SHA,
                 "source_pins": dict(SOURCE_PINS),
                 "note": "the Part EK kit is PUBLISHED (42 files, byte-pinned "
                         "above; MANIFEST-sha256 rev2 97574401...); the adopted "
                         "aj039 key is fresh at BASE (never adopted before; "
                         "probed honestly to EXHAUSTED at 15M in batch-39 and "
                         "resolved fresh LOSS at the pre-declared 30M "
                         "condition - not a same-condition re-probe); the "
                         "probe-level WIN row aj030 and the 2 claim-reserved "
                         "batch-38 keys are NOT consumed"},
             },
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_rows": [
            {"lo": KEY_PINS[k]["lo"], "hi": KEY_PINS[k]["hi"],
             "legal": KEY_PINS[k]["legal"], "result": 1,
             "nodes": LABEL_PINS[k][1]} for k in WIN_IDS_UNCONSUMED],
        "exhausted_history_15m": {
            kid: {"result": EXH_LABEL_PINS[kid][0], "nodes": EXH_LABEL_PINS[kid][1],
                  "key": [KEY_PINS[kid]["lo"], KEY_PINS[kid]["hi"]]}
            for kid in ("aj030", "aj039")},
        "row_counts": {
            "adopted_loss_rows": 1,
            "wins_unconsumed_this_pool": 1,
            "exhausted_history_prior": 2,
            "claim_reserved_excluded": 2,
            "prior_canonical_rows_base": BASE_CACHE_ROWS_EXPECTED,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note":
            "the Part EK 30M packet holds, beside the adopted aj039 exact-LOSS "
            "row, the probe-level WIN row aj030 (nodes 15,284,699, WIN-HALT): "
            "it is NOT consumed by this Part (adoption of WIN verdicts is "
            "scrutiny-owner C++ second-implementation gate 9193f5b6... "
            "exclusive) and the aj030 key sits in NO cache",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical single-LOSS adoption increment: only the fresh Part EK "
            "exact-LOSS row aj039 (two-pass fresh-cold node-exact at the "
            "pre-declared 30M budget/order 0 condition, resolved in (15M,30M] "
            "beyond the honest EXHAUSTED 15M history) is consumed into the "
            "canonical cache via the fail-closed union merger; nodes are "
            "bookkeeping, never verdicts; the standard 11x11 empty board stays "
            "UNKNOWN; no class freed or excluded claim is made by the maker "
            "(the reaudit refresh derives scheduling effects machine-only)",
        "provenance": {
            "ek_kit_files": kit_files,
            "status_lines": STATUS_LINES,
            "raws_published": True,
            "audit_gates_total": 79,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_total_nodes_per_pass": ADOPTED_NODES_PER_PASS,
        "whole_packet_nodes_per_pass": WHOLE_PACKET_NODES_PER_PASS,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
