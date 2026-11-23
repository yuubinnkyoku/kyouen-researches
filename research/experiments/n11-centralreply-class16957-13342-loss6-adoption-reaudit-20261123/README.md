# n11 central-reply closure batch-24 (class 16957) + batch-27 (class 13342) joint 6-LOSS canonical adoption re-audit (Part BZ, 2026-11-23)

Part BZ (declaration in research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md,
commits 8b7111be + typo-fix b37117d9): fail-closed canonical adoption of the 6 resolved
LOSS rows of batch-24 (class 16957, keys y002/y004) and batch-27 (class 13342, keys
o001/o003/o005/o007) into the Part BU canonical cache via the pinned byte-copy
fail-closed union merger (scripts/s5_union_merge.py, sha256 907119610034...).

Adopted rows are 2-pass node-exact result 2 at budget 15M (pinned jsreplay replica),
re-derived from the published batch kits (83 + 92 files, all sha256-verified against
the published MANIFEST-sha256.txt of each kit). The batch WIN rows y001/y006 (batch-24)
and o002 (batch-27) are honest labels, NOT adopted (verdict unconsumed; scrutiny owner
C++ second-implementation gate pin 9193f5b6... remains the only WIN adoption route).
fragment o009 (batch-27) is bookkeeping only, UNPROBED, not adopted. batch fileless
keys (49 + 48) are UNPROBED and untouched.

## Pipeline (all deterministic, every step byte-reproduced this host)

1. scripts/make_increments_b24b27.py: kit integrity (83+92 files, per-file sha),
   2-way p1/p2 node-exact + '# replay_done' completeness, status.log each-once
   (budget,result,nodes) agreement, WIN sets == unadopted, WIN-HALT pair pins,
   row-audit winhalt schema agreement, batch-keys legal/(lo,hi) agreement,
   adopted pass node sums (batch-24 850,035; batch-27 13,967,778), zero BASE overlap,
   quarantine 0. Output: output/increment-b24b27-loss6-20261123.cache (6 rows)
   + output/increments-manifest.json. x4 byte-stable.
2. scripts/s5_union_merge.py (byte-copy, pin 90711961..., selftest PASS): union merge
   BASE (Part BU canonical 6,287-row cache, sha e32a2e44...) + increment with the
   WIN/LOSS conflict gate. x3 byte-identical; merge-audit-run1/2/3.json identical.
   Output: the 6,293-row scenario cache (WIN 158 / LOSS 6,135).
3. reaudit/scripts/refresh_adoption_b24b27.py: full 19-root refresh (per-root
   coverage, closure-classes, probe-worklist, frozen update8 plan) against the
   scenario cache. x3 byte-identical + isolated run (env -i, PYTHONHASHSEED=random,
   cwd=/tmp) byte-identical. Outputs: reaudit/output/{refresh-summary.json,
   closure-classes.csv, per-root-coverage.csv} (+ regenerated probe-worklist.csv,
   worklist not published by design).
4. scripts/compare_deltas_b24b27_adoption.py: fail-closed deltas BASE -> scenario
   (15 sha pins + manifest semantic gates; increments-manifest row_counts adopted
   6 / WIN 3 / fragment 1 / fileless 97). x4 + isolated byte-identical.
   Output: output/decomp-deltas-b24b27-adoption.json:
   class 16957 unknown_now 53->51 (rank 22->10), class 13342 54->50 (rank 26->6),
   flips=[], new_free=[], free_now 38->38, update8 resolved +0, joint greedy
   38,301->38,295, probe-worklist 64,754->64,747, closure churn left=[] entered=[],
   individual greedy movers roots {5,16,24,48}, per-root free/uncovered unchanged.

Tamper battery (scratch tree /tmp/tb/kr = different absolute path): 16/16 detected +
restore byte-verification, including a 3-level pin bypass probe (status tamper + kit
MANIFEST rebuild + script pin constants updated; caught by the semantic
"WIN set [] != unadopted ['o002']" gate) and a merger same-key verdict conflict
(GATE FAILED, no output written). Control: full chain re-run on the scratch tree
reproduced every published sha byte-exactly.

## UNKNOWN guarantee

The standard 11x11 empty board, the 19 central-reply roots, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, class 16957 and class 13342 (all keys)
remain UNKNOWN at every point of this Part. Node counts are bookkeeping, never
verdicts. This Part makes no root-coverage/closure/secured/root-outcome claim:
closure churn left=[]/entered=[] is only the machine record that the class set is
unchanged; joint greedy 38,295 and worklist 64,747 are bookkeeping, not outcomes.
