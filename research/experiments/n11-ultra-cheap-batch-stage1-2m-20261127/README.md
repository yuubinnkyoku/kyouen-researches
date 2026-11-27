# n11 ultra-cheap batch stage-1 sweep (2M cold pairs + 15M WIN-stopped escalation)

Execution kit of the ultra-cheap batch declared in
`research/log/2026-11-27-n11-ultra-cheap-batch-declaration.md` (commit
`3781d82f`), covering the four one-unknown class-completion S5 keys
published by the ultra-cheap census (`a60716ac...`) with
dual-implementation legal pre-check (`89fd85ac...`), under canonical head
of record `1e2eeda2...` (6,890 rows WIN 208 / LOSS 6,682).

## Results

- Stage-1 sweep: **4/4 keys UNKNOWN at the 2,000,000-budget cold pair**
  (result 0, nodes 2,000,000; 4/4 cold pairs node-identical; u02/u03
  pairs byte-identical, u01/u04 pairs differ only in wall_s fields).
- 15M escalation (declared order u01..u04, WIN-stopping rule active):
  **u01 `1153485622925590528:0` resolves WIN(1) at nodes 4,893,014**
  (cold pair node-identical; raws at15m-u01-p1/p2.raw).  The WIN
  stopping rule fired: u02, u03, u04 are escalation-suppressed and stay
  UNKNOWN at 2M (parking/L50M only under a future declaration).
- No overreach: no suppressed key was run at any higher budget; no other
  key was run at any budget in this Part.

## Pillar status (single implementation only)

All rows are single-implementation (Node.js replica jsreplay.js,
byte-clone of the published `84585617...`, pinned in the tenth/eleventh
selection kits on main and locally sha256-verified at assembly; not
republished here).  The u01 WIN row requires the C++
second-implementation scrutiny gate and a third-implementation
corroboration (both separate Parts) before any adoption; a u01
adoption would also require the standing WIN-side flip-census review
(class 1849 completion would be Board-verified free_now at adoption
time).  The verdict is NOT consumed: the u01 row is cache bookkeeping,
not a class closure, not a root verdict, and transfers nothing.

## Files

- batch-summary.json - machine summary (schema
  n11-ultra-cheap-batch-stage1-summary-v1), per-key at2m pairs and the
  u01 at15m WIN pair, WIN-stop bookkeeping, disclosures, guards.
- raws/at2m-u01..u04-p1/p2.raw - 8 stage-1 raws (2M cold pairs).
- raws/at15m-u01-p1/p2.raw - the u01 15M escalation cold pair (WIN).
- input/u01..u04.input.csv - the four probe input rows (wave A).
- MANIFEST-sha256.txt - sha256 of every file in this kit.

## Meaning and non-meaning

Scheduling/batch bookkeeping only: NO verdict is claimed or implied.
Nodes are bookkeeping, never evidence of WIN or LOSS.  The standard
11x11 empty board, the two-stone root {60,27} and its remaining third
moves 100/108 stay UNKNOWN.
