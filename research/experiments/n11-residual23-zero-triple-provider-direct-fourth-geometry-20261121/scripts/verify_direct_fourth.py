#!/usr/bin/env python3
"""Fourth independent geometry for the three residual-23 zero triple-provider rows."""
from __future__ import annotations
import argparse, hashlib, itertools, json
from collections import Counter
from pathlib import Path

INPUT_SHA256 = "51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822"
K1148_AUDIT_SHA256 = "526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573"
K1147_AUDIT_SHA256 = "17dbd6ab3a9a9b5aef1cf1cf517a5a0fd216dff755f0ed86fcf029e1612cabcb"
EXPECTED_ZERO_ROWS = [
    "00000000000000003800000008002010",
    "0000000000000000380000000a080000",
    "00000000020000801202000000100000",
]
EXPECTED_ROOTS = {
    "00000000000000103800000009080040",
    "0000000000000010380000000a080040",
    "0000000000000010380000000b080000",
    "00000000020000801202000011100000",
    "00000000020000801202000810100000",
    "00000000020000809202000800100000",
    "00000000020000841202000010100000",
    "00000000020000841202000800100000",
}
TRANSFORMS = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0: X, Y = x, y
        elif t == 1: X, Y = 10-y, x
        elif t == 2: X, Y = 10-x, 10-y
        elif t == 3: X, Y = y, 10-x
        elif t == 4: X, Y = 10-x, y
        elif t == 5: X, Y = x, 10-y
        elif t == 6: X, Y = y, x
        else: X, Y = 10-y, 10-x
        tab.append(11*Y+X)
    TRANSFORMS.append(tab)
PERMS = list(itertools.permutations(range(4)))
SUBS6 = list(itertools.combinations(range(8), 6))

def sha256(data): return hashlib.sha256(data).hexdigest()
def bits(mask):
    out=[]
    while mask:
        low=mask & -mask; out.append(low.bit_length()-1); mask ^= low
    return out
def transform_mask(mask,t):
    out=0
    for p in bits(mask): out |= 1 << TRANSFORMS[t][p]
    return out
def canonical(mask): return min(transform_mask(mask,t) for t in range(8))
def determinant4(points):
    rows=[]
    for p in points:
        x,y=p%11,p//11
        rows.append((x,y,x*x+y*y,1))
    total=0
    for perm in PERMS:
        inv=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        product=1
        for i,j in enumerate(perm): product *= rows[i][j]
        total += -product if inv & 1 else product
    return total
