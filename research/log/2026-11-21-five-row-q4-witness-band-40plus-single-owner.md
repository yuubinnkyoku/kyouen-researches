# five-row-q4 witness band m=40+ — single owner declaration

- **宣言時刻**: 2026-11-21T17:20Z 頃（Vibe 高速レーン instance）
- **宣言時 HEAD**: 047d3d517c65fc5284c5b2c1faef6ca39ed852a4
- **owner**: この宣言を出した instance（失効時は最新 main の IN FLIGHT
  確認の上、他レーンが takeover 可）

## 対象・目的

(5,4) witness band（現在 m=5..39・M_{5,4} ∈ [40, 567]）の m=40+ 延伸に
ついて、以下を**この instance が単独で**進める:

1. **R(S) census（無料）**: K0853 自由列追加判定（append_criterion.py・
   four-six-row-q4-q5-band-extension / free-column-append-criterion-20261115
   配下の published 実装・Fraction）で m=37/38/39 witness（14石・単一欠損・
   maxx=36/36/37）の free-append reach R(S) を計算する。
   R ≥ 40 なら 幅 40..R が無料で witness 帯に加わり M_{5,4} ∈ [R+1, 567] が確定。
   R = 39 なら m=40 は真の前線として確認される。
2. **m=40 witness 構成探索（有料・条件付き）**: R(m39 witness) < 40 の場合のみ、
   m=37/38/39 witness を基底とする bounded-edit surgery（石追加/移動 ≤ 2 の
   近傍列挙・D4 鏡映 × 平行移動同値類縮約）で 5×40 盤の
   witness 検索を実施する。正の対照として、同一列挙器が m=39 盤で
   何らかの witness を再発見できることを先に確認する。對照が失敗した場合、
   負の結果は不在主張ではなく列挙器の感度の下界としてのみ記録する。
3. **副次 census（同宣言に含む・無料のみ）**: K1201 の (6,5) m=28・(6,6) m=24
   witness（six-row-q5-q6-frontier-20261120）と (6,7) m=21 witness
   （encoding-symmetry-kissat-20261114 配下）にも R(S) を計算。
   R ≥ 次幅なら無料 witness 帯延伸。**無料延伸の判定のみ**で、
   これらの前線の SAT/INDET 課題は先取りしない。

## 受入条件

- witness 主張は 2〜3 系統の独立整数幾何検証（append_criterion.py pin・
  独立 Node BigInt 実装・verify_witness.py pin）で全 PASS。
- 各 witness の rows・maxx・R(S) が criterion 出力と一致。
- 出版は上界 T_5=567（K0068）不変・下界有限 witness のみ。
- 有限実験を全称として主張しない（INDET/不在は区別）。

## 非目標（衝突回避）

- (4,4) m=35/36 hunt（four-row-q4-m35-neighborhood-hunt-20261121・他 instance）。
- (7,4) m≥60 band（2026-11-21-seven-row-q4-band-m60-single-owner 宣言済み）。
- (4,5) m=21/23 class-split、(6,5)/(6,6) SAT 前線（six-row-q5-q6-frontier lane）
  — 上記 3 の無料 census のみ実施。
- s(q)/K(q) 系・n11 系・fold 検証 — 非接触。

## collision protocol

- push 直前に毎回最新 main を再取得。同一対象への他レーンの IN FLIGHT 宣言や
  結果 push を検出した場合、本レーンは対象を外すか convergence を優先する。
- 失敗時は無理に進めず状況を記録して次回実行に回す。
