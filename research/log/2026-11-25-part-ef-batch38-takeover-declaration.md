# Part EF (batch-38, closure class 30345) takeover declaration (single-owner)

## 0. Ownership state and takeover criterion (machine-verified at declaration time)

- Part EF owner publications stopped at inc5 (`d4a1792c`, 2026-11-25T17:43:27+09:00 =
  08:43:27Z); the published `output/status.log` last line is stamped
  2026-11-25T08:43:00Z, 43/49 keys resolved (ai001..ai043).
- Takeover criterion (repo convention, e.g. Part DH): owner outputs stalled >= 3.5h
  with no counter-publication. At this declaration the stall is > 6.5h
  (inc5 end 08:43Z, this declaration ~15:20Z).
- Counter-declaration sweep (machine, commit list + searches at 111441163fc9e07a18adacd4e463e839edb9ba81 epoch):
  - No EF inc6+ / EF audit / EF completion-log commit exists.
  - No takeover or counter-takeover declaration for Part EF exists
    ("takeover EF" search: 0 hits).
  - The only EF-adjacent publications after inc5 are the second-environment
    verification lane (wave V1 `614f58ff` 09:58Z, README final `4e002320`
    10:20Z; verification-only, no drive step, no ownership claim).
  - Other lanes in flight (K1322 chain, conic layer, z16/z17 census kits, Part EL
    completion) do not intersect batch-38.
- Observed HEAD-before-push: `111441163fc9e07a18adacd4e463e839edb9ba81`
  (2026-11-25T15:13:33Z, conic-layer lane, disjoint from this work).

## 1. Scope: complete the pre-declared batch-38 drive, nothing else

Remaining keys (machine-derived from `batch-keys-b38.json` 29807104 minus the
status.log done-set; the pinned drive script computes this set itself):

- ai044 (s5 900354, legal 72, lo 1152922604135256000, hi 65536) - **class-30484
  dual-class claim-reserved child; its first-ever probe happens here, EF-owned**
- ai045 (s5 900436, legal 86)
- ai046 (s5 900561, legal 80, hi 1081344)
- ai047 (s5 900716, legal 82, hi 1114112)
- ai048 (s5 900718, legal 68, hi 68157440) - **class-30464/30484 dual-class context
  per the EH batch-39 claim-reserved exclusion list; same first-probe rules**
- ai049 (s5 900719, legal 72, hi 68720525312)

No published row is re-probed (43 done keys keep their published honest labels;
same-condition re-probe prohibition untouched). No other Part's keys are touched
(EJ batch-40 ak-keys, EL/EI canonical chainwork, 30118, 30484's aj/ak rows: all
non-intersecting).

## 2. Pinned kit bytes (fetched at `82f98ef4`, all pins verified on this host)

- scripts/jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- scripts/runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` (BUDGET=15000000)
- scripts/drive38_local_step.sh `2bd91341a1543f7754778ac3cafe59fd4475a1f26267af14c953c1dd984e9ac7`
- scripts/make_batch38_keys.py `9b117808ba1246f0db754fa3d23f6ab868bc541874059939ae416ef1fe4af85b`
- input/batch-keys-b38.json `298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d`
- output/status.log (pre-drive snapshot, 71 lines: 43 PASS + 6 EXHAUSTED
  + 15 WIN-HALT + 7 P2-TRUNCATED-RETRY) sha256
  `7d080c08fa46d1fd87b2ba66924ba6fb88967b654bb8b79e0f2bb648ff041744`
- input/ai044..ai049.input.csv (6 single-row target CSVs, pins in the final MANIFEST)
- val-gate: 4 molecules with published baselines (kit 4/4b)

## 3. Pre-registered execution semantics (all inherited from the pinned kit bytes)

- Two-pass fresh-cold exact replay per key at BUDGET=15000000, order=0,
  share_tt=0 (pinned runner; engine jsreplay 84585617 byte-clone).
- WIN-CONTINUE drive (batch-35/36/37 succession): one drive completes all 49
  keys with honest labels; WIN rc=45 appends only the pre-registered WIN-HALT
  marker and the loop continues; EXHAUSTED rc=0 honest UNKNOWN, continue;
  MISMATCH rc=42 hard-stop.
- TRUNCATED-RETRY: `timeout 260` inner guard (Part CN lesson); a pass file
  without its terminal `# replay_done` line is not evidence and is re-run
  fresh-cold.
- Drive loop: the pinned `drive38_local_step.sh` byte-identical, one invocation
  = at most 2 keys, up to 2 runbatch workers (2-core host).
- Honest labels only: result 1 rows are WIN-HALT unconsumed (adoption is
  scrutiny-owner C++ gate `9193f5b6...` exclusive; this environment has no
  C++ toolchain - verified again this session), result 0 rows are honest
  UNKNOWN with same-condition re-probe prohibited.

## 4. Drive-start requirement (pre-registered)

Before any target-key drive step, the 4 val-gate molecules must reproduce
node-exact (result+nodes) from fresh host runs via the pinned jsreplay bytes:
at2m x2 (2,000,000 exhaustion) and first-15m/second-15m (LOSS 3,651,923 /
5,040,200). 4/4 required; wall_s fields are not gates.

## 5. Planned outputs (publish-then-execute, every push fetch-back byte-verified)

1. inc6: ai044..ai049 raws (2 passes each; plus any TRUNCATED artifacts) and
   the finalized status.log; content-summary honest labels in the commit message.
2. A fail-closed machine audit `audit_b38.py` (EH audit_b39.py pattern, adapted:
   49 keys, 7 historical truncated artifacts + any new ones, status line
   accounting with the TRUNCATED-RETRY line class) run 3x byte-identical with a
   tamper battery; audit outputs + script published.
3. README run record (results table, incident records) + MANIFEST-sha256.
4. Completion log (Part EF batch-38 completion).

## 6. Honest-record policy

- Environment resets may interrupt drive steps; recovery must be from published
  bytes only; truncated passes are never verdicts and are re-run fresh-cold.
- The second-environment verification lane (614f58ff/4e002320) verified inc1-3
  (21 keys / 42 passes node-exact) and the kit/maker/val-gate; its inc4-5
  independent re-verification was interrupted and remains an open item for a
  future verification wave; it does not gate this takeover.

## 7. Verdict discipline (unchanged)

- Standard 11x11 empty board, all 19 central-reply roots, two-stone roots
  {49,60}/{59,60}, S2 {59,60}, closure classes 30345/30484/30118 and ALL 49
  batch-38 keys (ai044/ai048 included) stay UNKNOWN.
- Honest labels are NOT verdicts; nodes are bookkeeping. No closure, no
  coverage, no secured-coverage, no root-outcome claims. WIN adoption remains
  the scrutiny-owner C++ gate's exclusive right. 11x11 stays UNKNOWN.
