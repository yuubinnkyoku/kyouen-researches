"""Tasks 3 (required) and full independent PGL orbit enumeration.

For every representative in reps.py, BFS its orbit under the verified
2-generator set of PGL(3,8), record the orbit size and the membership of all
other representatives and of the Frobenius images.  Results are written to
orbits_output.json incrementally.
"""
import gc
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import bfs as B
import reps as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "orbits_output.json")


def phi_perm(pts):
    return sorted(C.PHI[p] for p in pts)


def phi2_perm(pts):
    return sorted(C.PHI[C.PHI[p]] for p in pts)


def main():
    reps = R.REPS
    rep_masks = {label: B.mask_of(pts) for _, label, pts, _, _ in reps}
    results = {}
    t_start = time.time()
    for k, label, pts, expected, cls in reps:
        print(f"\n=== {label} (k={k}) expected {expected} ===", flush=True)
        t0 = time.time()
        seen, orb = B.orbit_bfs(pts, progress=500000, label=label)
        size = len(seen)
        dt = time.time() - t0
        print(f"  orbit size {size} (expected {expected}) in {dt:.1f}s",
              flush=True)
        assert size == expected, (label, size, expected)
        # sample caps from the orbit and verify they are caps
        sample_ok = True
        for idx in range(0, len(orb), max(1, len(orb) // 500)):
            pts2 = B.points_of(orb[idx])
            if not C.is_cap(pts2):
                sample_ok = False
                break
        assert sample_ok, label + " contains a non-cap"
        # memberships of all representatives
        mem = {other: (rep_masks[other] in seen) for _, other, _, _, _ in reps}
        self_ok = mem[label]
        assert self_ok
        # Frobenius images
        pm = B.mask_of(phi_perm(pts))
        p2m = B.mask_of(phi2_perm(pts))
        rec = {
            "k": k,
            "class": cls,
            "size": size,
            "expected": expected,
            "seconds": round(dt, 2),
            "caps_sample_ok": sample_ok,
            "memberships": mem,
            "phi_in_orbit": pm in seen,
            "phi2_in_orbit": p2m in seen,
            "phi_mask": pm,
            "phi2_mask": p2m,
        }
        # special probes for the maximal-6 triple (A -> C -> B -> A)
        for _, other, pts_o, _, _ in reps:
            if other.startswith("k6-max-"):
                om = rep_masks[other]
                rec[f"phi({other})_in_orbit"] = B.mask_of(
                    phi_perm(pts_o)) in seen
        results[label] = rec
        print(f"  phi(rep) in orbit: {rec['phi_in_orbit']}; "
              f"phi^2(rep) in orbit: {rec['phi2_in_orbit']}", flush=True)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=1, sort_keys=True)
        del seen, orb
        gc.collect()
    print("\ntotal time %.1fs" % (time.time() - t_start))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
