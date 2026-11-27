# 2026-11-27 n11 Part SZ: seventh-cost 42-row canonical adoption completed

Part SZ (n11-seventhcost-sz-adoption-20261127) is complete.  The
canonical S5 head of record advanced from
merged-exact-s5-chain-plus-sixthlossk38-20261126.cache (sha256
42dbb58f..., 6,832 rows WIN 201 / LOSS 6,631) to
merged-exact-s5-chain-plus-seventhcost42-20261127.cache (sha256
5b6e77f7..., 6,874 rows WIN 202 / LOSS 6,672) by adopting exactly the
42 published seventh-cost rows (41 LOSS + the single k05 WIN
1152921504607932416:536870912).

## Waves (publish-then-execute)

- Wave A (declaration, commit e9d3b53e):
  research/log/2026-11-27-n11-seventhcost-sz-adoption-declaration.md.
  Pre-registered: 42 rows, WIN 201+1 / LOSS 6,631+41, merged head
  sha256 pinned by construction, three byte-identical merger runs.
- Wave B (kit, commit 80a0a3ab): experiment kit published with the
  fresh SZ maker (sha256 9620d91e...), the 42-row increment
  (sha256 959ae2dd..., 3,389 bytes), the adoption manifest
  (sha256 14ef4fc2...) and the kit README (sha256 3d72ea45...).
- Wave C (merged head, commit d00eed39): the new canonical head
  (sha256 5b6e77f7..., 287,763 bytes) plus the three byte-identical
  merger audit records (each sha256 94b04cef...).

## Verification summary (all re-run live on this host)

- SZ maker: two runs byte-identical; G0-G7 fail-closed gates all
  PASS (anchor byte gates on base head / merger 90711961 /
  quarantine 81d23160 / policy 78655e94 / frozen graph 54f9c364;
  SW 145/145 + SX 24/24 + SY 143/143 MANIFEST-verified; live audits
  audit_gate.py PASS x2 and audit_sy.py AUDIT-PASS targets=42
  raws=84; 42 pins re-derived against SW/SX gate-rows expected
  quadruples and SY replica_expected_quad; freshness 42, WIN-LOSS
  conflict 0, duplicate 0, quarantined 0, noncanonical 0).
- Merger s5_union_merge.py (pinned sha256 90711961...) run three
  times: three byte-identical outputs, MERGED unique=6874
  dup_elided=0 WIN=202 LOSS=6672, exactly the pre-registered shape.
- Independent pre-adoption verification of the 42 pins: SW
  gate-rows 41/41, SX k05, SY replica quad agreement; replica node
  total 227,552,924 (bookkeeping, never verdicts).

## Meaning and non-meaning

Admission of published, triple-pillar corroborated S5 raw verdicts
into the canonical solver-trusted cache chain only.  NO root
verdict consumed, no class freed, no class excluded.  The standard
11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27}, its remaining third moves {100,108}, S2 and all closure
classes remain UNKNOWN.

## Frozen pins

- base head: 42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4
- merged head: 5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2
- increment: 959ae2dd249a1d78be1f67f68640a4371fa13ca2e4b31d3b39bb44cb05519f1f
- adoption manifest: 14ef4fc23cf6649b47fb67a9f544626ec3a4637d08c5e2b236e7906cbe0b9f82
- maker: 9620d91e23d39e796581ca786cef135769e1db9f4dcb800bea767b8425f554e0
- merger: 907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a
- quarantine registry: 81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9
- evidence policy: 78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2
- frozen dependency graph: 54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b
- merge audits (x3): 94b04cefac9060a2897e3a3d7bf86fe1a3f6e97dc668bd13c715aca1271fa049
- pillar manifests: SW 09a8bca0..., SX 68f91473..., SY 366771ff...
- declaration commit: e9d3b53e2f4cf52468934fc5ff8cdee96acc0075
- wave B commit: 80a0a3abb1f0824b05e1be4d0a27e876b1ad6142
- wave C commit: d00eed39437e067a5271f698862eccf81883724b

## Next (declared follow-ups)

- Wave E (pre-registered in the declaration): BASE vs SCEN census
  measurement via the SV/ST-procedure clone measurer, and the
  reaudit refresh of the new canonical head.
