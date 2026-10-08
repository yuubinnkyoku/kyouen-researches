# 11×11 探索前監査の予算結合修正（2026-10-08）

## 背景・修正範囲

11×11 reply27 の dual-tight s5 probe では、保存済み raw-history 監査と s6 監査を結合して局面を選ぶ。従来の `verify_dual_tight_probe_preflight.py` は、raw-history JSON に存在しない `requested_budget` を実行時の `--budget` から補っており、監査生成時の予算と実行時予算が一致したという記録を保証できなかった。

以下を `main` に直接修正した（branch / PR なし）。

- `audit_s5_raw_history.py` は正の探索予算のみ受け入れ、出力JSON自身に `requested_budget` を記録する。
- `verify_dual_tight_probe_preflight.py` は保存済み予算をそのまま比較する。後付けの代入を廃止し、旧 `requested_budget` 欠落監査は fail-closed とする。
- `prepare_dual_tight_probe.py` と `prepare_dual_tight_ready_subset_probe.py` は共通 `validate_audits` を実行し、完全な対象集合、cacheとtargetのSHA-256、同等以上予算の既知UNKNOWN、s6境界監査の照合を要求する。
- 同等以上の予算で過去にUNKNOWNだった局面は、判定結果としてではなく同予算での再探索対象からだけ除外する。WIN/LOSSには昇格しない。
- `tests/test_audit_probe_preflight.py` に18件の回帰試験を追加。64bit canonical keyを精度損失なく比較する例、古い予算欠落監査、異なる親集合、異なるハッシュ、未統合のexact結果を含む。

## 検査結果

CT202上に公開 `main` の浅い複製を作成し、`1f361e260cedeae370bca94ef93be59c300081a7` を対象に実行した。

- 新規監査試験: **18/18 成功**
- 変更したscripts/testsの `compileall`: 成功
- `uv sync --locked`: 成功
- `tools/knowledge/check.py`: **362項目、0 error、0 warning**
- 知識基盤の単体試験: **33/33 成功**
- `tools/knowledge/build.py`: 正常終了
- `git diff --exit-code -- README.md research/knowledge/generated`: 差分なし

既存の旧raw-history JSONを自動補正して再利用することは禁止する。次の探索では **指定予算を明記して raw-history 監査を再生成し、保存済みs6 auditと結合してから** dispatch すること。過去の未完探索を新しいWIN/LOSSとして扱わない。

## 解決状態

本変更は探索前監査の安全性と重複探索回避の改善であり、新しいexact verdict、s4 LOSS、secured coverageの増加を意味しない。最後に確認した既存のreply27 checkpointでは二石root `{60,27}`、標準11×11空盤はともに **UNKNOWN**。最新の勝敗・被覆数は都度 `main` の証拠ファイルから再計算すること。
