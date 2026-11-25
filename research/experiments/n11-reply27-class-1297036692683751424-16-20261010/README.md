# 11×11 reply27: 対象S4 classの独立境界確認と段階的S5 probe

## 目的と現在の結論

開始時の監査済みmainは `154f3b7a67b97e13acbaee8b04dc74ddca728d19`。対象S4 class `(1297036692683751424,16)` の完全なcanonical S5 child集合108局面を独立geometry実装で再生成し、保存cache・raw replay・S6/S7 evidenceと突き合わせた。

probe後のpush直前fetchではmainが`a89eecba5870f8e1743fab2b98f7fbb550bdc490`へ4 commit進んでいたため、reply27と無関係な変更をfast-forwardした。この4 commitは対象solver、K0355、reply27 frontierを変更していない。今回の成果commitはこのmainを親として作成する。

対象classは、S5 child `(1297036692683751424,67108880)` の直接exact WINにより **WIN** と判定した。境界はLOSS 9 / WIN 1 / UNKNOWN 98。WIN childは独立geometryでsafe・canonical・legalな子と確認した。これは元の先手固定視点でのS4 OR判定である。9件のLOSSがcache由来かraw由来かはWIN witnessの判定に影響しない。

そのWINを得た後、残る第三手 `{100,108}` を同時に覆う低未確定数の別class `(1188950301626859520,536870912)` を調べた。child `(1188950301626859552,536870912)` は15M-node exact LOSSだが、このS4 classはLOSS 11 / UNKNOWN 98のままUNKNOWN。従って、このLOSS単独では第三手被覆は増えない。

全frontierはS4 LOSS 31 / WIN 272 / UNKNOWN 3,081。secured third movesは117/119、残りは `{100,108}`。整数最小追加class数1、有理LP双対1のまま。`{60,27}` rootと11×11空盤はUNKNOWNである。

## 実行量と新しいexact結果

既存の監査済みsolverをfresh process・1 worker・180秒watchdogで実行した。source `cpp/solvers/kyouen_dfpn_root.cpp` のSHA-256は `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`、solver binary `.local/n11-independent-audit-solver.exe` は `ac8f4931e4c81bd06ba1622844933962134f663d970885c2990fbb96a167677a`。実行オプションは `--n=11 --memo=22 --exact-order=count`。

合計14 probe（9件×2M、5件×15M）、9 distinct S5 positions、総計67,339,676 nodes。10回はbudget上限まで到達してUNKNOWN。新しく得た直接raw exactは次の4件である。

| S5 key | 結果 | legal手数 | budget | nodes |
|---|---:|---:|---:|---:|
| `(1297036692683751424,67108880)` | WIN | 81 | 15M | 14,920,591 |
| `(10448351135500599296,536870912)` | LOSS | 83 | 15M | 3,240,574 |
| `(1224979098645823488,536870976)` | WIN | 84 | 15M | 9,611,717 |
| `(1188950301626859552,536870912)` | LOSS | 87 | 15M | 6,566,794 |

exact判定に使った総node数は34,339,676。全raw input/output/log、probe summary、source hash、各S4→S5 geometry照合、cache merge receiptを同じ実験領域に保存した。最初の8件は各2MでUNKNOWN、その後に選んだ4件を15Mまで段階的に処理した。最後のS4 classについても、2M UNKNOWNを同一keyの15M再試行前にraw/S6/S7再監査した。

実行履歴sourceは2 snapshotに分かれる。最初の2M pilotと最初の15M target probeは開始mainにある`history.json`（SHA-256 `1ed1f0f4d94417ab1b81ec6ddbe81cbeaef0596a0b62db9929a7f3f794d58791`）を使い、後続probeは作業領域に存在した更新版（SHA-256 `212ce320b141ad2a322b13f788a0d60ba31d594860768b5de7d578883bb9bd3e`）を使った。両者を`input/`へbyte-exactで保存し、`output/probe-history-snapshots.json`で各run summaryへ対応付けた。更新版の原本は変更していない。

二つのS5 WINについて独立terminal-only minimaxも行ったが、各30,000状態で上限に達しUNKNOWN。独立終局までの証明DAGは完成していない。したがって、直接raw solver結果はsolver-trusted exactであり、独立checkerによる完了証明とは区別する。既存cacheにはcache-only evidenceが含まれるため、frontier全体も全面的な独立証明DAGではない。

