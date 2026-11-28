# 2026-11-28 n11 thirteenth ladder-top class-16757 k01+k02 adoption declaration

Single-owner declaration (publish-then-execute) for the canonical
adoption of the two thirteenth ladder-top WIN rows into the head of
record:

- k01 `1153204147814662144:65536` (class 16757, legal 72, s5_index
  556117, WIN(1) nodes 2,678,305 @15M): escalation kit
  `n11-thirteenth-ladder-top-escalation-20261128` (`12d8359c`), both
  pillars COMPLETE (cppgate GATE-PASS `72,15000000,1,2678305` +
  thirdimpl CORROBORATION-PASS, commit `f1f5c49d`), cross-host
  replicated XHOST-PASS (`eb542121`, this lane).
- k02 `1152922672837951488:65792` (class 16757, legal 72, s5_index
  558553, WIN(1) nodes 3,485,963 @15M): escalation kit
  `n11-thirteenth-ladder-top-k02-escalation-20261128` (`3087c38b`),
  both pillars COMPLETE (declaration `177b1086`, completion
  `7ebf903e`), cross-host replicated XHOST-PASS (`8cc714bf`, this
  lane).

## Pre-registered adoption facts

- BASE head of record: `beecb024...`
  (`merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache`),
  6,894 rows WIN 212 / LOSS 6,682, sha256-verified on this host; both
  adopted keys verified fresh/absent (no WIN/LOSS conflict possible
  by absence).
- Expected merged shape: **6,896 rows WIN 214 / LOSS 6,682** (BASE +
  exactly these 2 fresh WIN rows; any other shape is a fail-closed
  stop).
- New head name: `merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`.
- Merger pin `90711961...` x3 byte-identical; maker (fresh structural
  descendant of the u04 adoption maker) x2 byte-identical, with G0
  pins (merger/policy/quarantine/BASE/gate source+headers + 6 published
  kit MANIFEST self-verifications), G1 live re-run of BOTH published
  gate_runner.sh instances, G2 six-pillar re-parse, G3 freshness +
  no duplicates + no WIN/LOSS conflicts, G4 quarantine-free +
  canonical-safe per s5_evidence_policy, G5 increment build, G6
  merger x3 + shape check.  All gates fail-closed.
- Owner-union pre-registration: kit
  `n11-thirteenth-owner-union-precheck-20261128` (`fdb704d7`) -
  combined owner union [16612, 16740, 16757, 30542], serving class
  16757 leaves the 800-row closure ladder (unknown_now 2 -> 0).
- Known kit defect disclosed up front: the published k02 cppgate
  kit's MANIFEST contains a self-referential
  `MANIFEST-sha256.txt` line (a manifest cannot contain its own
  sha256); the maker excludes that line from verification and the
  adoption kit README discloses it.

## Scope and guards

Only the 2 named rows may be adopted in this Part.  NO root verdict
is consumed; the rows are cache bookkeeping, NOT a class closure, NOT
a root verdict, and transfer nothing.  Class 16757 completion
additionally requires Board-verified free_now at adoption time; the
WIN-side flip-census review (BASE `beecb024` -> SCEN measurement,
owner-union prediction from the precheck kit) is the declared
follow-up Part.  The standard 11x11 empty board, the 19 central-reply
roots, the two-stone root {60,27} and third moves 100/108 stay
UNKNOWN.  Nodes are bookkeeping, never verdicts.

The maker (with its live gate re-runs) runs only AFTER this
declaration is on main.
