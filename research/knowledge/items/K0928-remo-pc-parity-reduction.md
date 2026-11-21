---
id: K0928
title: 一様盤P(C)のpot定式化と偶奇ストレッチ・パリティ定理・U/V縮約定理（全称）
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0859
- type: related
  target: K0919
- type: related
  target: K0922
- type: related
  target: K0926
artifacts:
- path: research/experiments/remo-pc-twin-laws-20261117/report.md
  role: proof
  note: "補題P（pot定式化）・s+pot=C不変量・補題E/O・定理PAR（パリティ）・定理RED（U/V縮約）の全称証明レポート（K0859計数再帰・一様盤・零リセット）"
- path: research/experiments/remo-pc-twin-laws-20261117/verify_pc_twin_laws.py
  role: verifier
  note: "10チェック（PIN/REF/TWIN/STRE/STRO/RED/RECON/LAW等）の機械照合器（stdlibのみ・決定的）"
- path: research/experiments/remo-pc-twin-laws-20261117/output/pc_twin_laws_audit.json
  role: data
  note: "監査正本（全チェックOK・コールド実行間でbyte同一・sha256 6bc2ee08…）"
- path: research/experiments/remo-pc-twin-laws-20261117/data/pc_p8000.json
  role: data
  note: "P(C) C=1..8000 の完全センサス（sha256 58a414bc…）"
- path: research/experiments/remo-pc-twin-laws-20261117/data/pc_uv8000.json
  role: data
  note: "U(m)/V(m) m=1..8000 の完全センサス（sha256 8a3b318b…）"
- path: research/experiments/remo-pc-twin-laws-20261117/pc_fast.js
  role: solver
  note: "閉形式フェーズによる直接評価エンジン（2実装交差の一方）"
- path: research/experiments/remo-pc-twin-laws-20261117/pc_reduced.js
  role: solver
  note: "縮約ゲーム上の独立実装エンジン（別データ構造による交差の他方）"
date: 2026-11-17
tags: [remo, uniform-board, counting-recursion, survivor, parity, reduction, universal-proof]
---

## 主張（すべて全称、Cは人数）

対象は K0859 の計数再帰（非一様盤とは無関係の一様設定）。
P(C) は K0926 で確立した r 非依存性（E6U）により意味が確定する生存位置。

### 補題P（pot定式化）

各フェーズ開始時の配分石数は「直前の敗者の保持石数」に等しい。
したがって s + pot = C は全フェーズを通って不変で、
P(C) は初期盤 G(C)（C人それぞれ石1・pot 0・pointer 0）の生存者に等しい。

### 補題E（偶数Cの第1ストレッチ）

C = 2m+2 >= 4 のとき、最初の m+2 フェーズはちょうど
P_0, P_2, ..., P_{2m}, P_1 をこの順に除去する（保持石数は 1, 1, ..., 1, 2）。
残るのは P_3, P_5, ..., P_{2m+1} の m 人（各2石・pot 2・pointer P_3）。

### 補題O（奇数C版）

C = 2m+1 >= 3 のとき、最初の m+1 フェーズは偶数番地の全員
P_0, P_2, ..., P_{2m} をこの順に除去する（各1石）。
残るのは P_1, P_3, ..., P_{2m-1} の m 人（各2石・pot 1・pointer P_1）。

### 定理PAR（パリティ定理）

C >= 2 に対し P(C) は常に奇数。

### 定理RED（U/V縮約定理）

U(m) := m人・各2石・pot 2・pointer 0 の一様ゲームの生存位置（0-based）、
V(m) := 同・pot 1 の生存位置、と定めると

- P(2m+2) = 3 + 2*U(m)  （m >= 1）
- P(2m+1) = 1 + 2*V(m)  （m >= 1）

### 系（法則の半分）

偶数 C >= 4 では P(C) >= 3 なので P(C) = 1 は起きない。
奇数 C >= 3 では P(C) <= C-2 なので P(C) = C-1 は起きない。
したがって LAW1（P(C)=1 の特徴付け）は V側の予想と、
LAW2（P(C)=C-1 の特徴付け）は U側の予想と同値になる。

## 証明

すべて初等的な帰納法による。詳細は report.md（実験ディレクトリ内）の
証明セクションに記述した。要点のみ:

- 補題P: 配分石数の定義と s+pot=C の保存から帰納。
- 補題E/O: 偶数番地が1石で除去され pointer が +2 ずつ進むこと、
  pot が偶数 C では 2・奇数 C では 1 に落ち着くことを帰納で追跡。
- 定理PAR: 偶数 C では定理REDの 3+2U、奇数 C では 1+2V の形から従う。
- 定理RED: 補題E/O の残った盤を U/V ゲームに読み替え、
  位置の対応（P_{2i+3} -> i）で生存位置を比較。
- 系: PAR の形から直ちに従う。

検証スクリプト verify_pc_twin_laws.py が独立実装（python）で
縮約を再構成し、m <= 150 で U/V の直接計算と一致することを確認した。
さらに縮約 engine（pc_reduced.js）が全 C <= 8000 の P 表を
直接 engine（pc_fast.js）と完全に再構成（違反0、RECONチェック）。

## 範囲と限界

- 本 item は全称定理のみを主張する。LAW1/LAW2 の予想部分は K0929 に分離した。
- 非一様盤には一切言及しない。
