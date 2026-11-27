# Part EQ completion log: b38-win-18 C++ scrutiny gate (class 30345) (2026-11-25)

Close-out of Part EQ, the THIRD execution of the C++ second-implementation
scrutiny gate in the central-reply chain.

## Result

All 21 rows GATE-PASS (18 unconsumed batch-38 WIN rows of closure class
30345 + the 3 anchors at2m/af039/aj001): every row two fresh-cold passes,
one process per pass, p1 == p2 on (legal,budget,result,nodes) and both
node-exact against the published batch-38 drive raws.  Zero MISMATCH /
GATE-FAIL / GATE-CRASH; no truncated artifacts.  The 18 rows are now
gate-verified UNCONSUMED WIN labels - eligible for a future adoption Part
(Part EP pattern), but NO verdict is consumed by this Part and the
canonical head fd29a337... is untouched.

## Publication waves (all landed on main; each preceded by a fresh head fetch)

* A 233ebe38  declaration log (research/log/2026-11-25-part-eq-win18-cppgate-declaration.md)
* B 9e8db4b5  kit: 26 files (declaration.md mirror, 21 input CSVs,
  gate-rows-eq.json machine registry, maker, runner, rev4 audit)
* C 81310623  outputs: 48 files (gate-status.log 21 lines, 42 raws,
  audit_gate.json + 3 replication runs all sha256 c2ff2232..., tamper.log)
* D this close-out wave (README run record, MANIFEST-sha256 74 entries,
  this completion log)

Parallel-lane head movement (f8b78b8c / 28835ae0 and others) was observed
between waves and checked each time: all orthogonal, no conflict on these
paths.

## Run record

Gate source 9193f5b6... + headers 5976935d... / 2e36d694... at commit
154f3b7a67; zig 0.13.0 build (binary 1d6ca50d..., not pinned, source
authoritative); official execution 20:38:17Z-20:49:47Z at a 4-core-light
2-worker policy (anchors sequentially first, targets in 2-worker waves);
the maker G0-G8 recovered all pins from published bytes (b38 kit verified
file-by-file against its MANIFEST including all 105 raws and the
status.log == batch-audit cross-SSOT; the EP increment c245bc4c and the
canonical head fd29a337 machine-verify ai048's consumption and the 18
targets' freshness).  Audit rev4: 4 byte-identical runs; tamper battery
3/3 fail-closed with byte-change assertions plus a clean control.

## Guarantees

No verdict consumed beyond the gate verification itself: WIN adoption is
a separate declared Part's exclusive right.  The standard 11x11 empty
board stays UNKNOWN, all 19 central-reply roots stay UNKNOWN, class 30345
stays UNKNOWN, nodes are bookkeeping, and no free/secured coverage or
root resolution is claimed anywhere in this Part.
