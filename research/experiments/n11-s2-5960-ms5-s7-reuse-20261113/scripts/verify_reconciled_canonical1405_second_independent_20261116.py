#!/usr/bin/env python3
"""Second independent verification of the published cost-70g fork
reconciliation (commit ca0e8c42,
research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/
class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json,
new canonical head 1405/6443/509457/4713/373180).

The published reconciliation re-based the 7 cost-70g WIN7-D10 receipts on the
canonical 1400 head.  This verifier is an INDEPENDENT implementation of the
same merge from the opposite direction: it folds BOTH receipt sets (the 63h
bit-89 and 67d bit-97 covers plus the 7 cost-70g receipt covers) on the shared
cost-65m 1396 baseline, reproducing both published branch heads through their
published scripts in subprocesses, and asserts the resulting merged state
equals the published reconciled head field-by-field, with the regenerated
ranking and top-candidates CSVs asserted byte-identical to the published ones.
No new head is declared; the published reconciled head remains canonical.
"""
import csv
import hashlib
import json
import runpy
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS_63H = OUT / "class2-lane-cost63h-certificates"
CERTS_70G = OUT / "class2-lane-cost70g-certificates"
CHILD_H = "00000000000000801202000040080000"
CHILD_H_V = int(CHILD_H, 16)
CHILD_G = "00000000000000801202000040000001"
CHILD_G_V = int(CHILD_G, 16)
BIT_H = 89
ROOT_H = f"{CHILD_H_V | (1 << BIT_H):032x}"
ROOT_H_V = CHILD_H_V | (1 << BIT_H)
P1 = "00000000000000801202000040000000"
P2_H = "00000000000000801202000000080000"
P3_H = "00000000000000003800000001800000"
P2_I = "00000000000000403800000008000000"
P2_D = "00000000000000801002000001080000"
P2_G = "00000000000000003800000008000001"
AUDIT_BLOCKED = "00000000000000809082000000000000"
WIN_BITS_G = [18, 24, 28, 59, 89, 112, 120]


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def git_blob_sha_bytes(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


_orig_write_text = Path.write_text


def _write_text_lf(self, data, encoding=None, errors=None, newline=None):
    with self.open("w", encoding=encoding or "utf-8", errors=errors,
                   newline="\n") as f:
        f.write(data)


Path.write_text = _write_text_lf


# ---------- 1. reproduce the cost-65m chain head (1396, the common fork base) ----------
ns65m = runpy.run_path(str(HERE / "scripts" / "recompute_frontier_cost65m_receipts_20261116.py"))
s_1396 = ns65m["s_cur"]
st_1396 = ns65m["stF2"]
covers = ns65m["covers"]
manifest = ns65m["manifest"]
classes = ns65m["classes"]
summary_state = ns65m["summary_state"]
rem_1396 = ns65m["remF2"]
dem_1396 = ns65m["demF2"]
canon = ns65m["canon"]
prevB = set(ns65m["prev"])
for c in ns65m["certs"].values():
    prevB.add(int(c["root_hex"], 16))
assert st_1396["solved_s6_in_manifest"] == 1396 and st_1396["unique_remaining_s6"] == 6452
assert st_1396["sum_remaining_cost"] == 510115
assert st_1396["s6_needed_by_open_classes"] == 4722 and st_1396["cost_needed_by_open_classes"] == 373838
assert len(prevB) == 704, len(prevB)  # 696 + 8 cost-65m roots
sha, blen = git_blob_sha(OUT / "class-frontier-cost65m-receipts-recompute-20261116.json")
assert sha == "9798a9fc53b2277b17744737511354b1a830c4d2" and blen == 10414, \
    "regenerated cost-65m head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost65m-receipts-20261116.csv")
assert sha == "ad9a62f6a65f03016e957e01c61bf0b9675d2d0a" and blen == 7535
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost65m-receipts-20261116.csv")
assert sha == "6df96d8fb8fa9e2ea25a337b8bb8457ca3ef7c17" and blen == 4059
print("CONTROL cost-65m chain head reproduced byte-identically: "
      "1396/6452/510115/4722/373838 (head JSON + both CSVs blob == main)")

