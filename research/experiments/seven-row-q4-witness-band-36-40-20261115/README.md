# seven-row-q4-witness-band-36-40-20261115 — (7,4) witness帯の36..40へのSAT延伸（下界 36→41）

Date: 2026-11-15
Lane: 高速レーン（seven-row-q4-extension-band-sat3-20261115 の直接の続き）
Status: COMPLETED

## 概要

sat3 streaming census（seven-row-q4-extension-band-sat3-20261115・sat2.js と
byte-identical）により、K0827 構成的延伸帯の先端 m=35 の先を SAT 探索した。
**m=36..40 の全5幅で行欠損極大 witness が SAT で発見され2系統検証 PASS** —
(7,4) の witness 帯は 35 で終わっておらず、**M_{7,4} ≥ 41**（従来36から更新）。

## 結果（全幅 SAT・kissat 4.0.4・200s cap・sat3 生成）

| m | gen(s) | kissat(s) | conflicts | 石数 | rows |
|---|---|---|---|---|---|
| 36 | 6.0 | 16.1 | 402 | 20 | [3,3,3,3,3,2,3] |
| 37 | 6.0 | 15.7 | 117 | 20 | [2,3,3,3,3,3,3] |
| 38 | 7.0 | 19.1 | 137 | 20 | [3,3,3,2,3,3,3] |
| 39 | 7.3 | 26.0 | 230 | 20 | [2,3,3,3,3,3,3] |
| 40 | 7.9 | 27.8 | 280 | 20 | [2,3,3,3,3,3,3] |

- 全 witness は decode_verify.js（sat.js verifyConfig・census不使用）と
  verify_witness.py（Python Fraction・独立実装）の2系統で safe+maximal+行欠損 PASS。
- 行マルチセットは全幅 {3,3,3,3,3,3,2}（20石）— m=28..35 の sat3 witness と同一。
- m=40: 8,101,031 clauses・CNF 155MB・kissat 27.8s。

## スコープ

有限機械検証。m=36..40 の各幅の witness 存在は完全証明（SAT+2系統検証）。
**M_{7,4} ∈ [41, 1929]**（下界更新・上界は K0068/K0318 のまま）。
witness 帯の真の前線は未確定（m=41 以降は本バッチでは未実施・不在主張ではない）。
sat3 の探索は m=41 以降も継続可能（生成 <10s/幅）だが、sat3 の dedup Set が
m=50 生成で OOM（rc 137・全円キー保持のため）→ ≥q円のみ登録する修正が
次バッチの課題（3点円は三つ組が1つしかなく dedup 不要のため出力不変）。

## ファイル

- `output/records.jsonl` — m=36..40 の5レコード（cnf_md5 付き・CNFは実行後削除）
- `witnesses/s7x36..40q4.witness.json` — デコード済み witness
- `raw-logs/` — 代表3本の kissat ログ（model 行は容量削減のため除去）
- 使用スクリプト: `seven-row-q4-extension-band-sat3-20261115/scripts/`
  （sat3.js・leanband4.sh・decode_verify.js・verify_witness.py・sat.js と同一コマンド列）
