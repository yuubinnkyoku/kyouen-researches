# 2026-11-27 kit-19x AUTHORITATIVE CROSS-CHECK vs published kit-19 (record-of-record comparison)

## S1 Context

The kit-19x blind second census (this kit dir, commit f38d2b43, frozen
census sha256 275faedc80d04e2899c081eb7c56a0bcb80f7cf01b644793c6b846eb3d10a2f4)
was measured BLIND, before any kit-19 output was read. kit-19 has now been
published to main (takeover publication, waves 9c3c057b / b48e12fc /
fe78f9ba, frozen .out sha256
12277fd483aac7dfed4e3b687f3eb2433de44706d74377b08cd4c7db7acd623f,
626,727 bytes). This closes the pending authoritative cross-check.

## S2 Method

Fresh single-file comparator `crosscheck_kit19_authoritative.py`
(kit-18x precedent, commit 6ee2cfc0): neither explorer source is read; the
two frozen JSON outputs are compared row-by-row over the 49 row_record
sections by canonicalized separation multisets
(sorted X, S, value, collapse, direction).

Fail-closed gates: G0 kit-19x census sha pin 275faedc...; G1 kit-19x census
engine pin 582c93c1... PASS; G2 kit-19 .out sha pin 12277fd4...; G3 49 rows
each side, identical name sets; G4 all 49 row separation multisets
identical; G5 totals 273 both sides.

## S3 Result

CROSSCHECK-PASS. 49/49 rows identical, 273/273 separations identical
(multiset of sorted X, S, value, collapse, direction), frontier 40th/41st
m53/m54 datums, windows m51/m52 16 clean rows, 28 ladder rows, 3 evenlife
z=3m+18 rows included. The two independent implementations (kit-19 explorer
owner-lane pipeline; kit-19x fresh nested-loop harness) measured the same
registration (published kit-18 future constants) with the same engine SSOT
and agree exactly on every published datum.

## S4 Verification of the comparator

- Determinism: 2 runs, stdout byte-identical (cmp).
- Tamper battery 2/2 fail-closed (scratch copies, deleted after):
  T1 kit-19x census frontier m53 value flip -> G0 (sha pin) + G4 FAIL;
  T2 published-.out copy frontier m54 value flip with the tampered file's
  own sha pinned (pin gate satisfied by construction) -> G4 FAIL only.
- Clean control after the battery: rc=0 CROSSCHECK-PASS (the frozen run
  re-verified).

## S5 Honest disclosure

1. The comparison ran against the local frozen kit-19 .out file whose bytes
   were fetch-back-verified byte-identical to the published GitHub blob at
   HEAD fe78f9ba in the kit-19 publication step (7/7 byte-match on the full
   resource text, including the 626,727-byte .out) immediately before this
   cross-check; the G2 sha pin equals the published .out sha256.
2. This session is the kit-19x census lane; it also performed the kit-19
   takeover publication (disclosed in the kit-19 README/log, disclosure 1).
   The cross-check compares the kit-19x frozen census (frozen at 02:15Z,
   published 02:22Z, before the takeover session read any kit-19 measurement)
   against the kit-19 owner lane's 4-run frozen battery, which this lane
   published byte-unchanged. The blind property (kit-19x frozen before any
   kit-19 output read) is documented in the kit-19x log and was not violated
   by the takeover: freeze preceded first read.
3. A pre-publication informational comparison (vs the kit-19 owner lane's
   local runs) had already matched 49/49 rows and 273/273 separations
   (fresh comparator crosscheck_kit19_pre_pub.py, tamper 3/3 fail-closed,
   not republished here); this publication supersedes it as the record of
   record.
4. Hand-typed pins forbidden: every pin was machine-extracted.
5. This cross-check is a consistency result between two frozen finite
   censuses. It consumes no verdict. The standard 11x11 empty board, all 19
   central-reply roots, the two-stone root {60,27}, the third-move
   {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all times.
   Frontier parity 42/42 and the even-m lifecycle template are finite
   observation counts, not laws. No K-slot claim is made.
