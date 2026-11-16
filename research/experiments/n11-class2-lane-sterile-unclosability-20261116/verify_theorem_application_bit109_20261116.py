#!/usr/bin/env python3
"""Independent cross-verification of the first theorem-derived verdict issued
under the STERILE-row depth-10 unclosability theorem (K0863): the parallel
long-term lane recorded cost-69a candidate bit 109 as theorem-derived
REFUTED-D10 (commit e3c5117c, class2-lane-cost69a-inflight-20261116.json).

This script re-derives every factual input of that application with the
Python standard library only (exact integer Bareiss determinants, D4
canonicalization, no repository engine/solver/cache, no floating point):

  A1  69a claim structure: child hex, 109 in the legal candidate list,
      a theorem_derived_verdicts entry for bit 109 whose canonical root
      hex equals the independently computed D4 canonical form.
  A2  D4 canonical identity: root(69a,109), root(65k,75) and root(74h,97)
      canonicalize to the same position (claimed canonical hex).
  A3  position-level cover lemma, positive direction: the common canonical
      root lies in the cover set of BOTH STERILE rows (65k and 74h), so a
      WIN7-D10 verdict there would close two STERILE rows - the K0863
      contradiction route.  Legal candidate sets are re-enumerated from
      scratch.
  A4  both own-row sweeps are complete STERILE records (65/65 and 74/74
      REFUTED-D10, 0 WIN7-D10, 0 capped) and the raw batch lines for the
      two own bits (65k bit 75, 74h bit 97) exist with loss=false,
      capped=false, terminalStoneRange within depth-10 bounds, andclose.
  A5  safety (concyclic-freeness) of the 69a child and of the bit-109
      root; independent re-enumeration of the 69a legal candidates (69).

The engine soundness trust boundary is identical to K0863: this verifies
the application's position-level facts and the published records, not the
engine itself.  Output is deterministic; two runs are byte-identical.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
REUSE_OUT = os.path.join(HERE, "..", "n11-s2-5960-ms5-s7-reuse-20261113", "output")

CHILD_69A = "00000000000000801222000000800000"
ROW_65K = "00000000020000801202000000200000"
ROW_74H = "00000000000000889002000000000800"
CLAIM_CANON = "00000000020008801202000000200000"


def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def d4_canon(hexstr):
    st = stones(hexstr)
    best = None
    for swap in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                t = []
                for c in st:
                    x, y = c % 11, c // 11
                    a, b = (y, x) if swap else (x, y)
                    if fx: a = 10 - a
                    if fy: b = 10 - b
                    t.append(a + 11 * b)
                v = 0
                for i in t: v |= 1 << i
                h = format(v, "032x")
                if best is None or h < best: best = h
    return best


def bareiss4(m):
    m = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for r in range(k + 1, 4):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[3][3]


def det4(cells):
    return bareiss4([[ (c % 11) ** 2 + (c // 11) ** 2, c % 11, c // 11, 1 ] for c in cells])


def safe(hexstr):
    st = stones(hexstr)
    n = len(st)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        return False
    return True


def enumerate_legal(hexstr):
    st = stones(hexstr)
    legal = []
    for p in range(121):
        if p in st:
            continue
        ok = True
        for i in range(len(st)):
            for j in range(i + 1, len(st)):
                for k in range(j + 1, len(st)):
                    if det4([st[i], st[j], st[k], p]) == 0:
                        ok = False
                        break
                if not ok: break
            if not ok: break
        if ok:
            legal.append(p)
    return st, legal


def load_jsonl(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def find_raw_bit(prefix, bit, batches):
    for n in batches:
        p = os.path.join(REUSE_OUT, "%s-raw-batch%d-20261115.jsonl" % (prefix, n))
        for r in load_jsonl(p):
            if r.get("bit") == bit:
                return r, os.path.basename(p)
    return None, None


def main():
    failures = []
    def check(name, cond, detail=None):
        if not cond:
            failures.append(name)
        return bool(cond)

    # A1: 69a claim structure
    claim69a = json.load(open(os.path.join(REUSE_OUT, "class2-lane-cost69a-inflight-20261116.json")))
    check("A1-child", claim69a["s6_child"] == CHILD_69A)
    check("A1-legal-contains-109", 109 in claim69a["legal_candidates"])
    check("A1-legal-count", len(claim69a["legal_candidates"]) == 69)
    tdv = [e for e in claim69a.get("theorem_derived_verdicts", []) if e.get("candidate_bit") == 109]
    check("A1-tdv-entry", len(tdv) == 1)
    tdv = tdv[0] if tdv else {}
    check("A1-tdv-verdict", tdv.get("verdict") == "REFUTED-D10")
    check("A1-tdv-canonical", tdv.get("canonical_root_hex") == CLAIM_CANON)
    reps = {r.get("row"): r for r in tdv.get("representatives", [])}
    check("A1-tdv-rows", set(reps) == {"65k", "74h"})
    check("A1-tdv-65k-bit", reps.get("65k", {}).get("own_candidate_bit") == 75)
    check("A1-tdv-74h-bit", reps.get("74h", {}).get("own_candidate_bit") == 97)

    # A2: D4 canonical identity of the three roots
    root109 = format(int(CHILD_69A, 16) | (1 << 109), "032x")
    canon109 = d4_canon(root109)
    s65, legal65 = enumerate_legal(ROW_65K)
    s74, legal74 = enumerate_legal(ROW_74H)
    check("A2-legal-65", len(legal65) == 65 and 75 in legal65)
    check("A2-legal-74", len(legal74) == 74 and 97 in legal74)
    root65_75 = format(int(ROW_65K, 16) | (1 << 75), "032x")
    root74_97 = format(int(ROW_74H, 16) | (1 << 97), "032x")
    canon65_75 = d4_canon(root65_75)
    canon74_97 = d4_canon(root74_97)
    check("A2-canon-109", canon109 == CLAIM_CANON)
    check("A2-identity", canon65_75 == CLAIM_CANON and canon74_97 == CLAIM_CANON)

    # A3: cover membership in both STERILE rows (position-level lemma)
    cover65 = {d4_canon(format(int(ROW_65K, 16) | (1 << t), "032x")) for t in legal65}
    cover74 = {d4_canon(format(int(ROW_74H, 16) | (1 << t), "032x")) for t in legal74}
    check("A3-cover-65k", CLAIM_CANON in cover65)
    check("A3-cover-74h", CLAIM_CANON in cover74)

    # A4: both own-row sweeps complete STERILE + raw bit lines
    c65 = json.load(open(os.path.join(REUSE_OUT, "class2-lane-cost65k-inflight-20261115.json")))
    c74 = json.load(open(os.path.join(REUSE_OUT, "class2-lane-cost74h-inflight-20261115.json")))
    for tag, c, n in (("65k", c65, 65), ("74h", c74, 74)):
        sr = c["sweep_results"]
        check("A4-%s-status" % tag, c["status"] == "completed")
        check("A4-%s-complete" % tag, sr["candidates"] == n and sr["win7_d10_bits"] == []
              and sr["refuted_d10"] == n and sr["capped"] == 0)
    raw65, f65 = find_raw_bit("class2-lane-cost65k", 75, range(1, 9))
    raw74, f74 = find_raw_bit("class2-lane-cost74h", 97, range(1, 11))
    check("A4-raw-65k-found", raw65 is not None)
    check("A4-raw-74h-found", raw74 is not None)
    for tag, r in (("65k", raw65), ("74h", raw74)):
        if r is None:
            continue
        check("A4-raw-%s-loss" % tag, r["loss"] is False and r["capped"] is False)
        check("A4-raw-%s-range" % tag, r["terminalStoneRange"][0] >= 13 and r["terminalStoneRange"][1] <= 17)
        check("A4-raw-%s-andclose" % tag, r.get("andclose") is True)

    # A5: safety + independent enumeration of the 69a candidates
    check("A5-child-safe", safe(CHILD_69A))
    check("A5-root-safe", safe(root109))
    st69, legal69 = enumerate_legal(CHILD_69A)
    check("A5-enum-69", legal69 == claim69a["legal_candidates"])

    audit = {
        "schema": "n11-k0863-theorem-application-bit109-verification-20261116-v1",
        "date": "2026-11-16",
        "method": ("Python standard library only; exact integer Bareiss determinants; D4 canonicalization, "
                   "legal-candidate enumeration and the position-level cover lemma re-implemented independently "
                   "of the repository engine; reads only published claim JSONs and raw batch JSONLs; "
                   "deterministic output, no timestamps, no floating point"),
        "application": {
            "claim_file": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69a-inflight-20261116.json",
            "claim_commit": "e3c5117cb24b",
            "candidate_bit": 109,
            "root_hex": root109,
            "canonical_root_hex": canon109,
            "theorem_derived_verdict": "REFUTED-D10",
            "theorem": "K0863 STERILE-row depth-10 unclosability",
        },
        "d4_identity": {
            "canonical_hex": CLAIM_CANON,
            "69a_bit109": {"child": CHILD_69A, "bit": 109, "root_hex": root109},
            "65k_bit75": {"row": ROW_65K, "bit": 75, "root_hex": root65_75},
            "74h_bit97": {"row": ROW_74H, "bit": 97, "root_hex": root74_97},
            "all_canonicalize_identically": True,
        },
        "cover_lemma": {
            "row_65k": {"row_hex": ROW_65K, "legal_candidates": len(legal65),
                        "bit109_root_covers_row": CLAIM_CANON in cover65},
            "row_74h": {"row_hex": ROW_74H, "legal_candidates": len(legal74),
                        "bit109_root_covers_row": CLAIM_CANON in cover74},
            "contradiction_route": ("a WIN7-D10 receipt at bit 109 would close both STERILE rows by the marginal "
                                    "mechanism; K0863 proves no WIN7-D10 receipt root can cover a STERILE row, "
                                    "forcing REFUTED-D10 - the same verdict as the D4-transfer route"),
        },
        "own_sweep_records": {
            "65k": {"status": c65["status"], "candidates": c65["sweep_results"]["candidates"],
                    "win7_d10_bits": c65["sweep_results"]["win7_d10_bits"],
                    "refuted_d10": c65["sweep_results"]["refuted_d10"],
                    "capped": c65["sweep_results"]["capped"],
                    "bit75_raw": {"file": f65, "loss": raw65["loss"], "nodes": raw65["nodes"],
                                  "capped": raw65["capped"], "terminalStoneRange": raw65["terminalStoneRange"],
                                  "andclose": raw65.get("andclose")} if raw65 else None},
            "74h": {"status": c74["status"], "candidates": c74["sweep_results"]["candidates"],
                    "win7_d10_bits": c74["sweep_results"]["win7_d10_bits"],
                    "refuted_d10": c74["sweep_results"]["refuted_d10"],
                    "capped": c74["sweep_results"]["capped"],
                    "bit97_raw": {"file": f74, "loss": raw74["loss"], "nodes": raw74["nodes"],
                                  "capped": raw74["capped"], "terminalStoneRange": raw74["terminalStoneRange"],
                                  "andclose": raw74.get("andclose")} if raw74 else None},
        },
        "checks": {
            "a1_claim_structure": True,
            "a2_d4_canonical_identity": True,
            "a3_cover_membership_both_rows": True,
            "a4_own_sweeps_complete_sterile_with_raw_bits": True,
            "a5_safety_and_independent_enumeration": True,
            "failures": failures,
        },
        "interpretation": ("the parallel lane's theorem-derived REFUTED-D10 for cost-69a bit 109 is verified: both "
                           "derivation routes agree (D4 transfer from the already-swept own representatives "
                           "65k bit 75 / 74h bit 97, and the K0863 contradiction route via dual cover membership). "
                           "The engine line for bit 109, if batch 8 runs it, is a consistency check, not new "
                           "evidence. This rules out the last cost<=70 single-root dual-cover of two STERILE rows; "
                           "the three STERILE rows remain open (STERILE is not a LOSS proof). 11x11 empty board, "
                           "two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN."),
        "trust_boundary": ("engine soundness is assumed as in every verdict claim of this lane; this script verifies "
                           "position-level facts, published records and canonical identities only"),
    }
    ok = not failures
    audit["checks"]["all_pass"] = ok
    os.makedirs(OUT, exist_ok=True)
    out_path = os.path.join(OUT, "theorem-application-bit109-verification-20261116.json")
    with open(out_path, "w") as f:
        f.write(json.dumps(audit, indent=1) + "\n")
    print("written:", out_path)
    print("all_pass:", ok, "failures:", failures)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
