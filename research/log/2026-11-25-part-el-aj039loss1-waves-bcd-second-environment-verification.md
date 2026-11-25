# Part EL waves B-D 第二環境検証 (aj039loss1 loss-only canonical adoption, 2026-11-25)

独立レーン (本 log) による Part EL 出版済み wave の第二環境検証。対象は本検証の着手時点
(HEAD `9df5a474`, 2026-11-25T14:36Z) で出版済みの **宣言 `11ac123f` → kit wave B `405dcc17`
(scripts + README stub) → wave C outputs `56bcc871` → wave D refresh fork `648ef1b0` +
reaudit outputs 3 files**。**delta extractor (wave E)・README run record・MANIFEST・完了log は
本検証時点で未出版** (mid-flight 検証・EJ inc1 型)。オーナーのローカル状態には不触、
検証は出版 bytes のみから (publish-then-execute 原則)。

## 1. clean-tree 再構成と入力 pin (全照合 OK)

tree は repo 構造どおりに再構成: EK kit 42 ファイル (commit `15ec6809` 固定 raw fetch・
MANIFEST rev2 42/42 pin OK = 本レーン先行 log
`2026-11-25-part-ek-wave-cd-second-environment-verification.md` と同じ bytes)・
EI BASE cache `merged-exact-s5-chain-plus-b39loss46-20261125.cache` (= `73482be0…`・
6,712 行・EK kit sources の byte 同一 copy)・quarantine `81d23160…`・
refresh 依存 4 ファイルを main から取得し pin 照合:
dependency-graph `54f9c364…`・repaired-joint-plan-update8 `b658290a…`・
independent.py `954d3a10…`・s5_evidence_policy.py `78655e94…` — 全て期待 pin と一致。

## 2. maker 3x byte-identical (出版 bytes から)

出版 `make_increments_el_adoption.py` (`910ede30…`) を 3 回実行: 全 rc=0・
increment `output/increment-aj039loss1-20261125.cache` (1,254 B) = sha256
`7838b081…`・manifest `output/increments-manifest.json` = `34439f4d…`
**3 回とも出版 bytes と完全 byte 同一**。
fail-closed gate 群 (EK kit MANIFEST 42 ファイル全 pin・raw two-pass
node-exact・status 7 行 pin・audit_ek SSOT pin・exh15m honest history・
fresh-increment (BASE 内 aj039 不在)・quarantine・WIN 不消費・claim-reserved 不触) が
出版 bytes の tree で全て素通りして同一出力に到達 = 出版出力が出版 bytes から機械導出
可能であることの第二環境確定。

## 3. union merger 3x byte-identical (出版 merge-audit も byte 同一)

出版 `s5_union_merge.py` (`90711961…`・EE/EI と同一 bytes) selftest PASS
(positive dedupe/sort・cross-file conflict・within-file conflict・malformed・double-run
確定性の 5 電池)。merge 3 回 (BASE + increment):
merged cache `cf08e181…` (6,713 行・WIN 158 / LOSS 6,555) **3 回とも出版 bytes と完全
byte 同一**。merge-audit `0ab05a15…` も 3 回とも出版 bytes と byte 同一。

再現細部 (honest): merger の audit JSON は CLI に渡した入力 path 文字列を記録するため、
repo-root 相対 path (オーナーの起動規約) で起動した場合に限り audit が byte 同一になる。
EL 実験dir 内相対 path で起動した場合、cache は byte 同一でも audit の `file` 2 フィールド
だけが変化する (`88c08943…`)。実測値・会計への影響なし (path 文字列のみ)。

## 4. refresh fork 再実行 (3 outputs byte 同一・会計の機械導出)

出版 `refresh_adoption_el.py` (`c0debd18…`・EI refresh `1bcf1972…` との差分確認済み
運用) を再実行: rc=0・`closure-classes.csv` `880e1c37…`・`per-root-coverage.csv`
`bafc7b66…`・`refresh-summary.json` `4579a021…` **3 ファイルとも出版 bytes と完全
byte 同一**。probe-worklist.csv (`ed289920…`) も再生成 (会計整合向け既知の
非出版対象・EI と同じ運用)。

