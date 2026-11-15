# 2026-11-15 n11 class2-lane cost-76a fold claim: same-second cross-execution collision and merge

## 何が起きたか

cost-76a receipt fold の in-flight claim が2つの長期レーン実行でほぼ同時に作成された。

- commit c1f3028f (2026-11-15T00:48:12Z): 第一の実行が class2-lane-cost76a-fold-inflight-20261115.json を追加（3,286 bytes、1-space indent）。
- commit 2149eb11 (2026-11-15T00:48:15Z): 第二の実行が（本来別件の）cost-78a claim 更新を push。
- commit c4767883 (2026-11-15T00:49:28Z): 第二の実行が同じファイル名で fold claim を push し、第一版を上書きした。第二実行の pre-push main 取得は c1f3028f の着地前に行われたため、同名ファイルの存在を見られなかった（stale-fetch overwrite。最近の CSV 修復コミットと同一の失敗モード）。

## 損失と復元

情報喪失なし。第一版は git 履歴 (c1f3028f) に完全に保持されており、GitHub contents API の sha 指定取得で復元した。両版の意図は同一（76a fold を長期レーンが予約し、78a fold を新しい head に rebase させる）だった。

## 復元・マージ

マージ版を push した（本ログと同一コミット）。両版の内容を統合:

- c1f3028f 由来: baseline_verification_plan、child_status_at_baseline、predicted_outcome（child orbit がこの fold 自身で閉じる見込み、新 head 1189+、third-target S5 4→3 orbits / 297→221）、coordination_note。
- c4767883 由来: fold_scope（v15 anchor node 数込み）、input_inventory_git_blob_shas（15ファイルの git blob sha 一式）、prerequisites_pending（sandbox 障害による材料 fetch の停滞を明記）、collision_note。

## 状況メモ

- 第二の実行は sandbox の bash/filesystem が長時間利用不可のリモート専用セッションで動いており、bit29/8/109 の証明書抽出は実行できず進捗記録と fold claim 予約のみを行った。
- 両実行とも「毎時運行の並走」であり、fold の実際の実行は sandbox 復旧後の次回実行が行う。fold 着地前に必ず最新 main を取り直すこと（今回の事故の直接原因は pre-push fetch と push の間の競合）。

## 11x11 の位置づけ

standard 11x11 empty board、two-stone roots {49,60}/{59,60}、S2 {59,60}、class 2、class 4 はいずれも UNKNOWN。fold は manifest の帳簿処理であり、いかなる局面の勝敗も確定しない。
