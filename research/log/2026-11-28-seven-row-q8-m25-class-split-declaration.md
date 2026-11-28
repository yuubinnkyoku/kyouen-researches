# 2026-11-28 seven-row q8 7x25 SAT-side class {3} krow/minpos decomposition — single-owner declaration (publish-then-execute)

- Task: resolve the (7,8) frontier width 7x25 in the SAT direction by the
  krow/minpos class-split decomposition of the single-deficiency central
  class {3} (deficient row = {3}, krow=3:6, minpos P=0..12 sound H-split,
  floor((m-1)/2)=12), mirroring the successful six-row-q7-m22-class-split-20261127
  pattern. Class {0}/{1}/{2} single-deficiency and multi-deficiency classes may
  be probed with the same machinery within the session budget; each is a
  separate disclosed extension, not part of the primary target.
- Outcome semantics: SAT => new deficient-maximal witness, M_{7,8} >= 26
  (current published range [25,651], witness family m=8..24 single-deficiency
  48 stones [7,7,7,6,7,7,7]-type, K0825/K0826/seven-row-q5-q8-sat-frontier-20261115).
  UNSAT/INDET => honest negatives per piece only, no absence claim (71 canonical
  deficiency classes at w=7; a class-krow-minpos UNSAT excludes only that piece).
- WIN-stop rule: on the first SAT in the primary class {3} sweep, stop and
  publish; further classes are not swept this session.
- Pre-declaration calibration (disclosed here, ran before this commit):
  7x24 q8 class {3} krow=6 kissat 4.0.4 SAT 869,797 conflicts, decoded 48 stones
  rows [7,7,7,6,7,7,7], dual-verified sat.js verifyConfig + fresh Fraction
  verify_frac.py (safe + maximal) — reproduces the published m=24 witness class.
- Machinery: sat3.js/sat2.js/sat.js/verify_frac.py byte-clones of the published
  six-row-q7-m22-class-split-20261127 kit (sha256 sat fcc0cfd8..., sat2
  14ceb854..., sat3 e04581eb..., verify_frac 837fe24b... — verified against the
  local fetch), kissat 4.0.4 official linux-amd64 binary sha256 21da5d98...
  (same pin as the published kits), caps <= 272s per piece under the sandbox
  wall-clock budget.
- Declaration-time HEAD: 4505b70a358bd3f1eed0baff8d01a76963c96b38.
- Non-claims: no 11x11 root / two-stone root {60,27} / third move {100,108} /
  S2 / closure-class verdict is created, consumed, or transferred by anything
  here; all such values remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 7x25 (7,8) class-split lane
  for this session; any parallel execution of the same cells should treat
  this lane as owned and defer.
