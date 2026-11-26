# newband m33/m34 frontier first contacts + m19..m32 ladder continuation + m13/15/17 probe lifecycles + even-mid trio probes + m31/m32 window sweeps pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the REGISTERED kit-8 frozen output future
constants (commit 7af915fb, publish-priority kit-8 census; the
m=31/m=32 window rows were the kit-8 log S5 item-12 proposals): the 34
binding candidate rows (the one-past/birth rows of m=19..m=28 items
1-20, the m=29/m=30 mini-ladder rows items 21-26, the CONTINGENT
m=31/m=32 mini-ladder rows items 27-32 the kit-8 births made
contingency-resolved, and the frontier first contacts m=33@z=65 /
m=34@z=66, the registered 21st / 22nd K1268 parity datum candidates,
FIRST-EVER rows for those m), the TRIO-TRACKER continuation rows
(m=19 z=58 / z=59, NON-BINDING: the stacked trio {19,19,19}@S=57
tracked beside the binding seats, either outcome the datum), the
m=13/15/17 PROBE LIFECYCLE rows (kit-8 log S5 item-11 continuation,
NON-BINDING scaffold rows z=3m-1 / 3m / 3m+1 with the S5 item-9
stack-shadow candidates registered for the z=3m birth slices), the
EVEN-MID-SLICE PROBES m=14@z=40 / m=16@z=46 / m=18@z=52 (kit-8 log
S5 second-census item, counter-probed 0-hit at this build,
birth-template seats + trio exact-mimic candidates), and the WINDOW
SWEEPS m=31 z in {53..60} / m=32 z in {54..61} (kit-8 log S5 item-12,
register-before-measure satisfied by this freeze; FIRST-EVER
below-frontier rows for m=31/m=32), plus 234 published anchor
rechecks (the kit-8-era 180 anchors VERBATIM + the 54 kit-8
separation spots, machine-extracted from the published kit-8 frozen
.out and machine-verified 54/54 BEFORE the first run of this kit by
verify_new_anchors_kit9.py, independent pre-freeze script). No K slot
is claimed and no claim is made here: everything below is machine
observation; the only PROVED statement remains the K0832 closed form.

## Files

- `engine_block.py` -- byte-clone of the published chain engine, sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8841d3a6610d5c0`
  (byte-identical to the kit-4..kit-8 chain); embedded ENGINE_BLOCK
  startup pin `bd5f22e4...` asserted (engine_gate PASS in the frozen
  output).
- `explore_m33m34_frontier_ladders.py` -- frozen pre-declaration
  explorer, sha256
  `d38af1b6e48708e643cd73c4ea9a3a85e2c3830fcb0ce3d1bd88227948d154a5`
  (127,224 bytes; assembled programmatically from the published kit-8
  explorer -- ENGINE_BLOCK, the row_record/row_record_x0 helpers and
  the 180-entry anchor_spec copied verbatim, byte-fidelity asserted
  by the assembler -- plus the machine-derived kit-9 rows). Every
  registered literal was machine-regenerated engine-free by
  `derive_kit9.py` (579 structural asserts, 0 failures; the
  regenerated prediction TEXT of all 34 binding rows byte-matches the
  kit-8 frozen future constants).
- `explore_m33m34_frontier_ladders.out` -- the frozen stdout, sha256
  `eb0c0c146c3d16090a604377a1aafc50bd56faee48a81cbdfa6d995df7db7a3f`
  (201,566 bytes): EXPLORE-DONE, 62 rows, 1,230 shapes, 100
  separations.
- `derive_kit9.py` -- engine-free paper derivation of every registered
  literal from the K0832 closed form and the seat-lifecycle scaffold
  (z*(m)=2m-2+(m%2) per K1268; birth slice z=z*+2d, co-token m+2d+1
  (odd) / m+2d (even), S=2m+2d+1 (odd) / 2m+2d (even), one-past
  z=z*+2d+1, dead shape S=z-1, stick seat S=z, NEW birth S=z+2). 579
  checks, 0 errors, run BEFORE the first row sweep; the regenerated
  prediction text of all 34 binding rows byte-matches the kit-8 frozen
  output section future_slice_registration constants.
- `verify_new_anchors_kit9.py` -- the 54 kit-8 separation spots
  re-measured 54/54 on the published canonical engine, plus 180+54
  anchor-table byte-fidelity and 54/54 transcription and 54/54
  second-census agreement, all BEFORE any census row ran.
- `audit_kit9.py` -- INDEPENDENT ordered-engine audit re-executing
  every row with the ordered product: 62/62 rows 0 mismatches, 234/234
  anchors, battery 1,454/1,454, the 34-row classification reproduced
  (30 FULL HIT + 4 HIT-with-unregistered-shadow rows), lifecycle /
  probe / window / tracker outcomes explicit, and the CO-SPLIT SHADOW
  pattern machine-checked row by row (0 anomalies; see the log).
- `README.md` -- this file.

## Protocol

Pre-declaration (publish-then-execute): the registrations, the
derived literals, the anchor table and this README were frozen BEFORE
the first census row execution; the frozen .out was produced by a
single run of the frozen explorer and re-verified byte-identical 5
further times (2 default, PYTHONHASHSEED=random, 2 env-isolated) plus
the push-time isolated rerun (7 executions, one byte string). The
counter-probe at build (12 code-collision queries over the kit-9
territory) returned 0 hits; the push-time counter-probe is re-run and
recorded in the log. Standard caveats: the K0832 closed form remains
the only PROVED statement; every item in the log is a finite machine
observation; the standard 11x11 cell remains UNKNOWN at all times; no
K slot is claimed; no residual verdict is consumed. Kit bytes are
never edited after the first run.
