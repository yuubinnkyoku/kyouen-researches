# Four-row q=6 M_{4,6} reconcile — 2026-11-21

> **実験一次資料**：本文の判定・数値・計画は記録時点のものです。現在の結論・未解決・検証境界の唯一の正本は[knowledge](../../../knowledge/README.md)です。この資料を現在知識の正本として並行更新しません。

単一オーナー宣言: `research/log/2026-11-21-four-row-q6-m46-reconcile-single-owner-note.md`
（commit `df64d850`・2026-11-21T19:56Z・宣言時HEAD `af60cc65`・受入条件つき）。

## 背景（main上の矛盾の発見）

K0302（2026-10-03・status proved）は**M_{4,6}=16 の完全証明**（実験一次資料
`fixed-width/reports/q48-q6-exact-threshold.md`・同 `q48-nearby-q6-bounds.md`・
機材 q48_q6_exclusion.cpp / q46_pair_upper_bound.cpp / q48_nearby_q6_bounds.py と
完了 JSON 同梱）を出版済みである。しかし 2026-11-21 の四行q=6掃引レーン群
（K1177・第2..4次帯延伸）は K0302 に気づかず「M_{4,6} = 16 or ∈[35,103]」の
未閉鎖扱いで m=30..34 の再掃引を続けていた。`mwq_stabilization.csv` の
`exact-threshold,4,6,6,16,proved,K0302` 行と `results/fixed-width/README.md`
の確定値11件リストは (4,6)=16 を既に掲載したまま（矛盾）。

K1182 は同じ構図の前例である（K0302 が5閾値に含む M_{4,7}=13 を、掃引+K0318
上界の別経路で再閉鎖した）。3行q=4 では K1203 がリコンサイルを確定させた。

## 本実験の範囲（受入条件: 宣言のとおり・fail-closed）

K0302 証明の機械部分をこの環境で再検証し、矛盾を解消する。採用条件は:

1. **(a) 公刊 Python 再現器の byte 一致**: `q48_nearby_q6_bounds.py`
   （依存 `q48_exact_threshold.py`・`curve_packing_fixed_width.py`）を編集なしで
   実行し、出版 `output/q48_nearby_q6_bounds.json` と byte 比較。
2. **(b) 有限排除の第三実装再計算**: `q48_q6_exclusion.cpp` を Node.js に
   文対文移植（2系統: literal BigInt 参照実装 + 高速 uint32×9bit 実装）し、
   m=16..35 の全40ケースを出版 `q48_q6_finite_exclusions.json` の7計数フィールド
   （circles/target_subsets/reflection_representatives/searched_subsets/
   unknown_subsets/found_witness）と照合。全幅が予算内で不可能な場合は
   対象幅をスコープに明記し、残りは「未検証」として区別する。
3. **(c) 三行型計数上界の第三実装再計算**: `q46_pair_upper_bound.cpp` を
   Node.js に文対文移植し、出版 `q46_pair_upper_bound.json`（383,504形状・
   上界 6,6,7,6,7・合計 ≤19）と構造比較。
4. **(d) 現代的 UNSAT 帯延伸 m=35..38**: 同じ手続き（genfast3 生成・pinned
   kissat 4.0.4 linux-amd64〔md5 3a5eba830aa6008a604fcc9bbe99a325〕・各幅2回・
   conflicts bit-exact・較正 (4,34,6) CNF byte 一致）で
   四行frontier dir に第5次帯延伸として出版。
   成果物は frontier 実験 dir側
   （`four-row-q6-q7-frontier-20261121/output/q6ext5/`・
   `scripts/append_records_q6d.js`）に置く。

不一致・witness 発見・unknown>0 はすべて fail-closed（不採用）。判定は各時点の
 `- **各検証の結果**` に追記する。

## 各検証の結果（時系列・実行時刻は UTC）

- **(a) PASS（instance 1: ~19:52Z・instance 2: 20:24Z）** — 再現実行
  0.914 s、出力 7,959 bytes、出版 `output/q48_nearby_q6_bounds.json` と
  byte-identical（md5 `e33a78b6f8c71657cdcee1f7c9a1188c`・cmp exit 0）。
  §1-§5（packing 上界 U=103・四行弦分類 (1,3,3,1)/(35,51,63,73)/(73,63,51,35)・
  gap graph・blocker budget 67・4×15 の19石 witness）を一括検証。
  入力スクリプト3点は main と byte-identical（md5 `81fead2d…`/`56876f6a…`/
  `a9575c0a…`）。記録: `output/repro/repro_verification.json`・
  `output/repro/q48_nearby_q6_bounds_repro.json`。
