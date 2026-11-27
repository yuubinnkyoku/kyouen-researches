# 2026-11-27 Part SY wave-C independent re-audit (third host)

## Context

Part SY wave C landed (commit 6148e568: 42/42 third-impl verdict-level
agreements, 84 cold-pair raws; owner audit rev2 722175e7 x4 byte-identical
AUDIT-PASS). The wave-B cross-check lane's pre-landing review had predicted
its audit_sy.py G1 would fail-closed on the three calibration raws' missing
rc=0 trailers; the owner lane resolved this by republishing the wave-C
calibration raws with rc=0 lines (values identical, disclosed in the run
record) before running the audit. The pending resume item was therefore
cleared, and this lane ran the official-outputs verification.

## What this lane did (no target pass executed; verification only)

1. Wave-B cross-check kit integrity on a third host: all 229 MANIFEST
   files re-fetched from published main, sha256 229/229; published
   crosscheck_sy.py re-run: CROSSCHECK-PASS rc=0, failures=0.
2. Published audit_sy.py (rev2, 722175e7) re-run twice on the official
   wave-C outputs: rc=0 rc=0, sha256 5ce0151f byte-equal to the owner's
   published audit_sy.run1..run4.
3. Fresh independent re-audit (scripts/fresh_reaudit_sy_wavec.py):
   84 raws, fresh parser, kit pins vs cross-check clones, calibration
   values, per-pass expected_result, cold pairs (result/expansions/ttHits),
   41 LOSS + k05 WIN, exactly 84 files, expansion bill 529,416,996, and a
   three-pillar verdict consistency check (third-impl vs replica-derived
   vs C++ gate expected quads for all 42 targets incl. SX k05
   90,50000000,1,15763505): PASS, 2 runs byte-identical (11e93d9b).
4. Tamper battery (scratch copies, deleted after): 5/5 fail-closed
   (T1 k05 expected flip / T2 k10.p2 expansion edit / T3 phantom k99 /
   T4 k01.p1 result flip / T5 k07.p2 rc-trailer removal) + clean control
   rc=0. An earlier clean-control rc=1 was a restore-method artifact
   (phantom file left by a non-pruning copytree), re-run with fresh
   copies rc=0; disclosed.

## Honest disclosures

- The author had read the first 40 lines (docstring) of the published
  audit_sy.py before writing the fresh verifier; its parser, gates and
  derivation are fresh. The two implementations agree on everything.
- Verdict-level bookkeeping only; NO verdict consumed, no cache increment,
  no class-status change. Standard 11x11 empty board, 19 central-reply
  roots, two-stone root {60,27}, third moves {100,108}, S2 and all closure
  classes remain UNKNOWN; expansions/nodes are bookkeeping.
- With the third pillar corroborated on three hosts (owner lane + wave-B
  second host + this lane) and the C++/replica pillars gate-verified, the
  42-row seventh-cost batch (41 LOSS + k05 WIN) is adoption-eligible.
  Adoption requires a separately declared adoption Part against the
  canonical head of record 42dbb58f (6,832 rows WIN 201 / LOSS 6,631)
  with a fresh declaration and the parent batch's WIN/LOSS conflict
  review; nothing here consumes any verdict.
