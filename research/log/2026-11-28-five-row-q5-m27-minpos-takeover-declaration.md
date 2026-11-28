# 2026-11-28 five-row q5 5x27 class {0} krow=0:3 minpos p=4..13 sweep takeover — declaration (single-owner, publish-then-execute)

- 本レーンは停滞レーン `research/experiments/five-row-q5-m27-minpos-sweep-20261115/`
  (IN FLIGHT 2026-11-15・実行環境喪失で raw/records とも p1..p3 のみ出版・13日停滞) の
  **takeover** を宣言する。対象: **(5,5) 前線 5×27 class {0} krow=0:3 minpos p=4..13** の掃引
  (sound H-split bound min(x1, 26−x3) ≤ ⌊(m−1)/2⌋ = 13)。p4/p5 は旧レーンの手記値
  (INDET 3,317,615 / 3,501,337) が raw log 喪失で reported-only のため**再実行で置き換える**。
  p1..p3 (INDET 2,961,487 / 3,233,600 / 3,398,950 @400s・出版済み records.jsonl) は再実行しない。
- 実行時 HEAD: 88a24418f441a640a7becd28c25d5a39a0687b7f。
- 目標: SAT ⟹ 5×27 witness で witness 帯 m=5..27 延伸・**M_{5,5} ∈ [28, 336]**
  (CSV/K0833 更新・witness は decode + verifyConfig + verify_frac.py の複数系統検証)。
  UNSAT は当該サブインスタンスの決定的除外。INDET は cap 到達の honest negative であり
  **不在主張ではない**(k=0..2・他クラス・H/V 鏡像類は残る・19 正準類の完全掃引でない)。
- 手法・較正 (宣言前実施・開示): 生成器 sat3.js md5 d03f908ea99ba819caee2a6fbb471c1b
  (sat2 282ae832efa0080127c6c153e65e1c3c・sat.js 0cc6021a4e523a0d7f4d5ea0f5f5d40c)・
  kissat 4.0.4 official prebuilt md5 3a5eba830aa6008a604fcc9bbe99a325。
  CNF md5 bit-exact: 5×27 c0k3p0 4d2b52a8203591e13cfc8ae126beb9b5・
  c0k3p1 6808000255911616de71430c6a0080cb・c0k3p2 47b3f40d6d636b4cf08a5b7765bf71b3・
  5×25 c0 1d62f2428fd5fb2fdba5cfd19114d78e・5×26 c0 60e71cfd2f1620cfa9b4070f259c1572。
  エンドツーエンド較正 (本環境・bit-exact): **5×25 c0 SAT 35,972 conflicts**・
  **5×26 c0 SAT 1,631,556 conflicts / 204.22s** — いずれも出版値と conflicts 完全一致。
- cap は旧計画の 400s から **285s に変更**(本実行環境の呼び出し上限 300s 内に収めるため・開示)。
  予想抵抗は p1..p3 帯 (2.9M..3.4M conflicts @400s) と同程度。
- 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。
- 結果着地時に records.jsonl 増分・raw logs・README COMPLETED 更新・完了 log を main 直接出版。