# ---------- 2. reproduce branch M (merged 63h+63i+63j+65m+67d, head 1400) ----------
# subprocess: the branch script re-runs the published fold chain (including
# its own branch C/D subprocess reproductions) with all its blob asserts and
# asserts its three output blobs byte-identical to main; the merged state is
# received through a dump file.
DUMP_M = OUT / "tmp-merge2-dump-branchM-20261116.json"
code_m = (
    "import runpy, json\n"
    "ns = runpy.run_path(str(%r))\n"
    "json.dump({\n"
    "  's_f': sorted(f'{k:032x}' for k in ns['s_f']),\n"
    "  'st_f': ns['st_f'],\n"
    "  'cov_h': sorted(f'{k:032x}' for k in ns['cov_h']),\n"
    "  'cov_d': sorted(f'{k:032x}' for k in ns['cov_d']),\n"
    "  'root_h': ns['ROOT_H'], 'bit_h': ns['BIT_H'],\n"
    "  'prev_all': sorted(f'{k:032x}' for k in ns['prev_all']),\n"
    "  'P1': ns['P1'], 'P2_H': ns['P2_H'], 'P3_H': ns['P3_H'],\n"
    "  'P2_I': ns['P2_I'], 'P2_D': ns['P2_D'],\n"
    "  'AUDIT_BLOCKED': ns['AUDIT_BLOCKED'],\n"
    "  'rows_63h': ns['ROWS_63H'], 'md5_63h': ns['MD5_63H'],\n"
    "}, open(%r, 'w'))\n"
) % (str(HERE / "scripts" /
         "recompute_frontier_merged_cost63h_63i_63j_65m_67d_20261116.py"), str(DUMP_M))
subprocess.run(["python3", "-c", code_m], check=True)
dumpM = json.loads(DUMP_M.read_text())
s_M = set(int(x, 16) for x in dumpM["s_f"])
st_M = dumpM["st_f"]
cov_h = set(int(x, 16) for x in dumpM["cov_h"])
cov_d = set(int(x, 16) for x in dumpM["cov_d"])
assert dumpM["root_h"] == ROOT_H and dumpM["bit_h"] == BIT_H
assert set(covers(ROOT_H_V)) == cov_h, "63h covers recomputed from the root"
prev_all = set(int(x, 16) for x in dumpM["prev_all"])
assert len(prev_all) == 705  # 704 branch-B roots + the 63h root
assert st_M["solved_s6_in_manifest"] == 1400 and st_M["unique_remaining_s6"] == 6448
assert st_M["sum_remaining_cost"] == 509842 and st_M["s6_needed_by_open_classes"] == 4718
assert st_M["cost_needed_by_open_classes"] == 373565
sha, blen = git_blob_sha(OUT / "class-frontier-merged-cost63h-63i-63j-65m-67d-recompute-20261116.json")
assert sha == "777474faf6730242b7e0080bfcdad390cca3a0ee" and blen == 7460, \
    "regenerated branch M head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-merged-cost63h-63i-63j-65m-67d-20261116.csv")
assert sha == "bd1c06140c69856764220563c3285d19251343ea" and blen == 7535
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-merged-cost63h-63i-63j-65m-67d-20261116.csv")
assert sha == "f9aa6e061279f3e84b830fbafe8d85403abbe7b6" and blen == 3887
print("CONTROL branch M (merged 63h+63i+63j+65m+67d fold) head reproduced: "
      "1400/6448/509842/4718/373565 (3 output blobs == main)")

