---
id: K0441
title: 固定11点Grundy5証人は13×13以下の標準盤で正確な残余ゲームにならない
kind: proposition
status: needs-review
topics:
- grundy
- residual-games
- geometry
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 標準4点共円・共線禁止規則
artifacts:
- path: research/experiments/grundy-five-residual-obstruction-20261018/proof.md
  role: proof
  note: 必要条件への一般帰着と6〜13盤の有限完全列挙
- path: research/experiments/grundy-five-residual-obstruction-20261018/verify.py
  role: verifier
  note: 整数行列式・全緩和候補列挙
- path: research/experiments/grundy-five-residual-obstruction-20261018/independent_verify.cpp
  role: verifier
  note: 独立の円方程式・ビット集合再帰
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 固定11点Grundy5証人の残余実現障害

W={(0,0),(0,4),(1,1),(1,3),(3,1),(3,2),(3,4),(4,1),(4,5),(5,0),(5,2)} は4個の禁止4点組を持ち、空盤Grundy値5（全安全局面1,635）。

n=6..13の標準正方形盤の原点にこのWを置いた場合、占有集合SをWの外側に選んでも、合法手集合がちょうどWで、W内の制約がW単独盤と完全に一致する残余局面は存在しない。

Wの3点と禁止4点組を作る外点はSに含められない。さらにWの2点とSの2点、Wの1点とSの3点の禁止を排除する必要がある。この条件だけを課した緩和集合を全列挙し、各SとSの3点によって塞がれる外点の合計が常に全外点数に満たないことを証明した。最大候補数はn=13で1,425,787、最大占有数12、最大被覆数126、外点158。整数行列式と独立の円方程式判定で一致。

座標を動かした埋め込み、n≥14、他の11点Grundy5証人、標準盤のGrundy無界性は対象外。有限完全列挙を無界命題の証明に読み替えない。
