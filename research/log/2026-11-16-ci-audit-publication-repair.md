# 2026-11-16：CI監査アーティファクト出版破損3件の修復 — 切断JSON全文再出版・キー順正規化・seed CSV bool表記統一

開始時状況: knowledge.yml（push毎CI）と refresh workflow（"Refresh knowledge generated views"・run #161〜#174連続失敗）の両方が赤。最新runの失敗stepはそれぞれ「Audit Q-family remaining D4 orbit worklist」（`n11-frontier-q-family-orbit-dedup-20261116/verify.py`）と「Audit multiplayer coalition census」（`verify_multiplayer_coalition.py` + `git diff --exit-code`）。生成ビュー（`research/knowledge/generated/`）は31dcedd時代のままstale（K0869が旧p2647監査への壊れたリンクを持ち、K0871以降が未掲載）。

## 診断方法

mainの実験script一式をraw CDNで取得した隔離mirror（gitバイナリなし・`rev-parse HEAD:<path>`をローカルblob sha1で応答するshim経由）で、各検証器を出版済みoutputと突き合わせて再実行した。失敗stepの検証器に加え、失敗stepより後段でまだCI上で走っていないstep（K0867 r8-target・K0872 residue signature等）も同様に検査した。

## 破損1：multiplayer-coalition census audit.json — 出版時の64KB打ち切り

`multiplayer-coalition-kyouen-20261116/output/audit.json` のコミット済み版が **63,999バイトで途中切断した無効JSON**（真の出力130,081バイトの厳密プレフィックス）。K0858レーンの出版時に書き込みが~64KBで打ち切られたもの。

**修復**: `verify_multiplayer_coalition.py` を再実行して130,081バイト全文を再出版した。検証器はexit 0（2独立エンジン完全一致・既刊アンカー386件・回転対13組・決定性・族ルート表の全内部制御PASS）で、コミット済み切断版が再生成物の厳密プレフィックスであることを機械確認した（意味内容の変化なし・欠落は後半の打ち切り分のみ）。

## 破損2：K0867 r8-target audit.json — キー順非正規化

`remo-k-branch-r8-target-refutation-20261116/output/audit.json`（6,927B）のコミット済み版は現行 `verify_r8_target.py` の再生成物と**意味完全一致だがJSONキー順が異なる**（現行検証器は `sort_keys=True` でserializeするため、挿入順の差異は出版後に検証器が正規化された時点で不可避）。検証器は "FATAL: regenerated audit differs from committed JSON" でCI失敗する。

**修復**: 再生成物（6,927B・ソート済みキー）を再出版した。修復後に検証器を2回通してend-to-end PASS・byte-identical determinismを確認した。

## 破損3：Q-family pair-cover seed CSV — bool表記の新旧混在

`n11-frontier-q-family-orbit-dedup-20261116/output/q-family-pair-cover-seed.csv`（37行）のコミット済み版の `is_primary` 列が `true/false`（旧生成物の表記）に対し、現行 `verify.py` はPython boolの `True/False` を書くため "Q pair-cover seed differs from recomputation" でCI失敗する。

**修復**: `verify.py --write` で再生成して再出版した。他3出力（audit.json・worklist CSV・cross-family overlaps CSV）は再計算とバイト同一であり不変。修復後に `verify.py` が "Q_FAMILY_ORBIT_DEDUP_VERIFIED: 1238 -> 687; 9-pair seed; 16 cross-family overlaps" でPASS。bool表記を小文字化で正規化した比較で36データ行が完全一致することを確認（数値・意味内容の変化なし）。

## 修復ファイルとsha256

| ファイル | サイズ | sha256（先頭16桁） |
| --- | --- | --- |
| `research/experiments/multiplayer-coalition-kyouen-20261116/output/audit.json` | 130,081B | `1158070cbafdf29d` |
| `research/experiments/remo-k-branch-r8-target-refutation-20261116/output/audit.json` | 6,927B | `502a4b26b126b7e1` |
| `research/experiments/n11-frontier-q-family-orbit-dedup-20261116/output/q-family-pair-cover-seed.csv` | 4,080B | `069699d13c74e1a2` |

## 解釈境界（重要）

- 3件とも**出版レイヤの破損**（書き込み打ち切り・キー順・bool表記）であり、監査の数値・主張・意味内容は一切変わっていない。該当実験の数学的内容（K0858のセンサス・K0867のr=8反証・Q-family worklistの正準化）は不変。
- K0867のK itemはr7-extension検証器のGit blob SHA pin（`8c8ea051…`）を持つが、今回の修復はscriptを変更しないためpinは無傷。K0858・K0867・K0865〜K0873のいずれのK itemも修復対象3ファイルのshaをpinしていないことを確認済み。
- 修復後も未ローカル検証の重いstep（K0863 sterile・K0864 r_boundary・K0866 r7_extension・K0869 r8_sweep・K0861 k_branch・K0862 collapse_boundary）はCIに委任する。それらは破損2・3と同種の出版破損を持つ可能性が残るが、直近の成功runでは緑だったものであり、今回の再生・triggerでrefresh workflowが最初に失敗したstepで止まる位置が変われば改めて診断する。
- refresh workflowの末尾にtrigger comment行を追加した（本workflowは自身のymlへのpushで発火する）。これにより監査step連鎖が全て緑になれば「docs: refresh generated knowledge views」が着地し、staleな生成ビュー（K0869壊リンク・K0871+未掲載）が解消される。
