# 2026-11-15 自由列追加判定補題（K0853）— 定式化・機械検証・(6,4) m=46 保留検証の完遂

高速レーン。

## 動機

- K0833 の (6,4) m=46 構成 witness（free-column append・ソルバ不使用）には
  「js+py 2系統検証は bash 環境復旧後に実施予定」という保留項目が残っていた。
  本セッションは bash が使えるので完遂した。
- 各レーン（(4,4) m=29/31/33/34 のシフト・(6,4) m=45→46 の空列追加）は
  per-instance で全盤走査（verifyConfig / pure-TS full-board scan）をして
  延伸可否を判定していた。この判定が「石集合に対する1回の列走査」に
  縮約できる一般補題だと気づいたので定式化・証明・実装した。

## 補題（K0853・全称）

1. 安全性は幅非依存（禁止配置は石集合のみで決まる）。
2. 空点の blocked 判定は (S, c) のみの関数。旧列のブロック状態は幅不変。
   よって S が幅 m0 で safe+maximal なら、max_x 右側で最初の非ブロックセル列
   R(S) まで全幅で safe+maximal、R(S) を超えると極大でない。
   行欠損 witness なら幅 m0..R(S) 全部の witness。

## 実装とバグの発見

- `append_criterion.py`（純 Python Fraction・blocking 直線は (c,s) 族・
  blocking 円は石三つ組族の完全列挙）。
- **初版バグ**: 円係数の連立一次方程式の右辺を −(f2−f1)/2 としていた。
  垂直二等分線の中点形式の /2 は中心 a=−D/2, b=−E/2 と打ち消し合うので、
  正しくは −(f2−f1)。初版は (6,4) m=46 witness の列 40 の到達を
  「(40,0) 非ブロック」と誤判定し、published 記録（m=46 PASS）と矛盾。
  verify_witness.py の blocked 論理とセル単位で突き合わせて
  円 (−75,−15,1400)〔石 (33,1),(31,3),(30,5)〕を見つけ、右辺を修正して一致。
  **独立実装同士の不一致検出が実効した実例**。

## 機械検証結果（published 3 witness と完全一致）

- (6,4) m=46 witness: R=46・停止 (46,0)。同一17石が幅 **40..46 の 7 幅**で witness。
- (4,4) m=32 witness: R=33・停止 (33,2) → m=33 off=0 延伸の根拠・m=34 はシフト必須の理由。
- (4,4) m=34 witness: R=34・停止 (34,2) → 前線 m=35 が真の前線である理由。
- 陰性対照 2 件（石移動 → unsafe / 非極大）正検出。2 回実行 byte-identical。

## (6,4) m=46 js+py 検証（保留項目の完遂）

- js: sat.js verifyConfig(6,46,4) ok・(6,45,4) 同一石 ok。
- py: verify_witness.py (6,46,4) ok:true・(6,45,4) ok:true。
- 陰性対照: 4 石行直線 → 両系統 unsafe-line 棄却。
- 記録: free-column-append-criterion-20261115/output/m46-js-py-verification-20261115.json
  および four-row-q4-q5-frontier-20261115/output/q4-w6-construct-m46/verify-js-py-20261115.json
  （新規ファイル・既存 records.jsonl は不変）。
- これで m=46 witness は 4 系統検証（純TS・js・py・criterion）。

## 各レーンへの指針

- witness を新規取得したら append_criterion.py を1回走らせるだけで
  無料延伸幅 R(S) がわかり、R(S)+1 が真の前線。
- 前線の INDET が続くとき、R(S) の停止セルは「次に必要な新配置の位置」の
  ヒントになる（例: (4,4) m=34 の停止 (34,2) は行 2 = 欠損行の右端）。

## 解釈境界

- R(S) を超える幅は不在主張ではない。11×11 空盤・二石 root・S2・
  class1/2/4 はいずれも UNKNOWN のまま。