def first_forbidden_quad(root):
    pts=bits(root)
    for quad_idx in itertools.combinations(range(8),4):
        quad=tuple(pts[i] for i in quad_idx)
        if determinant4(quad)==0:
            return {"indices":list(quad),"coordinates_xy":[[p%11,p//11] for p in quad]}
    return None
def child_coverage(root,row_index):
    pts=bits(root); found=set()
    for keep in SUBS6:
        child=0
        for i in keep: child |= 1 << pts[i]
        child=canonical(child)
        if child in row_index: found.add(row_index[child])
    return found
def direct_roots_containing_row(row):
    empty=[p for p in range(121) if not (row>>p)&1]
    if len(empty)!=115: raise SystemExit("FAIL-CLOSED: source row is not six stones")
    roots=set()
    for a,b in itertools.combinations(empty,2):
        roots.add(canonical(row | (1<<a) | (1<<b)))
    return roots,6555

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True); ap.add_argument("--k1148-audit",required=True)
    ap.add_argument("--k1147-audit",required=True); ap.add_argument("--output",required=True)
    args=ap.parse_args()
    ib=Path(args.input).read_bytes(); b8=Path(args.k1148_audit).read_bytes(); b7=Path(args.k1147_audit).read_bytes()
    if sha256(ib)!=INPUT_SHA256: raise SystemExit("FAIL-CLOSED: input fixture SHA-256 mismatch")
    if sha256(b8)!=K1148_AUDIT_SHA256: raise SystemExit("FAIL-CLOSED: K1148 audit SHA-256 mismatch")
    if sha256(b7)!=K1147_AUDIT_SHA256: raise SystemExit("FAIL-CLOSED: K1147 audit SHA-256 mismatch")
    fixture=json.loads(ib); k1148=json.loads(b8); k1147=json.loads(b7)
    rows_hex=fixture["residual_rows"]; rows=[int(x,16) for x in rows_hex]
    row_index={row:i for i,row in enumerate(rows)}
    excluded={int(x,16) for x in fixture["refuted_d10_roots_excluded"]}
    expected_avail=fixture["expected_per_row_triple_availability"]
    if len(rows)!=23 or len(row_index)!=23 or len(excluded)!=50:
        raise SystemExit("FAIL-CLOSED: malformed residual/exclusion fixture")
    zero_indices=[i for i,n in enumerate(expected_avail) if n==0]
    zero_rows=[rows_hex[i] for i in zero_indices]
    if zero_rows!=EXPECTED_ZERO_ROWS or zero_indices!=[1,2,21]:
        raise SystemExit("FAIL-CLOSED: fixture zero rows differ from pinned target")
    k1148_zero_map={x["row"]:x for x in k1148["zero_provider_rows"]}
    if not k1148["checks_all_ok"] or k1148["status"] != "third-independent-geometric-reconstruction-passed":
        raise SystemExit("FAIL-CLOSED: K1148 third-geometry audit is not PASS")
    if k1148["inputs"]["source_pins"] != fixture["source_pins"]:
        raise SystemExit("FAIL-CLOSED: K1148 source pins differ from input fixture")
    if k1148["enumeration"]["per_row_triple_availability"] != expected_avail:
        raise SystemExit("FAIL-CLOSED: K1148 availability differs from pinned fixture")
    if not k1147["checks_all_ok"] or k1147["checks_total"]!=71:
        raise SystemExit("FAIL-CLOSED: K1147 external audit is not 71/71 PASS")
    k1147_gates = {x["name"]: x["ok"] for x in k1147["results"]}
    if not all(k1147_gates.get(name) is True for name in (
        "audit-max-cover-3", "certificate-rows-match", "certificate-kmin-kmax-recorded", "certificate-contradiction")):
        raise SystemExit("FAIL-CLOSED: K1147 global max-cover/counting gates are not PASS")
    if k1147["published_decision_sha256"] != fixture["source_pins"]["eight_root_decision_json_sha256"]:
        raise SystemExit("FAIL-CLOSED: K1147 decision pin differs from fixture source pin")
    if set(k1147["structure_observations"]["zero_triple_rows"])!=set(zero_rows):
        raise SystemExit("FAIL-CLOSED: K1147 zero rows disagree with pinned fixture")

    per_row=[]; union_records={}; total_events=0; total_unique=0; total_child_tests=0
    for idx in zero_indices:
        roots,events=direct_roots_containing_row(rows[idx])
        total_events+=events; total_unique+=len(roots); coverage_hist=Counter(); triple_roots=[]
        for root in sorted(roots):
            if root != canonical(root) or root.bit_count() != 8:
                raise SystemExit("FAIL-CLOSED: generated root is not canonical 8-stone")
            covered=child_coverage(root,row_index); coverage_hist[len(covered)]+=1; total_child_tests+=28
            if len(covered) > 3:
                raise SystemExit("FAIL-CLOSED: a zero-row root covers more than three residual rows")
            if len(covered)==3:
                if idx not in covered: raise SystemExit("FAIL-CLOSED: generated root misses source row")
                triple_roots.append((root,covered))
        row_records=[]
        for root,covered in triple_roots:
            forbidden=first_forbidden_quad(root); root_hex=f"{root:032x}"
            if forbidden is not None:
                classification="unsafe_cocircular_quadruple"; forbidden_xy=forbidden["coordinates_xy"]
                if root in excluded: raise SystemExit("FAIL-CLOSED: unsafe root appears in safe REFUTED exclusion")
            elif root in excluded:
                classification="safe_but_refuted_d10_excluded"; forbidden_xy=None
            else:
                classification="eligible_triple_provider"; forbidden_xy=None
            rec={"root":root_hex,"covered_row_indices":sorted(covered),
                 "classification":classification,"forbidden_quad_xy":forbidden_xy}
            row_records.append(rec); union_records[root]=rec
        safe_excluded=sum(x["classification"]=="safe_but_refuted_d10_excluded" for x in row_records)
        unsafe=sum(x["classification"]=="unsafe_cocircular_quadruple" for x in row_records)
        eligible=sum(x["classification"]=="eligible_triple_provider" for x in row_records)
        expected=k1148_zero_map.get(rows_hex[idx])
        if expected is None: raise SystemExit("FAIL-CLOSED: K1148 zero-row record missing")
        if (len(row_records)!=expected["candidate_root_count"] or safe_excluded!=expected["safe_excluded_root_count"]
            or unsafe!=expected["unsafe_root_count"] or eligible!=0):
            raise SystemExit("FAIL-CLOSED: direct row+two-point counts disagree with K1148")
        per_row.append({
            "row_index":idx,"row":rows_hex[idx],"generation_events":events,
            "unique_D4_roots_containing_row":len(roots),"intrinsic_child_tests":28*len(roots),
            "child_coverage_histogram":{str(k):coverage_hist[k] for k in sorted(coverage_hist)},
            "triple_candidate_roots":len(row_records),"safe_but_excluded":safe_excluded,
            "unsafe":unsafe,"eligible_in_P3":eligible,"candidate_roots":row_records,
        })
    union_hex={f"{r:032x}" for r in union_records}
    if union_hex!=EXPECTED_ROOTS or len(union_records)!=8:
        raise SystemExit("FAIL-CLOSED: direct generation root union differs from K1148")
    expected_union={x["root"]:x for x in k1148["zero_rows_candidate_root_union"]}
    if set(expected_union)!=union_hex: raise SystemExit("FAIL-CLOSED: K1148 candidate-root union differs")
    for root_int,rec in union_records.items():
        root_hex=f"{root_int:032x}"
        old=expected_union[root_hex]
        if rec["covered_row_indices"]!=old["covered_row_indices"] or rec["classification"]!=old["classification"] or rec["forbidden_quad_xy"]!=old["forbidden_quad_xy"]:
            raise SystemExit("FAIL-CLOSED: direct root record differs from K1148")
    counts=[len(x["candidate_roots"]) for x in per_row]
    excluded_counts=[x["safe_but_excluded"] for x in per_row]
    unsafe_counts=[x["unsafe"] for x in per_row]
    if counts!=[4,5,5] or excluded_counts!=[1,2,1] or unsafe_counts!=[3,3,4]:
        raise SystemExit("FAIL-CLOSED: per-row candidate classification counts differ")

    a=3; k_min=(a+1)//2; k_max=3*8-23
    capacity=2*k_min-a+3*(8-k_min)
    if not (k_min==2 and k_max==1 and capacity==19):
        raise SystemExit("FAIL-CLOSED: counting certificate arithmetic mismatch")
    checks=[
        {"name":"input-and-two-published-audit-pins","ok":True},
        {"name":"K1148-third-geometry-audit-and-source-pins","ok":True},
        {"name":"K1147-71-check-audit-global-capacity-gates-and-zero-row-agreement","ok":True},
        {"name":"direct-row-plus-two-empty-points-19665-events","ok":total_events==19665},
        {"name":"all-zero-row-roots-D4-canonicalized-and-cover-at-most-three-rows","ok":True},
        {"name":"all-C8,6-children-reconstructed","ok":total_child_tests==28*total_unique},
        {"name":"per-row-triple-candidate-counts-4-5-5","ok":counts==[4,5,5]},
        {"name":"zero-row-candidate-root-union-eight","ok":union_hex==EXPECTED_ROOTS},
        {"name":"root-classification-unsafe5-safe-excluded3","ok":
            sum(x["classification"]=="unsafe_cocircular_quadruple" for x in union_records.values())==5 and
            sum(x["classification"]=="safe_but_refuted_d10_excluded" for x in union_records.values())==3},
        {"name":"no-eligible-triple-provider-for-any-zero-row","ok":all(x["eligible_in_P3"]==0 for x in per_row)},
        {"name":"exact-match-to-K1148-independent-triple-union-geometry","ok":True},
        {"name":"counting-certificate-kmin2-kmax1-capacity19","ok":True},
    ]
    if not all(x["ok"] for x in checks): raise SystemExit("FAIL-CLOSED: internal gate failed")
    result={
        "schema":"n11-residual23-zero-triple-direct-fourth-geometry-20261121-v1",
        "status":"direct-row-plus-two-point-fourth-geometry-passed",
        "source_pins":{"input_fixture_sha256":INPUT_SHA256,"k1148_third_geometry_audit_sha256":K1148_AUDIT_SHA256,
                       "k1147_external_second_verification_audit_sha256":K1147_AUDIT_SHA256},
        "method":{"generation":"for each zero row, add every unordered pair among its 115 empty board points",
                  "canonicalization":"minimum 128-bit mask over all eight D4 transforms",
                  "coverage":"reconstruct all C(8,6)=28 children and canonicalize each independently",
                  "safety":"direct 4x4 determinant of (x,y,x^2+y^2,1), expanded over 24 permutations",
                  "independence":"does not use K1148's 3-row x 8^3 orientation-union generator or either published 3x3 determinant predicate"},
        "enumeration":{"zero_rows":zero_rows,"zero_row_count":3,"generation_events":total_events,
                       "unique_D4_roots_per_zero_row":[x["unique_D4_roots_containing_row"] for x in per_row],
                       "unique_D4_roots_containing_zero_rows_sum":total_unique,"intrinsic_child_tests":total_child_tests,
                       "triple_candidate_roots_per_zero_row":counts,"candidate_root_union_size":len(union_records),
                       "candidate_root_union":[union_records[k] for k in sorted(union_records)]},
        "per_zero_row":per_row,
        "counting_certificate":{"max_rows_per_P3_provider":3,"zero_rows_with_no_P3_triple_provider":3,
                                "minimum_roots_touching_zero_rows":k_min,
                                "maximum_other_rows_coverable_by_eight_roots":capacity,
                                "other_rows_required":20,"strict_deficit":1,
                                "conclusion":"an 8-root cover of the residual-23 rows is impossible in P'''"},
        "checks":checks,"checks_all_ok":True,
        "trust_boundary":"This fourth geometry independently re-derives all roots containing the three zero rows from row+two-empty-point generation and direct 4x4 determinants. The global P''' provider maximum of three rows and the REFUTED-D10 exclusion list are imported from pinned K1147/K1148 records; no DFPN verdict, certificate, receipt, or game outcome is created.",
        "interpretation_guard":["No residual row is closed by this computation.","REFUTED-D10 is not a LOSS proof.",
            "Candidate-root cover counts are planning geometry, not game-theoretic certificates.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."]
    }
    output=(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    Path(args.output).write_bytes(output)
    print(json.dumps({"status":result["status"],"output_sha256":sha256(output),"output_bytes":len(output),
                      "checks":len(checks),"generation_events":total_events,"unique_roots_sum":total_unique,
                      "candidate_root_union":len(union_records),"candidate_counts":counts},
                     ensure_ascii=False,sort_keys=True))

if __name__=="__main__": main()
