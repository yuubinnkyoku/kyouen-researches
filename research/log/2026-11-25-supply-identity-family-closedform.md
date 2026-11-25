# 2026-11-25 tail supply-identity family: complete closed-form characterization (K1334, provisional) — verification log

Lane: high-speed lane. Status of this document: primary record for
one new engine-free universal result (Theorem A, the supply-identity
family characterization) plus its Lemma S companion, published as
provisional knowledge item K1334 with the machine kit. No census
slot is claimed; no verdict of any game position is consumed. Same
session note: immediately before this work, the same session
completed the fetch-back addendum of the earlier crossrun kit
(commit `659658a`, log §4 of the crossrun record).

## 1. Context and ordering

The published census kits (z16..z22) sweep, in every slice, the
"tail supply identity" pair v(s,z+1,z+1) =? v(s,z,z+1) over
s in {0} U {12..59}, always labeled `engine_free` (pure K0832
closed-form precomputation) but recorded as FINITE observations
("ninth..fifteenth tail", "even-z form 3/3", "odd-z form 3/3",
predeclared candidates confirmed 4/4, etc.). The z18 kit even
records a failed naive "+2-shift, 1v0" prediction for the ninth
tail. This run derived, ON PAPER FIRST (K0832 branch arithmetic,
four cases), the complete universal characterization of the whole
family — including the parity split that explains the kits' even/odd
form tallies and the failed z18 guess — then built the machine kit
verify_k1334.py to (i) check the hand algebra over a wide grid,
(ii) re-validate the K0832 transcription against the raw engines,
and (iii) re-parse every published identity/spot row against the
theorem.

## 2. Theorem A (proved, engine-free)

For all k >= 1 and s >= 0, with A_k(s)=v(s,k+1,k+1) and
B_k(s)=v(s,k,k+1) (K0832 single-token closed form):

- A_k(s) = s mod 2 on [0..k]; for s >= k+1 constant: 0 (k odd) /
  2 (k even).
- B_k(s) = s mod 2 on [0..k-1]; B_k(k) = 1 (k odd) / 2 (k even);
  B_k(s) = 1 for ALL s >= k+1.

Hence the identity A=B holds exactly on [0..k] (k odd) / [0..k-1]
(k even), and the break is uniform in s with NO upper cutoff:
(0,1) from k+1 (k odd); (0,2) at k then (2,1) from k+1 (k even).

Proof: four-case branch computation on the K0832 closed form
(cases s<=k-1 / s=k / s=k+1 / s>=k+2; full text in the K1334 item).
Both K0832-side values at the break are branch-stable in s, which
is what makes the tail constants uniform forever.

## 3. Lemma S (proved, engine-free)

For all z >= 1, m >= 0 and token sums S >= max(z+1, m+2):
v(S, z, m+z+1) = (m+1) mod 2 — independently of S. On the T-Zz
lattice line R=m+z+1 the middle branch applies whenever two
explicit sum conditions hold. Instances:

- K1332 (base spot, m=z-5, S=2z-10, z>=11) is subsumed.
- Every published strip spot row (m in {z..z+3}, shapes
  (m+1,m), (m+2,m), (m+1,m,m)) and base spot row sits on
  (m+1)%2 on the collapse side.

## 4. Machine verification (kit, frozen output sha256 63f7730f...)

- Theorem A grid: k in {1..140} x s in {0..300}: 42,140 rows,
  0 mismatches.
- Lemma S: exhaustive small grid (z,m in {0..20}, S in {1..90}):
  31,850 in-conditions rows, 0 mismatches; 5,950 out-of-conditions
  rows with 2,915 formula failures recorded (conditions are
  necessary; nothing claimed there); wide boundary grid
  (z,m in {0..120}): 72,600 rows, 0 mismatches.
- K0832 transcription re-validation vs the RAW canonical engine:
  45,000 rows (x 1..30, z 0..24, R 1..60), 0 mismatches; vs the
  ordered engine on a subset: 5,850 rows, 0 mismatches.
- Determinism: SIX runs byte-identical (default x2,
  PYTHONHASHSEED=1, env -i same cwd, env -i isolated dir, plus a
  post-rename re-run after the K1333 -> K1334 renumbering; all
  six froze the same sha), rc 0.
- Engine: pinned block sha `bd5f22e4...` gate PASS; kit
  engine_block.py sha `582c93c1...` (same bytes as the chain).

## 5. Cross-artifact: every published row sits on the theorem

Inputs re-fetched from main and sha-pin-verified at runtime: z18
(`c4e7757c...`), z20 (`09e9026a...`), z21 (`10f94100...`), z22
(`f16a87d4...`); z19 recorded (`3354dfc6...`, no separate
published pin). Parsed and compared value-for-value:

