#!/usr/bin/env python3
"""Build the class 23101 batch-14 residual 10-key input set, fail-closed.

Executes the published single-owner Part AW declaration (note amendment,
pushed 2026-11-22 as commit da131f10; declaring and executing host = this
lane session).  All inputs are published main bytes, re-verified against this
host before use:

  * batch-14 dir at publication commit 7b211d38: batch-keys.json
    (sha256 dfde0e90...), the 10 input CSVs q043..q052 (per-file sha256
    from the batch-14 MANIFEST), status.log, row-audit.json.
  * batch-17 dir at publication commit ffc09de1: batch-keys.json
    (sha256 db762175...) for the s5_index disjointness gate.
  * current canonical exact-S5 verdict cache 6,120 rows
    (sha256 be9cb24e..., Part AS publication commit 8c42e44c).
  * quarantine registry results/n11-s5-evidence-quarantine.json
    (sha256 81d23160...).

Fail-closed gates (all ABORT on any deviation):
  G1  batch-14 batch-keys.json sha256 == dfde0e90... and holds exactly the
      52 key ids q001..q052 of class 23101.
  G2  residual key ids == {q043..q052}; probe_order 580..589 in order;
      s5_index set == {745455..745457, 745459..745465} (10 keys);
      q042's unadopted WIN s5_index 745184 NOT in the residual set.
  G3  each input CSV byte-equals the published file (per-file sha256 from
      the batch-14 MANIFEST pin list below) and its (lo,hi,legal) fields
      agree with the batch-keys row.
  G4  canonical cache sha256 == be9cb24e... , 6,120 rows, and NONE of the
      10 residual keys is present (0/10 hits by (lo,hi)).
  G5  quarantine registry sha256 == 81d23160... and 0/10 residual hits.
  G6  batch-17 batch-keys.json sha256 == db762175... and its s5_index set
      is disjoint from the residual s5_index set.
  G7  published batch-14 status.log probed set == {q001..q042} (with the
      'q042 WIN-HALT' stop row), row-audit rows == 42 keys q001..q042, so
      the residual set is exactly the published key-set complement.

Outputs (deterministic, byte-identical across runs):
  input/batch-keys.json                  the 10 residual keys
  input/residual-keys-manifest.json     gate results + hashes
  input/q0NN.input.csv                  byte-copies of the published CSVs

11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.  This scaffold
consumes no verdicts and claims no closure/coverage.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # scripts/
EXP = HERE.parent                               # experiment dir
INPUT = EXP / "input"
REFS = Path("/home/user/work/aw23101/refs")    # published bytes pulled by the host

BATCH_KEYS_B14_SHA = "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"
BATCH_KEYS_B17_SHA = "db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2"
CANONICAL_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"

# per-file sha256 pins from the published batch-14 MANIFEST (commit 7b211d38)
CSV_SHA = {
    "q043": "2dc4af3d94663380902e2253725f2be938109fc467607f1059a545e83c1ba10c",
    "q044": "e1ab06811332222fca61047e5d1d18a7dc33a2776a4365168c04450655bfa081",
    "q045": "7dd487180374914d22ca872cc32af148edfc9e2cb9d7423e27f1776b4bbcca3b",
    "q046": "6040c5f1c8ea35cb58a13b097af851dc75f2a73bef383e4af3970e4121cf9afe",
    "q047": "66ba3c903d6430417bcd92148d75212471f62575a7accf9e5100c8b64fa0e3c8",
    "q048": "06afadf834149aa6e42779e9ef89bee8d913675120bc5f9c2cb6a0ff737a715c",
    "q049": "5f94a8925cf45796b719427626bbf44a6487391f24f719cefcb3f3ab4d95d6de",
    "q050": "f367ea5413556038cfc5310d6398ddcf836f89f088bd33df503d647d076569b2",
    "q051": "f757781df92792b35d20678ebf40b7fc8e03c33b42ac8100a89eca60184c0e3b",
    "q052": "d4d3e0c7e7ba002337ab07893129af06d368f7c468bc24e43f79fbc6e987e8a8",
}

RESIDUAL_IDS = [f"q{i:03d}" for i in range(43, 53)]
EXPECTED_S5 = {745455, 745456, 745457, 745459, 745460, 745461,
               745462, 745463, 745464, 745465}
UNADOPTED_WIN_S5 = 745184  # q042, published, NOT consumed; must not be here


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def die(msg: str):
    sys.exit(f"ABORT {msg}")


def main() -> None:
    INPUT.mkdir(parents=True, exist_ok=True)
    (EXP / "output").mkdir(parents=True, exist_ok=True)

    # pinned byte sources -------------------------------------------------
    if sha(REFS / "jsreplay.js") != JSREPLAY_SHA:
        die("jsreplay.js sha drift")
    if sha(REFS / "batch-keys-b14.json") != BATCH_KEYS_B14_SHA:
        die("batch-14 batch-keys.json sha drift")
    if sha(REFS / "batch-keys-b17.json") != BATCH_KEYS_B17_SHA:
        die("batch-17 batch-keys.json sha drift")
    if sha(REFS / "canonical-6120.cache") != CANONICAL_SHA:
        die("canonical cache sha drift")
    if sha(REFS / "quarantine.json") != QUARANTINE_SHA:
        die("quarantine registry sha drift")

    # G1 -------------------------------------------------------------------
    b14 = json.loads((REFS / "batch-keys-b14.json").read_text())
    by_id = {k["key_id"]: k for k in b14["keys"]}
    if len(by_id) != 52 or set(by_id) != {f"q{i:03d}" for i in range(1, 53)}:
        die(f"batch-14 key ids unexpected: {len(by_id)}")
    if b14["class_index"] != 23101 or b14["class_mask"] != ["1152921504892059648", "16"]:
        die("batch-14 class header unexpected")

    # G2 -------------------------------------------------------------------
    if any(r not in by_id for r in RESIDUAL_IDS):
        die("residual id missing from batch-14 keys")
    orders = [by_id[r]["probe_order"] for r in RESIDUAL_IDS]
    if orders != list(range(580, 590)):
        die(f"residual probe_order unexpected: {orders}")
    s5_set = {int(by_id[r]["s5_index"]) for r in RESIDUAL_IDS}
    if s5_set != EXPECTED_S5:
        die(f"residual s5_index set unexpected: {sorted(s5_set)}")
    if UNADOPTED_WIN_S5 in s5_set:
        die("unadopted q042 WIN s5 inside the residual set")
    if len(s5_set) != 10:
        die("residual s5 set not 10 distinct")

    # G3 -------------------------------------------------------------------
    csv_rows = {}
    for r in RESIDUAL_IDS:
        p = REFS / f"{r}.input.csv"
        if sha(p) != CSV_SHA[r]:
            die(f"{r}.input.csv sha drift vs published batch-14 MANIFEST")
        fields = p.read_text().strip().split(",")
        k = by_id[r]
        if fields[0] != "target" or fields[2] != "5":
            die(f"{r}: csv header fields unexpected: {fields[:3]}")
        if (fields[3], fields[4], fields[5]) != (k["lo"], k["hi"], str(k["legal"])):
            die(f"{r}: csv (lo,hi,legal) disagree with batch-keys row")
        csv_rows[r] = fields

    # G4 -------------------------------------------------------------------
    base_keys = {}
    for line in (REFS / "canonical-6120.cache").read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        f = line.split(",")
        base_keys[(int(f[1]), int(f[2]))] = (int(f[4]), int(f[5]))
    if len(base_keys) != 6120:
        die(f"canonical cache row count {len(base_keys)} != 6120")
    hits = [(r, (int(by_id[r]["lo"]), int(by_id[r]["hi"])))
            for r in RESIDUAL_IDS if (int(by_id[r]["lo"]), int(by_id[r]["hi"])) in base_keys]
    if hits:
        die(f"canonical BASE cache overlap: {hits}")

    # G5 -------------------------------------------------------------------
    q = json.loads((REFS / "quarantine.json").read_text())
    qk = {tuple(e["key"]) for e in q["entries"] if e.get("active")}
    qhits = [r for r in RESIDUAL_IDS
             if (int(by_id[r]["lo"]), int(by_id[r]["hi"])) in qk]
    if qhits:
        die(f"quarantine overlap: {qhits}")

    # G6 -------------------------------------------------------------------
    b17 = json.loads((REFS / "batch-keys-b17.json").read_text())
    s17 = {int(k["s5_index"]) for k in b17["keys"]}
    if s17 & s5_set:
        die(f"batch-17 s5 overlap: {sorted(s17 & s5_set)}")
    if b17["class_index"] != 10661 or len(s17) != 52:
        die("batch-17 batch-keys header unexpected")

    # G7 -------------------------------------------------------------------
    status_text = (REFS / "b14-status.log").read_text()
    probed = set(re.findall(r"^\S+ (q\d{3}) PASS", status_text, re.M))
    if "q042 WIN-HALT" not in status_text:
        die("published batch-14 status.log lacks the q042 WIN-HALT stop row")
    probed.add("q042")
    if probed != {f"q{i:03d}" for i in range(1, 43)}:
        die(f"published probed set != {{q001..q042}}: {sorted(probed)}")
    ra = json.loads((REFS / "b14-row-audit.json").read_text())
    if ra.get("schema") != "n11-centralreply-closure-class23101-batch14-rowaudit-takeover-v1":
        die("published batch-14 row-audit schema unexpected")
    if ra.get("probed_rows") != 42 or ra.get("wins") != ["q042"] \
            or ra.get("exhausted_result0") not in (0, [], False) \
            or ra.get("mismatch") not in (0, [], False):
        die("published batch-14 row-audit probed/wins/exhausted/mismatch unexpected")
    ra_unprobed = ra.get("unprobed_keys")
    if ra_unprobed != RESIDUAL_IDS:
        die(f"published row-audit unprobed_keys != residual set: {ra_unprobed}")

    # emit -------------------------------------------------------------------
    keys_out = {
        "schema": "n11-centralreply-class23101-residual10-batch-input-v1",
        "class_index": 23101,
        "class_mask": b14["class_mask"],
        "source": ("published batch-14 batch-keys.json (publication commit 7b211d38, "
                   "sha256 dfde0e90...) residual complement of the probed set "
                   "{q001..q042} (Part AQ WIN-HALT at q042); Part AW declaration "
                   "commit da131f10"),
        "groups_served_count": b14.get("groups_served_count"),
        "groups_served_first_seen": b14.get("groups_served_first_seen"),
        "budget": 15000000,
        "keys": [by_id[r] for r in RESIDUAL_IDS],
    }
    (INPUT / "batch-keys.json").write_text(
        json.dumps(keys_out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in RESIDUAL_IDS:
        (INPUT / f"{r}.input.csv").write_bytes((REFS / f"{r}.input.csv").read_bytes())

    manifest = {
        "schema": "n11-centralreply-class23101-residual10-keys-manifest-v1",
        "part": "Part AW (solver, batch-14 residual q043..q052)",
        "declaration_commit": "da131f10891b27ff6d3ff27b06b477caf304cf43",
        "class_index": 23101,
        "residual_ids": RESIDUAL_IDS,
        "residual_count": 10,
        "probed_complement_published": sorted(probed),
        "gates": {
            "g1_batch_keys_b14_sha": BATCH_KEYS_B14_SHA,
            "g2_probe_orders": orders,
            "g2_s5_index_set": sorted(s5_set),
            "g2_unadopted_win_s5_absent": True,
            "g3_csv_sha_pins": CSV_SHA,
            "g3_csv_keys_agreement": True,
            "g4_canonical_sha": CANONICAL_SHA,
            "g4_canonical_rows": len(base_keys),
            "g4_canonical_hits": 0,
            "g5_quarantine_sha": QUARANTINE_SHA,
            "g5_quarantine_hits": 0,
            "g6_batch17_s5_overlap": 0,
            "g7_row_audit_probed_rows": 42,
            "g7_row_audit_unprobed_keys_equals_residual": True,
        },
        "pinned_replica": {
            "jsreplay_js_sha256": JSREPLAY_SHA,
            "runbatch_sha256": sha(EXP / "scripts/runbatch.sh"),
            "runwave_sha256": sha(EXP / "scripts/runwave.sh"),
            "runbatch_delta_from_batch17": ("WIN rows labeled honestly WIN-CONTINUE and the "
                                            "batch CONTINUES (pre-registered Part AW rule); "
                                            "batch-17 published script halted with exit 45. "
                                            "runwave done-set adds WIN-CONTINUE."),
        },
        "interpretation_guard": ("scaffold only: no verdict consumed, no closure/coverage/"
                                 "secured claim; the 10 keys and class 23101 stay UNKNOWN; "
                                 "nodes are bookkeeping, never verdicts"),
    }
    (INPUT / "residual-keys-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"OK 10 residual keys {RESIDUAL_IDS[0]}..{RESIDUAL_IDS[-1]}: all gates PASS "
          f"(canonical 0/10, quarantine 0/10, batch-17 s5 disjoint, "
          f"probed complement exact)")
    print(f"   input/batch-keys.json sha256 {sha(INPUT / 'batch-keys.json')}")
    print(f"   input/residual-keys-manifest.json sha256 {sha(INPUT / 'residual-keys-manifest.json')}")


if __name__ == "__main__":
    main()
