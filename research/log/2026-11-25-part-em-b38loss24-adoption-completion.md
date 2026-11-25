# Part EM 完了: b38loss24 (Part EF batch-38 の fresh exact-LOSS 24行) loss-only canonical adoption + reaudit 完了 (2026-11-25)

単一オーナー Part EM・publish-then-execute。Part EF batch-38 kit
(class 30345 target・49キー全て first-ever probe・two-pass fresh-cold
node-exact @15M/order 0・MISMATCH 0) の産物のうち、**fresh exact-LOSS
24行** (ai001,004,008,009,011,012,015,016,018,019,020,021,022,025,026,
027,029,031,032,033,037,042,044,045・採用 node 合計/pass 168,055,078)
のみを canonical exact-S5 chain cache に採用し、reaudit (refresh +
delta extractor) まで完了した。 **ai044 (class 30484 dual-class child)
を含む**点が本 Part の構造的要点である。

| wave | 内容 | commit |
|---|---|---|
| A | 対抗宣言走査クリーン確定後の単一オーナー宣言 `research/log/2026-11-25-part-em-b38loss24-adoption-declaration.md` (Part EF 完了logの resume note (b) として登録済みの採用) | `4e3185b7` |
| B | kit: maker `c787472a…` (EL-maker fork・EF 181-file kit 全検証・49キー pin は kit SSOT から機械再生成・fail-closed) + pinned union merger byte-clone `90711961…`。maker 3x byte-identical・tamper T-EM1/2/3 rc=1・復旧 byte-identical | `98b4bfb7` |
| C1 | merged chain head `b5be64e6…` **6,737行 WIN 158 / LOSS 6,579** (宣言どおり) | `ff2a3836` |
| C2 | increment `3c632661…` (2,638B・24行) / manifest `ac5649f8…` (schema em-b38loss24-increments-manifest-v1) / merge-audit ×3 同一 sha `4a877e17…`。merger 3x byte-identical | `3c174ef2` |
| D | refresh fork `baf9cbde…` (EL refresh `c0debd18…` の 3箇所変更: docstring/CACHE path/sha pin)。publish-then-execute・3回 byte-identical (~62s/回・4 output 全て)。outputs: refresh-summary `bacf6a68…` / closure-classes `93a68897…` / per-root-coverage `bce9f8f1…` (probe-worklist.csv 3,719,664B は不出版・regen pin `b4d16b7f…`) | `c56cb936` / `c7b24ce4` |
| E | delta extractor `compare_deltas_em_adoption.py` `2d6ae570…` + 機械 decomp `cd8bbf89…`。2x byte-identical・tamper T-EM4/5/6 (scenario cache / manifest / closure-classes 1バイト改変) 全て rc=1 fail-closed・復旧 byte-identical・clean control PASS | `2c03af4e` |
| F | README.md run record 確定 + MANIFEST-sha256.txt (14 entries) + 本完了log | (本 commit) |

## 出版経路の正直な記録

- 本セッションは compaction ハンドオフ (Part EM wave C2 完了時点) から
  再開した。ハンドオフに記載の実測値 (merged head `b5be64e6…`・
  increment `3c632661…`・manifest `ac5649f8…`・audit `4a877e17…`) は
  すべて本セッションで出版バイト fetch-back 再照合のうえ使用した
  (ハンドオフメモを鵜呑みにせず SSOT から再確認)。
- wave D の refresh fork 作成時にローカル dry-run (rc=0, 61s) で動作確認
  后に出版し、出版バイト fetch-back → 3x 実行 byte-identical の順で
  実施した (publish-then-execute; dry-run は何も消費しない read-only
  planning 計算であるため出版前に許容)。
