# single-token tail supply identity theorem (2026-11-26)

Universal closed-form case analysis for the per-k tail supply
identity that the strip kits (z26-floor20 census through the
sixth-wave kit) have been registering and pre-computing one k at a
time (k=31..46 published, plus k=39..46 candidates). The theorem
proves the pattern for ALL k >= 1 with no upper cap on s, closing the
per-k pre-computation lane. The proof is the written case analysis
below; the frozen audit script is mechanical corroboration only.

## Theorem (published single-token closed form, pin `bd5f22e4`)

For every integer k >= 1 and every integer s >= 1, with
A = v(s,k+1,k+1) and B = v(s,k,k+1):

- (i) 1 <= s <= k-1:  A = B = s mod 2        (HOLD)
- (ii) s = k, k odd:  A = B = 1              (HOLD)
- (iii) s = k, k even:  A = 0, B = 2         (single break)
- (iv) s >= k+1, k even:  A = 2, B = 1       (uniform break)
- (v) s >= k+1, k odd:  A = 0, B = 1         (uniform break)

Corollary: every per-k "tail supply chain candidate" registered by
the strip kits (k=31 thirtieth ... k=46 thirty-seventh) is the
restriction of this theorem to the kits' scan domain
{0} U {12..k+34}; the theorem holds for ALL k >= 1 and ALL s >= 1,
so no future k needs a pre-computation kit item. (The kits' floor 12
is a scan convention, not a structural boundary: the hold region is
all of {1..k-1}, values s mod 2.)

## Proof (case analysis over the closed form's branches)

The published closed form, for x = s, both seats R = k+1 fixed:
branch (0) x <= 0 -> 0; (1) z = 0 -> min(R,x) mod 2; (2) z = x;
(3) 1 <= z <= x-1; (4) z >= x+1; with m = q_odd(t) = t if t odd else
t-1. Assume k >= 2; k = 1 follows by the same steps (checked below).

Case s = 0: (0) both seats: A = B = 0 (degenerate; see boundary note).

Case I, 1 <= s <= k-1: A has z = k+1 >= s+1, B has z = k >= s+1, so
both seats take branch (4). m = q_odd(s) <= s < k+1 = R in both seats,
so (4b) gives A = s mod 2 and B = s mod 2. HOLD, value s mod 2. (i)

Case II, s = k: A has z = k+1 >= x+1 (branch 4): m = q_odd(k) <=
k < k+1 = R, so A = k mod 2. B has z = k = x (branch 2): if k even,
R = k+1 is odd and R <= 2x-1 = 2k-1 iff k >= 2, so (2a) gives B = 2;
if k odd, R = k+1 is even, (2b) needs R <= x-1 = k-1 but R = k+1,
so (2c) gives B = x mod 2 = 1. So k even: (A,B) = (0,2); k odd:
(A,B) = (1,1). (ii)/(iii)

Case III, s = k+1: A has z = x (branch 2): if k even, R = k+1 odd and
R <= 2x-1 = 2k+1 always, so A = 2; if k odd, R = k+1 even, (2b) needs
R <= x-1 = k, false, so (2c) gives A = x mod 2 = 0. B has z = k in
branch (3) (1 <= k <= x-1 = k): m = q_odd(k) <= k < R = k+1, and
(3b) applies since R = k+1 < x + z = 2k+1 iff k > 0, giving
B = (R+z) mod 2 = (2k+1) mod 2 = 1. So k even: (2,1); k odd: (0,1).

Case IV, s >= k+2: A has z = k+1 <= x-1 (branch 3): m = q_odd(k+1).
If k even, m = k+1 = R, so (3a) gives A = 2 (R odd). If k odd,
m = k < R = k+1, and (3b) applies since R < x + z = s+k+1 iff s > 0,
giving A = (R+z) mod 2 = (2k+2) mod 2 = 0. B has z = k <= x-1
(branch 3): m = q_odd(k) <= k < R = k+1, and (3b) applies since
R < x + z = s+k iff s > 1, giving B = (R+z) mod 2 = (2k+1) mod 2 = 1.
So k even: (2,1); k odd: (0,1). (iv)/(v)

The five cases cover all s >= 0 for fixed k; branch (1) never occurs
(z = k or k+1 >= 2). k = 1 is covered: Case I is empty, Case II at
s = 1 gives A = 1 (4b), B = 1 (2c with x = 1, R = 2 even, (2b) needs
R <= 0 false, x mod 2 = 1), Case III at s = 2 gives A = 0 (2c with
x = 2, R = 2, (2b) needs R <= 1 false, x mod 2 = 0), B = 1 (3b),
Case IV identical with s >= 3. QED (as a case analysis of the
published closed form).

The closed form equals both raw engines (canonical and ordered) on
every single-token position sampled in this audit and in every
strip-kit battery to date; the identity therefore describes the raw
engines on all s >= 1 seats where that published equivalence holds.

## Degenerate s = 0 boundary note (recorded by the audit)

At the meaningless zero-size-token input s = 0 the ENGINES return
H(R,(0,),z) = 1 on both seats (hold A = B = 1) while the closed form
returns 0 by its x <= 0 convention. This is a convention divergence
at the degenerate boundary only: no strip-kit measurement involves
x = 0 (row scans use parts >= m >= 13; tail scans are closed-form
only). Recorded verbatim in the audit output for the integrator.

## Files

| file | sha256 | size |
|---|---|---|
| `supply_identity_theorem_audit.py` | `d4a8922caf4ca981f55eec828299098e4abdb25917fe8b024e8a6951332df4f3` | 10327 B |
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | 2540 B |
| `supply_identity_theorem_audit.out` | `aafe5045140e6ca22a8435e2719157ddda31421ec58663ad43e44dd1230856e2` | 2756 B |

`engine_block.py` byte-identical to the series engine (pin
`bd5f22e4…`), embedded and asserted inside the audit script
(engine_gate PASS).

## Reproduce

```sh
python3 supply_identity_theorem_audit.py > outfile
cmp outfile supply_identity_theorem_audit.out
```

Determinism: 2/2 byte-identical runs, < 1 s per run.

## Audit results (finite corroboration; NOT the basis of universality)

- closed-form grid: k in {1..400}, s in {1..k+45}: 98,200/98,200
  positions agree with the case analysis (mismatches 0).
- large-s extension: k in {1,2,3,44,45,99,100,101,199,200},
  s in {k+46..k+300 step 7} plus s = k+5000: 380/380 agree — far
  beyond every kit scan cap (k+34).
- engine spot audit (canonical AND ordered engines): complete
  k in {1..14} x s in {1..k+10} plus sampled k in {15,16,20,21,30,
  31,43,44,50,51,64,65} x s in {k-1,k,k+1,k+2,k+10,2k}:
  317/317 agree on both engines.
- degenerate s=0 boundary: recorded (engines 1/1, closed form 0/0,
  engines satisfy the identity A = B at s = 0 as well).

FINITE audit observations corroborate but do not replace the case
analysis; the universal claim is the written proof above. No K slot
claimed by this experiment; knowledge-item promotion is deferred to
the integrator session (the closed-form/engine provenance numbering
used by the strip lane, "K0832"/"K1138"/"K1257", is not part of the
repo's `research/knowledge/items/` K-number space and must be
resolved there first). 11x11 empty board, two-stone roots, S2, class
1/2/4 and all central-reply roots UNKNOWN, unchanged; no verdict
consumed.
