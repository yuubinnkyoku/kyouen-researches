---
id: K1370
title: "t>=2 の補集合双対性確認と6盤の極大安全・最小重ブロッキング計数"
kind: computation
status: computed
topics: [maximum-safe, blocking-set, geometry, statistics]
aliases:
- t>=2 blocking duality confirmation six boards
- maximal safe vs minimal t-fold blocking counts for t>=2
relations:
- type: related
  target: K1365
  note: 補集合双対性の命題（既証明）。本項目は t>=2 インスタンスの初の全数確認
- type: related
  target: K1369
  note: 従来の t=1 4盤確認の総括
- type: related
  target: K1300
  note: PG(2,3) s=2 極大アーク 4:234・AG(2,4) s=2 サイズ集合 {4,6} との照合
- type: related
  target: K1355
  note: PG(2,4) s=3 極大 7:360, 9:11,480 との照合
- type: related
  target: K1357
  note: AG(2,5) s=3 極大サイズ集合 {9,10,11} との照合（個数は新規）
- type: related
  target: K1298
  note: PG(2,5) s=4 のサイズ偶奇混在が G>=2 を示唆（Grundy は未計算）
artifacts:
- path: research/experiments/t2-blocking-duality-20261128/output/summary.json
  role: data
  note: 6盤の全結果まとめ
- path: research/experiments/t2-blocking-duality-20261128/output/counts/all_counts.json
  role: data
  note: サイズ別個数
- path: research/experiments/t2-blocking-duality-20261128/README.md
  role: code
  note: 手順・3系統検証・non-claims
scope: 直線サイズ l の6盤（AG(2,3) s=2, PG(2,3) s=2, AG(2,4) s=2, PG(2,4) s=3, AG(2,5) s=3, PG(2,5) s=4）における、極大 s-安全集合と最小 t=l-s 重ブロッキング集合の完全列挙による全数・サイズ別個数、および補集合全単射の要素レベル確認。従来の4盤確認（K1369）はすべて t=1 であったのに対し、今回は t>=2 の初確認。
evidence: 2^n 全部分集合を1回の Gray-code 走査で判定する単一 C 列挙器（両側を各 mask で独立の直接論理で判定、要素レベル両方向補集合照合、全盤2回実行で byte-identical）で6盤を完全列挙した。PG(2,3) s=2: 極大 4:234・最小2重ブロッキング 9:234（最小サイズ 9=3q）。PG(2,4) s=3: 極大 7:360, 9:11,480（K1355 と一致）・最小 12:11,480, 14:360。AG(2,4) s=2: 極大 4:120, 6:48・最小 10:48, 12:120。AG(2,5) s=3: 極大 9:12,500, 10:28,000, 11:9,000（サイズ集合は K1357 と一致、個数は新規）・最小 14:9,000, 15:28,000, 16:12,500（新規）。PG(2,5) s=4: 極大 13:15,500, 14:372,000, 15:604,500, 16:595,975・最小 15:595,975, 16:604,500, 17:372,000, 18:15,500（両側とも新規、2^31 全走査）。AG(2,3) s=2: 極大 4:54・最小 5:54。補集合全単射は全盤で 0 fail。宣言前較正として t=1 の4盤（AG(2,4) s=3, PG(2,3) s=3, PG(2,4) s=4, AG(2,5) s=4）で出版値 1,240 / 247 / 10,741 / 36,475 とサイズ別内訳を完全再現。独立検証3系統: (1) 純 Python GF(q) 盤独立再構成 + 2-(v,k,1) 検査 + 全 dump mask の直接定義再判定（全盤 all_ok、PG(2,5) は約3分）、(2) 純 Python 第三全列挙（n≤25 の5盤で完全一致）、(3) 独立構成のラベル違い導出盤での列挙器再実行が全盤で同一 count。有限観察: PG(2,q) の最小2重ブロッキング最小サイズは q=3,4,5 で 3q（全称主張ではない）。
confidence: 完全列挙 + 3系統独立検証 + 宣言前較正。K1365 の命題自体は既証明であり、本項目は経験的確認と新規計数の記録。
open_questions:
- PG(2,q) の最小2重ブロッキング最小サイズ = 3q の一般証明（q=7 は n=57 で全列挙不可）
- AG(2,5) s=3 の最小2重ブロッキング 14 点集合の構造分類
- PG(2,5) s=4 の Grundy 値（K1298 から G>=2 の存在が示唆）
---
[実験キット](../../../experiments/t2-blocking-duality-20261128/README.md)（宣言 [9def0879](../../log/2026-11-28-t2-blocking-duality-declaration.md)）。

主結果表:

| board | s | t | 極大安全 | 最小t重ブロッキング |
|---|---|---|---|---|
| AG(2,3) | 2 | 1 | 4:54 | 5:54 |
| PG(2,3) | 2 | 2 | 4:234 | 9:234 |
| AG(2,4) | 2 | 2 | 4:120, 6:48 | 10:48, 12:120 |
| PG(2,4) | 3 | 2 | 7:360, 9:11,480 | 12:11,480, 14:360 |
| AG(2,5) | 3 | 2 | 9:12,500, 10:28,000, 11:9,000 | 14:9,000, 15:28,000, 16:12,500 |
| PG(2,5) | 4 | 2 | 13:15,500, 14:372,000, 15:604,500, 16:595,975 | 15:595,975, 16:604,500, 17:372,000, 18:15,500 |

補集合全単射は全盤で 0 fail（両方向）。詳細な手順・non-claims はキット README 参照。
