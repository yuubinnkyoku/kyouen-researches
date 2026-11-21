# Five-row q=4: band 41..44 witnesses (census over K1209 width-40 witness re-placements)

Date: 2026-11-21
Status: EXPERIMENT (finite exhaustive census + independent verification). Institutional claims scoped as stated.
Claim update: **M_{5,4} ∈ [45, 567]** (previous [41, 567] from K1209; here lower bound improved from 41 to 45).
Upper bound T_5 = 567 unchanged. m = 45 witness existence: **UNDETERMINED** (not claimed either way).
Standard 11×11 status: unchanged, UNKNOWN. mwq_stabilization.csv: not modified.

## Motivation

K1209 (five-row q=4 surgery, width-40 → 41) concluded R(S) = 40 for all 16 published
width-40 witness stone sets and that none of them extends to width 41. This experiment
re-examined that closure claim by re-placing the same 16 stone sets under the full
D4 image group (id/H/V/HV) and all translations, then evaluating first-uncovered reach R
with the fail-closed engine+criterion+node triple. Result: the closure statement in the
K1209 README is inconsistent with K1209's own published raw output, and the translation
census alone pushes the five-row lower bound from 41 to 45.

## Erratum recorded against K1209 (README claim, not primary data)

K1209's own published raw file `output/criterion-m40-witnesses.txt` (five-row exp,
pins in that exp's sha256s.txt) records for its second record (labeled "witness 2",
0-based W[1], the maxx=37 set): `free_append_reach = 42`, `first_unblocked = [42, 1]`,
`witness_widths = [38, 42]`, i.e. width-41 and width-42 witnesses were already present
in K1209's own published raw output.
This contradicts the K1209 README sentence "R(S)=40 for all 16 sets ... none extends
to width 41". The K1209 value claim M_{5,4} ∈ [41, 567] itself remains valid (no material
conflict: 41 was witnessed regardless). Per AGENTS.md convention, K1209 primary files
are not modified; this note is the erratum record on the fast lane side.

## Setup

- Seeds: the 16 published K1209 distinct width-40 witness stone sets (five-row w=5, q=4).
- Configs: `configs/cfg-census-m40seeds.json` (16 seeds, scan 64, 2 fail-closed calib gates),
  `configs/cfg-census-R44seeds.json` (the 4 R=44 stone sets, scan 80).
