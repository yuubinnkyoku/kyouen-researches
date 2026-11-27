# n11-ninthcost-4loss-cppgate-20261127

Ninth-cost 4 LOSS row C++ scrutiny gate (k01/k03/k05/k06 of the exclusive
S5 probe class `1297036692683751424:134217728`, wave C6 commit 95883e09).
Thirteenth execution of the C++ gate lineage (after EN, EO, EQ, ET, EV,
SK, SM, SN, SR, SW, SX, and the eighth-cost k01 WIN gate), batch form per
the SW precedent. Scope, protocol, pins and the pre-registered execution
order are in the wave A declaration
(research/log/2026-11-27-n11-ninthcost-4loss-cppgate-declaration.md,
commit c703ca80, publish-then-execute).

- Targets: k01 `89,15000000,2,2163556` / k03 `86,15000000,2,7753840` /
  k05 `91,15000000,2,8687533` / k06 `99,15000000,2,8130387` - all
  machine-derived from the published at15m cold pairs (every replay field
  except wall_s identical in-pair; k01/k05 pairs byte-identical); the 2M
  UNKNOWN stage raws of all four keys are pinned (stage policy: the 15M
  escalations were published after the wave C5 2M sweep).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of the
  published SW kit inputs; quadruples == the SW kit anchors block).
- Freshness: all four [lo,hi] pairs ABSENT from the canonical head of
  record 0935c94c (6,875 s5verdict rows WIN203/LOSS6672, sha-verified) -
  verdict-unconsumed at declaration, run and publication time.
- Audit: FRESH multi-row fail-closed implementation (SS/SX single-row
  precedent extended to the SW batch form, disclosed) with the
  canonical-head freshness re-verification gate (G6).
- Third-implementation corroboration: OPEN for all four rows (and for
  the whole ninth-cost ladder, including the concurrent-C7 k12 WIN row,
  which this Part deliberately does NOT claim).

This kit consumes NO verdict. The four LOSS rows stay gate-verified
UNCONSUMED labels; a LOSS(2) gate result is only a verdict-level
agreement of the second implementation with the published
first-implementation cold pairs. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts. S5 raws are not class closure
claims and not routes to the root certificate.

Kit layout: scripts/ (maker, runner, audit, tamper battery),
input/ (4 target inputs + 3 anchor inputs + gate-rows.json),
output/ (gate-status.log, raw p1/p2 per row, audit_gate.json x3)
published by the run-record waves. MANIFEST-sha256.txt published with
the kit and refreshed with the run record.

## Run record (2026-11-27, publish-then-execute per declaration c703ca80)

Waves A/B published first (declaration c703ca80; kit a4ea02e4 with maker
gates all PASS, 2 runs byte-identical). Official execution
10:31:32Z-10:35:11Z sequential (pre-registered order anchor-at2m,
anchor-aj001, anchor-af039, then k01, k03, k05, k06 at budget 15000000),
all 7 rows GATE-PASS with (legal,budget,result,nodes) exactly the
published values (output/gate-status.log):

- k01 GATE-PASS 89,15000000,2,2163556
- k03 GATE-PASS 86,15000000,2,7753840
- k05 GATE-PASS 91,15000000,2,8687533
- k06 GATE-PASS 99,15000000,2,8130387

The pinned C++ second implementation reproduces the published LOSS(2)
verdicts of the four at15m cold pairs node-exactly (verdict-level
agreement of the second implementation; single cold pair per pass, p1
and p2 fresh processes, byte-identical replay fields except wall_s).

Audit: fresh multi-row audit PASS, 52/52 gates, 3 runs byte-identical
(audit_gate.json sha256 3ddb451e1e6e85431df24f8dac0ad632ae2948d9a0b6595
331bbdfeeb1f556db). Tamper battery 5/5 fail-closed (T1 expected-pin
flip k01 -> G0+G3 / T2 expected-pin flip k05 -> G0+G3 / T3 raw k03.p1
nodes edit -> G2+G3 / T4 phantom GATE-PASS -> G4 / T5 head byte append
-> G6) + clean control rc=0 (tamper.log; scratch copies only, including
a scratch copy of the canonical head cache).

Pillar status after this Part: the four C6-published ninth-cost LOSS
rows each have the replica cold pair (wave C6) and the C++
second-implementation gate (this Part); the third-implementation
corroboration remains OPEN for all ninth-cost rows, and the concurrent
wave-C7 k12 WIN(1) row (nodes 14521862) is not gated or claimed here.
No verdict consumed: all four rows stay gate-verified UNCONSUMED
labels; the canonical head 0935c94c (6,875 rows WIN203/LOSS6672) keeps
all four absent (G6 re-verified at audit time). The standard 11x11
empty board, every central-reply root, the two-stone root {60,27}, its
remaining third moves {100,108}, S2, class 1/2/4 and all closure
classes stay UNKNOWN. Nodes are bookkeeping.

Host disclosure: zig 0.13.0 (tarball sha256 d45312e6...), zig c++ -std=c++20
-O2 (the pinned source needs -std=c++20 on this host for
std::popcount/countr_zero; the flag does not alter the pinned source
bytes), binary not pinned. The pre-declaration anchor-at2m sanity run
(disclosed in the declaration) and the official anchor run both
reproduced 98,2000000,0,2000000.
