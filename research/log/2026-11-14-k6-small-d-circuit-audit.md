# 2026-11-14 K0568 circuit縮約の小次元独立監査

## 作業前の確認

- 最新main: 9a803382139918511ead1b790ff1725833af54d9。
- AGENTS.mdはmain直接反映、K項目を正本、generatedは直接編集せず、knowledge check・単体試験・buildを実行する方針。
- research/knowledge/README.mdは有限計算・証明・未監査を区別する方針。
- generated summaryはK項目800件、警告なし。K0568はscope-unclearとして残っていた。
- K0568本文は2026-11-14のexactly-10 circuit同値性補題を既に採用していたが、実験READMEとresults.jsonは「circuit縮約は無効」と古い評価を残していた。

## 独立監査

d=3,4,5（q=d+1）の全サイズ4..q部分集合を列挙した。階数は素数1,000,003と1,000,033で照合し、第二実装では列順を反転した。Hadamard上界216未満により有理数階数と一致する。

- d=3: 依存4集合12、circuit12、依存4集合の被覆12/12。
- d=4: 依存4集合100、依存5集合1,360、circuitは100・160、依存5集合の被覆1,360/1,360。
- d=5: 依存4/5/6集合720/22,240/350,000、circuit720/2,080/41,760、依存6集合の被覆350,000/350,000。
- 生成circuitのq点拡張370,080件は全て依存q集合に含まれた。

検査器は全件PASS。有限完全監査の対象はd=3..5に限り、d=6の列挙器完全性を保証しない。

## 訂正・反映

- exactly-K・K≥qに限り、全依存q集合禁止とサイズ≤qのcircuit禁止は元の点変数上で同値である。小次元監査はこの列挙手順の有限検査であり、d=6の証明ではない。
- READMEとresults.jsonの「circuit縮約は無効」という過剰な記述を、固定基数判定に限る正しい範囲へ修正。
- K0568のstatusをscope-unclearからopenへ変更。対象範囲は明確で、数学的上界が未解決だからである。タイトルもK_6≥9・上界未確定へ修正。
- build_k6_circuits.cppはK<7のcircuit-only CNFを拒否し、exactly-Kカウンタのk=0ケースも扱うよう修正。
- knowledge workflowに小次元検査器・C++構文/引数検査を追加。generatedファイルは編集していない。

## 証拠境界と次の課題

K_6≥9は既存証人により確定。K_6≤9は未証明。既存kissat実行はSIGTERM終了でUNSATではない。次はd=6のcircuit族を、全依存7点組一覧または別の独立列挙器と突き合わせる。