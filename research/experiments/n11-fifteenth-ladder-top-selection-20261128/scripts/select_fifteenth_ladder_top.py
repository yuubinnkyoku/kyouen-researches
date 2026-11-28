"""Fifteenth closure-ladder top-candidate selection under the canonical
head of record a66f636e (fourteenth k01 adoption, 6,897 rows WIN 215 /
LOSS 6,682) plus the update8 receipts.

Purpose (scheduling bookkeeping only, no verdict claimed or consumed):
the published fourteenth k01 adoption reaudit closure ladder
(reaudit/output/closure-classes.csv, sha256 8fe6125f..., 799 rows)
shows, at its top, class 5804 with exactly three remaining unknown S5
children under the current head (the adopted k01 WIN row resolved one
of the four). Resolving all three keys would complete the class (a
candidate free_now flip for the adaptive coordinator, Board-verified
at adoption time). This instrument - a structural adaptation of the
published fourteenth selection instrument
(select_fourteenth_ladder_top.py, sha256 eb776f38...; the refresh
machinery itself is NOT read or executed) - independently recomputes
the per-class unknown_now counts for ALL 799 ladder rows from the
frozen dependency graph (54f9c364...), the head of record and the
update8 receipts (the same trust boundary the published refresh uses,
fresh re-implementation), gates the published top-5 ladder rows,
selects the first ladder class whose remaining unknown S5 keys are
ALL unclaimed, fresh, quarantine-free, 5-stone, D4-canonical and
canonical-safe, and re-derives each selected key's legal move count
with two independent implementations (the repo independent.py Board
and a fresh integer 4x4-determinant concyclicity implementation).

Fail-closed: rc=1 on any gate failure.
"""
from __future__ import annotations

import ast as _ast
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path("/home/user/repo")
GEOM_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
CAND_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
QUAR_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
HEAD_SHA = "a66f636ed4314b7385b713ed6e24798409db0b284eb252a9bda626ad3dcd67dc"
CLOSURE_SHA = "8fe6125f070ad472b02a7d41069fe9409f958e807955b35e7eb0c8282c67a385"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
HEAD_ROWS, HEAD_WIN, HEAD_LOSS = 6897, 215, 6682
LADDER_ROWS = 799
EXPECTED_TOP5 = [(5804, 3), (20421, 5), (34269, 11), (12264, 33), (5343, 46)]
EXPECTED_SELECTION_CLASS = 5804
EXPECTED_SELECTION_KEYS = [("6053682324116078592", 0),
                           ("6052837899185946628", 128), ("6053400849139367936", 128)]
EXPECTED_SELECTION_S5_INDEX = [207094, 212115, 212536]
ULTRA_CHEAP_4 = ["1153485622925590528:0", "1297036830121656320:131074",
                 "1153202979851993088:272", "1152921505747697664:1032"]
