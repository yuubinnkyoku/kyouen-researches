# 2026-11-17 n11 class2-lane: extractor/engineコピー9本のmemo欠陥構造監査（K0907 follow-up）

## Context

K0907（`K0907-extractor-memo-sign-bug-and-dead-negative-bounds.md`・log
`2026-11-17-n11-class2-lane-extractor-memo-sign-bug-and-fixed-battery-73k.md`）
は class4_child1_cert_extractor_exact.ts 1コピーについて符号付きmemoキー
（bug A）と死んだsentinel 255負境界（bug B）の2欠陥を定量・修正batteryで
測定したが、scope に「sweep engine・chunk prover・FBT-saturation runner等の
他コピーは本項の範囲外で未監査のまま」という限界を残していた。本実行で
その限界を閉じるため、該当系の残り全エンジンコピー9本に対する構造監査を
実施した。

## What was done

1. **script** `audit_extractor_copies_memo_defects_20261117.py`
   （stdlib Python + Node・決定的・2回実行で出力JSON byte同一・md5
   `fa358d67`）:
   - 監査対象9ファイルを commit `99f83e51` 固定の raw CDN から取得し、
     **9/9 git blob sha pin検証 PASS**（mismatch 0）。
   - memoFind/memoEntry ブロックの空白正規化 token 比較:
     extractor族3本（cert_extractor `6716075d…`・exact `52bcaf50…`・
     exact_ms23 `c267f260…`）が token 同一、sweep-side族3本
     （v15 sweep_engine `bd6a650a…`・chunk_prover `fc74d215…`・
     FBT runner `8744fc65…`）が token 同一、両バグ持ち族は完全空白
     除去後に同一 = textual に同一機構。したがって K0907 の dump 定量
     機構（重複挿入・私有窓・nowin=nolose全255）がそのまま全コピーに
     妥当する。
   - ms23 は exact とちょうど1行差（MS=1<<18→1<<23・line 77）を
     assert で確認 → K0907 監査が 73k/73l 出版バンドの抽出器
     （ms23）を被覆。
   - bug パターン計数: 符号比較2箇所（mNoWin/mNoLose検索の
     `mNoWin[h]===d` 形）・死んだ負境界更新行 nowin/nolose 各1行
     （`d>mNoWin[h]` sentinel 255逆方向）が各バグ持ちコピーで正確な
     回数で存在し、修正版では sentinel 対応形
     （`mNoWin[h]===255||d>mNoWin[h]`）に置換されていることを確認。
   - node -e 符号 demo: Uint32Array への int32 格納は +2^32 で読み
     戻るため `===` 比較が不成立、Int32Array は正確（K0907 と同じ
     実証のコピー監査版）。

2. **監査結果（9コピー）**:
   - **bug A+B 存在: 6コピー**。extractor族（cert_extractor・exact・
     exact_ms23）と sweep-side族（v15 sweep_engine・chunk_prover・FBT
     runner・いずれも2026-11-13 batch1世代）。両族のmemoブロックは
     空白除去後に完全同一。
   - **両fix済み: 3コピー**。runner_v16 `0a4a86f6…`・runner_v17
     `c132cc64…`（両fix・memoブロック同一）・extractor_exact_v16
     `5518d375…`。
   - 特に出版 73i/73j/73k/73l raw 掃引で使用した **v17 エンジンは両
     fix済み** ため、掃引側の MS 容量測定（log
     `2026-11-17-n11-class2-lane-sweep-memo-capacity-measurement.md`）
     の利得は重複挿入ノイズを含まない純容量効果であることが確定した。

3. **K0907 item 更新**: title 拡張・aliases 2件追記・artifacts 2件追記
   （監査script + 監査JSON）・evidence に追記記録・scope の「他コピーは
   未監査」限界を閉包・body 限界節を更新。

## Interpretation guard

- 両bugとも memo は最適化のみで、誤った hit は不可能（符号なし格納値は
  負の比較値と決して等しくならない）。見逃し（再探索）のみを生じる
  性能欠陥であり、**全出版verdict・証明書・ノード数は verbatim 値と
  して有効・サウンド性無影響**（K0907 と同一の解釈境界が9コピーすべて
  に妥当）。
- 本監査は構造監査（token同一性・パターン計数・blob pin）であり、
  コピー個別の dump 定量や修正battery再測定は実施していない
  （token同一性により K0907 の定量が妥当する根拠）。
- fold chain（66i/66j/69j/71e/72d/73i/73j/73k）・receipt fold は並走
  管理のため着手していない。73i 証明書は出版待ちのため本監査の対象外。
- **11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4 は
  すべて UNKNOWN のまま**。本監査は性能・構造確認であり、勝敗変更を
  含まない。

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_extractor_copies_memo_defects_20261117.py`
- data: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-extractor-copies-memo-defect-audit-20261117.json`
- knowledge item: `research/knowledge/K0907-extractor-memo-sign-bug-and-dead-negative-bounds.md`（更新）
- README bullet: `research/knowledge/README.md` K0907 bullet に追記
