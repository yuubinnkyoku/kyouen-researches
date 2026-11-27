# Part EP second-environment verification (epwin10 FIRST-EVER WIN canonical adoption) - 2026-11-25

Independent re-execution of the entire published Part EP chain from the
published bytes only, in a third environment (this run: Python 3.12.14,
Linux 6.18.35 x86_64), with no reliance on any local state from either
prior host.  Every conclusion of Part EP that is re-executed below
reproduced byte-identically.  This log asserts NO root verdict and NO
11x11 outcome: the standard 11x11 empty board and all 19 central-reply
roots stay UNKNOWN; verdicts remain unconsumed beyond the 10 adopted WIN
rows; nodes are bookkeeping.

## 1. Fetch provenance (publish-then-verify)

All inputs were fetched fresh from raw.githubusercontent at pinned commit
`94a68ab1` (EP wave F completion; every dependency and the EP kit itself
landed strictly before it):

* the 10 kit MANIFEST-sha256.txt files (EM/EN/EO/b33/EA/EK/b39/b38/EG/EP),
  giving 835 byte-pinned entries in total;
* all 835 kit-referenced files (one exception: the EN kit
  `declaration.md` does not exist on main - the EN kit's own README/audit
  treat it as the published log mirror
  `research/log/2026-11-25-part-en-cppgate-30484win4-declaration.md`,
  which was fetched instead; the EP maker resolves it through exactly
  that fallback);
* the 5 frozen reaudit dependencies of the refresh fork: frozen graph
  54f9c364..., update8 b658290a..., Board source 954d3a10..., policy
  78655e94..., quarantine registry 81d23160....

Authenticity of every fetched byte was machine-verified end-to-end
during re-execution (not by hand): the maker G1 re-hashes all 8
referenced kits file-by-file against their pinned MANIFESTs (en 34,
eo 37, b33 186, ea 61, ek 42, b39 178, b38 181, eg 88 entries), every
kit MANIFEST is itself sha-pinned by a maker constant, and the
refresh/extractor re-pin the frozen dependencies and both caches
(b5be64e6..., fd29a337...).  A 404-junk residue of the nonexistent
`declaration.md` (14 bytes) was deleted locally before running; see
honest note (a).

## 2. Re-execution matrix (all from published bytes)

| stage | result vs published pin |
|---|---|
| maker `make_increments_ep_win10_adoption.py` (efc40a0b...) | rc=0 PASS in 0.48 s (owner run record: 0.5 s); G0-G6 all-PASS; emitted increment `c245bc4c...` byte-identical to `output/increment-epwin10-20261125.cache`; emitted manifest `25d3abdf...` byte-identical to `output/increments-manifest.json`; rows=10 nodes=98,335,817 |
| merger `s5_union_merge.py` (90711961...) selftest | PASS (positive dedupe+sort; cross-file conflict reject; within-file conflict reject; malformed verdict reject; double-run determinism) |
| merger merge BASE(b5be64e6...) + increment, 3 runs | 3/3 rc=0, merged cache `fd29a337...` (6,747 rows WIN 168 / LOSS 6579) and audits `efbe25bc...` all byte-identical across runs and to the published pins |
| refresh fork `refresh_adoption_ep.py` (99d583c3...) | rc=0 PASS in 61.4 s (owner: 61 s); `refresh-summary.json` 5a1ff0c5..., `closure-classes.csv` fdd4e4b2..., `per-root-coverage.csv` 487a95c4... all byte-identical to the published reaudit outputs; unpublished-size-policy `probe-worklist.csv` regenerated at exactly the regen pin `7cd566bf...` (3,718,981 B) |
| extractor `compare_deltas_ep_adoption.py` (e28a6893...) | rc=0 PASS in 120.6 s (owner: 122 s); re-executed BOTH refresh forks byte-verbatim in isolated scratch trees (EM BASE + EP SCEN), byte-verified all eight outputs against the pins, and emitted `decomp-deltas-epwin10-adoption.json` byte-identical to the published `ce7974c4...` |

Key extractor stdout: `EP decomp OK: flips=20 caches=6737->6747 win=158->168
closure_left=[30484, 34908] greedy=36460->36643`.

## 3. Numeric independence confirms (published-bytes parse)

* `closure-classes.csv` exactly 805 rows; classes 30484 and 34908 both
  ABSENT (left the file; their s4_cost sets became fully known via the
  10 adopted keys); class 30345 row: rank 9, unknown_now 25, groups
  served 4.
* `refresh-summary.json` census: unknown 34,477 / excluded_now 43 /
  free_now 39 static; update8 frozen-baseline refresh resolved_count
  260, exactly 10 win_hit_groups all of s4 class 30354; joint greedy
  union 36,643 (the honest +183 tradeoff of consuming WIN labels).
