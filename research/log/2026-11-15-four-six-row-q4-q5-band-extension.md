# 2026-11-15 four-six-row q4/q5 band extension（高速レーン）

## 概要

`four-six-row-q4-q5-witness-search-20261114` の残課題（sat3 OOM 壁越え・
rowY 分割・前線掃引）を継ぐ band-extension レーン。claim c91eb241。

## 実施

- 較正: sat3 ≡ sat2 DIMACS バイト一致 11 対照（lex 付き/rowY/lex=H 各種・
  (4,34,4)/(4,20,5)/(5,23,5)/(6,32,4) 等の目標ファミリーを網羅）+ repo meta
  一致（(6,31,4) --lex=H,V で vars/clauses/curves 完全一致）+ kissat 閾値
  コントロール 7/8（残る 1 点 (3,4) m=24 INDET は既知 honest negative と整合）+
  lean5.sh 端到端 + ext_constructive.js の m=33 off=0 / m=34 off=1 再現。
- 発見: 前レーンの lex "H,V,HVHV" は実効 [H,V]（SIG={H,V,HV} で HVHV が
  フィルタ）。判定不変だが記録上の訂正として README/K0833 に明記。
- 掃引: (6,4) m=32..38 def SAT・m=39/40 rowY=0 SAT・(5,4) m=37 rowY=0/38 def/
  39 rowY=1 SAT・(4,4) m=35 def INDET（260s/317,151）。全 SAT witness は
  js verifyConfig + Python Fraction 2系統検証 PASS。
- 事故と回復: (1) 300s bash タイムアウトで実行環境リセット・ローカル記録消失 →
  決定的再実行で (6,4) m=32..36・(5,4) m=38 の conflicts がリセット前と
  bit-exact 一致（cross-reset 決定性の傍証）。(2) push ファイル名に sentinel
  "===" が混入（5a059ea7）→ 20件を個別削除して正名で再 push（7c8fbc8c）。
  (3) 実行環境が一時停止（Filesystem rollback failed）→ ローカル第3バッチ
  （(6,4) m=41 SAT rowY=0 8,226/212.0s・(5,4) m=40 SAT rowY=0 13,441/187.0s・
  (5,5) m=24 SAT 117,243/20.6s・m=25 SAT 1,518,239/192.5s・m=26 INDET
  255s/1,792,002・(4,4) m=35 rowY=0/1 INDET 260s/361,630/253,459・(4,5) m=21
  未実施）は未反映。復旧後に決定的再実行で再生して push する。

## 境界の更新（push 済み分）

- (6,4): [32, 1113] → **[41, 1113]**（witness 帯 m=6..40）
- (5,4): [37, 567] → **[40, 567]**（witness 帯 m=5..39）
- (4,4): 変わらず [35, 237]・前線 m=35 に最初の honest negative（260s INDET）

## 教訓

- 1 bash コールの最悪合計時間を 300s 未満に抑える（5インスタンス×120s cap で
  リセット事故）。バッチ完了ごとに即 push。
- 多数小ファイルの push は manifest（名前+バイト長）+ 単一連結テキスト +
  JS 分割（sentinel は行末 "===" を含めない・サイズで切る）が安全。
- github_app.get_file_contents の内容はサンドボックスコードからは空文字列で
  返る（添付リソースとしてのみ読める）→ raw.githubusercontent.com/<sha>/<path>
  を open_url で取得して JS 内で文字列加工するのが動く手法。
- 環境一時停止中も connector（github_app・web_search.open_url）だけで
  統合（CSV/K/README/log）が可能。

## 追記（統合・修復・第3系統検証）

- 統合 1/2 着地（fbea1838）: CSV 3行更新（(6,4) 41..1113・(5,4) 40..567・(4,4) m=35
  honest negative 注記）+ K0833（title・artifacts 7件・追記）+ README 結果 +
  本ログ。コンパクション前の統合 push は未着地だったため再実行した。
- **pushデータ完全性監査で2件の破損を発見・修復**: q4-w6/records.jsonl の
  m=35/m=38 レコードに結合push由来の余分な改行が混入し JSON が壊れていた
  （921366ba で改行除去・9レコード全て正常パース・値は K0833/CSV 記載と一致）。
  また 5a059ea7 事故のジャンクファイル（"===" 付き）5件が残存していたので削除
  （q4-w6 3件・q4-w5 2件）。全 witness/meta 28ファイルは JSON パース検証で正常。
- **第3系統検証（connectorのみで完結）**: 実行環境停止中、raw URL 取得 +
  run_typescript sandbox 上で verify_independent.ts を verbatim 実行（フラグメント
  照合18/18）し、band-extension 全12 witness が PASS。陰性対照（石移動→
  maxCirc=4 unsafe 検出）・陽性対照（前レーン3系統検証済み (6,31,4) witness
  再PASS）。ts-verify-band-extension.json として push（2a011d4b）。全 witness
  3系統検証済み。
- 技法の記録: github_app.get_file_contents の内容は sandbox コードからは
  空文字列で返る（添付リソースとしてのみ読める）ため、raw.githubusercontent.com
  からの open_url 取得で fetch→JS加工→push が動く。
