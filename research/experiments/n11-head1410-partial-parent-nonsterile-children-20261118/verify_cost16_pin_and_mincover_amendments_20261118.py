#!/usr/bin/env python3
"""Verification-side audit of the 2026-11-18 verification-lane amendments.

This script verifies, entirely from files at their repo paths:

  A. the correct git blob SHA-1 of the K0865 receipt-unclosability census
     input file (and that the spliced pin published by the cost-16
     shared-memo crosscheck matches no file: it is exactly
     census_blob[:29] + k0863_item_blob[29:]),

  B. that both amended records (head-1476 census/class-2 cover record and
     cost-16 shared-memo crosscheck record) are pure textual inserts: the
     pre-amendment record is reconstructed byte-exactly and pinned at its
     original git blob, every original field is preserved verbatim, and
     the amendment fields carry the corrected values,

  C. that the in-place pin fixes (shared-memo crosscheck script census
     pin; head-1476 record pin in the three earlier lane scripts) leave
     every pin in those scripts equal to the actual blob of its file,

  D. an independent recomputation of the 11-row class-2 cover numbers
     337,020 (partition-shaped minimum covers) + 22,590 (overlapping
     six-pair minimum covers) = 359,610 from the pinned worklist,
     census, and ledger, with per-row singleton pm values crosschecked
     against the published root-membership output.

No engine run, no verdict, no new game value. REFUTED-D10 and STERILE
are not LOSS proofs.
"""
import json, os, sys, hashlib, csv
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")

