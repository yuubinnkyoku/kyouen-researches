---
id: K1295
title: 射影平面 PG(2,q) のブロッキング集合共演ゲーム — 完全 Grundy と最小多重ブロッキング集合
kind: computation
status: computed
topics: [grundy, geometry, statistics]
aliases:
- blocking-set Kyouen on projective planes
- minimal multiple blocking sets as maximal safe sets
- K_3(PG(2,q)) exact values
relations:
- type: extends
  target: K1253
  note: 反転平面盤の完全 Grundy を射影平面盤へ拡張（補集合が多重ブロッキング集合）
- type: related
  target: K1298
  note: 全極大サイズが奇数であるため parity-graded 補題が Grundy ∈{0,1} を説明
- type: related
  target: K1274
  note: 多重ブロッキング集合のスペクトル τ_d と、その補集合としての K_3 の関係
artifacts:
- path: research/experiments/projective-blocking-kyouen-20261125/report.md
  role: log
  note: 完全 Grundy 表・極大集合の構造・K_3 列・parity-graded 補題の適用
- path: research/experiments/projective-blocking-kyouen-20261125/scripts/build_pg2.py
  role: source
  note: F_q^3 の部分空間から PG(2,q) を構成（素体と GF(4)）、点対の一意性を検証
- path: research/experiments/projective-blocking-kyouen-20261125/scripts/structure_pg2.py
  role: verifier
  note: 極大安全集合の DFS 全列挙と補集合（最小多重ブロッキング集合）のプロファイル計算
- path: research/experiments/projective-blocking-kyouen-20261125/scripts/ks_pg2.py
  role: solver
  note: scipy HiGHS のバイナリ ILP で K_3, K_4 を厳密計算
- path: research/experiments/projective-blocking-kyouen-20261125/output/grundy_pg2q3.txt
  role: data
  note: PG(2,3) の完全 Grundy（safe 4,330、極大 7:234, 9:13、0:2184, 1:2146）
- path: research/experiments/projective-blocking-kyouen-20261125/output/grundy_pg2q4.txt
  role: data
  note: PG(2,4) の完全 Grundy（safe 180,058、極大 7:360, 9:11,480、0:89,799, 1:90,259）
- path: research/experiments/projective-blocking-kyouen-20261125/output/structure.json
  role: data
  note: 極大安全集合のサイズ別代表と補集合の直線交差プロファイル
- path: research/experiments/projective-blocking-kyouen-20261125/output/ks_pg2.json
  role: data
  note: K_3, K_4 の ILP 厳密値（q=2,3,4,5）
- path: research/experiments/projective-blocking-kyouen-20261125/independent/REPORT.md
  role: log
  note: 独立実装による全タスク検証（PASS、D1/D2 の訂正を含む）
- path: research/experiments/projective-blocking-kyouen-20261125/independent/run_all.ps1
  role: verifier
  note: 独立検証のドライバ（Grundy エンジン・ILP 不使用）
- path: research/experiments/projective-blocking-kyouen-20261125/scripts/orbits_pg2.py
  role: solver
  note: PGL(3,q) の生成元による軌道分解と完全四辺形/三角形の同定
- path: research/experiments/projective-blocking-kyouen-20261125/output/orbits.json
  role: data
  note: PG(2,3) の完全四辺形 234、PG(2,4) の 3 軌道（10,080/1,120/280）とプロファイル
