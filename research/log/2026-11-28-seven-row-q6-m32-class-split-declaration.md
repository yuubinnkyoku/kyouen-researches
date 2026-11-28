# 2026-11-28 seven-row q6 7x32 class {3} krow/minpos split 宣言

高速レーン・単一オーナー・publish-then-execute。宣言時 HEAD `40a05ee36b180a0426fa8d45216efed1940bcff0` (2026-11-28T01:22Z)。

## Claim (single-owner)

- 本レーンは **(7,6) 前線 7x32 の class {3} krow/minpos 分解掃引**を着手する
  (sat3.js class-split・cap 272s・sandbox bash piece cap 内の逐次実行)。
- 着手時点の境界: witness 帯 m=6..31 (m=31 は 34 石 rows [5,5,5,4,5,5,5]・2 編集 surgery で構成)・
  **M_{7,6} ∈ [32, 862]** (上界 K0318 substitution U=862)。
  7x32 の既存 honest negatives: two-edit surgery 完全列挙 負 (2,224,675 候補 0 safe-maximal・
  seven-row-q6-m32-two-edit-surgery-20261127)・class {3} krow=3:4 minpos=0 INDET 1,240,713 @260s
  (同 kit・m=31 krow=3:4 INDET 1,279,251 @250s)・m=32 plain class {3} CNF は同 kit で生成済み。
- 分解の soundness: class {3} = 欠損行は行3のみ (石数 ≤4)、他行は exactly 5。
  krow=3:k で行3の石数を k に固定し、minpos=P で行3の最左石を列 P に固定する H-split。
  H (列 x → 31−x) は行構造を保存するので min(x1, 31−x_last) ≤ 15 が成り立ち、
  **P=0..15 の 16 片で各 k ∈ {1,2,3,4} を完備分割**する。k=0 は単一インスタンス。
  全片 UNSAT ⟹ (7,32,6) class {3} 不在が確定 (71 クラス全体の不在ではない)。
  **SAT ⟹ 7x32 witness で witness 帯は m=32 に延伸し M_{7,6} ∈ [33, 862]**。
- INDET は cap 到達であり不在主張ではない。conflicts は bookkeeping。

## 実行順 (事前登録)

1. 正対照・較正 (宣言前実施・下記開示)。
2. k=4: minpos P=0..15 (16片・昇順)。
3. k=3: minpos P=0..15。
4. k=0 単一片、k=2 / k=1 (時間が許す限り)。
5. SAT 発見で即時打ち切り・witness の二系統検証 (sat3 decode verifyConfig + verify_witness.py Fraction)・
   kit 出版・CSV 行更新。

## 較正 (宣言前実施・全て本 host)

- sat3.js md5 `d03f908ea99ba819caee2a6fbb471c1b`・sat2.js `282ae832efa0080127c6c153e65e1c3c`・
  sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・verify_witness.py `0530d166572987988a01ec40dee12d4c`
  (seven-row-q6-m32-two-edit-surgery-20261127/scripts と byte 一致)。
- kissat 4.0.4 official linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325`。
- **CNF 決定性較正**: (7,31,6) class {3} plain CNF md5 `48eb715f96ac1f0be4a8c5429025483d`
  = m31 kit 出版値 bit-exact。** (7,32,6) class {3} plain CNF md5 `bc10c516134c8fff56a20f42f0bf6d61`
  = m32 surgery kit 出版値 bit-exact (156,185 vars / 547,944 clauses)。**
- SAT 側 pipeline 対照: (7,8,6) class {3} SAT 814 conflicts・decode verifyConfig ok
  (30 石 rows [5,5,5,0,5,5,5]) + verify_witness.py Fraction PASS。
- 負対照: 2x9 q4 class {0} UNSAT 517 conflicts = 出版値 bit-exact。

## Not claimed

- class {3} 以外の 70 クラス・7x33 以降・(7,q≠6) 家族・Grundy・
  11x11 関連 (全時点 UNKNOWN・verdict 不消費)。
