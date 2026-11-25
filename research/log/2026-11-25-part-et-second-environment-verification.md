# Part ET second-environment verification (2026-11-25, long-term lane)

Independent third-host verification of the Part ES re-probe-6 C++ scrutiny gate
(closure class 30345) published as commit waves 78ad43f4 / c17a7663 / 76697c6c /
8caefe38 (kit `research/experiments/n11-centralreply-closure-class30345-es6-cppgate-20261125/`).
Every artifact consumed here was fetched from published bytes at pinned commits
and sha256-verified before use. This verification consumes NO verdict and
changes NO canonical state.

## V0 - published-bytes fetch-back (all sha256 + size verified)

| source | pinned commit | result |
|---|---|---|
| ET kit (38 MANIFEST entries + README + MANIFEST) | 8caefe38 (close-out) | 38/38 byte-identical, 0 mismatch |
| gate source kyouen_dfpn_root.cpp + kyouen_residual_micro.hpp + n11_s5_quarantine.hpp | 154f3b7a | 3/3 = pins 9193f5b6... / 5976935d... / 2e36d694... |
| ES kit (Part ES source kit, 38 entries) | 2f22aa3b (close-out) | 38/38 byte-identical, 0 mismatch |
| EQ kit subset (runner/audit/maker + 3 anchor inputs + 6 anchor raws + MANIFEST) | 697b50dee8c59ec75a80a1c56e434ed58dfe39b8 (close-out) | 12/12 fetched entries byte-identical vs the 74-entry EQ MANIFEST |
| ER chain: increment-erwin18 cache 4f6b7797... + merged head 9c4dd94e... | 06119a79 (ER wave C) | 2/2 byte-identical; merged parsed 6,765 rows WIN186/LOSS6579 |

## V1 - maker replication (G0-G8) at the third host

`scripts/make_kit_et_es6_cppgate.py` (published bytes, sha 465a150b...) run with
the source tree above (HEAD.txt = the published `main_head_at_maker`
3683bf7d... so the emit is byte-comparable): **rc=0, ALL PASS**. Emitted kit
files byte-compared against the published kit: **12/12 byte-identical**
(9 input CSVs + gate-rows-et.json registry + gate_runner.sh + audit_gate.py
465a150b/60b6a6d6/6825e047 pins). G1 (ES 38-file verify), G2 (EQ subset),
G3 (status == targets-30m SSOT), G4 (6 targets, 2 WIN / 4 LOSS), G5 (p1==p2
discipline), G6 (targets fresh vs canonical head 9c4dd94e 6765/186/6579, ER
increment survival), G7 (anchor quadruples) all re-derived independently.

## V2 - gate rebuild

Pinned sources built with zig 0.13.0 `zig c++ -std=c++20 -O2` at the third
host. Binary sha256 06be2036... - not pinned, per the EN/EO/EQ disclosure
policy (the source pins are authoritative; this is yet another independent
binary from the same pinned sources).

## V3 - full official re-run from published kit bytes (the core check)

All 9 rows re-executed with the published `scripts/gate_runner.sh` (published
bytes aaf12017...) two fresh-cold passes per row, one process per pass, exact
kit inputs, sequential like the official run (anchors first). Third host,
2026-11-25 23:40:12Z-23:49:53Z (~9m41s wall, single process at a time).

**9/9 GATE-PASS** with (legal,budget,result,nodes) exactly the published
quadruples: anchor-at2m 98,2000000,0,2000000; anchor-aj001 84,30000000,2,5156075;
anchor-af039 89,30000000,2,19234232; ai041 91,30000000,2,15781960; ai030
91,30000000,2,16504156; ai024 86,30000000,2,19127057; ai038 89,30000000,2,19851840;
ai007 84,30000000,1,16090493 (WIN); ai040 85,30000000,1,20711023 (WIN).
Zero MISMATCH / GATE-FAIL / GATE-CRASH / TRUNCATED.

- wall_s-masked raw comparison (replay line field 8 + replay_done tail masked):
  **18/18 byte-identical** to the published raws. Honest disclosure: raw wall_s
  clock values differ per host (e.g. ai007 p1 37s published vs 35s here) - the
  only non-identical bytes in every raw, exactly the runner's declared
  pass-invariance discipline (all other replay fields, key_lo/key_hi included,
  byte-exact).
- Per-pass node total recomputed from the 9 re-run raws:
  **134,456,836** - equal to the published README SSOT and re-confirming the
  published honest erratum (declaration prose sum 134,449,387 is a mis-sum).
  Two-pass bill 268,913,672 (bookkeeping only).