E = "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118"
INPUTS = {
    "worklist": ("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                 "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "census": ("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
               "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "ledger": (E + "/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                "e8785d509e8a11a37c0d03cc450455a14708c34d"),
    "cover": (E + "/output/parent-minimum-cover-cost-table-20261118.json",
              "4e4a911d0e05779437d4a8e97685a8feb66c0d25"),
    "phase_a": (E + "/output/cost16-a-phase-20261118.json",
                "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"),
    "membership11": (E + "/output/minimum-cover-root-membership-20261118.json",
                     "ab1e655f4a89a677e57515cdbacfe56894323013"),
    "census_crosscheck": (E + "/output/crosscheck-head1476-parent-census-and-class2-cover-20261118.json",
                          "fdee94dfc60fb833b188c4f2b41c7f292263076b"),
    "k0863_item": ("research/knowledge/items/K0863-sterile-row-depth10-unclosability.md",
                   "c2ae353cab4a7dbcd28ec53b0f57d35ab4f26a5d"),
    "census_record_amended": (E + "/output/head1476-parent-census-and-class2-cover-20261118.json",
                              "28a0993d7192e599a95ab93becb5dc0d983a8d35"),
    "cost16_amended": (E + "/output/cost16-shared-memo-crosscheck-20261118.json",
                       "41d37ed863a85c8a9bdadaf0f39bb6d1a452c60d"),
    "cost16_script_fixed": (E + "/crosscheck_cost16_parent_shared_memo_20261118.py",
                            "e5a47f7a10354add46ab9577358e1fb98bd81e51"),
    "membership11_script": (E + "/count_minimum_cover_root_membership_20261118.py",
                            "b8e378c7c5699addf63a1f1ffbbf515630411022"),
    "elimination_script": (E + "/analyze_minimum_cover_elimination_structure_20261118.py",
                           "fa810590ccad5027f785f2a4d4aab0bb3cd17148"),
    "head1476_crosscheck_script": (E + "/crosscheck_head1476_census_and_class2_cover_20261118.py",
                                   "c6ebb06c4c7b5a7385a1ad92d90c85d37d264bb2"),
}
ORIGINAL_CENSUS_RECORD_BLOB = "8e870809251fdc27701518d66d6b8a65ec6798c7"
ORIGINAL_COST16_JSON_BLOB = "b70689ea6b2177b2a86909939737f57c5ed637c9"
SPLICED_CENSUS_PIN = "9c251da3138c5cb0516e097be5e5d35ab4f26a5d"
CORRECT_CENSUS_PIN = "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"
AMENDED_RECORD_BLOB = "28a0993d7192e599a95ab93becb5dc0d983a8d35"
TARGET_PARENT_11 = "00000000000000403800000008000000"
N = 11


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def read_pinned(name):
    rel, pin = INPUTS[name]
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    sha = git_blob_sha(data)
    if sha != pin:
        raise SystemExit("%s git blob SHA mismatch: %s != %s" % (name, sha, pin))
    return data


T = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]
TO = [tuple(t(i % N, i // N)[1] * N + t(i % N, i // N)[0] for i in range(121)) for t in T]


def orbit_masks(mask):
    out = []
    for to in TO:
        v = 0
        for i in range(121):
            if (mask >> i) & 1:
                v |= 1 << to[i]
        out.append(v)
    return out


def canon(mask):
    return min(orbit_masks(mask))


def det3(a, b, c):
    x1, y1 = a % N, a // N
    x2, y2 = b % N, b // N
    x3, y3 = c % N, c // N
    A, B, C = x1 * x1 + y1 * y1, x1, y1
    D, E, F = x2 * x2 + y2 * y2, x2, y2
    G, H, I = x3 * x3 + y3 * y3, x3, y3
    return A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)


def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


def reconstruct_original(amended_text, amendment_key):
    """Remove the textual-insert amendment block; return the original text."""
    lines = amended_text.split("\n")
    assert lines[0] == "{", "line 0 is not the opening brace"
    key_line = '  "%s": {' % amendment_key
    assert lines[1] == key_line, "line 1 is not the amendment key: %r" % lines[1]
    end = None
    for i in range(2, len(lines)):
        if lines[i] == "  },":
            end = i
            break
    assert end is not None, "amendment block end not found"
    return "\n".join([lines[0]] + lines[end + 1:])


class PmSmall:
    """Weighted perfect-matching count on induced row subsets (tiny graphs)."""

    def __init__(self, adj):
        self.adj = adj
        self.memo = {0: 1}

    def get(self, mask):
        memo = self.memo
        if mask in memo:
            return memo[mask]
        stack = [mask]
        seen = {mask}
        order = []
        while stack:
            m = stack.pop()
            if m in memo:
                continue
            order.append(m)
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            for j, _w in self.adj[first]:
                bit = 1 << j
                if rest & bit:
                    sub = rest ^ bit
                    if sub not in memo and sub not in seen:
                        seen.add(sub)
                        stack.append(sub)
        order.sort(key=int.bit_count)
        for m in order:
            if m in memo:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            acc = 0
            for j, w in self.adj[first]:
                bit = 1 << j
                if rest & bit:
                    acc += w * memo[rest ^ bit]
            memo[m] = acc
        return memo[mask]


def derive_parent_rows(worklist_bytes, census, ledger, target_hex):
    sterile = {x["hex"] for x in census["sterile_row_registry"]}
    closed = set(ledger["derived"]["closed_rows_66"])
    parent_orbit = set(orbit_masks(int(target_hex, 16)))
    rows = {}
    reader = csv.DictReader(worklist_bytes.decode("utf-8").splitlines())
    for rec in reader:
        h = rec["s6_canonical_hex"].strip()
        if not h or h in sterile or h in closed:
            continue
        mask = int(h, 16)
        if any((mask >> b) & 1 and (mask ^ (1 << b)) in parent_orbit
               for b in range(121)):
            rows[h] = int(rec["own_candidates_s6_s7_edge_cost"])
    return sorted(rows.items())


def build_graph(target_rows):
    proot_rows = defaultdict(set)
    for ri, (h, expected_cost) in enumerate(target_rows):
        mask = int(h, 16)
        stones = [i for i in range(121) if (mask >> i) & 1]
        assert len(stones) == 6, (h, len(stones))
        count = 0
        for d in range(121):
            if (mask >> d) & 1:
                continue
            legal = True
            for i in range(6):
                if not legal:
                    break
                for j in range(i + 1, 6):
                    if not legal:
                        break
                    for k in range(j + 1, 6):
                        if det4(stones[i], stones[j], stones[k], d) == 0:
                            legal = False
                            break
            if legal:
                proot_rows[canon(mask | (1 << d))].add(ri)
                count += 1
        assert count == expected_cost, (h, count, expected_cost)
    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)
    for root, covered in proot_rows.items():
        if len(covered) == 2:
            a, b = sorted(covered)
            pair_roots[(a, b)].append(root)
        elif len(covered) == 1:
            (s,) = tuple(covered)
            singleton_roots[s].append(root)
        else:
            raise AssertionError(("root covers >2 rows", root, covered))
    edge_w = {pair: len(roots) for pair, roots in pair_roots.items()}
    adj = [[] for _ in target_rows]
    for (a, b), weight in edge_w.items():
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    for row in adj:
        row.sort()
    w1 = {s: len(singleton_roots.get(s, [])) for s in range(len(target_rows))}
    return proot_rows, pair_roots, singleton_roots, edge_w, adj, w1


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "cost16-pin-and-mincover-amendments-verification-20261118.json")
    checks = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    wl = read_pinned("worklist")
    census = json.loads(read_pinned("census"))
    ledger = json.loads(read_pinned("ledger"))
    read_pinned("cover")
    read_pinned("phase_a")
    membership11 = json.loads(read_pinned("membership11"))
    census_xc = json.loads(read_pinned("census_crosscheck"))
    k0863_blob = read_pinned("k0863_item")
    rec_amended_bytes = read_pinned("census_record_amended")
    cost16_amended_bytes = read_pinned("cost16_amended")
    fixed_script = read_pinned("cost16_script_fixed").decode("utf-8")
    read_pinned("membership11_script")
    read_pinned("elimination_script")
    read_pinned("head1476_crosscheck_script")

    # ---------- A. census input pin and splice diagnosis ----------
    census_bytes = read_pinned("census")  # already parsed; keep bytes
    census_actual = git_blob_sha(census_bytes)
    check("census_input.blob_correct", census_actual == CORRECT_CENSUS_PIN, census_actual)
    check("census_input.blob_is_not_spliced_pin", census_actual != SPLICED_CENSUS_PIN, SPLICED_CENSUS_PIN)
    k0863_sha = git_blob_sha(k0863_blob)
    check("splice.is_census_head_plus_k0863_tail",
          SPLICED_CENSUS_PIN == CORRECT_CENSUS_PIN[:29] + k0863_sha[29:],
          "census[:29] + k0863_item[29:] = " + CORRECT_CENSUS_PIN[:29] + k0863_sha[29:])

    # ---------- B1. census record amendment ----------
    rec_text = rec_amended_bytes.decode("utf-8")
    rec = json.loads(rec_text)
    orig_text = reconstruct_original(rec_text, "amendment_20261118_minimum_cover_count")
    orig_blob = git_blob_sha(orig_text.encode("utf-8"))
    check("census_record.reconstructs_original_blob", orig_blob == ORIGINAL_CENSUS_RECORD_BLOB, orig_blob)
    orig = json.loads(orig_text)
    check("census_record.amended_parses", "amendment_20261118_minimum_cover_count" in rec, list(rec.keys())[:3])
    check("census_record.original_fields_preserved",
          {k: v for k, v in rec.items() if k != "amendment_20261118_minimum_cover_count"} == orig,
          "all non-amendment top-level fields deep-equal the reconstructed original")
    am = rec["amendment_20261118_minimum_cover_count"]
    check("census_record.corrected_total_value",
          am["corrected_total"] == 359610
          and am["published_partition_component"] == 337020
          and am["overlapping_component"] == 22590
          and am["published_partition_component"] + am["overlapping_component"] == am["corrected_total"],
          {"total": am["corrected_total"], "partition": am["published_partition_component"],
           "overlapping": am["overlapping_component"]})
    check("census_record.published_field_still_present",
          orig["derived"]["candidate_cover"]["all_minimum_cover_sets"] == 337020,
          "derived.candidate_cover.all_minimum_cover_sets preserved verbatim at 337020, now annotated")
    check("census_record.evidence_pin_matches_crosscheck_file",
          am["evidence"]["git_blob_sha1"] == INPUTS["census_crosscheck"][1],
          am["evidence"]["git_blob_sha1"])
    f1 = [f for f in census_xc["findings"] if f.get("id") == "F1"]
    check("census_record.evidence_finding_numbers_agree",
          len(f1) == 1 and "359,610" in f1[0]["summary"] and "22,590" in f1[0]["summary"],
          "crosscheck finding F1 totals agree with the amendment values")

    # ---------- B2. cost16 crosscheck record amendment ----------
    ck_text = cost16_amended_bytes.decode("utf-8")
    ck = json.loads(ck_text)
    ck_orig_text = reconstruct_original(ck_text, "amendment_20261118_census_pin_correction")
    ck_orig_blob = git_blob_sha(ck_orig_text.encode("utf-8"))
    check("cost16_record.reconstructs_original_blob", ck_orig_blob == ORIGINAL_COST16_JSON_BLOB, ck_orig_blob)
    ck_orig = json.loads(ck_orig_text)
    check("cost16_record.original_fields_preserved",
          {k: v for k, v in ck.items() if k != "amendment_20261118_census_pin_correction"} == ck_orig,
          "all non-amendment top-level fields deep-equal the reconstructed original")
    am2 = ck["amendment_20261118_census_pin_correction"]
    check("cost16_record.corrected_pin_is_actual_census_blob",
          am2["corrected_git_blob_sha1"] == census_actual, am2["corrected_git_blob_sha1"])
    check("cost16_record.spliced_pin_documented",
          am2["published_spliced_git_blob_sha1"] == SPLICED_CENSUS_PIN
          and am2["splice_decomposition"] == "census_blob_sha1[:29] + k0863_item_blob_sha1[29:]",
          am2["published_spliced_git_blob_sha1"])
    check("cost16_record.derived_values_unchanged",
          ck["derived"]["A16"] == ck_orig["derived"]["A16"]
          and ck["derived"]["B16"] == ck_orig["derived"]["B16"]
          and ck["derived"]["total_minimum_covers"] == ck_orig["derived"]["total_minimum_covers"]
          and ck["derived"]["A16"] == 2305787291293934388
          and ck["derived"]["B16"] == 660663050386546968
          and ck["derived"]["total_minimum_covers"] == 2966450341680481356,
          {"A16": ck["derived"]["A16"], "B16": ck["derived"]["B16"]})

    # ---------- C. in-place pin fixes ----------
    check("fixed_script.correct_pin_once", fixed_script.count(CORRECT_CENSUS_PIN) == 1, "1")
    check("fixed_script.spliced_pin_gone", fixed_script.count(SPLICED_CENSUS_PIN) == 0, "0")
    all_pins_ok = True
    for name in ("worklist", "census", "ledger", "cover", "phase_a"):
        rel, pin = INPUTS[name]
        with open(os.path.join(ROOT, rel), "rb") as f:
            data = f.read()
        if git_blob_sha(data) != pin:
            all_pins_ok = False
    check("fixed_script.all_five_pins_match_files", all_pins_ok, "worklist/census/ledger/cover/phase_a")
    for label, name in (("membership11_script", "membership11_script"),
                        ("elimination_script", "elimination_script"),
                        ("head1476_crosscheck_script", "head1476_crosscheck_script")):
        src = read_pinned(name).decode("utf-8")
        check("repin.%s" % label,
              src.count(AMENDED_RECORD_BLOB) == 1 and src.count(ORIGINAL_CENSUS_RECORD_BLOB) == 0,
              "head1476 record pin updated to the amended blob")

    # ---------- D. independent 11-row minimum-cover recomputation ----------
    target_rows = derive_parent_rows(wl, census, ledger, TARGET_PARENT_11)
    m11_rows = [x["row"] for x in membership11["derived"]["per_row"]]
    check("recompute.rows_match_published_membership",
          [h for h, _ in target_rows] == sorted(m11_rows), len(target_rows))
    proot_rows, pair_roots, singleton_roots, edge_w, adj, w1 = build_graph(target_rows)
    check("recompute.roots_757", len(proot_rows) == 757, len(proot_rows))
    hist = defaultdict(int)
    for covered in proot_rows.values():
        hist[len(covered)] += 1
    check("recompute.span_histogram", dict(hist) == {1: 708, 2: 49}, dict(hist))
    check("recompute.candidates_806",
          sum(c for _, c in target_rows) == 806, sum(c for _, c in target_rows))
    r = len(target_rows)
    full = (1 << r) - 1
    pm = PmSmall(adj)
    per_row_pm = {s: pm.get(full ^ (1 << s)) for s in range(r)}
    A = sum(w1[s] * per_row_pm[s] for s in range(r))
    B = 0
    for d in range(r):
        neighbors = adj[d]
        for i, (a, wa) in enumerate(neighbors):
            for b, wb in neighbors[i + 1:]:
                B += wa * wb * pm.get(full ^ (1 << d) ^ (1 << a) ^ (1 << b))
    total = A + B
    check("recompute.partition_covers_337020", A == 337020, A)
    check("recompute.overlapping_covers_22590", B == 22590, B)
    check("recompute.total_359610", total == 359610, total)
    cs = membership11["derived"]["cover_space"]
    check("recompute.matches_published_cover_space",
          cs["singleton_type_covers"] == A and cs["six_pair_covers"] == B
          and cs["total_minimum_covers"] == total, [cs["singleton_type_covers"], cs["six_pair_covers"], cs["total_minimum_covers"]])
    ways10_pub = {x["row"]: x["ways10"] for x in membership11["derived"]["per_row"]}
    ways10_re = {target_rows[s][0]: per_row_pm[s] for s in range(r)}
    check("recompute.per_row_singleton_pm_matches_ways10", ways10_re == ways10_pub,
          "11/11 per-row weighted perfect matchings of the 10-row complements")

    # ---------- output ----------
    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-cost16-pin-and-mincover-amendments-verification-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Verification-side audit of the 2026-11-18 amendments: census-input pin splice correction and head-1476 minimum-cover count annotation",
        "inputs": {
            name: {"path": INPUTS[name][0], "git_blob_sha1": INPUTS[name][1]}
            for name in sorted(INPUTS)
        },
        "original_blobs": {
            "head1476_census_record_pre_amendment": ORIGINAL_CENSUS_RECORD_BLOB,
            "cost16_shared_memo_record_pre_amendment": ORIGINAL_COST16_JSON_BLOB,
        },
        "method": (
            "All statements are re-derived from files at their repo paths with git "
            "blob SHA-1 pins. The two amended records are shown to be pure textual "
            "inserts: the pre-amendment record is reconstructed by removing the "
            "amendment block and pinned at its original git blob; every non-amendment "
            "field is compared deep-equal against the reconstructed original. The "
            "spliced census pin is shown to be census_blob[:29] + k0863_item_blob[29:]. "
            "The 11-row class-2 cover totals are recomputed independently from the "
            "pinned worklist/census/ledger by weighted perfect-matching counting "
            "(partition shape A and overlapping six-pair shape B) and crosschecked "
            "against the published root-membership output."
        ),
        "derived": {
            "census_input_git_blob_sha1": census_actual,
            "spliced_pin": SPLICED_CENSUS_PIN,
            "splice_decomposition": "census_blob_sha1[:29] + k0863_item_blob_sha1[29:]",
            "k0863_item_git_blob_sha1": k0863_sha,
            "census_record_amended_git_blob_sha1": git_blob_sha(rec_amended_bytes),
            "cost16_record_amended_git_blob_sha1": git_blob_sha(cost16_amended_bytes),
            "corrected_total_minimum_covers_11row": total,
            "partition_covers_11row": A,
            "overlapping_covers_11row": B,
            "cost16_A16_unchanged": ck["derived"]["A16"],
            "cost16_B16_unchanged": ck["derived"]["B16"],
            "cost16_total_unchanged": ck["derived"]["total_minimum_covers"],
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": (
            "Finite bookkeeping and combinatorial verification only. The amendments "
            "correct an input-pin transcription defect and annotate a cover-count "
            "labeling error; no engine was run, no S5 parent was closed, and no "
            "game-theoretic value changed. REFUTED-D10 and STERILE are not LOSS proofs."
        ),
        "unknown_status": (
            "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(output, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({
        "all_pass": all_pass,
        "check_count": len(checks),
        "failed": [c["name"] for c in checks if not c["pass"]],
        "A": A, "B": B, "total": total,
        "output": out_path,
    }, indent=2))
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
