# 2026-11-17 n11 class2-lane: cost71e certificates complete — all thirteen WIN7-D10 roots extracted, independently verified and published

## Summary

Following the cost71e sweep (fresh v17 71-bit depth-10 sweep, 13 WIN7-D10
bits [3,4,8,41,54,58,76,79,94,96,100,116,119] + 58 REFUTED-D10, 0 capped,
commit `54c94390`, claim v2), all thirteen WIN7 certificates were extracted
and verified:

* extraction: blind extraction with `class4_child1_cert_extractor_exact.ts`
  (repo-verbatim, engine v15 inlined, FBS=1<<20) via the archived
  `cert_driver71e.ts` (empty kill table), fbt_drops=0 on all thirteen, no
  fatal, no capped per-move
* total certificate rows 534,804; total extraction nodes 141,067,035;
  published bytes 19,300,105 (bits 41/79/58 whole files, the other ten
  split part1of2/part2of2 at line boundaries with a README-split per bit)
* independent verification with `verify_bit7_win7_cert.ts` (engine-free,
  Bareiss 4x4), orchestrated per root by `verify_cost71e_one.sh`:
  root-check stones=7 on every root, loser mobility equals the independent
  legal_candidates.py enumeration on the RAW root
  (bit41:51, bit79:48, bit58:48, bit3:54, bit4:64, bit8:56, bit54:56,
  bit76:54, bit94:57, bit96:59, bit100:55, bit116:65, bit119:62), all
  sub-roots PASS (subroots_pass == loser mobility on every root), terminal
  stone range [13,17] everywhere, consumed-winner-state union vs the
  certificate row set 0 missing / 0 extra in both directions on every root
* determinism: fresh-process re-extraction byte-identical (md5) on bit 41
  within the first environment. A mid-run execution-environment reset then
  destroyed the first full extract+verify pass's local files after
  verification but before publication; the full re-extraction in the fresh
  environment reproduced all five recorded pre-reset md5s (bits 41/3/4/8/54)
  byte-identically and re-verified all thirteen certificates (unplanned
  cross-environment determinism check; the same reset-failure pattern was
  previously hit and recorded by the 69j certificate lane)
* all 23 certificate files (3 whole + 20 parts) landed byte-exact on the
  raw CDN at commit pins `128b4703`..`0216de11`; every split recombination
  was re-checked with cat + md5sum against the manifest md5s

Coordinate convention carried over from the 66i lesson: loser defenses and
the certificate root use the RAW child|bit position. For bits
3/4/8/41/54/58/79 raw==canon; for bits 76/94/96/100/116/119 the raw root
is a non-canonical D4 image (d4_canon_root recorded per manifest entry)
and the defense list is enumerated on the raw root; the verifier's
root-header check guards this.

Driver repair recorded with this lane: the published `cert_driver69j.ts`
carried a push-transport-mangled literal newline split (`split('\n')`
became `split('\\n')`) that crashed with a NaN BigInt on use.
`cert_driver71e.ts` repairs this to `String.fromCharCode(10)`, the same
convention as the extractor's own 2026-11-14 fs-import repair note. The
archived driver here is argv-driven and reads the defense list on stdin.

Erratum carried from claim v2 (unchanged): the claim v1 legal_candidates
field was a cost78a template carry-over (78 bits, wrong child); the
recomputed 71-bit list is in claim v2 (git blob
`3299f80fd42079a4a956afb606df513b1e7bb869`); candidate_count (71),
engine_candidate_bits, transfers and every executed bit were correct and
the published stdlib raw audit recomputes legal_candidates itself and
passed all checks.

## Interpretation guard

WIN7-D10 certificates prove a first-player win within depth 10 from the
individual 7-stone roots of this child only. REFUTED-D10 is not a LOSS
proof. No manifest row of the head-1472 family is closed by publication.
The receipt fold of this row waits behind the pending cost-76c, cost-66i,
cost-66j and cost-69j folds (managed by their own lanes).

**The 11x11 empty board remains UNKNOWN. The two-stone roots {49,60}
and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.**

## Files pushed (this commit)

* `output/class2-lane-cost71e-certificates/README-split-bit{b}.md` — ten
  split recombination notes (bits 3/4/8/54/76/94/96/100/116/119)
* `output/class2-lane-cost71e-certificates/bit{b}-rootcheck.json` and
  `bit{b}-subroots.jsonl` — per-bit verification records (13 bits)
* `output/class2-lane-cost71e-certificates/class2-lane-cost71e-win7-certificates-20261117.json`
  — certificate manifest (v1 schema, thirteen entries with
  md5/sha256/rows/extraction_nodes/loser_mobility/d4_canon_root/split)
* `output/class2-lane-cost71e-inflight-20261117.json` — claim v3,
  certificates-complete (updater asserts the v2 git blob)
* `scripts/update_claim71e_v3_20261117.py`, `scripts/cert_driver71e.ts`,
  `scripts/verify_cost71e_one.sh`, `scripts/ev71e.sh` — archived lane
  tooling
* `research/log/2026-11-17-n11-class2-lane-cost71e-certificates-complete.md`
  — this log
