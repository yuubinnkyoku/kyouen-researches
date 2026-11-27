# Three-row q=4, m=28 SAT row-sum partition (P(28) independent second-method cross-check)

継続単一オーナー宣言: `research/log/2026-11-28-three-row-q4-m28-partition-continuation-note.md`
(commit `cfcdffdeb7afa26e000251c46edb27965bcce9f0`・宣言時 HEAD `548695e70c8544d8637fb26221c959a149092da9`・
publish-then-execute)。元宣言 `02307f675f4c3c0d2700ca470b173b4c2310fd54` の
「実行時間が許す限り m=26 以降の増分掃引」条項の m=28 増分。
姉妹 kit: `research/experiments/three-row-q4-m25-partition-20261128/`（治具・較正・
split_piece.py の意味論）・`three-row-q4-m26-partition-20261128/`（閉包スクリプト一般化）。
並走の m=27 実行（`ddbe1392`・2026-11-27T19:55Z 完了）とは掃引幅で完全分離。

## 主張（有限機械検証の正確な範囲）

1. **P(28) の SAT 行和分割による独立確認**: 3×28・q=4 の行欠損極大 witness の
   非存在を m=24..27 と同一の行和 63-triple 分割（row-k piece 4件 +
   row-sum piece 12件〔うち2件は分割で決着〕）で掃引し、
   **全63 triple UNSAT・exactly-once 被覆**（`partition_closure_3row.py`・
   decided 63 / pending 0 / uncovered 0 / SAT 0）。P(28) は列挙閉包
   （three-row-q4-enumeration-20261121・ext28plus）で既に確定済みのため、
   本実行の新規性は **P(28) の 2方法化** のみ。**m≥29 の新幅主張はしない。**
2. **決定ピース台帳**（全70実行・全 UNSAT・合計 8,381,193 conflicts）:
   - row-k piece 4件: (0,0) 408・(0,1) 82,598・(1,0) 380・(1,1) 78,112。
   - row-sum piece 10件（lex=H）: (0,2,0) 1・(1,2,0) 0・(1,2,1) 1,147・
     (2,2,0) 70・(2,2,1) 3,520・(2,2,2) 27,560・(3,2,0) 143・(3,2,1) 14,173・
     (3,2,2) 312,503・(2,3,2) 275,232。
   - **(3,2,3) は leftmost-column 28分割で全滅**（合計 3,364,388 conflicts・
     最大片 c07 264,558・非自明片は c00..c26・c27 は lex 制約で即時 UNSAT 0 conflicts）。
     **(2,3,3) も同 28分割で全滅**（合計 4,220,958 conflicts・最大片 c11 318,508・
     c27 は同様に 0 conflicts）。分割の意味論・完備健全性は m25 kit の
     `split_piece.py` と同一（ベース片の一体実行は実施せず・分割28片の全 UNSAT で反証）。
   - m=26 との比較: 決定打 (2,3,3) 分割合計は 3,222,643 → 4,220,958（約1.31倍/2幅）、
     (3,2,3) は 2,727,793 → 3,364,388（約1.23倍/2幅）。1幅あたり約1.11-1.15倍で、
     cap 300s に対する最大片（318,508 conflicts・wall 44s @本環境）には十分な余裕。
   - conflicts の集計和は参考値（非加法）で、UNSAT verdict が反証の本体。
3. **決定性の独立確認**: 代表2件（s233_c11 = 318,508・(2,2,2) = 27,560）の
   再実行で conflicts bit-exact 一致（rc 一致・wall のみ相違）。
4. **閉包**: `partition_closure_3row.py`（m26 kit 版・byte-clone）で
   records 台帳から decided 63 / pending 0 / uncovered 0 / SAT 0 を機械検査
   （`output/m28_partition_closure.json`・exit 0）。

## 較正（宣言時に開示済み・宣言文に同じ）

- m=26 の全16 CNF を本環境で再生成し m26 kit 出版 `cnf_manifest_m26.txt` の
  md5 と **16/16 byte-exact 一致**。
- pinned kissat で m=26 代表4片（s_0-2-0 / k_r0_0 / s_2-2-2 / s_3-2-2）を実行し
  出版 `records_m26.jsonl` の conflicts（1 / 611 / 18,195 / 202,989）と
  **4/4 bit-exact 一致**（全 UNSAT）。以降は同一 pin 器材の増分適用。
- m=28 CNF メタ: curves 10,269（m=26 は 8,083）・rspec (2,2,2) 片で
  vars 105,000 / clauses 347,395。CNF 本体は size policy で非出版
  （`output/cnf_manifest_m28.txt` が md5 台帳）。

## 開示

- 分割片実行は bash 呼び出し cap のため 1回の呼び出しで予算内の数片を逐次実行
  （wall 予算駆動・全片 cap 内で決着・INDET 0・タイムアウト片なし）。
- 本レーンは w=3 固定幅で標準 11×11 盤に無関係。**verdict NOT consumed・
  標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN。**

## 器材 pin（m25/m26 kit と同一）

sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`・
sat3.js md5 `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js md5 `96a84063f77bb45463ba470f05a06d58`・
verify34.py md5 `7b97ef1ac727b0741847a81d4dea9bc8`・
kissat 4.0.4 linux-amd64 sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`
（release zip `kissat-4.0.4-linux-amd64.zip` sha256 `63282e5168ca040a2018edfba0726bf893a7a6bcdb1db87feb67857e2da697a7`）。

## 再現コマンド

    node scripts/sat3.js 3 28 4 --rowY=0 --kex=0 --lex=H cnf/k_r0_0.cnf
    node scripts/sat4.js 3 28 4 --rspec=0:3,1:2,2:3 --lex=H cnf/s_3-2-3.cnf
    python3 scripts/split_piece.py cnf/s_3-2-3.cnf 28 1 split/s323 s323
    ./kissat-4.0.4-linux-amd64 split/s323/s323_c07.cnf
    python3 scripts/partition_closure_3row.py output/records_m28.jsonl m28 > closure.json

## レジューム（着手前に必ず最新 main 再取得・hourly 並走注意）

1. **m=29**: 同一手順で実行可能（P(29) の2方法化・分割片は約1.1-1.15倍/幅で
   cap 内 見込み）。m=27 レーンが m≥28 不着手を宣言しているため、m=29 は
   新規単一オーナー宣言が必要。
2. m=30/31 も同様だが、列挙閉包 m=30/31 は chunk 分割で確定済み。
3. **m≥32 は SAT 分割では片当たり数千万 conflicts 見込みで非現実的**
   （K1183 の指摘どおり列挙閉包側 wsearch34.js の m≥32 治具拡張〔BigInt 化等〕が本命）。