- Engine v2 census ("det4"): for each seed, each D4 image (id/H/V/HV), and each horizontal
  shift s in 0..scan-1, place the image and compute R = column of the first strip cell
  (coordinate convention as in K0853/K1211) not covered by stone-or-block, with
  maximality/safety verified. A placement at large shift may have stones beyond column R;
  such stones only matter on wider boards, so the placement's witness width range is
  maxx+1 ≤ m ≤ R (same convention as `append_criterion.py`'s witness_widths). Fail-closed:
  any placement outside the calib expectations aborts the run.
- Calib gates (fail-closed, both matched): m40_1 id s15 → R=42, firstUncovered [42,1];
  m40_3 id s15 → R=40, firstUncovered [40,1] (both equal the K1209 published values,
  including the 42-reach already present in K1209 raw output).

## Census results

`output/census-5row-m40seeds.json`: 2476 placements (16 seeds × 4 images × shifts).
R distribution: R=41: 18, R=42: 6, R=43: 6, R=44: 4 placements with R ≥ 41 (34 total;
the remaining 2442 placements have R ∈ {0..40} dominated by R=0: 1570).

Per-placement witness width ranges (integer board widths m with maxx+1 ≤ m ≤ R):

- R=41: 18 placements (e.g. m40_1 H s2 → [25,41]; m40_3 V/id s16 → [41,41]).
- R=42: 6 placements (m40_1 H/HV s3 → [26,42]; m40_3 V/id s17 → [42,42]).
- R=43: 6 placements (m40_1 H/HV s4 → [27,43]; m40_3 V/id s18 → [43,43]).
- R=44: 4 placements, all seed m40_3:
  - H s0 and HV s0 → witness_widths **[25, 44]** (20 consecutive widths from a single
    stone set+image: staircase), firstUncovered [44,1].
  - V s19 and id s19 → witness_widths [44, 44].

Width coverage on board 5×m: every width m ∈ {41, 42, 43, 44} has at least one placement
with maxx+1 ≤ m ≤ R (counts among the 34: width 41: 28, 42: 12, 43: 8, 44: 4). Hence
safe+maximal covering witness configurations exist for 5×41, 5×42, 5×43, 5×44: the
(5,4) def-mode witness band now includes m = 41..44, so **M_{5,4} ∈ [45, 567]** (lower
bound = width 44 witnessed; upper bound T_5 = 567 = B_max(5)+1 from the K1207
demand-supply inequality, unchanged).

Structure note (single-set staircase record): the m40_3-family set at shift 0 (H/HV
image, maxx = 24) witnesses twenty consecutive widths 25..44 on its own, replacing the
K1209 record of nine consecutive widths (32..40, maxx=31 set) as the widest single-set
staircase recorded for (5,4).

`output/census-R44seeds.json`: cascade census over the 4 R=44 placements as seeds
(m40_3 H s0 / HV s0 / V s19 / id s19, scan 80, 896 placements) reproduces a clean
shift-generated staircase: at effective left-offset k ∈ {0..19} the family reaches
R = 25 + k with saturation (8 placements per intermediate value, 16 at R=44 — each
of the four seed sets in each of its D4 images at exactly one shift — all images
included), and beyond that
coverage collapses to R ∈ {0,1}; each board width m ∈ [25, 44] is witnessed by these
stone sets at exactly one offset band. The max R over the whole scan-80 window is 44,
and no placement with R ≥ 45 appears anywhere in the scanned windows (scan 64 for the
seed census, scan 80 for the cascade census; max R over all 2476 + 896 placements is 44).

## Verification (three independent systems)

1. Engine v2 `verifymany` (`output/verify-engine.json`): all 52 bank items ok.
2. Node BigInt/Bareiss `verify_node.mjs` (`output/verify-node.json`): all 52 items ok,
   same tags in same order.
3. Published Fraction criterion `append_criterion.py` (K1209 original, byte-identical,
   sha256 d08d8fb1…): re-ran on all 34 R≥41 placements; first_unblocked agrees with the
   census engine on 34/34 (`output/criterion-5row-R41plus.txt`).

Verification bank `output/bank-5row-m41plus.json`: 52 items = for each of the 34 placements
every width m with max(41, maxx+1) ≤ m ≤ R (widths 41/42/43/44 with counts 28/12/8/4).
An earlier bank version used the range 41..R without the maxx+1 floor; the engine's
fail-closed assert caught out-of-board stones and the bank was corrected before any
verification was accepted. Tamper control (`output/verify-tamper.json`): one stone shifted
by +1 in x → ok=false, uncoveredCount=2 (both engine and node).

Determinism: census outputs regenerated twice, byte-identical (sha256 in digests.txt both
runs equal).

## Scoping / honest limitations

- Result type: FINITE EXHAUSTIVE CENSUS (16 published stone sets × D4 × translations,
  not all configurations) + INDEPENDENT VERIFICATION. The claim is existence of witnesses
  for widths 41..44 (lower bound), not a proof that width 45 has none.
- m = 45 (M_{5,4} = 45) remains UNDETERMINED. The census shows no R ≥ 45 placement within
  the searched family; that is a bounded-family negative observation only.
- 11×11 roots, S2, class 1/2/4 items: untouched, UNKNOWN.
- Scripts here are byte-identical copies of the published versions (engine v2 from the
  six-row q=4 experiment K1211 with configs set w=5; append_criterion.py and surgery
  curve engine conventions from K1209). No new engine code was introduced for the census.

## Files

- `scripts/engine_v2.py`, `scripts/append_criterion.py`, `scripts/verify_node.mjs` —
  published, byte-identical (sha256 in digests.txt).
- `configs/` — census configs (seeds inline), calib gates.
- `output/` — censuses, criterion agreement record, verification bank, tamper control.
- `digests.txt` — sha256 of every file in this directory.
