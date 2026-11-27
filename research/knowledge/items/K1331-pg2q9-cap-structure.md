---
id: K1331
title: "PG(2,9) のキャップ構造 — サイズ別 conic/極大分解（非 conic 非極大 7-キャップ = |PGL(3,9)|）"
kind: computation
status: computed
topics: [geometry, maximum-safe]
aliases:
- structure of caps in PG(2,9) by size, conic and maximality
- decomposition of PG(2,9) caps
relations:
- type: related
  target: K1321
  note: PG(2,9) の円錐曲線レイヤー（conic k-キャップの個数と軌道）
- type: related
  target: K1300
  note: PG(2,9) のキャップ国勢調査（サイズ別個数）と極大サイズ
- type: related
  target: K1303
  note: PG(2,9) の完全アーク（極大キャップ）の軌道
- type: related
  target: K1305
  note: PG(2,9) の 5-キャップ 2 軌道
artifacts:
- path: research/experiments/pg2q9-cap-game-20261125/output/conic_layer.json
  role: data
  note: conic k-キャップの個数
- path: research/experiments/pg2q9-cap-game-20261125/output/census_pg2q9.txt
  role: data
  note: サイズ別キャップ数と極大数
- path: research/experiments/s-parameter-kyouen-20261125/output/grundy_pg2q5_s3.txt
  role: data
  note: 参照用（PG(2,5) s=3 の Grundy）
scope: PG(2,9)（91 点、91 直線）上のキャップ（k=5..10）の、conic 部分集合・極大キャップ・非 conic 非極大への分解と個数。
evidence: 国勢調査（K1300）と conic レイヤー（K1321）・極大キャップ（K1303）の個数から、k=5 は全 14,859,936 が conic（非 conic 0、極大 0）。k=6 は全 52,009,776 = conic 12,383,280 + 非 conic 39,626,496、極大 707,616 は非 conic に含まれる。k=7 は全 51,554,880 = conic 7,076,160 + 極大 2,021,760 + 非 conic 非極大 **42,456,960**。k=8 は全 7,960,680 = conic 2,653,560 + 極大 5,307,120（非 conic はすべて極大）。k=9 は全 589,680 が conic（非極大、conic 10 へ延長）。k=10 は conic 58,968 がすべて極大。非 conic 非極大 7-キャップ 42,456,960 は |PGL(3,9)| = 42,456,960 と一致する。**独立検証（5/5 PASS）により構造的**と判明し、非 conic 非極大 7-キャップは **2 個の PGL(3,9) 軌道（各 |PGL|/2 = 21,228,480、固定群 2）**に分かれる（代表 {11,22,29,32,44,61,89} と {11,22,32,41,44,61,89}）。
---

# PG(2,9) のキャップ構造（サイズ別分解）

| k | 全体 | conic | 非 conic | 極大 |
|---:|---:|---:|---:|---:|
| 5 | 14,859,936 | 14,859,936 | 0 | 0 |
| 6 | 52,009,776 | 12,383,280 | 39,626,496 | 707,616 |
| 7 | 51,554,880 | 7,076,160 | 44,478,720 | 2,021,760 |
| 8 | 7,960,680 | 2,653,560 | 5,307,120 | 5,307,120 |
| 9 | 589,680 | 589,680 | 0 | 0 |
| 10 | 58,968 | 58,968 | 0 | 58,968 |

- k=5 は全キャップが conic（任意の 5 点は一意な conic 上）。
- k=9 は全キャップが conic（K1321）で、conic 10 へ延長されるため非極大。
- k=8 は非 conic の 5,307,120 個がすべて極大（complete 8-arc）。
- **k=7 の非 conic 非極大キャップは 42,456,960 = |PGL(3,9)|** で、2 個の PGL 軌道（各 21,228,480、固定群 2）に分かれる。
- k=6 の極大 707,616 は非 conic に含まれる。