# ---------- 3. reproduce branch G (cost-70g fold, head 1403) ----------
DUMP_G = OUT / "tmp-merge2-dump-branchG-20261116.json"
code_g = (
    "import runpy, json\n"
    "ns = runpy.run_path(str(%r))\n"
    "json.dump({\n"
    "  's_cur': sorted(f'{k:032x}' for k in ns['s_cur']),\n"
    "  'stF2': ns['stF2'],\n"
    "  'cov18': sorted(f'{k:032x}' for k in ns['cov18']),\n"
    "  'addition': ns['addition'],\n"
    "  'prev': sorted(f'{k:032x}' for k in ns['prev']),\n"
    "  'child': ns['CHILD'], 'p1': ns['PARENT1'], 'p2': ns['PARENT2'],\n"
    "  'win_bits': ns['WIN_BITS'],\n"
    "  'certs': {b: {'root_hex': c['root_hex'], 'md5': c['md5'], 'rows': c['rows'],\n"
    "               'd4': c['d4_canonical_hex'], 'bytes': c['bytes'],\n"
    "               'sub_roots': c['sub_roots_total'],\n"
    "               'loser_first_moves': c['loser_first_moves']}\n"
    "            for b, c in ns['certs'].items()},\n"
    "  'zero_mim': ns['zero_mim'], 'child_closed_by': ns['child_closed_by'],\n"
    "}, open(%r, 'w'))\n"
) % (str(HERE / "scripts" / "recompute_frontier_cost70g_receipts_20261116.py"), str(DUMP_G))
subprocess.run(["python3", "-c", code_g], check=True)
dumpG = json.loads(DUMP_G.read_text())
s_G = set(int(x, 16) for x in dumpG["s_cur"])
st_G = dumpG["stF2"]
cov_g_all = set(int(x, 16) for x in dumpG["cov18"])
assert dumpG["child"] == CHILD_G and dumpG["p1"] == P1 and dumpG["p2"] == P2_G
assert dumpG["win_bits"] == WIN_BITS_G and dumpG["child_closed_by"] == 18
certs_g = dumpG["certs"]
assert set(certs_g) == {str(b) for b in WIN_BITS_G}
cov_g_re = set()
for b, c in certs_g.items():
    cov_g_re |= covers(int(c["root_hex"], 16))
assert cov_g_re == cov_g_all, "70g union covers recomputed from the 7 roots"
assert st_G["solved_s6_in_manifest"] == 1403 and st_G["unique_remaining_s6"] == 6445
assert st_G["sum_remaining_cost"] == 509589 and st_G["s6_needed_by_open_classes"] == 4715
assert st_G["cost_needed_by_open_classes"] == 373312
sha, blen = git_blob_sha(OUT / "class-frontier-cost70g-receipts-recompute-20261116.json")
assert sha == "8eb71c91bd39f5899171dd588156e0c10a763c63" and blen == 9896, \
    "regenerated branch G head JSON must be byte-identical to main"
sha, blen = git_blob_sha(OUT / "class-frontier-s5-ranking-after-cost70g-receipts-20261116.csv")
assert sha == "df92f3d020358dd053c12e5d45aded2bf2dfce53" and blen == 7535
sha, blen = git_blob_sha(OUT / "class-frontier-top-candidates-s6-after-cost70g-receipts-20261116.csv")
assert sha == "22607d3ac5edbc746100cd524f25faf78b3039e6" and blen == 3887
print("CONTROL branch G (cost-70g fold) head reproduced: "
      "1403/6445/509589/4715/373312 (3 output blobs == main)")

# ---------- 4. fork set equalities, cover overlaps, root disjointness ----------
assert s_M == s_1396 | cov_h | cov_d, "set-equality of the branch M merged fold"
assert s_G == s_1396 | cov_d | cov_g_all, "set-equality of the branch G 70g fold"
overlap_cov_hg = cov_h & cov_g_all
assert overlap_cov_hg == {int("00000000020000801202000040000000", 16)}, \
    "the exact one-position raw overlap between the 63h covers and the 70g union covers"
overlap_g_in_M = cov_g_all & s_M
overlap_h_in_G = cov_h & s_G
assert len(overlap_g_in_M) == 10 and len(overlap_h_in_G) == 2
assert CHILD_H_V not in cov_g_all and CHILD_G_V not in cov_h
print(f"CONTROL fork covers: |cov(63h)|={len(cov_h)} |cov(67d)|={len(cov_d)} "
      f"|cov(70g union)|={len(cov_g_all)}; raw overlap cov(63h)&cov(70g)=1 "
      f"(non-manifest position {next(iter(overlap_cov_hg)):032x}); "
      f"cov(70g)&s_1400={len(overlap_g_in_M)} cov(63h)&s_1403={len(overlap_h_in_G)}")
