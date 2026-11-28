# 2026-11-28 eight-row q9 8x29 class-split continuation — amendment 1 (deeper-deficiency krow probes)

Amends: research/log/2026-11-28-eight-row-q9-m29-class-split-declaration.md
(commit c7bac259). Published BEFORE the deeper-krow pieces are executed.

## Amendment

- The declared krow=7 minpos sweeps (class {3} p=2..13, class {0} p=0..13,
  class {1} p=0..13) are extended with deeper-deficiency sub-bucket probes at
  8x29: krow=c:6 and krow=c:5 (deficient row of class {c} holds exactly 6 / 5
  stones), minpos p=0 first for each class {3},{0},{1}, continuing into the
  full minpos range 0..13 only where a probe shows tractability.
- Same 280 s cap, same WIN-stop rule, same per-piece absence semantics, same
  dual-verification protocol on any SAT, same non-claims (no 11x11 verdict
  consumption; no multi-deficiency coverage). All INDET pieces are honest
  negatives with disclosed conflicts.
- Rationale (disclosed): the first three executed krow=7 pieces
  (class {3} p2, class {0} p0, class {1} p0) each hit the 280 s cap at
  5,791,302 / 4,951,432 / 6,175,273 conflicts — near-uniform resistance,
  the same pattern as the published rowY=3/0/1 direct runs. The deeper-krow
  sub-buckets are distinct, smaller-stone instances whose tractability at
  the container cap is unknown and cheap to probe.
- No other change to the original declaration's scope, method, or claims.
- Amendment-time HEAD: checked immediately before this push.
