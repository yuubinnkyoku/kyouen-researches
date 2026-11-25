# 2026-11-25 main tip mass-deletion incident (commit d0755ecc) - report and recovery anchor

Report by the 11x11 long-term lane (scheduled autonomous run). This is an
infrastructure incident report, not a research result. No research claim in
this document. Status of the standard 11x11 question and all related roots
and classes is unchanged: UNKNOWN. No verdict is consumed anywhere in this
report.

## 1. What happened (observed from public main history only)

Timeline (all times 2026-11-25 UTC, from commit author dates):

- 15:55:58Z c7cbd718  Part EM wave F (b38loss24 adoption README/MANIFEST/completion log) published. Repo tree normal.
- 16:00:57Z e5cc9f8e  K1325 wave 3 (official outputs + detcheck.json) published. Repo tree normal.
                     e5cc9f8e is the LAST COMMIT WITH THE FULL KNOWN-GOOD TREE.
- 16:02:12Z d0755ecc  Commit message: "PG(2,8) maximal cap orbits: independent
                     verification PASS (56 checks; Schreier-Sims order, 12 extra
                     caps => exactly 3 orbits, independent census); fix stale
                     probe-orbit label". Actual effect: the main tree was
                     replaced by (almost) ONLY the pg2q8-cap-game experiment.
                     The message does not mention any deletion.
- 16:04:22Z e3a2f749  K1325 lane wave 4 (K item + completion log) published
                     additively ON TOP of the wiped tip, apparently without
                     noticing the wipe.

## 2. Evidence (machine-collected on 2026-11-25 ~16:05Z)

Tree at e5cc9f8e (parent of the wipe commit):
- Root: 26 entries, including AGENTS.md, README.md, LICENSE, Main.lean /
  lakefile.lean / lean-toolchain (Lean formalization), CMakeLists.txt, cpp/,
  Kyouen/, certificates/, docs/, results/, scripts/, rust/, tests/, tools/,
  output/, release-assets/, .github/, research/ etc.
- research/experiments/: >=1000 entries (GitHub contents API listing caps at
  1000; includes all n11 strip / closure-class / Part kit dirs).
- research/knowledge/: README.md (1,136,882 B), SCHEMA.md, VOCABULARY.yaml,
  items/ >=1000 K-items.
- research/log/: >=1000 entries.

Tree at d0755ecc (the wipe commit), full recursive walk:
- Root: only research/.
- research/experiments/: 1 directory (pg2q8-cap-game-20261125) with 70 files
  total (incl. independent/, independent_conic/, independent_orbits/, output/,
  scripts/, README, report).
- research/knowledge/items/: exactly 1 file (K1324-pg2q8-maximal-cap-orbits.md).
- research/log/: exactly 1 file (2026-11-25-pg2q8-maximal-orbits.md).
- AGENTS.md, research/knowledge/README.md, SCHEMA.md, VOCABULARY.yaml,
  certificates/, cpp/, tools/, docs/, results/, scripts/, rust/, Kyouen/,
  tests/, .github/ and every 11x11 experiment/kit/certificate/cache/log/K-item
  published before 16:02Z: absent from the tip tree.

So commit d0755ecc deleted on the order of tens of thousands of files
(the pre-wipe repo tarball measured earlier today: 65,779 files / 3.4 GB),
while adding only its own pg2q8 round-19 artifacts (its own K1324 item was
also modified: 3420 B -> 4284 B).

## 3. Nothing is lost

All deleted content remains fully retrievable from git history, because the
wipe is a normal commit on top of intact history (no force-push, no orphan).
Verified byte-exact raw-CDN fetches at commit e5cc9f8e at report time:

- AGENTS.md                                                  sha256 f8b4f78f43ab1fc7d398e045795513879cafcd1bed8645e9b4d239a651d180d9 (3,993 B)
- research/knowledge/README.md                               sha256 fee4f5d78260ba0b1818f29bd2122e6bf8db64eb93a8bab42ed34a8e7cb7a1db (1,136,882 B)
- research/log/2026-11-25-part-em-b38loss24-adoption-completion.md
                                                             sha256 e05a8d2b18073f8a8d42b908a37a2988ea44f595ea06969cc65aa021eb469356 (10,553 B)
- research/experiments/strip-z17-min12-20261125/official_runs/run1.out  HTTP 200

Rule for all lanes until recovery: ALWAYS fetch historical bytes by commit
sha (e.g. e5cc9f8e or the specific publication commit), never by branch path.

## 4. Interpretation and classification

- Observed facts are as above. Attribution (who/what produced d0755ecc and
  whether the deletion was intended) is not determined by this lane; the
  mismatch between message and effect strongly suggests an accident of the
  pg2q8 lane (e.g. a tree/`git add` mistake), but this is inference, and the
  decision belongs to the repo owner.
- The commit that wiped the tree carries no policy note, and AGENTS.md (the
  operating rules, also deleted) describes no cleanup/reset policy: items/ is
  the SSOT, history is kept, "新しい研究記録は独立したlogとして追加する".
- Nothing about this incident changes any verdict or exploration state: the
  canonical chain (head merged cache b5be64e6..., 6,737 rows WIN158/LOSS6579),
  s5 verdict cache, certificates, and all probes live in history bytes and in
  the published pins, so the 11x11 lane itself is not invalidated. However,
  ALL path-based (non-sha) fetches of pre-16:02Z artifacts now 404.

## 5. Actions taken by this lane

- Report only. NO restore, NO revert, NO further publications to main besides
  this log. Rationale:
  (a) A restore means re-creating tens of thousands of files / multi-GB via
      single-file push APIs - infeasible from this toolset, and a partial
      restore would create a mixed tree that confuses other lanes further.
  (b) If the wipe was an intentional owner action, overriding it would be
      wrong; if it was an accident, the owner can revert in one step.

## 6. Recommended owner-side recovery (choose one)

1. git revert d0755ecc  (from a current local clone, then push). This is a
   single commit that re-adds the entire pre-wipe tree. Files added after the
   wipe (K1325 item/completion log at e3a2f749, this incident log) are new
   paths and do not conflict.
2. Or force-push the tree of e5cc9f8e (equivalent result, discards the wipe
   commit; not preferred since history stays cleaner with revert).
3. After recovery, re-run the AGENTS.md post-merge checks
   (uv sync --locked; uv run --locked python tools/knowledge/check.py; ...).
   Decide explicitly whether the deletion was intended before reverting.

## 7. Notes to all parallel lanes

- Before any further publication to main, re-check the tree state
  (e.g. existence of AGENTS.md at the tip). The K1325 wave-4 push (e3a2f749)
  already landed on the wiped tip; if the owner reverts, that commit survives
  as an additive commit and stays consistent.
- Do not treat the current tip's knowledge/ contents (K1324 alone) as the
  knowledge base; the SSOT is the pre-wipe tree pinned at e5cc9f8e.
- Do not initiate new declarations (e.g. batch-41 on class 30345, EJ
  takeover checks, C++ gate WIN adoptions) until the tree is recovered or the
  owner declares the wipe intentional - new kits would reference a broken SSOT.

## 8. Guarantees (unchanged)

Standard 11x11 empty board, 19 central-reply roots, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, 16371/20421/34908, 30118, 30345,
30484: all UNKNOWN at every point. Verdicts unconsumed. This incident report
makes no claim about wins, coverages, secured coverage, or node counts.
