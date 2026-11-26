# 2026-11-26 — single-token tail supply identity: UNIVERSAL closed-form theorem (case analysis) closes the per-k pre-computation lane for ALL k; degenerate x=0 engine/closed-form convention divergence discovered and recorded (no measurement affected); finite corroboration 98,200 + 380 grid points and 317 engine points (canonical + ordered) ALL PASS, determinism 2/2

Experiment: `research/experiments/single-token-tail-supply-identity-theorem-20261126/`
(supply_identity_theorem_audit.py `d4a8922c` 10327 B / engine_block.py
`582c93c1` pin `bd5f22e4` / frozen .out `aafe5045` 2756 B / README
with the full written proof).

Slot check (pre-claim, at build time): latest main head `1514e1f5`
(the sixth-wave kit publication). The strip kits have published per-k
tail supply identity pre-computations as registered handoff items
(#4 in each kit log S5, k=31..46, each verified in its scan domain
{0} U {12..k+34}), always phrased as "supply chain candidate N/N".
No universal statement of the identity exists in the published lane
(the kit logs and READMEs were checked; none claims the general k
result), and no knowledge item describes it (see the promotion note
below). The universal case analysis below is therefore new.

## The theorem

For the published single-token closed form v (pin `bd5f22e4`, the
transcription embedded byte-identically in every strip kit), for
every integer k >= 1 and every integer s >= 1, with A = v(s,k+1,k+1)
and B = v(s,k,k+1):

- 1 <= s <= k-1:  A = B = s mod 2        (HOLD; the kits' scan floor
  12 is a convention, not a structural boundary)
- s = k, k odd:    A = B = 1              (HOLD)
- s = k, k even:  A = 0, B = 2           (single break)
- s >= k+1, k even:  A = 2, B = 1        (uniform break, NO cap on s)
- s >= k+1, k odd:   A = 0, B = 1        (uniform break, NO cap on s)

Proof: five-case analysis over the closed form's branches (0)-(4)
with q_odd, written in full in the experiment README. Basis facts:
both seats share R = k+1; A has z = k+1, B has z = k; for
1 <= s <= k-1 both seats sit in branch (4) below m = q_odd(s); s = k
puts A in branch (4) and B in branch (2) (the k-parity fork); s = k+1
puts A in branch (2) and B in branch (3b); s >= k+2 puts A in branch
(3) with the q_odd(k+1) parity fork and B in branch (3b). QED over
the closed form. Transfer to the raw engines (canonical and ordered)
holds on all s >= 1 seats by the published single-token equivalence,
which every strip-kit battery re-verifies and this audit re-verifies
on 317 identity seats.

## What this closes, and the discovered divergence

1. The per-k pre-computation lane is CLOSED for every k: all future
   kit S5 item #4 registrations (k=45, 46, 47, ...) and their
   "candidate N/N" scans are corollaries. Future kits should cite
   this theorem (experiment dir + this log) instead of re-running
   per-k grids, keeping at most a small battery spot-check.
2. The registered scan-domain floor {12..} and cap k+34 were lane
   conventions; the theorem's hold region is ALL of {1..k-1} and the
   uniform break extends to ALL s >= k+1 (audit corroborated to
   s = k+5000).
3. DEGENERATE BOUNDARY DISCOVERY: at s = 0 (zero-size token) the raw
   engines return H(R,(0,),z) = 1 on BOTH seats (the identity
   A = B still holds) while the closed form returns 0 by its
   x <= 0 convention. The engines agree with the closed form on all
   s >= 1 positions sampled here and in every strip-kit battery; the
   divergence is confined to the degenerate x = 0 convention and
   affects NO strip-kit measurement (row scans use parts >= m >= 13;
   tail scans are closed-form only). Recorded verbatim in the audit
   output (degenerate_s0_boundary_record, k in {1,12,31,44,45}).

## Finite corroboration audit (frozen artifact, < 1 s, determinism 2/2)

- closed-form grid k in {1..400}, s in {1..k+45}: 98,200/98,200
  agree with the case analysis, mismatches 0.
- large-s extension k in {1,2,3,44,45,99,100,101,199,200},
  s in {k+46..k+300 step 7} + k+5000: 380/380 agree.
- engine spot audit on BOTH raw engines: complete k in {1..14} x
  s in {1..k+10} plus sampled k in {15,16,20,21,30,31,43,44,50,51,
  64,65} x s in {k-1,k,k+1,k+2,k+10,2k}: 317/317 agree.
- engine gate PASS (pin `bd5f22e4` assert).

FINITE audits corroborate only; the universal claim is the written
case analysis. 有限計算を全称性の根拠にはしていない。

## Deferred: knowledge-item promotion (explicitly NOT done here)

The natural promotion target is a `proposition` / `proved` item in
`research/knowledge/items/`, but the strip lane's provenance numbering
for the closed form and raw engines ("published K0832 single-token
closed form", "K1138 verifier block", "y22 machine K1257") does not
match the repo's current items K-number space (repo item K0832 is the
vertical-fiber item, and items run to K1021 with no K1138/K1257), so
a `depends_on` relation would currently point at the WRONG items.
Promotion is deferred to an integrator session that first resolves
which repo knowledge item (if any) carries the single-token closed
form, then registers this theorem as a proved proposition with
artifacts pointing at this experiment and log. No K slot is claimed
by this run.

## Handoff

1. Next kits: replace S5 item #4 per-k tail registrations by a
   pointer to this theorem (one-line corollary + optional battery
   spot-check); keep registering rows/touches at the same cadence.
2. Integrator: resolve the closed-form provenance K-number, promote
   this theorem (status `proved`, scope = all k >= 1, s >= 1 over the
   pinned closed form with engine transfer note, the s=0 convention
   divergence recorded), and note the two open structural questions
   below.
3. Open structural questions for the next case-analysis lane:
   (a) the same treatment for the two-supply family
   v(s,k+2,k+2) vs v(s,k,k+2) and general d-shifts — do they admit
   closed-form k-universal patterns too? (b) the m-row supply
   analogues of the strip bands (R = m+z+1, m in {13..18}) where the
   separation life-cycle scaffold lives — is the scaffold's
   "exactly two at birth slices" profile also a closed-form case
   analysis over the published shape-vs-collapse formula?

## Caveats

Finite machine observations + one written universal case analysis of
the PUBLISHED closed form; no claim beyond that closed form's
validity regime; engine transfer is sample-verified (317 seats +
every kit battery) and per the lane's published equivalence claim;
no K slot claimed (1 experiment != 1 K); 11x11 empty board,
two-stone roots, S2, class 1/2/4, 19 central-reply roots and all
closure classes: UNKNOWN unchanged; no verdict consumed.
