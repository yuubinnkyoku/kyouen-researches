# Verification log: u04 adoption head of record beecb024 - independent third-party check

Read-only independent verification (no runs, no adoption, disjoint
from every declared Part) of the new head of record published by the
u04 WIN-row canonical adoption (commits `ed1aab54`/`04b8c23a`,
kit `research/experiments/n11-ultra-cheap-u04-win-adoption-20261127`).

## Checks (all fresh from main raw CDN, sha256-gated)

- `merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache`:
  sha256
  `beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544`
  (matches the published head-of-record pin) - byte-verified.
- Shape: 6,894 data rows (1 header comment line), verdict field
  counts WIN(result=1) 212 / LOSS(result=2) 6,682 - matches the
  pre-registered adoption manifest shape exactly.
- Increment audit vs the u03 head `c5082866...` (fetched and
  sha256-verified from the u03 adoption kit): set difference =
  EXACTLY ONE added row
  `s5verdict,1152921505747697664,1032,5,1,9149084` (the adopted u04
  WIN row), 0 removed rows, 0 changed rows, 0 duplicate keys.
- WIN/LOSS conflict audit: no key carries two different verdicts.
- The adopted row is fresh (absent from the BASE head), nodes
  9,149,084 matches the escalation raw / C++ gate / third-impl
  consensus (bookkeeping only).

Verdict: the published u04 adoption head is internally consistent
and is exactly the single-row pre-registered increment over the u03
head.  This check consumed no verdict and adopts nothing.

## Standing UNKNOWN notice

Adoption bookkeeping only; NO verdict consumed.  The standard 11x11
empty board, the two-stone root {60,27} and its remaining third
moves 100/108 stay UNKNOWN.  The u04 adoption flip-census reaudit
Part (declaration `34b3c559`) remains owned by its declaring lane.
