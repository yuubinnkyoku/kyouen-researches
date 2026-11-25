# 2026-11-20 n11 残余72行 36-witness掃引の準備成果物（prep 53b07ebe16）独立監査

## 経緯と着手判断

前回実行（続行11・fold10第二検証）のレジュームの通り、resolve7/cache-join再構築・36 witness掃引・unsafe分類はそれぞれ単一オーナー宣言済みであり、本レーンは着手しない。最新main（着手時HEAD `2339957f76`）を確認したところ、掃引オーナーが2026-11-19T22:14:15Zに**準備コミット `53b07ebe1647b2c966af098897290df243ba0d19`**（roots.json・residual72.json・runner_v17.ts固定コピー・prepare_roots.py・driver.py・assemble.py・READMEの7ファイル）を出版し、掃引本体を着手していた。このprep成果物は出版直後で**まだ独立検証が一切存在しない**。72 probe×最大280秒の掃引が完走した後にassemble gateが入力のピン不一致で落ちれば計算が全部流失するため、実行前に独立監査で排除できるリスクを除外するのがこの時点で最も価値が高いと判断した。resolve7第二検証・K1075 whole-record第二検証と同じ宣言ノート方式で単一オーナー宣言を先行出版（commit `18ec5f76`）してから着手した。

## 機械と結果

機械 `scripts/audit_sweep_prep_20261120.py`（stdlibのみ・repo-root相対パスで解決・全入力SHA pinでfail-closed）。D4正準化は本レーンが独自に書いた点変換実装で、手計算で検証した4つのself-test（角対 {0,120} の軌道2値化とcanon、中心cell 60の全不動、L字3石のrot90/transpose像、回転合成 t1∘t1=t2・t1∘t3=id）を組み込んだ。当初のself-test期待値は本レーンの手計算ミス（cell座標の y/x 転倒）で2回失敗したが、機械出力が正しく手計算側が誤りと特定して修正した。この失敗は機械の健全性確認にもなった（期待値を壊すとgateが必ず落ちる）。

**40/40 gate PASS**（正本 `output/sweep-prep-independent-audit-20261120.json`・SHA-256 `e89fbe72ff8f8713cdc0d9cfedd37886e0a43d9750e5337109af269e3c622d6c`）。主な確定事項:

1. **roots.json・residual72.jsonのbyte-exact独立再導出**: K1075正本 `49b6f85f…` の `witness_full`（36根・safe・rows）・`residual_row_hex`（72行）から独自D4実装で再導出した36根の `{root, child, bit, pcount, rows, safe}` とソート済72行が、出版済み2ファイルのbytesと完全一致（`json.dumps(indent=1)+"\n"` 直列化で比較）。child=root−最小セットビット（RAW hex）・bit=最小ビット位置の runner意味論ラウンドトリップ（child∪{bit}==root）も36根全てで確認。
2. **exact 1-cover**: 36根×2行=72被覆が72残余行と完全一致、各行ちょうど1回。D4削除軌道は36根全てが7要素（2石削除の正準合流なし）。
3. **ピン活性**: K1075正本SHA・roots SHA（3904041e…）・residual SHA（78e3ee7a…）・runner git blob（c132cc64…）・prepコピーとrepo原本のbyte同一。すなわち**assemble.pyが掃引完走後に検査する3ピンは全て実在成果物と一致**し、入力側でgateが落ちる経路が消えた。
4. **driver静的整合**: roots[W::4]分割9×4非交差、(root,ordering) 72キー一意、cap 30M/timeout 280s均一、resume述語（resultかつerrorなしのみskip）がassembleのok-record述語と同一、argvフラグがrunner解析器と過不足一致（--nocontrol不使用→全probeでpilot制御実行）、andclose閾値d≥8でdepth 10の両モード有効。
5. **smoke test（cap 2000・非判定）**: node --experimental-strip-types での実起動で pilot_d6 `{loss=false, nodes=3402, capped=false}` 厳密再現・両順序で確定的capped micro-probe（nodes=2001）・2行JSONL形式がdriverの解析と整合。**capped結果はどの方向の証拠でもない**。

3回実行（同一cwd 2回＋別cwd別プロセス再生成1回）でbyte-identical。

## 運用メモ

- prepコミットの実価値は「掃引オーナーの高価な実行の前に、別レーンが出版物だけで全入力を検証できた」点にある。40 gateのうちbyte-equal 2 gate以外は全て出版後にしか検証できないもの（assemble内ピン文字列と実体の一致・driver/runnerソース間の静的契約・実行smoke）で、独立レーンでなければ書けない検査群である。
- 本監査は掃引の判定結果には一切触れない（掃引は実行中であり、結果の回収・第二検証は掃引出版後の次回実行候補）。
- K1079（22:24出版）がK1076パッケージのbyte-pin不整合（検証器実SHA a7878b8e vs pin主張388e1a47）を検出報告済み。pin修正はK1076レーン管轄。同じ種類の事故が36witness掃引パッケージで起きないことをは assemble 3ピンの実性確認（上記3）でこの時点のrepo内容では担保した。

## 解釈規約（不変）

REFUTED-D10はLOSS証明ではない。被覆・matching・監査は簿記である。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## レジューム（次回・着手前に必ず最新mainを取り直す）

1. **36 witness掃引の結果回収**: 掃引オーナー（systemd-run 4 worker・各probe 280s）が完了して正本JSONが出版されたら、分類表（WIN7-D10候補数・REFUTED数・capped・順序矛盾）を確認する。WINがあれば第18証明書抽出・検証・foldは掃引オーナー（または宣言ノートで分離されたレーン）の管轄。**結果JSON出版後には、出版正本＋roots/residual/K1075からのみで分類集計・pilot/cap整合・両順序合意・被覆閉包を再検査する独立第二検証が本レーンの自然な次の価値ある作業**（assemble gateの外部再現）。foldまで済んだ場合はfold記録の第二検証が候補。
2. fresh-unsafe 2,871分類＋add-two-stones census（宣言ノート済み・`n11-residual72-unsafe-classification-add2stones-20261120/`）の出版状態も回収する。
3. K1076 byte-pin修正（388e1a47→a7878b8e）がK1076レーンで実施されたか確認する（未実施ならCIのK1076監査ステップは引き続き落ちる。本レーンからは触らない）。
4. 11×11戦略がfresh-safe 36本掃引の全REFUTEDに終わった場合、次の調整は add-two-stones拡張の実掃引（宣言必要）か depth>10 か fresh-unsafe供給のいずれか。いずれも出版済みcensus・コスト見積りを待ってから着手判断する。
