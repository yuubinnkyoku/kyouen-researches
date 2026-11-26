# n11 sixth-cost k09..k43 resolved-rows third-implementation batch (30 LOSS + parked4 WIN k13/k19): single-owner note (2026-11-26)

Declared: 2026-11-26T08:45Z (lane: the recurring n11 long-term lane; same lane
and same host-session as the k06/k07/k08 third-impl addendum declared at 07:58Z
(`b9dc2bb3`) and published at `ebdc7de7`. This note extends the
third-implementation verdict re-verification program
(`research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`,
notes 53d8fe28 / d33d752b / bcc39add / f5124331 / b9dc2bb3) - per its own
fresh-declaration rule - to the thirty resolved-LOSS rows of the fifth
resumption batch k09..k43 of the sixth-cost exclusive S5 probe AND to the two
fresh WIN rows k13/k19 published minutes ago by the parked4 L50M ladder
(`73dfd4a7` checkpoint with halt-audit close-out `4e87e67b`), whose
consumption gate requires third-implementation scrutiny ("delegated targets
recorded"; this batch supplies that scrutiny record for third_impl, while the
pinned C++ gate stays delegated)). HEAD re-fetched immediately before this
push: `4e87e67b` (the parked4 ladder close-out; territory disjoint from every
path written here - probe dir untouched, parked4 kit dir untouched, this lane
writes only its own experiment dir and two log files). Repo probe (this
session, before this push): `audit_k09` 0 hits; no k09..k43 third-impl note,
kit file or claim of any kind exists on main; no k13/k19 third-impl artifact
exists (the parked4 close-out states both WINs stay UNCONSUMED pending pinned
C++ and third-implementation scrutiny, which is not claimed by that lane).

Host honesty: same NEW host as the k06/k07/k08 addendum (Vibe sandbox, Node.js
v22.20.0, Python 3.12.14, no C++ toolchain). The C1 calibration raws of this
session (out/calib-verify-tbl-k06k07k08.txt: replica quads 95,670 == mine
95,670 over 195,044 triples, 0 mismatches, rc=0; out/calib-anchor-w2-k06k07k08.txt
and out/calib-anchor-w2-run2-k06k07k08.txt: anchor w2 `10376293541461626880:131328`
WIN(1) expansions 7,583,990 == the published ea73c3e3 witness value on two
executions with identical counts) are HONESTLY REUSED for this batch extension:
same host, same session, no clock restart between them (k04-addendum precedent).

## Scope (32 rows; every replica raw unconsumed)

The thirty resolved-LOSS exclusive keys of the fifth resumption
(k09..k43 minus the parked keys k19-was/k20/k33/k38 before the ladder), PLUS
the two parked4-L50M-ladder WIN rows, all in ascending truncated-cost-proxy
machine order: k09, k10, k11, k12, k13(WIN), k14, k15, k16, k17, k18, k19(WIN),
k21, k22, k23, k24, k25, k26, k27, k28, k29, k30, k31, k32, k34, k35, k36,
k37, k39, k40, k41, k42, k43. The three still-parked keys k20/k33/k38 have no
new verdict and are outside this scope (neither measured nor claimed).

- The 30 LOSS rows: row specs are the published batch inputs of
  `n11-sixthcost-exclusive-selection-v1` (each fetched at HEAD `ebdc7de7` and
  byte-compared against the pinned lane kit copies on this host; per-file sha
  pins recorded inside the new auditor). Twenty-six resolved at the 15M stage
  (at2m UNKNOWN raws result 0 nodes 2,000,000 plus a 15M cold pair both
  LOSS(2) with identical nodes); four resolved at the 2M stage (k17/k18/k28/
  k32: 2M determinism pair both LOSS(2); k17/k18 additionally have a 15M cold
  pair with identical result and counts published as extra evidence).
