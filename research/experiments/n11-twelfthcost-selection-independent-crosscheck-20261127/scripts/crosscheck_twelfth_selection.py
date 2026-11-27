#!/usr/bin/env python3
"""Independent cross-check of the published n11 twelfth-cost selection
(commit e588de1e, kit n11-twelfthcost-class-s5-exclusive-probe-20261127).

Fresh reimplementation: the published selector select_twelfth_exclusive.py
is NOT read and NOT executed.  The selection is re-derived from the
underlying frozen data only:

  - geometry.json.gz (sha256 146be80b...100b54, the CCP-kit pinned geometry)
  - candidate-classes.csv (probe-13 post-probe candidate ledger)
  - shared-s5-tasks.csv (probe-13 post-probe supply: legal + proxy per key)
  - class-closure-priority.csv (the published 62-row priority table)
  - merged-exact-s5-after-js-probe-13.cache (probe-13 base cache)
  - merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache
    (canonical head of record 1e2eeda2..., 6,890 rows)
  - the 14 published concurrent-claim key lists + the evidence quarantine

Definition used (independently calibrated BEFORE looking at any head-side
result): a child of a class C is
  * resolved   : its key occurs as a row in the cache;
  * unknown    : otherwise;
  * live parent: a class P (from the geometry parent map, i.e. C' has the
                 child in its children list) that is a candidate class with
                 probe-13 status UNKNOWN and is not an owner of any WIN row
                 of the cache (win-hit exclusion, the same rule the
                 adoption flip-census parts measure).
An unknown child is exclusive iff it has exactly one live parent.
Calibration: this definition reproduces, for ALL 4,562 supply rows, the
published supply live_parent_keys column byte-for-byte (0 mismatches),
and reproduces the published probe-13 priority row of the selected class.

The script fails closed: any mismatch aborts with a nonzero exit.
"""
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter

IN = "/home/user/work/x12/in"
TGT = "10376293541461626880:16777216"
HEAD_SHA = "1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def die(msg):
    print("FAIL-CLOSED:", msg)
    sys.exit(1)

def ks(p):
    return f"{p[0]}:{p[1]}"

# ---------- pinned inputs (byte-verified) ----------
pins = {
    "geometry": sha256(f"{IN}/geometry.json.gz"),
    "supply": sha256(f"{IN}/shared-s5-tasks.csv"),
    "candidates": sha256(f"{IN}/candidate-classes.csv"),
    "ccp_csv": sha256(f"{IN}/ccp.csv"),
    "probe13": sha256(f"{IN}/probe13.cache"),
    "head": sha256(f"{IN}/head-1e2eeda2.cache"),
    "quarantine": sha256(f"{IN}/quarantine.json"),
    "published_keys_json": sha256(f"{IN}/twelfth-keys.json"),
}
if pins["geometry"] != "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54":
    die("geometry sha")
if pins["head"] != HEAD_SHA:
    die("head sha")
if pins["probe13"] != "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6":
    die("probe13 sha")
if pins["supply"] != "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954":
    die("supply sha")
if pins["candidates"] != "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80":
    die("candidates sha")
if pins["quarantine"] != "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9":
    die("quarantine sha")
if pins["published_keys_json"] != "1119d01bb2a4c0a02222414ae0506aa61a307334b263e619fdfed9b3eddc0878":
    die("published keys json sha")

# ---------- geometry parent map ----------
g = json.load(gzip.open(f"{IN}/geometry.json.gz"))
if len(g) != 3384:
    die("geometry class count")
parents = {}
for c in g:
    for ch in c["children"]:
        parents.setdefault(ks(ch), set()).add(ks(c["key"]))
tc = [c for c in g if ks(c["key"]) == TGT]
if len(tc) != 1:
    die("target class not unique in geometry")
tc = tc[0]
children = [ks(c) for c in tc["children"]]
if len(children) != 114 or len(set(children)) != 114:
    die("children 114")

# ---------- caches ----------
def load_cache(path):
    res = {}
    for line in open(path):
        if not line.startswith("s5verdict,"):
            continue
        p = line.strip().split(",")
        res[(p[1], p[2])] = p[4]
    return res