- wave E の extractor は EL extractor の設計をなぞりつつ、本 Part の
  教訓 (MANIFEST 転写事故) を反映し **48個の adopted raw sha ピンを
  手書きせず manifest `kit_integrity.raw_file_sha256_pins` (SSOT,
  sha pin 済み) から参照**する構成にした。開発中の fail-closed
  検出 3件 (EF kit MANIFEST が `<sha> <size> <path>` 3-field 形式で
  2-field parse されて失敗 / truncation 集計 key の所在誤り /
  pool ID が `ef-b38loss24`) はいずれも fail-closed 側で捕捉・修正し、
  最終版 2x byte-identical + tamper battery 全 FAIL 確認済み。
- 並走 (hourly) lane が `de7b3065`/`5a3c17f4` (K1325 z=17 slice・
  別dir) を出版した時点で HEAD が動いたため、wave E push 前に sweep
  を再実行し衝突なしを確認してから出版した (経路分離・競合なし)。

## 採用結果 (honest label・verdict は 24 LOSS行のみを消費)

- merged canonical
  `output/merged-exact-s5-chain-plus-b38loss24-20261125.cache`
  (281,016B) sha256 `b5be64e6…` = **BASE (Part EL `cf08e181…` 6,713行
  ・WIN 158 / LOSS 6,555) + fresh 24行 = 6,737行・WIN 158 / LOSS
  6,579** (3回 merge 同一 bytes・merge-audit ×3 同一 sha・quarantine
  hits 0・BASE 重複 0)。
- **不消費の明示** (extractor で key 単位に NO-cache を機械検証):
  (1) batch-38 の 19 probe-level WIN行 (ai048 含む・WIN 採用は
  scrutiny-owner C++ 第二実装 gate pin `9193f5b6…` 専権)・(2) 6
  honest-EXHAUSTED キー (ai007/ai024/ai030/ai038/ai040/ai041・15M
  同一条件再probe 禁止のまま)・(3) b018 (prior batch-1 dual-class
  WIN・除外継続)・(4) aj030/aj049/aj050 (batch-39/EK probe-level
  WIN)。
- 採用 24行は全て first-ever probe (published prior-probe universe
  `6deee846…` 2,104 pair に不在・two-pass fresh-cold node-exact
  @15M/order 0・同一 pass 内で解決)。

## reaudit 機械導出の確定値 (extractor fail-closed 検証・全 byte 再現)

- **class 30345** (batch-38 target): unknown **50→26**・rank
  **13→11**・groups_served 4 static・**NOT freed・NOT excluded**。
  51-child Board 境界 (non-s5 child 1・in-universe 50子は BASE で
  全て unknown) を独立 integer-geometry で再生成し、24採用行全てが
  境界内側であることを機械検証。
- **class 30484** (EL/EM dual-class owner): unknown **5→4**・rank
  7→7・groups_served 4 static・**NOT freed・NOT excluded**。採用 ai044
  (s5 900354) が境界内側の唯一の採用行。残 4子はすべて不消費
  probe-level WIN: {892576 aj030, 900718 ai048, 902511 aj049,
  902512 aj050}。**この段階で class 30484 の残りは WIN 採用
  (C++ gate 専権) を残すのみ**となった。
- **class 30118** (Part EJ batch-40 の in-flight target): unknown
  **52→51**・rank **21→17**。採用 ai033 1行が 56-child 境界内側。
  EJ owner lane は本 Part では一切触れていないが、**EJ の baseline
  (prior-probe universe・worklist) が本出版で動いたため EJ は再開時に
  必ずこの cache head `b5be64e6…` から re-baseline すること**。
- witnesses 16371/20421/34908: byte-static。closure表 807行両側・
  left/entered 空・groups_served churn 0・rank-churn-only 6行 (1518/
  2634/5343/8106/8785/13342)・fully stable 798行・上記 3 class 以外の
  unknown_now 変更は Board own-membership 検証で 0。
- update8: 完全 byte-static (resolved 259 / remaining 31,600 /
  groups_free_now 131・newly_resolved []・win_hit_groups [])。
  採用 24 s5 index はすべて凍結 baseline requirement の外側。
- class_status: {excluded 390, excluded_now 23, free_now 39,
  unknown 34,497} 完全 static (Board 検証 39/39・reject 0 両側)。