THIRTEENTH_2 = ["1153204147814662144:65536", "1152922672837951488:65792"]
FOURTEENTH_1 = ["6053401124017274880:0"]

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
SUPPLY = ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/shared-s5-tasks.csv"
CAND = ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/candidate-classes.csv"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
HEAD = ROOT / "research/experiments/n11-fourteenth-ladder-top-k01-adoption-20261128/output/merged/merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
INDEP = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
INDEP_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
FIFTHSEL = ROOT / "research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/scripts/select_fifth_exclusive.py"
FIFTHSEL_SHA = "af68af3c9c9567487727161905e2622b35fd3e3724c5986d5186098a53324cc3"
SELJSON = {
    "fifth_44": ("research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/output/fifth-cost-exclusive-keys.json",
                 "2d7d3a9db62f10acd144dd096ebd2e624698c2057f0f963d177e516296965380"),
    "sixth_43": ("research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/sixth-cost-exclusive-keys.json",
                 "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"),
    "seventh_42": ("research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/seventh-cost-exclusive-keys.json",
                   "c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627"),
    "eighth_43": ("research/experiments/n11-eighthcost-class-s5-exclusive-probe-1297036692750860288-20261127/output/eighth-cost-exclusive-keys.json",
                  "691dcd807d52b9b9dbe0118f2347db9a613565377350246fda53a6c518aeef33"),
    "ninth_45": ("research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127/output/ninth-cost-exclusive-keys.json",
                 "772c9235fe226e9b52a36a6860ef2096a099a3be374daf0b80de21ee81bd4568"),
    "tenth_44": ("research/experiments/n11-tenthcost-class-s5-exclusive-probe-20261127/output/tenth-cost-exclusive-keys.json",
                 "3d0f791effe78d73697f8f627ab0111e1c58e7fefbc154d99935e5a6d9a3ba6e"),
    "eleventh_46": ("research/experiments/n11-eleventhcost-class-s5-exclusive-probe-20261127/output/eleventh-cost-exclusive-keys.json",
                    "5a29b5be27430eb0f19221234b7d001a92a7f02be577a30d169c5e011da14bd5"),
    "twelfth_51": ("research/experiments/n11-twelfthcost-class-s5-exclusive-probe-20261127/output/twelfth-cost-exclusive-keys.json",
                   "1119d01bb2a4c0a02222414ae0506aa61a307334b263e619fdfed9b3eddc0878"),
}
KEYMAP = ROOT / "research/experiments/n11-s4bd-fresh-corpus-regen-20261121/input/keymap.json"
KEYMAP_SHA = "0aa054c829b912afa10c56ccf62fa6ae5f3bec6bcf932a46b157565baa9d552a"
PARKED2 = [
    (ROOT / "research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-1297036830122704896-67108864.input.csv",
     "8e530240731fea53d3655ca218ed3aa055d02928273035b56a825e1fb3161ca1"),
    (ROOT / "research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-10376294091217440768-33554432.input.csv",
     "d22df157dbb9ccde348e280b26fabb5aa68deeea0ceaa7ae845758cde4b7c63b"),
]
PARKED4_DIR = ROOT / "research/experiments/n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126/input"
PARKED4_SHA = ["298dd6e6b6655d12aefaae138a2e1d85388220546ff68e4d6b7081c6097b0526",  # batch-k13
               "88c107d7d060ef756a394d722de3a80b4ee60bad5647785cbbb65eb088da6190",  # batch-k19
               "0984400f8aa99735e11e2638f5bc9a9273ddd296e845f7b7118f3ada81adddad",  # batch-k20
               "ca081b0f2f85e62b39cbbd1178a7be839c87e3446b2357657bbfe8681f82e2f4"]  # batch-k33


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _extract_declared_list(source_text, name):
    tree = _ast.parse(source_text)
    for node in tree.body:
        if isinstance(node, _ast.Assign):
            for t in node.targets:
                if isinstance(t, _ast.Name) and t.id == name:
                    v = node.value
                    if isinstance(v, _ast.Call):
                        v = v.args[0]
                    return _ast.literal_eval(v)
    raise SystemExit(f"list {name} not found in pinned fifth-cost selector")


