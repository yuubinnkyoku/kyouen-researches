---
id: K1353
title: "錐＋枠二重数え上げ法 — 推移群と単一錐の完全 DP で Grundy 分布を厳密に得る"
kind: proposition
status: proved
topics: [grundy, search-methods]
aliases:
- cone double counting for Grundy distributions
- orbit-transitivity method for exact Grundy tables
relations:
- type: related
  target: K1352
  note: PG(2,9) の完全分類をこの方法で厳密に再現（独立検証）
- type: depends_on
  target: K1058
  note: 共演ゲームの定義と Grundy の自己同型不変性
scope: 有限ハイパーグラフ盤の共演ゲーム一般。自己同型群 G が k0-キャップに推移的で Grundy が G 不変なとき、単一の k0-キャップの錐（それを含む安全集合全体）の完全 DP から、k≥k0 の全サイズの Grundy 分布を厳密に得る方法。
evidence: 補題。盤 B、G ≤ Aut(B)、G は k0-キャップに推移的、Grundy は G 不変とする。固定した k0-キャップ F の錐で T_m(g) = #{M ⊇ F かつ |M|=m, Grundy(M)=g} を計算する。m ≥ k0 に対し N_m(g)·C(m,k0) = Σ_{F'} T_{F'}(g) = N_{k0}·T_m(g)（二重数え上げと推移性・不変性）。よって N_m(g) = N_{k0}·T_m(g)/C(m,k0)。PG(2,9) s=2 では k0=4（PGL(3,9) は 4-キャップに推移、|PGL|=91·90·81·64）、F={0,1,10,20}、錐は 1,868 局面。錐 DP と枠二重数え上げで k=4..10 の全分布が厳密に再現され、k=0..4 は mex 連鎖で確定する（独立検証 全項目 PASS、K1352）。
---

# 錐＋枠二重数え上げ法

## 補題

盤 B の共演ゲーム、G ≤ Aut(B) が k0-キャップに推移的、Grundy は G 不変とする。
固定した k0-キャップ F について

```
T_m(g) = #{ M ⊇ F : |M| = m, Grundy(M) = g }
```

を錐の完全 DP で計算すると、m ≥ k0 に対して

```
N_m(g) · C(m, k0) = N_{k0} · T_m(g)
```

（左辺は (k0-部分集合, m-キャップ) の二重数え上げ、右辺は推移性と Grundy 不変性）。
よって

```
N_m(g) = N_{k0} · T_m(g) / C(m, k0)
```

## 応用（PG(2,9) s=2）

- k0 = 4、F = {0,1,10,20}、錐 = 1,868 局面。
- 錐 DP で T_m(g) を計算し、上の式で k=4..10 の全分布を厳密に再現。
- k=0..4 は mex 連鎖（4→3→2→1→0）で確定。
- 独立検証で全項目 PASS（K1352）。

## 意義

- **1 億 2,891 万局面のゲームでも、単一錐（1,868 局面）の DP と群の推移性だけで
  全分布が厳密に得られる**ことを示す。
- 計算量は錐のサイズに依存し、盤全体の列挙を不要にする。
- 推移群が大きい盤（PG, AG, 設計ボード）に広く適用可能。