roots_g = {int(certs_g[str(b)]["root_hex"], 16) for b in WIN_BITS_G}
d4_roots_g = {certs_g[str(b)]["d4"] for b in WIN_BITS_G}
prev_G = set(int(x, 16) for x in dumpG["prev"])
assert len(prev_G) == 705  # 704 branch-B roots + the 67d root
root_d_v = next(iter(prev_G - prev_all))
assert prev_all - prev_G == {ROOT_H_V}, "branch M prev adds exactly the 63h root"
assert prev_G - prev_all == {root_d_v}, "branch G prev adds exactly the 67d root"
assert prev_all ^ prev_G == {ROOT_H_V, root_d_v}
assert cov_d == covers(root_d_v), "67d covers recomputed from the 67d root"
assert not (roots_g & prev_all), "70g roots raw-disjoint from the 705 branch-M roots"
prev_all_d4 = {f"{canon(r):032x}" for r in prev_all}
assert not (d4_roots_g & prev_all_d4), "70g roots D4-disjoint from the 705 branch-M roots"
assert ROOT_H_V not in roots_g and f"{canon(ROOT_H_V):032x}" not in d4_roots_g
assert len(d4_roots_g) == 7
print("CONTROL root disjointness: 7 new 70g roots vs the 705 branch-M folded roots "
      "(including the 63h root) raw-hex and D4-canonically; the 63h root itself "
      "raw and D4-disjoint from the 7 70g roots")

# ---------- 5. re-assert all 8 published certificates against local bytes ----------
c63_path = CERTS_63H / f"bit{BIT_H}-root-{ROOT_H}.cert"
whole63 = c63_path.read_bytes()
assert hashlib.md5(whole63).hexdigest() == dumpM["md5_63h"]
lines63 = whole63.splitlines()
assert lines63[0] == b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
assert lines63[1] == b"root " + ROOT_H.encode()
assert len(lines63) - 2 == dumpM["rows_63h"] == 26070
assert dumpM["rows_63h"] == 26070 and dumpM["md5_63h"].startswith("b721d428")
sums = {"rows": 0, "bytes": 0, "sub_roots": 0}
for bit in WIN_BITS_G:
    c = certs_g[str(bit)]
    root = c["root_hex"]
    parts = sorted(CERTS_70G.glob(f"bit{bit}-root-{root}.cert.part*of2"))
    if parts:
        whole = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
    else:
        whole = (CERTS_70G / f"bit{bit}-root-{root}.cert").read_bytes()
    assert len(whole) == c["bytes"], bit
    assert hashlib.md5(whole).hexdigest() == c["md5"], bit
    assert whole.splitlines()[0] == b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
    assert whole.splitlines()[1] == b"root " + root.encode()
    assert len(whole.splitlines()) - 2 == c["rows"], bit
    assert f"{int(root, 16):032x}" == f"{CHILD_G_V | (1 << bit):032x}"
    sums["rows"] += c["rows"]
    sums["bytes"] += c["bytes"]
    sums["sub_roots"] += c["sub_roots"]
assert sums["rows"] == 350567 and sums["bytes"] == 12679157 and sums["sub_roots"] == 395
print(f"CONTROL certificates re-asserted against local bytes: 63h {dumpM['rows_63h']} rows "
      f"md5 {dumpM['md5_63h'][:8]}...; 70g 7/7 files {sums['rows']} rows / "
      f"{sums['bytes']} bytes / {sums['sub_roots']} sub-roots (BigInt + Number "
      "Bareiss union 0/0 asserted by the branch G reproduction)")

# ---------- 6. both children genuinely remaining at the 1396 fork baseline ----------
parents_h = {}
for name, h in (("parent1", P1), ("parent2", P2_H), ("parent3", P3_H)):
    rows = rem_1396.get(h, [])
    d = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows}
    assert CHILD_H in d, (name, "the 63h child must be a remaining row of this open parent")
    parents_h[name] = d
assert CHILD_G in parents_h["parent1"], \
    "the 70g child must be a remaining row of parent1 at the 1396 baseline"
