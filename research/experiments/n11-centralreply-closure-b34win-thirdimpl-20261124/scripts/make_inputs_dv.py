#!/usr/bin/env python3
"""make_inputs_dv.py - Part DU-b input maker with fail-closed gates.

Experiment: n11-centralreply-closure-b34win-thirdimpl-20261124
Targets: the two published batch-34 honest-label WIN rows (ag001 / ag002, 2-pass
node-exact at budget 15M, outputs commit 1039a95d000..., dir
n11-centralreply-closure-smallpockets-batch34-20261124). Anchors/negatives:
the published third-impl anchor pair k02a/l1a and negatives ng1/ng2, byte-
identical to the published CZ chain inputs (provenance chain AR -> ... -> CZ).

Layout (experiment root = parent of this scripts/ dir):
  scripts/          this maker + pinned byte-clones (third_impl.js 08ea958f..,
                    run_thirdimpl.sh a0b77d83.., jsreplay.js 84585617..,
                    runbatch.sh f591f8c2..) + verify_tbl_b34.js + audit_dv.py
  sources/          published bytes, sha-pinned below (read-only evidence)
  input/            this maker's output: 6 .input.csv + rows.json
  val-gate/         published 4 gate pairs + fresh .dv-host.out (declared D2)
  output/           third-impl/replica/val-gate outputs + status.log

Gates (all fail-closed, rc=1, partial-output-free):
  M1 sources/raw pins: ag001/ag002 p1/p2 2-pass node-exact (budget,result,
     nodes equal), result == 1 (WIN honest label), replay_done, quads == 95670,
     key_lo/key_hi/legal match batch-keys-b34.json.
  M2 sources/status-b34.log pin: 4 lines, ag001/ag002 PASS consistent with the
     pinned raw (budget,result,nodes) + one WIN-HALT per key, nothing else.
  M3 sources/batch-keys-b34.json pin: target table fields (lo/hi/legal/s5_index/
     serving_class/membership_class_count/canonical_cache_same_lo_rows_context)
     read from the pinned file, never hand-typed.
  M4 sources/anchors-negatives pins: k02a/l1a/ng1/ng2 published CZ-chain bytes.
  M5 sources/inputs pins: emitted target CSVs byte-equal to the published
     batch-34 kit inputs, re-verified after write.

Outputs: input/{ag001,ag002,k02a,l1a,ng1,ng2}.input.csv and input/rows.json
(schema n11-centralreply-closure-b34win-thirdimpl-input-v1). Pure function of
the pinned inputs; the completion protocol requires byte-identical re-runs and
a tamper battery that must ABORT on any pin/field drift. Neither target
verdict is consumed: both rows stay UNADOPTED honest WIN labels pending the
scrutiny owner C++ second-implementation gate (kyouen_dfpn_root.cpp pin
9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e). The
canonical cache 973bcd19.. (6,547 rows) is not modified; it carries no row for
either exact (lo,hi) pair.
"""
import hashlib
import json
import os
import sys