byte 同一再生成から読み取れる会計 (解釈なし・出版 bytes と同一であることによる確定):
class 30484 `unknown_now` **6→5** (aj039 1 LOSS 行の採用分だけ減少・残 5子 =
aj030 probe-level WIN + aj049/aj050 batch-39 probe-level WIN + ai044/ai048 claim-reserved
2キー)、closure 807 行・`class_status_counts` unknown 34,497 静態・excluded 390・
`free_now` 39 (Board 39/39 verified・rejected {})・worklist_total 64,365 (EI 64,366 から
-1)・joint greedy union 36,505・unique_groups 2,115。

## 5. tamper 電池 (出版 bytes から 4/4 fail-closed・復元後 clean PASS)

- T-EL1 (aj039 p1 raw nodes 桁 -1): rc=1・`ABORT Part EK kit file sha drift:
  output/raw/aj039.p1.out`・出力は消去済み (no output)。
- T-EL2 (EK status.log へ行追加): rc=1・`Part EK kit file sha drift: output/status.log`。
- T-EL3 (BASE cache へ aj030 行注入): rc=1・`base cache (Part EI canonical) sha drift`。
- T-EL4 深層 (協調改竄): aj039 p1/p2 両 raw の nodes を同時に +1 (two-pass 整合の
  偽装) し `RAW_SHAS` pin 2 点を改竄 sha に再配線しても rc=1 fail —
  検出は 1 層手前の **kit MANIFEST ファイル pin 層** (`output/raw/aj039.p1.out` の
  MANIFEST 行)。maker は EK raw を MANIFEST listing と RAW_SHAS と内容交叉 pin
  (status/audit/LABEL_PINS) の 3 層で pin しており、RAW_SHAS だけの再配線では
  突破できない (defense-in-depth の実測)。
- 復元後 clean 再実行: rc=0・increment/manifest 出版 byte 同一 (control PASS)。
  復元後 sha: maker `910ede30`・raws `529b3efe`/`930d0b48`・status `868bfbff`・
  BASE `73482be0`。

## 6. honest near-miss (運用知見・今回 new)

初回の T-EL1/T-EL4 は sed の検索パターンに**本レーンの複製実測 wall_s (197/185) を
使ってしまい、出版 raw の wall_s (96/98) と不一致で sed が no-op** →
改竄テストが rc=0 の clean run と同一の実行になり、静黙化した。rc と「出力未作成」
の両 assert で捕捉し、正しいパターンでやり直して fail-closed を確認した。
**教訓: tamper 電池は改竄側ファイルの sha が実際に変化したことを先に assert して
から gate を走らせること** (改竄未適用の tamper test は黙って PASS を返す = 偽陰性)。
EK の出版 MANIFEST 手書き転写ミス (3 件) と合わせ、*pins と sed パターンは期待値を
写すのでなく対象 bytes から採番する*原則の重要性が 2 回続けて実証された。

## 7. 結論と UNKNOWN 担保

- Part EL waves B-D の全出版 bytes (maker・merger・refresh・outputs) が第二環境で
  完全再現、**不整合ゼロ**。class 30484 unknown の 5 減少 (6→5) と worklist -1
  (64,366→64,365) は byte 同一再生成による機械確定 (delta extractor が出版され
  次第、その deltas との交叉確認が次回の追加検証になる)。
- **verdictは不消費。** aj030 probe-level WIN (scrutiny-owner C++ gate 専権)・
  aj049/aj050 batch-39 WIN・ai044/ai048 claim-reserved (Part EF) はこの Part の
  前後を通じて不採用のまま。
- **標準 11×11 空盤・19 central-reply roots・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・30484 (残 5子含む) は本検証の前後を通じてすべて UNKNOWN のまま。**
  nodes は bookkeeping・勝敗・被覆・secured coverage の主張は本 log のどこにもない。

## 8. レジューム (着手前に必ず最新 main 再取得・hourly 並走注意)

- Part EL の残 wave (delta extractor (EI 型 fork)・README run record・MANIFEST・
  完了log) が出版されたら、本 log の再現工程 (maker 3x → merger 3x → refresh →
  byte 照合) に extractor 再実行 (出版 bytes から PASS + decomp byte 同一) を加えた
  完結版の第二環境検証が次候補 (所要 ~5 分)。
- Part EF (ai044/ai048) は所有権侵害回避で不触のまま。EJ inc2+ は未出版
  (最新 main で確認済み)。
- 次の fresh-class batch probe 候補 (本 Part では probe しない): 完了log出版後の
  refresh 再選定待ち。
