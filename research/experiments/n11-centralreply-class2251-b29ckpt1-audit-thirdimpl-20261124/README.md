# Part CV: batch-29 (class 2251) ckpt-1/3 rows — pinned-replica + third-implementation fail-closed audit (2026-11-24)

- Pre-registered declaration: `research/log/2026-11-24-part-cv-b29ckpt1-audit-declaration.md`
- Scope: the 16 published batch-29 ckpt-1/3 rows `ab001..ab016` (all honest label LOSS, result=2, budget 15M, 2-pass fresh-cold, class 2251).
- This Part audits computational reproducibility and three-implementation verdict agreement only. It consumes no verdicts, writes no cache, and makes no win/loss claim.

## What is here

| dir | contents |
| --- | --- |
| `input/` | 21 runner inputs (rows.json + 16 targets, anchors k02a/l1a, negatives ng1/ng2) |
| `sources/` | published evidence pins: raw 2x16, anchor-third-published 4, negative-third-published 2, batch-keys-b29.json, pins-b29ckpt1.json, read-only canonical cache `854800f3...` (6,301 rows), status-ckpt13.log |
| `scripts/` | audit_cu.py, third_impl.js, jsreplay.js, runbatch.sh, run_thirdimpl.sh, run_valgate_cu.sh, make_rows_cu.py, tamper_battery_cu.sh |
| `output/` | replica raw 32, third-impl targets 32, anchors 4, negatives 2, status.log, audit-run1/2/3.txt, audit-summary.json + run variants (4), tamper-battery.txt + tamper-battery-buggy-grep-record.txt |
| `val-gate/` | 12 hosted gates (4 gate keys x {cu-host.out, input.csv, published-baseline.out}) |

## Headline results

- **D3 pinned-replica**: 16/16 node-exact vs published, per-pass total 57,463,971 nodes; p1 == p2 on every field except wall_s; quads 95,670.
- **D4 third implementation** (`third_impl.js`): 32/32 target runs clean (a/b deterministic pair per key); `third = replica = 2` verdict agreement 16/16 (three-implementation corroboration); anchors reproduced exactly (k02a: result=1, expansions 9,106,337 / ttHits 4,991,527; l1a: result=2, 7,660,602 / 3,951,175; a/b pairs equal); both negatives fail-closed with the exact expected `GATE_FAIL` wording. Target totals: 66,057,589 expansions (first observation).
- **D5 fail-closed audit** (`audit_cu.py`): 3 executions, rc=0, stdout byte-identical across runs (md5 `34b4f4c0ddde156cb456809239f1f434`), **ALL 352 GATES PASS**, LOSS agreement 16/16, inconclusive=0; canonical cache `854800f3...` (6,301 rows) untouched and the 16 audited keys absent from it (G6, verdict-non-consumption machine guarantee).
- **D6 tamper battery**: 7/7 pre-registered corruptions detected with rc=1 at exactly the pre-registered gate (T1 replica-ab002-det-pair, T2 third-ab005-det-pair, T3 third-ab009-verdict-agree, T4 replica-ab012-done, T5/T6 pin-all-73, T7 anchor-l1a-a-expansions) + control rc=0.
- **D2 val-gate**: hosted gate runners match published baselines (12 files; at2m-...-912 cu-host.out is byte-identical to its published baseline, a legitimate exact match).

## Honest deviations (recorded per protocol)

1. `scripts/tamper_battery_cu.sh` first run used `grep -o` (BRE), so the wrapper treated `+` literally and failed to extract the first failed gate; fixed to `grep -oE` (one line). The buggy run is preserved verbatim in `output/tamper-battery-buggy-grep-record.txt`. The audit tool itself detected all tamper variants in both runs.
2. B1 push: `ab016.p2.out` had a one-digit key_lo transcription error; detected by fetch-back blob comparison and corrected by an immediate follow-up push (final fetch-back 75/75 files matched).
3. B2 push: `audit-run{1,2,3}.txt` were initially published with transcription corruption (11 spurious line-wraps, one merged PASS-line pair around the at2m-B node-exact/first-15m-present gates, a missing trailing newline, and one quote substitution on the `neg-ng2-failclosed` line). Corrected repush verified byte-exact: sha256 `8fc03804...f125e`, git-blob `62d7ad69b82981b8317ba45e74973885061ce61e` x3, 353 lines, 22,753 bytes.
4. A B1-fix commit message contained one stray non-ASCII token (typo). Commit messages are immutable; the typo has no content impact and is recorded here.
5. D7 was published as four commits (B1 outputs, B2 audit-run logs, B3 audit summaries, B4 tamper records + corrected script) instead of one, due to per-commit payload size. (The declaration's B-commit file list is fully covered by B1+fix, B2+fix, B3, B4.)

## Verification

`MANIFEST-sha256.txt` lists all 163 published data files (sha256, bytes, git-blob-sha1). Every entry was cross-checked against the GitHub tree on main (size and git-blob-sha1) on 2026-11-24 after the B2-fix commit: 163/163 match. `README.md` and `MANIFEST-sha256.txt` itself are excluded from the listing (self-exclusion).

## UNKNOWN guarantee (unchanged)

The standard 11x11 empty board, the 19 central-reply roots, the two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1/2/4, class 10968, class 23964, class 2251 (all 54 keys, including the 16 audited keys and their LOSS rows), class 34269, and every other key remain **UNKNOWN at all times**. Node counts, expansion counts, ttHit counts, and wall-second counts are never read as win/loss. The 16 LOSS row verdicts are not consumed by this Part (honest label = adoption candidate only; adoption belongs to a separately declared adoption Part). Third-implementation agreement is not adoption. No closure, coverage, secured, or root-outcome claims are made.
