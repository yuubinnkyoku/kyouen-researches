# y=10 two-token 汎用証明機械 — 予備検査（machine pre-flight・出版）

**日時**: 2026-11-20 (UTC)
**対象**: H(R; (x,10); z), z>=0, x>=10, R>=0（vertical-fiber 2トークン y=10 族）
**位置づけ**: K1141（cand10 有限 fitting, status: observed）の第2段階。
正本 verify_y10_universal.py（12チェック・3回 byte-identical・observed→proved 昇格・CI step）の
**前段階の機械的予備検査**。実験dir `research/experiments/vertical-fiber-two-token-y10-universal-machine-preflight-20261120/`
に自足型スクリプト・出力・report を出版した（y=9 の JS pre-flight が log のみだったのに対し、
今回は Python 実行環境が使えたため再現可能な成果物そのものを出版）。
単一オーナー宣言は y=10 skeleton single-owner note が継続保持。

## 結果（全 bad 0・4回実行 byte-identical・約1.6秒/回・Python 3.12）

| check | 概要 | points | bad |
|--|--|--|--|
| C2a | 恒等式グリッド cand10==mex(opts)（B子=cand9・x=10合流子）z=0..40, x=10..56, R<=x+z+36 | 171,503 | 0 |
| C2b | 深z窓 z∈{60..400}, x=10..80, R∈[x+z+1,x+z+40] | 22,720 | 0 |
| C2c | 深x窓 x∈{70..400}, z=0..40, R∈[x+z+1,x+z+40] | 9,840 | 0 |
| C2d | x=10 エッジ z=0..60, R∈[x+z+1,x+z+70] | 4,270 | 0 |
| C3 | 選択肢分解 raw アンカー（閉形式子供集合==raw 子供集合） | 5,070 | 0 |
| C1b | (9,10)=(10,9)=canonical==cand9(z,10,R) z=0..30 R<=55 | 1,705 | 0 |
| C1c | cand9 fit版転写==K1138検証器版転写（T/P 表意味同一性・文本差2箇所は吸収） | 308,484 | 0 |
| merge 系 | x<=z-11 ⇒ single_token_val(x+10,R) | 41,300 | 0 |
| tail 系 | R>=x+z+11 ⇒ (x+10)%2 | 78,182 | 0 |

T/P 重複 0・sentinel (-99) 出現 0・`overall: PASS`。

## 副産物

K1138 の2つの出版本文（fit dir `cand9.py`〔SHA `6c3e9242…`〕と出版検証器内 cand9 表
〔SHA `299acb6a…`〕）には奇z d=-7 行・d=-5 行の P 接頭（b5/b4・b6/b5）と sentinel
（-99/fail-closed assert）の文本差があるが、C1c が 308,484 点で意味同一（吸収差）を機械確認。
以後の y=10 正本での cand9 転写（検証器テキストから採る規約）と fit 版で差がないことの前担保。

## 正本転写の確認（本 log の執筆時点）

- cand10 表: K1141 出版 `cand10.py`（SHA-256 `7c08e065d1278e9e…`）から逐語抽出・取得 SHA 照合済み
- cand9 表・raw 両エンジン: 上記2 出版から逐語抽出・取得 SHA 照合済み
- 詳細は `research/experiments/vertical-fiber-two-token-y10-universal-machine-preflight-20261120/report.md`

## 次の工程（正本出版・未実施・単一オーナー宣言の対象）

1. `verify_y10_universal.py` を y=8/y=9 正本と同一構造で構築
   （C1..C12。C1d は出版 z=8/9/10/15/16/17 切片の y=10 特化を再転写。
   C4 型機械 clip 窓 ±22/番兵 ±23〔族式候補 2y+2 の 6 族連続 tight 判定〕）。
   3回実行 byte-identical。
2. census_rows.py（y=10 版, z=0..79, x=10..70, R<=x+z+12, 両エンジン）を作成し実行。
3. 全 PASS なら K1141 を observed→proved に昇格・出版・CI audit step 追加。
   README・K1141 item・本系列 log 更新。
4. push 前の最新 main 再取得・競合確認の方針は不変（並走: n11 residual29 / inversive K1058 / AG(2,16)）。
