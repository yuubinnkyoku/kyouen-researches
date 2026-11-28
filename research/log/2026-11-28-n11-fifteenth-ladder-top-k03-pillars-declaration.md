# Declaration: n11 fifteenth ladder-top k03 WIN-row pillars (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the k03 target runs. Any parallel lane must not gate or corroborate the
key below until this Part's completion log appears.

## Scope

The two remaining pillars for the fifteenth class 5804 k03 WIN row
`6053400849139367936:128` (class 5804, s5_index 212536, legal 92,
**WIN(1) nodes 3,364,655 @15M**, kit
`n11-fifteenth-ladder-top-k02k03-reescalation-20261128`, commits
declaration `88a24418` / kit+log `09358acd`), against the canonical
head of record `b5f322dd...` (6,898 rows WIN 216 / LOSS 6,682; k03
verified fresh/absent from the head by the re-escalation Part).
Declaration HEAD pin:
`09358acd7a3c0595de1be22f0cfab0f323813c07`.

## Method

1. **C++ second-implementation scrutiny gate**: gate source
   `kyouen_dfpn_root.cpp` sha256 `9193f5b6...` + headers
   `kyouen_residual_micro.hpp` `5976933d...` /
   `n11_s5_quarantine.hpp` `2e36d694...` (byte-fetched from the
   published tenth-cost k01k02 cppgate kit, sha-verified), built with
   zig 0.13.0 (tarball pin `d45312e6...`, sha-verified this session)
   `c++ -std=c++20 -O2`. Runner `gate_runner.sh` sha256
   `f2ebcc3e...` (byte-identical to the published u04/thirteenth/
   fourteenth/fifteenth-k01 runner). Fresh-cold pair (one process per
   pass); acceptance: p1 == p2 on (legal,budget,result,nodes) and both
   == the expected `92,15000000,1,3364655` (published re-escalation
   raw pair sha256 `58f2ad9d...` x2, byte-identical pair). Anchors
   (run as scratch before publication, precedent thirteenth/
   fourteenth/fifteenth-k01): anchor-at2m `98,2000000,0,2000000`,
   anchor-aj001 `84,30000000,2,5156075`, anchor-af039
   `89,30000000,2,19234232` (published-raw-pinned, inputs
   byte-identical to the published fifteenth k01 kit inputs).
   Tamper battery 4 cases fail-closed + clean control.
2. **Third-implementation corroboration**: standing `third_impl.js`
   sha256 `08ea958f...` (byte-fetched from the published tenth-cost
   thirdimpl kit, sha-verified),
   `--row=k03 --stones=5 --legal=92 --lo=6053400849139367936 --hi=128
   --cap=400000000 --wallcap=260 --memo-power=22`, two fresh-cold
   passes; acceptance: both report result 1 with identical
   expansions/nodes/quads/ttOverwrites.

Anchors and build ran as scratch before publication (precedent:
thirteenth/fourteenth/fifteenth-k01 pillars); the k03 target rows run
only after this declaration is on main.

## Non-meaning

Pillar bookkeeping only: NO verdict is consumed. Even on full
two-pillar COMPLETE, the k03 WIN row's adoption remains a separate
declared Part with the standing WIN-side flip-census review (k03
owner class union derived from the frozen graph `54f9c364...`;
caveat: shared-owner pre-exclusion as measured in the fifteenth k01
adoption reaudit, where the naive owner-union prediction over-predicted
flips [5601, 5804, 8675] vs measured [5601, 8675]). Class 5804 is NOT
complete (k02 remains 15M UNKNOWN; parking/L50M only under a future
declaration). The standard 11x11 empty board, all 19 central-reply
roots, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN. Nodes/expansions are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The k03 input csv is byte-identical to the published re-escalation
  kit input (sha256 `cad75b29...`); anchor inputs byte-identical to
  the published fifteenth k01 cppgate kit (pins in gate-rows.json).
- Anchor raws of this session reproduce the published anchors
  node-exactly (this host wall_s: at2m ~2s, aj001 ~9s, af039 ~38s per
  pass; host wall-clock only).
- Expected third_impl expansions are NOT pre-registered (measured
  this Part, precedent u03/k01).
