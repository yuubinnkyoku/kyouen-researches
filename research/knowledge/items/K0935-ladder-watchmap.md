---
id: K0935
kind: proposition
status: proved
title: 監視位置のラダー境界越え写像（WATCH-MAP）とストレッチ間死亡判定の合成
aliases: []
relations:
  - depends_on: [K0934]
  - connects: [K0931, K0933]
artifacts:
  - research/experiments/watchmap-20261118/report.md
  - research/experiments/watchmap-20261118/watchmap_verify.py
  - research/experiments/watchmap-20261118/audit_build.py
  - research/experiments/watchmap-20261118/output/watchmap_audit.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, ladder, stretch, watched-tracking, machine-evidence]
---

## 主張（すべてK0928のpot力学上の全称証明）

### 補題WATCH-MAP（生存監視位置の新circle内位置・全称）

w≥2・0≤h≤w・n=(w+1)t+r（t≥2・すなわちn≥2w+2）・1≤a≤w+1とし、
監視位置n−aが第一stretch-wを生存（K0934 LAD-GEN (e)によりa≠r+1・
例外(h,r,t,a)=(0,0,2,w+1)以外）とする。終状態F(w+1,h2;n2)
（LAD-GEN (c)）の新ptrフレームcircleにおける監視のindexはちょうど
n2−a2で、a2は次の閉形式で与えられる:

- r<h・a≤r → a2=n2−r+a（前segment）・a≥r+2 → a2=a−r−1（長segment）
- r≥h・r≥1・a≤r → a2=a+w−r（cold prefix）・a≥r+2 → a2=a+w−r−1
- r=h=0・a≤w → a2=w+a−1（a=w+1は死亡例外）

### 系WM-COMP（SIEVE bookkeeping原始操作・全称）

監視は第二stretch（第一stretch-(w+1)）で死ぬ ⟺ 位置n2−a2が
F(w+1,h2;n2)のLAD-GEN除去集合（block { j(w+2)−1 } ∪ breaking敗者）に
属し、死亡フェーズ・保持もその除去のものと一致する。a2≤w+2の監視
範囲ではLAD-GEN判定式に簡約: 死ぬ ⟺ a2=r2+1（r2=n2 mod (w+2)）・
a2≥h2+1で冷死・a2≤h2でhot最終死。**WATCH-MAP+LAD-GENの反復で監視の
ストレッチ間追跡が(w,h,n,a)上の純算術になる（シミュレーション不要）**。
K0933のS3/S4で手計算だったものの一般化であり、SIEVE7（spf=7・
stretch-5/6・m mod 42類）はこの反復の有限計算に帰着する。

### w=4の表（SIEVE7入力・閉形式で機械確認済み）

K0933 S4のweight-4四族（生存rのみ・rの死亡類はS4の通り）の
stretch-5状態F(5,h2;n2)へのa2表:

- W4(n)（監視a=1）: r≥1でa2=5−r・h2=4−r・n2=4t+r−1
- F(4,1;n)（監視a=1）: r≥1でa2=5−r・h2=5−r・n2=4t+r−1
- F(4,2;n)（監視a=3）: a2はr=0→2・1→1・3→4・4→3（h2=1−r（r≤1）・
  6−r（r≥3）・n2=4t+r（r<h側）・4t+r−1（r≥h側））
- F(4,3;n)（監視a=3）: a2表はF(4,2)と同一（h2=2−r（r≤1）・7−r（r≥3））

stretch-5判定（a2=r2+1・r2=n2 mod 6）をこの表に適用しもう1回反復する
のがSIEVE7の計算（次回レーン）。

## 機械的証拠

- watchmap_verify.py（LAD-GEN coreは出版済みK0934検証器からverbatim
  copy・標準ライブラリのみ・決定的）: w=2..7・h=0..w・n≤155の全
  グリッドでWM1（生存監視の新circle index==n2−a2・23,714検査）と
  WM2（合成: 監視のstretch-2死亡⟺n2−a2∈elim(F(w+1,h2;n2))・
  フェーズ・保持まで照合・23,713検査）が0失敗。
- audit_build.py: 全チェック2回in-process実行・一致確認・
  output/watchmap_audit.json生成（決定的）。2回cold実行でbyte同一
  （file sha256
  024d86211a1a72f5c26f395b78d4e10d727594bb006190c357c10d9b1a27c36b）。
- 証明はreport.mdの紙上証明（K0934終状態censusのsegment構造からの
  読み取り・場合分け3ケース）。スクリプトは機械アンカー。

## 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。
- 定理域はLAD-GEN＋t≥2・1≤a≤w+1・監視は第一stretch生存に限る。
  崩壊(t,r,h)=(1,0,0)はt≥2で発生しない。h2>w+1の終状態もWATCH-MAP
  自体は写像するが、次stretchのLAD-GEN判定域外（WM2はその点をskip）。
- a2>w+2となる写像先では監視範囲の簡約式でなく除去集合 membership
  （WM2の実装）を使う必要がある。
- SIEVE7本体（mod 42類の表・死亡 residues の決定）は本項の範囲外
  （次回レーン）。P(C)の一般閉形式は主張しない。
- 11×11空盤の状況は不変（空盤・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4はすべてUNKNOWN）。
