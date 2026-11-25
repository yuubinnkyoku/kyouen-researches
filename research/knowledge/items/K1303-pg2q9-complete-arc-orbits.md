---
id: K1303
title: "PG(2,9) の完全アーク — サイズ 6,7,8,10 はそれぞれ PGL(3,9) の単一軌道"
kind: computation
status: computed
topics: [geometry, maximal-safe, statistics]
aliases:
- complete arcs of PG(2,9) are projectively equivalent within each size
- PGL(3,9) orbits of complete arcs
- complete 7-arcs in PG(2,9)
relations:
- type: related
  target: K1300
  note: PG(2,9) のキャップ国勢調査（極大 6/7/8/10 の個数）を軌道計算で精密化
- type: related
  target: K1298
  note: パリティ混在（7 が奇数）から Grundy ≥2 が出る盤の幾何的構造
- type: related
  target: K1253
  note: アーク（キャップ）と共演ゲームの関係
artifacts:
- path: research/experiments/pg2q9-cap-game-20261125/report.md
  role: log
  note: 国勢調査と軌道計算の総括
- path: research/experiments/pg2q9-cap-game-20261125/scripts/orbit_bfs.c
  role: solver
  note: 91 点盤の 128-bit マスク軌道 BFS
- path: research/experiments/pg2q9-cap-game-20261125/output/orbits.txt
  role: data
  note: サイズ別の軌道サイズと固定群の位数
- path: research/experiments/pg2q9-cap-game-20261125/output/gens.txt
  role: data
  note: PGL(3,9) の生成元 8 個（91 点の置換）
- path: research/experiments/pg2q9-cap-game-20261125/independent_orbits/REPORT.md
  role: log
  note: 軌道の独立検証（独自生成元・第 2 アークとの射影変換・固定群構造 A5/C7:C3/D4/PGL(2,9)）
scope: PG(2,9)（91 点、91 直線）上の完全アーク（どの点も追加できないキャップ）。サイズ 6,7,8,10 の極大キャップと PGL(3,9) の作用。
evidence: 極大キャップ数は国勢調査（K1300）で 6:707,616、7:2,021,760、8:5,307,120、10:58,968（9 は 0）。PGL(3,9) の生成元 8 個（GF(9) の transvection・対角・置換）による軌道 BFS で、各サイズの 1 個の完全アークの軌道サイズがちょうど全個数と一致（707,616 / 2,021,760 / 5,307,120 / 58,968）→ 各サイズは単一軌道。固定群の構造は 6-アーク A5 = PSL(2,5)、7-アーク Frobenius C7:C3、8-アーク D4、10-アーク PGL(2,9)（位数 720、円錐曲線上で鋭 3-推移。S6 ではない）。独立検証（独自生成元 14 個、第 2 の完全アークとの明示的射影変換 60/21/8/720 要素、固定群の完全列挙）が全項目 PASS、不一致 0。9-アークは存在しない（すべて円錐曲線に延長）。
---

# PG(2,9) の完全アークの軌道

## 結果

| サイズ | 極大キャップ数 | 軌道サイズ | 単一軌道 | 固定群 |
|---:|---:|---:|---|---:|
| 6 | 707,616 | 707,616 | ✓ | A5 = PSL(2,5)（60） |
| 7 | 2,021,760 | 2,021,760 | ✓ | Frobenius C7:C3（21） |
| 8 | 5,307,120 | 5,307,120 | ✓ | D4（8） |
| 10 | 58,968 | 58,968 | ✓ | PGL(2,9)（720、鋭 3-推移） |

- **完全 6-, 7-, 8-, 10-アークはそれぞれ PGL(3,9) の単一軌道**。
- 固定群の構造: 6-アークは **A5 = PSL(2,5)**（6 点上 2-推移）、7-アークは **Frobenius C7:C3**、
  8-アークは **D4**、10-アークは **PGL(2,9)**（円錐曲線上で鋭 3-推移、位数 720。S6 ではない）。
- 9-アークは存在せず、すべて円錐曲線に延長される（K1300）。
- 独立検証: 独自生成元 14 個で軌道 707,616 / 2,021,760 / 5,307,120 / 58,968 を再現し、
  第 2 の完全アークとの明示的射影変換（60/21/8/720 個）も構成。
  14 生成元が PGL(3,9) 全体を生成すること（指数が gcd(60,21,8,720)=1 を割る）も確認。

## 方法

- 国勢調査（K1300）で極大キャップの個数を確定。
- GF(9) 上で PGL(3,9) の生成元（transvection 6 個・対角・座標置換の 8 個）を
  91 点の置換として構成。
- 各サイズの完全アークを 1 個ずつ取り、C の軌道 BFS（128-bit マスク、ハッシュ集合）
  で軌道サイズを計算し、全個数と比較。

## 意義

- PG(2,9) の完全アークはサイズごとに一意な射影類しかない、という強い一様性。
- サイズ 7（奇数）の完全アークの存在が K1298 のパリティ混在・Grundy ≥2 の
  幾何的起源になっている。
