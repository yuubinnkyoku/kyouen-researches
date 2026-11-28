# five-row-q5-m27-minpos-sweep-20261115

高速レーン。**COMPLETED (2026-11-28 takeover・宣言 `24736c72`・単一オーナー・publish-then-execute)**。
停滞していた 2026-11-15 レーン (p1..p3 出版後に実行環境喪失・13日停滞) を
2026-11-28 高速レーンが takeover し p4..p13 掃引を実施・**p=9 で SAT**。

## 結果

- **(5,5) 前線 5×27 class {0} krow=0:3 minpos=9 は SAT**:
  kissat 4.0.4 **1,556,533 conflicts / 169.09s**・19石 witness
  rows [3,4,4,4,4] (row0 x=[9,19,21])。
  2系統検証: sat3.js decode → sat.js verifyConfig ok・
  verify_frac.py (独立 Fraction 実装) safe+maximal ok (max_curve_stones=4・unblocked=[])。
  cold pair 再実行: conflicts bit-exact・v-line 同一。
- **witness 帯は m=5..27 に延伸し M_{5,5} ∈ [28, 336]** (着手前 [27, 336]・上界 K0318 U=336 不変)。
  **前線は 5×28 へ。** CSV・K0833 更新済み。
- p4..p8 は cap 285s INDET (honest negatives・不在主張ではない):
  p4 2,290,237 / p5 2,255,250 / p6 2,526,618 / p7 2,423,463 / p8 2,525,494 conflicts。
  旧レーンの reported-only 手記値 p4/p5 (3,317,615 / 3,501,337 @400s) は本再実行で置き換え。
- p1..p3 は旧レーン出版値のまま (再実行せず): INDET 2,961,487 / 3,233,600 / 3,398,950 @400s。
- **p10..p13 は未掃引 (WIN-stop)**。k=0..2・他の正準欠損クラス・H/V 鏡像類も残る。
  5×27 全体の不在主張ではない (sat3 H-split の一部クラスの掃引である)。

## 較正 (takeover・宣言前実施・宣言 `24736c72` で開示)

- 生成器: sat3.js md5 d03f908ea99ba819caee2a6fbb471c1b (sat2 282ae832efa0080127c6c153e65e1c3c・
  sat.js 0cc6021a4e523a0d7f4d5ea0f5f5d40c)。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325。
- CNF md5 bit-exact: 5×27 c0k3p0 4d2b52a8203591e13cfc8ae126beb9b5・
  c0k3p1 6808000255911616de71430c6a0080cb・c0k3p2 47b3f40d6d636b4cf08a5b7765bf71b3・
  5×25 c0 1d62f2428fd5fb2fdba5cfd19114d78e・5×26 c0 60e71cfd2f1620cfa9b4070f259c1572。
- エンドツーエンド: 5×25 c0 SAT 35,972 conflicts / 9.16s・5×26 c0 SAT 1,631,556 conflicts / 204.22s
  — いずれも出版値と conflicts bit-exact。
- cap は旧計画 400s から **285s に変更** (実行環境の呼び出し上限 300s 内・宣言で開示)。

## 元計画 (2026-11-15・停滞時点の記録として保持)

- 本レーンは **(5,5) 前線 5×27 の class {0} krow=0:3 minpos p=1..13 掃引**を着手する
  (sat3.js・resumable)。`five-row-q5-m26-extend-20261115`(COMPLETED)が委譲した残り minpos 帯。
  sound H-split bound: min(x₁, 26−x₃) ≤ ⌊(m−1)/2⌋ = 13。
- SAT ⟹ witness 帯は m=5..27 に延伸し M_{5,5} ∈ [28, 336]。
  全 p UNSAT でも単独で 5×27 不在は確定しない (k=0..2・他クラス残る)。
  INDET は cap 到達であり不在主張ではない。

## 進捗 (2026-11-15・停滞時点の記録として保持)

- p=1..3 着地済み (INDET・records 3件)。p4/p5 はローカル完走も push 前に実行環境喪失で
  raw log・records とともに喪失 (手記値のみ・reported-only)。records.jsonl には p1..p3 のみ。

## 成果物

- output/records.jsonl: p1..p3 (旧レーン) + 較正2件 + p4..p9 + c0k3p9.p2 (cold pair)
- output/rc5x25q5_c0.txt / rc5x26q5_c0.txt (較正 raw logs)
- output/r5x27q5_c0k3p4.txt .. r5x27q5_c0k3p9.txt (p4..p9 raw logs)
- output/r5x27q5_c0k3p9.p2.txt (cold pair raw log)
- output/witness_5x27_c0k3p9.json / witness_5x27_c0k3p9_stones.json

## スコープ

有限機械検証まで。SAT は witness 存在証明。UNSAT は符号化限定の不在。
INDET は cap 到達であり不在を意味しない。上界不変: K0318 U_{5,5}=336。
標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
全 closure class は全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。