scope: 射影平面 PG(2,q) 上の「各直線と高々3点」共演ゲーム。完全 Grundy は q=2,3,4（v=7,13,21）。K_3 と K_4 の厳密値は q=2,3,4,5。
evidence: ボードは F_q^3 の部分空間から構成し点対の一意性を全数検査。完全 Grundy は出版済み grundy_full.exe（n≤64）で全安全局面を列挙。極大安全集合は DFS で全列挙し、補集合の直線交差プロファイルを計算。(i) 極大安全サイズは q=2:7、q=3:7 と 9、q=4:7 と 9（すべて奇数）。(ii) 補集合は最小 (q−2) 重ブロッキング集合。q=3 は直線 13 個と 6 点集合 234 個（PGL(3,3) 単一軌道、profile {1:6,2:3,3:4}）。q=4 は 12 点 11,480 個が 3 プロファイル（{2:10,3:6,4:3,5:2} 10,080 / {2:9,3:9,5:3} 1,120 / {2:12,4:9} 280）と 14 点 360 個（profile {2:7,4:14}）。(iii) 完全 Grundy は 3 盤すべて {0,1} のみ、空盤は 1（K1298 の parity-graded 補題と整合）。(iv) K_3(PG(2,q)) = 7, 9, 9, 11（q=2,3,4,5、ILP 厳密）。q=7 の ILP は未完了。独立検証（標準ライブラリのみ、Grundy エンジン・ILP 不使用）は q=2,3,4 の Grundy・極大集合・K_3 を再計算して一致し、q=4 の 12 点集合が単一プロファイルでなく 3 クラス（10,080/1,120/280）であることを指摘、本項はその訂正を反映済み。追加解析（orbits_pg2.py）で、q=3 の 234 個は完全四辺形の頂点集合（4 本の 3 点直線が一般位置、個数 C(13,4)−13·4·9−13=234）であり、q=4 の 11,480 個は 3 個の PGL(3,4) 軌道（サイズ 10,080/1,120/280、固定群位数 6/54/216）に分かれ軌道＝プロファイルクラスであることを確認（生成群の位数 60,480 = |PGL(3,4)|）。1,120 軌道は 3 直線の三角形（個数 C(21,3)−21·C(5,3)=1120）。
---

# 射影平面 PG(2,q) のブロッキング集合共演ゲーム

## 双対

`PG(2,q)` の直線は `q+1` 点。安全条件 `|S∩ℓ| ≤ 3` は補集合
`X = V\S` について `|X∩ℓ| ≥ q−2`、すなわち **`(q−2)` 重ブロッキング集合**。
`S` が極大 ⟺ `X` が包含極小な `(q−2)` 重ブロッキング集合。
とくに q=3 は通常のブロッキング集合、q=2 は条件なし（全部分集合が安全）。

## 完全 Grundy

| board | v | safe | Grundy(∅) | misère | K | 極大サイズ（個数） | Grundy 分布 |
|---|---:|---:|---:|---:|---:|---|---|
| PG(2,2) | 7 | 128 | 1 | 0 | 7 | 7 (1) | 0:64, 1:64 |
| PG(2,3) | 13 | 4,330 | 1 | 0 | 9 | 7 (234), 9 (13) | 0:2184, 1:2146 |
| PG(2,4) | 21 | 180,058 | 1 | 0 | 9 | 7 (360), 9 (11,480) | 0:89,799, 1:90,259 |

全極大サイズが奇数なので K1298 より Grundy は `{0,1}`、空盤は先手勝ち。

## 極大安全集合＝最小多重ブロッキング集合

| q | 安全サイズ（個数） | 補集合サイズ | 直線交差プロファイル | 構造 |
|---:|---|---:|---|---|
| 3 | 9 (13) | 4 | 1:12, 4:1 | 直線 |
| 3 | 7 (234) | 6 | 1:6, 2:3, 3:4 | **完全四辺形の 6 頂点**（単一 PGL(3,3) 軌道） |
| 4 | 9 (11,480) | 12 | {2:10,3:6,4:3,5:2} 10,080 / {2:9,3:9,5:3} 1,120 / {2:12,4:9} 280 | **3 個の PGL(3,4) 軌道**（固定群位数 6/54/216）。1,120 は 3 直線の三角形 |
| 4 | 7 (360) | 14 | 2:7, 4:14 | **Baer 部分平面 PG(2,2) の補集合**（Fano 7 点、360/360） |

q=3: 完全四辺形の個数 `C(13,4) − 13·4·9 − 13 = 234` と一致。
q=4: 生成群の位数 60,480 = |PGL(3,4)| を確認。三角形の個数
`C(21,3) − 21·C(5,3) = 1120` が 1,120 軌道と一致。14 点クラス 360 個は
Baer 部分平面 PG(2,2) の補集合（2 点直線 7 本の残り 3 点が Fano 平面、360/360 一致）。

## K_3

| q | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|
| v | 7 | 13 | 21 | 31 |
| K_3 | 7 | 9 | 9 | 11 |

Ball (1996) の `(k,n)`-arc 上界 `k ≤ (n−1)q+n` は n=3 で `2q+3`。
q=3 で tight（9）、q=4,5 は下回る。

## 限界

- 完全 Grundy は q≤4 のみ。q=5（v=31）は全列挙が非現実的。
- q=4 の 11,480 個の PGL(3,4) 軌道分解は未実施（群 60,480）。
- K_3 の q≥7 は未計算。
- 12 点 2 重ブロッキング集合の分類は未着手。