PIN_RAW = {
    "ag001": ("ag001.p1.out", "3ac9ab81a66804efbfa766cd227f4d8abd9cca2f193ee7dec8979b8e90b5550c",
              "ag001.p2.out", "829b960aeee3addc30c1299c1344ce7fbfacba24f28fbdd9d4764e9825d7fa87"),
    "ag002": ("ag002.p1.out", "f99796ae9f800de993332c84fcf88900411a508526f58e033da67a1cb4665bee",
              "ag002.p2.out", "7ab4cbb46ef5c7e12379ba296353835204ab4aee68107d342d1c6f2a401d0718"),
}
PIN_STATUS = "2b5c0aa57406c17539abe8d471379605f8cb2819874e6414517c6fdb1b10c2b5"
PIN_BATCHKEYS = "47754a70c793a850dc4d7e13590fe5d134f0b850280a984aeddd4debcf4925ac"
PIN_ANCHOR_NEG = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}
PIN_TARGET_CSV = {
    "ag001": "e09332d76bd506e7a6613e29411fbd06b55135389c02260727336375c3fb6479",
    "ag002": "52d79efc91f4b12935e9fcf6529e3b53a896d30060e8ef5af5503fc7e6fca21e",
}
ANCHOR_VALUES = {
    "k02a": {"lo": 1297036692683751424, "hi": 68157440, "legal": 87,
             "expect_third": 1, "expect_kind": "win",
             "expansions": 9106337, "ttHits": 4991527},
    "l1a": {"lo": 13019119616, "hi": 16448, "legal": 116,
            "expect_third": 2, "expect_kind": "loss",
            "expansions": 7660602, "ttHits": 3951175},
}
EXPECT_GATE_FAIL_LINE = {
    # exact complete third line third_impl.js prints for the published negatives
    # (third_impl.js fail path: 'third,' + row + ',' + stones + ',' + legalIn
    #  + ',,GATE_FAIL,' + JSON.stringify(msg); row = key_id + tag 'a')
    "ng1": 'third,ng1a,5,88,,GATE_FAIL,"legal count mismatch: derived=87 declared=88"',
    "ng2": 'third,ng2a,6,87,,GATE_FAIL,"stone count mismatch: bits=5 declared=6"',
}
SCHEMA = "n11-centralreply-closure-b34win-thirdimpl-input-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg):
    sys.stderr.write("ABORT: %s\n" % msg)
    sys.exit(1)


