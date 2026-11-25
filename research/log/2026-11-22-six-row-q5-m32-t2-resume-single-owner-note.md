# 2026-11-22 six-row (6,5) 6x32 t2 remaining 23 bases — single-owner declaration note (resume)

- 日時: 2026-11-22T02:2xZ付近・宣言時HEAD `05785cdfa5…` (2026-11-22T01:55:30Z)
- オーナー: 高速レーン（本セッション・単一オーナー）。
- 前段: 同レーン 2026-11-22 01:02Z 宣言 `bc11e28b26`（6x31 band extension・K1216出版済）の
  resumeノートが指定する最優先課題。先行セッションで base-000 (c009@off3) の t2
  (rem3add2T targeted-complete) は完走済み・全0 witness（出版 `880e288663`）。

## 宣言スコープ（claim）

1. **6x32 t2 (rem3add2T targeted-complete) 残り23 base の掃引**: `config_w32_u3.json`
   の base index 1..23（c009@off4 → c009@off2/c009@off5 → c008/c011群 → c004/c006/c010群の順）。
   surgery_deep.js の 180s/呼び出し time-budget + 16-removal checkpoint resume で
   全baseの t2 クラスを done まで走らせる。
2. **witness が見つかった場合のみ**: 3系統独立検証（surgery_gen.js 整数正準曲線鍵・
   det_q_verify.py 行列式・append_criterion.py Fraction）+ tamper/陽性対照を添えて
   下界更新 **M_{6,5} ∈ [33, 658]** として出版する（下界のみの主張）。
3. **全baseが陰性の場合**: 6x32 UNDETERMINED 不変。t2 クラスの targeted-complete 陰性を
   base ごとに記録した上で、有界編集近傍（r0s..r4a1 完了済み + t2 targeted-complete）に
   6x32 witness が存在しないという限定命題を誠実に出版する（24 base のみを対象とする
   限定陰性・6x32 全配置の不在主張ではない）。

## 受入条件

- 全 base について `base-XXX.t2.cls.json` (done:true) を得るまで反復する。
  checkpoints (`base-XXX.t2.part.json`) は kit 退避で環境リセット耐性を保つ。
- 決定性: t2 完了 base のうち1つ以上で time-budget カット境界を跨ぐ再開 resume が
  動作したことを確認（part.json からの doneIdx 再開）。
- witness の場合は K1216 と同一の 3系統検証ゲートを全て PASS させてから出版。

## 非目標（着他レーンとの境界）

- **(6,6) m=26 probe**: 宣言済み `05785cdfa5` (01:55Z) の並走レーンが所有。非接触。
- **seven/eight-row families census+surgery**: 宣言済み `66e7033b6e` (01:51Z)。非接触。
- **(6,7) 6x22 rowfixed**: 宣言済み `24a98f89d3`。非接触。
- n11 系（sixth-cost・s4bd・thirdimpl）: 非接触。
- 標準 11x11 空盤・二石 root・S2・class 1/2/4: 本レーン非接触で UNKNOWN のまま。
- 6x33 (rem3add3 / unblocked≥4 対応) は本宣言スコープ外。

## 判定規約

- nodes/candidates/pairs 数を勝敗として読まない。
- t2 の陰性は「base の unblocked target セットが構成する rem3add2 クラスの
  targeted-complete 陰性」（surgery_deep.js docstring の枝刈り完全性）であり、
  編集距離3+追加2を超える witness や他 family 由来の構成は含まない。
