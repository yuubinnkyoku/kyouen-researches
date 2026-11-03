# Finite tree real-root audit (2026-11-03)

This is **finite exhaustive enumeration**, not a proof for arbitrary trees or arbitrary q.

For every unlabelled tree on 4..8 vertices with maximum degree at least 3, and each r=q-3 in {1,2,3,4,5}, enumerate all admissible cores B directly using K0648's formula. SymPy's exact real-root count (Sturm method) verifies that the center-containing terminal polynomial has strictly fewer negative real roots (counted with multiplicity) than its degree. Thus it is **not** real-rooted.

Branching-tree counts by n: 4:1, 5:2, 6:5, 7:10, 8:22. Total 200 tree/r cases. The result suggests, but does not prove, that among trees only paths have center-containing real-rooted terminal polynomials for all q>=4. K0664 proves the path direction; K0665 proves the star obstruction. Whether every non-path tree fails for every q remains open.

Run: `python verify.py` (requires networkx and sympy). This verifier uses the direct K0648 core formula rather than any root-location floating-point approximation.