assert (len(parents_h["parent1"]), sum(parents_h["parent1"].values())) == (9, 639)
assert (len(parents_h["parent2"]), sum(parents_h["parent2"].values())) == (69, 5265)
assert (len(parents_h["parent3"]), sum(parents_h["parent3"].values())) == (77, 5548)
rows_g2 = rem_1396.get(P2_G, [])
d2 = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rows_g2}
assert CHILD_G in d2 and (len(d2), sum(d2.values())) == (53, 4270)
d_dem_h = dem_1396[CHILD_H]
assert (d_dem_h["c1"], d_dem_h["c2"], d_dem_h["c4"]) == (0, 2, 2), d_dem_h
d_dem_g = dem_1396[CHILD_G]
assert (d_dem_g["c1"], d_dem_g["c2"], d_dem_g["c4"]) == (0, 2, 0), d_dem_g
print("CONTROL both children genuinely remaining at the 1396 fork baseline: "
      "the 63h child in three open parents (9/639, 69/5265, 77/5548, demand "
      "c1=0,c2=2,c4=2), the 70g child in parent1 (9/639) and its own parent2 "
      "(53/4270, demand c1=0,c2=2,c4=0)")

# ---------- 7. fold both receipt sets on the common 1396 baseline ----------
s_f = s_1396 | cov_h | cov_d | cov_g_all
assert s_f == s_M | cov_g_all == s_G | cov_h
marg_g = cov_g_all - s_M
marg_g_m = marg_g & manifest
marg_h2 = cov_h - s_G
marg_h2_m = marg_h2 & manifest
assert len(marg_g) == 33 and len(marg_g_m) == 5
assert len(marg_h2) == 5 and len(marg_h2_m) == 2
assert CHILD_G_V in marg_g_m and CHILD_H_V in marg_h2_m
assert CHILD_H_V in s_f and CHILD_G_V in s_f
st_f, rem_f, uniq_f, dem_f = summary_state(s_f)
assert st_f["solved_s6_in_manifest"] == 1400 + len(marg_g_m) == 1403 + len(marg_h2_m)
assert st_f["solved_s6_in_manifest"] == 1405
assert st_f["unique_remaining_s6"] == 6443 and st_f["sum_remaining_cost"] == 509457
assert st_f["s6_needed_by_open_classes"] == 4713 and st_f["cost_needed_by_open_classes"] == 373180
print("AFTER merged fold:", json.dumps(st_f, indent=1))
print(f"70g receipts on the 1400 head: marginal={len(marg_g)} in-manifest={len(marg_g_m)}; "
      f"63h receipt on the 1403 head: marginal={len(marg_h2)} in-manifest={len(marg_h2_m)}")

# ---------- 8. reverse-order replay control ----------
s_alt = s_G | cov_h
assert s_alt == s_f, "reverse-order replay (the 63h covers on the 1403 head) must "
"reproduce the identical merged set"
st_alt, rem_alt, uniq_alt, dem_alt = summary_state(s_alt)
assert st_alt == st_f and dem_alt == dem_f
s_alt2 = s_M | cov_g_all
assert s_alt2 == s_f
print("CONTROL reverse-order replay: identical merged set and summary (both directions)")

# ---------- 9. per-parent rows at the merged head ----------
rows_after = {}
for name, h in (("parent1", P1), ("parent2", P2_H), ("parent3", P3_H),
                ("parent2_67d", P2_D), ("parent2_63i", P2_I), ("parent2_70g", P2_G)):
    rows_after[name] = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_f.get(h, [])}
lost_h = {name: set(parents_h[name]) - set(rows_after[name])
          for name in ("parent1", "parent2", "parent3")}
cov_h_hexes = {f"{k:032x}" for k in cov_h}
cov_d_hexes = {f"{k:032x}" for k in cov_d}
cov_g_hexes = {f"{k:032x}" for k in cov_g_all}
for name in ("parent1", "parent2", "parent3"):
    assert CHILD_H in lost_h[name], name
    assert lost_h[name] <= cov_h_hexes | cov_d_hexes | cov_g_hexes, (name, sorted(lost_h[name]))
