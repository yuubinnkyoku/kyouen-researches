# 2026-11-27 (6,6) 6x26 class {1} krow/minpos decomposition: 単一オーナー宣言 (高速レーン)

- 宣言時 HEAD: `05b3aa52` (2026-11-27T14:52:05Z)。着手前に最新 main を再取得済み。
- 前線の位置づけ: **M_{6,6} ∈ [26, 495]**、前線 6x26 (K1217 witness 帯 m=5..25・
  6x26 は未解決)。kit `six-row-q6-m26-class-split-20261127` (commit `c4d2e9dbb0`)
  は class {2} krow=2:4 minpos 10..13 を 272s cap で 4 INDET (honest negative) で
  完了し、そのレジュームが「class {1} krow 分割・残クラス未走」を登録済み。
  並走の minpos-REST lane (宣言 `e61acf82`・class {2} P∈{0..9,14..22}) および
  6x23 q7 系2 lane (`f43cd66b`/`a8075223`)・4行 m24 lane (`855f52d8`)・REMO cap16
  (`7a100862`)・kit20 strip lane とは不交差。
- 本宣言: **6x26 q=6 class {1} (欠損行 = 行1のみ) を krow=1:4 (行1ちょうど4石)
  で固定し、minpos (行1の最左石位置) を P=0..11 で完全に分割掃引する**
  (sound H-split: min(x1, 25−x_4)≤11 ゆえ P=0..11 で全列挙・m26 kit と同一規約)。
  H鏡映で class {1}≡class {4}。
- 器材: `sat3.js`/`sat2.js`/`sat.js` は m26 class-split kit 出版 byte
  (sha256 `e04581eb…`/`14ceb854…`/`fcc0cfd8…`)・kissat 4.0.4 公式 linux-amd64
  (sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`)。
  CNF は再生成 (size policy・非出版)。生ログ・records.jsonl・meta を出版。
- 較正 (事前登録): 陽性対照 6x25 q=6 class {2} krow=2:4 minpos=11 は出版値
  **SAT 3,574,244 conflicts の bit-exact 再生**を合格条件とする (m26 kit
  `output/r6x25q6_c2k4p11.txt`)。較正は宣言後に実行・記録する。
- 受入条件: (1) 陽性対照 bit-exact 再生。(2) 全12 probe は各 272s cap・
  kissat 1走ずつ (環境 reset 回避)。(3) SAT の場合は witness 復号 +
  `verifyConfig` (sat.js) と fresh Fraction 検証器 `verify_frac.py` (sha256
  `837fe24b…`) の二系統 PASS + 負制御 (1石除去で非極大・1石追加で拒否) +
  cold pair 再現。(4) INDET は honest negative (不在主張でない)。
- 判定: **SAT なら M_{6,6} ∈ [27, 495] に前線更新**・witness を出版。
  全 INDET なら M_{6,6} ∈ [26, 495] 不変・前線 6x26 のまま。
- Not claimed: 個別 INDET は不在主張でない。class {0}/{5}・multi-class・
  6x27 は本宣言の対象外。(6,q≠6)・w 行族・Grundy・11×11 は一切不消費
  (全時点 UNKNOWN)。verdict 不消費・conflicts は bookkeeping。
