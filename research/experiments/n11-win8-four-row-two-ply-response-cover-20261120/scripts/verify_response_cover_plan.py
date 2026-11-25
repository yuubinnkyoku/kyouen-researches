#!/usr/bin/env python3
"""Stdlib-only verifier for the four-row WIN8 two-ply response-cover plan.

It reconstructs safe 8-stone D4 root orbits for four pinned S6 rows, excludes
all known REFUTED-D10 root orbits from K1097, pins the two known WIN8 roots,
and verifies a 147-edge perfect matching plus a 1/2 dual lower bound.

No additional root is promoted to WIN8 by this script.  It verifies only the
geometry and the minimum candidate count conditional on later certificates.
"""
from __future__ import annotations
import hashlib, itertools, json, sys
from collections import Counter, defaultdict
from pathlib import Path

N = 11
CLAIMED_ROWS = [
    "00000000000000003800000008001080",
    "00000000000000003800000008001100",
    "00000000000000003800000008002080",
    "00000000000000003800000008002100",
]
FIXED_ROOTS = [
    "00000000000000003800000008003180",  # K1096: certificate triple-verified
    "0000000800000000380000000810000a",  # K1095: WIN8-D10 candidate, no certificate yet
]
KNOWN_WIN8_ROOTS = [
    "00000000000000003800000008003180",
    "00000000000000003800000008005021",
    "00000000000000003800000009840004",
    "00000000000000909002200080100000",
    "00000000000200003800200008180000",
    "00000000010000889002000080100000",
    "00000000012000003800080009000000",
    "00000000000000801202000000840500",
    "00000000000000801202000800880200",
    "00000000000020809002000480100000",
    "00000000000000003800000008d10000",
    "00000000000000043800000008180010",
    "00000000000000801212000001009000",
    "00000000000000801202000000901010",
    "00000000000000801202000022081000",
    "0000000800000000380000000810000a",
]
REFUTED_ROOTS = [
    "00000000000000003800000008710000","00000000000000003800000008b10000",
    "0000000000000000380010000a002010","00000000000000003800100028002040",
    "00000000000000043800000609000000","00000000000000043800020008900000",
    "00000000000000083800000048300000","00000000000000083820000048100000",
    "00000000000000103800000009080040","0000000000000010380000000b080000",
    "00000000000000103800000209080000","00000000000000143800000009080000",
    "00000000000000801202000000840300","00000000000000801202000000901002",
    "00000000000000801202000001000448","00000000000000801202000001004408",
    "00000000000000801202000001004440","00000000000000801202000001089000",
    "00000000000000801202020001005000","00000000000000801202020022001000",
    "00000000000000801202040000901000","00000000000000801212000001081000",
    "00000000000000821082000000000818","00000000000000821082000000000848",
    "00000000000000821082000000000890","000000000000008210820000000008c0",
    "00000000000000821086800000001000","00000000000000821086800000100000",
    "00000000000000841202000000880400","00000000000000a21083000000001000",
    "00000000000000a21083000000100000","00000000000040809002000022100000",
    "00000000000040809002000040102000","00000000000040809002000802100000",
    "00000000010000809002000040000006","00000000010000809002000040000009",
    "00000000020000801202080800100000","00000000020000809202000800100000",
    "00000000020008003800000009001000","00000000040000801202100100800000",
    "00000000100008003800000009001000","00000008000000003800000008100006",
    "00000010000000003840000008080040","0000001000000080120200000000040c",
    "00000010000000801202000000000414","00000010000000801202000000000444",
    "00000010000000801202040000000204","00000010000000809202000080000400",
    "00000010000010003800000008003000","00000010040000801202000100000200",
]
UPSTREAM = {
    "k1086_sweep_sha256": "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced",
    "k1095_sweep_sha256": "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707",
    "k1096_certificate_sha256": "1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c",
    "k1096_audit_sha256": "ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da",
    "k1096_certificate_git_blob_sha1": "afc0a1bc005215696e18e02baaaad3c3bf9ba599",
    "k1097_refsolve_git_blob_sha1": "4660c012333b04896c36a23a0837fbdbc2572ef9",
}
EXPECTED_REFUTED_INTERSECTION = "00000008000000003800000008100006"


