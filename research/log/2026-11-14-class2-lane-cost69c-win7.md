# class2-lane cost-69c sweep + WIN7 certificate (2026-11-14)

Long-term n11 lane, session 7. Continued from cost-69b (13th sterile child).

## Sweep

S6 child `00000000000000809082040000000000` (S5 parent `00000000000000809082000000000000`, edge cost 69, demand c1=2 c2=1 c4=0), 69 candidates:

- **1 WIN7-D10** (bit 103, 13,442,759 nodes) + 68 REFUTED-D10, 0 capped
- Total: 440,238,688 nodes across batches A-I, each batch with pilot d6 control (5949 nodes), 9 controls total
- Heaviest bits: 110 (23,731,323), 68 (22,139,194), 29 (14,367,154)
- Determinism rerun: bits 110/68/29 + WIN7 bit 103 all node-exact vs primary batches
- All 69 candidates terminal stone range [13,17]
- Candidate count cross-checked by independent legal_candidates.py enumeration (69)

Raw batches: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69c-raw-batch{A..I}-20261114.jsonl` + determinism rerun. Sweep record: `class2-lane-cost69c-sweep-20261114.json`.

## WIN7 certificate bit 103

- Root `00000080000000809082040000000000` (7 stones) - new root, previously absent from the repo (code search total_count=0)
- Root check: loser mobility 53 = independent legal_candidates.py enumeration 53
- Blind extraction (cert_driver69c.ts, kill table empty): 52,338 rows, 20,357,850 nodes, fbt_drops=0, fatal=null
- Full verification (verify_bit7_win7_cert.ts): **53/53 sub-roots PASS**, union 0/0, terminal range [13,17]

## Transport

1.89 MB certificate pushed as xz+base64 in 3 parts (76,983/76,983/76,919 bytes) under `research/experiments/n11/output/class2-lane-cost69c-certificates/`. Remote verification at commit fb71dbff: concatenation + decode reproduces md5 `4bb1299324fb69634a848cebc109961c` byte-identical to the locally verified certificate.

Operational note: the previous session's part1of3 push actually landed truncated (29,794/76,983 bytes) at a wrong path; it was deleted and re-pushed complete and verified this session.

## Status

11x11 empty board, two-stone roots, S2 {59,60}, class 2, class 4: **all UNKNOWN**. The WIN7 certificate proves only that this specific 7-stone root is a WIN for the first player within depth 10; the sterile/refuted child results do not determine the outcome of any larger root.

Next cheapest unswept child per after-cost69a ranking: `00000000000000809082000000000001` and `00000000000000809082080000000000` (cost-70 band) were swept sterile by a parallel lane this same day; frontier recompute pending with 69c receipt added.
