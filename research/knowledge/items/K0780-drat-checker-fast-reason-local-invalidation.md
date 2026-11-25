---
id: K0780
title: DRAT検査器の高速版（削除時はreasonのみ失効・節検索をhash化）は既存4証明書で同一判定のまま3〜11倍速い
kind: method
status: active
topics: [verification, search-methods, maximum-safe]
aliases: []
relations:
- type: depends_on
  target: K0707
  note: 削除で代入を失効させないと偽UNSATを受理する不具合と、その修正方針（reason単位の失効）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_fast.cpp
  role: verifier
  note: drat_check_incremental.cppの高速版。Zobrist hashの節索引＋reason単位の削除失効
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/validate_fast_checker.py
  role: verifier
  note: 既存4証明書の再検査と負の対照（リテラル反転・空節削除）を一括実行
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/fast_checker_validation.json
  role: data
  note: 4証明書の新旧時間・speedup・負の対照2件の拒否記録
scope: RUP/RATのDRAT証明書一般。ここでは repo の h+2 単一CNF証明書4件で検証した。
evidence: 4証明書すべてVERIFIED（receiptと一致）、負の対照2件はともに拒否。速度は同一マシンでの実測。
---

## 変更点（`drat_check_incremental.cpp` との差）

1. **削除節の探索を hash 化**。旧版は削除のたびに全節を後ろから線形走査していて、証明が大きいと
   二乗的時間になっていた。Zobrist hash で候補を引き、multiset 完全一致で確定する。
2. **level-0 の代入は、削除される節が現に代入の reason であるときだけ失効**させる。旧版は削除のたびに
   全代入を捨てていた（K0707 の安全側修正）。reason でない節を消しても、残る各代入の reason 連鎖は
   壊れないので健全性は保たれる。
3. level-0 の伝播を毎回やり直す部分（`qhead = 0`）は**そのまま残した**。ここを省くと
   p=2647 の証明が step 53058 で落ちた（watch を既に偽のリテラルへ移すときに伝播が閉じないため）。
   つまり「伝播の閉性」は現行アルゴリズムでは再伝播に依存している。

## 検証

| 証明書 | 旧検査器 (s) | 高速版 (s) | 倍率 | 判定 |
|---|---|---|---|---|
| cert-2207-1105（237,785 step） | 875.0 | 122.0 | 7.2x | VERIFIED |
| cert-2531-1267（86,533 step） | 103.5 | 35.1 | 3.0x | VERIFIED |
| cert-2647-1325（7,256 step） | 39.3 | 3.6 | 10.9x | VERIFIED |
| cert-3251-1627（93,926 step） | 185.6 | 54.6 | 3.4x | VERIFIED |

- 4件とも receipt の判定（VERIFIED）と一致（`matches_receipts: true`）。
- 負の対照: p=2647 証明のリテラル反転 → step 4097 で拒否。末尾の空節を削除 → 「no empty clause derived」で拒否。
- 出力: `output/fast_checker_validation.json`。

## 限界

- RAT を使う証明書では未検証（4件はすべて `rat=0`）。RAT の実装は旧版と同一だが、
  削除失効の局所化が RAT 経路でも健全かは証明ではなく議論（reason 連鎖の議論）に依る。
- 速度は実測であり、証明の形（削除の多さ）で倍率は変わる。
