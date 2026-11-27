# n11 ultra-cheap u02 WIN-row canonical adoption (new head of record)

Adoption kit of the single-owner declaration
`research/log/2026-11-27-n11-ultra-cheap-u02-adoption-declaration.md`
(commit `6522b9b6`).  Consumes exactly 1 row into the canonical head of
record:

- u02 `1297036830121656320:131074` (class 2251, legal 80, s5 index
  93815), WIN(1) nodes 3,167,121 at the 15M budget.

## Result: MAKER-PASS (2 runs, all outputs byte-identical)

- **New head of record:
  `merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache`**
  (sha256 `82b525777843ecb44c3857b034f7a135284c2587b42dbaa94aa295b01adc7509`,
  288,677 bytes, **6,892 rows WIN 210 / LOSS 6,682**), exactly the
  pre-registered shape 6,891+1 / 209+1 / 6,682+0.
- Increment `increment-ultra-cheap-u02-adoption-20261127.cache`
  (sha256 `ef727442a84ba507d8be767ca05ce818a3ea7af3b699f67fea9aabc678f43712`,
  1 WIN row).
- Merger: standing `s5_union_merge.py` (`90711961...`), 3 runs
  byte-identical (`merge-audit-run1..3.json`); maker executed twice,
  all outputs byte-identical between runs.

## Maker gates (all PASS, fail-closed)

- G0 pin shas: merger `90711961...`, policy `78655e94...`, quarantine
  `81d23160...`, BASE `0ec4080d...` (6,891 rows WIN 209 / LOSS 6,682),
  gate source `9193f5b6...` + headers `5976935d...`/`2e36d694...`;
  published kit MANIFEST self-verification (26 files across the
  escalation and pillars kits, byte-fetched from main).
- G1 LIVE re-run of the published `gate_runner.sh` on a scratch copy of
  the pillars kit: `u02 GATE-PASS 80,15000000,1,3167121` (2 fresh-cold
  C++ passes, node-exact vs the published raws; binary built from the
  sha-pinned source with zig 0.13.0 `-std=c++20 -O3`, glibc-version
  warning disclosed in the pillars kit).
- G2 re-parse of the three pillars: replica 15M cold pair
  (byte-identical), C++ gate pair (node-exact), third_impl pair
  (result 1, legal 80 = 80, clean, expansions 3,595,562 identical).
- G3 freshness: u02 absent from BASE; no duplicate adopted keys; no
  WIN/LOSS conflict vs BASE.
- G4 quarantine-free and canonical-safe per `s5_evidence_policy`.
- G5/G6 increment build + merge x3 byte-identical + shape check
  (6,892 rows WIN 210 / LOSS 6,682).

## Meaning and non-meaning

Adoption bookkeeping only.  The adopted row is cache bookkeeping, NOT a
class closure, NOT a root verdict, and transfers nothing.  The
WIN-side flip-census review of the u02 row's owner-class union (class
2251 completion would be Board-verified free_now at adoption time) is a
SEPARATE follow-up Part per the standing pattern (u01 precedent:
`n11-ultra-cheap-u01-adoption-reaudit-20261127`).  Nodes are
bookkeeping, never evidence.  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.

## Files

- adoption-manifest.json - machine manifest (schema
  n11-ultra-cheap-u02-win-adoption-manifest-v1).
- scripts/make_adoption.py - the fresh maker (structural descendant of
  the published u01 adoption maker).
- output/increment-ultra-cheap-u02-adoption-20261127.cache - the 1-row
  increment.
- output/merged/merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache
  - the new head of record.
- output/merged/merge-audit-run1..3.json - merger audits (byte-equal).
- MANIFEST-sha256.txt - sha256 of every file in this kit.

## Honest disclosures

- The maker's kitbuild fetch of the two published kits initially missed
  their own MANIFEST files (excluded from their self-lists); the first
  maker run fail-closed on exactly that (G0 "missing MANIFEST") and the
  MANIFESTs were fetched before the passing runs.  No output was
  written by the failed run.
- The gate binary emits a zig glibc-version warning (host 2.41 vs
  provided 2.39); all rows ran to replay_done.
