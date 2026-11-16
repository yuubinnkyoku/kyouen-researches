# class2-lane: cost-62 neighbor 70j-coverage pre-check (2026-11-16)

## What was done

- The cost-60c fold record (head 1410) names the next unswept one-stone-replacement neighbor of the STERILE 70j child, cost 62 00000000000000801282020000000000, and requests a pre-check whether any legal root covers the 70j row before sweeping. This run performs that pre-check with the verified third implementation (the same one behind the 1405->1419 row-level fold verification).

## Results

- Candidate cost re-enumerated exactly: 62 legal roots (claimed 62).
- Coverage at the D4-orbit level: **2 of the 62 roots cover the open STERILE 70j row** - bit 21 (root 00000000000000801282020000200000, canonical itself) and bit 109 (root 00002000000000801282020000000000, canonical 00000000000080829002000000000800).
- Neither covering root is D4-equal to the known REFUTED-D10 cross-cover root of the cost-60c sweep (bit 119, canonical 00000000000000881282000000200000). Both are fresh, unrefuted certificate targets.
- 65k (00000000020000801202000000200000) and 74h (00000000000000889002000000000800): 0/62 coverage each - this candidate cannot close them.
- Candidate status at 1419: still open (open at 1410 per the fold record; not among the 65j lost children D4-canonically; none of its six parent orbits is a 65j fold parent).

## Sweep decision

- DO NOT SKIP the cost-62 sweep: if bit 21 or bit 109 yields a WIN7-D10 certificate, the STERILE 70j row closes via cross-cover (the known loophole for STERILE rows). These two bits are the sweep's 70j-relevant targets; the other 60 roots are relevant only for the candidate's own orbit (cost 62) and in-manifest marginals.
- The engine lane should prioritize bits 21 and 109 for certificate extraction when running this candidate.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged).
- No game-theoretic value is asserted by this pre-check; a covering root still requires a WIN7-D10 certificate.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost62-neighbor-70j-coverage-precheck-20261116.json`
