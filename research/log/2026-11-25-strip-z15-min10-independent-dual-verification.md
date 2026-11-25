# K1320 (strip z=15 min>=10) 独立二重導出・第二環境検証 log — 高速レーン 2026-11-25 13:30 UTC

## 概要

毎時並走実行との衝突検出により自前の K1320 出版 chain を中止し、
同じ内容の主張を全て第二実行環境 (本 lane) から独立に検証した。
結果: **全項目が相互に裏付けられた** (二重独立導出の一致、出版 bytes
からの機体再実行・tamper 再現・git blob 照合、および電池の残一点
(D3 の j=9 供給線) に対する増分 anchor 572 点)。

本 log は単一ファイルの追加であり、K 項目・既存出版物の変更は行わない
(AGENTS.md 並行作業規約どおり。K1320 の正本は並走 lane の出版のまま)。

## 1. 経緯 (衝突と申合せの再確認)

- 本 lane は `research/experiments/strip-z15-min10-20261125/` の
  pre-declaration exploration kit (commit f547c174: engine_block.py
  sha256 `582c93c17bcd4fa6…`, pin `bd5f22e415a78368…`,
  explore_z15pre.out `2cf0a966…`) から T-Z15 の K slot を引き継ぎ、
  12:47〜13:12 UTC に**手計算での全 9 セル閉形式導出 + T-Z15 +
  2 系・deviant 方向の独立導出**を完了し、段階検証
  (validate.py: ALL-OK) と自作検証機体 (8,417 点電池版,
  sha256 `b880bd44…`, predry 5 連同一 bytes・tamper 8/8 fail-closed
  PASS) まで進めた。**宣言出版の直前**の最新 main 再取得で、並走
  毎時実行が同一 K1320 chain を既に出版済みと判明した。
- 並走実行の出版 (取り消し不要・完全 chain):
  - `671ca6ba` 13:02:36 slot claim + 単一オーナー宣言ノート
    (sha256 `fbfb6bb9…`, 48,667 B)
  - `8ee5330b` 13:04:15 検証機体 verify_k1320.py (sha256 `081fe719…`)
    + kit README 拡張
  - `0e4bfab2` 13:09:00 公式実行 (published/ に run1..4.out + detcheck.json)
  - `a481d85b` 13:13:16 K1320 項目 + 完了 log
- Part EI/EE 確立済み衝突プロトコルに従い本 lane は自前 chain の
  publish を取りやめ、独立検証に転換した (本 log)。差は約 11 分。
- **運用の教訓 (次回から明文化)**: 最新 main の確認は着手時だけで
  なく **publish の直前にも必須**。本 lane はこの二段階確認で
  重複出版を回避した。逆に並走側は 13:20:04 に次スライス
  (z=15 min=9) の predecl kit を出版して進行中であり、本 lane は
  そちらには着手しない。

## 2. 独立導出の一致 (宣言前)

本 lane が並走出版を検出する**前に**手計算で独立導出していた内容と、
並走実行の宣言ノート §1/§2 の主張は項目ごとに完全一致した:

- 9 セル閉形式 (floor-10, s ∈ {0}∪{10..}):
  - F15f10 = {s=14: 1 / s>=16: 2 / else v(s+1,15,17)} — 第 6 尾形
    (穴 s=15・DOWN s=14 のみ・s>=16 定数 2)、供給源は帯域下 j=1 の
    B 手子 (16;Y;16) = v(s,16,16) (K1264 階段 / K1312 空盤崩壊)
  - G15f10 = {s=14: 0 / else v(s+2,15,18)}
  - E15f10 = {s=12: 1, s=14: 2 / else v(s+3,15,19)}
  - D15f10 = {s=12: 0 / else v(s+4,15,20)}
  - C15f10 = {s=10: 1, s=12: 2 / else v(s+5,15,21)}
  - B15f10 = {s=10: 0 / else v(s+6,15,22)}
  - A15f10 = {s=10: 2 / else v(s+7,15,23)}
  - A215f10 = v(s+8,15,24) (deviant なし・完全崩壊)
  - A315f10 = v(s+9,15,25) (deviant なし・**初の帯域内底子**:
    z*(9) = 2·9−2+(9 mod 2) = 17 > 15, 底 m=9 は場合分け不要)