- **(d) 較正 PASS（20:21Z）** — genfast3.js（md5 `12c2bd9c…`・SEVEN_SCRIPTS
  経由で sat.js `0cc6021a…`/sat2.js `282ae832…` を読む）で (4,34,6) def-mode
  CNF を再生成し、出版第4次帯延伸 CNF と byte 一致
  （md5 `1f58cdfc895ef4de493528ebf40d33f2`・calib meta 同梱）。
- **(d) 生成 PASS（19:55Z）** — (4,35..38,6) の CNF 4点を生成:
  m=35 vars 24908/clauses 86625/curves 1128・m=36 vars 26565/clauses 92388/
  curves 1205・m=37 vars 28222/clauses 98151/curves 1282・m=38 vars 30005/
  clauses 104352/curves 1365（gen meta 4本・cnf md5 4点とも記録済み）。
- **(c) PASS（20:19Z）** — Node 移植の再計算（20.1 s）が出版
  `q46_pair_upper_bound.json` と**構造完全一致**（jq -S 正規形の diff が空・
  5形状 × 全フィールド: 标準化5点集合 383,504・上界表 6,6,7,6,7〔t0 は
  (1,2),(1,3),(2,3) の3選択で計 19・t1 は (0,2),(0,3) で計 13・行2,3 は反射〕・
  32 chord profile 表も含む）。出版 3,169B と port 出力 8,821B の差は JSON
  pretty-print 幅のみ。記録: `output/q46replay/q46_compare.json`。
- **(b) 部分完了・進行中（20:19Z 時点）** — BigInt 参照移植 m=16,17（4ケース）
  と高速移植 m=17,18,19 が**出版 7/7 フィールド完全一致**（unknown=0・witness=0・
  m=17 は2移植クロス一致）。高速移植の掃引は m=20 以降も継続中（レジューム
  ドライバ: m 完了ごとに jsonl へ追記・kill/再開で途切れない設計）。掃引が
  m=35 に達するまでは「m=⟪N⟫ まで第三実装一致・残り未検証」として区別する。
- **(d) 進行中（20:19Z 時点）** — (4,35,6) run1 完了: **UNSAT・rc=20・
  conflicts 5,055,908・process-time 388.20 s**（wall 564 s はポート掃引との
  CPU 共有を含む）。run2 および m=36..38 は nohup detached ドライバで継続中。
  完了後にこの節を確定値で更新する。

## スクリプト

- `scripts/port_q48_exclusion.js` — q48_q6_exclusion.cpp の literal BigInt 移植
  （参照実装。実行: m=16,17）。
- `scripts/port_q48_exclusion_fast.js` — 同アルゴリズム・同一探索順の高速第二実装
  （9-word uint32 マスク・epoch 方式 open-addressing 失敗メモ。実行: m=17..35）。
  m=17 は bigint 移植とのクロスチェック幅。
- `scripts/port_q46_pair_upper_bound.js` — q46_pair_upper_bound.cpp の Node 移植。
- `scripts/compare_port_vs_published.js` — (b) の fail-closed 照合機
  （7フィールド全一致・unknown=0・witness なし・m=17 クロス固定・過剰重複禁止）。

## 出力

- `output/q48replay/port_bigint_16.txt` — bigint 移植 m=16,17 の4ケース。
- `output/q48replay/port_fast_17_35.jsonl` — 高速移植の掃引（m=17..35・逐次追記）。
- `output/q48replay/stdout_17_35.log`・`sweep_driver.log` — 生ログ（レジューム
  ドライバ: m ごとに node を起動し、jsonl の既存 (m,target) を検査して再開）。
- `output/repro/` — (a) の再現出力と pin 記録。
- `output/q6ext5/` — (d) の作業ディレクトリ。出版分（solve log 8本・gen meta
  4本・較正 meta 1点）は frontier dir 側へ移して公開する。

## 解釈規約

- 本実験は K0302 の status・本文を一切変更しない。上記 (a)-(d) がすべて
  PASS した場合、K0302 の先行証明を正として「M_{4,6}=16 は先行確定済み・
  K1177 の区間表記は置き換え可能」というリコンサイル判断を知識側
  （K1210・relations/knowledge README bullet）に記録する。
- (b)(c) の移植は同一アルゴリズムの再実装であり、手法の独立性は
  K1177 の SAT 符号化（census 非依存ではないが符号化独立）と隔たりがある。
  「第三実装による再生」は bit-exact 照合の意味で使う。
- 出力の conflicts 数・visited_states・実行秒数は品質の指標ではなく勝敗ではない。
- 標準 11×11 空盤・二石 root は本レーンの非目標のまま UNKNOWN。
