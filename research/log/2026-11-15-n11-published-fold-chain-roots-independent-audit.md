# 2026-11-15 n11 published-fold chain — independent whole-chain receipt audit (class2 lane)

Class2 lane (11x11 two-stone-root proof-support lane). Independent re-verification of the
entire published WIN7 fold chain — 26 base certificate files, 52 chain heads, 14 post-70e
heads, and the 77a claim — from the pinned blob identities up to the head arithmetic, with
no reuse of any prior audit script state.

## What was audited (all byte-exact against pinned git blob shas)

- 88 pins verified byte-exact: 26 base WIN7 certificate files + 52 chain heads + 10
  post-70e pinned heads. The last unpinned pins were recovered this session:
  72c (`42dbb92e…`, inside the 73g fold script), 77a head (`a2ba7235…`, from the 77a
  claim's fold.output_blob_shas), plus 65l/74g/69i/73h/mergedAB/merged1277/76b/70e from
  the merged and per-lane fold scripts.
- 4 unpinned post-70e heads (71c, 70f, 73g, 70g) carry computed blob shas in the audit
  JSON as pin proposals for a later pin commit.

## Verified results

1. **Root inventory reconciled, branch-aware**: base 26 files -> 195 raw / 194 distinct
   WIN7 roots (one intra-base duplicate `00000000000000801a02040080000000` listed by both
   cost68 and cost75 base files); chain 52 heads -> 402 distinct; base∩chain overlap 104;
   @1233 folded = 497 (matches 71c published). Post-70e cumulative in document order:
   497→499→503→512→520→528→532→534→544→548→544→548→550→553, and every head's
   own-branch lineage (following own_baseline links across fork/merge branches) matches
   its published own claim (65l 534, 74g 542, 69i 546, mergedAB 544, merged1277 548,
   76b 550, 77a 553).
2. **D4 orbit analysis** on the full 553-root inventory: 542 orbits, exactly 11 twin pairs
   (each twin pair = two inventory roots sharing one D4 orbit), multi-provenance roots
   enumerated.
3. **Per-record geometry** over every published receipt shape (per-bit dicts, root-list
   aggregates, single dicts, record lists, lane-nested `group_additions`, merged-receipt
   suffixes): 418 receipt records + 40 group records, all popcount-7 / covers-7 /
   canonical-hex / marginal-subset / mim-count checks PASS; 0 logical anomalies.
4. **New published-data erratum found**: `cost63b_addition` in
   `class2-lane-cost63cd-frontier-recompute-20261114.json` carries one malformed
   35-character marginal hex string `00000000000010000003800000000100020` (the other 7
   entries are valid; `marginal_in_manifest`=8 is count-consistent, and no 1-4 char
   deletion/Levenshtein-4 repair pins a unique intended value among the 15 unlisted
   covered candidates). Count-level arithmetic is unaffected; hex-level identity of that
   one entry is not recoverable from the published corpus alone.
5. **Head arithmetic, 66 heads, 0 anomalies**: classification 46 sequential-fold-union,
   11 parallel-batch-union, 1 own-label-recompute (cost69a), 1 cross-head-merge
   (unified-merge head: 37 local receipt marginals + 8 declared cost68d lane marginals
   whose records live in the 68dhyg head), 7 no-numeric-baseline-quote.
6. **Baseline-quote provenance, exact state matching**: a global table of every published
   5-field frontier state in the 66-head corpus was built; 58 of 59 numeric baseline
   quotes match some published state exactly. One genuine quote erratum confirmed and
   characterized: **cost70f** quotes 71c's final solved count (1235) but its four
   remaining-fields are the pre-71c baseline values (6614/522131/4884/385854 vs 71c's
   actual final 6612/521988/4882/385711) — the quoted 5-tuple matches no published head;
   delta arithmetic uses the correct solved baseline and reconciles with the receipts.
   **cost74g** is the single pointer-differs case: prose names 72c but the quoted values
   are 73h's `frontier_after_cost73h` state exactly (values correct, pointer name wrong).
7. **Convention-external receipt confirmed benign**: exactly one receipt outside the
   `_addition`/`merged_receipts`/`group_additions` convention — root
   `00008000000000803202000000000200` under `cost72_fold` in the cost75c head; its D4
   orbit `00000008000000803800000008200000` is in the audited inventory (twin of an
   in-inventory root).
8. **Child-orbit closure**: 21 heads declare an s6 child closed by a bit; for each, the
   audit independently located the closing receipt record(s) containing that child hex in
   their marginal sets.
9. **77a endpoint**: 1282/6565/518522/4835/382245, receipts 3 (bits 40, 64, 111), child
   closed at bit 40; the 77a claim's fold record matches the published head JSON
   byte-exact (blob sha + 7554 bytes), and the published head transition
   1280/6567/518678/4837/382401 -> 1282/6565/518522/4835/382245 holds.
10. **Canonical-line hex-level exactly-once (1233 -> 1282)**: walking the canonical
    chain 71c/70f/72c/73g/70g/73h/merged-1277/76b/77a (every consecutive baseline
    provenance already verified by the state matching in item 6; branch marginals
    65l/74g/69i enter once via the merged-1277 `merged_receipts`), the 49 manifest
    hexes solved between the 1233 baseline and the 1282 endpoint are each claimed as
    a marginal by exactly one receipt record: total mim 49 == 49 distinct hexes ==
    1282 - 1233, zero multi-claims. The count-level head arithmetic and the hex-level
    claims agree with no double counting anywhere on the canonical line.

## Interpretation guard

This is a bookkeeping audit over published receipts and head records only. Solved counts
measure manifest coverage, not the game-theoretic value of any position. WIN7
certificates prove a win within depth 10 from the individual 7-stone roots only.
Nothing in this audit decides any S5 parent, any class, the two-stone root {49,60} or
the 11x11 empty board: **11x11 empty board / two-stone root {49,60} / S2 {59,60} /
class 1 / class 2 / class 4 all remain UNKNOWN.**

## Machine-readable record

- Audit JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-20261115.json`
  — git blob sha `79cab6414f9fd23f7ad7ba16966fe0b214f231a5`, 80309 bytes,
  md5 `854d5ee5864b9c3087758ec5f086d371`; two consecutive runs byte-identical
  (supersedes the first landing blob `2bffb633…` / md5 `4daa8da8…`, which did not yet
  include the canonical-line exactly-once check).
- Audit script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_independent_20261115.py`
  — git blob sha `2fb84e55f088bab36416d17bce2882415dfa555e`, 51308 bytes. Runs from the
  experiment directory with `output/` holding the 93 published files (verified to run
  in-repo, byte-identical, with the repo's full output/ present); every check is an
  assert, verdict prints `AUDIT PASSED`.
- Pin proposals (computed this session, not yet pinned): 71c
  `61af2eb311f938f5ee5bf2bb20d8c1a76787dc87` (11891 B), 70f
  `4d0f130e975b6a7bec4759387bd6d54dfe2b6a18` (9643 B), 73g
  `e4fb98dc8670fbb85786ab02f017a0a95e357648` (12956 B), 70g
  `73890fe34580ec2f869a97a00b3e6400eda30c0a` (13915 B).

## Resume notes

- cost-77b / cost-78a / cost-75d fold work belongs to the parallel class2-lane runs
  (`tmp-cost77b`, `tmp-cost78a` already exist in the experiment directory); this audit
  lane did not touch them.
- Next candidates for this lane: (1) pin the four proposed blob shas in a later fold
  script's pin table; (2) record the cost63cd malformed-hex erratum in the lane's errata
  list if one is maintained; (3) extend the same whole-chain audit to heads published
  after 77a once the 77b/78a chain lands.

## v3 extension (2026-11-15, same audit lane): chain extended to the 77b/77c/75d heads

Three folds landed after the v2 audit (77b head
`1286/6561/518211/4831/381934`, 4 receipts bits 9/12/59/105; 77c head
`1290/6557/517923/4827/381646`, 8 receipts bits 10/40/50/54/58/95/96/111;
and the deferred 75d fold rebased onto the 77c head per its deferral-note
rebase clause, head `1296/6551/517468/4821/381191`, 4 receipts bits
12/40/92/111), so the same whole-chain audit was extended (v3) to the new
canonical endpoint 1296. No prior audit script state is reused beyond the
v2 script's own verified structure; every new number is re-derived from the
published files.

What changed in v3 (all re-verified, two consecutive runs byte-identical):

1. **Pins extended 88 -> 95**: the four v2 pin proposals (71c `61af2eb3…`,
   70f `4d0f130e…`, 73g `e4fb98dc…`, 70g `73890fe3…`) are now pinned in the
   audit's POST70E pin table (v2 resume item (2)), and the three new heads
   are pinned from published provenance: 77b `b648ed06…` (the 77c head's
   `baseline_main` quote), 77c `7f2badce…` (the in-flight cost-77d claim's
   `chain_head_at_claim`), 75d `c801e605…` (the completed 75d claim's
   `output_blob_shas`). All 95 pins assert byte-exact; no post-70e head
   remains unpinned.
2. **Root inventory 553 -> 569** (557@77b, 565@77c, 569@75d), all reconciled
   branch-aware (77b's baseline 77a, 77c's baseline 77b, 75d's baseline 77c;
   every own-branch lineage matches the published own claim). The 16 new
   receipt roots add 16 new D4 orbits and **no new twin pair** (558 orbits /
   569 roots / 11 twin pairs), independently confirming the 77b/77c/75d
   fold scripts' raw+D4 disjointness assertions against the full prior
   inventory — in particular that the deferred-then-rebased 75d receipts
   were never counted anywhere before.
3. **Per-record geometry**: 434 receipt records + 40 group records, 0
   anomalies; the cost63cd malformed-hex erratum remains the single
   published hex erratum.
4. **Head arithmetic 66 -> 69 heads, 0 anomalies**: 77b, 77c and 75d all
   classify as sequential-fold-union (deltas 4/4/6 with sum_mim ==
   union_mim == delta; 77c's raw marginal 36 and 75d's raw marginal 22 each
   carry only 4/6 in-manifest); all three baseline quotes match published
   states exactly (77b quotes the 77a frontier state, 77c the 77b state,
   75d the 77c state). The 70f quote erratum and the 74g pointer-differs
   case remain the only two quote-level findings.
5. **Canonical-line hex-level exactly-once extended 1233 -> 1296**: the
   canonical line now ends at 75d (77a -> 77b -> 77c -> 75d appended); 63
   manifest hexes (49 + 4 + 4 + 6) are each claimed as a marginal by
   exactly one receipt record, total mim 63 == 63 distinct == 1296 - 1233,
   zero multi-claims.
6. **Endpoint checks extended to 77a/77b/77c/75d**: all four completed-claim
   fold records match their published head JSONs byte-exact (blob shas
   a2ba7235…/b648ed06…/7f2badce…/c801e605…, 7554/8073/10558/8992 bytes) and
   the published head transitions 1280 -> 1282 -> 1286 -> 1290 -> 1296 hold.

cost-77d (sweep in flight on a parallel lane against the 77c head) is NOT
part of this audit — no fold head exists yet; its eventual fold must rebase
to the new canonical head 1296. This lane touched neither the 77d sweep nor
any in-flight claim.

The cost63cd malformed-hex erratum is recorded in K0783 this session
(v2 resume item (3)).

### v3 machine-readable record

- Audit JSON (supersedes the v2 landing): schema
  `n11-class2-lane-published-chain-roots-independent-audit-20261115-v3`,
  md5 `77d3b34952c46f16d074692b468eeb66`, 86060 bytes.
- Audit script: same path, extended in place (the v2 structure is kept;
  POST70E pin table and order, own-claim/own-baseline tables, canonical
  line and endpoint checks are the changed regions).

### Interpretation guard (unchanged)

Bookkeeping audit over published receipts and head records only. Solved 1296
is manifest coverage, not any position's game-theoretic value. REFUTED-D10
is not a LOSS proof. **11x11 empty board / two-stone root {49,60} /
S2 {59,60} / class 1 / class 2 / class 4 all remain UNKNOWN.**
