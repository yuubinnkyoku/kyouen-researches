---
id: K0454
title: 5〜63連続整数行で水平中心が半整数の円の最大格子点数は二重点行数の2倍
kind: proposition
status: proved
topics:
- geometry
- rectangles
- variants
aliases: []
relations:
- type: depends_on
  target: K0368
  note: 幅5〜43の二重点行数の厳密最大値と達成円
- type: depends_on
  target: K0369
  note: 幅44〜63の二重点行数の厳密最大値と達成円
artifacts:
- path: research/experiments/geometry/reports/circle-band-halfcenter-5-63-20261016.md
  role: proof
  note: 水平接線の分母帰着、法5040の完全排除、達成円
- path: research/experiments/geometry/scripts/verify_circle_band_max_5_63_20261016.py
  role: verifier
  note: 法16・9・5・7の独立マスクとCRT、59幅の達成検算
- path: research/experiments/geometry/scripts/verify_circle_band_max_5_63_independent_20261016.cpp
  role: verifier
  note: 法5040の直接走査による独立上界検査
- path: research/experiments/geometry/output/circle_band_max_5_63_20261016.json
  role: data
  note: 13右端・3分母の剰余上界と59幅の達成円
- path: research/experiments/geometry/output/circle_band_max_5_63_independent_20261016.txt
  role: data
  note: 独立C++検算結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 標準整数格子の5〜63本の連続水平行。中心のx座標が半整数の円に限る。横幅・半径は無制限。
evidence: '2026-10-21監査。接線から分母g≤3への帰着、全mod5040と13右端の完全性、達成円を確認。PythonとC++を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 半整数水平中心の円の帯内最大点数

`T(w)` を一本の円が2整数点ずつ持つ行の最大本数、`Q(w)` を中心のx座標が半整数の円の全格子点数最大とする。

**全ての `5≤w≤63` について `Q(w)=2T(w)`**。

`T(w)` の既知の厳密値から、`Q(w)` は幅5〜6で8、7で10、8〜10で12、11で14、12〜21で16、22で18、23〜24で20、25で22、26〜42で24、43で26、44〜45で28、46〜47で30、48〜63で32。

証明：半整数中心の円では、整数点が一つだけの行は水平接線で高々2本。接線行と `T(w)` 本の二重点行が同時にあると仮定すると、接線行からの相対高さjに対し `u²=j(H−j)`。既約分母gは全jを割る。幅5〜63ではg≥4だと行数が不足するのでg≤3。`H=s/g`, `j=gz` として `u²=z(s−g²z)` を法5040で完全検査すると、全13区間右端で許容行数が `T(w)` 未満。従って接線と最大二重点行数の共存は不可能。既存の達成円は全て中心x=−1/2で、下界も一致する。

**限界**：中心のx座標が半整数でない円を含む無条件の最大点数 `P(w)` の等号は、w≥17で未確定。`P(w)>2T(w)` の反例があれば、円は各行に高々1点しか持てない。今回の結果だけから標準q点版・circle-only版の全中心全長解決は導かない。
