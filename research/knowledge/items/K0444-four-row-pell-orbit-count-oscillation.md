---
id: K0444
title: 4行8点円の既知Pell族の円数は厳密閉公式を持ち対数周期振動する
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
- statistics
aliases: []
relations:
- type: depends_on
  target: K0317
  note: 既知のu²−10v²=1無限円族と水平移動数を利用
- type: depends_on
  target: K0432
  note: 固定傾きの円型数の対数増大を、特定族の配置数へ精密化
artifacts:
- path: research/experiments/fixed-width/reports/q48-pell-orbit-count-oscillation-20261015.md
  role: proof
  note: 全mの閉公式、二階差分、誤差の上下極限の証明
- path: research/experiments/fixed-width/scripts/q48_pell_orbit_oscillation_20261015.py
  role: verifier
  note: Pell構成と弦長漸化式の独立照合、144個の盤長の整数検証
- path: research/experiments/fixed-width/output/q48_pell_orbit_oscillation_20261015.json
  role: data
  note: 閉公式・閾値差分の監査と振動数値
scope: 標準4行盤の傾き9/1の明示的Pell軌道と上下反転から得られる円のみ。全円数C8(m)の精密漸近は主張しない。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 既知Pell族の8点円数の閉公式と対数周期振動

最大弦長 `d0=1,d1=73,d[n+1]=38d[n]−d[n−1]` の既知Pell族（および上下反転）の円の個数を `C_P(m)` とし、`N=#{n≥1:d_n<m}` とする。**任意の整数m≥1**について

`C_P(m)=2Nm−(d[N+1]−d[N]−72)/18`。

`λ=19+6√10` とすると `C_P(m)=(2/log λ)m log m+O(m)`。主項を引いた誤差をmで割ったものは収束せず、厳密な上下極限を報告書で与える。二階差分は `m=d_n` のとき2、その他は0で、この族の円数関数は最終的な準多項式ではない。

これはPell無限族の全称代数的証明である。付属検証器の有限計算は独立監査であり、全称性の根拠ではない。全ての8点円の総数への精密漸近は未解決。
