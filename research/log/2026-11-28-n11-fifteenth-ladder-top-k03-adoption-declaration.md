# Declaration: n11 fifteenth ladder-top k03 WIN-row canonical adoption (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
the adoption maker runs. Any parallel lane must not adopt or audit the
key below until this Part's completion log appears.

## Scope

Canonical adoption (k03-only) of the fifteenth class 5804 k03 WIN row
`6053400849139367936:128` (class 5804, s5_index 212536, legal 92,
WIN(1) nodes 3,364,655 @15M), two-pillar COMPLETE as of completion
log `e805ee23` (jsreplay replica cold pair + C++ scrutiny gate
GATE-PASS `92,15000000,1,3364655` + third-impl CORROBORATION-PASS
result 1 expansions 3,906,063 x2 identical; kits published at commit
`ea3f482f`). Base head of record `b5f322dd...` (6,898 rows WIN 216 /
LOSS 6,682; k03 verified fresh/absent from the head by the
re-escalation Part). Declaration HEAD pin:
`e805ee23648b4d0a663af2890804c60743bb7444`.

## Method

Fresh maker `make_adoption_fifteenth_k03.py` (machine-adaptation of
the published fifteenth k01 adoption maker
`make_adoption_fifteenth.py` sha256 `cea18c48...`, single-row
structure identical), fail-closed G0-G6:

- G0 pins: merger `s5_union_merge.py` `90711961...`, policy
  `s5_evidence_policy.py` `78655e94...`, quarantine
  `results/n11-s5-evidence-quarantine.json` `81d23160...`, BASE
  head.cache `b5f322dd...` (288,955B), gate source `9193f5b6...` +
  headers `5976933d...`/`2e36d694...` (all byte-fetched and
  sha-verified this session).
- G1 live re-run of the published C++ gate runner on a scratch kit
  copy (expected `92,15000000,1,3364655`).
- G2 re-parse of the three pillars (replica raw pair byte-identical
  `58f2ad9d...` x2, gate pair, third-impl pair + summary cross-check,
  TI expansions 3,906,063).
- G3 freshness vs BASE (6,898 rows WIN 216 / LOSS 6,682; k03 absent)
  + WIN/LOSS conflict scan.
- G4 quarantine + canonical safety per s5_evidence_policy.
- G5 increment build; G6 merger x3 byte-identical; expected merged
  shape **6,899 rows WIN 217 / LOSS 6,682**, new head of record
  `merged-exact-s5-chain-plus-fifteenth-k03-20261128.cache`.

Pre-registered expected shape: rows 6,898+1, WIN 216+1, LOSS 6,682+0.
Maker run twice; kitout recursive diff must be clean. Tamper battery
fail-closed on distinct maker gates + clean control.

## Non-meaning

Adoption bookkeeping only: NO verdict consumed. The k03 WIN row is
cache bookkeeping, never a root/class verdict. The WIN-side
flip-census review is the declared follow-up Part (owner class union
to be derived from the frozen graph `54f9c364...`; caveat: shared-owner
pre-exclusion as measured in the fifteenth k01 reaudit, where the
naive owner-union prediction over-predicted flips [5601, 5804, 8675]
vs measured [5601, 8675]). Class 5804 is NOT complete (k02
`6052837899185946628:128` stays 15M UNKNOWN; parking/L50M only under a
fresh declaration). The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN. Nodes/expansions are bookkeeping,
never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The published fifteenth k01 adoption increment's header comment
  contains a stale node figure ("replica 15M cold pair WIN(1) nodes
  4,360,661" and "adopted node total 4,360,661" vs the row's actual
  12,803,283) - a machine-adaptation comment bug in the k01 kit's
  comment block only; the k01 data row (s5verdict,...,1,12803283) and
  the adoption manifest are correct and the head of record is
  unaffected. This k03 increment's comment block is written from the
  measured k03 values (3,364,655).