## 幾何・raw履歴・S6/S7監査

- 対象108-child集合は独立Boardで完全再生成し、key set SHA-256 `633595fe66774ed7b4d9573e4951c0dfc038ba469d2d6778d8ba61d03d67dfa1` を記録した。
- 保存済みS5 cacheの開始時5734 rowsから直接raw exactをconflictなしで追加。途中5737 rows、最終5738 rows（WIN 158 / LOSS 5,580）。最終cache SHA-256はreportとmerge receiptに記載。
- 最終raw auditは全11,915 CSVを検査。対象S4境界でverdict conflict 0、same/higher-budget UNKNOWN 0。follow-up candidateでもconflict 0、15M以上UNKNOWN 0。
- 対象classのS6 boundaryは5,226 canonical keys。raw S6 exact 16、cache S6 exact 18、S7 raw/cache intersection 0、S6/S7から導くS5結果0。
- follow-up classのS6 boundaryは5,392 canonical keys。raw S6 exact 16、cache S6 exact 17、S7 raw/cache intersection 0、S6/S7から導くS5結果0。
- budget-zero projectionはexact evidenceに使っていない。S7 LOSSひとつからS6 WINへ反転させる伝播もしていない。

S5 LOSSはraw solverが直接返したoriginal-player固定視点の判定として統合した。S4再分類は常にS4 OR（子に1件でもWINならWIN、全子LOSSならLOSS、それ以外UNKNOWN）。S5 AND則やS6/S7則で手番視点を反転していない。

## 次に探索する局面

次候補S4 `(1188950301626859520,536870912)` は coverage `{55,65,100,108}`、完全境界109 child、LOSS 11 / UNKNOWN 98。次の最小legal-count childはS5 `(3494793310840553472,536870912)`、legal手数88。最終raw-history監査でdispatch-ready 98 childの一つ、same/higher-budget UNKNOWNなし。S6/S7 auditからこのchildの結果は導けない。これは次の候補であり、まだdispatchしていない。

## 再現・検査

コマンドはrepository rootから実行する。raw-history auditorは保存済みの `research/experiments` と `.local` のCSV corpusを読む。`.local` のsolver binaryは実験環境の入力で、再配布物として仮定しない。入力、raw output、logはGit管理されるこの実験フォルダに保存してある。

```powershell
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/preflight.py
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/layer_preflight.py --preflight research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output/preflight.json --raw-s5-audit research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output/raw-s5-history-final-target-after-followup.json --out $env:TEMP/target-layer-recheck.json
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/merge_followup_s5_loss.py
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/reclassify_frontier.py --cache research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output/current-exact-s5-after-followup-loss.cache --compare-to-cache research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output/current-exact-s5-latest.cache --out $env:TEMP/frontier-recheck.json
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/build_report.py
```

`preflight.py` and `reclassify_frontier.py` compare against the frozen 3,384-class geometry. Exact cache/report output hashes and every artifact's size/SHA-256 are in `output/artifact-sha256.json`. The manifest intentionally excludes itself. The final repository knowledge checks are recorded by the commit that includes this experiment.

## 主なartifact

- `output/report.json`: probe件数、node数、exact結果、cache/frontier、監査根拠をまとめるreport。
- `output/current-exact-s5-after-followup-loss.cache` と `output/followup-s5-cache-merge.json`: final cacheとdirect raw LOSSのgeometry/hash-bound merge receipt。
- `output/frontier-reclassification-from-start-final.json` と `output/frontier-reclassification-after-followup-loss.json`: 5734-row開始cacheからの4件のS4 UNKNOWN→WIN遷移、および追加LOSS後の全frontier再評価。
- `output/raw-s5-history-final-target-after-followup.json`、`output/followup-after-loss-raw-history-audit.json`、対応する `saved-layer-*.json`: raw historyとS6/S7境界監査。
- `output/independent-win-check.json`、`output/candidate-s5-win-independent-check.json`: geometry照合と30K-state independent minimax上限。
- `output/artifact-sha256.json`: 実験source/input/raw/outputのSHA-256 inventory。