* merged-cache accounting rows 6,747 WIN 168 / LOSS 6,579 (base 6,737 /
  158 / 6,579 + 10 WIN rows).

All equal the published decomp/README/knowledge values; no re-executed
number diverged anywhere.

## 4. Tamper battery (fail-closed, sha-change pre-asserted)

Every scenario asserts the tampered file's sha256 actually changed
BEFORE running the gate (the EL no-op-tamper lesson), then restores and
re-verifies clean:

* T-EP1 scenario-cache tamper: +1 on a single LOSS-row nodes field of the
  merged cache `fd29a337...` -> sha change asserted (`66c811f3...`),
  refresh fork rc=1 fail at `merged cache sha256 drift`; restored to
  `fd29a337...`.
* T-EP2 quarantine tamper: one trailing byte appended to the quarantine
  registry -> sha change asserted, refresh fork rc=1 fail at `quarantine
  registry sha256 drift`; restored to `81d23160...`.
* T-EP3 source-raw tamper: +1 on the nodes field of the b38 kit
  `output/raw/ai048.p2.out` -> sha change asserted, maker rc=1 fail at
  `kit sha drift (b38): output/raw/ai048.p2.out` (the MANIFEST pin layer
  catches a live nodes falsification, before any eligibility logic);
  restored, control clean maker re-run rc=0 byte-identical emission.
* T-EP4 merger WIN/LOSS conflict: a synthetic increment re-emitting an
  existing BASE LOSS key as WIN -> merger rc=1 `GATE FAILED: WIN/LOSS
  conflict at 135268368:536870912` with NO output file written (the
  first-ever-WIN-adoption chain's central safety property: a falsified
  WIN can never cross the union merger silently).

Post-tamper controls: clean maker re-run rc=0 and clean merge 3/3
byte-identical `fd29a337...` (the clean control audit differs from the
published `efbe25bc` only in the CLI input-path strings it records, the
known merger behavior; measured fields identical).

## 5. Honest notes

(a) The EN kit `declaration.md` fetch attempt left a 14-byte `404: Not
Found` residue file inside the local tree; the first maker run
correctly FAILED CLOSED on it (`kit sha drift (en): declaration.md`) -
the maker treats any present-but-wrong file as a drift, it does not
silently prefer the mirror fallback.  The residue was deleted and the
run repeated clean.  This is a working demonstration that the maker's
file-presence fallback cannot be turned into a bypass by planting a
file.

(b) This environment's raw CDN returned persistent 404 for full 40-hex
commit-sha URLs while serving the same paths at the short sha
(`94a68ab1`); the fetch driver fell back to the short sha, which
resolves to the identical commit and bytes.  All pins were verified
afterwards regardless, so the fetch path quirk affects nothing.

(c) The first T-EP1 tamper attempt selected its target line with an
endswith(',2') heuristic that matched no line (the CSV row ends with
the nodes field, not the verdict) - i.e. a no-op tamper.  The protocol
requirement that the sha change itself be asserted caught it
immediately (rc path: ASSERT-FAIL, no gate run), and the tamper was
re-issued with a proper verdict-field selector.  Same lesson class as
the EL sed no-op incident: a tamper test only counts when the tamper
was proven to happen.

(d) EP outputs remain single-published (no byte of the EP kit was
altered on main by this verification; re-execution wrote only to local
scratch and /tmp).

## 6. Guarantees

Part EP is now verified in a second, independent environment from
published bytes alone: the adopted 10 WIN rows' full eligibility chain
(two-pass fresh-cold node-exact source raws, C++ second-implementation
EN/EO gate audits, EG JS third-implementation corroboration, batch-keys
SSOT quadruples, freshness to BASE b5be64e6..., quarantine absence),
the deterministic union merge, and the complete reaudit/extractor delta
accounting all reproduce.  The standard 11x11 empty board stays
UNKNOWN; all 19 central-reply roots stay UNKNOWN; class 30484/34908
exclusion is derived scheduling bookkeeping from the WIN consumptions;
nodes are bookkeeping; no verdict beyond the 10 adopted WIN rows is
consumed anywhere by this log.

## 7. Resume

* The canonical head remains `fd29a337...`; every future adoption /
  refresh / extractor must re-baseline here (and now in a proven
  third-host-reproducible way).
* Part EQ (3rd C++ gate execution, 18 unconsumed batch-38 WIN rows of
  class 30345) completed in parallel (21/21 GATE-PASS, close-out
  697b50de) - their canonical adoption is the natural next Part, with
  this verification log's re-execution recipe (the dependency tree is
  fully fetchable from published bytes as demonstrated).
