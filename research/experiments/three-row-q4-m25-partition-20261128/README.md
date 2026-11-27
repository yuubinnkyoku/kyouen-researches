# Three-row q=4, m=25 SAT row-sum partition (P(25) independent second-method cross-check)

単一オーナー宣言: commit `02307f675f4c3c0d2700ca470b173b4c2310fd54`
(`research/log/2026-11-28-three-row-q4-m25-partition-single-owner-note.md`・2026-11-27T17:58Z・
宣言時 HEAD `07937d7415`・publish-then-execute)。

## 主張（有限機械検証の正確な範囲）

1. **P(25) の SAT 行和分割による独立確認**: 3×25・q=4 の行欠損極大 witness の
   非存在（P(25)）を、m=24 と同一の行和 63-triple 分割（row-k piece 4件 +
   row-sum piece 12件）で掃引し、**全63 triple が UNSAT で exactly-once 被覆**
   （`m25_partition_closure.py` 機械検査・decided 63 / pending 0 / uncovered 0 /
   SAT triple 0）。ただし **P(25) 自体は既に列挙閉包（three-row-q4-enumeration-20261121・
   SAT 非依存第二方法）で確定済み** であり、本 kit の新規性は
   (a) P(25) が SAT 分割・列挙閉包の **2 方法一致** になったこと（P(24) と同格）、
   (b) 重い row-sum piece を決着させる **leftmost-column 分割治具**（`split_piece.py`・後述）、
   の2点である。**m≥26 の新幅主張はしない。**
2. **較正（宣言前に実施・宣言文に開示済み）**: 陽性対照 (3,23,4) --rowY=1 --lex=H が
   **SAT 471,357 conflicts で出版値と bit-exact 再現**（CNF vars 57,742 / clauses 191,141・
   md5 `782b6104c8aa3e399a278cfc77a65be1`）。witness 8石 rows [3,2,3]
   `9:0,12:0,18:0,18:1,19:1,4:2,15:2,18:2` は sat.js verifyConfig (ok=true) +
   verify34.py (safe=1・maximal=1・deficient=1) の 2系統 PASS。
   エンコーダ決定性統制: m=25 CNF メタ (curves 7,258・plain vars 74,163 / clauses 245,245)
   は K1183 観察の出版値と一致。
3. **決定ピース台帳**（全64件・全 UNSAT・conflicts は pinned kissat 4.0.4 の
   決定論的再現対象）:
   - row-k piece (sat3・rowY×kex・行2は行0のV鏡像): (0,0) 463・(0,1) 68,642・
     (1,0) 412（lex=H,V）・(1,1) 79,086（lex=H,V）。
   - row-sum piece (sat4・rspec 完全指定・lex=H): (0,2,0) 1・(1,2,0) 0・(1,2,1) 924・
     (2,2,0) 43・(2,2,1) 2,729・(2,2,2) 15,887・(3,2,0) 106・(3,2,1) 10,402・
     (3,2,2) 173,615・(2,3,2) 205,318。V鏡像で (3,2,3)/(2,3,3) 以外の15 triple を被覆。
   - **(3,2,3) と (2,3,3) は leftmost-column 分割で決着**
     （ベース piece の一体実行は呼び出し境界で死滅・下記開示）:
     欠損行（row1 / row0）の最左石の列 c∈{0..24} で25分割
     （`split_piece.py`: ベース CNF に unit cell 制約
     cell(Y,c)=1 ∧ cell(Y,c')=0 (c'<c) を付与・全モデルがちょうど1片に所属する
     完備かつ健全な case-split）。
     - (3,2,3): 25/25 UNSAT（合計 2,468,531 conflicts・最大片 c09 211,713・
       各片 cap 40-60s 内で決着）。
     - (2,3,3): 25/25 UNSAT（合計 2,988,508 conflicts・最大片 c10 263,597）。
     - m=24 の決定打 (2,3,3) 単体 2,671,271 conflicts と比較して、m=25 の同型は
       分割合計約 299万 conflicts（約1.12倍）で全滅。
   - 全ピース合計 6,014,667 conflicts。
