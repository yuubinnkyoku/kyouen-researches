# 2026-11-27 n11 ninth-cost parked-3 L50M rows third-impl corroboration: completion

Wave A declaration: commit 9b4cdaac
(`research/log/2026-11-27-n11-ninthcost-parked3-l50m-thirdimpl-declaration.md`).
Wave B kit: commit a8867e6a
(`research/experiments/n11-ninthcost-parked3-l50m-thirdimpl-corroboration-20261127/`,
README + scripts/third_impl.js (pin 08ea958f) + 6 raws + MANIFEST-sha256.txt).

## Outcome

CORROBORATION-PASS (verdict-level) on all three pre-registered targets,
pre-registered acceptance met exactly:

| key | published replica L50M row | third_impl (2 cold passes each) | verdict-level |
| --- | --- | --- | --- |
| k02 | WIN(1) nodes 18,123,017 | result 1 WIN, expansions 21,380,266 | AGREE |
| k04 | LOSS(2) nodes 24,309,957 | result 2 LOSS, expansions 28,939,982 | AGREE |
| k07 | WIN(1) nodes 27,621,128 | result 1 WIN, expansions 33,128,202 | AGREE |

All 6 passes: reason clean, node_rc=0 (captured directly by the shell in
the same command), quads=95670, legal derived == published legal (87/98/96),
per-key pairs identical on every field except wall_s. No INDET pass, no
discarded pass. Execution strictly after the declaration push
(publish-then-execute honored). Kit fetch-back: 9/9 files byte-verified
against the published commit via the authenticated contents API
(raw CDN 10-minute propagation delay disclosed; commit-pinned read used).

## Status after this Part

Every resolved row of the ninth-cost ladder (9 LOSS + 3 WIN) now has the
third-implementation pillar. The k02/k04/k07 C++ second-implementation
scrutiny gate (Part SR/SW/SX pattern, budget 50,000,000, expected
node-exact quads k02 WIN(1) 18,123,017 / k04 LOSS(2) 24,309,957 /
k07 WIN(1) 27,621,128; full machine-derived quadruples in the gate kit)
remains OPEN. After
that gate the three rows join the adoption-eligible set; the batch
adoption Part (BASE 0935c94c, fresh single-owner declaration, WIN/LOSS
conflict review, merger 90711961, flip-census review for the WIN rows
per the k12 precedent) is a separate lane step.

Verdict NOT consumed: no cache increment, no class-status change, no
coverage claim, no adoption. Standard 11x11 empty board UNKNOWN; all 19
central-reply roots UNKNOWN; two-stone root {60,27} UNKNOWN; third-move
pair {100,108} UNKNOWN; every closure class UNKNOWN unless a published
Part says otherwise. Nodes and expansions are bookkeeping.
