---
id: K0781
title: 剰余放物線Q_2531はサイズh+1=1266の集合を持たず、上界はh=1265に下がる（ソルバ主張、証明書未検査）
kind: proposition
status: needs-review
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2と、サイズh+1の集合が(x,c,e)で3形状に尽きること
- type: depends_on
  target: K0702
  note: サイズh+2=1267の不存在（単一CNF・監査済み）からA(2531)<=1266、本項はそこから1下げる
- type: depends_on
  target: K0001
  note: 安全集合の定義（整数平面で共円・共線の四点を含まない）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-2531-1266-shapec/a2531_1266.cnf
  role: data
  note: 形状(c)（0＋一完全対＋一空対＋各対一側）の単一CNF。10,118変数・62,189節、sha256 896a4efa...
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_c_2531_unsat.json
  role: manifest
  note: ソルバ・実行コマンド・開始/終了時刻・結果の記録
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_class_2531_1266.json
  role: data
  note: 形状(a)(b)のUNSAT記録（4.1秒・7.5秒、200万衝突予算）
- path: research/log/2026-11-13-p2531-no-size-h1-set.md
  role: log
  note: 発見の経緯と当時の検証状態、4素数を並べた表
scope: p=2531のみ。形状(a)(b)は既存記録のUNSAT、形状(c)はcadical 1.7.3の既定設定によるUNSAT主張。
evidence: 形状(a)(b)はshape_class_2531_1266.json。形状(c)はCNFのsha256固定済みで cadical が約5,920秒で`s UNSATISFIABLE`。DRAT証明書は再生成中で未検査。
---

## 主張

`p = 2531`（`h = 1265`）について、サイズ `h+1 = 1266` の安全集合は存在しない。したがって

```
A(2531) <= 1265 = h
```

## 根拠

サイズ `h+1` の集合は `x + c - e = 1` から3形状に尽きる。

| 形状 | `(x,c,e)` | 判定 | 記録 |
|---|---|---|---|
| (a) | `(1,0,0)` | UNSAT | 4.1 秒（200万衝突予算） |
| (b) | `(0,1,0)` | UNSAT | 7.5 秒（同） |
| (c) | `(1,1,1)` | UNSAT | cadical 1.7.3 既定設定、約 5,920 秒（98 分） |

- 形状(c)のCNFは `search_1104_shape_c.py --write-cnf` で再生成でき、sha256 が
  `896a4efa25a0a73666ca63cf584c4c87685f290b92182aa66fc91a91699bd233` に一致する。
- 同じ符号化は p=2207 で1104点のモデルを返すので（K0722）、符号化の健全性は別経路で裏づけ済み。
- 99 分かけて決着したのは、`--sat` 寄り設定ではなく**既定設定**の長時間走行だった。

## 4 つの等号不達成素数の現在地

| p | h | h+2 | h+1 = サイズ形状3種 | 上界 | 下界 |
|---|---|---|---|---|---|
| 2207 | 1103 | UNSAT（証明済み） | (c) が **SAT**（K0722） | **1104 = h+1** | 1104 |
| 2531 | 1265 | UNSAT（証明済み） | 3形状すべて UNSAT（本項） | **1265 = h** | 未確定 |
| 2647 | 1323 | UNSAT（証明済み） | 3形状すべて UNSAT | 1322（K0711） | 1303（K0711） |
| 3251 | 1625 | UNSAT（証明済み） | 3形状すべて UNSAT（K0775） | **1625 = h** | 未確定 |

「h+2 は無理でも h+1 は届く」は p=2207 だけの話で、2531・2647・3251 は `h` 以下に落ちる。

## 限界

- 証明書の検査を実行中（5.26 GB のテキスト DRAT）。先頭 400 MB を別プロセスで検査して
  790,809 step すべて RUP・削除の取りこぼし 0 を確認済み（1,925 秒 = 218 KB/s）。
  この速度なら全体は約 6.7 時間。完了まで status は `needs-review` のまま。
- 下界は K0787 が与える: `A(2531) >= 1262`（独立整数幾何監査済み）。よって
  `1262 <= A(2531) <= 1265`。サイズ `h=1265` の4形状のうち (0,0,0) と (1,0,1) は UNSAT、
  (0,1,1) と (1,1,2) は走行中。
