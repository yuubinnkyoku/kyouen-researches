# (5,4) band 45/46 surgery: witnesses to m=45 and m=46, M_{5,4} ∈ [47, 567]

Date: 2026-11-21 (single session, UTC). Lane: five-row fixed-width, q=4, w=5 (K1209 → K1212 → this experiment).

## Claims

- **Band update: M_{5,4} ∈ [47, 567]** (lower bound 45 → 47).
  - m=45: 17 witness species found (34 records / 14 stones each, D4-canonical rows type [3,2,3,3,3]).
  - m=46: **4 species reach R=46** (criterion + census, all 16 placements re-verified by engine and node): w45-05, w45-11, w45-16 in their id/shift-0 form (criterion witness_widths to 46), and w45-13 via mirrored placements (H/HV shift 16, V/id shift 4).
  - Upper bound 567 unchanged (K1212).
- **Staircase records**: w45-00/w45-01 (maxx=25) are witnesses at 20 consecutive widths 26..45 (previous (5,4) record: 9 widths). w45-16 is a witness at widths 30..46 (17 consecutive).
- **m=47 UNDETERMINED** (scoped negative, not an absence claim): all 16 R=46 placements were run under surgery budget 2 (1R1A/2R1A/2R2A full joint enumeration) and budget 3 (+3R1A/3R2A), all negative.

## Method: SurgeryJoint-3 (`scripts/surgery45.py`)

This session diagnosed and closed an **incompleteness in the published engine** (`engine_v2.py`, unchanged here):

- The engine's 2-addition-level prefilter enumerates blocker candidates as "one surviving stone + two added stones". **Joint triples of three surviving stones** (same blocking shape as K1213 case-c, which blocks appended plays) are not enumerated by the prefilter class.
- Positive control: the K1209 m39→m40 transition. Engine alone reproduces only 14/16 placements; SurgeryJoint reproduces **16/16 completely** (all 4 D4 images, byte-identical across 2 runs; `output/control45-m39-m40-joint.json`, ALL_EQUAL).
- SurgeryJoint-3 keeps `engine_v2.py` unmodified (subclass) and runs exact joint pools restricted to surviving stones for budget-2 (~5 s/placement) and budget-3 (~33 s/placement) surgery.
- Speed internals: integer Cramer circle coefficients + isqrt root solving; 5,000-curve cross-check against engine cell logic with assertion (0 mismatches; a duplicate-curve disc=0 bug was caught by the pre-xcheck). A degenerate-curve infinite loop (removed-stone coordinate ∈ U) was diagnosed and skipped via `s==u or s==y`.
- Scope: joint mode completes the 2-/3-addition prefilter classes; higher budgets and other move classes are not claimed.

## Two-stage lineage

1. **Hunt (m=45)**: the published m40-seeds census (`configs/census-5row-m40seeds.json`, byte-copy from the 41plus pin) provides seeds. SurgeryJoint budget 2, `--minR 41 --mtarget 45`: all 34 placements with R≥41 swept; 10 placements yielded hits; 34 witness records → **17 D4-canonical species** (`w45-00`..`w45-16`, `output/main45-budget2.jsonl`, `output/bank-45plus.json`).
2. **Census (width extension)**: the 17 species become seeds of a fresh census (scan 60, `configs/cfg-census-45w.json` → `output/census-45w.json`, 1792 placements). Calibration anchors: w45-05 id0 → R=46, first uncovered [46,1]; w45-00 id0 → R=45, first uncovered [45,1].

`output/census-45w.json` R histogram (top): R=45: 64 placements, **R=46: 16 placements** (4 each from the w45-05, w45-11, w45-13, w45-16 families), **no R=47 within scan 60**. This is what fixes the m=46 witnesses and seeds the m=47 negative searches. The full census output (1,010,451 bytes) is byte-pinned in `digests.txt` and deterministically regenerable from the published engine + config; the repo carries `output/census-45w-extract.json` (calibration, full histogram, all 16 R=46 placements with stones).

## The 17 witness species (`output/bank-45plus.json`, criteria in `output/criterion-45.txt`)

| tag | maxx | witness_widths | R | note |
|-------|------|----------------|---|-------|
| w45-00 | 25 | 26..45 (20 consecutive) | 45 | staircase record |
| w45-01 | 25 | 26..45 (20) | 45 | staircase record |
| w45-02 | 37 | 38..45 | 45 | |
| w45-03 | 39 | 40..45 | 45 | |
| w45-04 | 40 | 41..45 | 45 | |
| w45-05 | 41 | 42..46 | 46 | m=46 witness |
| w45-06 | 42 | 43..45 | 45 | |
| w45-07 | 30 | 31..45 | 45 | |
| w45-08 | 37 | 38..45 | 45 | |
| w45-09 | 39 | 40..45 | 45 | |
| w45-10 | 40 | 41..45 | 45 | |
| w45-11 | 41 | 42..46 | 46 | m=46 witness |
| w45-12 | 33 | 34..45 | 45 | |
| w45-13 | 28 | 29..45 | 45 | family also reaches R=46 via census translation (shift 4/16) |
| w45-14 | 28 | 29..45 | 45 | |
| w45-15 | 33 | 34..45 | 45 | |
| w45-16 | 29 | 30..46 (17 consecutive) | 46 | m=46 witness, staircase |

All 17 species: n=14 stones, rows [3,2,3,3,3], min_row=2, maxcirc=3, maxline=3, safe=true, old_uncovered_count=0.

## Verification battery

