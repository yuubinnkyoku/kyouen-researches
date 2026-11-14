# 2026-11-14 高速レーン: SAフロンティア第2弾 — M_{6,5}≥28 と最前線5件の抵抗

- 開始時点で最新 main を確認（HEAD 53270e7d・並走は class2-lane cost-63b sweep と
  11050-circle w86〜91 予想で主題独立）。AGENTS.md・research/knowledge/README.md を再確認。
- K0811 のレジュームに従い SA 機を repo から再取得して verbatim で実行
 （2×8 q=4 制御で K0796 再発見を確認してから本番）。パラメータ多様化ドライバ
  `run2.js`（1ケースごと JSONL 追記・環境リセット耐性）で実行。
- **(6,5) m=26 を4.4秒で発見（23石・独立検証 PASS）→ M_{6,5} ≥ 27。**
- **(6,5) m=27 も47秒で発見（23石・独立検証 PASS）→ M_{6,5} ≥ 28。**
  23石 witness 連続帯は 6×22..6×27 の6盤に。
- (6,5) m=28 は6実行（計~5.5分）で抵抗・(6,6) m=21 は10実行・(5,6) m=19 は6実行・
  (6,8) m=16 は4実行・(5,7) m=20 は7実行でいずれも満容量維持（非発見の記録のみ）。
- 反映: 実験 `research/experiments/sa-frontier2-20261114/`（scripts/output/report）・
  K0811 更新（下界26→28・coverage・抵抗記録・artifact 追加）・
  mwq_stabilization.csv 6,5行更新・fixed-width README の bounds 行の整合更新・
  本 log。1コミット1ファイル・全読み戻し検証。
- 次の一手: (6,5) m=28 の SAT 長時間攻撃・(6,6) m=21 / (5,6) m=19 の長時間 SA・
  M_{6,7} 上界402の 2+2+1+1 型追加予算設計。
