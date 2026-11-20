#!/usr/bin/env python3
"""One-off MILP plan finder; the committed verifier does not require SciPy."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import scipy
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix, csr_matrix
from verify_response_cover_plan import (
    FIXED_ROOTS, CLAIMED_ROWS, UPSTREAM, build_geometry, points_of,
)


def main(out_path: str) -> None:
    geo=build_geometry()
    obligations=sorted(geo["obligations"])
    fixed=geo["fixed_roots"]
    fixed_cov=geo["fixed_covered"]
    positive=sorted(geo["positive"])
    positive_index={x:i for i,x in enumerate(positive)}
    roots=[r for r in sorted(geo["available_roots"]) if r not in fixed]
    A=lil_matrix((len(positive),len(roots)),dtype=np.float64)
    for j,r in enumerate(roots):
        cov=sorted(geo["root_cover"][r] & geo["positive"])
        if len(cov) not in (1,2): raise AssertionError((f"{r:032x}",cov))
        for x in cov: A[positive_index[x],j]=1.0
    A=csr_matrix(A)
    result=milp(c=np.ones(len(roots)),integrality=np.ones(len(roots)),
                bounds=Bounds(np.zeros(len(roots)),np.ones(len(roots))),
                constraints=LinearConstraint(A,np.ones(len(positive)),np.full(len(positive),np.inf)),
                options={"time_limit":120,"mip_rel_gap":0.0,"presolve":True})
    if result.status!=0 or abs(result.fun-len(positive)/2)>1e-8:
        raise RuntimeError(f"no minimum perfect matching: {result.status} {result.fun} {result.message}")
    selected=[roots[i] for i,x in enumerate(result.x) if x>0.5]
    if len(selected)!=147: raise AssertionError(len(selected))
    matched=set(); additional=[]
    for r in selected:
        pos=sorted(geo["root_cover"][r] & geo["positive"])
        if len(pos)!=2 or matched.intersection(pos): raise AssertionError((f"{r:032x}",pos))
        matched.update(pos)
        zero=sorted(geo["root_cover"][r] & fixed_cov)
        additional.append(f"{r:032x}")
    if matched!=set(positive): raise AssertionError("not a perfect matching")
    fixed_records=[]
    statuses=[
        {"status":"certificate-verified","source":"K1096","certificate_sha256":UPSTREAM["k1096_certificate_sha256"],"audit_sha256":UPSTREAM["k1096_audit_sha256"]},
        {"status":"WIN8-D10-candidate-certificate-not-yet-extracted","source":"K1095/K1097","sweep_sha256":UPSTREAM["k1095_sweep_sha256"],"refsolve_git_blob_sha1":UPSTREAM["k1097_refsolve_git_blob_sha1"]},
    ]
    for i,r in enumerate(fixed):
        cov=geo["root_cover"][r]
        coverage=[{"row_hex":CLAIMED_ROWS[ri],"first_moves":sorted(q for rri,q in cov if rri==ri)} for ri in range(4) if any(rri==ri for rri,q in cov)]
        fixed_records.append({"root_hex":FIXED_ROOTS[i],"canonical_root_hex":f"{r:032x}",**statuses[i],"coverage":coverage})
    plan={
        "schema":"n11-win8-four-row-two-ply-response-cover-plan-20261120-v2",
        "date":"2026-11-20",
        "status":"geometric-perfect-matching-plan-not-game-solved",
        "source_pins":UPSTREAM,
        "parent_rows":CLAIMED_ROWS,
        "fixed_roots":fixed_records,
        "known_refuted_root_orbits_excluded":[f"{r:032x}" for r in sorted(geo["refuted_hits"])],
        "candidate_universe_before_refuted_exclusion":len(geo["all_roots"]),
        "candidate_universe_after_refuted_exclusion":len(geo["available_roots"]),
        "obligations_total":len(geo["obligations"]),
        "fixed_obligations_total":len(fixed_cov),
        "fixed_obligations":[{"row_hex":CLAIMED_ROWS[ri],"first_move":q} for ri,q in sorted(fixed_cov)],
        "positive_obligations_total":len(positive),
        "additional_root_count":len(additional),
        "total_root_count_if_all_selected_are_proved_win8":len(fixed)+len(additional),
        "additional_roots":additional,
        "solver_discovery":{"method":"SciPy milp / HiGHS; plan validity and optimality are independently checked by the stdlib verifier","scipy_version":scipy.__version__,"status":int(result.status),"message":result.message,"objective":int(round(result.fun)),"mip_gap":float(result.mip_gap)},
        "interpretation_guard":[
            "K1096 is the only certificate-verified root among the two fixed roots.",
            "K1095 root is only a WIN8-D10 candidate; it still needs certificate extraction and independent verification.",
            "All 147 additional roots are safe 8-stone candidates only; they have no verdict or certificate in this plan.",
            "The 149-root count is optimal for this four-row two-ply response-cover construction, not a game-theoretic result.",
            "No S6 row is closed until every selected root is independently proved P and the reply strategy is folded.",
        ],
    }
    raw=json.dumps(plan,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    Path(out_path).write_text(raw,encoding="utf-8")
    print(json.dumps({"additional_roots":len(additional),"total_roots":len(fixed)+len(additional),"plan_sha256":hashlib.sha256(raw.encode()).hexdigest(),"scipy_version":scipy.__version__},sort_keys=True))

if __name__=="__main__": main(sys.argv[1] if len(sys.argv)>1 else "selected-response-cover-plan.json")