assert CHILD_G in lost_h["parent1"]
lost_g2 = set(d2) - set(rows_after["parent2_70g"])
assert CHILD_G in lost_g2 and lost_g2 <= cov_g_hexes, sorted(lost_g2)
assert (len(rows_after["parent1"]), sum(rows_after["parent1"].values())) == (6, 439)
assert (len(rows_after["parent2"]), sum(rows_after["parent2"].values())) == (68, 5202)
assert (len(rows_after["parent3"]), sum(rows_after["parent3"].values())) == (75, 5416)
assert (len(rows_after["parent2_67d"]), sum(rows_after["parent2_67d"].values())) == (82, 6269)
assert (len(rows_after["parent2_63i"]), sum(rows_after["parent2_63i"].values())) == (24, 1704)
assert (len(rows_after["parent2_70g"]), sum(rows_after["parent2_70g"].values())) == (48, 3885)
print("per-parent rows at the merged head: "
      f"parent1 {len(rows_after['parent1'])}/{sum(rows_after['parent1'].values())}; "
      f"parent2_dual {len(rows_after['parent2'])}/{sum(rows_after['parent2'].values())}; "
      f"parent3_class4 {len(rows_after['parent3'])}/{sum(rows_after['parent3'].values())}; "
      f"parent2_67d {len(rows_after['parent2_67d'])}/{sum(rows_after['parent2_67d'].values())}; "
      f"parent2_63i {len(rows_after['parent2_63i'])}/{sum(rows_after['parent2_63i'].values())}; "
      f"parent2_70g {len(rows_after['parent2_70g'])}/{sum(rows_after['parent2_70g'].values())}")

# ---------- 10. per-receipt addition records on the merged baseline ----------
addition_g_on_1400 = []
s_run = set(s_M)
child_closed_by_g = None
for bit in WIN_BITS_G:
    c = certs_g[str(bit)]
    root_v = int(c["root_hex"], 16)
    cov = covers(root_v)
    marg = cov - s_run
    marg_m = marg & manifest
    if CHILD_G_V in marg_m:
        assert child_closed_by_g is None
        child_closed_by_g = bit
    addition_g_on_1400.append({
        "bit": bit, "root_hex": c["root_hex"], "d4_canonical_hex": c["d4"],
        "certified": True, "covers": len(cov), "marginal": len(marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
        "marginal_non_manifest_hexes": sorted(f"{k:032x}" for k in marg - marg_m),
        "rows": c["rows"], "md5": c["md5"], "sub_roots_pass": c["sub_roots"],
        "loser_first_moves": c["loser_first_moves"],
    })
    s_run |= marg
assert s_run == s_f and child_closed_by_g == 18
addition_h_on_1403 = {
    "bit": BIT_H, "root_hex": ROOT_H, "certified": True,
    "covers": len(cov_h), "marginal": len(marg_h2),
    "marginal_in_manifest": len(marg_h2_m),
    "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_h2_m),
    "marginal_non_manifest_hexes": sorted(f"{k:032x}" for k in marg_h2 - marg_h2_m),
    "rows": dumpM["rows_63h"], "md5": dumpM["md5_63h"],
}


# ---------- 11. rankings at the merged head ----------
def best(rem, bit):
    return sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"], r["s5_hex"]))


class2 = best(rem_f, 2)
class4 = best(rem_f, 4)
ranking = sorted(
    ({"s5_hex": k, "classes": classes.get(k, 0),
      "remaining_s6_orbits": len(rows),
      "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows)}
     for k, rows in rem_f.items()),
    key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                   r["remaining_s7_edge_cost"], r["s5_hex"]))

# ---------- 11b. independent merged state vs the published reconciled head ----------
REC = OUT / "class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json"
sha, blen = git_blob_sha(REC)
assert sha == "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb" and blen == 11352, \
    "the published reconciled head JSON must be the one from commit ca0e8c42"
rec = json.loads(REC.read_text())
fa = rec["frontier_after_reconciled"]
assert fa["solved_s6_in_manifest"] == st_f["solved_s6_in_manifest"] == 1405
assert fa["unique_remaining_s6"] == st_f["unique_remaining_s6"] == 6443
assert fa["sum_remaining_cost"] == st_f["sum_remaining_cost"] == 509457
assert fa["s6_needed_by_open_classes"] == st_f["s6_needed_by_open_classes"] == 4713
assert fa["cost_needed_by_open_classes"] == st_f["cost_needed_by_open_classes"] == 373180
assert fa["remaining_s5_orbits"] == st_f["remaining_s5_orbits"] == 174
assert fa["demand_histogram_open_only"] == st_f["hist"]
mine = {
    "best_class2": class2[0],
    "audit_blocked_class2": next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None),
    "best_coverable_class2": next((c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED), None),
    "next_class2": class2[1:4],
    "best_class4": class4[0],
    "next_class4": class4[1:4],
}
for key in ("best_class2", "audit_blocked_class2", "best_coverable_class2",
            "next_class2", "best_class4", "next_class4"):
    assert fa[key] == mine[key], key