def fresh_legal_count(lo: int, hi: int, n: int = 11) -> int:
    """Independent legality: a move is legal iff it is empty and lies on no
    circle-or-line completion of any triple of the existing stones.
    Circle/line membership by an integer 4x4 determinant (Bareiss-free
    direct expansion), no floating point, no repo code."""

    def det4(m):
        return (m[0][3] * (m[1][2] * (m[2][1] * m[3][0] - m[2][0] * m[3][1])
                           - m[1][1] * (m[2][2] * m[3][0] - m[2][0] * m[3][2])
                           + m[1][0] * (m[2][2] * m[3][1] - m[2][1] * m[3][2]))
                - m[0][2] * (m[1][3] * (m[2][1] * m[3][0] - m[2][0] * m[3][1])
                             - m[1][1] * (m[2][3] * m[3][0] - m[2][0] * m[3][3])
                             + m[1][0] * (m[2][3] * m[3][1] - m[2][1] * m[3][3]))
                + m[0][1] * (m[1][3] * (m[2][2] * m[3][0] - m[2][0] * m[3][2])
                             - m[1][2] * (m[2][3] * m[3][0] - m[2][0] * m[3][3])
                             + m[1][0] * (m[2][3] * m[3][2] - m[2][2] * m[3][3]))
                - m[0][0] * (m[1][3] * (m[2][2] * m[3][1] - m[2][1] * m[3][2])
                             - m[1][2] * (m[2][3] * m[3][1] - m[2][1] * m[3][3])
                             + m[1][1] * (m[2][3] * m[3][2] - m[2][2] * m[3][3])))

    pts = []
    for i in range(n * n):
        word = lo if i < 64 else hi
        if (word >> (i % 64)) & 1:
            pts.append((i % n, i // n))
    if len(pts) != 5:
        raise ValueError("not a 5-stone key")

    def row(p):
        return [p[0] * p[0] + p[1] * p[1], p[0], p[1], 1]

    blocked = set()
    for triple in combinations(pts, 3):
        base = [row(p) for p in triple]
        for i in range(n * n):
            q = (i % n, i // n)
            if q in pts:
                continue
            if det4([row(q)] + base) == 0:
                blocked.add(i)
    return n * n - len(pts) - len(blocked)


def main() -> int:
    closure = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("closure-classes.csv")
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    gates = {}

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
        return bool(ok)

    ok = True

    # ---------- pins ----------
    ok &= g("P0:dependency-graph-sha", sha256(GRAPH) == GRAPH_SHA, "")
    ok &= g("P0:update8-sha", sha256(UPDATE8) == UPDATE8_SHA, "")
    ok &= g("P0:supply-sha", sha256(SUPPLY) == SUPPLY_SHA, "")
    ok &= g("P0:candidates-sha", sha256(CAND) == CAND_SHA, "")
    ok &= g("P0:quarantine-sha", sha256(QUARANTINE) == QUAR_SHA, "")
    ok &= g("P0:closure-sha", sha256(closure) == CLOSURE_SHA, "")
    ok &= g("P0:head-sha", sha256(HEAD) == HEAD_SHA, "")
    ok &= g("P0:geometry-sha", sha256(GEOMETRY) == GEOM_SHA, "")
    ok &= g("P0:independent-sha", sha256(INDEP) == INDEP_SHA, "")
    ok &= g("P0:policy-sha", sha256(POLICY) == POLICY_SHA, "")
    ok &= g("P0:fifthsel-sha", sha256(FIFTHSEL) == FIFTHSEL_SHA, "")
    for name, (rel, sha) in SELJSON.items():
        ok &= g(f"P0:{name}-sha", sha256(ROOT / rel) == sha, rel)
    ok &= g("P0:keymap-sha", sha256(KEYMAP) == KEYMAP_SHA, "")
    for p, s in PARKED2:
        ok &= g(f"P0:parked2-{p.name}-sha", sha256(p) == s, "")
    parked4_files = sorted(PARKED4_DIR.glob("batch-k*.input.csv"))
    ok &= g("P0:parked4-files", len(parked4_files) == 4
            and [sha256(p) for p in parked4_files] == PARKED4_SHA,
            str([p.name for p in parked4_files]))

    # ---------- head ----------
    cache = {}
    for line in HEAD.read_text().splitlines():
        if not line.startswith("s5verdict,"):
            continue
        p = line.strip().split(",")
        cache[(p[1], p[2])] = p[4]
    ok &= g("P1:head-shape", len(cache) == HEAD_ROWS
            and Counter(cache.values()) == {"2": HEAD_LOSS, "1": HEAD_WIN}, str(len(cache)))

    # ---------- frozen dependency graph ----------
    gph = json.load(gzip.open(GRAPH))
    s4_masks, s4_cost, s5_masks = gph["s4_masks"], gph["s4_cost"], gph["s5_masks"]
    ok &= g("P1:graph-shape", len(s4_masks) == 34949 and len(s4_cost) == 34949
            and len(s5_masks) == 962525, "")

    # ---------- update8 receipts ----------
    u8 = json.loads(UPDATE8.read_text())
    ok &= g("P1:update8-shape", u8.get("schema") == "n11-night-repaired-joint-plan-update8-v1"
            and u8.get("union_size") == 31859
            and len(u8.get("required_new_s5", [])) == 31859
            and u8.get("verification", {}).get("passed") is True, "")
    receipts = {int(k): int(v) for k, v in u8["resolved_s5_verdicts"].items()}
    ok &= g("P1:update8-receipts", len(receipts) == 23, str(len(receipts)))
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    def known(j: int):
        v = cache.get((str(s5_masks[j][0]), str(s5_masks[j][1])))
        if v is not None:
            return int(v)
        return receipts.get(j)

    conflicts = 0
    for (lo, hi), v in cache.items():
        i = mask_to_index.get((int(lo), int(hi)))
        if i is not None and i in receipts and receipts[i] != int(v):
            conflicts += 1
    ok &= g("P1:receipt-cache-conflicts", conflicts == 0, conflicts)

    # ---------- closure ladder full recomputation ----------
    rows = list(csv.DictReader(open(closure)))
    ok &= g("P1:closure-rows", len(rows) == LADDER_ROWS, len(rows))
    mismatch, per_class = [], {}
    for r in rows:
        i = int(r["class_index"])
        cost = s4_cost[i]
        unk = [j for j in cost if known(j) is None]
        per_class[i] = unk
        if len(unk) != int(r["unknown_now"]):
            mismatch.append(f"{i}:{len(unk)}!={r['unknown_now']}")
    ok &= g("P2:closure-unknown-recomputed-799", not mismatch, ";".join(mismatch[:5]))
    ranked = sorted(rows, key=lambda r: int(r["class_rank"]))
    top5 = [(int(r["class_index"]), int(r["unknown_now"])) for r in ranked[:5]]
    ok &= g("P2:top5-ladder-rows", top5 == EXPECTED_TOP5, str(top5))

    # ---------- supply ----------
    supply = {r["key"]: r for r in csv.DictReader(open(SUPPLY))}
    ok &= g("P1:supply-shape", len(supply) == 4562, len(supply))

    # ---------- claim sets ----------
    src = FIFTHSEL.read_text(encoding="utf-8")
    claims = {
        "focus_35": sorted(_extract_declared_list(src, "FOCUS_35")),
        "cert_38": sorted(_extract_declared_list(src, "CERT_38")),
        "third_39": sorted(_extract_declared_list(src, "THIRD_39")),
        "fourth_41": sorted(_extract_declared_list(src, "FOURTH_41")),
    }
    for name, (rel, _sha) in SELJSON.items():
        d = json.load(open(ROOT / rel))
        claims[name] = [e["key"] for e in d["exclusive_probe_order"]]
    km = json.load(open(KEYMAP))
    claims["sbd_101"] = [f"{v[0]}:{v[1]}" for v in km["targets"].values()]
    parked = []
    for p, _s in PARKED2:
        f = p.read_text().strip().split(",")
        parked.append(f"{f[3]}:{f[4]}")
    for p in parked4_files:
        f = p.read_text().strip().split(",")
        parked.append(f"{f[3]}:{f[4]}")
    claims["parked_6"] = parked
    claims["ultra_cheap_4"] = ULTRA_CHEAP_4
    claims["thirteenth_2"] = THIRTEENTH_2
    claims["fourteenth_1"] = FOURTEENTH_1
    sizes = {k: len(v) for k, v in claims.items()}
    ok &= g("P3:claim-sizes", sizes == {"focus_35": 35, "cert_38": 38, "third_39": 39,
            "fourth_41": 41, "fifth_44": 44, "sixth_43": 43, "seventh_42": 42,
            "eighth_43": 43, "ninth_45": 45, "tenth_44": 44, "eleventh_46": 46,
            "twelfth_51": 51, "sbd_101": 101, "parked_6": 6, "ultra_cheap_4": 4,
            "thirteenth_2": 2, "fourteenth_1": 1},
            json.dumps(sizes))
    ok &= g("P3:ultra-cheap-adopted", all((k.split(":")[0], k.split(":")[1]) in cache
            for k in ULTRA_CHEAP_4), "")
    ok &= g("P3:thirteenth-adopted", all((k.split(":")[0], k.split(":")[1]) in cache
            for k in THIRTEENTH_2), "")
    ok &= g("P3:fourteenth-adopted", all((k.split(":")[0], k.split(":")[1]) in cache
            for k in FOURTEENTH_1), "")
    quar = json.load(open(QUARANTINE))
    qkeys = [e.get("key") if isinstance(e, dict) else str(e)
             for e in (quar if isinstance(quar, list) else quar.get("entries", []))]
    ok &= g("P3:quarantine-entries", len(qkeys) == 2, str(len(qkeys)))

    # ---------- Board + policy ----------
    sys.path.insert(0, str(INDEP.parent))
    from independent import Board, mask_from_key  # noqa: E402
    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import is_canonical_safe_s5_key  # noqa: E402
    board = Board(11)

    def key_available(j):
        ukey = f"{s5_masks[j][0]}:{s5_masks[j][1]}"
        claimed_in = [name for name, lst in claims.items() if ukey in lst]
        s = supply.get(ukey)
        info = {
            "key": ukey, "s5_index": j,
            "in_probe13_supply": s is not None,
            "proxy": int(s["truncated_cost_proxy_nodes"]) if s else None,
            "fresh_vs_head": (str(s5_masks[j][0]), str(s5_masks[j][1])) not in cache,
            "claimed_in": claimed_in,
            "quarantined": ukey in qkeys,
        }
        mask = mask_from_key(s5_masks[j][0], s5_masks[j][1])
        pts = board.points(mask)
        info["stones"] = len(pts)
        info["d4_canonical"] = board.canonical(mask) == mask
        info["canonical_safe"] = is_canonical_safe_s5_key((s5_masks[j][0], s5_masks[j][1]))
        board_legal = len(board.points(board.legal(mask)))
        fresh_legal = fresh_legal_count(s5_masks[j][0], s5_masks[j][1])
        info["legal_board"] = board_legal
        info["legal_fresh_det"] = fresh_legal
        info["legal"] = board_legal if board_legal == fresh_legal else None
        info["available"] = (not claimed_in and info["fresh_vs_head"]
                             and not info["quarantined"] and info["stones"] == 5
                             and info["d4_canonical"] and info["canonical_safe"]
                             and board_legal == fresh_legal)
        return info

    # ---------- selection: first ladder class with ALL-unknown available ----------
    selection = None
    scanned = []
    for r in ranked:
        i = int(r["class_index"])
        infos = [key_available(j) for j in sorted(per_class[i])]
        entry = {"class_rank": int(r["class_rank"]), "class_index": i,
                 "class_key": f"{s4_masks[i][0]}:{s4_masks[i][1]}",
                 "unknown_now": len(infos), "keys": infos,
                 "all_available": all(k["available"] for k in infos)}
        scanned.append(entry)
        if entry["all_available"] and selection is None:
            selection = entry
        if len(scanned) >= 12 and selection is not None:
            break
    ok &= g("P4:selection-found", selection is not None, "")
    ok &= g("P4:selection-class", selection is not None
            and selection["class_index"] == EXPECTED_SELECTION_CLASS,
            str(selection["class_index"]) if selection else "none")
    sel_keys = [(k["key"].split(":")[0], int(k["key"].split(":")[1])) for k in selection["keys"]]
    ok &= g("P4:selection-keys", sel_keys == EXPECTED_SELECTION_KEYS, str(sel_keys))
    ok &= g("P4:selection-s5-index", [k["s5_index"] for k in selection["keys"]]
            == EXPECTED_SELECTION_S5_INDEX, "")
    ok &= g("P4:selection-unclaimed-quarantine-free",
            all(not k["claimed_in"] and not k["quarantined"] and k["fresh_vs_head"]
                for k in selection["keys"]), "")
    ok &= g("P4:selection-legal-dual", all(k["legal"] is not None for k in selection["keys"]), "")
    ok &= g("P4:selection-not-in-supply", all(not k["in_probe13_supply"] for k in selection["keys"]), "")

    out = {
        "schema": "n11-fifteenth-ladder-top-selection-v1",
        "head_basis": {"sha256": HEAD_SHA, "rows": HEAD_ROWS, "win": HEAD_WIN, "loss": HEAD_LOSS},
        "closure_ladder": {"sha256": CLOSURE_SHA, "rows": LADDER_ROWS,
                           "unknown_recomputed": "all 799 rows match the published unknown_now"},
        "published_top5": [{"class_index": c, "unknown_now": u} for c, u in EXPECTED_TOP5],
        "selection": {"class_index": selection["class_index"],
                      "class_key": selection["class_key"],
                      "probe_order": [{"key": k["key"], "s5_index": k["s5_index"],
                                       "legal": k["legal"], "proxy": k["proxy"],
                                       "in_probe13_supply": k["in_probe13_supply"],
                                       "stones": k["stones"], "d4_canonical": k["d4_canonical"],
                                       "canonical_safe": k["canonical_safe"],
                                       "legal_board": k["legal_board"],
                                       "legal_fresh_det": k["legal_fresh_det"]}
                                      for k in selection["keys"]]},
        "scanned_candidates": [{"class_rank": e["class_rank"], "class_index": e["class_index"],
                                "class_key": e["class_key"], "unknown_now": e["unknown_now"],
                                "all_available": e["all_available"],
                                "blocked_keys": [{"key": k["key"], "reasons":
                                                  [r for r, v in [("claimed", bool(k["claimed_in"])),
                                                                  ("in_head", not k["fresh_vs_head"]),
                                                                  ("quarantined", k["quarantined"]),
                                                                  ("not_canonical_safe", not k["canonical_safe"])]
                                                  if v]}
                                                 for k in e["keys"] if not k["available"]]}
                               for e in scanned],
        "claim_sets_checked": sorted(claims) + ["quarantine_2"],
        "gates": gates,
        "overall": "PASS" if ok else "FAIL",
        "meaning": ("selection and scheduling bookkeeping only; no verdict is claimed or "
                    "consumed; resolving a selected key would still require the standing "
                    "cold-pair + C++-gate + third-implementation pillars before any "
                    "adoption; the standard 11x11 empty board, all 19 central-reply "
                    "roots, the two-stone root {60,27} and third moves 100/108 remain "
                    "UNKNOWN"),
    }
    js = json.dumps(out, indent=1, sort_keys=True) + "\n"
    if out_path is not None:
        out_path.write_text(js)
    sys.stdout.write(js)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
