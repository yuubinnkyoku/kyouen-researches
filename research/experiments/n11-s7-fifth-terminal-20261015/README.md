# n11: fifth independently terminal-certified S7 WIN (2026-10-15)

Standard 11x11 q=4, complete calling, normal play. WIN/LOSS is fixed to the original first player (K0371); S7 and S9 are AND, S8 and S10 are OR.

Canonical S7 root: 00000000000400001000401108400000. Fixed-first WIN, side-to-move LOSS. The complete S7 boundary has 35 canonical S8 children. Each has an S9 WIN witness, and all S10 children of each selected S9 witness are WIN. The terminal-only certificate has 35 S8->S9 edges, 738 S9->S10 edges, 468 distinct S10 leaves and 93,481 memoized terminal states. Zero trusted cache leaves. Independent C++ and Python integer geometry and terminal solvers agreed on all 468 leaves (verdict, legal move count, memoized state count). Seven canonical S6 parents become fixed-first WIN, six new relative to the preceding 23.

Run with Python 3.10+ from this directory:

    python3 fifth_verify_standalone.py fifth-s7-win-terminal.cert

Do not use python -O. The checker enumerates legal geometry and all required AND children and independently recomputes every S10 game to terminal positions. The certificate and verifier are the complete proof; no cache file is required.

Selection-only progress: 935 new canonical S10 results, 850 WIN / 85 LOSS, independently checked by C++ and Python (268,300 memoized terminal states). Existing cache 34,167 -> 35,102; no overlapping key or conflict. Over 54 eligible S9 candidates the set-cover MILP reported 468 leaves and lower bound 468 (zero gap), not a global optimum proof. Full delta, C++ checker, mutation tests, candidate search, and source cache are preserved in conversation archive n11-fifth-s7-terminal-proof-20261015.zip, SHA256 1f48588f4164a053cf9c212df62d45fa4391e69db72102fe866d0a601e6dda0f. Only the cache-independent certificate and standalone verifier are required for the new theorem.

No two-stone root closed. The 11x11 empty-board winner is UNKNOWN.
