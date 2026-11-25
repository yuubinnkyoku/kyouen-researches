# supply-identity family closed-form verification kit (2026-11-25)

Machine cross-check kit for the provisional knowledge item K1334
(**tail supply-identity family, complete closed-form characterization**
+ **Lemma S strip-line closed form**). Both statements are derived
ENGINE-FREE from the published K0832 single-token closed form; the
paper derivation was completed BEFORE the machine run (the K1320/
K1321/K1325 hand-calculation-first ordering). The machine checks the
hand algebra and the closed-form transcription against the raw
engines; it is not a proof substitute.

## Statements being checked

Theorem A (k >= 1, s >= 0), A_k(s)=v(s,k+1,k+1), B_k(s)=v(s,k,k+1):
A = s%2 on [0..k], then constant 0 (k odd) / 2 (k even);
B = s%2 on [0..k-1], B_k(k) = 1 (k odd) / 2 (k even), B = 1 for
all s >= k+1; the identity holds exactly on [0..k] (k odd) /
[0..k-1] (k even); the break is uniform in s with NO upper cutoff.

Lemma S (z >= 1, m >= 0, S >= max(z+1, m+2)):
v(S, z, m+z+1) = (m+1) mod 2.

## Files

- `verify_k1334.py` (sha256 `d0c751a2279a62942d6d632e48466ed81eea93aa3e7592a05a5cacd6b4347f7a`)
  — the verifier, with the pinned engine block embedded (startup
  gate: sha256 == `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`).
- `verify_k1334.out` (sha256 `63f7730f740d1d3f75ebd9b5225c2955520b4d591f0de6b64166b0bd4e474e5f`)
  — frozen stdout of the run; determinism SIX runs byte-identical
  (default x2, PYTHONHASHSEED=1 same cwd, env -i same cwd, env -i
  isolated directory, post-rename re-run), rc 0 each, ~0.2 s each.
- `engine_block.py` (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`)
  — the published chain engine standalone, same bytes as the K1282..K1332 chain.
- `README.md` — this file.

## Inputs (published kit frozen outputs, re-verified at runtime)

The cross-artifact section (e) reads, by relative path, the five
published census kit frozen outputs and asserts their sha256 pins at
runtime:

- `../strip-z18-min13-20261125/explore_z18f13.out` pin `c4e7757c587883bb41b0f297de336128cd6bafc55865ba10673b28c7338d0b0b`
- `../strip-z19-min14-20261125/explore_z19f14.out` — no separately
  published pin; observed and recorded `3354dfc6c7f65dedc02aeb95fa257e8a19526e1a5a25fd45e040b287d9dd510f`
- `../strip-z20-min15-20261125/explore_z20f15.out` pin `09e9026a436bf25aed05eabaf3629975971bd320a4c4c5ce5da122239f19f789`
- `../strip-z21-min16-20261125/explore_z21f16.out` pin `10f94100eb6240a807a32ac5d0e91f532800f86320a64d40e3ae47891dd2f643`
- `../strip-z22-min17-20261125/explore_z22f17.out` pin `f16a87d447d61b631cca153665b4a577d844ab5fe96eb9f740a74e400c82c7ac`

## Sections (frozen output)

- (a) engine_gate: pin PASS.
- (b) lemmaA_grid: Theorem A vs the closed form over
  k in {1..140} x s in {0..300}: 42,140 rows, mismatches 0
  (witness rows k in {17..26}, s in {0..40} recorded).
- (c) lemmaS_grid: exhaustive small grid (z,m in {0..20},
  S in {1..90}): inside-conditions 31,850 rows, mismatches 0;
  outside-conditions 5,950 rows with 2,915 formula failures
  (the two sum conditions are necessary; no claim outside);
  wide boundary grid (z,m in {0..120}): 72,600 rows,
  mismatches 0.
- (d) k0832_revalidate: closed form vs the RAW canonical engine,
  x in {1..30} x z in {0..24} x R in {1..60}: 45,000 rows,
  mismatches 0; ordered-engine subset
  x in {1..15} x z in {0..12} x R in {1..30}: 5,850 rows,
  mismatches 0.
- (e) cross_artifact: every identity row (hold and break), strip
  spot and base spot of the five published kits parsed and compared
  value-for-value against the theorem: 679 rows total
  (614 identity rows over 13 sections with k = 17..24, 60 strip
  spots, 5 base spots), mismatches 0; strip-spot collapse values
  recomputed from the closed form: 60/60; input sha pins 4/4
  asserted + 1 recorded.
- (f) future_predictions_k25_32: the full a-priori constants for
  k = 25..32 (e.g. sixteenth tail k=25: hold [0..25], uniform
  (0,1) from s=26; k=26: (0,2) at 26 then uniform (2,1)).

## Honest caveats

Everything here is a pure function of the pinned engine bytes and of
the published K0832 closed form; the only universal statements are
the two K0832-derived results (Theorem A, Lemma S), whose proofs are
hand case analyses recorded in the K1334 item. The H-engine side of
the published observations (below-band full collapse, spot
absorption) remains per-slice observation and is not claimed. No
K slot is claimed by the machine; the item claims the slot. No
verdict of any game position is consumed. Standard 11x11 empty
board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4,
and all central-reply roots: all UNKNOWN, unchanged.