def replay_row(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if "# replay_done" not in text:
        fail("M1 %s missing replay_done" % path)
    if "forbidden quadruples: 95670" not in text:
        fail("M1 %s quads != 95670" % path)
    row = None
    for line in text.splitlines():
        if line.startswith("replay,"):
            if row is not None:
                fail("M1 %s multiple replay rows" % path)
            row = line.split(",")
    if row is None:
        fail("M1 %s no replay row" % path)
    # row: replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
    if len(row) != 11:
        fail("M1 %s replay row has %d fields, expected 11" % (path, len(row)))
    return row


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(root, "sources", "raw")
    for sub in ("sources/raw", "sources/inputs", "sources/anchors-negatives",
                "sources", "scripts", "val-gate"):
        if not os.path.isdir(os.path.join(root, sub.split("/")[0])):
            fail("layout missing %s/" % sub)

    # M3 batch-keys pin (target table is read from the pinned file)
    bk_path = os.path.join(root, "sources", "batch-keys-b34.json")
    if sha256_file(bk_path) != PIN_BATCHKEYS:
        fail("M3 batch-keys-b34.json pin mismatch")
    with open(bk_path, "r", encoding="utf-8") as f:
        bk = json.load(f)
    if bk.get("schema") != "n11-centralreply-closure-batch34-keys-v1":
        fail("M3 batch-keys schema unexpected: %r" % bk.get("schema"))
    bkmap = {k["key_id"]: k for k in bk["keys"]}
    if set(bkmap) != {"ag001", "ag002"}:
        fail("M3 batch-keys key set unexpected: %s" % sorted(bkmap))
    if bk.get("pins", {}).get("canonical_cache") != "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b":
        fail("M3 batch-keys canonical cache pin unexpected")

    # M1 raw pins + 2-pass node-exact + WIN + field match against batch-keys
    target_meta = {}
    for key_id, (f1name, pin_p1, f2name, pin_p2) in sorted(PIN_RAW.items()):
        p1 = os.path.join(raw_dir, f1name)
        p2 = os.path.join(raw_dir, f2name)
        if sha256_file(p1) != pin_p1 or sha256_file(p2) != pin_p2:
            fail("M1 raw pin mismatch for %s" % key_id)
        r1, r2 = replay_row(p1), replay_row(p2)
        q1 = r1[5:8]  # budget,result,nodes
        q2 = r2[5:8]
        if q1 != q2:
            fail("M1 %s 2-pass NOT node-exact: %r vs %r" % (key_id, q1, q2))
        budget, result, nodes = q1
        if result != "1":
            fail("M1 %s result != 1 (honest WIN row expected): %s" % (key_id, result))
        if int(nodes) > int(budget):
            fail("M1 %s nodes exceed budget" % key_id)
        b = bkmap[key_id]
        if int(r1[3]) != int(b["legal"]):
            fail("M1 %s legal disagrees with batch-keys" % key_id)
        if int(r1[9]) != int(b["lo"]) or int(r1[10]) != int(b["hi"]):
            fail("M1 %s key_lo/key_hi disagree with batch-keys" % key_id)
        target_meta[key_id] = {
            "key_id": key_id,
            "stones": int(r1[2]),
            "lo": b["lo"],
            "hi": b["hi"],
            "legal": b["legal"],
            "s5_index": b["s5_index"],
            "serving_class": b["serving_class"],
            "membership_class_count": b["membership_class_count"],
            "canonical_cache_same_lo_rows_context": b["canonical_cache_same_lo_rows_context"],
            "replica_result": int(result),
            "replica_nodes": int(nodes),
            "source": "part-du-batch34",
            "expect_third": 1,
        }

    # M2 status pin + nodes consistency with pinned raws
    status_path = os.path.join(root, "sources", "status-b34.log")
    if sha256_file(status_path) != PIN_STATUS:
        fail("M2 status-b34.log pin mismatch")
    with open(status_path, "r", encoding="utf-8") as f:
        lines = [l.split() for l in f.read().splitlines() if l.strip()]
    if len(lines) != 4:
        fail("M2 status-b34.log expected 4 lines, got %d" % len(lines))
    for key_id in ("ag001", "ag002"):
        pass_lines = [l for l in lines if len(l) == 4 and l[1] == key_id and l[2] == "PASS"]
        halt_lines = [l for l in lines if len(l) == 3 and l[1] == key_id and l[2] == "WIN-HALT"]
        if len(pass_lines) != 1 or len(halt_lines) != 1:
            fail("M2 status PASS/WIN-HALT lines missing for %s" % key_id)
        if pass_lines[0][0] != halt_lines[0][0]:
            fail("M2 status timestamp mismatch for %s" % key_id)
        f = pass_lines[0][3].split(",")
        if len(f) != 3 or f[2] != str(target_meta[key_id]["replica_nodes"]):
            fail("M2 status nodes disagree for %s" % key_id)
    if not all(l[2] in ("PASS", "WIN-HALT") for l in lines):
        fail("M2 status carries unexpected line kinds")

    # M6: canonical cache (same-lo context reconciliation, exact-pair absence)
    cache_path = os.path.join(root, "sources", "canonical-cache-973bcd19.cache")
    if sha256_file(cache_path) != "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b":
        fail("M6 canonical cache pin mismatch")
    s5rows = [l for l in open(cache_path, encoding="utf-8").read().splitlines()
              if l.startswith("s5verdict,")]
    if len(s5rows) != 6547:
        fail("M6 canonical cache expected 6,547 s5verdict rows, got %d" % len(s5rows))
    for key_id, meta in sorted(target_meta.items()):
        same_lo = [l for l in s5rows if l.startswith("s5verdict,%d," % meta["lo"])]
        if len(same_lo) != int(meta["canonical_cache_same_lo_rows_context"]):
            fail("M6 %s same-lo context %d != batch-keys %s"
                 % (key_id, len(same_lo), meta["canonical_cache_same_lo_rows_context"]))
        exact = [l for l in same_lo if l.startswith("s5verdict,%d,%d," % (meta["lo"], meta["hi"]))]
        if exact:
            fail("M6 %s exact (lo,hi) pair already in canonical cache (conflict): %r" % (key_id, exact))

    # M4 anchors/negatives pins
    an_dir = os.path.join(root, "sources", "anchors-negatives")
    for name, pin in sorted(PIN_ANCHOR_NEG.items()):
        src = os.path.join(an_dir, name + ".input.csv")
        if not os.path.isfile(src):
            fail("M4 anchor/negative source missing: %s" % src)
        if sha256_file(src) != pin:
            fail("M4 anchor/negative pin mismatch for %s" % name)

    # M5 source target CSVs pins
    for key_id, pin in sorted(PIN_TARGET_CSV.items()):
        if sha256_file(os.path.join(root, "sources", "inputs", key_id + ".input.csv")) != pin:
            fail("M5 published target input pin mismatch for %s" % key_id)

    # emit outputs (byte-copies of pinned sources, re-verified after write)
    input_dir = os.path.join(root, "input")
    os.makedirs(input_dir, exist_ok=True)
    for name in sorted(PIN_ANCHOR_NEG):
        with open(os.path.join(an_dir, name + ".input.csv"), "rb") as f:
            data = f.read()
        dst = os.path.join(input_dir, name + ".input.csv")
        with open(dst, "wb") as f:
            f.write(data)
        if sha256_file(dst) != PIN_ANCHOR_NEG[name]:
            fail("M4 emitted anchor/negative drift for %s" % name)
    for key_id, pin in sorted(PIN_TARGET_CSV.items()):
        with open(os.path.join(root, "sources", "inputs", key_id + ".input.csv"), "rb") as f:
            data = f.read()
        dst = os.path.join(input_dir, key_id + ".input.csv")
        with open(dst, "wb") as f:
            f.write(data)
        if sha256_file(dst) != pin:
            fail("M5 emitted target input drift for %s" % key_id)

    rows = {
        "schema": SCHEMA,
        "sources": {
            "b34_outputs": ("published batch-34 outputs (experiment n11-centralreply-"
                            "closure-smallpockets-batch34-20261124, outputs commit 1039a95d), "
                            "raw+status sha-pinned in this maker"),
            "batch_keys": ("sources/batch-keys-b34.json sha 47754a70c793a850dc4d7e13590fe5d134f0b85"
                           "0280a984aeddd4debcf4925ac (published batch-34 kit)"),
            "anchors_negatives": ("published CZ kit inputs, byte-identical (sha-pinned); "
                                  "provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> BX -> "
                                  "BY -> CC -> CL -> CM -> CR -> CW -> CZ -> DU-b"),
            "unadopted": ("both targets are UNADOPTED honest WIN labels pending the scrutiny "
                          "owner C++ second-implementation gate (kyouen_dfpn_root.cpp pin "
                          "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e); "
                          "canonical cache 973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6"
                          "f9412ca5b unchanged (6,547 rows), carries no row for either exact "
                          "(lo,hi) pair (ag001 same-lo context 8 rows all hi != 1032, ag002 lo absent)"),
        },
        "consumed_into_canonical_cache": False,
        "unadopted_win_rows": True,
        "unadopted_loss_rows": False,
        "canonical_cache_sha256_unchanged": "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b",
        "targets": [target_meta["ag001"], target_meta["ag002"]],
        "anchors": [],
        "negatives": [
            {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
             "stones": 5, "why": "legal+1 vs derived 87",
             "expect_gate_fail_line": EXPECT_GATE_FAIL_LINE["ng1"]},
            {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
             "stones": 6, "why": "stones 6 vs actual 5",
             "expect_gate_fail_line": EXPECT_GATE_FAIL_LINE["ng2"]},
        ],
    }
    for name in ("k02a", "l1a"):
        v = ANCHOR_VALUES[name]
        rows["anchors"].append({
            "key_id": name,
            "stones": 5,
            "lo": v["lo"],
            "hi": v["hi"],
            "legal": v["legal"],
            "expect_third": v["expect_third"],
            "expect_kind": v["expect_kind"],
            "anchor_expansions": v["expansions"],
            "anchor_ttHits": v["ttHits"],
            "replica_result": None,
            "replica_nodes": None,
        })
    tmp = os.path.join(input_dir, "rows.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, indent=1, sort_keys=False)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "rows.json"))
    print("make_inputs_dv: ALL GATES PASS, wrote 6 inputs + rows.json "
          "(targets ag001 nodes=%d, ag002 nodes=%d)"
          % (target_meta["ag001"]["replica_nodes"], target_meta["ag002"]["replica_nodes"]))


if __name__ == "__main__":
    main()