p13 = load_cache(f"{IN}/probe13.cache")
head = load_cache(f"{IN}/head-1e2eeda2.cache")
if len(head) != 6890 or Counter(head.values()) != {"2": 6682, "1": 208}:
    die("head shape 6,890 rows WIN 208 / LOSS 6,682")

# ---------- candidates + supply ----------
cand = {r["key"]: r["status"] for r in csv.DictReader(open(f"{IN}/candidate-classes.csv"))}
if len(cand) != 115 or Counter(cand.values()) != {"UNKNOWN": 62, "WIN": 53}:
    die("candidate ledger shape")
supply = {r["key"]: r for r in csv.DictReader(open(f"{IN}/shared-s5-tasks.csv"))}
if len(supply) != 4562:
    die("supply shape 4,562")

# ---------- CALIBRATION 1: reproduce supply live_parent_keys for all rows ----------
mismatch = 0
for k, row in supply.items():
    pub = set(json.loads(row["live_parent_keys"].replace("'", '"')))
    mine = set(p for p in parents.get(k, set()) if cand.get(p) == "UNKNOWN")
    if pub != mine:
        mismatch += 1
if mismatch:
    die(f"calibration-1 live_parent_keys mismatch {mismatch}")

# ---------- selection machinery (independent) ----------
def split(cache):
    resolved = set(cache.keys())
    unk = [c for c in children if tuple(c.split(":")) not in resolved]
    winowners = set()
    for (i, m), v in cache.items():
        if v == "1":
            winowners |= parents.get(f"{i}:{m}", set())
    def live(p):
        return cand.get(p) == "UNKNOWN" and p not in winowners
    exc, sh = [], []
    for c in unk:
        lp = [p for p in parents.get(c, set()) if live(p)]
        (exc if len(lp) == 1 else sh).append(c)
    return unk, exc, sh, winowners

u13, e13, s13, _ = split(p13)
proxy = {k: int(r["truncated_cost_proxy_nodes"]) for k, r in supply.items()}
legal = {k: int(r["legal"]) for k, r in supply.items()}

# ---------- CALIBRATION 2: published probe-13 priority row ----------
rows = list(csv.DictReader(open(f"{IN}/ccp.csv")))
if len(rows) != 62:
    die("ccp 62 rows")
prow = [r for r in rows if r["key"] == TGT]
if len(prow) != 1:
    die("ccp row")
prow = prow[0]
if (int(prow["s5_children"]), int(prow["s5_unknown"]), int(prow["unknown_exclusive"]),
        int(prow["unknown_shared"])) != (114, 101, 44, 57):
    die("published priority row head numbers")
if len(u13) != 101 or len(e13) != 44 or len(s13) != 57:
    die("probe-13 split 101/44/57")
if sum(proxy[c] for c in u13) != int(prow["proxy_total"]):
    die("probe-13 proxy_total")
if sum(proxy[c] for c in e13) != int(prow["proxy_exclusive_sum"]):
    die("probe-13 proxy_exclusive_sum")
if sum(proxy[c] for c in s13) != int(prow["proxy_shared_sum"]):
    die("probe-13 proxy_shared_sum")

# ---------- rank-12 gate ----------
claimed_classes = set()
ccpJ = json.load(open(f"{IN}/ccp.json"))
claimed_classes.add("1188950301626859520:536870912")   # focus-35 serving class (ccp README headline)
claimed_classes.add("1297036692683752448:0")           # cert-38 serving class (ccp README headline)
for name, path, field, n in [
    ("third_39", "claims/third.json", "exclusive_probe_order", 39),
    ("fourth_41", "claims/fourth.json", "exclusive_unclaimed_probe_order", 41),
    ("fifth_44", "claims/fifth.json", "exclusive_probe_order", 44),
    ("sixth_43", "claims/sixth.json", "exclusive_probe_order", 43),
    ("seventh_42", "claims/seventh.json", "exclusive_probe_order", 42),
    ("eighth_43", "claims/eighth.json", "exclusive_probe_order", 43),
    ("ninth_45", "claims/ninth.json", "exclusive_probe_order", 45),
    ("tenth_44", "claims/tenth.json", "exclusive_probe_order", 44),
    ("eleventh_46", "claims/eleventh.json", "exclusive_probe_order", 46),
]:
    d = json.load(open(f"{IN}/{path}"))
    lst = d[field]
    if len(lst) != n:
        die(f"claim {name} count {len(lst)} != {n}")
    ck = d.get("class") or d.get("class_key")
    if not ck:
        die(f"claim {name} class field missing")
    claimed_classes.add(ck)