- metrics (bookkeeping・決して verdict ではない): joint greedy
  36,505→36,460・unique_groups 2,115 static・worklist 64,365→64,339・
  known_universe 892→916・cache_in_universe 869→893・
  **free/uncovered は全 19 root で完全同一 (= 何も free 化していない)**
  ・individual greedy 再選択のみ 6 root (0: 3001→3000, 1: 6352→6351,
  2: 6129→6134, 12: 2890→2866, 24: 2781→2780, 36: 2997→2975)・
  root27 119/119。
- extractor は毎回 BASE (EL) refresh `c0debd18…` と SCEN (EM) refresh
  `baf9cbde…` の両 fork を scratch で実行し 8 output 全てを出版 pin と
  byte-identical で gate (EM reaudit outputs が出版バイトのみから
  誰でも再生成可能なことの機械保証)。さらに EF kit 181 file の
  sha+size 検証・49キー全 two-pass raw 再検証 (batch-keys SSOT
  `29807104…`・manifest 分解表と突合・7 truncation retry 産物が
  audit 上唯一の非完全 raw であることも検証) を行う。
- 実行コスト実測: refresh fork 1回 ~61s・extractor 1回 ~123s (2
  refresh 再実行込み)・いずれも単一 bash foreground (300s 上限内)。

## 解釈ガード

- 採用 24行は全て fresh (BASE 不在・quarantine 不在・first-ever)・
  two-pass fresh-cold node-exact @15M の honest label のみ
- probe-level WIN行 (batch-38 の 19行 incl. ai048・aj030・aj049・aj050)
  は本 Part では 1行も消費しない (いずれも NO cache・extractor が
  key 単位で機械検証)。EXHAUSTED 6キーは honest UNKNOWN のまま
- loss-only adoption は class を free化も excluded化もしない
  (closure 表・class_status の機械導出で確定)
- nodes は bookkeeping・pn/dn ではない・solved数は勝敗ではない
- **11×11 空盤は UNKNOWN のまま。root verdict・coverage claim は
  本dir のどこにも無い**

## 次の実行可能選択肢 (resume notes)

1. **C++ scrutiny gate `9193f5b6…` (最重要・本環境では実行不能)**:
   batch-38 の 19 probe-level WIN行 (incl. **ai048**・class 30484 の
   残 4子のうち 1つ) の WIN canonical adoption は C++ 第二実装 gate
   の専権。g++ が使える環境の提供が現時点でこのレーンへの最大の
   外部貢献である。ai048 WIN が採用されれば class 30484 は
   excluded (WIN が cost child) または boundary win 扱いとなり、
   EL/EM を通じた loss-only 積み上げと合流する。
2. **class 30484 の残 4子は全て不消費 probe-level WIN**
   (aj030/ai048/aj049/aj050)。この class を閉じる正規ルートは WIN
   採用のみであり、本レーン (loss-only) からは何もできない。
   次の loss-only 積み上げは class 30345 残 26 unknown の probe
   (batch-41 候補) とするのが計算量的に最適 (rank 11・unknown 26)。
3. **Part EJ (batch-40・class 30118)** は original owner のまま
   in-flight。stall 13:01Z から 3.5h 超過で takeover 可否を毎回
   確認する規定は継続。ただし本出版で unknown 52→51・rank 21→17
   に動いているため、EJ 再開時は cache head `b5be64e6…` からの
   re-baseline が必須。
4. **second-environment 検証**: Part EM の waves B-E は本 (単一)
   環境でのみ検証済み。EL で実績のある並走 lane による独立環境
   検証 (maker/merger/refresh/extractor の新規 clone からの
   byte-identical 再現 + tamper battery) が望ましい。
5. 11×11 空盤は UNKNOWN。canonical cache 6,737行 ( WIN 158 / LOSS
   6,579) の時点でも、19 central-reply root は free_now 39 /
   unknown 34,497 のまま全て UNKNOWN。
