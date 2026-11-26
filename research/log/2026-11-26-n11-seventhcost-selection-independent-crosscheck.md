# n11 seventh-cost selection independent cross-check (2026-11-26)

The seventh-cost lane declared and published its exclusive S5 selection kit
(class `1306043891938492416:0`, coverage {100, 103, 105, 108}, 42 exclusive
head-fresh keys; wave A 8d8c3c5c, wave B 2098c3ea) and is running the k01..k42
ladder as single owner. This lane, running in parallel, performed an
independent cross-check of the selection artifact only and did NOT touch the
ladder: no claimed-key replay was run, no raw row consumed.

## Cross-check results (kit: research/experiments/n11-seventhcost-selection-independent-crosscheck-20261126/)

1. **Pins**: selector sha256 581cb045..., jsreplay sha256 84585617... both
   byte-verified against the declaration; published selection JSON c395fe03...
   reproduced.
2. **Selector rerun**: 214/214 fail-closed gates PASS on this host in a
   reconstructed dependency tree (14 pinned sources fetched individually from
   raw CDN at 2098c3ea, each re-verified by the selector's own pin gates);
   two runs identical; regenerated keys JSON byte-identical to the published
   JSON; all 42 regenerated batch inputs byte-identical to the published
   inputs. Head-basis numbers reproduce: 108 children / 100 unknown under head
   42dbb58f / 42 exclusive / 58 shared / proxy_exclusive_sum 226,065,724 /
   bands 5,041,585 x4, 5,234,938 x28, 5,932,112 x10.
3. **Val-gate reproduction**: 4/4 node-exact on this host (2M x2: result 0 /
   nodes 2,000,000; 15M x2: result 2 / nodes 3,651,923 and 5,040,200).
4. **Fresh independent recomputation** (own logic, selector source not
   consulted): rank-7 unclaimed live class, exclusivity, full 42-key order
   with per-key proxy/legal, proxy sum and bands all match the published
   selection JSON, 14/14 ALL-CHECKS-PASS. Bookkeeping observation: 60 live
   classes under the head.

## Disclosure

- This sandbox has no git; the dependency tree was reconstructed file-by-file
  from raw CDN at 2098c3ea and every sha re-checked by the selector's
  fail-closed pin gates before any gate could pass.
- Concurrent-claim disjointness and quarantine absence were verified through
  the selector rerun's machine gates; the fresh recomputation independently
  confirmed all 42 keys are absent from the canonical head.
- The cross-check lane deliberately did not start any k01..k42 replay to keep
  the single-owner ladder undisturbed.

## Status guard

Selection/scheduling cross-check only; no verdict claimed, implied or
consumed; nodes and proxy values are never evidence of WIN or LOSS. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise.
