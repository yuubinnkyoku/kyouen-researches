# class2-lane cost-75 session: child sweep, 19 WIN7 certificates, frontier closure of the cost-75 S5

Date: 2026-11-14 (class2 long lane)

## What was done

1. Cost-75 S6 child sweep (`output/class2-lane-cost75-sweep-20261114.json`): all 75 legal 7-stone children of S6 `00000000000000801a02040000000000` under the repo v15 runner (close-first AND d>=8, cap 100M, depth 10 single-shot). Result: **19 WIN7-D10 + 56 REFUTED, 0 capped, 233,689,814 nodes**. WIN7 bits: 0,4,14,17,20,21,22,31,32,34,50,54,72,76,79,90,92,108,118. The sweep was completed once before an execution-environment reset wiped the local workspace; the post-reset rerun reproduced the WIN7 bit set, the total node count, and the five heaviest candidates node-exactly (118/31/77/88/32) — recorded as a cross-run reproduction like the cost-64 precedent.

2. Certificates for all 19 WIN7 roots (`output/class2-lane-cost75-win7-certificates-20261114.json`, `output/class2-lane-cost75-certificates/n11_s7_<root>.cert`): 866,595 rows, extraction via `extractor_exact` (FBS 1<<20, probe 96, drop-counter; built to avoid the fbt-cache saturation silent-drop bug documented in `2026-11-14-fbt-saturation-silent-drop.md`) with `fbt_drops == 0` and `fatal == null` asserted for every root; independent Bareiss-det4 verification PASS for every root (root-check stones=7, all sub-roots, union 0/0, terminal range [13,17]). All 19 remote certificate files verified md5-identical after push.

3. Frontier recompute (`scripts/recompute_frontier_cost75.py`, `output/class2-lane-cost75-frontier-recompute-20261114.json`): full manifest-level recomputation with staged controls reproduced exactly (baseline 638/7208/565500 through after-cost58 814/7032/552811/5256/413283). Cost-75 addition: 112 covers, 89 marginal, 17 in-manifest. **After cost-75: solved 831, unique remaining 7016, sum cost 551,482, open 5240/411,954; the cost-75 target S5 `00000000000000801a02000000000000` is fully closed (absent from the remaining ranking — all S6 children covered by WIN7 receipts).** Best class-2 target is now S5 `00000000000000809082000000000000` (33 orbits / 2245 remaining, next cheapest child cost 61); best class-4 target S5 `00000000020000003800000080000000` (24 orbits / 1934).

## Operational notes

- During the session a set of stale background certificate workers survived an environment restart and raced the relaunched workers on the same output files (bits 21/31/54/118); all racing processes were killed and those bits were re-extracted cleanly from scratch. Every one of the 19 certificates in the record comes from a verified-complete run (union 0/0, drops 0) — the record contains only post-cleanup artifacts.
- Push transport: `cat`-based file transfer into `push_files` is safe only for short-line files (certificates); for JSON records use line-paged `read_file`. A mid-token newline corruption of the cost-75 sweep record JSON by the cat route was caught by remote-vs-local comparison and fixed in a follow-up commit (`b242ec93`).

11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN; WIN7-D10 certificates prove wins only from their individual 7-stone roots.
