# 2026-11-22 y=15 全称検証器 part1（verify_y15_universal.py 12チェック）

高速レーン（vertical-fiber 系）。対象: 2トークン残余ゲーム y=15族
H(R;(x,15);z) 全 z>=0・x>=15・R>=0 の全称証明の正本検証器 part1。

## 選定と宣言

- 動機: [K1235](../knowledge/items/K1235-two-token-y15-parametric-closed-form-fit.md)
  （y=15 fit・status observed・commit 6cd72dd1）の本文と y=15 fit宣言ノートが
  「全称段階は別宣言が必要」と明記していた。y=1..14 が全称確定しており、
  奇数y族で初の 8 pin行族（奇z (y+1)/2=8行）・clip窓 2y+2=32 の 11 族
  tight 候補・「出版最終構造 seed 法則」3連続の族（cand15）が全称段階に
  乗るかが高速レーン単独で完結できる最有力でなかった。横断法則一般補題化
  レーン（y>=15）は本実行では未着手。
- 単一オーナー宣言: commit `c34a19ff`（2026-11-22T20:33台・観測 HEAD
  `bcc761b8`・対抗宣言 grep 空・K1058/n11 系は非接触と確認）を検証器実行前に出版。
  保持範囲: part1 12チェック + part2（C1d/C11r・K1235 昇格判定）。
- 採番: K1236 を予備採番し、push 直前に最新 main で 3 点確認
  （commits・item path 404・knowledge README grep）。

## 機械構成

- 母体: 出版 verify_y14_universal.py part2 正本（commit 7026c860・SHA-256
  6ac219cf…）。y14 が y13 part1 機を母体に(part1を)組んだのと違い、本機は
  part2 版から C1d/C11r/cand13/anchor block を除去した構成で part1 を組んだ
  （builder の marker 限定抽出 + 禁止トークン gate で機械保証）。
- B子 = 出版 cand14（K1233 全称証明済み・逐語転写 5 連目〔y11..y14 に続き〕）。
  x>=15 行で使用し K1233 の定義域 x>=14 の内側。
- A子 x=15 合流子 (14,15)≡(15,14) → cand14(z,15,R-1)（y=14 族 x=15 行）。
- cand15 は出版 cand15.py（K1235 fit・SHA-256 f61997dd…）から fit driver 省き
  verbatim。builder・出版byte pin 2種（published_verify_y14_universal.py・
  published_cand15.py）を実験dir に同梱し SHA 照合で消費。
- 機械組立後に出版前 smoke spot 6種 計22,442点（raw照合・merger・B子・選択肢・
  マージ行全域raw〔fit probe boxに存在しなかった領域〕・tail行）すべて 0 不一致
  を確認してから本実行。

## 実行結果（part1 overall PASS）

- 12チェック総照合点 **6,349,309**・全 bad 0・型 335,658（C4時点 279,619）。
- C4t: clip 31 で **2,030 違反・最初 (60,94,94)** → clip 窓 2y+2=32 が tight・
  **11 族連続**（y=5..15）。最初違反がband下端offsetとともに歩く観察
  （(60,90,90)/(60,92,92)/(60,94,94))の3点目。
- merge corollary 1,304,870点（y=15 ではマージ領域が probe box に存在しなかったため
  本機が初の全域 raw anchor）・tail corollary 195,917点・ともに bad 0。
- census 443,520点/エンジン（4,480行・R<=x+z+16）・LRU cap 1.6M 双生機・
  ordered 15秒/canonical 19秒・12チェック一括 33秒。
- 決定性: 3実行 byte-identical（同一cwd 2回＋隔離 tree/cwd/HOME+
  PYTHONHASHSEED=random 1回・census parts は隔離側再生成で byte一致）。
- fail-closed 3/3 捕捉（census points 改ざん・part 欠落・corollary 境界改ざん
  → total_bad 223 で overall FAIL・rc=1）。

## 出版系列（各 push 後 fetch-back byte検証）

- commit A: 実験dir `vertical-fiber-two-token-y15-parametric-allz-proof-20261122`
  （README・verify_y15_universal.py・scripts/build_verify_y15.py・
  published byte pin 2種・output/audit.json・census parts・published_run.txt）
- commit B: K1236 item（status computed・part2 昇格判定は K1235/同一手続きに留保）+
  本 log
- commit C: knowledge README 末尾 bullet

## 知見・誠実記録

- y=14 の part2 正本を母体にしたため印刷体の差分が y13→y14 移行と少し異なる
  （part1 12チェック構成であることは禁止トークン gate で機械保証・
  生成物 942行）。
- published_run.txt に実行環境の制約（/usr/bin/time 不在のため date +%s
  計測・ホストで OOM なし）を記録。
- C8 の x=14 行は y14 機の x=13 行・y13 機の x=12 行と同じ閉形式
  extension-consistency 行として扱った（0 bad・README/itemに明記）。

## レジューム（着手前に必ず最新 main 再取得・hourly 並走注意）

- 次の最有力 = part2（同一宣言 c34a19ff の継続・着手条件は part1 着地済み）:
  (a) preflight_c1d_y15.py（y=15 行特殊化の 4方照合+z別点数・アンカー領域
  z0∈{8,9,10,15,16,17}・x=15..45・R<=x+z0+31・低R R<=z+6）
  → (b) census_rows.py 第三実装（XMIN=15・XMAX=70・RBUF=17・4,480行）
  → (c) 検証器 in-place 拡張（C1d/C11r 追加）→ フル14チェック 3回
  byte-identical → K1235 observed→proved 昇格・K1236 item part2追記。
- 昇格後の候補: 横断法則の y>=15 一般補題化レーン（y=1..15 全称が揃い
  帰納構造の一般証明価値が最高に）・y=16 族 fit（偶数y・seed法則4連続目の
  テスト）。
- 標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。3トークン以上・y>=16 族（fitを除く）・固定幅・
  q点版安定化長は範囲外。
