---
id: K1218
title: (7,4) 7×65 witness w65-01 — 幅60..65 を超える2R2A targeted surgery による下界更新 M_{7,4}∈[66,1929]・単一石集合で幅54..65の12連続 witness・幅66クラス(i)完備陰性
kind: proposition
status: proved
topics: [rectangles, maximal-safe, fixed-width]
aliases: []
relations:
- type: extends
  target: K0827
  note: (7,4) 家族初の band witness は m=20 まで 7×4..7×20 を確立。本項は幅65までの witness と M_{7,4}≥66 に更新（上界不変）
- type: related
  target: K1211
  note: (6,4) W1 family の「単一石集合で幅42..51の10連続」の (7,4) 対応物。w65-01 family は幅54..65の12連続で単一 seed として past 記録
- type: depends_on
  target: K0318
  note: 上界（代入 U=1929）は不変
- type: related
  target: K1209
  note: 手術クラス体系（1R1A/2R1A/2R2A・T-curve完備クラス）と境界での c0 ケース分割は本レーン手術の先行方式
artifacts:
- path: research/experiments/seven-eight-row-translation-census-20261122/witness/w65-01.json
  role: source
  note: 7×65 q=4 witness 20石 rows [3,3,3,3,3,3,2]（def-mode）。origin は w60-10 id像+10シフト 7×65 の 2R2A (remove [[21,5],[50,1]], add [[33,1],[63,5]])・sha256 1056ce42…
- path: research/experiments/seven-eight-row-translation-census-20261122/scripts/verify_int.py
  role: source
  note: 新規独立整数検証器（3×3行列式円・isqrt2次・浮動小数点なし。判別式0の接円で同一点を二重計上する v1 バグを陰性対照で捕捉し修正済み）
- path: research/experiments/seven-eight-row-translation-census-20261122/scripts/surgery66.py
  role: source
  note: 幅66クラス(i) c0=2 targeted surgery (T=(0,6) 単一不足 base)。1R1A計1860・2R1A計17670候補を per-a1 progress resume で完走
- path: research/experiments/seven-eight-row-translation-census-20261122/output/verify_w65-01.json
  role: data
  note: 独立検証の出力（safe/maximal/def すべて true・maxCurveCount=3・unblockedCount=0）
- path: research/experiments/seven-eight-row-translation-census-20261122/output/tamper-and-controls.json
  role: data
  note: tamper対照 drop(13,4)→not maximal ((1,4)が first unblocked・計23 cell) と relocate(13,4)→(50,6)→unsafe。JS発見エンジンの記録と cell レベルで一致
- path: research/experiments/seven-eight-row-translation-census-20261122/output/translation_sweep_54_75.json
  role: data
  note: D4像×全並進の幅54..75完全スイープ。幅ごとの witness 配置数 54:4, 55..64:8each, 65:4, 66..75:0
- path: research/experiments/seven-eight-row-translation-census-20261122/output/surgery66_summary.json
  role: data
  note: 幅66クラス(i)完備陰性の機械記録（クラス(ii) 2R2A・クラス(iii) c0=0 は未走査・c0=0 は def-mode 非互換）
---

## 命題

7×65 (q=4) に 20石 row-deficient maximal witness が存在する:
**w65-01**, stones (10,2),(13,4),(14,6),(17,1),(17,3),(20,4),(26,3),(28,2),(29,5),(31,3),(32,0),(33,0),(33,1),(38,4),(42,2),(42,6),(43,1),(43,5),(57,0),(63,5),
rows [3,3,3,3,3,3,2]（def-mode）。

よって **M_{7,4} ≥ 66**（下界 60 から更新。上界 T_7=1929 不変、M_{7,4}∈[66,1929]）。

## 根拠

- 発見: 宣言済み高速レーン (単一オーナー宣言 `66e7033b6e`) の targeted surgery。
  seed は幅60 witness (pair0 family) の id 像 +10 シフト 7×65 配置、クラス (ii) 2R2A
  (N=5,434,000, 33.0s), remove [[21,5],[50,1]] / add [[33,1],[63,5]]。
- 2系統検証: (1) 発見エンジン (JS BigInt, safe+maximal+def, tamper drop (13,4) で
  (1,4) unblocked), (2) 本実験の独立 Python 整数検証器 (全コード無共有)。
  両系統で safe+maximal+def 全成立、tamper 記録は cell レベルで一致。
- 翻訳スイープ: 単一 w65-01 family の D4 像×全純並進を幅54..75で機械検証し、
  **幅54..65の12連続幅すべてに witness 配置**（幅あたり4..8配置、全て def-mode）、
  幅66..75では 0配置。この seed に閉じた観察であり、他の石集合への不在主張はしない。
- 幅66: base = w65-01 id像@shift 11 は unblocked T=(0,6) のみの単一不足配置。
  クラス (i) c0=2 (ブロック曲線が base 石ちょうど2 + 追加1) を完全列挙:
  1R1A 1,860 / 2R1A 17,670 候補、**0 hit**（scoped local negative）。
  クラス (ii) 2R2A (c0=1, ≈13.8M final states) は今回未走査、クラス (iii) c0=0 は
  3石追加で rows 0..5 (既に q−1) を必ず超え def-mode 非互換。
  7×66 の成否は UNDETERMINED（本項は不決着を明示し決着を主張しない）。

## 限界とスコープ

- 下界の存在主張のみ。7×66..7×1929 の任意幅の不在は主張しない。
- 幅60..64 の連続 witness は翻訳機械検証で本項に含まれる（幅60 の旧 witness 記録と
  独立に再構成されたもの。前セッションの 26 witness stones 喪失事故は session log
  `research/log/2026-11-22-seven-eight-row-translation-census-session-log.md` 記録の通り、
  本項の主張は w65-01 とその翻訳族のみに依拠する）。
- 標準 11×11 空盤・二石 root・class 1/2/4 は非接触で UNKNOWN のまま。
  候補数を勝敗として読まない。