- **Three independent systems**:
  1. `engine_v2.py` deterministic q=4 cell check — `output/verify-engine-45.json` (17/17 species at m=45, ok+safe+maximal), `output/verify-engine-46.json` (w45-05/11 at m=46), `output/verify-engine-46-R46census.json` (all 16 census R=46 placements at m=46, 16/16)
  2. `append_criterion.py` exact Fraction arithmetic — `output/criterion-45.txt`, `output/bank-45plus.json` (witness_widths for every species)
  3. `verify_node.mjs` BigInt + Bareiss determinant — `output/verify-node-45.json` (17/17), `output/verify-node-46.json` (w45-05/11), `output/verify-node-46-R46census.json` (16/16)
  - So every m=45 witness species and every m=46 witness claim (direct, translated, staircase) is checked by at least 3 mutually independent implementations.
- **Tamper negatives**: a perturbed variant (w45-00 with its last stone shifted) fails in all checked systems — `output/bank-tamper.json`, `output/verify-tamper.txt` (engine log), `output/verify-tamper-node.json`.
- **Determinism**: every major output re-run with byte-identical results (sha256 records in `digests.txt`).
- **Staircase re-check**: w45-00/w45-01 at widths 26..45 and w45-16 at widths 30..46 re-verified per width on 2026-11-21 (`output/staircase-45.txt`).
- **Reproduced published inputs**: census m40seeds/R44seeds and control m40 surgery outputs byte-match the published five-row-q4-band-41plus experiment (pin 59b1251aa736), so this experiment extends an identical baseline.

## Negative records (scoped)

- **m=47, budget 2**: the 16 census R=46 placements (families w45-05, w45-11, w45-13, w45-16; 4 D4/shift images each), ~5 s per placement, all negative — `output/main47-from46-budget2.jsonl` (16 lines).
- **m=47, budget 3**: same 16 placements, ~33 s each, all negative — `output/main47-from46-budget3.jsonl` (16 lines). (The first 12-placement runs before the w45-16 family was discovered are superseded; kept in the local kit only, see `digests.txt` note.)
- These are **not** absence claims: only surgery up to budget 3 over these 16 placements was excluded. m=47 remains UNDETERMINED.
- main45 hunt swept all 34 R≥41 placements (R=44:4, R=43:6, R=42:6, R=41:18 of the m40-seeds census), budget 2 — `output/main45-budget2.jsonl`: 10 placements yielded 34 witness records (all class 2R2A) → 17 species.

## Honesty record

- No absence claims anywhere; census/surgery negatives are scope-stated.
- Published set: everything needed to re-run and check the results; byte-copy reproductions of already-published 41plus/K1209 files and superseded intermediate runs are not duplicated (pinned in `digests.txt`, note appended there).
- `mwq_stabilization.csv` untouched (K1201/K1209/K1212 precedent).
- The standard 11×11 (5,4) value remains UNKNOWN; this experiment concerns fixed-width boards only.
- witness_widths entries in `criterion-45.txt` are verified endpoints, not exhaustive width scans except where consecutive runs are stated.

## Reproduction

All commands from this directory ([x] = command whose output byte-matched a rerun during the session).

```
# positive control: K1209 m39->m40, 4 D4 images, 16/16 set-equality  [x]
python3 scripts/surgery45.py control configs/s5x39q4.json configs/surgery-control-m39.json output/control45-m39-m40-joint.json

# census, scan 60, calibrates on w45-05 (R=46) and w45-00 (R=45)  [x]
python3 scripts/engine_v2.py census configs/cfg-census-45w.json > output/census-45w.json

# main hunt, m=45, budget 2, all m40-seed placements with R>=41 (34 swept)  [x]
# (census-5row-m40seeds.json = the byte-identical file published at
#  research/experiments/five-row-q4-band-41plus-20261121/output/census-5row-m40seeds.json)
python3 scripts/surgery45.py main configs/census-5row-m40seeds.json output/main45-budget2.jsonl --minR 41 --budget 2 --mtarget 45

# m=47 negative searches over all 16 R=46 placements  [x]
python3 scripts/surgery45.py main output/census-45w.json output/main47-from46-budget2.jsonl --minR 46 --budget 2 --mtarget 47
python3 scripts/surgery45.py main output/census-45w.json output/main47-from46-budget3.jsonl --minR 46 --budget 3 --mtarget 47
```

Pins: `digests.txt` (all output sha256, script sha256, published-input sha256). Inputs `surgery-main-m40.json` / `surgery-control-m39.json` (published pin 73058a4b..., byte-match) and `s5x39q4.json` are byte-copies of the published K1209 experiment (`research/experiments/five-row-q4-witness-band-40plus-20261121/`); the m40-seeds census that seeds the hunt is the byte-identical file published as `research/experiments/five-row-q4-band-41plus-20261121/output/census-5row-m40seeds.json` (sha 789c09a2...); the reproduced census copies and the superseded first-12 m=47 runs are pinned in `digests.txt` and kept in the local kit, not duplicated here.

## Files

- `scripts/`: engine_v2.py (published, unmodified), append_criterion.py (published), verify_node.mjs (published), verify_frac.py (published, unused this session), surgery45.py (new: control/main modes, joint pool, --mtarget/--minR/--budget/--limit/--only/--resume).
- `configs/`: published byte-copies (cfg-census-m40seeds/cfg-census-R44seeds, s5x39q4 seed, K1209 control expectations surgery-control-m39.json) + cfg-census-45w.json (census config with calib anchors). K1209 main surgery output (surgery-main-m40.json) and the two byte-copy censuses are pinned in digests.txt but not duplicated.
- `output/`: census-45w-extract.json (from the byte-pinned full census), control, hunt jsonl (append-resume format, per-placement records with witnessesByClass), witness banks, verify batteries, tamper checks, m47 negatives.
