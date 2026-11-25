# Session log: n11 sixth-cost third-implementation verdict re-verification (2026-11-21, continuation)

Continuation of the third-implementation lane declared in
`research/log/2026-11-21-n11-sixthcost-third-implementation-verdict-reverification-single-owner-note.md`.
Scope, gates and A1-A5 multipliers of that note are unchanged; this entry records
execution.

## Executed this session

1. **Bug hunt -> root cause found and fixed.** The bugged third implementation
   matched the replica on every LOSS row but flipped all 158 WIN rows to LOSS.
   Comparative child enumeration + rule-table sweeps isolated the cause: a single
   global kid-scratch set (`KID_IMG/KID_M/KID_CB/KID_CNT`) was overwritten by each
   child's own enumeration, corrupting pending siblings' canonical keys/TT keys.
   LOSS verdicts fire early (one bad child, often before the first deep recursion
   returns); WIN proofs must visit every child, so only WIN proofs were destroyed.
   Fix: per-depth (stones-indexed) kid pools; plus replica-parity child dedup,
   TT-status-priority ordering, and a passed-down legal mask with a per-node
   `--verify-legal` cross-check. No rules/value-semantics change.
2. **Fixed implementation reproduces every anchor row**, including k02
   `1297036692683751424:68157440` -> WIN (9,106,337 expansions, deterministic x4
   runs), the parked pair (LOSS `1297036830122704896:67108864`; WIN
   `10376294091217440768:33554432`), and the four legacy two-target rows
   (3 WIN + 1 LOSS). All agree with the pinned replica at 15M and the corpus.
   Bank sample vs probe-13 cache: 16 rows, 14 agree, 0 disagree, 2 wall-inconclusive.
3. **Rule-engine equality re-proven**: forbidden-quad count 95,670 == replica;
   195,044 random triples: TBL == wob with 0 mismatches; --verify-legal runs
   node-clean. Negative input gates fail closed as designed.
4. **Environment reset incident (recorded honestly).** Mid-session the sandbox
   wiped the work tree, including the just-fixed script and raw stdout captures.
   The script was rebuilt from the documented design and re-validated (identical
   expansion counts on all witness rows vs the pre-reset runs), then immediately
   canonically archived to the lane kit. Lesson applied: canonical artifacts go to
   persistent storage before or together with runs, not after.

## Status after this session

- k02's WIN verdict is now independently corroborated verdict-level by a
  non-df-pn minimax implementation (in addition to the pinned df-pn replica and the
  original corpus entry). The C++ second-implementation gate remains the
  pre-registered adoption gate; the owner decides. **No corpus verdict was
  consumed, and 11x11 empty-board is still UNKNOWN.**
- Bank full-band recalibration (140+ rows) and the stretch-37 sweep are deferred
  to follow-up runs of this lane (per-row 30-120s at current JS speeds).

## Artifacts pushed this session

- `research/experiments/n11-sixthcost-third-implementation-verdict-reverification-20261121/`
  (README, third_impl.js, verify_tbl.js, run_bank.py, MANIFEST.sha256,
  out/witness/*, out/bank-fixed-A/*)
- this log entry.

Publication used the GitHub App push path (repo was private to unauthenticated
fetches and `get_file_contents` stayed unstable, as already recorded in the owner
report; `list_commits` was used for pre-push main verification; MANIFEST.sha256 pins
published bytes pending a later byte-exact fetch-back).