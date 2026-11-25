# 7行 q=4 witness band 60plus レーン: 実行成果（2026-11-21 高速レーン）

- 宣言: `research/log/2026-11-21-seven-row-q4-band-m60-single-owner.md`（11:35Z・宣言時 HEAD `e0d072fb`）。
- 成果物: `research/experiments/seven-row-q4-witness-band-60plus-20261121/`。
- publish:
  - part1 `5d22f006`: scripts（enum_two.js・verify_witnesses.py）+ 較正 + 幅60 witness 4件 + 2系統検証（fetch-back md5 照合 MATCH）。
  - part2 `b0a663a6`: 幅61..67 チェーン成果（frontier/stats/witness 各幅）+ チェーン代表検証 7件（fetch-back 抽査 MATCH）。
  - part3 `ce026735`: 第三系 verify_third.py + third_verify.json + README 追記 + K0827 反映 + knowledge README 反映 + 本ログ。
  - repair `8afa77d5`: part3 の切り詰めを正本へ復元。
  - part4 `a2acdd6a`: 幅68 witness（下界69）。
  - part5 scripts `e91f6f74`: 幅69掃引scripts fresh+holes（データは環境復旧後に）。

## 結果（下界更新）

1. **7×60 witness 4件を発見**（w60_a..d）: A57（7×57 witness・2026-11-15 two-swap レーンの
   既発見だが 7×60 近傍は未調査だった seed）の fresh 2-for-2 近傍完全列挙で
   95,722 safe 候補のうち 4件が安全かつ行欠損極大。
2. **チェーンで幅61..67 の全幅に witness**（2-for-2 fresh・frontier cap 10・max-x 貪欲）:
   新規 61:49 / 62:29 / 63:72 / 64:18 / 65:41 / 66:38 / 67:2 件。
3. **M_{7,4} ∈ [68, 1929]**（従来 [60, 1929]）。上界は K0068 の 1929 が不変。
4. 幅68 は最終 frontier 2件の近傍で 0件（局所負記録のみ・不在主張なし）。

## 検証

- 列挙器 `enum_two.js`: pinned `audit_two_swap.cpp` 出版計数に完全一致較正
  （base53@57 1,436,643/60,921/2 + witness 2件の石配置一致、base53@60 1,599,648/83,225/0、
  foundB@60 1,599,648/110,748/0）。
- witness 13件（アンカー A57/B59・幅60 4件・幅61..67 代表 7件）:
  (b) 正規化整数直線/円方程式 Python 検証器 PASS、(c) 第三系（素朴 4×4 行列式総当たり）PASS。
  浮動小数点不使用。3系統一致。

## 環境メモ（次回実行用）

- 今回の実行は途中 2 回、bash 300s 超過で実行環境リセットにより作業ファイルを喪失し、
  そのたびに seed pool・スクリプトを再構成した（列挙器は較正で計数再現を確認）。
  **中間成果は小刻みに main へ publish して永続化する運用が有効**（part1..part3 方式）。
- チェーンの endpoint（幅68）は frontier cap 10 の貪欲に依存。cap・選別基準を
  変えれば 68+ 到達の可能性が残る（幅68 witness 探索が次の実行可能課題）。
- 実行時間の目安: 1近傍列挙につき 2〜4 秒（幅60前後）、1幅あたり cap 10 で 10〜36 秒。
- 2026-11-21 第二バッチの後半で bash・file_system の実行環境が一時ダウンした
  （GitHub コネクタは稼働）。大ファイルのローカル成果は次回実行時に再取得・再構成が必要。

## 事故と修復（part3 publish の切り詰め）

- part3 commit `ce026735` で K0827 と knowledge README が約64KBで切り詰められた状態で
  push されていた（K0827 63,951B・本来 70,010B。README 63,749B・本来 741,264B。
  ともに正本のバイトプレフィックスであることを SHA 指定 raw fetch と md5 で確認）。
  原因は publish 前のファイル読み込みが単発 read（~64KB cap）で was_truncated を
  確認していなかったこと。push 直後の raw main 指定 fetch は CDN キャッシュの
  旧 blob を返しており、断面が検査で見えなかった。
- 修復（commit `8afa77d5`）: 分割読み込み（returned_bytes 合計と file_size_bytes の照合で
  70,010B・741,264B を完全復元）で再構成した正本を push し、commit SHA 指定 raw fetch の md5 が
  local と一致することで完了を確認。
- 教訓: 大ファイルの publish は分割読み込み + byte 数照合が必須。push 後の検査は
  `main` 指定 raw でなく commit SHA 指定 raw で行う（CDN 遅延を回避）。
- part4 push の際、作業側で手違いにより本事故セクションが一度欠落した（part4節の
  修復記録行のみが残っていた）。本 commit で復元した。

## part4（幅68 witness — 第二バッチ・下界69）

- 幅68 witness 探索: 既知全199基底（anchor群+幅61..67全チェーンwitness・重複除去）の
  幅68 fresh 2-for-2 掃引で、3つの幅65基底近傍から同一の一意な幅68 safe row-deficient
  maximum（20石 rows [3,3,3,3,3,3,2]・maxX=57）を発見。2系統検証 PASS
  （正規化整数直線・円 + 素朴4×4行列式）。被覆は幅68でちょうど尽きる（(68,6)未遮断）。
- **M_{7,4} ∈ [69, 1929]・witness帯 m=4..68・前線 7×69**。幅69は幅68 witness の
  fresh 近傍で0件（局所負記録のみ）。

## part5（幅69 fresh+holes 全200基底掃引 — 完全局所負記録・データpublishは環境復旧後）

- 幅69をpart4と同一の全基底掃引で評価: 基底は199基底+幅68 witness の200基底。
  fresh 2-for-2 全掃引: 428,241,000候補・43,208,643 safe・**行欠損極大 0件**。
  holes 2-for-2 全掃引: 437,885,400候補・45,578,855 safe・**0件**。
  いずれも既知基底の（≤2除去,≤2追加）近傍に限る完全列挙による局所負記録であり、
  幅69全体の不在主張ではない（3編集surgery・他の移動型・未発見配置は残る）。
- **M_{7,4} ∈ [69, 1929] 不変・前線 7×69**。
- 環境ダウン時の扱い: sweep69.js・sweep69h.js は正確に再構成して publish 済み（`e91f6f74`）。
  未 publish: output/w69/results.jsonl・results_holes.jsonl・output/w69/bases.json
  （= output/w68/bases.json（part4でpublish済み）+ 幅68 witness）・実験README追記・K0827追記。
  列挙は決定的なので再実行で計数・候補数は完全に再現する（results.jsonl の ms
  フィールドのみ wall-clock 依存で変わる）。次回実行時の宿題: 環境復旧後に上記データを
  再生成・push して実験 README・K0827 に w69 両モード負記録を反映する。