def points_of(mask: int) -> list[int]:
    out=[]
    while mask:
        low=mask & -mask; out.append(low.bit_length()-1); mask ^= low
    return out


def xy(p: int) -> tuple[int,int]: return p % N, p // N


def lifted(p: int) -> tuple[int,int,int,int]:
    x,y=xy(p); return x*x+y*y,x,y,1


def det3(a: list[list[int]]) -> int:
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def det4_perm(ps: tuple[int,int,int,int]) -> int:
    rows=[lifted(p) for p in ps]; total=0
    for perm in itertools.permutations(range(4)):
        inv=sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        v=1
        for i in range(4): v*=rows[i][perm[i]]
        total += -v if inv & 1 else v
    return total


def safe(mask: int) -> bool:
    ps=points_of(mask)
    return all(det4_perm(q)!=0 for q in itertools.combinations(ps,4))


def coeff3(a: int,b: int,c: int) -> tuple[int,int,int,int]:
    rs=[lifted(p) for p in (a,b,c)]; out=[]
    for col in range(4):
        minor=[[rs[r][j] for j in range(4) if j!=col] for r in range(3)]
        v=det3(minor); out.append(-v if col%2==0 else v)
    return tuple(out)


def legal(mask: int) -> set[int]:
    ps=points_of(mask); banned=set(ps)
    for a,b,c in itertools.combinations(ps,3):
        cf=coeff3(a,b,c)
        for q in range(121):
            if q in (a,b,c): continue
            r=lifted(q)
            if sum(cf[j]*r[j] for j in range(4))==0: banned.add(q)
    return set(range(121))-banned


def legal_direct(mask: int) -> set[int]:
    return {q for q in range(121) if not (mask>>q)&1 and safe(mask | (1<<q))}


def tf(p: int,t: int) -> int:
    x,y=xy(p)
    table=[(x,y),(10-y,x),(10-x,10-y),(y,10-x),
           (10-x,y),(x,10-y),(y,x),(10-y,10-x)]
    X,Y=table[t]; return 11*Y+X


def transform(mask: int,t: int) -> int:
    z=0
    for p in points_of(mask): z |= 1<<tf(p,t)
    return z


def canonical(mask: int) -> int:
    return min(transform(mask,t) for t in range(8))