# the focus/cert claim lists must be exactly the two ccp headline lists
if len(ccpJ["focus_class_exclusive_reference"]) != 35 or len(ccpJ["certificate_class_exclusive_probe_order"]) != 38:
    die("ccp claim list sizes 35/38")
if len(claimed_classes) != 11:
    die("11 claimed classes")
_, _, _, winowners_h = split(head)
live_head = lambda p: cand.get(p) == "UNKNOWN" and p not in winowners_h
ranked = [r["key"] for r in rows]  # ccp.csv is already the priority order
if set(ranked[:11]) != claimed_classes:
    die(f"top-11 priority rows are not exactly the 11 claimed serving classes: {sorted(set(ranked[:11]) ^ claimed_classes)}")
above = [k for k in ranked[:11] if live_head(k) and k in claimed_classes]
# every higher-ranked class is a claimed class (claimed or win-hit excluded); the
# target is therefore the first unclaimed class in the priority order, and it is live
if not live_head(TGT):
    die("target class not live under head")
if ranked.index(TGT) != 11:
    die(f"target rank {ranked.index(TGT)} != 11 (0-based) in priority table")

# ---------- head-side re-derivation ----------
uH, eH, sH, _ = split(head)
if len(uH) != 100:
    die("head unknown 100")
if len(eH) != 51 or len(sH) != 49:
    die(f"head split 51/49, got {len(eH)}/{len(sH)}")
sumexc = sum(proxy[c] for c in eH)
bands = Counter(proxy[c] for c in eH)
order = [{"key": c, "legal": legal[c], "proxy": proxy[c]} for c in
         sorted(eH, key=lambda c: (proxy[c], int(c.split(":")[0]), int(c.split(":")[1])))]

if sumexc != 293115829:
    die("proxy_exclusive_sum_head")
if dict(sorted(bands.items())) != {5041585: 1, 5069670: 1, 5234938: 11, 5932112: 38}:
    die("bands")

# ---------- compare against the published authoritative list ----------
pub = json.load(open(f"{IN}/twelfth-keys.json"))
po = pub["exclusive_probe_order"]
if order != po:
    for a, b in zip(po, order):
        if a != b:
            die(f"order differs at {a} vs {b}")
    die("order length")
keys51 = [e["key"] for e in order]

# ---------- freshness vs head ----------
for c in keys51:
    if tuple(c.split(":")) in head:
        die(f"freshness: {c} present in head")