- The 2 WIN rows (published by the parked4 lane at `73dfd4a7`, consumed at
  HEAD `4e87e67b`): **k13 `1152921573327376384:536870912`** (stones 5, legal
  95; row spec `target,0,5,1152921573327376384,536870912,95,0,0,0,0,0`) with
  four identical WIN(1) runs at nodes 16,402,480 (50M pair + 32M margin + 50M
  verify per the ladder's close-out) and a fresh base15m parked baseline
  (result 0, nodes 15,000,000); **k19 `10376293541461626880:65664`**
  (stones 5, legal 95; row spec `target,0,5,10376293541461626880,65664,95,0,0,0,0,0`)
  with four identical WIN(1) runs at nodes 15,379,062 and the same fresh base15m
  baseline. Their twelve replica raws are re-published inside this experiment
  dir at out/k13-replica-raws/ and out/k19-replica-raws/ with per-file sha pins
  inside the auditor (self-contained kit, k05 precedent).

Implementation and pins identical to every earlier note of this program
(third_impl.js sha256 `08ea958f...`, verify_tbl.js `c8c52528...`, replica
jsreplay.js `84585617...` consumed by verify_tbl.js only; all 102 replica
raws consumed over raw.githubusercontent.com at the recorded HEADs, byte-hashed
here before any run).

## Pre-registered gates (fail-closed, decided before any run this session)

- C2 verdict-level expectations, pre-registered from the published replica
  raws: LOSS(2) for each of the 30 LOSS rows (TWO full cold runs each,
  --cap=400000000 --wallcap=270 --memo-power=22, independent fresh solvers,
  identical (result, expansions, ttHits, ttOverwrites)); WIN(1) for k13 and
  k19 (THREE full cold runs each per the WIN-row precedent: kNN-a, kNN-b,
  kNN-v with --verify-legal=1, all identical). Execution serial, one node
  process at a time, ascending machine order. Expansion counts are never
  compared to replica node counts; the verdict is the agreement gate, plus
  the anti-copy requirement int(expansions) != int(replica resolution nodes).
- C4 fail-closed input gates per row: declared legal+1 and declared stones=6
  both GATE_FAIL with process rc=1 (--cap=4000000 --wallcap=60).
- C5 any disagreement (a third-impl result differing from the published
  replica verdict on a claimed row, or a determinism-pair divergence) is a
  HARD STOP of the batch: publish the executed raws plainly with an honest
  stop label, no interpretation, no auditor for the unresolved portion, hand
  to the scrutiny owner; completed rows are still published as raws with
  their verdicts UNCONSUMED.
- Pre-registered session budget stop: if the session budget ends before the
  last row, the batch stops at the last completed row (honest budget-stop in
  the session log); remaining rows stay claimable by a fresh declaration.
- Auditor: a separate data-driven `audit_k09k43.py` (audit.py, audit_k04.py,
  audit_k05.py, audit_k06k07k08.py stay byte-frozen), deterministic,
  byte-identical output across runs in a fixed layout (resolved-path detail
  strings only being layout-dependent, as in the k06/k07/k08 auditor), exit 0
  only on all-pass; it re-derives every gate from the raw files, the pinned
  scripts and the pinned row-spec inputs. Negative tamper controls on full
  kit copies (a verdict flip on one claimed LOSS row and on the WIN row k13;
  a replica-raw nodes edit on one claimed row) must each fail closed with
  rc=1; restores byte-verified; final clean control rc=0.
- C6 no verdict consumed; no cache file touched; adoption stays with the
  scrutiny owner under the unchanged delegated pinned C++
  second-implementation gate (cpp/solvers/kyouen_dfpn_root.cpp sha256
  `9193f5b6...`; no executable C++ toolchain in this sandbox, re-verified
  this session). This batch records row specs and verdict-level expectations
  (including the two WIN rows' targets) for any future C++ execution; any
  later C++ disagreement fails closed in favor of discarding the row.
- Publication: addendum files + README batch addendum + MANIFEST append
  inside this lane's experiment dir; no probe-dir or parked4-kit writes, no
  K item, no knowledge README edit; a session log closes the run.

## Concurrency and disjointness

HEAD re-fetched immediately before this push (`4e87e67b`). Territory disjoint:
the parked4 kit is only READ (its raws are consumed and re-published inside
this lane's experiment dir); k20/k33/k38 (still parked) are untouched; the
z-strip lane and every probe-dir path are untouched; the third-impl program
extension territory has been idle for every key outside k01..k08 (probed
above).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves {100,108} remain UNKNOWN throughout. Node/expansion counts, wall
times and budgets are never verdicts. Third-implementation agreement is
cross-implementation evidence only; the sixth-cost class status continues to
be decided by the canonical chain, not by this lane. No WIN or LOSS found by
the parked4 ladder or the probe batch is consumed by this note.
