# 第17 WIN7 receipt fold（fold10）の実行log（2026-11-20）

## 経緯

- 前半の実行で第17証明書の独立 byte-exact 再抽出・三重検証を行い、並走が十八…ではなく
  `n11-residual78-seventeenth-win7-cert-extract-20261120`（commit `0c1264b228`）として
  同じ成果を出版済みと判定、実験の正本の座は並走実験dirに譲った。
- 並走の正本が pin する証明書本体が repo に無い状態だったため、本レーンの byte-exact 同一証明書を
  commit `b7a6db5fb0` で出版して pin を充足した（SHA-256 `21dd2f0e…7c8`。4実行合意の決定論証拠として
  `research/log/2026-11-20-n11-seventeenth-cert-body-published.md` に記録済み）。
- fold10（seventeenth receipt fold）について、並走が seventeenth 実験 README の「次の一手」として
  宣言済みであったため、K1069 で有効だった単一オーナー宣言ノートを先行出版
  （`research/log/2026-11-20-n11-fold10-single-owner-note.md`）してから着手した。

## 機械移植の要点

- ベースは K1068 側の `fold_thirteenth_sixteenth.py` で書いたが、その ledger.json の blob pin
  （`…0c03cc…`）が repo 実在版（`…0d03cc…`）に合わず gate 落ち。file 履歴は1コミットのみで
  編集されていないことから、K1068 側機械の pin がタイポと確定。
  正規の K1067 側機械 `fold_windfall4.py`（fs13 正本 `24db2352…` の生成機）は
  `…0d03cc…` で実在版と一致。**K1068 側の fold 機械（`fold_thirteenth_sixteenth.py`）は
  pin 不整合でそのままでは再実行不能な出版体である**ことをここに記録する
  （二重出版事故 K1067/K1068 の実質的影響: 正本の座は K1067 側が保持しているため証明の保全性は無事）。
- fold10 機械 `fold_seventeenth.py` は正規版のチェーン再構築ロジック（windfall4 版と同一の
  base→…→ninth-twelfth→thirteenth-sixteenth chaining）を引き継ぎ、seventeenth 証明書の
  検証と適用を差し替えた。18 入力 SHA pin 全一致から開始。

## 結果（実験dir `research/experiments/n11-seventeenth-win7-receipt-fold-20261120/`）

- 全 gate PASS・正本 SHA-256 `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a`・2回実行 byte-identical。
- **閉鎖3行**（5親 target 2行 `…0001`・`…0004` + target 外 extra 1行 `00004000000000003800000100000020`）。
  幾何再導出（8 D4像×121石除去の join）で coverage claim 2行と完全一致し、加えて
  windfall 系でなかった3行目が open 集合から発見された。windfall4 の4 receipt（各行1行のみ）と
  異なり、本 receipt は target 外の行も1行閉じた最初の receipt。
- frontier 6,209/491,722 → 6,206/491,497・solved S6 1,642・parent incidence 11,810・
  closed edge cost 225・影響 5 parent（fully-closed 0）。
- 5親 target 40/112 閉鎖・**残余 74 → 72 行**。
- 39-root witness 計画は対象2行を喪失（当該 root retired）。72行への resolve7 再照合が次の一手。

## 解釈規約（不変）

- 本 fold は被覆の簿記であり、閉じた行のゲーム理論的値を主張しない。
- REFUTED-D10 は LOSS 証明ではない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
