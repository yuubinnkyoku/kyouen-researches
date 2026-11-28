# 2026-11-28 n11 thirteenth k01+k02 adoption reaudit (flip-census/refresh) declaration

Single-owner declaration (publish-then-execute) for the WIN-side
flip-census/reaudit Part of the thirteenth class-16757 k01+k02
canonical adoption, declared as follow-up in the adoption completion
log (35a00c2e); this lane is the declared owner of this Part.

## Pre-registered plan and predictions

- SCENARIO cache (measured head of record):
  `merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`
  sha256 `d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec`
  (6,896 rows WIN 214 / LOSS 6,682), adopted at commits
  35a00c2e + c1aa0eee (kit n11-thirteenth-ladder-top-k01k02-adoption-20261128).
- BASE for the census comparison: beecb024 (6,894 rows WIN 212 /
  LOSS 6,682, ultra-cheap u04 head of record).
- The refresh is a byte-clone of the published ultra-cheap u04
  adoption-reaudit refresh (u04 reaudit kit template) differing in
  EXACTLY three regions (docstring, CACHE path, expected cache sha);
  every computation byte identical.  Three sequential runs must be
  byte-identical (fail-closed otherwise).
- Pre-registered census prediction (from the owner-union precheck kit
  n11-thirteenth-owner-union-precheck-20261128, fdb704d7): owner-union
  classes [16612, 16740, 16757, 30542]; expected refresh census
  unknown 34,376 -> 34,372, excluded_now 144 -> 148, free_now 39 -> 39;
  serving class 16757 departs the closure ladder (rank-1/unknown_now=2
  at BASE beecb024).  Caveat: u03-style pre-exclusion may reduce the
  observed flip set; the measurement decides.
- Dependency pins (all pre-verified sha256 on this host): frozen
  dependency graph 54f9c364..., update8 repaired-joint-plan
  b658290a..., independent.py 954d3a10..., s5_evidence_policy
  78655e94..., quarantine 81d23160...
- Disjointness: no solver search, no new verdicts, no root verdict
  consumed; read-only planning/audit computation over the adopted
  cache.  The standard 11x11 empty board and every one of the 19
  central-reply roots stay UNKNOWN unless and until the required S5
  children are all exact LOSS.

No branch, no PR; results go to main directly per repo policy.
