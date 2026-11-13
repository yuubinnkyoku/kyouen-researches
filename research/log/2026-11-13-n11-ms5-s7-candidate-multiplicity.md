# 2026-11-13 n11 S2 {59,60}: S7 reuse candidate multiplicity audit

Evidence: deterministic recount of the **published candidate CSVs**, not independent regeneration, WIN/LOSS certification, or a proof of candidate completeness.

Baseline main at start: `460d9097a32ff793658f5c9785086e1e4e80a646`. Read `AGENTS.md`, `research/knowledge/README.md`, K0023, and the milestone-5 S7 reuse experiment README. The generator `ms5_s7_reuse_analysis.ts` is still a comment-only stub; the classification and completeness limitations in the experiment README remain.

Input: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_candidates_part{1,2,3}.csv` from main. Parse CSV rows (skip the header where present), group by `s6_hex`, and count `cat=1` and `cat=2` separately. No geometry or solver assumptions are used in this recount.

Recount: 8,763 rows; 8,763 distinct `s7_hex` keys; 6,276 distinct `s6_hex` parents. Category counts: cat1 396, cat2 8,367. The parent multiplicity distribution is:

| cat1 known-LOSS candidates | cat2 possible-win-pool candidates | S6 parents |
|---:|---:|---:|
| 0 | 1 | 3,749 |
| 0 | 2 | 2,039 |
| 0 | 3 | 114 |
| 1 | 0 | 181 |
| 1 | 1 | 144 |
| 1 | 2 | 27 |
| 2 | 0 | 22 |

Checks: parent total 6,276; weighted row total 8,763. Thus 6,073 parents have at least one cat2 candidate, and **203 parents have only cat1 candidates**. Among parents with cat2 candidates, 3,749 have exactly one cat2 candidate, 2,183 have two, and 141 have three. No parent has more than three total candidates in this published set.

Scheduling implication: the 3,749 single-cat2 parents are a natural first intersection target against the external certified win-child key pool, because each positive hit immediately establishes a reusable LOSS-child witness for the corresponding parent (subject to the oracle and certificate trust boundary). This is a prioritization heuristic, not a proof of greater expected hit rate. The 203 cat1-only parents cannot be closed as WIN by this particular candidate list alone.

**No new verdict**. Cat2 means potential match only, not WIN7; the published generator remains unreproducible. Standard 11×11 empty root and S2 {59,60} remain **UNKNOWN**.
