# 単一オーナー宣言: K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証（2026-11-20）

本ノートは、残余29行レーンの3証明書抽出
（K1136: root `00000000000000043800000008180010`・K1137: root
`00000000000200003800200008180000`・K1139: root
`0000000800000000380000000810000a`）に対する**外部第二検証**
（出版実験dirのbyte pin → probe・抽出・検証器・監査機械の新規再実行 →
出版正本との照合）を単一オーナーで着手する宣言である。
fold/fold23/fold25/fold26外部第二検証・round-5 refsolve・WIN8-D10 root
`00000000010000809002000040002001` 証明書抽出・WIN8証明書行共有監査は
他レーンが宣言済みであり本宣言の対象外。fold24候補A/Bのreceipt foldも対象外。

## 受入条件

1. **出版byte pin**: 3実験dir
   `n11-residual29-win8-cert-extract-root438000000818-20261120/`・
   `n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/`・
   `n11-residual29-win8-cert-extract-root0810000a-20261120/` の全61ファイルを
   GitHub raw（pinned commit）から取得し、git blob SHA-256とbyte一致で照合
   （runner v17固定コピー git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`
   3点・証明書3点 SHA-256 `dbcb0bae…`/`7bd64a47…`/`089e175d…` 込み）。
2. **probe再現**: 各rootで両AND順序×2回=4 probe＋pilot_d6制御4件を
   pinned runner v17でfresh実行し、出版probe-repro-both-orderings.jsonlの
   nodes・loss・terminal石数・capped と**値完全一致**（`ms`は時刻依存で
   再現対象外とする。K1160の`wall_s`学knowsと同型）。
3. **抽出再現 (A1/A2/B)**: 各rootでA1（初手毎新規プロセス・xargs -P 2・
   実行環境が2コアのため控えめ並列）を2回（A1・A2）とRun B（単一プロセス一括）
   を新規実行し、(a) per-move nodes/nRows/fbt_drops/fatal が出版
   ext-summary-a1/a2/b.jsonl と node-exact・(b) A1==A2 per-move完全一致・
   (c) A1の証明書組立（header行+root行+sorted-unique戦略行）が出版証明書と
   **byte-identical**（SHA-256 3点再一致）。`ms`は再現対象外。
4. **検証器再実行**: BigInt独立検証（`verify_win8_certificate_bigint_independent.mjs`）
   とBareiss検証（`verify_win8_cert_bareiss.ts` root-check＋subroots全走査）を
   出版証明書に新規実行し、出版 `bigint-verification.json`・
   `bareiss-root-check.json`・`bareiss-stats.txt` と比較（byteまたは値完全一致）。
5. **監査機械再実行**: `assemble_win8_audit_root*.py` を出版dirのpristine
   複写（取得byteそのまま）で新規実行し、出版監査正本
   `output/win8-cert-extract-verification-20261120.json` 3点
   （SHA-256 `d0653834…`〔K1136〕・`dafa177b…`〔K1137〕・`e706ca6f…`〔K1139〕）
   と**byte-identical**（19/19 gate PASS）。同一cwd 2回＋隔離cwd 1回の3実行で
   出力byte一致。APIコスト上、rootごとの監査機械再実行回数は合計で
   2回×3root以上を確保する。
6. **tamper 3件**: 出版社が試験していないoffsetでの1 byte改変（証明書本文・
   監査pin入力JSON・ext-summaryのnodes値の各1件）がfail-closed捕捉
   （returncode非0・監査正本未書込・gate fail・検証器verdict非PASSのいずれか）
   であることを機械確認。
7. **出版とguard**: 成果はpart1（self-contained実験dir）→ part2（K item＋研究log）
   → part3（knowledge README末尾bullet）で出版。K番号はpush直前3点確認。
   **本検証は行を1つも閉じない。残余行数・pool P⁗ 120,416根は不変。**
   nodes数・solved数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。
   **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
   すべてUNKNOWNのまま。**

## 実行資源

- 共有環境のCPUは2コア。抽出・検証器は原則並列度2（xargs -P 2）で実行し、
  高負荷の常時占有を避ける。失敗・timeoutも実験事実として記録する。
- pin取得基準commit: `28d223a2d`（2026-11-20 19:41Z時点のmain HEAD。
  実験dir・正本は出版後不変のため、取得時点のmain pinでよい）。