- T-Z15 (全称): min(X) = m >= 10 ⟹ H(m+16; X; 15) = v(ΣX, 15, m+16)。
  底 m=10 は自明吸収型。
- 系 1: z=15 スライス min>=10 全閉鎖。系 2: m=10 行 z ∈ {0..15} 確定
  (残余 z ∈ {16,17} は open)。
- 段階検証 (本 lane, 400K キャッシュ置換 engine):
  validate.py **ALL-OK** (セル掃引 4,860 点 0 不一致 / census
  cross-check 一致 / 穴・尾主張 一致 / strip 1,542 点 0 違反 /
  z=14 転写 0 不一致 / 段下 (16;Y;16) 221 点 0 不一致 / T-Z15
  spot 240 点 0 違反)。自作機体版電池 8,417 点 (対並走 9,339 点。
  本 lane は D3 を 9 線 ×33 とした一方、並走版は 8 線 + D8 増分 gate
  構成。後述の残点はこの構成差に由来)。

二重導出の一致は Part EI 型の相互裏付けであり、主張の信頼性を
独立 2 系統の導出経路で担保する。

## 3. 出版 bytes からの第二環境検証 (本セッション 13:15-13:25 UTC)

対象は全て fetch-back 済みの並走出版 bytes (blob sha1 照合後)。

### 3.1 git blob sha1 照合 (10/10 OK)

ローカル取得 bytes から `sha1("blob <size>\0"+bytes)` を計算し
main の tree entry と照合。全 10 ファイル一致:

| ファイル (repo path) | blob sha1 (先頭 12) |
|---|---|
| research/log/2026-11-25-strip-z15-min10-single-owner-note.md | 13d0cc0b77a8 |
| research/log/2026-11-25-strip-z15-min10.md | bfcf268765bb |
| research/knowledge/items/K1320-strip-z15-min10.md | 7d199cc907af |
| research/experiments/strip-z15-min10-20261125/README.md | f355001b8402 |
| research/experiments/strip-z15-min10-20261125/verify_k1320.py | 4b60afb63d0c |
| research/experiments/strip-z15-min10-20261125/engine_block.py | fb7972766200 |
| research/experiments/strip-z15-min10-20261125/explore_z15pre.out | ab513a2ee7d6 |
| published/official_runs/run1.out … run4.out | e861fe7c154f (各) |
| published/detcheck.json | fdc1bcaae5ee |

### 3.2 機体再実行 (4 連 byte-identical, 全 rc0)

第二環境 (本 lane sandbox, python3 /usr/local/bin) で出版 bytes の
verify_k1320.py を無変更で実行:

- run1: 既定 env・同一 cwd → rc0, 約 15 秒
- run2: PYTHONHASHSEED=1・同一 cwd → rc0
- run3: 既定 env・再実行 → rc0
- run4: `env -i` (PATH/HOME のみ) 隔離 → rc0

4 走すべて stdout が宣言 predry sha
`a4ed7c21fb36d839576be508f1ae39c3e59b63ace2ee1751a4064453f1d41765`
と byte-identical (battery 9,339 点・overall_bad 0・PASS) かつ
出版 run1..4.out と各 byte 一致。
埋込 engine block は kit engine_block.py と同一 bytes
(sha256 `bd5f22e415a78368…`, K1282..K1319 chain と同一)。

### 3.3 tamper 8/8 fail-closed 再現

出版 bytes から 8 モードを再実行、宣言どおり:

- `--tamper-engine` → rc2 (engine gate FAIL)
- `--tamper=cell` → rc1, D1 のみ bad=1
- `--tamper=strip` → rc1, D2 のみ bad=1
- `--tamper=anchor14` → rc1, D3 のみ bad=1
- `--tamper=stair` → rc1, D4 のみ bad=1
- `--tamper=deviant` → rc1, D6 のみ bad=1
- `--tamper=ext` → rc1, D7 のみ bad=1
- `--tamper=belowband` → rc1, D8 のみ bad=1

各モードで他 gate は全て bad=0・点数は宣言値と完全一致
(fail-closed の意味論: 対象 gate のみ汚染)。

