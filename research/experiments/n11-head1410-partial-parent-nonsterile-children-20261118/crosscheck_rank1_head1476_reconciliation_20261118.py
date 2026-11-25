#!/usr/bin/env python3
"""Verification-side crosscheck of the head-1476 rank-1 parent reconciliation.

Independently re-derives, from blob-pinned published inputs only:
  - the K0865 census entry and the effective-worklist rank-1 position of the
    partial-STERILE S5 parent 00000000000000802000040000000 (hex literal below),
  - the 5-row orbit join from the raw head-1410 worklist (fresh fourth-implementation
    D4: coordinate transforms on an 11x11 grid),
  - the fold-chain bookkeeping (cost76d+77e at 1450->1452, cost76c bit61 at
    1472->1473, cost66i bit19 at 1473->1476),
  - the receipt/covers/marginal arithmetic of every folded WIN7-D10 root,
  - byte-level certificate re-hashing of all six folded receipts,
  - the static check-set of the published reconciliation verifier (Node/BigInt mjs)
    against its published result JSON,
  - a K0863-consistency conflict scan: no STERILE row may be covered by any
    folded WIN7-D10 root.

No engine is run. No new verdict is produced. REFUTED-D10 is not a LOSS proof.

Inputs: all files are the published main blobs listed in INPUT_PINS below;
they must be fetched at their pinned commits (see the published log) into the
input directory. Usage: python3 crosscheck_rank1_head1476_reconciliation_20261118.py --input-dir in --output out.json
"""
import argparse
import csv
import hashlib
import json
import re
import sys

N = 11  # board side; bit i -> (x=i%N, y=i//N)

PARENT_HEX = "00000000000000801202000040000000"
ROW_71 = "00000000000000801202000040000400"
ROW_64 = "00000000000000801282000040000000"
ROW_76C = "00000000010000809002000001000000"
ROW_76D = "00000000040000003800080008000000"
ROW_77E = "00000000040000809002000000004000"

SOURCE_MAIN_HEAD = "0c9881826a2e25bf665a19804ba5655f14aa932e"
RECONC_RESULT_COMMIT = "cb7769314a260c91ed062486b600fa98ac689ea3"
RECONC_LOG_COMMIT = "a99f34b89e766d642583260e502ba30264753297"

# git blob sha1 pins (published records)
INPUT_PINS = {
    "k0863.md": "c2ae353cab4a7dbcd28ec53b0f57d35ab4f26a5d",
    "k0865.md": "6b79dbcb2db0b8c34c108c1c227be139a3f1493b",
    "k0868.md": "b097210d0b49d7cf014cc6a554298b1e49e83384",
    "k0865_census.json": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
    "rank1_script.py": "606de306c9d08bac3cc0e119a486dc59cb04de6e",
    "rank1_output.json": "881b7c7777b313bd88ae1840e32f06f397a31e7c",
    "worklist1410.csv": "2fee1d0718547a62e346d35f5858d7913e37c097",
    "s5_closability1410.csv": "65215b6582de6efedfed8d77d91630edd883a2cb",
    "claim76c.json": "678211c5a35c25cf41b4a56473942860903647f6",
    "fold76c.json": "953beaea054989e8b1de33f48b1f2ebc13ae7e11",
    "audit76c.json": "de79a3a7bfc6c5b8fb77db885354f01b82e023f7",
    "manifest76c.json": "00cf337f9365b10ac1db090b9f9cf9a464b83347",
    "claim76d.json": "ec598676317b748eb34c7d2bf4044992343c518e",
    "claim77e.json": "36515c516c7270e1869a52d0a76285200b1e33e8",
    "fold76d77e.json": "8d4bc622f9da22b8754f2e398e5481359656d956",
    "verify76d77e.json": "d267fa8d93017110ff74df4520b3a8e8a47bee5b",
    "manifest76d.json": "e8a6116aec45c19642877db85340e120d23331b3",
    "claim66i.json": "f8556f6c054d821e845b7ebe5035b8c280d2e97b",
    "audit66i.json": "e1fbf301bb6795432dbb015289b4a68c63095ef0",
    "fold66i.json": "a555ee3a575df04ecddf98ce890bd8eec53dd415",
    "reconcile_mjs.mjs": "77e9fa4a8013ba42adbebbbbe24cdeeb1b928d24",
    "reconc.json": "6992f2dcc8b87a5409cff31c8a87134fc4283a6a",
}