def build_geometry() -> dict:
    row_masks=[int(h,16) for h in CLAIMED_ROWS]
    row_legal=[legal(m) for m in row_masks]
    row_legal_direct=[legal_direct(m) for m in row_masks]
    if row_legal != row_legal_direct:
        raise AssertionError("independent legal-move implementations disagree")

    row_candidates=[]
    for pm,lm in zip(row_masks,row_legal):
        roots=set()
        for a in sorted(lm):
            l2=legal(pm | (1<<a))
            for b in sorted(l2):
                if b<=a: continue
                # Two exact legal additions imply the final 8-set is safe.
                roots.add(canonical(pm | (1<<a) | (1<<b)))
        row_candidates.append(roots)

    all_roots=set().union(*row_candidates)
    refuted_canon={canonical(int(h,16)) for h in REFUTED_ROOTS}
    refuted_hits=all_roots & refuted_canon
    known_win8_canon={canonical(int(h,16)) for h in KNOWN_WIN8_ROOTS}
    known_win8_hits=all_roots & known_win8_canon
    if {f"{x:032x}" for x in known_win8_hits}!=set(FIXED_ROOTS):
        raise AssertionError(("unexpected known-WIN8 intersection",[f"{x:032x}" for x in known_win8_hits]))
    if {f"{x:032x}" for x in refuted_hits}!={EXPECTED_REFUTED_INTERSECTION}:
        raise AssertionError(("unexpected known-refuted intersection",[f"{x:032x}" for x in refuted_hits]))
    available=all_roots-refuted_canon

    root_cover={}
    for r in sorted(available):
        imgs={transform(r,t) for t in range(8)}
        by_row=defaultdict(set)
        for ri,pm in enumerate(row_masks):
            for im in imgs:
                if (pm & im)==pm and (im ^ pm).bit_count()==2:
                    by_row[ri].update(points_of(im ^ pm))
        root_cover[r]=set((ri,q) for ri,qs in by_row.items() for q in qs)

    obligations=[(ri,q) for ri,lm in enumerate(row_legal) for q in sorted(lm)]
    fixed=[canonical(int(h,16)) for h in FIXED_ROOTS]
    if len(set(fixed))!=2 or any(r not in root_cover for r in fixed):
        raise AssertionError("known WIN8 roots missing from available candidate universe")
    if any(len(points_of(r))!=8 or not safe(r) for r in fixed):
        raise AssertionError("known WIN8 root is not a safe 8-set")
    fixed_images=[{transform(r,t) for t in range(8)} for r in fixed]
    if any(len(x)!=8 for x in fixed_images):
        raise AssertionError("a fixed root does not have 8 distinct D4 images")
    fixed_coverages=[root_cover[r] for r in fixed]
    if fixed_coverages[0] & fixed_coverages[1]:
        raise AssertionError("the two fixed roots overlap on first-move obligations")
    fixed_covered=set().union(*fixed_coverages)
    positive=set(obligations)-fixed_covered
    return {
        "row_masks":row_masks,"row_legal":row_legal,"row_legal_direct":row_legal_direct,
        "row_candidates":row_candidates,"all_roots":all_roots,"available_roots":available,
        "refuted_hits":refuted_hits,"known_win8_hits":known_win8_hits,"root_cover":root_cover,"obligations":set(obligations),
        "fixed_roots":fixed,"fixed_coverages":fixed_coverages,
        "fixed_covered":fixed_covered,"positive":positive,
    }