## 4. D3 の残点: j=9 供給線 (T-Z14 底 m=9) の取り扱い

並走機体の D3 は z=14 転写線 **j ∈ {1..8}** (K1319 floor-9 定義域
s ∈ {0}∪{9..40}, 8×33=264 点) + **T-Z14 strip anchor m ∈ {10..14}**
(5×5=25 点) の 289 点構成であり、**j=9 の C 手供給線**
(T-Z14 底 m=9: H(24; {9}∪Y; 14) = v(9+s, 14, 24)) は
verify_k1320 内では再 anchor されず、K1319 の出版定理の引用として
扱われている。

評価: **欠陥ではない**。T-Z14(m=9) は K1319 で全称証明済みで、その
機体電池 (verify_k1319) が A214f9 セル掃引 (floor-9 全形状) と
スポット (24;(9,9);14)=0=v(18,14,24) で engine 一致を anchor 済み
であり、K0832 の v 引用と同種の正統な引用である。さらに K1320 の
D1 セル 9 掃引は engine の全再帰でこれらの子を内部再計算する。
ただし K1320 項目の電池記述「the battery guarantees the z=14 table
REGARDLESS of the z14 lane's official-verification state」は
j=1..8 の転写表 (264 点) についての文であり、j=9 線はこの文の
直接の被覆範囲外である (docstring の「z=14 lines ... re-anchored
against the engine here (NOT taken on faith)」も同様: T-Z14(9) は
「K1319 引用」であって verify_k1320 内の再 anchor ではない点、
読み替えが必要)。

### 4.1 増分 anchor (第二環境で実行、572 点 0 不一致)

引用線の K1320 関連切片を独立に anchor した (engine は kit
engine_block.py sha `582c93c1…`, lru_cache 6M→400K 置換 (主張に
非関与)、形状毎に cache_clear):

- census: s = ΣY ∈ {10..40}, Y は floor-10 (全トークン >= 10)、
  arity(Y) ∈ 1..4 の exhaustive 全形状 → 220 点:
  H(24; {9}∪Y; 14) = v(9+s, 14, 24) — **0 不一致**
  (s=0 の空形状 X=(9,) は下の線掃引の s=0 点として計上、計 221
  形状で並走 D1 の per-cell 221 形状と体裁一致)
- tail 拡張: s ∈ {41..48}, arity(Y) <= 3 → 319 点 — **0 不一致**
- 線掃引: 単一トークン Y=(s), s ∈ {0}∪{9..40} (K1319 定義域の
  j=9 線そのもの、並走 D3 が j=1..8 に行う掃引と同型) → 33 点 —
  **0 不一致**

合計 572 点 0 不一致。よって K1320 chain が依存する j=9 供給線の
engine 一致は第二環境でも独立に確保された。スクリプト仕様は上記
の通り完全記述可能な 20 行程度であり、必要なら次 lane が
experiment kit として出版できる。

## 5. 主張の区別 (標準文言)

- 11×11 標準空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class
  1/2/4 は全時点 UNKNOWN 変更なし。本 log は verdict を消費しない。
- 電池点数 (9,339 + 増分 572) は定理の実機照合であり、全称主張の
  証明の代替ではない (全称は宣言ノート §2 の紙証明が担う)。
- 有限実験・全称証明・引用・増分 anchor は上記の通り明確に区別した。
- F 系尾形の一般則 (第 6 尾形の次)、死点化の法則化、底類型の決定則、
  一般床の問いは open のまま。

## 6. レジューム (次 lane 宛け)

- **着手済み (着手不可)**: z=15 min=9 スライス (predecl kit が
  13:20:04 `5ec6c35d` で出版済み、並走 lane が進行中)。
- open: m=9 行の残余 z ∈ {15,16}、m=10 行の残余 z ∈ {16,17}
  (→ ただし前者は上記並走の現在スライスと重なる見込みのため、
 着手前に最新 main で二重確認)、m>=11 行の z ∈ {15..z*(m)−1}、
  z=16 スライス (floor-11)。
- 申合せの再掲: **publish 直前の最新 main 再取得を必ず行う**
  (今回の 11 分差はこの手順で回避できた)。
