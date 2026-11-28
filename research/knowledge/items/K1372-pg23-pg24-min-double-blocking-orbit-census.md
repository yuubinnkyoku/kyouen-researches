---
id: K1372
title: PG(2,3)/PG(2,4) 最小2重ブロッキング・極大safe族の完全PGL軌道分類
kind: proposition
status: proved
topics: [blocking-sets, finite-geometry, orbit-classification]
aliases: [PG23 PG24 double blocking orbit census]
relations:
- type: depends_on
  target: K1370
  note: 列挙較正値 (PG(2,3) 4:234/9:234, PG(2,4) 7:360, 9:11480/12:11480, 14:360) を入力とする
- type: depends_on
  target: K1365
  note: 補集合双対 (maximal safe <-> minimal t-fold blocking) を両方向全件再検証
- type: depends_on
  target: K1371
  note: AG側 (AG(2,4)/AG(2,5)) の軌道分類は既完了。本項目はPG側
artifacts:
- path: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/scripts/boards.py
  role: verifier
  note: GF(3)/GF(4) 独立盤構成 + 2-(v,q+1,1) design 検査
- path: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/scripts/enumerate_families.py
  role: verifier
  note: 反射Gray + O(1)違反計数器による極大safe・最小DB全数列挙
- path: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/scripts/orbits.py
  role: verifier
  note: PGL(3,q) 全生成・厳密軌道分割・線プロファイル
- path: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/scripts/verify.py
  role: verifier
  note: 定義直接再検証・独立2^n全走査・群閉包サンプル・補集合双対・Fano検査 (ALL_OK)
- path: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/out/orbits.json
  role: data
  note: 軌道census (rep mask・orbit size・line profile)・PG(2,3) 1+1軌道・PG(2,4) 4+4軌道
- path: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/out/verify.json
  role: data
  note: 検証結果 (def_check fail 0・independent match・Baer/Fano all-360)
- path: research/log/2026-11-28-pg23-pg24-orbit-census.md
  role: log
  note: 宣言・実行・検証・出版の一次記録
scope: >-
  有限射影平面 PG(2,3) (s=2) と PG(2,4) (s=3) の2つの族:
  (a) 極大safe集合 (全直線 <=s 点かつ追加不能) と
  (b) 最小2重ブロッキング (全直線 >=2 点かつ各点critical)。
  PGL(3,q) 作用下の完全軌道分割を主張する。
evidence: >-
  有限全数機械列挙 (2^13 / 2^21 反射Gray走査・O(1)違反計数器) と
  PGL(3,q) 全群像による厳密軌道分割。較正として K1370/K1300 出版計数
  (234/234, 360/11480, 11480/360) を完全再現。独立検証4系統:
  定義直接再検査 (fail 0)、Gray法と独立な2^n直接popcount全走査の全集合一致、
  軌道クラスの群閉包ランダムサンプリング + |orbit| divisibility、
  補集合双対の両方向全件一致。PG(2,4) size-7 族は 360/360 が
  2-(7,3,1) (Fano/Baer 部分平面) として機械検証済み。
  宣言後のクリーン再実行で mask list は byte-identical。
---

## 命題・範囲

PG(2,3) s=2 と PG(2,4) s=3 の (a) 極大safe族・(b) 最小2重ブロッキング族の
PGL(3,q) 完全軌道分類（有限・全数・機械検証済み）。

## 結果

- **PG(2,3) s=2**: 極大safe 4:234 は単一 PGL(3,3) 軌道（安定化群 24・oval 型、
  古典的な PG(2,3) oval 数 234 と整合）。最小2重ブロッキング 9:234 も単一軌道
  （min = 9 = 3q は既知の出版値と一致）。
- **PG(2,4) s=3**: 極大safe 11,840 個 = 4 軌道。size 7: 360 個・単一軌道・
  安定化群 168・**全 360 個が Baer (Fano) 部分平面**（7本の3点交差直線が
  2-(7,3,1)。PG(2,4) の Fano 部分平面の古典的個数 360 と一致）。
  size 9: 3 軌道 (10,080 + 1,120 + 280)。
  最小2重ブロッキングも 4 軌道 (size 12: 10,080+1,120+280, size 14: 360)。
- 補集合双対 (K1365) は両盤で全件・両方向一致し、軌道単位でも対応する。
- PΓL(3,4)（σ: α→α+1 を含む半線形群・位数 120,960）でも 4 軌道は併合しない
  （すべて σ 不変）。

## 現在の根拠と限界

根拠は有限完全列挙 + 厳密軌道分割 + 4系統の独立検証（すべて fail-closed、
ALL_OK）。較正値は K1370 出版計数と完全一致。一般 q への外挿
（「PG(2,q) の size-3q 最小2重ブロッキングの軌道数」等）は主張しない。
PG(2,5) s=4（31点・2^31 全走査は本手法のスケール外）の軌道分類は未実施。

## 次の接続

- PG(2,5) s=4 の軌道分類（K1370 の非出版 14MB mask list を用いるか、
  対称性で割った列挙が必要）。
- PG(2,9) の Baer 部分平面対による 3q 未満候補の厳密判定（レジューム (d)）。
