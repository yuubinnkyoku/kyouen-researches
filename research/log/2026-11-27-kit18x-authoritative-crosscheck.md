# kit-18x authoritative cross-check against the published kit-18 frozen census (2026-11-27)

Lane: long-term lane (11x11), autonomous session; the user's PC was unreachable
this session (GitHub API publishing only). kit-18x had disclosed at publication
(commit 79bee22c) that its cross-check against the concurrent kit-18 build was
informational only, because kit-18 was not yet published; the authoritative
comparison against the published kit-18 record of record was left to a future
execution. kit-18 was published at HEAD 9ac8e079 (wave C, frozen census
sha256 c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba,
git blob d6e61bbf, 557,319 bytes). This Part closes that pending item.

## What was done

Fresh single-file comparison instrument
`crosscheck_kit18_authoritative.py` (published into the kit-18x kit
`research/experiments/strip-newband-m51m52-blind-second-census-20261126/`;
it does not read or reuse audit_kit18x.py, and the kit-18 explorer source was
not read). Fail-closed gates, in order:

- G0: sha256 pins of both inputs (published kit-18 frozen .out
  c3087285...; kit-18x frozen census .out 97b6ebef...) - fail-closed before
  any comparison;
- G1: 49 `*_row_record` sections in the kit-18 .out, 49 sections in the
  kit-18x .out, unique (m,z) keys in both;
- G2: the two (m,z) row sets are equal (28 ladder + 2 frontier + 3 evenlife +
  16 in-band windows);
- G3: for every row, the multiset of separations
  {sorted X, S, value, collapse, direction} is identical between the two
  censuses;
- G4: total separations 241 in each;
- G5: per-row separation counts identical.

Inputs were fetched from raw.githubusercontent.com at HEAD 9ac8e079 and
byte-verified against the pins before the run; the kit-18 .out git blob sha
d6e61bbf was additionally verified via the authenticated contents API listing.

## Result

CROSSCHECK-PASS (rc=0, 11/11 gates): **49/49 rows and 241/241 separations
identical** between the published kit-18 record of record and the frozen
kit-18x blind second census, including the frontier 38th/39th datum
(m=51@z=101 {51,52}@S=103 UP 2v0; m=52@z=102 (52,52)@S=104 UP 2v1, both
EXACT), the m49/m50 in-band windows (16/16 clean) and the even-m z=3m+16 rows.
This upgrades the previously disclosed informational cross-check to an
authoritative published-vs-published comparison, in both directions: the two
independent implementations measured the same registered rows from the same
published SSOT (kit-17 frozen .out) and agree on every finite observation.

Output: `crosscheck_kit18_authoritative.out`
(sha256 7ae00f47591a07ec129b0bd78275a55f1a018a5fee4f99322072e71a80144b69,
per-row reports with separation counts and match flags).

## Verification

- Determinism: 3 runs byte-identical output.
- Tamper battery (scratch copies, deleted after the battery):
  - T1: byte-edit of a separation value in a reserialized scratch kit-18 .out
    with the pins updated to the scratch shas -> G3 FAIL at row (51,101),
    rc=1 (comparison logic itself is fail-closed, not only the pin gate);
  - T2: content flip without repinning -> G0 fail-closed before comparison;
  - post-battery clean control re-run: rc=0, byte-identical output.

## Honest disclosure

- This is a fresh comparison implementation, not the "gate added to
  audit_kit18x.py" variant that the kit-18x resume note suggested; the
  authoritative result is equivalent (published-vs-published, pinned, machine
  compared) and the choice is disclosed here.
- Single implementation of the comparison (one lane, one script); the two
  censuses being compared are already independent of each other.
- kit-18x future constants were NOT read for this Part; kit-19 registration
  remains the kit-18-owning lane's next step.
- Everything compared is a finite observation. No universal claim is made
  from the parity scaffold 40/40, rule v2 shadows, or the even-m template.

## Status guard

Nothing here claims, implies or consumes any verdict. The standard 11x11 empty
board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root {60,27}:
UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN
unless a published Part says otherwise. Verdicts are never consumed by census
or cross-check Parts.
