# n11 class-2634 base control: cross-host reproduction of the Part M canonical re-audit (2026-11-22)

Before building the batch-8 (class 2634) `h045` IF-ADOPTED decomposition
(`../n11-central-reply-class2634-win-h045-ifadopted-20261122/`), the pinned
Part M refresh script was re-run twice in a fresh takeover-host environment to
establish a byte-reproducible BASE for all scenario deltas.

- script: `scripts/refresh_19root_frontier.py`, sha256
  `0bc10a05039945d937ccfaaed8230761a0b175306820750e97abbf2ce01348f9`
  (byte-fetched from the published Part M re-audit experiment at
  `../n11-central-reply-10324-closure-reaudit-20261122/`, sha-verified);
  the only pin-relevant environment difference is the local filesystem path
  of the merged cache, whose sha256 was gate-checked
- pinned inputs (unchanged sha256): dependency graph `54f9c364...`
  (`../n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz`),
  update8 plan `b658290a...`, Board source `954d3a10...`, s5 evidence policy
  `78655e94...`, quarantine registry `81d23160...`, merged chain cache
  `a998f4c0b13383cb50bbbdb60761182722ba45280fd585739ad5d08bc182ed1b`
  (5,975 rows, the published canonical re-audit cache)
- both runs (`output/run1.log`, `output/run2.log`) are byte-identical, and the
  three published outputs of the Part M experiment reproduce byte-exactly on
  this host (cross-host determinism):
  `output/refresh-summary.json` sha256
  `d934043524c86638f5a9d9e1ba27c5afe70155dfd84641b991acc448d85a2019`,
  `output/closure-classes.csv` sha256
  `1404234cd3f95281b16768146e26ead2b5a889330593ca376e97e7fa69f5e03f`,
  `output/per-root-coverage.csv` sha256
  `819ae368617143c51316feffc2545aab73aad206a513f95f6dac8a50d91e0be2`
  (all three byte-equal to the published ones at
  `../n11-central-reply-10324-closure-reaudit-20261122/output/`)
- the fourth output, `probe-worklist.csv`, is NOT published here or in the
  Part M experiment (3.77 MB; long-standing lane convention). Local
  reproduction sha256
  `ca3ee3bc7772ff38462cb60fc41ab4570cb236a880213322de230410fa550e80`,
  byte-identical between run1 and run2.
- measured BASE (matches the published summary): excluded 390 /
  excluded_now 23 / free_now 34 (board verification 34/34, rejected 0) /
  unknown classes 34,502; update8 remaining 31,836 of baseline 31,859,
  resolved 23, win-hit groups 0; joint greedy union 35,857 over 2,132 unique
  groups; probe worklist total 65,155; baseline root {X,60,27} 119/119 free
  thirds.

This control publishes the reproduction evidence; the canonical BASE
remains the published Part M outputs. Read-only planning computation; no
verdict is consumed; the standard 11x11 empty board and all 19
central-reply roots stay UNKNOWN.
