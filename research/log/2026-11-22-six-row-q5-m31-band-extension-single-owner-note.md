# 2026-11-22 six-row (6,5) 6x31 band extension — single-owner declaration note

- 日時: 2026-11-22T01:05Z付近・宣言時HEAD `3b6c23b3c40e0307bafdf78931c9cb263ec5d0da` (2026-11-22T00:57:36Z)
- オーナー: 高速レーン（本セッション・単一オーナー）。

## 背景（正直記録）

knowledge 側に先行セッション（2026-11-21 19:06–19:12Z頃・環境リセットで中断）の
staging kit `knowledge/kyouen-research/_sixrow-lane-kit/` が残存しており、その中に
**repo 未出版**の (6,5) 6x31 witness 候補
`found/w6x31q5_L2shift1.json`（K0815 第6弾 L2 6x30 witness の x+1 平行移動・23石・rows [4,4,4,4,4,3]）
と、3系統検証器（`det_q_verify.py` det3/det4 ゼロ判定・`surgery_gen.js` 整数正準曲線鍵・
`append_criterion.py` 純Python Fraction〔sha256 `d08d8fb1…`＝出版pinと一致〕）、
6x32 bounded-surgery の 18-base 陰性 checkpoint、配置census表があった。
先行セッションは **repo への宣言・出版を一切行っていない**（2026-11-21 19:00Z 以降の
コミット列に該当なし・CSV/knowledge README に 6x31 の記録なし）。
本レーンはこの未出版候補を**生の石座標から再検証**して出版し、レーンを完走させる。
先行 kit の出力ビットは一切 utilise せず、全実行を本セッションで再実行する。

## 宣言スコープ（claim）

1. **(6,5) 6x31 witness の出版**: 候補配置の 3系統独立検証（受入条件は下記）と
   陽性/陰性対照を添え、下界更新 **M_{6,5} ∈ [32, 658]** として出版する
   （下界のみの主張・6x32 以降の存在不在は主張しない）。
2. **配置census（全数）**: 出版済み (6,5) witness プール（K0808 m<=19・
   six-row-q5-q6-frontier-20261120 m=19..29・extended.json 6x29・w65_30 2件・L2 6x30）
   の D4 像 × 全配置 x-offset について free-append census
   （`append_criterion.py` Fraction + `census_shift.py`）を実行し、
   配置ごとの被覆幅帯を記録する。band top 31 超えの配置は全て 3系統で再検証する。
3. **6x32 以降の bounded surgery hunt**: m=30 witness 群（a0/a1/L2 の D4 像・全 offset）と
   census で得た新配置を base とし、single-move / rem2add1 / rem2add2（必要なら
   rem3 add1/add2）の編集予算で 6x32, 6x33, ... の witness を構成的に探索する。
   発見れば同様に 3系統検証・出版し、cascade する。陰性は編集近傍内の限定陰性として
   記録する（不在主張ではない）。

## 受入条件（witness 出版ゲート）

- 3系統すべて PASS: (a) `surgery_gen.js --verify`（整数正準曲線鍵・safety+全盤maximality+行欠損）
  verdict WITNESS_OK、(b) `det_q_verify.py`（純3x3/4x4行列式ゼロ判定・曲線方程式非形成）
  safe+maximal_at_m+deficient、(c) `append_criterion.py`（純Python Fraction・出版pin同一バイナリ）
  safe+old_uncovered 0+対象幅まで被覆。
- 陰性対照: tamper（1石移動2種）が両系統で FAIL（unsafe/not-maximal）、5同行制御が FAIL。
- 陽性対照: 出版済み L2 6x30 witness が同経路で WITNESS_OK 再現。
- 決定性: 検証 2回実行で出力 byte 一致。
- 主張は witnessed band の下界更新のみ。真の安定化長の全帯閉包・不在主張はしない。

## 非目標（着他レーンとの境界）

- **(6,6) m=25 frontier crunch**: 宣言済み `2c3254ef9f`（00:26Z）の並走レーンが所有。**非接触**。
- **(6,7) 6x22 rowfixed y-split**: 宣言済み `24a98f89d3`（00:21Z）の並走レーンが所有。**非接触**。
  （先行 staging kit に c66_m25 / c67_m22 の surgery 設定が残っていたが本レーンでは実行しない。
  m=24 witness は K1215 で出版済み・m=25 は上記 crunch レーン管轄。6x21 q=7 witness は K0815 出版済み。）
- n11 系（sixth-cost・s4bd・thirdimpl）: 非接触。
- 標準 11x11 空盤・二石 root・S2・class 1/2/4: 本レーン非接触で UNKNOWN のまま。
- 11x11 巨大探索・数時間 root 証明: 本レーンの主目的ではない。

## 手法メモ

- safety は幅非依存（K0853 lemma 1）。blocked 性は (S,c) のみで決まる（同 lemma 2）。
  よって配置 S を x-offset s に置いた盤幅 m2 での極大性は
  「旧列領域の空セル被覆（old_uncovered==0）」と「右端列の free-append reach」で判定できる。
- 編集手術の行欠損保存: def-mode witness は高々 w(q-1)-1=23石で、23石 base からの
  純追加は不可。編集予算は |add|<=|rem| に自動的に制限される。
- conflicts 数・leaves 数・checked 数を勝敗として読まない。
