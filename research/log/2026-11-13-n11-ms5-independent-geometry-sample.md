# 2026-11-13 n11 S2 {59,60} milestone-5: independent geometric cost spot-check

Evidence level: deterministic sample audit, **not** a full independent certificate or verdict.

Baseline main: f15b5f567e5d14d935d8caed3af457a536ceca0c. Read AGENTS.md, research/knowledge/README.md, K0023, the milestone-5 experiment and recent n11 logs. Retrieved all six published ms5_s6_manifest_part*.csv files via GitHub connector, parsed 7,867 data rows and verified their recorded cost sum 615,497.

Independent check: sample row indices 0,37,74,...,7844 (zero-based; 213 rows). For each 128-bit six-stone hex key, enumerate all 121 board positions, exclude occupied positions, and for every candidate enumerate all 20 triples of existing stones. A candidate is forbidden if four points are collinear (zero 2D cross product) or concyclic. For noncollinear triple (P1,P2,P3), let A=P2-P1, C=P3-P1, E=P-P1, cross=det(A,C), q1=|P2|²-|P1|², q2=|P3|²-|P1|², qp=|P|²-|P1|². Test the exact integer equality

    (q1*C_y-q2*A_y)*E_x + (A_x*q2-C_x*q1)*E_y == qp*cross

and for collinear triples test det(A,E)==0. No floating point and no reuse of the source script's forbidden() circle-mask routine.

Result: **213/213 rows match** the published S7 legal-edge cost; zero disagreements; all sampled keys contain exactly six occupied positions. The six files together contain 7,867 rows and their published cost sum is 615,497.

Scope: deterministic sampling only (about 2.71% of rows), not a full geometry recount, not independent derivation of the S6 worklist or membership bits, and not a WIN/LOSS certificate. No game outcome is established; n11 empty root and S2 {59,60} remain **UNKNOWN**.
