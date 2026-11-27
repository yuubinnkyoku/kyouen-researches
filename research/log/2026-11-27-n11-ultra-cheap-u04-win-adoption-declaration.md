# Declaration: n11 ultra-cheap u04 WIN-row canonical adoption (2026-11-27)

- Part: single-row canonical adoption of the u04 WIN row into the head
  of record.  Single-owner Part, publish-then-execute.
- Adopted row: u04 `1152921505747697664:1032` (class 23101, legal 85,
  s5 index 745184) **WIN(1) nodes 9,149,084 @15M**.
- Sources of record: replica escalation kit
  `n11-ultra-cheap-u04-escalation-15m-20261127` (commit `24c5b85f`,
  15M cold pair byte-identical), C++ scrutiny gate kit
  `n11-ultra-cheap-u04-win-cppgate-20261127` (commit `378ec332`,
  GATE-PASS `85,15000000,1,9149084` with anchors 3/3 and tamper
  4/4 fail-closed), third-impl corroboration kit
  `n11-ultra-cheap-u04-thirdimpl-20261127` (commit `2691ac04`,
  CORROBORATION-PASS WIN(1) expansions 10,728,035 x2 identical).
  Three-implementation verdict-level agreement; the two-pillar
  requirement is complete.
- Base head of record: `merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache`
  sha256 `c5082866c1bb61e9cbcb86b80b29c3b2a141b4b5e93a0b8d4b46e04151b631c8`,
  6,893 rows WIN 211 / LOSS 6,682; u04 verified fresh/absent.
- Pre-registered merged shape: **6,894 rows WIN 212 / LOSS 6,682**.
- Maker gates (fail-closed): G0 pins (merger `90711961...`, policy
  `78655e94...`, quarantine `81d23160...`, BASE, gate
  source+headers) + published-kit MANIFEST self-verification
  (escalation + cppgate + thirdimpl kits); G1 LIVE re-run of the
  published gate_runner.sh on a scratch kit copy (2 fresh-cold C++
  passes, node-exact vs the published raws; gate binary rebuilt in
  this environment from the pinned source, provenance disclosed);
  G2 three-pillar re-parse (replica pair, C++ gate pair, third_impl
  pair); G3 freshness + duplicates + WIN/LOSS conflict review; G4
  quarantine-free + canonical-safe; G5 increment build; G6 merger x3
  byte-identical + shape check.  Maker x2 byte-identical.
- Follow-up Part (declared): the WIN-side flip-census/reaudit of the
  u04 owner-class union (serving class 23101 completion must be
  Board-verified free_now at adoption time), u01/u02/u03 precedent.
- 11x11 UNKNOWN.  Status guard: adoption bookkeeping only, NO verdict
  consumed, the adopted row is NOT a class closure and NOT a root
  verdict, transfers nothing; nodes are bookkeeping.
