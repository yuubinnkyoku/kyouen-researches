# seven-row-q4-band-41-20261115 — (7,4) m=41 SAT（下界42）とソルバRAM壁の記録

Date: 2026-11-15
Lane: 高速レーン（seven-row-q4-witness-band-36-40-20261115 の直接の続き）
Status: COMPLETED

## 概要

sat3 の dedup 修正（≥q点円のみ Set 登録・出力不変: q点未満の円は三つ組が1つしか
なく再遭遇しない）を加え、(7,4) witness 帯をさらに1幅伸ばした。生成の壁は解消したが、
今度は **kissat の RAM 壁**（本コンテナで ~9M clauses）に到達した。

## 結果

- **m=41 SAT**（281 conflicts・39.0s・8,704,218 clauses・20石
  rows [3,3,3,3,3,3,2]・js+py 2系統検証 PASS）→ **M_{7,4} ≥ 42**
  （witness 帯 7×4..7×41・下界36→42）。
- **m=42**: 生成6.7s OK（9,337,618 clauses）・kissat はパース中に OOM kill
  （rc 137・13s・不在主張ではない）。**ソルバ壁 ~9M clauses（本コンテナRAM）**。
- **m=50**: 修正済み sat3 で生成 OK（446,731 curves・15,519,624 clauses・CNF 305MB・
  11.6s）・kissat はパース中に OOM kill（rc 137・2s）。
- sat3 dedup 修正の検証: 小規模4対照 + m=28/m=40 の保存CNFとの byte-identity
  （cmp MATCH・出力不変）。

## スコープ

有限機械検証。m=41 の witness 存在は完全証明。**M_{7,4} ∈ [42, 1929]**。
前線 7×42（未実施・不在主張ではない）。以降の幅は生成可能だが
kissat が本コンテナのRAMで落ちるため、より大きいメモリ環境・節削減符号化
（例: q4向けの対称性破壊強化・変数分割）・または構造論証が必要。

## ファイル

- `output/records.jsonl` — m=41 SAT + m=42/m=50 OOM 負記録の3レコード
- `witnesses/s7x41q4.witness.json` / `raw-logs/` — witness と代表ログ
- `scripts/sat3.js` — dedup 修正版（≥q円のみ登録・byte-identical・検証済み）