# ---- fourth-implementation D4 over the 11x11 grid ----
TFS = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]


def stone_bits(mask):
    return [i for i in range(N * N) if (mask >> i) & 1]


def apply_t(mask, t):
    out = 0
    for i in stone_bits(mask):
        x, y = i % N, i // N
        x2, y2 = t(x, y)
        out |= 1 << (y2 * N + x2)
    return out


def canon(mask):
    return min(apply_t(mask, t) for t in TFS)


def hx(mask):
    return format(mask, "032x")


def popcount(m):
    return bin(m).count("1")


def orbit_related(parent, row):
    """True iff some D4 image of the 5-stone parent is a subset of the 6-stone row."""
    return any(apply_t(parent, t) & ~row == 0 for t in TFS)


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail)})


def load_json(d, name):
    return json.loads((d / name).read_bytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default="in")
    ap.add_argument("--output", default="out.json")
    args = ap.parse_args()
    from pathlib import Path

    d = Path(args.input_dir)

    # ---------- pins ----------
    for name, pin in INPUT_PINS.items():
        data = (d / name).read_bytes()
        stem = name.rsplit(".", 1)[0]
        check("pin." + stem, git_blob_sha(data) == pin, git_blob_sha(data))

    k0863 = (d / "k0863.md").read_text()
    k0865 = (d / "k0865.md").read_text()
    k0868 = (d / "k0868.md").read_text()
    census = load_json(d, "k0865_census.json")
    rank1 = load_json(d, "rank1_output.json")
    old_script = (d / "rank1_script.py").read_text()
    work_rows = list(csv.DictReader((d / "worklist1410.csv").open()))
    s5rows = list(csv.DictReader((d / "s5_closability1410.csv").open()))
    claim76c = load_json(d, "claim76c.json")
    fold76c = load_json(d, "fold76c.json")
    audit76c = load_json(d, "audit76c.json")
    manifest76c = load_json(d, "manifest76c.json")
    claim76d = load_json(d, "claim76d.json")
    claim77e = load_json(d, "claim77e.json")
    fold76d77e = load_json(d, "fold76d77e.json")
    verify76d77e = load_json(d, "verify76d77e.json")
    manifest76d = load_json(d, "manifest76d.json")
    claim66i = load_json(d, "claim66i.json")
    audit66i = load_json(d, "audit66i.json")
    fold66i = load_json(d, "fold66i.json")
    mjs = (d / "reconcile_mjs.mjs").read_text()
    reconc = load_json(d, "reconc.json")

    # ---------- static crosscheck of the published mjs verifier ----------
    lits = re.findall(r'check\("([^"]+)"', mjs)
    pin_block = re.search(r"PINS = \{(.*?)\n\};", mjs, re.S)
    pin_keys = re.findall(r"^\s{2}(\w+): \[", pin_block.group(1), re.M) if pin_block else []
    pin_vals = dict(re.findall(r"^\s{2}(\w+): \[[^\]]*\"([0-9a-f]{40})\"\]", pin_block.group(1), re.M)) if pin_block else {}
    real_lits = [x for x in lits if x not in ("pin.", "F.folds_pending")]
    mjs_names = sorted(real_lits + ["pin." + k for k in pin_keys])
    rec_names = [c["check"] for c in reconc["checks"]]
    check("mjs.check_names_match_result",
          mjs_names == sorted(rec_names) and len(mjs_names) == 47 and len(pin_keys) == 19,
          "literals=%d pin_keys=%d" % (len(real_lits), len(pin_keys)))
    pin_key_to_file = {
        "k0863": "k0863.md", "k0865": "k0865.md", "k0868": "k0868.md",
        "k0865_census": "k0865_census.json", "rank1_script": "rank1_script.py",
        "rank1_output": "rank1_output.json", "worklist1410": "worklist1410.csv",
        "s5_closability1410": "s5_closability1410.csv",
    }
    ok_pt = True
    for k, v in pin_vals.items():
        fname = pin_key_to_file.get(k, k + ".json")
        if INPUT_PINS.get(fname) != v:
            ok_pt = False
    check("mjs.pin_table_matches_inputs",
          ok_pt and len(pin_vals) == 19 and set(pin_vals) == set(pin_keys), str(len(pin_vals)))
    check("mjs.parent_constant", PARENT_HEX in mjs, "")
    check("mjs.result_all_pass", reconc.get("all_pass") is True and reconc.get("check_count") == 47 and all(c["pass"] for c in reconc["checks"]), str(reconc.get("check_count")))
    check("mjs.source_main_head_pinned", reconc.get("source_main_head") == SOURCE_MAIN_HEAD and SOURCE_MAIN_HEAD in mjs, "")

    # ---------- basis items ----------
    check("basis.k0863_proved", "status: proved" in k0863 or "status: proved" in k0863.replace(" ", ""), "")
    check("basis.k0865_head1410", "head-1410" in k0865 and census["head_state"]["solved_manifest_rows"] == 1410, "")
    check("basis.k0868_convention", "own_candidates" in k0868, "")

    # ---------- census entry ----------
    P = int(PARENT_HEX, 16)
    entry = next(e for e in census["open_s5_census"] if e["hex"] == PARENT_HEX)
    check("census.parent_entry",
          entry["classification"] == "partial_sterile" and entry["remaining_s6_orbits"] == 5
          and entry["effective_remaining"] == 3 and entry["effective_cost"] == 229
          and entry["sterile_cost"] == 135 and entry["remaining_s7_edge_cost"] == 364
          and entry["sterile_refs_count"] == 2 and entry["classes"] == 2,
          "")
    check("census.sterile_refs",
          {r["hex"] for r in entry["sterile_refs"]} == {ROW_71, ROW_64}
          and {r["cost"] for r in entry["sterile_refs"]} == {71, 64}, "")
    top0 = census["effective_worklist_top16"][0]
    check("census.top16_rank1", top0["hex"] == PARENT_HEX and top0["effective_cost"] == 229 and top0["effective_remaining"] == 3 and top0["sterile_refs_count"] == 2, "")
    t = census["census_totals"]
    check("census.totals", (t["open_s5"], t["unclosable"], t["partial"], t["no_sterile"], t["sterile_refs"], t["remaining_row_refs"], t["eff_remaining"]) == (174, 3, 57, 114, 91, 12274, 12183), json.dumps(t))
    reg = {e["hex"]: e for e in census["sterile_row_registry"]}
    check("census.sterile_registry",
          ROW_64 in reg and ROW_71 in reg
          and PARENT_HEX in reg[ROW_64]["open_parents"] and PARENT_HEX in reg[ROW_71]["open_parents"]
          and reg[ROW_64]["cost"] == 64 and reg[ROW_71]["cost"] == 71, "")

    # ---------- independent orbit join from the raw worklist ----------
    check("join.worklist_rows", len(work_rows) == 6438, str(len(work_rows)))
    check("join.parent_popcount", popcount(P) == 5, str(popcount(P)))
    related = []
    for r in work_rows:
        m = int(r["s6_canonical_hex"], 16)
        if popcount(m) == 6 and orbit_related(P, m):
            related.append({"hex": r["s6_canonical_hex"], "cost": int(r["own_candidates_s6_s7_edge_cost"]), "category": r["category"]})
    related.sort(key=lambda x: x["hex"])
    join_hexes = [x["hex"] for x in related]
    check("join.d4_related_rows",
          join_hexes == sorted([ROW_64, ROW_71, ROW_76C, ROW_76D, ROW_77E]),
          json.dumps(join_hexes))
    check("join.total_cost_364", sum(x["cost"] for x in related) == 364, str(sum(x["cost"] for x in related)))
    join_by_hex = {x["hex"]: x for x in related}
    check("join.sterile_rows_match_census",
          {x["hex"] for x in related if x["category"] == "sterile"} == {ROW_64, ROW_71}, "")
    check("join.canon_implementation_witnessed",
          hx(canon(int(ROW_76C, 16) | (1 << 61))) == "0000000001000080b002000001000000"
          and hx(canon(int(ROW_76C, 16) | (1 << 99))) == "00000000040000809002000000400800", "")

    # ---------- s5 closability CSV row ----------
    s5row = next(r for r in s5rows if r["s5_hex"] == PARENT_HEX)
    check("s5csv.parent_row",
          s5row["category"] == "cross_cover_required" and int(s5row["remaining_s6_orbits"]) == 5
          and int(s5row["remaining_s7_edge_cost"]) == 364 and int(s5row["rows_sterile"]) == 2
          and int(s5row["rows_win_pending"]) == 2 and int(s5row["rows_transfer_partial"]) == 1
          and int(s5row["rows_unswept"]) == 0
          and set(s5row["sterile_rows"].split(";")) == {ROW_64, ROW_71}, "")

    # ---------- historical rank-1 audit ----------
    s = rank1["summary"]
    check("hist.checks_29_all_pass", rank1["all_checks_pass"] is True and len(rank1["checks"]) == 29, str(len(rank1["checks"])))
    check("hist.summary_fields",
          s["parent"] == PARENT_HEX and s["remaining_rows"] == 5 and s["sterile_rows"] == 2
          and s["nonsterile_rows"] == 3 and s["win7_d10_bits"] == [19, 37, 49, 61, 69, 99]
          and s["certificates_published_and_verified"] == [19, 37, 49, 69]
          and sorted(s["fold_pending_bands"]) == ["cost76c", "cost76d", "cost77e"]
          and s["effective_worklist_rank"] == 1 and s["effective_cost"] == 229
          and s["receipt_channel_sweep_work_remaining_on_own_rows"] == 0, "")
    r1rows = {r["hex"]: r for r in rank1["rows"]}
    check("hist.rows_match_join",
          set(r1rows) == set(join_hexes)
          and all(r1rows[x]["cost"] == join_by_hex[x]["cost"] for x in join_hexes), "")
    # raw-root arithmetic for the four win_pending roots and derived canons for 76c
    ok = True
    for rowhex, bits_, key in ((ROW_76D, [19, 49], "win_root_hexes"), (ROW_77E, [37, 69], "win_root_hexes")):
        for b, root in zip(bits_, r1rows[rowhex][key]):
            ok = ok and (int(root, 16) == int(rowhex, 16) | (1 << b)) and popcount(int(root, 16)) == 7
    for b, root in zip([61, 99], r1rows[ROW_76C]["win_root_canon_hexes_derived"]):
        ok = ok and hx(canon(int(ROW_76C, 16) | (1 << b))) == root
    check("hist.win_root_arithmetic", ok, "")

    # ---------- fold 76d+77e ----------
    f = fold76d77e
    rec_by_bit = {r["bit"]: r for r in f["receipts"]}
    check("fold76d77e.receipts_bits",
          sorted(rec_by_bit) == [19, 37, 49, 69]
          and rec_by_bit[19]["root_hex"] == r1rows[ROW_76D]["win_root_hexes"][0]
          and rec_by_bit[49]["root_hex"] == r1rows[ROW_76D]["win_root_hexes"][1]
          and rec_by_bit[37]["root_hex"] == r1rows[ROW_77E]["win_root_hexes"][0]
          and rec_by_bit[69]["root_hex"] == r1rows[ROW_77E]["win_root_hexes"][1], "")
    ok = True
    for r in f["receipts"]:
        root = int(r["root_hex"], 16)
        cc = {hx(canon(root ^ (1 << b))) for b in stone_bits(root)}
        ok = ok and cc == set(r["covers_hexes"]) and len(cc) == 7
        ok = ok and set(r["marginal_hexes"]) <= set(r["covers_hexes"])
        ok = ok and set(r["marginal_manifest_hexes"]) <= set(r["marginal_hexes"])
    check("fold76d77e.covers_and_marginal_arithmetic", ok, "")
    closed = set()
    for r in f["receipts"]:
        closed |= set(r["marginal_manifest_hexes"])
    check("fold76d77e.rows_closed",
          closed == {ROW_76D, ROW_77E} == set(f["totals"]["rows_closed_hexes"])
          and closed <= set(join_hexes), json.dumps(sorted(closed)))
    hb = f["baseline_record"]["basis_head_1450"].split(" ")[0]
    fa = f["frontier_after_cost76d77e"]
    check("fold76d77e.head_segment",
          hb == "1450/174/6398/506297/4671/370211"
          and (fa["solved_s6_in_manifest"], fa["unique_remaining_s6"], fa["sum_remaining_cost"], fa["s6_needed_by_open_classes"], fa["cost_needed_by_open_classes"]) == (1452, 6396, 506144, 4669, 370058)
          and 506297 - 506144 == 153 == join_by_hex[ROW_76D]["cost"] + join_by_hex[ROW_77E]["cost"]
          and 6398 - 6396 == 2 and 4671 - 4669 == 2 and 370211 - 370058 == 153, "")
    pa = f["parents_after"][PARENT_HEX]
    check("fold76d77e.parent_after",
          pa["rows"] == 3 and pa["edge_cost"] == 211 and pa["rows_before"] == 5 and pa["edge_cost_before"] == 364
          and 364 - 153 == 211, "")
    check("fold76d77e.claims_complete",
          "1452/174/6396/506144/4669/370058" in json.dumps(claim76d)
          and "FOLD COMPLETE" in claim76d["status"] and "FOLD COMPLETE" in claim77e["status"], "")
    check("fold76d77e.second_verification",
          verify76d77e["verdict"] == "VERIFICATION PASSED" and verify76d77e.get("failures") in ([], None, ""), "")
    check("fold76d77e.verify_pins_manifest76d",
          verify76d77e["inputs_git_blob_shas"]["output/class2-lane-cost76d-win7-certificates-20261116.json"]
          == git_blob_sha((d / "manifest76d.json").read_bytes()) == "e8a6116aec45c19642877db85340e120d23331b3", "")
    # certificate re-hash: 76d whole files, 77e joined parts
    cert_files = {
        "76d_bit19": (d / "certs/76d_bit19.cert", rec_by_bit[19]["certificate"]),
        "76d_bit49": (d / "certs/76d_bit49.cert", rec_by_bit[49]["certificate"]),
        "77e_bit37": (d / "certs/77e_bit37.p1", rec_by_bit[37]["certificate"]),  # joined below
        "77e_bit69": (d / "certs/77e_bit69.p1", rec_by_bit[69]["certificate"]),
    }
    ok = True
    details = {}
    b19 = (d / "certs/76d_bit19.cert").read_bytes()
    b49 = (d / "certs/76d_bit49.cert").read_bytes()
    j37 = (d / "certs/77e_bit37.p1").read_bytes() + (d / "certs/77e_bit37.p2").read_bytes()
    j69 = (d / "certs/77e_bit69.p1").read_bytes() + (d / "certs/77e_bit69.p2").read_bytes()
    for tag, data, cmeta in (("76d_bit19", b19, rec_by_bit[19]["certificate"]), ("76d_bit49", b49, rec_by_bit[49]["certificate"]),
                             ("77e_bit37", j37, rec_by_bit[37]["certificate"]), ("77e_bit69", j69, rec_by_bit[69]["certificate"])):
        m5 = hashlib.md5(data).hexdigest()
        s2 = hashlib.sha256(data).hexdigest()
        okrow = (len(data) == cmeta["bytes"] and m5 == cmeta["md5"] and s2 == cmeta["sha256"])
        ok = ok and okrow
        details[tag] = {"bytes": len(data), "sha256_ok": s2 == cmeta["sha256"], "md5_ok": m5 == cmeta["md5"], "lines": data.count(b"\n")}
    check("fold76d77e.certificates_rehash", ok, json.dumps(details))
    # 76d certs also carry git blob pins in manifest76d
    m76d = {c["bit"]: c for c in manifest76d["certificates"]}
    check("fold76d77e.cert_blob_pins",
          git_blob_sha(b19) == m76d[19]["published_cert"]["git_blob_sha"]
          and git_blob_sha(b49) == m76d[49]["published_cert"]["git_blob_sha"]
          and m76d[19]["root_hex"] == rec_by_bit[19]["root_hex"]
          and m76d[49]["root_hex"] == rec_by_bit[49]["root_hex"], "")
    check("fold76d77e.cert_rows",
          b19.count(b"\n") == rec_by_bit[19]["certificate"]["rows"] + 2
          and b49.count(b"\n") == rec_by_bit[49]["certificate"]["rows"] + 2
          and j37.count(b"\n") == rec_by_bit[37]["certificate"]["rows"] + 2
          and j69.count(b"\n") == rec_by_bit[69]["certificate"]["rows"] + 2, "")

    # ---------- fold 76c bit61 ----------
    fr = fold76c["receipts"][0]
    check("fold76c.receipt_bit61",
          fold76c["receipts"].__len__() == 1 and fr["bit"] == 61
          and int(fr["root_hex"], 16) == int(ROW_76C, 16) | (1 << 61)
          and fr["d4_canon_root"] == fr["root_hex"]
          and manifest76c["certificates"][0]["raw_is_canon"] is True, "")
    fa76c = fold76c["frontier_after_cost76c"]
    check("fold76c.basis_head",
          fold76c["basis_head"] == 1472
          and fold76c["baseline_record"]["frontier_before"]["sum_remaining_cost"] == 504672
          and claim76c["receipt_fold"]["basis_head"] == [1472, 174, 6376, 504672, 4649, 368586], "")
    check("fold76c.frontier_after",
          (fa76c["solved_s6_in_manifest"], fa76c["unique_remaining_s6"], fa76c["sum_remaining_cost"], fa76c["s6_needed_by_open_classes"], fa76c["cost_needed_by_open_classes"]) == (1473, 6375, 504596, 4648, 368510)
          and 504672 - 504596 == 76 == join_by_hex[ROW_76C]["cost"]
          and 6376 - 6375 == 1 and 4649 - 4648 == 1 and 368586 - 368510 == 76, "")
    pa76c = fold76c["parents_after"][PARENT_HEX]
    check("fold76c.parent_cumulative",
          pa76c["rows_before"] == 5 and pa76c["rows_after"] == 2 and pa76c["edge_cost_before"] == 364
          and pa76c["edge_cost_after"] == 135 and pa76c["lost_rows"] == 3 and pa76c["lost_edge_cost"] == 229
          and set(pa76c["lost_rows_hexes"]) == {ROW_76C, ROW_76D, ROW_77E}
          and {x["hex"] for x in related if x["category"] != "sterile"} == {ROW_76C, ROW_76D, ROW_77E}, "")
    check("fold76c.marginal_manifest",
          ROW_76C in fr["marginal_manifest_hexes"] and fr["marginal_manifest_rows"] == 1
          and all(popcount(int(x, 16)) == 6 for x in fr["marginal_manifest_hexes"]), "")
    check("fold76c.audit_pass",
          audit76c["all_checks_pass"] is True and audit76c["check_count"] == 56 and audit76c["status"] == "PASS", "")
    mc = manifest76c["certificates"][0]
    check("fold76c.manifest",
          len(manifest76c["certificates"]) == 1 and mc["bit"] == 61
          and manifest76c["s6_child_hex"] == ROW_76C and manifest76c["s6_s7_edge_cost"] == 76
          and mc["root"] == fr["d4_canon_root"], "")
    b61 = (d / "certs/76c_bit61.cert").read_bytes()
    check("fold76c.certificate_rehash",
          len(b61) == mc["bytes"] == fr["certificate"]["bytes"]
          and hashlib.sha256(b61).hexdigest() == mc["sha256"] == fr["certificate"]["sha256"]
          and hashlib.md5(b61).hexdigest() == mc["md5"] == fr["certificate"]["md5"]
          and git_blob_sha(b61) == mc["git_blob_sha"] == fr["certificate"]["git_blob_sha"], "")
    check("fold76c.cert_rows", b61.count(b"\n") == mc["rows"] + 2, str(b61.count(b"\n")))
    check("fold76c.claim_status",
          "receipt fold complete at head1473" in claim76c["status"] and claim76c["receipt_fold"]["status"] == "fold-complete", "")

    # ---------- fold 66i bit19 ----------
    check("fold66i.basis_chain",
          fold66i["basis_head"]["sum_remaining_cost"] == 504596 and fold66i["basis_head"]["solved_s6_in_manifest"] == 1473
          and claim66i["receipt_fold"]["basis_head"] == [1473, 174, 6375, 504596, 4648, 368510], "")
    fa66i = fold66i["frontier_after_cost66i_bit19"]
    check("fold66i.frontier_after",
          (fa66i["solved_s6_in_manifest"], fa66i["unique_remaining_s6"], fa66i["sum_remaining_cost"], fa66i["s6_needed_by_open_classes"], fa66i["cost_needed_by_open_classes"]) == (1476, 6372, 504389, 4645, 368303)
          and 504596 - 504389 == 207 and 1476 - 1473 == 3 and 6375 - 6372 == 3 and 4648 - 4645 == 3 and 368510 - 368303 == 207, "")
    r66 = fold66i["receipts"][0]
    check("fold66i.receipt_bit19",
          r66["bit"] == 19 and r66["root_hex"] == "00000000000000801226000000080000"
          and r66["marginal_manifest_rows"] == 3 and fold66i["totals"]["s6_edge_cost_removed"] == 207, "")
    marg66 = r66["marginal_manifest_hexes"]
    wl = {r["s6_canonical_hex"]: int(r["own_candidates_s6_s7_edge_cost"]) for r in work_rows}
    check("fold66i.marginal_costs",
          all(x in wl for x in marg66) and sum(wl[x] for x in marg66) == 207, json.dumps(marg66))
    check("fold66i.does_not_touch_parent",
          PARENT_HEX not in fold66i["parents_after"]
          and all(not orbit_related(P, int(x, 16)) for x in marg66), "")
    check("fold66i.audit_pass", audit66i["all_checks_pass"] is True and audit66i["check_count"] == 50 and audit66i["status"] == "PASS", "")
    j66 = (d / "certs/66i_bit19.p1").read_bytes() + (d / "certs/66i_bit19.p2").read_bytes()
    c66 = r66["certificate"]
    check("fold66i.certificate_rehash",
          len(j66) == c66["bytes"] and hashlib.sha256(j66).hexdigest() == c66["sha256"]
          and git_blob_sha((d / "certs/66i_bit19.p1").read_bytes()) == c66["part1_git_blob_sha"]
          and git_blob_sha((d / "certs/66i_bit19.p2").read_bytes()) == c66["part2_git_blob_sha"], "")
    check("fold66i.claim_partial_fold",
          claim66i["receipt_fold"]["status"] == "partial-fold-complete; bit19 folded, 8 receipts remain"
          and claim66i["receipt_fold"]["folded_bits"] == [19]
          and claim66i["receipt_fold"]["frontier_after_bit19"] == [1476, 174, 6372, 504389, 4645, 368303], "")

    # ---------- K0863 consistency: no STERILE row under any folded WIN root ----------
    folded_roots = [int(r["root_hex"], 16) for r in fold76d77e["receipts"]] + [int(fr["root_hex"], 16), int(r66["root_hex"], 16)]
    ok = True
    for srow in (ROW_71, ROW_64):
        sm = int(srow, 16)
        for root in folded_roots:
            if sm & ~root == 0:
                ok = False
    # and no cover (root minus one stone, any D4 image) equals a STERILE row
    covers_all = set()
    for root in folded_roots:
        for b in stone_bits(root):
            for t in TFS:
                covers_all.add(hx(apply_t(root ^ (1 << b), t)))
    for srow in (ROW_71, ROW_64):
        sm = int(srow, 16)
        for c in covers_all:
            if sm & ~int(c, 16) == 0 and popcount(sm) == 6:
                ok = ok and False
    check("conflict.sterile_rows_not_covered_by_folded_roots", ok, str(len(folded_roots)) + " roots scanned")

    # ---------- reconciliation result JSON field-by-field ----------
    check("reconc.historical_audit_fields",
          reconc["historical_audit"]["check_count"] == 29 and reconc["historical_audit"]["all_checks_pass"] is True
          and sorted(reconc["historical_audit"]["record_time_fold_pending_bands"]) == ["cost76c", "cost76d", "cost77e"], "")
    fr76 = reconc["fold_reconciliation"]["cost76d77e"]
    check("reconc.fold_76d77e_fields",
          fr76["head_before"] == "1450/174/6398/506297/4671/370211" and fr76["head_after"] == "1452/174/6396/506144/4669/370058"
          and fr76["receipts"] == 4 and set(fr76["rows_closed"]) == {ROW_76D, ROW_77E}
          and fr76["parent_rows_after"]["rows"] == 3 and fr76["parent_rows_after"]["edge_cost"] == 211, "")
    fr76c = reconc["fold_reconciliation"]["cost76c"]
    check("reconc.fold_76c_fields",
          fr76c["status"] == "fold-complete" and fr76c["folded_bits"] == [61] and fr76c["fallback_unextracted_bits"] == [99]
          and fr76c["cumulative_parent_rows_after"]["rows_after"] == 2
          and fr76c["cumulative_parent_rows_after"]["edge_cost_after"] == 135
          and set(fr76c["cumulative_parent_rows_after"]["lost_rows_hexes"]) == {ROW_76C, ROW_76D, ROW_77E}, "")
    fr66i = reconc["fold_reconciliation"]["cost66i_bit19"]
    check("reconc.fold_66i_fields",
          fr66i["status"] == "partial-fold-complete; bit19 folded, 8 receipts remain"
          and fr66i["frontier_after"]["solved_s6_in_manifest"] == 1476
          and fr66i["frontier_after"]["sum_remaining_cost"] == 504389
          and fr66i["target_parent_affected"] is False, "")
    cp = reconc["current_parent"]
    check("reconc.current_parent",
          cp["head"] == "1476/174/6372/504389/4645/368303"
          and cp["parent"] == PARENT_HEX
          and cp["current_head1476"]["classification"] == "all_remaining_sterile_for_D10_receipts"
          and [r["hex"] for r in cp["current_head1476"]["remaining_rows"]] == [ROW_71, ROW_64]
          and [r["cost"] for r in cp["current_head1476"]["remaining_rows"]] == [71, 64]
          and cp["current_head1476"]["remaining_edge_cost"] == 135
          and cp["current_head1476"]["d10_receipt_closable"] is False
          and cp["current_head1476"]["s5_parent_closed"] is False
          and cp["current_pending_folds_on_this_parent"] == []
          and cp["win7_d10_bits_available_in_historical_rows"] == [19, 37, 49, 61, 69, 99]
          and cp["verified_certificate_bits_used_in_folds"] == [19, 37, 49, 61, 69]
          and cp["fallback_unextracted_bits"] == [99], "")
    # remaining rows == my join minus the 3 fold-closed rows, and == census sterile refs
    check("reconc.remaining_equals_join_minus_folds",
          set(x["hex"] for x in cp["current_head1476"]["remaining_rows"]) == set(join_hexes) - {ROW_76C, ROW_76D, ROW_77E}
          == {r["hex"] for r in entry["sterile_refs"]}, "")
    check("reconc.interpretation_guard_present",
          "does not prove LOSS" in reconc["interpretation_guard"] and "UNKNOWN" in reconc["unknown_status"], "")
    # old audit time-scope note: the old script's pending check read sweep-record fields
    check("hist.script_time_scope",
          'check("F.folds_pending"' in old_script and reconc["historical_audit"]["time_scope_note"].startswith("The prior F.folds_pending check"), "")

    all_pass = all(c["pass"] for c in CHECKS)
    out = {
        "schema": "n11-rank1-parent-head1476-reconciliation-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, verification-side crosscheck session (standard 11x11 weak-resolution)",
        "title": "independent crosscheck of the published head-1476 reconciliation of the rank-1 partial-STERILE S5 parent 00000000000000801202000040000000: pins, orbit join, fold-chain arithmetic, receipt/covers arithmetic, certificate re-hashes, mjs static check-set, and K0863 conflict scan",
        "source_main_head": SOURCE_MAIN_HEAD,
        "reconciled_result_commit": RECONC_RESULT_COMMIT,
        "reconciled_log_commit": RECONC_LOG_COMMIT,
        "inputs": {k: v for k, v in INPUT_PINS.items()},
        "method": "fourth-implementation D4 (coordinate transforms on the 11x11 grid; canon witnessed against both published cost-76c derived canon roots), independent orbit join over the raw 6,438-row head-1410 worklist, per-receipt covers/marginal set arithmetic, head-segment delta arithmetic across the three published folds, byte-level re-hash (sha256/md5/git-blob) of all six folded WIN7-D10 certificates from pinned raw files, static extraction of the published mjs verifier check-set, K0863 conflict scan (no STERILE row under any folded root or any D4 image of its one-stone reductions); no engine, no new verdict",
        "derived": {
            "orbit_join_rows": related,
            "join_total_cost": sum(x["cost"] for x in related),
            "fold_segments": [
                {"segment": "cost76d77e", "head_before": "1450/174/6398/506297/4671/370211", "head_after": "1452/174/6396/506144/4669/370058", "closed_rows": [ROW_76D, ROW_77E]},
                {"segment": "cost76c_bit61", "head_before": "1472/174/6376/504672/4649/368586", "head_after": "1473/174/6375/504596/4648/368510", "closed_rows": [ROW_76C]},
                {"segment": "cost66i_bit19", "head_before": "1473/174/6375/504596/4648/368510", "head_after": "1476/174/6372/504389/4645/368303", "closed_rows": marg66},
            ],
            "remaining_rows_head1476": [
                {"hex": ROW_71, "cost": 71, "category": "sterile"},
                {"hex": ROW_64, "cost": 64, "category": "sterile"},
            ],
            "folded_win_roots_scanned": [hx(r) for r in folded_roots],
        },
        "checks": CHECKS,
        "check_count": len(CHECKS),
        "all_pass": all_pass,
        "interpretation_guard": "This is a verification-side crosscheck of published bookkeeping and certificates. It creates no new engine verdict, closes no S5 parent, and proves no LOSS. The two remaining rows are STERILE, so K0863 excludes WIN7-D10 receipt closure for them; that is a depth-10 receipt-channel statement only.",
        "unknown_status": "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("checks:", len(CHECKS), "all_pass:", all_pass)
    for c in CHECKS:
        if not c["pass"]:
            print("FAIL:", c["check"], c["detail"][:200])
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
