# n11 tenth-cost k01/k02 third-impl corroboration

Third-implementation corroboration pillar for the two resolved
tenth-cost batch rows (declared in
research/log/2026-11-27-n11-tenthcost-k01k02-thirdimpl-declaration.md,
commit 55d4a33a; replica raws published in kit
n11-tenthcost-batch-stage1-2m-20261127, commits b8049d8b / 3485348c).

## Result: CORROBORATION-PASS (verdict-level, both keys)

- k01 `1297036692683751424:131074` (legal 86): third_impl reported
  **result 2 (LOSS)** in both fresh cold passes, expansions 7,886,706
  mutually identical (ttHits 4,350,324, quads 95670, ttOverwrites
  3,692,866, memoPower 22, legal derived 86 = declared 86, reason
  clean, node_rc 0). Replica had reported LOSS(2) nodes 6,783,438.
- k02 `1297036692683751424:131136` (legal 84): third_impl reported
  **result 1 (WIN)** in both fresh cold passes, expansions 10,287,104
  mutually identical (ttHits 5,687,157, quads 95670, ttOverwrites
  6,092,800, memoPower 22, legal derived 84 = declared 84, reason
  clean, node_rc 0). Replica had reported WIN(1) nodes 8,799,140.
- Parameters: cap 400,000,000, wallcap 260, memo-power 22, exactly as
  declared (no 15M passes; the ninth-cost k12 precedent showed the 15M
  cap ends runlimit:cap INDET).
- Verdict-level agreement in both directions. Expansions and nodes are
  bookkeeping and are not expected to match across implementations.

## Honest disclosures

- The wall_s field differs per pass (24.55/23.36 and 29.65/29.52);
  timing is not evidence. All other fields are byte-identical within
  each key's pair (machine-gated before publication).
- Exactly 2 passes per key were executed on this host; no discarded
  passes.
- This is one of the two pillars required before any adoption of
  these rows. The C++ second-implementation scrutiny gate (expected
  quadruples 86,15000000,2,6783438 / 84,15000000,1,8799140, gate
  source 9193f5b6 @154f3b7a) remains pending. A WIN-side flip-census
  review at adoption follows the ninth-cost precedent.
- The verdict is NOT consumed: no cache increment, no class-status
  change, no coverage claim, no adoption.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Files

- `scripts/third_impl.js`: the pinned standing third implementation
  (sha256 08ea958f...), fetched from main and byte-verified.
- `output/raw/k01.p1.txt`, `k01.p2.txt`, `k02.p1.txt`, `k02.p2.txt`:
  the official cold-pass raws with node_rc trailers.
- `MANIFEST-sha256.txt`: kit manifest (sha256sum -c compatible).

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. A third-implementation agreement is not a class closure
claim, not a root verdict, and transfers nothing.