- 13 identity sections, k = 17 (z17-partner recheck), 18 (ninth),
  19 (tenth), 20 (eleventh x2), 21 (twelfth x2), 22 (thirteenth
  x3), 23 (fourteenth x2), 24 (fifteenth): 614 rows, 0 mismatches
  — hold rows, break rows, break constants, and the `equal` fields
  all match the theorem exactly.
- 60 strip spot rows (12 per kit, m in {z..z+3}): all on
  (m+1)%2 with match=True, collapse recomputed from the closed
  form 60/60.
- 5 base spot rows (z=18..22, m=z-5): all on z%2, all match.
- 5 below-band sections (H(z+1;Y;z+1), 0 deviants each): the
  A-side v(s,z+1,z+1) is Theorem A's A_z in closed form; the
  H-side full collapse stays a per-slice observation.
Total 679 rows, 0 mismatches.

## 6. Consequences and predictions

- The kits' "even/odd supply form" tallies (3/3, 4/4, 2/2 ...) are
  finite observations of Theorem A's parity split; the z18 kit's
  failed naive "+2-shift, 1v0" prediction failed because it
  ignored the split (k=18 is even).
- All future tail precomputations are fixed a priori; e.g. the
  z=25 census (if the parallel lane takes it) will measure
  sixteenth tail k=25: hold {0} U {12..25}, then UNIFORM (0,1) for
  all s >= 26 (no cutoff); its precalc pair k=26: hold [0..25],
  (0,2) at s=26, uniform (2,1) beyond. k=25..32 tables are in the
  frozen output section (f).
- Below-band enumerations for future slices only need the H-side
  check; the supply side is closed-form.
- Strip-spot and base-spot collapse values for future censuses are
  closed-form (K1332's z>=11 base-spot statements remain a special
  case).

## 7. Honest record

- Prior-work search (2026-11-25): repo-wide code search for
  "supply identity" in research/knowledge/ returns only
  K1328/K1330, both of which record the identities as declaration-
  internal finite precomputations or census observations; no
  knowledge item contains the universal family characterization.
  The K1325 lemma BB' (z17 partner) and the z18/z19 declaration
  notes prove finite-domain versions inside their declarations.
- Derivation-first ordering: the Theorem A / Lemma S hand
  derivations (K0832 branch arithmetic) preceded every machine
  call in this session; the machine cross-checks defend the
  transcription, not the proof.
- K numbering incident: the work was drafted under K1333; at the
  mandatory immediate pre-push refetch of main, a parallel lane
  (PG(2,9) cap Grundy, commit `3ce3dda5`, 19:39:44Z, repair
  `8c5fa531`) turned out to have claimed K1333 for unrelated
  content minutes after this session's availability checks (code
  search 0 hits, list_commits clean, path probe clean — index
  lag again). The item was renumbered K1334 (provisional; the
  repo already carries a K1330 double-numbering). Content-level
  duplication check: no parallel publication touches the
  supply-identity family; the renumbering was purely numerical.
  Lesson (2nd instance after K1331): minute-scale numbering races
  with parallel lanes are routine; only the immediate pre-push
  latest-main refetch catches them.
- The earlier-slice (z15/z16-era) kit identity rows were not
  re-parsed in this run; they were computed by the same
  closed-form function covered by the exhaustive k=1..140 grid
  check.
- No wall-clock, randomness or hash-seed dependence anywhere in
  the frozen output; all counts are field-level and disclosed.
- This kit's engine bytes are the same pinned chain engine as all
  census kits (bd5f22e4...); the verification is same-engine-class
  cross-referencing, not third-party hardware verification.
- Fetch-back verification (post-push, same procedure as the crossrun
  addendum 659658ac): the six published files of commit `a80477fc`
  (item, log, kit README / verify_k1334.py / verify_k1334.out /
  engine_block.py) were re-fetched from main at that sha and compared
  byte-for-byte against the local payloads: 6/6 byte-identical PASS
  (10752/8508/4652/19311/36176/2540 bytes). Head of main at
  verification time remained `a80477fc` (no overtaking commit).

## 8. Handoff

- z>=23 census lane: the tail-identity predeclaration constants
  are determined a priori by Theorem A (kit section (f)); the
  strip-spot / base-spot collapse sides likewise (Lemma S);
  the H-side absorption/full-collapse checks remain the census's
  own work.
- T-Z20 / T-Z21 declaration lanes: unchanged needs (the absorption
  side); the base-spot K1332 description now comes with the whole
  family context (Lemma S).
- Integration pass: K1332/K1334 numbering reconciliation as usual.

## 9. Standard caveats

Everything in this kit and log is pure closed-form derivation from
the published K0832 universal closed form plus finite machine
cross-checks against the pinned raw engine and the published frozen
kits; no verdict of any game position is consumed. Standard 11x11
empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes
1/2/4, and all central-reply roots: all UNKNOWN, unchanged.