pa = rec["parents_at_reconciled_head"]
expect_parents = {
    "second_candidate_s5": (P1, "parent1"),
    "cost70g_parent2": (P2_G, "parent2_70g"),
    "dual_class2_4_s5": (P2_H, "parent2"),
    "class4_s5": (P3_H, "parent3"),
    "cost67d_parent2": (P2_D, "parent2_67d"),
    "cost63i_second_parent": (P2_I, "parent2_63i"),
}
for key, (h, rn) in expect_parents.items():
    assert pa[key]["s5_hex"] == h, key
    assert pa[key]["rows"] == len(rows_after[rn]), key
    assert pa[key]["edge_cost"] == sum(rows_after[rn].values()), key
add_rec = rec["cost70g_addition_on_canonical1400"]
assert len(add_rec) == len(addition_g_on_1400) == 7
for a, b in zip(add_rec, addition_g_on_1400):
    for k in ("bit", "root_hex", "d4_canonical_hex", "covers", "marginal",
              "marginal_in_manifest", "marginal_manifest_hexes",
              "marginal_non_manifest_hexes", "rows", "md5", "sub_roots_pass"):
        assert a[k] == b[k], (a["bit"], k)
assert rec["totals"]["total_marginal"] == 33 and rec["totals"]["total_marginal_in_manifest"] == 5
assert rec["totals"]["zero_marginal_in_manifest"] == ["bit59", "bit89", "bit112"]
assert rec["totals"]["child_closed_by_bit"] == 18
assert rec["totals"]["certificate_rows"] == sums["rows"] == 350567
assert rec["totals"]["certificate_bytes"] == sums["bytes"] == 12679157
print("CONTROL published reconciled head JSON equals this independent merged state: "
      "frontier 1405/6443/509457/4713/373180, histogram, best/next rankings, all "
      "six parents, per-bit addition records, totals (field-by-field)")

# ---------- 12. regenerated CSVs byte-identical to the published ones ----------
import io


def ranking_csv_bytes():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(("s5_hex", "classes", "remaining_s6_orbits", "remaining_s7_edge_cost"))
    for r in ranking:
        w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                    r["remaining_s7_edge_cost"]))
    return buf.getvalue().encode()


