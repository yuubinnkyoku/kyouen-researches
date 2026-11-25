# y=10 two-token パラメトリック全称証明 — 正本検証器 part1 出版

- 日時: 2026-11-20 (UTC)
- 実験dir: `research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/`
- 位置づけ: K1141（cand10 fit, status: observed）昇格審査の正本検証器
  verify_y10_universal.py の part1。単一オーナー宣言は
  [y=10 skeleton single-owner note](2026-11-20-y10-two-token-skeleton-single-owner-note.md)
  が引き続き保持（宣言 2026-11-20T10:25:00Z）。
- 前段階: y=10 raw skeleton survey・K1141 cand10 fit（observed）・
  [machine preflight 出版](2026-11-20-y10-universal-machine-preflight.md)に続き、
  y=8/y=9 正本（K1135/K1138）と同一構造の機械を構成・全チェック実行した。

## 結果（full run: C1 C1b C2 C2b C3 C4 C4t C7 C8 C9 C11 C12 全指定）

- **overall PASS・照合点 6,265,496・全チェック不一致 0**
  （C4 confluence_bad 0 / identity_bad 0・マージ系 1,494,591 点・
  tail 系 274,835 点・それぞれ 0）。
- 生 census アンカー C11（z=0..79・x=10..70・R<=x+z+12・両 raw エンジン）
  902,800 点も含めて part1 の時点で全 PASS。実行時間 約70秒/run。
- **3回実行で audit.json byte-identical**
  （SHA-256 `eabe74004ac352bc02671f24738cd4026e6ea7899a3311dd694e304b84d1b79b`）。
  検証器（verify_y10_universal.py）SHA-256
  `9fbaa013f8440a294e8bd6e4559ef23970f50b827189300b6af5728bdc2709e2`。
- C4t tightness probe: **clip 21 で confluence 違反 4,736 件・初違反
  (z=60,x=84,R=84) → 必要 clip 半径 2y+2=22 が tight**。
  族式候補 2y+2 は y=5:12, y=6:14, y=7:16, y=8:18, y=9:20, y=10:22 の
  **6族連続 tight・5予想連続的中**（K1135 予想系列の更なる延長）。
- 型機械全走型 123,543（C4 ボックス内 121,461 型）・confluence 不一致 0。

## 出版物（本コミット）

- 実験dir: verify_y10_universal.py（841行・正本）・output/audit.json・
  output/published_run.txt（3回目実行の標準出力）・report.md
- report.md に記号・定理骨子（T/P 表要点）・選択肢分解・12チェック表・
  横断族観察・信頼境界・未解決を記載。
- **K item・README bullet は未更新**（part1 は実験成果・昇格は part2 で
  全12チェック機を構成してから）。

## 転写の正本確認

- cand10 表: K1141 出版 cand10.py（SHA-256 `7c08e065d127…`）から逐語
  （fit driver 除外・q_odd 二重定義は preflight C1c 308,484 点で意味同一担保）。
- engine＋single_token＋cand9: 出版 K1138 検証器
  verify_y9_universal.py（SHA-256 `299acb6a70b9…`）から逐語
  （fail-closed assert そのまま）。B 子に cand9 を使う初の族
  （x=10 合流子 (9,10)≡(10,9)）。
- C1/C1b が本機内の raw 両エンジンで再錨止め済み。

## 次工程（part2）

1. C1d: 出版固定z切片の y=10 特化アンカー（z=8/9/10 は y>=9 汎用候補の
   y=10 行、z=15/16/17 は K1065/K1077/K1087 の y>=6 一様分類の引数変換
   Y=20, S=x+10。過渡セルは y=10 では 2y+d>=20+d > 17 ですべて消滅。
   組み込み前に H の y=10 行を生エンジンで事前検証・低R縮約 R<=z+6
   〔z=15,16,17 で R<=21,22,23〕も照合）。
2. census_rows.py y=10 版（z=0..79・x=10..70・R<=x+z+12・行表・tail アサート）。
3. 全12チェック PASS・3回 byte-identical で K1141 observed→proved 昇格
   （K item 同番号更新・README bullet・CI audit step・本 log の続報）。

## 並走・競合の記録

- push 前に最新 main を再取得してから出版（n11 residual29・inversive K1058・
  AG(2,16) レーンと並走）。本 part1 出版時点で y=10 レーンへの他オーナーの
   着手は main 上に確認されていない。
