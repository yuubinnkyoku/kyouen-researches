# 緊急監査：K0420 WIN側極性誤りの訂正（2026-10-12）

分離worktree `D:\wk-krr` で作業。監査前のWIN側パイロット探索は開始していない。

## 誤りの内容

旧 `win_side.py` / `win_witness_masks.py` は「S5 LOSS子を持つS4＝先手WIN（free）」「全子WIN＝dead」と判定していた。K0371（S4=OR層、元先手固定）では逆で、正しくは「WIN子あり＝free」「全子LOSSまたは子なし＝dead」「それ以外＝open」である。既存 `analyze_central_reply_frontier.py:s4_status`（WIN_CACHE / LOSS_CACHE / LOSS_TERMINAL / UNKNOWN）と照合して監査指摘を確認した。

## 修正

- 共有モジュール `scripts/s4_win_polarity.py` を単一真実源として新設し、`classify_s4`・`verdict_of`・定数を集約した。
- `win_side.py` は共有分類を使用し、未知S5のindex採番はopen S4のみに限定した。出力schemaをv2に上げ、polarity文・graph/cache/モジュールのSHA-256・S4種別内訳を記録した。応手単位の進捗logを追加した。
- `win_witness_masks.py` は被覆検証器に作り替え、幾何再計算で「dead混入なし・open全被覆・証人の正準/未cache・総数一致」を検査し、失敗時はexit 1にした。旧方式の件数突合（tie-break雑音あり）は廃止した。
- 回帰 `scripts/test_s4_win_polarity.py` 5件が通過：K0414 S4 `(1297036692683752448,0)` の106子全LOSS→dead、cache WIN子持ちS4→free、UNKNOWN境界→open、空子集合→dead（終局）、frontier `s4_status` との500件一致。

## 再計算結果（初手49、約45分＋検証約1分）

65/65閉鎖可能、無料0、証人要65、AND幅7,519、証人1,945（検証通過）、到達S4中free 98・dead 3・open 133,823、viable thirdは応手ごと109〜119。LOSS共同要求集合との重なり29件は逆極性で奪い合う衝突点（旧「両用16件」は誤り）。中央宇宙内の証人は120件。

## K0418/K0419の非依存確認

両項目のartifact・本文をgrepし、WIN側脚本・出力への参照がないことを確認した。K0418の双対は `s4_cost` 集合の濃度のみを使い、K0419のUBはLOSS側分類（全子LOSS、K0371通り）のみを使うため、極性誤りの影響を受けない。両項目は無改変とする。

## 履歴化

旧出力3件（win-side-analysis.json、win-witness-masks.json、pilot-candidates.json）は `output/superseded-polarity-bug-20261012/` に `git mv` で移動し、対応READMEを添えた。`pilot-candidates.json` のlegal分布・最安10件は極性不変で有効だったが、`dual_use` の意味が変わるため新ファイルを再生成した。K0420は同一番号で正本更新し、旧結果の誤り依存を本文に記録した（改名なし）。

## 引き継ぎ

- WIN側パイロットは訂正後の証人（衝突29件優先＋最安10件）を対象にすること。旧証人マスクでの探索開始は禁止のまま継続する。
- 上下差・非中央拡大・他初手WIN側・閉包実測の未実施分は親READMEの限界に残る。
