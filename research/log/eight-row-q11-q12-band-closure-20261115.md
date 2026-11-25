# 8行帯 q11/q12 閉包 — 作業記録 2026-11-15

高速レーン(共円・固定幅)の1セッション記録。

## 経緯・判断

- 対象は (8,11)（M ∈ [16,908]・SA witness 11..15・非発見帯 16..26）と (8,12)
  （M ∈ [15,883]・SA witness 12..14・15,16 非発見）。
- 8×m の全census（sat2 全三つ組）は生成コストが高く887幅の掃引に不向き。
  ≥11点円が F1 のみ（strip classification Theorem A・系4・m≤984）を健全性の核に据え、
  「8行 + m−7 個の12点 F1 円のみ」の族census生成器 genfam12.js を開発。
  CNF byte-identity 較正 21/21（sat2.js と 8×11..16・genfast.js と 8×17/20/26/40/60）で
  先行2生成器との同一インスタンス性を保証。
- sweep.sh に set -e を入れると kissat の SAT=10/UNSAT=20 終了コードで即死する
  （m=21 の記録を2回失った）。v2 は1幅ごとに tee -a で即時追記し resume-safe。

## 得られたもの

- **(8,11) 完全決着: M_{8,11} = 21 EXACT（w=8 初・w≥6 で3例目）**。witness 8×15..20 を
  kissat def-mode SAT で発見（79石単一欠損・SA 非発見帯 16..26 を突破・全witness 2系統検証 PASS）、
  witness-free 21..907 全887幅 UNSAT（conflicts 最大 1,379,955@21 から漸減・proc ≤41s・INDET 0）、
  m≥908 は K0318 U=908 で排除。
- (8,12): witness 8×15..16 を kissat で発見（87石・2系統検証）、witness-free 17..230 の
  214幅 UNSAT。M ∈ {17} ∪ [231,883]。
- 決定性: m=21 (1,379,955)・m=26 (162,762) の conflicts が完全リセット・再構築越しに bit-exact。
- CSV (8,11) 行を exact-threshold proved に、(8,12) 行を更新、K0843 新設、
  fwreadme の exact-threshold を11件化。

## 失敗・未達

- q12 掃引 231..882 未完（bash/VibeFS 障害で中断）。次回: sweep.sh 12 231..882 を
  バッチ実行 → 全完了で M_{8,12}=17 exact を確定し CSV・K・claim を更新。
- ローカル成果物の未格納: scripts 4本・records/sweep-q12.jsonl（17..230 分）・summary-q11.json・
  witness 8x15/16q11・SAT 生ログ 8本（q11 m15..20・q12 m15..16）。artifacts マウント
  （リセット耐性）に保存済み、file_system 回復後に push。
- UNSAT 生ログの batch tar は binary のため push 経路なし。conflicts・CNF md5 を records で担保。
- 運用事故（本セッション）: push リトライ版スクリプトで README・log・K項目の本文が
  プレースホルダーのまま commit された（57152a8f・3b189f6c）。同一セッション内で
  実内容を再 push して修復した。教訓: 長文の本文は変数に組んだら必ず文字数を
  assert してから push すること。

## 引き継ぎ

- 掃引の再開: artifacts マウントの scripts/sweep.sh を使い 1バッチ30..100幅・280s bash 制限内で
  （q12 は1幅あたり m≈200 で 0.2..1s・軽い）。
- 並走レーン（five-row-q7・anchored-window 等）が活発。push 前の最新 main 再取得と
  行プレフィクス一致確認は必須（今回は (8,11)/(8,12) CSV 行・確定値件数行をアサートで検証）。
  今回 five-row-q7 レーンが K0842 を使用したため本レーンの K 番号は K0843 とした。