4. **決定性の独立確認**: 代表2件（s323_c10 = 131,390・(2,2,2) = 15,887）の
   再実行で conflicts が bit-exact 一致（per-second 表示のみ wall 依存で相違・
   rc も一致）。全64ピースの decision 行（conflicts・exit・process-time）は
   `output/raw_decisions_m25.txt` に収録。
5. **閉包の意味論**: m=24 と同一（`partition_closure.py` の m25 適応版
   `m25_partition_closure.py`）。row-k piece は「いずれかの行が石数 0/1」の全
   triple を4片で被覆（行2は行0のV鏡像）、残る {2,3}^3 ∖ {(3,3,3)} の15 triple は
   12 rspec 片（V鏡像で (3,2,0),(3,2,1),(3,2,2),(3,2,3),(2,3,0),(2,3,1) 等の
   V-image を兼ねる）で exactly-once 袆覆。**pending 0 / uncovered 0** で
   P(25) 反証空間の全滅を機械検査。

## 開示（正直な失敗・制限）

- **ベース piece (3,2,3)/(2,3,3) の一体実行は失敗**: nohup バックグラウンド実行が
  呼び出し境界で死滅（既知の環境制約・(3,2,3) は ~6 分で死亡・partial log は
  `output/disclosure_m25_s_3-2-3_partial_diedrun.out` に収録、(2,3,3) は未開始）。
  このため leftmost-column 分割に切り替えて決着させた。台帳上の位置づけは
  「row-sum piece は分割25片の全 UNSAT で反証」であり、ベース片の一体決着は不要。
- **split_piece.py 初版の CNF 結合バグ**: body 末尾の改行欠落で unit 句が直前句に
  連結され parse error（rc=1・kissat が "one clause missing" で fail-closed 検出）。
  修正後に全片を再生成・再実行して全て決着。誤生成片の実行は台帳に含めない。
- **conflicts の集計**: 分割片の conflicts 和は参考値（探索の分割により非加法的）。
  各片の UNSAT verdict 自体が加法によらず反証を与える。
- 本レーンは w=3 固定幅で標準 11×11 盤に無関係。**verdict NOT consumed・
  標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN。**

## 器材 pin（宣言文と同一）

sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`・
sat3.js md5 `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js md5 `96a84063f77bb45463ba470f05a06d58`・
verify34.py md5 `7b97ef1ac727b0741847a81d4dea9bc8`・
kissat 4.0.4 linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325`
(sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`)。
CNF 再生成用 md5 台帳: `output/cnf_manifest_m25.txt`（66 file・CNF 本体は size policy で非出版）。

## 再現コマンド

    node scripts/sat3.js 3 25 4 --rowY=0 --kex=0 --lex=H cnf/k_r0_0.cnf
    node scripts/sat4.js 3 25 4 --rspec=0:3,1:2,2:3 --lex=H cnf/s_3-2-3.cnf
    python3 scripts/split_piece.py cnf/s_3-2-3.cnf 25 1 split/s323 s323
    ./kissat-4.0.4-linux-amd64 split/s323/s323_c09.cnf
    python3 scripts/m25_partition_closure.py output/records_m25.jsonl > closure.json

## レジューム（次回・着手前に必ず最新 main 再取得・hourly 並走注意）

1. **m=26 の同一分割掃引**（P(26) の第二方法化・CNF 生成済みだが本セッションでは
   未実行）。row-k piece は m=25 比で ~1.5-2倍、分割片も同程度と見込まれる。
2. m=27 以降は分割片の時間が cap 300s に漸近するため、(c1,c2) 対分割への拡張が
   必要になる見込み。
3. **m≥32 の掃引は SAT 分割では片当たり ~30M conflicts 見込みで非現実的**
   （m=24→25 で決定打 ~1.12倍でも m=25→32 は別スケール）。K1183 の指摘どおり
   列挙閉包側（wsearch34.js の m≥32 治具拡張〔BigInt 化等〕）が本命。
4. 6x26 四レーン・6x23 sweep・seven-row w70（18:16Z 宣言 5f3fc6901）には不参入。
