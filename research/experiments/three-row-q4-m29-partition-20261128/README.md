# Three-row q=4, m=29 SAT row-sum partition (P(29) independent second-method cross-check)

継続単一オーナー宣言: `research/log/2026-11-28-three-row-q4-m29-partition-continuation-note.md`
（commit `400f7e862c81628f850f8ab599a7b4067dc1076f`・2026-11-27T22:45Z・
宣言時 HEAD `2691ac0471`・publish-then-execute・較正事前開示つき）。
元宣言 `02307f675f4c3c0d2700ca470b173b4c2310fd54` の「m=26 以降の増分掃引」条項の
m=29 増分。姉妹 kit: `three-row-q4-m25/m26/m27/m28-partition-20261128/`。
m≥32 列挙閉包レーン（takeover 宣言 2026-11-27T20:05Z）とは完全分離。

## 主張（有限機械検証の正確な範囲）

1. **P(29) の SAT 行和分割による独立確認**: 3×29・q=4 の行欠損極大 witness の
   非存在を m=24..28 と同一の行和 63-triple 分割（row-k piece 4件 +
   row-sum piece 12件〔うち2件は leftmost-column 29分割で決着〕）で掃引し、
   **全63 triple UNSAT・exactly-once 被覆**（`partition_closure_3row.py`・
   decided 63 / pending 0 / uncovered 0 / SAT 0・exit 0）。P(29) は列挙閉包
   （three-row-q4-enumeration-20261121・ext28plus）で既に確定済みのため、
   本実行の新規性は **P(29) の 2方法化** のみ（P(24)..P(28) と同格）。
   **m≥30 の新幅主張はしない。**
2. **決定ピース台帳**（全72実行・全 UNSAT・conflicts 合計 8,915,494・参考値）:
   - row-k piece 4件: k:0:0 431・k:0:1 111,497・k:1:0 275・k:1:1 82,390。
   - row-sum piece 10件（lex=H）: s:0,2,0 1・s:1,2,0 0・s:1,2,1 958・
     s:2,2,0 65・s:2,2,1 4,599・s:2,2,2 18,695・s:3,2,0 208・s:3,2,1 14,725・
     s:3,2,2 272,177・s:2,3,2 206,727。
   - **(3,2,3) は leftmost-column 29分割で全滅**（合計 3,840,005 conflicts・
     最大片 c01 268,827・c28 は lex 制約で即時 UNSAT 0 conflicts）。
   - **(2,3,3) も同 29分割で全滅**（合計 4,362,741 conflicts・最大片 c13 308,847・
     c28 は同様に 0 conflicts）。分割の意味論・完備健全性は m25 kit の
     `split_piece.py` と同一（ベース片の一体実行は実施せず・分割29片の全 UNSAT で反証）。
   - m=28 との比較: (2,3,3) 分割合計 4,220,958 → 4,362,741（1.03倍）・
     (3,2,3) 3,364,388 → 3,840,005（1.14倍）。最大片 wall は 54s（s323_c00）で
     cap に対して十分な余裕。
3. **決定性の独立確認**: 代表2件（s233_c12 = 298,432・s:2,2,2 = 18,695）の
   再実行で conflicts bit-exact 一致（rc 一致・wall のみ相違）。
4. **閉包**: `partition_closure_3row.py`（m28 kit 版・byte-clone）で
   records 台帳から decided 63 / pending 0 / uncovered 0 / SAT 0 を機械検査
   （`output/m29_partition_closure.json`・exit 0）。

## 較正（宣言時に開示済み・宣言文に同じ）

- m=28 base 16 CNF を本環境で再生成し出版 `cnf_manifest_m28.txt` と
  **16/16 md5 byte-exact 一致**。
- pinned kissat で m=28 代表3片（k_r0_1 = 82,598 / s_2-2-2 = 27,560 /
  s233_c11 = 318,508）を再実行し出版 records・raw_decisions と
  **3/3 conflicts bit-exact 一致**（全 UNSAT）。
- m=29 CNF メタは `output/cnf_manifest_m29.txt`（16 file・CNF 本体は size policy で非出版）。

## 開示（正直な失敗・制限）

- **s_3-2,2 ベース片の wall 上昇**: m=29 の s:3,2,2（272,177 conflicts）は
  本環境で 107s を要し、runner の per-piece 100s cap を2度 KILLED した後、
  単独再実行で決着（rc=20 UNSAT・決定性は台帳どおり）。INDET ではない。
- 実行環境の reset が宣言後に2回発生し作業 tree を喪失した（kissat・pinned
  scripts・CNF を再取得・再生成し、md5 pin で同一性を再検証して続行した。
  m=28 較正は再構築後の器材で実施したものを採用）。
- conflicts の集計和は参考値（非加法）で、UNSAT verdict が反証の本体。
- 本レーンは w=3 固定幅で標準 11x11 盤に無関係。**verdict NOT consumed・
  標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN。**

## 器材 pin（m28 kit と同一・本環境で md5 再検証済み）

sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js `282ae832efa0080127c6c153e65e1c3c`・
sat3.js `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js `96a84063f77bb45463ba470f05a06d58`・
verify34.py `7b97ef1ac727b0741847a81d4dea9bc8`・
split_piece.py（m28 kit版）`0a6f6db104ab5bde34154d10c25f0799`・
partition_closure_3row.py（m28 kit版）`0d4d837b0f2724bfb47979cdf16154f8`・
kissat 4.0.4 linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325`
（sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`）。

## 再現コマンド

    node scripts/sat3.js 3 29 4 --rowY=0 --kex=0 --lex=H cnf/k_r0_0.cnf
    node scripts/sat4.js 3 29 4 --rspec=0:3,1:2,2:3 --lex=H cnf/s_3-2-3.cnf
    python3 scripts/split_piece.py cnf/s_3-2-3.cnf 29 1 split/s323 s323
    ./kissat-4.0.4-linux-amd64 split/s323/s323_c01.cnf
    python3 scripts/partition_closure_3row.py output/records_m29.jsonl m29 > closure.json

## レジューム（次回・着手前に必ず最新 main 再取得・hourly 並走注意）

1. **m=30 の同一分割掃引**（P(30) の第二方法化・最後の列挙閉包単独幅は
   m=30 と m=31）。分割片は m=29 比で約1.0-1.15倍と見込まれるが、
   s:3,2,2 型ベース片の wall 上昇（m=29 で 107s）に注意。
2. m=31 の後は SAT 分割の現実的な限界。m≥32 は列挙閉包 jig レーン
   （takeover 済み）の所有権。
3. 6x26 四レーン・n10 safe-set・n11 コスト系には不参入。
