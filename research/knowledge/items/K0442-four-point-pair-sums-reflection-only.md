---
id: K0442
title: 4点の無順序二点和復元では中心反射が唯一の曖昧性
kind: proposition
status: needs-review
topics:
- geometry
- variants
aliases: []
relations: []
artifacts:
- path: research/experiments/pairsum-fourpoint-reflection-20261018/proof.md
  role: proof
  note: 重複を許す4実数の二点和復元に関する全称証明
- path: research/experiments/pairsum-fourpoint-reflection-20261018/verify.py
  role: verifier
  note: 有理数復元による有限監査
- path: research/experiments/pairsum-fourpoint-reflection-20261018/verify_independent.cpp
  role: verifier
  note: 独立の全組合せ同値類監査
scope: 4実数多重集合の6個の無順序二点和。整数の場合の偶奇分類を含む。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 4点の無順序二点和復元では中心反射が唯一の曖昧性

4実数多重集合 `X` の総和を `T`、相異なる添字の6個の二点和の多重集合を `P(X)` とする。

`P(Y)=P(X)` なら `Y=X` または `Y={T/2−x:x∈X}` に限り、両者は必ず同じ二点和を持つ。両者が一致するのは `T/2∈P(X)` の場合に限る。従って実数上の逆像数は1または2であり、整数上では `T` が奇数なら常に一意、偶数なら中心対称のときだけ一意である。

証明は `xi−T/4` で中心化し、6つの二点和を `±a,±b,±c` に分解して4点を復元する。符号選択の偶奇によって、元の集合かその中心反射のいずれかだけが生じる。詳しい全称証明と2方式の有限監査はartifactsを参照。

**限界：** 円そのものの一致やGrundy値の一致、3×m・q=5の閾値改善は導かない。今回のK番号はmainへ統合するまで仮番号である。
