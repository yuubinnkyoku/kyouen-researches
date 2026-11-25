---
id: K1304
title: "PG(2,9) の 3-, 4-キャップは単一軌道で Grundy 値はそれぞれ 1, 0"
kind: computation
status: computed
topics: [geometry, grundy, maximal-safe]
aliases:
- all three-caps of PG(2,9) have Grundy 1
- all four-caps of PG(2,9) have Grundy 0
- PGL(3,9) orbits of small caps
relations:
- type: related
  target: K1303
  note: 完全アークの軌道分類（サイズ 6,7,8,10）と合わせ、小キャップ側の軌道・Grundy 値
- type: related
  target: K1300
  note: PG(2,9) のキャップ国勢調査（3-キャップ 110,565、4-キャップ 1,769,040）
- type: related
  target: K1298
  note: パリティ特性定理と局所形の注意（G はオービット不変、S 自身の G は極大拡大のパリティと同値でない）
artifacts:
- path: research/experiments/pg2q9-cap-game-20261125/report.md
  role: log
  note: 軌道と Grundy 値の総括
- path: research/experiments/pg2q9-cap-game-20261125/scripts/cap_grundy.py
  role: solver
  note: キャップのアップセット上の完全 DP で Grundy を計算
- path: research/experiments/pg2q9-cap-game-20261125/output/small_cap_grundy.json
  role: data
  note: 3-キャップ G=1（31,681 局面）・4-キャップ G=0（1,868 局面）
- path: research/experiments/pg2q9-cap-game-20261125/output/orbits_small.txt
  role: data
  note: 3-キャップ軌道 110,565（固定群 384）・4-キャップ軌道 1,769,040（固定群 24）
- path: research/experiments/pg2q9-cap-game-20261125/independent_small/REPORT.md
  role: log
  note: 独立検証（点番号の復元・軌道集合の一致・アップセット DP・全 42 五キャップ G=1）
scope: PG(2,9)（91 点、91 直線）上のキャップ（どの直線とも高々 2 点）のうちサイズ 3, 4（および参考として 5, 6）。PGL(3,9) の作用と、通常プレイ共演ゲームの Grundy 値。
evidence: 国勢調査（K1300）で 3-キャップ 110,565、4-キャップ 1,769,040。PGL(3,9) の生成元 8 個による C 軌道 BFS で、1 個の 3-キャップの軌道サイズが 110,565、1 個の 4-キャップの軌道サイズが 1,769,040 と全個数に一致 → いずれも単一軌道（固定群の位数 42,456,960/軌道 = 384, 24）。アップセット上の完全 DP で Grundy を計算した。3-キャップ {0,1,10} は G=1（アップセット 31,681 局面、サイズ 3..10）、4-キャップ {0,1,10,20} は G=0（1,868 局面）。Grundy は自己同型不変なので、**すべての 3-キャップが G=1、すべての 4-キャップが G=0**。独立検証では点番号を盤データから復元して 91 直線を完全再現し、軌道を集合として一致確認（対称差 0）、固定群を実際の射影変換の列挙で 384/24 と確認、3-キャップの 64 個の 4-キャップ子はすべて G=0、4-キャップの 42 個の 5-キャップ子はすべて G=1 を全数確認した。6-キャップは一様でなく、極大 6-アークは G=0、非極大の {0,1,10,20,32,39} は G=2（K1300 の明示局面）。
---

# PG(2,9) の小キャップの軌道と Grundy 値

## 結果

| サイズ | キャップ数 | 軌道サイズ | 単一軌道 | 固定群 | Grundy |
|---:|---:|---:|---|---:|---:|
| 3 | 110,565 | 110,565 | ✓ | 384 | **1** |
| 4 | 1,769,040 | 1,769,040 | ✓ | 24 | **0** |

- PGL(3,9) は 3-キャップ・4-キャップに推移的（軌道サイズ = 全個数）。
- Grundy は自己同型不変なので、**すべての 3-キャップが Grundy 1、すべての 4-キャップが Grundy 0**。
- 計算は各代表のアップセット上の完全 DP（3-キャップ: 31,681 局面、4-キャップ: 1,868 局面）。

## 参考

- 5-キャップは単一軌道ではない（14,859,936 は |PGL(3,9)| を割り切れない）。
  4-キャップを含む **全 42 個**の 5-キャップが G=1（独立検証で全数確認）。
- 6-キャップは一様でない: 極大 6-アーク（707,616 個、単一軌道）は G=0、
  非極大の {0,1,10,20,32,39} は G=2。

## 意味

- PG(2,9) の Grundy 関数の一部（サイズ 3, 4 の全局面）を軌道不変性で厳密に決定。
- 完全アークの単一軌道（K1303）と合わせ、サイズごとの「射影類 × Grundy 値」の
  絵が小さいサイズから揃ってきた。
