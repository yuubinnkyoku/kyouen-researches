# kit-20: strip-newband m55/m56 frontier first-contact, ladder continuations to depth, rule-v2 standing enumeration, first m=53/m=54 in-band windows, and the even-m z=3m+20 next-depth lifecycle rows (2026-11-27)

FROZEN PRE-DECLARATION census. Every binding candidate row was registered
(machine-derived from the kit-19 frozen future constants + derive-checked)
BEFORE the frozen official run of this kit, per the standing pre-declaration
protocol of the strip-newband kit series.

STATUS AT THIS PUBLICATION (wave A): registration, explorer generation and
derive_check are complete and published here. The official frozen
measurement run, the determinism battery, the audit runs and the tamper
battery are PENDING; this README will be updated in place at freeze with the
measured census and the honest-disclosure record. No measured value appears
anywhere in this wave.

## Provenance

- kit-19 frozen registration source: `research/experiments/strip-newband-m53m54-frontier-windows-evenlife-20261127/` (final wave commit fe78f9ba, frozen .out sha256 `12277fd483aac7dfed4e3b687f3eb2433de44706d74377b08cd4c7db7acd623f`, kit-19 explorer sha256 `9a010e433d030f7a83672db0d9f50d3478152d516e4db17034b7a272ccf398f6`, future_slice_registration_constants, 34 items).
- Engine block: byte-clone of the series engine (`engine_block.py` sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`, embedded ENGINE_BLOCK pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`, asserted in-explorer at run time and re-asserted by this build against the generated kit-20 explorer).
- This kit-20 explorer: `explore_m55m56_frontier_windows_evenlife.py` sha256 `b88bf7335c849d9c3f6f2ddbb7ca10aa765725103b78fbeea93155f9f2e818f3` (392,925 bytes).
- derive_check: `derive_check_kit20.py` (engine-free, K0832 closed form only) 3,725 checks DERIVE-PASS, 0 fails, run against the generated explorer before publication.
- audit: `audit_kit20.py` 20 gates, data-driven recomputation from the embedded engine block; PENDING against the frozen .out (no .out exists yet at wave A).

## Registered census for this kit (49 rows, engine-free, NOT measured here)

- 28 ladder next-depth one-past/birth rows for m=19..m=32 (one depth beyond
  the kit-19 measured depths: m19/m20 birth now at z=81/82, new
  series-deepest), machine-derived from the kit-19 frozen future constants;
  rule-v2 stack lists included wherever co >= 2m, composed FRESH for the
  kit-20 seats.
- Frontier 42nd/43rd datum candidates (FIRST-EVER m>54 rows if measured):
  m=55 @ z=109 (R=165) {55,56} @S=111 UP 2v0 (collapse v(111,109,165)=0) /
  m=56 @ z=110 (R=167) (56,56) @S=112 UP 2v1 (collapse v(112,110,167)=1);
  z*(m)=2m-2+(m mod 2) per K1268, derive_check double-checked.
- First m=53/m=54 in-band window sweeps: m=53 z{97..104}, m=54 z{98..105}
  (both NOT strip-covered).
- Even-m z=3m+20 lifecycle continuation rows (m=14 z=62 / m=16 z=68 /
  m=18 z=74), NON-BINDING continuation registered contingent on the kit-19
  z=3m+18 outcomes (3/3 EXACT there): template stick {m,2m+20} @S=3m+20
  DOWN 0v2 + NEW {m,2m+22} @S=3m+22 UP 2v1 + exact-mimic shadows
  (splits(2m+20,m) + splits(2m+22,m)) + trio {m,m,m} conform (absent) at
  z=3m+20.
- k0832 battery: 2,354 literal triples (2,290 kit-19 carried + 64 new;
  every new literal satisfies closed == vC == vO before the freeze;
  derive_check asserts the count and the v/vC/vO equality for the new
  literals against the kit-19 published explorer).
- Published anchor rechecks: 1,935 spots (1,662 kit-19 anchors
  byte-carried + the 273 kit-19 published census separation spots
  first-anchored here), verbatim published values, recompute gates in the
  audit.

## Registration for kit-21 (engine-free, NOT measured here)

34 future constants registered in the to-be-frozen .out section
future_slice_registration_constants:
- 28 ladder next-depth one-past/birth pairs for m=19..m=32 (one depth
  beyond this kit), rule-v2 stack lists included wherever co >= 2m,
  composed FRESH for the kit-21 seats.
- Frontier 44th/45th datum candidates: m=57 @ z=113 {57,58}@S=115 UP 2v0
  (collapse v(115,113,171)=0) / m=58 @ z=114 (58,58)@S=116 UP 2v1
  (collapse v(116,114,173)=1); z*(m)=2m-2+(m mod 2) per K1268,
  derive_check double-checked.
- In-band window sweep proposals: m=55 z{101..108}, m=56 z{102..109}
  (both NOT strip-covered).
- Even-m z=3m+22 continuation proposal (contingent on this kit's z=3m+20
  outcomes, NON-BINDING) registered.

## Honest disclosure (build record; measurement disclosures follow at freeze)

1. Single-owner declaration: this kit was declared single-owner in
   `research/log/2026-11-27-strip-kit20-m55m56-single-owner-declaration.md`
   before generation; no other lane is building kit-20.
2. Generation was machine-performed by a count-asserted transform
   (make_gen_kit20.py over gen_kit19.py, 166 fail-closed pairs) with every
   build gate green before the explorer was accepted: battery 2,354 /
   anchors 1,935 / K21_FUTURE 34 items / engine pin re-asserted. Three
   transform defects (an old_names K20_ANCHORS misdirection, a docstring
   paren omission, a LITS old/new 2-pass ordering slip) were each caught
   by the fail-closed pair counters and fixed before acceptance; the
   accepted explorer is the published bytes above.
3. Memory guard: the generator's anchor spot-check loop now clears the
   H_canonical lru_cache between spot-checks; the first generation attempt
   died at rc=137 (OOM) without it. H_canonical is a pure function, values
   are unchanged by the cache clear, and this is disclosed here.
4. FRESH seat labels: the frozen kit-19 prediction texts registered here
   carry FRESH seat labels (kit-19 received FRESH from kit-18 and emitted
   FRESH); freshness is ASSERTED in derive_check_kit20.py and in audit
   G14's seat checks. The cand texts are carried byte-verbatim per the
   series convention.
5. derive_check_kit20.py reads the kit-19 published explorer (not
   re-published in this kit dir) for the carried-battery comparison (same
   practice as kit-15..19).
6. Hand-typed pins forbidden: every pin in this README was
   machine-extracted from the frozen files or the build logs.

## ASCII gate and no-claim caveats

- All published files in this kit are pure ASCII (verified with a
  non-ASCII byte scan before push; a hard gate at push assembly). The log
  file keeps the established ASCII-normalized style.
- This kit makes NO universal claim. Finite observations only (and none
  yet at wave A). The frontier parity count, the rule-v2 shadow
  observations and the even-m lifecycle template are observation counts,
  not laws. The standard 11x11 empty board, all 19 central-reply roots,
  the two-stone root {60,27}, the third-move {100,108}, S2, and closure
  classes 1/2/4 remain UNKNOWN at all times. No verdict is consumed.
  Nodes and shape counts are bookkeeping. No K-slot claim is made.