- The published `scripts/audit_gate.py` run against the third-host run
  directory: **overall PASS, 46/46 gates PASS** (own audit json, wall_s detail
  fields naturally differ; not published - this log is the record).

## V4 - audit regeneration from published bytes

`audit_gate.py` executed 4x on the byte-verified published kit: **4/4 rc=0,
output byte-identical sha256 2c6d7441d6f752f160efbe7e275b807ff174d8cd70ece3c85aed135ead11c0d0**
(published audit value). Restore byte-verified afterwards.

## V5 - tamper battery (re-executed from published bytes)

Protocol kept: every tamper byte-change sha-asserted before the audit run;
restore byte-verified; clean control last.

- **T1** audit ROWS pin break (ai007 pin nodes 16090493 -> 16090494 in the
  audit script): tampered-state script sha256 e45be1a6... **byte-match with the
  published tamper.log T1 value**; audit rc=1, FAIL G3:ai007 exactly as
  published; restore to pin 6825e047... byte-OK.
- **T2** raw nodes alter (ai024.p1 19127057 -> 19127058): tampered-state raw
  sha256 f1b031da... **byte-match with the published tamper.log T2 value**;
  audit rc=1, FAIL G2:ai024 + G3:ai024; restore to pin d0ac312e... byte-OK.
- **T3** phantom GATE-PASS line appended to gate-status.log: audit rc=1,
  **FAIL G4 passes=10/9** exactly as published. Honest disclosure: the appended
  phantom-line bytes are this lane's variant (the original tamper.log records
  only its tampered sha 83f35058..., whose exact line content is not in any
  published file), so the tampered-state sha does not match here; the gate
  outcome is identical. Restore to pin ff102565... byte-OK.
- Clean control rc=0, regenerated audit byte-identical to the canonical
  2c6d7441... (see V4); post-battery full re-verify of the kit MANIFEST:
  **38/38 PASS, 0 bad**.

## Honest / environment lessons (this lane's own incidents, disclosed)

1. A first attempt at the ET MANIFEST was hand-typed into the workspace and
   produced two truncated sha mistakes before any use; it was abandoned unused
   and replaced by a raw fetch of the published MANIFEST itself
   (never hand-type pins - fetch every manifest byte-exactly; only the fetched
   copy was used for all verification above).
2. The first tamper-battery harness crashed on a relative-cwd subprocess path
   bug before any tamper-audit ran, and during triage a scratch "pristine"
   /tmp backup was overwritten with tampered bytes. Recovery: re-fetch of the
   tampered file from published bytes + pin-assert, then the battery was
   redone with the fail-safe ordering **pin-assert -> backup -> tamper ->
   pre-assert sha change -> audit -> restore -> restore-assert**, which is the
   run recorded above. No tamper touched any published state (all work is on
   the fetched local copy; the repo was never written by this verification).
3. Unauthenticated api.github.com hit its 60/h rate limit mid-run; metadata
   (commit shas, directory listings) moved to the authenticated GitHub app
   connector and byte fetches to raw at pinned commits (the K1344 protocol
   note that raw can be blocked by intermediaries did not reproduce here; all
   raw fetches succeeded).
4. Same class as prior lanes: single-process foreground execution only
   (~500K nodes/s here), no long-running background load.

## Status guarantees

Nothing is consumed: the 2 gate-verified WIN rows (ai007, ai040) remain
UNCONSUMED labels pending the Part EU adoption lane (declared 7136d22c, in
flight), the 4 gate-verified LOSS rows remain unconsumed EM-pattern territory,
b018 / k04 untouched. The standard 11x11 empty board, all 19 central-reply
roots, S2, class 1/2/4, and closure class 30345 all stay UNKNOWN. nodes are
bookkeeping, never verdicts. No coverage or root-resolution claim is made
anywhere in this Part. This verification adds no new claim - it raises the
evidence level of the published Part ET gate run to third-host reproduced.

## Resume notes (for the next run; re-fetch latest main first)

- Natural next second-environment candidate: Part EU adoption chain (waves
  C/D/E) once its completion log lands (declaration 7136d22c, wave B 3/3 done
  at feae2f6d; maker/merger/extractor byte-pins in the EU declaration).
- The 4 ES-resolved LOSS rows' EM-pattern loss-only adoption remains open
  territory after EU lands.
- b018 (dual-class batch-1) remains scrutiny-owner pending; same-condition
  re-probe ban untouched.