def main(plan_path: str, out_path: str) -> dict:
    plan=json.loads(Path(plan_path).read_text(encoding="utf-8"))
    geo=build_geometry()
    fixed=geo["fixed_roots"]
    fixed_cov=geo["fixed_covered"]
    positive=geo["positive"]
    if plan["fixed_roots"][0]["root_hex"]!=FIXED_ROOTS[0] or plan["fixed_roots"][1]["root_hex"]!=FIXED_ROOTS[1]:
        raise AssertionError("fixed-root metadata mismatch")
    if plan["fixed_roots"][0]["status"]!="certificate-verified": raise AssertionError("K1096 status mismatch")
    if plan["fixed_roots"][1]["status"]!="WIN8-D10-candidate-certificate-not-yet-extracted": raise AssertionError("K1095 status mismatch")
    if plan["obligations_total"]!=304 or plan["fixed_obligations_total"]!=10 or plan["positive_obligations_total"]!=294:
        raise AssertionError("obligation metadata mismatch")
    if plan["source_pins"]!=UPSTREAM: raise AssertionError("source pin mismatch")

    fixed_records=[]
    for i,r in enumerate(fixed):
        cov=geo["root_cover"][r]
        expected=[{"row_hex":CLAIMED_ROWS[ri],"first_moves":sorted(q for rri,q in cov if rri==ri)}
                  for ri in range(4) if any(rri==ri for rri,q in cov)]
        if plan["fixed_roots"][i]["coverage"]!=expected: raise AssertionError("fixed root coverage mismatch")
        fixed_records.append({"root_hex":f"{r:032x}","obligations":len(cov),"coverage":expected})

    # Exact dual certificate: weight 1/2 on all 294 obligations not covered by
    # the two known WIN8 roots; weight 0 on the 10 fixed obligations.
    positive_sizes=[]
    for r,cov in geo["root_cover"].items():
        if r in fixed: continue
        n=len(cov & positive)
        positive_sizes.append(n)
        if n>2: raise AssertionError((f"dual infeasible at {r:032x}",n))
        if n not in (1,2): raise AssertionError((f"unexpected candidate edge size at {r:032x}",n))

    selected=[]
    covered_positive=[]
    selected_set=set()
    for root_hex in plan["additional_roots"]:
        r=int(root_hex,16)
        if r not in geo["root_cover"] or r in fixed: raise AssertionError(f"unknown/fixed/refuted root {root_hex}")
        if r in selected_set: raise AssertionError("duplicate selected root")
        selected_set.add(r)
        if not safe(r): raise AssertionError((root_hex,"selected root unsafe"))
        cov=geo["root_cover"][r]
        pos=sorted(cov & positive)
        if len(pos)!=2: raise AssertionError((root_hex,"selected root does not cover two positive obligations",pos))
        # Check the two-point response is legal in both possible orders.
        for ri, move in pos:
            if move not in geo["row_legal"][ri]: raise AssertionError((root_hex,"illegal first move"))
        for ri in range(4):
            qs=sorted(q for rri,q in pos if rri==ri)
            if len(qs)==2:
                a,b=qs; parent=geo["row_masks"][ri]
                if b not in legal(parent | (1<<a)) or a not in legal(parent | (1<<b)):
                    raise AssertionError((root_hex,"illegal reply order"))
        covered_positive.extend(pos)
        selected.append(r)
    if len(selected)!=147: raise AssertionError(("additional roots",len(selected)))
    if len(set(covered_positive))!=294 or set(covered_positive)!=positive:
        raise AssertionError("selected roots do not form a perfect matching of all positive obligations")

    coverage_hist=Counter(len(cov) for cov in geo["root_cover"].values())
    row_counts=[len(s & geo["available_roots"]) for s in geo["row_candidates"]]
    degree=Counter(x for cov in geo["root_cover"].values() for x in cov)
    per_row=[]
    for ri,lm in enumerate(geo["row_legal"]):
        ds=[degree[(ri,q)] for q in lm if (ri,q) in positive]
        per_row.append({"row_hex":CLAIMED_ROWS[ri],"legal_moves":len(lm),
                        "available_safe8_candidate_orbits":row_counts[ri],
                        "positive_obligation_degree_min":min(ds),"positive_obligation_degree_max":max(ds),
                        "fixed_root_coverage":sorted(q for rri,q in fixed_cov if rri==ri)})
    positive_hist=Counter(positive_sizes)

    gates=[
        {"gate":"fixed_roots_are_safe_8_stone_with_8_d4_images","passed":all(len(points_of(r))==8 and safe(r) and len({transform(r,t) for t in range(8)})==8 for r in fixed)},
        {"gate":"four_parent_rows_are_safe_6_stone","passed":all(len(points_of(m))==6 and safe(m) for m in geo["row_masks"])},
        {"gate":"independent_exact_legal_move_methods_agree","passed":geo["row_legal"]==geo["row_legal_direct"]},
        {"gate":"known_win8_candidate_intersection_is_exactly_two","passed":len(geo["known_win8_hits"])==2 and {f"{r:032x}" for r in geo["known_win8_hits"]}==set(FIXED_ROOTS)},
        {"gate":"known_refuted_intersection_rebuilt_exactly","passed":len(geo["refuted_hits"])==1 and f"{next(iter(geo['refuted_hits'])):032x}"==EXPECTED_REFUTED_INTERSECTION},
        {"gate":"available_safe8_candidate_universe_has_9489_orbits","passed":len(geo["available_roots"])==9489},
        {"gate":"candidate_coverage_histogram_matches_9237_251_1","passed":coverage_hist==Counter({2:9237,4:251,8:1})},
        {"gate":"all_nonfixed_candidates_cover_at_most_two_positive_obligations","passed":max(positive_sizes)==2 and positive_hist==Counter({2:9351,1:136})},
        {"gate":"fixed_roots_cover_ten_distinct_obligations","passed":len(fixed_cov)==10},
        {"gate":"selected_147_roots_form_perfect_matching","passed":len(selected)==147 and len(set(covered_positive))==294 and set(covered_positive)==positive},
        {"gate":"dual_lower_bound_equals_matching_size","passed":len(positive)//2==len(selected)==147},
        {"gate":"no_s6_row_closed_or_game_value_claimed","passed":True},
    ]
    audit={
        "schema":"n11-win8-four-row-two-ply-response-cover-audit-20261120-v2",
        "date":"2026-11-20",
        "status":"geometric-plan-verified-no-row-closure",
        "source_pins":UPSTREAM,
        "fixed_roots":fixed_records,
        "known_win8_candidates_in_four_row_universe":len(geo["known_win8_hits"]),
        "known_win8_candidates_total_from_k1097":16,
        "known_refuted_roots_total_from_k1097":50,
        "known_refuted_root_orbits_intersecting_four_row_universe":[EXPECTED_REFUTED_INTERSECTION],
        "candidate_universe":{
            "safe8_d4_root_orbits_before_known_refuted_exclusion":len(geo["all_roots"]),
            "known_refuted_orbits_excluded":len(geo["refuted_hits"]),
            "available_safe8_d4_root_orbits":len(geo["available_roots"]),
            "row_memberships":sum(row_counts),
            "cross_row_membership_excess":sum(row_counts)-len(geo["available_roots"]),
            "coverage_obligations_histogram":dict(sorted(coverage_hist.items())),
            "nonfixed_positive_obligation_degree_histogram":dict(sorted(positive_hist.items())),
        },
        "per_row":per_row,
        "obligations":{
            "total_legal_first_moves":len(geo["obligations"]),
            "covered_by_known_win8_roots":len(fixed_cov),
            "remaining_positive_obligations":len(positive),
            "selected_additional_roots":len(selected),
            "total_known_plus_selected_roots":len(fixed)+len(selected),
            "positive_obligations_covered_exactly_once":len(set(covered_positive)),
            "selected_additional_root_row_incidence":dict(sorted(Counter(ri for r in selected for ri,q in geo["root_cover"][r]).items())),
        },
        "optimality_certificate":{
            "dual_weights":"1/2 on each of the 294 positive obligations; 0 on the 10 obligations covered by the two known WIN8 roots",
            "maximum_positive_obligations_covered_by_any_other_candidate":max(positive_sizes),
            "dual_objective":len(positive)/2,
            "lower_bound_additional_roots":len(positive)//2,
            "matching_upper_bound_additional_roots":len(selected),
            "optimality_proved":len(positive)//2==len(selected),
        },
        "plan_sha256":hashlib.sha256(Path(plan_path).read_bytes()).hexdigest(),
        "gates":gates,
        "all_gates_pass":all(g["passed"] for g in gates),
        "interpretation_guard":[
            "The K1096 root is a triple-verified certificate; the K1095 root is only a WIN8-D10 candidate and still needs extraction plus independent verification.",
            "The 147 additional roots are safe 8-stone candidates, not WIN8 verdicts or certificates.",
            "The 149-root total is an optimal geometric response-cover plan for these four S6 rows, conditional on proving all selected roots P for the player to move.",
            "No S6 row is closed by this audit. Receipt folding is not performed.",
            "This result does not determine the standard 11x11 empty board, the two-stone roots, S2, or classes 1/2/4.",
        ],
    }
    Path(out_path).write_text(json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return audit


if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: verify_response_cover_plan.py PLAN.json OUT.json")
    a=main(sys.argv[1],sys.argv[2])
    print(json.dumps({"all_gates_pass":a["all_gates_pass"],"available_candidates":a["candidate_universe"]["available_safe8_d4_root_orbits"],"additional_roots":a["obligations"]["selected_additional_roots"],"total_roots":a["obligations"]["total_known_plus_selected_roots"],"plan_sha256":a["plan_sha256"]},sort_keys=True))
