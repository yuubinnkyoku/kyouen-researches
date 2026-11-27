# kit-17x: independent blind second census of the kit-17 registered rows (m49/m50 frontier cross-check)

## What this is

An independent second census of the 49 rows registered for kit-17 (the
`strip-newband` m=49/m=50 frontier + m=47/m=48 windows + m19..m32 ladder
next-depth + even-m z=3m+14 rows), built and measured by a fresh harness in a
separate lane session, cross-checked against the published kit-17 frozen output
(record of record: commit `f90d5d5e`, kit dir
`strip-newband-m49m50-frontier-windows-evenlife-20261126/`).

Registration authority: the published kit-16 frozen `.out`
(sha256 `85c04e43...`, commit `f997daca`), section
`future_slice_registration_constants` (34 items) plus its window proposals
(z in {85..92} / {86..93}) and the even-m z=3m+14 continuation. Nothing was
registered from any unpublished source.

## Pins

| file | sha256 |
| --- | --- |
| engine_block.py (published byte-clone) | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` |
| engine startup pin | `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92` |
| census_kit17x.py | `3abfc53c2f2d0259478a1fd15fb0e0f2a86cffc8686c513dcbc46989c8b1290d` |
| census_kit17x.out (frozen) | `813e7e8b5321d24e0bf5c8d102671036d2c3fc48df99ac0dbfae511ed9b53305` |
| audit_kit17x.py | `e3da60b8fbfcf702ce4f2393f3678471f4a49fb9a9356ebcf5658f59ab577901` |
| published kit-17 .out (cross-check target) | `420d1c83350e5a1c38d1282fa974a3e91d3e50ddd26d82b4c069ea82c4367d95` |

## Method and independence statement

- Row semantics were independently reconstructed and then validated: the
  harness reproduced ALL 49 published kit-16 rows (shape counts and separation
  content, order-independent) BEFORE any kit-17 row was measured.
- The harness implementation is fresh (nested-loop enumeration, no `parts()`
  recursion, no transform of any published explorer). The kit-17 explorer source
  (`explore_m49m50_frontier_windows_evenlife.py`) was never read by this lane;
  only its published frozen `.out` was used, after this census was frozen, as
  the cross-check target.
- Engine is the published `engine_block.py` byte-clone (SSOT), with per-S
  `H_canonical.cache_clear()` (memory-safety, values unchanged).
- Determinism: the published `census_kit17x.py` re-run reproduced the frozen
  census content identically (49/49 rows, 211 separations, same shapes/R).

## Results (all finite observations)

- **49/49 census rows match the published kit-17 frozen `.out` exactly**
  (shapes, R, and every separation X/S/value/collapse/direction,
  order-independent content equality). Total separations 211 = published 211.
- **Frontier 36th datum: m=49@z=97 R=147: {49,50}@S=99 UP 2v0 EXACT**
  (independently confirmed; parity scaffold observation count 38/38, m=13..50).
- **Frontier 37th datum: m=50@z=98 R=149: (50,50)@S=100 UP 2v1 EXACT**
  (independently confirmed).
- Windows m=47 z{85..92}, m=48 z{86..93}: 16/16 CLEAN (0 separations each).
- 28 ladder next-depth rows (m19..m32 one-past + birth): all registered
  predictions FULL HIT in the independent census.
- Even-m lifecycle z=3m+14 (m=14 z=56, m=16 z=62, m=18 z=68): 3/3 EXACT
  (stick {m,2m+14} DOWN 0v2 + NEW {m,2m+16} UP 2v1 + rule v2 splits);
  trio {m,m,m}@S=3m CONFORM 3/3.

## Independent audit (fresh implementation, 9 gates)

`audit_kit17x.py` re-implements the cross-check fail-closed, recomputing the
published kit-17 battery (2,162 literals), anchors (1,210 spots), the census
comparison, windows cleanliness, registration provenance (binding texts
byte-verbatim in the kit-16 frozen future constants), and binding hit-check:

```
G0 kit-17 sha PASS   G1 engine gate PASS   G2 battery PASS (bad 0)
G3 anchors PASS (bad 0)   G4 census cross-check PASS 49/49
G5 windows PASS (16 clean)   G6 provenance PASS   G7 binding hits PASS (44)
G8 census totals PASS (49 rows / 211 seps)     AUDIT-PASS
```

Tamper battery 3/3 fail-closed: T1 battery literal flip -> G0+G2 FAIL,
T2 frontier separation value flip -> G0+G4 FAIL (48/49),
T3 anchor published_value flip -> G0+G3 FAIL.

## Honest disclosure

1. Two hand-typed 64-hex pin constants in this lane's own scripts were wrong
   (a 65-character kit-16 sha in `audit_kit17x.py`, and a mistyped pin in
   `census_kit17x.py`). Both were caught by this lane's own fail-closed gates
   before publication and fixed by machine extraction
   (`sha256sum` -> regex substitution, no manual typing). This re-confirms the
   standing rule: never hand-type pins.
2. This census was built while the kit-17 builder lane was still running. The
   builder lane's frozen `.out` (4 byte-identical determinism runs, sha
   `420d1c83...`) was compared only after this census was frozen; the builder
   lane published kit-17 itself (waves A/B/C, `d14a89bb`/`2e949ac1`/`f90d5d5e`)
   and remains the record of record. This kit is the independent second census.
3. Row semantics were reconstructed with reference to the published kit-16
   explorer source (published SSOT, commit `f997daca`); the enumeration code is
   fresh and was validated against all 49 published kit-16 rows first.

## Claims

Finite observation only. No universal claim is made from the parity scaffold,
rule v2 shadows, ladder or lifecycle templates. Verdict NOT consumed. 11x11
empty board, all 19 central-reply roots, the two-stone root {60,27}, third move
{100,108}, S2, closure classes 1/2/4: UNKNOWN throughout. K slot not claimed.