def topcand_csv_bytes():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_BLOCKED]
    for label, cand in (("best class-4 blocker-candidate S5", class4[0] if class4 else None),
                        ("best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)",
                         next((c for c in class2 if c["s5_hex"] == AUDIT_BLOCKED), None)),
                        ("best coverable class-2 blocker-candidate S5",
                         coverable[0] if coverable else None),
                        ("second coverable class-2 candidate S5",
                         coverable[1] if len(coverable) > 1 else None)):
        if cand is None:
            continue
        rows = rem_f.get(cand["s5_hex"], [])
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
        for row in sorted(rows, key=lambda r: int(r["s6_s7_edge_cost"])):
            d = dem_f[row["s6_hex"]]
            w.writerow((cand["s5_hex"], row["s6_hex"], row["s6_s7_edge_cost"],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
    return buf.getvalue().encode()


REC_RANK = OUT / "class-frontier-s5-ranking-after-reconciled-canonical1400-cost70g-20261116.csv"
REC_TOP = OUT / "class-frontier-top-candidates-s6-after-reconciled-canonical1400-cost70g-20261116.csv"
sha_pub_rank, blen_rank = git_blob_sha(REC_RANK)
sha_pub_top, blen_top = git_blob_sha(REC_TOP)
assert sha_pub_rank == "26fa720b9935ea3bfa1445409d941a5063c52694" and blen_rank == 7535
assert sha_pub_top == "c3433eeecccf0098a04f227af876b37196c7c0a5" and blen_top == 3801
assert ranking_csv_bytes() == REC_RANK.read_bytes(), \
    "the regenerated ranking CSV must be byte-identical to the published one"
assert topcand_csv_bytes() == REC_TOP.read_bytes(), \
    "the regenerated top-candidates CSV must be byte-identical to the published one"
print("CONTROL regenerated ranking CSV (7535 B) and top-candidates CSV (3801 B) "
      "are byte-identical to the published reconciliation outputs")

# ---------- 13. verification output ----------
verification = {
    "schema": "n11-class2-lane-reconciled-canonical1405-second-independent-verification-20261116-v1",
    "date": "2026-11-16",
    "verified": "class-frontier-reconciled-canonical1400-cost70g-recompute-20261116.json "
                "(git blob sha b3ad19d7bfd48c771d5a6827707a9f26940dc1bb, 11352 bytes, "
                "commit ca0e8c4230444d51540d86e1987a05b16dd7e8c5)",
    "method": "independent implementation of the same merge from the opposite "
              "direction: both receipt sets (the 63h bit-89 cover, the 67d "
              "bit-97 cover and the 7 cost-70g receipt covers) folded on the "
              "shared cost-65m 1396 baseline, with both published branch heads "
              "(1400 and 1403) reproduced through their published scripts in "
              "subprocesses (all blob asserts re-run), fork set equalities, the "
              "cover overlap facts pinned (cov(63h) & cov(70g) == 1 raw "
              "non-manifest position 00000000020000801202000040000000; "
              "cov(70g) & s_1400 == 10; cov(63h) & s_1403 == 2), root "
              "disjointness (7 70g roots vs the 705 branch-M roots raw + D4), "
              "all 8 published certificates re-asserted against local bytes, "
              "dual-direction reverse-order replays, then the merged state "
              "asserted equal to the published reconciled head field-by-field "
              "and both regenerated CSVs asserted byte-identical",
    "controls": {
        "both_branch_heads_reproduced_byte_identical": True,
        "fork_set_equalities": True,
        "cover_overlap_cov63h_cov70g": "1 raw non-manifest position (no solved effect)",
        "root_disjointness_70g_vs_705": True,
        "certificates_bytes_md5_verified": True,
        "reverse_order_replay_identical_both_directions": True,
        "published_head_json_field_by_field_equal": True,
        "published_head_json_blob_pinned": "b3ad19d7bfd48c771d5a6827707a9f26940dc1bb",
        "ranking_csv_byte_identical": "26fa720b9935ea3bfa1445409d941a5063c52694 (7535 B)",
        "top_candidates_csv_byte_identical": "c3433eeecccf0098a04f227af876b37196c7c0a5 (3801 B)",
        "frontier": "1405/6443/509457/4713/373180",
        "per_bit_addition_records_equal": True,
        "parents_equal": True,
        "totals_equal": True,
    },
    "result": "VERIFIED: the published reconciliation head "
              "1405/6443/509457/4713/373180 is reproduced byte-identically "
              "(both CSVs) and field-by-field (head JSON) by this independent "
              "opposite-direction implementation; the published reconciled "
              "head remains canonical",
    "interpretation_guard": "bookkeeping verification over published receipts; "
                            "no new head is declared here; solved counts measure "
                            "manifest coverage, not the game-theoretic value of "
                            "any position; REFUTED-D10 sweeps prove only absence "
                            "of WIN7-D10; WIN7 certificates prove a win within "
                            "depth 10 from the individual 7-stone roots only; "
                            "11x11 empty board / two-stone root {49,60} / "
                            "S2 {59,60} / class 1 / class 2 / class 4 remain UNKNOWN",
}
VOUT = OUT / "class2-lane-reconciled-canonical1405-second-independent-verification-20261116.json"
VOUT.write_text(json.dumps(verification, indent=1) + "\n")
sha_v, blen_v = git_blob_sha(VOUT)
print(f"written class2-lane-reconciled-canonical1405-second-independent-verification-20261116.json: "
      f"blob {sha_v} ({blen_v} bytes)")
print("SECOND INDEPENDENT VERIFICATION PASSED: reconciled canonical head "
      "1405/6443/509457/4713/373180")
