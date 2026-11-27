# Three-row q=4, m=27 SAT row-sum partition (P(27) independent second-method cross-check)

継続単一オーナー実行。宣言: `research/log/2026-11-28-three-row-q4-m27-partition-continuation-note.md`
(commit `65e22558`・宣言時 HEAD `6bf68e4b`・publish-then-execute・m=25 宣言 `02307f675` の
「実行時間が許す限り m=26 以降の増分掃引」条項の m=27 増分)。
姉妹 kit: `three-row-q4-m25-partition-20261128` / `three-row-q4-m26-partition-20261128`
(手法・器材 pin・split_piece.py の意味論は同一につき本 README では重複記述しない)。

## 主張（有限機械検証の正確な範囲）

1. **P(27) の SAT 行和分割による独立確認**: 3×27・q=4 の行欠損極大 witness の
   非存在を m=24/25/26 と同一の行和 63-triple 分割で掃引し、
   **全63 triple UNSAT・exactly-once 被覆**（`partition_closure_3row.py`・
   decided 63 / pending 0 / uncovered 0 / SAT 0）。P(27) は列挙閉包
   （three-row-q4-enumeration-20261121）で既に確定済みのため、本実行の新規性は
   **P(27) の 2方法化** のみ。**m≥28 の新幅主張はしない。**
2. **決定ピース台帳**（全68実行・全 UNSAT〔rc=20〕・合計 7,236,053 conflicts・INDET 0）:
   - row-k piece 4件: (0,0) 573・(0,1) 76,386・(1,0) 393・(1,1) 89,809
     （rowY=1 は --lex=H,V）。
   - row-sum piece 10件（lex=H）: (0,2,0) 1・(1,2,0) 0・(1,2,1) 963・(2,2,0) 87・
     (2,2,1) 6,528・(2,2,2) 17,659・(3,2,0) 106・(3,2,1) 14,888・(3,2,2) 224,135・
     (2,3,2) 228,502。
   - **(3,2,3) は leftmost-column 27分割で全滅**（合計 2,882,830 conflicts・
     最大片 c06 232,947）。**(2,3,3) も同 27分割で全滅**
     （合計 3,693,193 conflicts・最大片 c05 311,137）。
   - m=26 との比較: (3,2,3) 2,727,793 → 2,882,830（約1.06倍）・
     (2,3,3) 3,222,643 → 3,693,193（約1.15倍）。
     conflicts の集計和は参考値（非加法）で、UNSAT verdict が反証の本体。
3. **決定性の独立確認**: 代表2件（s:2,2,2 = 17,659・s233_c11 = 302,123）の
   再実行で conflicts bit-exact 一致（rc 一致・per-second 表示のみ相違）。
4. **閉包**: 汎用 `partition_closure_3row.py`（m26 kit 版 byte-clone・board_tag=m27）。
   coverage 63/63・sat_triples 空。

## 較正（宣言文に事前開示）

- m=26 全16 CNF を本環境で再生成し m26 kit 出版 manifest と md5 16/16 byte-exact
  一致（rowY=1 は --lex=H,V・rowY=0 は --lex=H・row-sum は --lex=H）。
  m=27 CNF 生成は同一 pin 器材の増分適用。m25 kit の (3,23,4) 陽性対照は
  姉妹 kit で bit-exact 済みのため本幅では追加較正なし（m26 kit と同一規律）。

## 器材 pin（宣言文と同一）

sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`・
sat3.js md5 `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js md5 `96a84063f77bb45463ba470f05a06d58`・
verify34.py md5 `7b97ef1ac727b0741847a81d4dea9bc8`・
kissat 4.0.4 linux-amd64 sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`。
CNF 再生成用 md5 台帳: `output/cnf_manifest_m27.txt`（70 file・CNF 本体は size policy で非出版）。

## 再現コマンド

    node scripts/sat3.js 3 27 4 --rowY=0 --kex=0 --lex=H cnf27/k_r0_0.cnf
    node scripts/sat3.js 3 27 4 --rowY=1 --kex=0 --lex=H,V cnf27/k_r1_0.cnf
    node scripts/sat4.js 3 27 4 --rspec=0:3,1:2,2:3 --lex=H cnf27/s_3-2-3.cnf
    python3 scripts/split_piece.py cnf27/s_3-2-3.cnf 27 1 cnf27/split323 s323
    ./kissat-4.0.4-linux-amd64 cnf27/split323/s323_c06.cnf
    python3 scripts/partition_closure_3row.py output/records_m27.jsonl m27

## 開示

- 分割片実行は bash 呼び出し cap のため 1回の呼び出しで2-8片を逐次実行
  （280s/片 timeout・全片 cap 内で決着・INDET 0）。
- 実行台帳 `output/ledger_m27.jsonl` は実行順・開始終了時刻 (UTC)・rc・conflicts
  を1行1片で記録。`output/raw_decisions_m27.txt` は各片の kissat 統計行
  （conflicts・process-time・exit）を抜粋。
- 本レーンは w=3 固定幅で標準 11×11 盤に無関係。**verdict NOT consumed・
  標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN。**

## レジューム（着手前に必ず最新 main 再取得・hourly 並走注意）

1. **m=28**: 同一手順で P(28) の 2方法化が可能。分割片は m=27 比でさらに
   約1.1-1.2倍と見込まれる（最大片 ~350k conflicts・cap 内見込み）。
2. m≥32 は SAT 分割では片当たり数千万 conflicts 見込みで非現実的。
   列挙閉包側 wsearch34.js の m≥32 治具拡張（BigInt 化等）が本命（K1183 レジューム）。
