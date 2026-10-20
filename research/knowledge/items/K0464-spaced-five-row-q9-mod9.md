---
id: K0464
title: 5本の等間隔整数行で間隔が3の倍数でなければ9点円は存在せず全長強解決
kind: proposition
status: needs-review
topics:
- rectangles
- geometry
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 9点共円・共線禁止と完全指摘のルール定義
artifacts:
- path: research/experiments/fixed-width/reports/spaced-five-row-q9-mod9-20261016.md
  role: proof
  note: 法9による無界全称証明と3倍数間隔の必要条件
- path: research/experiments/fixed-width/scripts/verify_spaced_five_rows.py
  role: verifier
  note: 独立した剰余検査と三点行列式による有限盤完全列挙
- path: research/experiments/fixed-width/output/spaced-five-row-q9-audit-20261016.txt
  role: data
  note: 剰余検査と有限盤完全列挙の出力
scope: 5本の等間隔整数水平行 y=t+id, i=0..4, d>=1, 3∤d, m>=1、9点共線・共円禁止通常プレイの全安全局面
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 5本の等間隔整数行のq9全長強解決

任意の整数t、正整数d,m（3∤d）に対し、5×m盤の行をy=t,t+d,...,t+4dに配置したとき、9点共円・非水平共線の禁止集合は存在しない。安全性は各水平行に8点以下と同値で、任意の安全局面Sで

`g(S)=(5 min(m,8)-|S|) mod 2`。

真の満容量安定化長は8。また、**任意の整数間隔**について、五行の**無限水平格子**上にちょうど9整数点を持つ円は存在しない（有限横幅に切り取ると9点だけが残る可能性は排除しない）。間隔が3の倍数の場合、9点以上の円があれば必ず10点円であり、各行の整数二根差の3進付値は全て同じで、行間隔の3進付値より小さい。証明は判別式平方列の二階差分 `-8d²` を法9で `d²` の逆元により正規化し、5連続平方剰余列が存在しないことに帰着する。9点円の不存在は全整数間隔に成立するが、10点円の不存在とGrundy式は間隔3の倍数には拡張しない。全証明と独立検算はartifacts参照。
