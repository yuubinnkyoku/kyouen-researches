"""Task 4: PGL(3,8)-orbits of the maximal 6-caps A, B, C by exhaustive BFS.

The BFS uses the same 8 explicit generators as verify_core.py (which were
proved to generate a group of order 16,482,816 = |PGL(3,8)|, acting as
collineations).  The orbit found is therefore exactly the PGL orbit.

Outputs:
  orbit_A.bin, orbit_B.bin, orbit_C.bin   (6 bytes per cap, increasing point order)
  orbit_results.json

Run:  python orbit_bfs.py
"""

import json
import os
import sys
import time
from array import array

import pg2q8 as G

HERE = os.path.dirname(os.path.abspath(__file__))

A = (10, 47, 49, 55, 61, 64)
B = (17, 27, 30, 44, 52, 70)
C = (8, 48, 50, 51, 58, 61)

ph = G.phi_perm()
ph2 = G.perm_mul(ph, ph)
PHI_A = tuple(sorted(ph[p] for p in A))
PHI2_A = tuple(sorted(ph2[p] for p in A))

CAPS = {"A": A, "B": B, "C": C, "phi(A)": PHI_A, "phi^2(A)": PHI2_A}

def cap_key(cap):
    return tuple(sorted(cap))

def bfs(start, gens, target_caps):
    """Exhaustive BFS of the orbit of `start`; parent tree recorded."""
    start = cap_key(start)
    caps = [start]
    idx = {start: 0}
    parent = array("i", [-1])
    pgen = array("b", [-1])
    target_idx = {}
    head = 0
    while head < len(caps):
        cur = caps[head]
        for gi, g in enumerate(gens):
            nxt = tuple(sorted(g[p] for p in cur))
            j = idx.get(nxt)
            if j is None:
                j = len(caps)
                idx[nxt] = j
                caps.append(nxt)
                parent.append(head)
                pgen.append(gi)
                if nxt in target_caps:
                    target_idx[nxt] = j
            elif nxt in target_caps and nxt not in target_idx:
                target_idx[nxt] = j
        head += 1
        if head % 200000 == 0:
            print(f"    ... {head} caps", flush=True)
    return caps, idx, parent, pgen, target_idx

def witness(start, target, target_idx, caps, parent, pgen, gens):
    """Recover a word in the generators mapping start to target."""
    j = target_idx[target]
    seq = []
    while parent[j] != -1:
        seq.append(pgen[j])
        j = parent[j]
    seq.reverse()
    perm = G.IDENT
    for gi in seq:
        perm = G.perm_mul(perm, gens[gi])
    return perm, seq

def main():
    t0 = time.time()
    mats = G.pgl_generators()
    gens = [G.mat_perm(M) for M in mats]
    assert G.group_order(gens) == 16_482_816

    targets = set(CAPS.values())
    out = {"orbits": {}, "probe_sets": {k: list(v) for k, v in CAPS.items()}}
    sizes = {}
    memberships = {}

    for name in ("A", "B", "C"):
        start = CAPS[name]
        print(f"\nBFS orbit of {name} = {start} ...", flush=True)
        t1 = time.time()
        caps, idx, parent, pgen, target_idx = bfs(start, gens, targets)
        dt = time.time() - t1
        print(f"  orbit size {len(caps)}  ({dt:.1f}s)", flush=True)
        sizes[name] = len(caps)
        memberships[name] = {pname: (cap_key(pcap) in idx) for pname, pcap in CAPS.items()}
        print("  membership:", memberships[name])
        # save caps
        path = os.path.join(HERE, f"orbit_{name}.bin")
        with open(path, "wb") as f:
            for cap in caps:
                f.write(bytes(cap))
        # witnesses
        wit = {}
        if name == "C" and cap_key(PHI_A) in target_idx:
            perm, seq = witness(start, cap_key(PHI_A), target_idx, caps, parent, pgen, gens)
            assert cap_key(perm[p] for p in start) == cap_key(PHI_A)
            wit["to_phi(A)"] = {"word_len": len(seq), "word_generators": seq,
                                "maps_start_to": [perm[p] for p in start]}
            print(f"  witness C -> phi(A): word length {len(seq)}")
        if name == "B" and cap_key(PHI2_A) in target_idx:
            perm, seq = witness(start, cap_key(PHI2_A), target_idx, caps, parent, pgen, gens)
            assert cap_key(perm[p] for p in start) == cap_key(PHI2_A)
            wit["to_phi^2(A)"] = {"word_len": len(seq), "word_generators": seq,
                                  "maps_start_to": [perm[p] for p in start]}
            print(f"  witness B -> phi^2(A): word length {len(seq)}")
        out["orbits"][name] = {"size": len(caps), "seconds": dt,
                               "membership": memberships[name], "witness": wit,
                               "start": list(start)}
        del caps, idx, parent, pgen, target_idx
        import gc
        gc.collect()

    out["sizes"] = sizes
    out["memberships"] = memberships
    out["union_size"] = sum(sizes.values())
    out["checks"] = {
        "sizes_are_686784": all(s == 686_784 for s in sizes.values()),
        "phiA_in_orbit_C": memberships["C"]["phi(A)"],
        "phi2A_in_orbit_B": memberships["B"]["phi^2(A)"],
        "A_not_in_orbit_B": not memberships["B"]["A"],
        "A_not_in_orbit_C": not memberships["C"]["A"],
        "B_not_in_orbit_C": not memberships["C"]["B"],
        "phiA_not_in_orbit_A": not memberships["A"]["phi(A)"],
        "phi2A_not_in_orbit_A": not memberships["A"]["phi^2(A)"],
        "phiA_not_in_orbit_B": not memberships["B"]["phi(A)"],
        "phi2A_not_in_orbit_C": not memberships["C"]["phi^2(A)"],
    }
    out["elapsed_sec"] = time.time() - t0
    with open(os.path.join(HERE, "orbit_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print("\n== orbit results ==")
    for name, s in sizes.items():
        print(f"  orbit {name}: {s}")
    print("  union:", out["union_size"])
    for k, v in out["checks"].items():
        print(("PASS " if v else "FAIL ") + k)
    print(f"total time {out['elapsed_sec']:.1f}s")
    return 0 if all(out["checks"].values()) else 1

if __name__ == "__main__":
    sys.exit(main())