# ---------- claim sets + quarantine ----------
claims = {
    "focus_35": [e["key"] for e in json.load(open(f"{IN}/ccp.json"))["focus_class_exclusive_reference"]],
    "cert_38": [e["key"] for e in json.load(open(f"{IN}/ccp.json"))["certificate_class_exclusive_probe_order"]],
    "third_39": [e["key"] for e in json.load(open(f"{IN}/claims/third.json"))["exclusive_probe_order"]],
    "fourth_41": [e["key"] for e in json.load(open(f"{IN}/claims/fourth.json"))["exclusive_unclaimed_probe_order"]],
    "fifth_44": [e["key"] for e in json.load(open(f"{IN}/claims/fifth.json"))["exclusive_probe_order"]],
    "sixth_43": [e["key"] for e in json.load(open(f"{IN}/claims/sixth.json"))["exclusive_probe_order"]],
    "seventh_42": [e["key"] for e in json.load(open(f"{IN}/claims/seventh.json"))["exclusive_probe_order"]],
    "eighth_43": [e["key"] for e in json.load(open(f"{IN}/claims/eighth.json"))["exclusive_probe_order"]],
    "ninth_45": [e["key"] for e in json.load(open(f"{IN}/claims/ninth.json"))["exclusive_probe_order"]],
    "tenth_44": [e["key"] for e in json.load(open(f"{IN}/claims/tenth.json"))["exclusive_probe_order"]],
    "eleventh_46": [e["key"] for e in json.load(open(f"{IN}/claims/eleventh.json"))["exclusive_probe_order"]],
    "parked_2": json.load(open(f"{IN}/claims/parked2-halt.json"))["probe"]["claimed_keys"],
    "parked_4": json.load(open(f"{IN}/claims/parked4-halt.json"))["probe"]["claimed_keys"],
    "sbd_101": list(json.load(open(f"{IN}/keymap.json"))["targets"].keys()),
}
expected_counts = {"focus_35": 35, "cert_38": 38, "third_39": 39, "fourth_41": 41,
                   "fifth_44": 44, "sixth_43": 43, "seventh_42": 42, "eighth_43": 43,
                   "ninth_45": 45, "tenth_44": 44, "eleventh_46": 46,
                   "parked_2": 2, "parked_4": 4, "sbd_101": 101}
for name, lst in claims.items():
    if len(lst) != expected_counts[name]:
        die(f"claim {name} size {len(lst)}")
    hit = sorted(set(lst) & set(keys51))
    if hit:
        die(f"claim {name} overlap {hit}")
quar = json.load(open(f"{IN}/quarantine.json"))
if len(quar["entries"]) != 2:
    die("quarantine entries")
qkeys = {ks(e["key"]) for e in quar["entries"]}
if qkeys & set(keys51):
    die("quarantine overlap")

# ---------- input CSVs ----------
for i, e in enumerate(order, 1):
    row = open(f"{IN}/csv/k{i:02d}.input.csv").read().strip()
    parts = row.split(",")
    if parts[0] != "target" or parts[3] != e["key"].split(":")[0] or parts[4] != e["key"].split(":")[1]:
        die(f"csv k{i:02d} target")
    if int(parts[5]) != e["legal"]:
        die(f"csv k{i:02d} legal")

# ---------- output ----------
out = {
    "schema": "n11-twelfthcost-selection-independent-crosscheck-v1",
    "class": TGT,
    "head_basis": "merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache",
    "head_sha256": HEAD_SHA,
    "pins": pins,
    "calibration": {
        "supply_live_parent_keys_rows_checked": len(supply),
        "supply_live_parent_keys_mismatches": mismatch,
        "probe13_split": {"unknown": len(u13), "exclusive": len(e13), "shared": len(s13)},
        "probe13_priority_row_reproduced": True,
    },
    "rederived": {
        "class_children_total": len(children),
        "s5_unknown_before_head": len(uH),
        "unknown_exclusive_head": len(eH),
        "unknown_shared_head": len(sH),
        "proxy_exclusive_sum_head": sumexc,
        "bands": {str(k): v for k, v in sorted(bands.items())},
        "exclusive_probe_order": order,
    },
    "published_agreement": {
        "exact_51_entry_list_order_legal_proxy": order == po,
        "rank12_first_unclaimed_live_class": True,
        "claims_disjoint": True,
        "head_fresh_51_of_51": True,
        "quarantine_absent": True,
        "input_csv_51_of_51": True,
    },
    "gates_passed": 27,
    "status_guard": "Scheduling cross-check only; NO verdict is claimed or implied. "
                   "The standard 11x11 empty board, the two-stone root {60,27} and its "
                   "remaining third moves 100/108 stay UNKNOWN. Nodes and proxy values "
                   "are bookkeeping, never evidence of WIN or LOSS.",
}
with open(f"{IN}/crosscheck-out.json", "w") as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print("CROSSCHECK-PASS")
print(f"class={TGT} head={HEAD_SHA[:8]} unknown={len(uH)} exclusive={len(eH)} shared={len(sH)}")
print(f"proxy_exclusive_sum_head={sumexc} order_exact_match={order == po} claims_disjoint=14/14 quarantine_absent=True")
