# n11 ninth-cost 4 LOSS row C++ scrutiny gate completion (2026-11-27)

Wave A declaration c703ca80 -> wave B kit a4ea02e4 (maker 32 gates
PASS, 2 runs byte-identical; runner comment-block-only transform of the
published SX runner, code lines machine-identical; fresh multi-row
audit G0-G6) -> wave C results + run record (this commit). Kit dir:
research/experiments/n11-ninthcost-4loss-cppgate-20261127/.

## Result

All 7 rows GATE-PASS (official execution 10:31:32Z-10:35:11Z,
pre-registered order, two fresh-cold passes per row):

- anchors: at2m 98,2000000,0,2000000 / aj001 84,30000000,2,5156075 /
  af039 89,30000000,2,19234232 (SW kit authority).
- k01 `1297036692683751424:134283264` GATE-PASS 89,15000000,2,2163556
- k03 `1297036761403228160:134217728` GATE-PASS 86,15000000,2,7753840
- k05 `1152921504624672768:536903680` GATE-PASS 91,15000000,2,8687533
- k06 `1152923703764321280:68719476736` GATE-PASS 99,15000000,2,8130387

The pinned C++ second implementation (kyouen_dfpn_root.cpp 9193f5b6 @
154f3b7a + headers 5976935d / 2e36d694, zig 0.13.0 c++ -std=c++20 -O2,
binary not pinned) reproduces the published ninth-cost wave C6 at15m
LOSS(2) cold pairs node-exactly. Expected quadruples were
machine-derived by the maker from the published raws (no hand
transcription); the 2M UNKNOWN stage raws of all four keys are pinned
(stage policy); the published cold-pair identity was re-verified on
every replay field except wall_s.

Audit: fresh multi-row fail-closed implementation, 52/52 gates PASS,
3 runs byte-identical (audit_gate.json sha256 3ddb451e...). Includes the
canonical-head freshness gate (G6): head of record 0935c94c (6,875 rows
WIN203/LOSS6672) sha-verified with all four [lo,hi] pairs ABSENT.
Tamper battery 5/5 fail-closed (T1/T2 expected-pin flips k01/k05 ->
G0+G3, T3 raw k03.p1 nodes edit -> G2+G3, T4 phantom GATE-PASS -> G4,
T5 head byte append -> G6) + clean control rc=0; all tampering on
scratch copies (including a scratch copy of the head cache).

## Pillar status and remaining work

The four C6-published ninth-cost LOSS rows now have two implementation
pillars each (replica cold pair + C++ gate). Still OPEN: (a)
third-implementation corroboration for all ninth-cost rows; (b) the
wave-C7 k12 WIN(1) row (nodes 14521862) and any further escalation rows
need their own gate Part(s) (SX WIN-side precedent); (c) adoption of any
ninth-cost row stays a separately declared Part under the parent
batch's WIN/LOSS conflict policy; (d) the ninth-cost pre-audit ledger
(08e4f924 schema family) will need the ninth batch-summary pin once the
ladder closes.

No verdict consumed. All four rows stay gate-verified UNCONSUMED labels.
The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. S2, class 1/2/4 and all closure classes: UNKNOWN. Nodes are
bookkeeping, never verdicts.
