# s_12/s_13 witness-hunt layer-3 近傍完全走査（（R,A）編集層の全列挙）— 単一オーナー宣言

- **宣言時刻**: 2026-11-21T19:59Z（Vibe 高速レーン instance）
- **宣言時 HEAD**: `29f3f65412cd423bfeb2e8e093ab5d1663706b37`
- **owner**: この宣言を出した instance。失効時は最新 main の IN FLIGHT 確認の上、他レーンが takeover 可。

## 対象・目的

s12/s13 constructive upper bounds lane（宣言 `593a567a`・K1205/K1206・commit 列 `7ad490bc`..`1d119b79`）が
自レーンのレジューム (a) として残した「3-swap 近傍の完全走査」を、この instance が単独で実行する。
K1206 が確定済みの編集層（witness の remove-1 / remove-2 / remove-2/add-1、wall の remove-1 / remove-2 /
remove-2/add-1、wall・plateau の 2-out/2-in 413,100 / 699,600 検査）の次層として、以下の
**（R,A）編集近傍の完全列挙**を行う。全ての基底は既刊の固定状態（出版座標をそのまま使用）:

- **Bases (n=12, 12×12)**: K0320-n12 witness（11石・`witnesses.mjs` pin）・W_c（K1206・11石）・
  wall 状態（K0320-n12 witness − [5,11] の10石・`probe2_wall_n12.json` pin・score 4）
- **Bases (n=13, 13×13)**: K0320-n13 witness（12石）・plateau 状態（同 witness − [7,12] の11石・
  `probe2_pl_n13.json` pin・score 6）

走査する（R,A）編集集合（A は可能な限り基底状態の空点から選ぶ。R は stone の部分集合・A は
W∖R の外の点の部分集合・重複構成は正準鍵で dedupe）:

- **n12 witnesses (11石, 目標 |S|≤10)**: (3,1) k=9・(3,2) k=10・(4,2) k=9・(4,3) k=10
- **n12 wall (10石, 目標 |S|≤10)**: (3,1) k=8・(3,2) k=9・(3,3) k=10・(4,2) k=8・(4,3) k=9
- **n13 witness (12石, 目標 |S|≤11)**: (3,1) k=10・(3,2) k=10・(4,2) k=10・(4,3) k=11
- **n13 plateau (11石, 目標 |S|≤11)**: (3,1) k=9・(3,2) k=9・(3,3) k=11・(4,3) k=10

優先順位: P1 = n12 witness(3,2) と wall(3,2)（witness 最近傍）→ P2 = wall(3,3)（K1206 が掲げた
主力ジョブ）→ P3 = n13 witness(3,2) と plateau(3,3) → P4 = (4,2)/(4,3) 層と残余の軽量層。
実行時間が尽きた場合、到達済み層までを誠実に出版し、未到達層は次回に回す。

## 主張の形式（受入条件）

- 正が得られた場合: **≥3 の独立整数系**（走査 engine〔safe-int64 increment〕＋
  `verify_witness.py`〔Fraction・4x4 行列式・quartet catalog 非依存〕＋`verify_witness.mjs`
  〔BigInt・別経路〕）で safe+maximal 全 PASS し、`classify.mjs`/`check_congruent.mjs` で既知
  witness（K0320-n12/W_c/K0320-n13）との格子合同判定を行った上で、石数が既刊上界より小さければ
  新規 K item として s_12 ≤ 10（またはそれ以下）/ s_13 ≤ 11 を主張する。
- 陰性の場合: 「列挙した機械検証サブセット内に witness なし」を主張するのみで、大域的な不在は
  主張しない。走査体積（R 総数×A 列挙数・branch 計数）を記録する。
- 枝刈りは**証明済みの排除**のみ（e ∈ U の被覆可能性の 4 分類に基づく DPLL 風分岐。
  分逸脱で棄却した A は全数列挙対照（unpruned brute-force を代表 R 数個で実行して hit 集合の
  一致を確認）で検証する）。
- quartet catalog は `census.mjs`（D_n/C_n/F_n アンカー組み込み検証つき・n=12: F=158,426・
  n=13: F=252,362 を再現）とし、wall/plateau の score（4/6）の再生を較正とする。
- K1206 の既存陰性（wall r2a0/r2a1・2-out/2-in、witness r1a0/r2a0/r2a1）を本 engine で再現
  （0 witness・bestScore 一致）してから本番層に入る。
- 有限実験を全称として主張しない。nodes 数・検査数は勝敗ではない。

## 非目標（衝突回避）

- s_11 決着レーン（`a45a626d`・SAT/CNF/kissat・11×11）— 非接触。
- K1206 の既掃引層の再実行そのものを成果としない（較正としてのみ）。
- n≥14 上界・host 移植・下界・UNSAT・SAT 符号化 — 非接触。
- 固定幅 M_{w,q} band・n11 S5/fold/receipt 系 — 非接触。
- knowledge corpus 修復・既存 K item の上書き変更 — 非接触（K1206/K1205 は追記参照のみ）。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。
- s_12/s_13 の値そのものの決着（下界・不存在証明）は本レーンの成果に含まない。

## collision protocol

- push 直前に毎回最新 main を再取得する。
- s_n 系への IN FLIGHT 宣言・結果 push を検出した場合、対象を外すか convergence を優先する。
- 失敗時は無理に進めず状況を簡潔に記録して次回実行に回す。

## 進行の公表

- 実験は新規 dir `research/experiments/s1213-layer3-neighborhood-scans-20261121/` に置く。
- 既存実験 dir・既存 records への追記はしない。pinned な出版物は 1 byte 変更しない。
