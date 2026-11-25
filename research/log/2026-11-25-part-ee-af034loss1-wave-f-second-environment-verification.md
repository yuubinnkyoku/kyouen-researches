# Part EE wave F 第二実行環境検証 (published bytes から全再構成・出版 extractor 再実行) (2026-11-25)

単一オーナー Part EE wave F の出版 set (commit `dcdd86c1` + docs
`10fbf47e`・addendum `d19b5ca`) を、**別サンドボックス実行 (b)**
から独立に全件検証した記録。本実行は wave F data push を別実行 (a)
に譲り (push 競合ゼロ)、検証に転じた。標準 11×11 空盤は
**UNKNOWN のまま**。

## 検証手順 (全て main published bytes からの取得のみ・ローカル遺物不使用)

1. raw fetch (main): wave F 6 files + README + MANIFEST rev2 取得。
   sha256 実測: refresh fork `01937f23…`・extractor `7660b441…`・
   refresh-summary `6af660a1…`・closure-classes `27e00b0d…`・
   per-root-coverage `6974299b…`・decomp `614bbda0…`。全て
   MANIFEST rev2 pin と一致 (6/6)。git blob sha1 再計算 8/8 が
   get_file_contents 返却 SHA と一致 (fork `12e92dfe`・summary
   `7503a560`・closure `502bb25d`・prc `5b0df4e4`・decomp
   `d0efc1e1`・extractor `a9e8a299`・README `ebbe6a24`・MANIFEST
   `79ec12d0`)。core 8 件の pin も復旧済み bytes (実行 (b) の
   getraw 復旧時の全 sha 照合済みコピー) と一致。
2. EA kit (61 files・MANIFEST `42ba81bc…`) を main から再取得:
   **61/61 sha 一致・0 fail** (ED kit 36 files・graph・update8
   policy も同時に pin 一致を再確認)。
3. **出版 extractor `7660b441…` をそのまま実行** (実測 1m59s):
   PASS (`DECOMP OK changed=0 rank_churn=1 gs_dec=0 stable=805
   left=0 entered=0`・class34908 unknown 7→6 NOT freed rank 8→7・
   16371 byte-static・20421 rank churn only・update8 byte-static)。
   scratch 隔離 tree で EC refresh `73186e63…` と EE fork
   `01937f23…` を再実行して両 output byte 同一を確認 (extractor
   内部 gate)。**decomp 書き出しが published bytes `614bbda0…`
   と完全 byte 一致**。非出版 worklist regen pin `b4933810…` も
   本環境で再生した probe-worklist と一致。

## 環境リセット復旧の実験事実 (「ローカルだけの証拠を残さない」原則の実証)

実行 (b) のサンドボックスは wave F extractor 実行中に環境リセット
し工作 dir を全喪失した。復旧は **repo published bytes + sha pin
のみ**で完結した: core 25 files + ED kit 36 files を curl raw 取得
し全 pin 一致、EC refresh fork (`73186e63…`) からの EE fork 再生成
(CACHE path 行 + CACHE_SHA pin のみ差し替え → sha256
`607f1f1f…` が pre-wipe pin と byte 一致)、refresh 再実行で 4 output
byte 再生 (summary `6af660a1…`・closure `27e00b0d…`・prc
`6974299b…`・worklist regen `b4933810…`)。この lineage ((b)-内製
extractor `a5abb50a…` も含む) は出版されなかったが、**測定値は出版
lineage と完全一致** (二重系統相互検証): class 34908 base-known LOSS
子 49→50 (56子 100% s5)・unknown 7→6・rank 8→7・closure 807行
(fully stable 805・churn 1 のみ 20421)・update8 resolved 259 /
remaining 31,600 static・joint greedy 36,509→36,508・worklist
64,415→64,414・universe 844→845・in-universe 821→822。

なお compaction 控えの「class 34908 known 47→48」は EC 自身の
BASE→SCEN ペアの誤記録であった。実行 (b) の extractor は
fail-closed `ABORT class-34908 BASE-known child count 49 != 47`
で即捕捉し、49→50 に修正のうえ PASS した (出版 lineage も同値を
機器導出・fail-closed 設計が pins の転記ミスを限定工程で捕捉する
ことを示す実例)。

## 結論

- wave F の機器導出 (class 34908 unknown 7→6・NOT freed・rank 8→7・
  closure/update8 byte-static) は **2 系統の独立実行 + 出版 bytes
  からの第三環境再実行** で同一確定。af034 60M 解決行は canonical
  cache に消費済み・以後同キーの再 probe 不要。
- 独立検証可能性は「published bytes + pin だけで誰でも全再構成・
  再実行できる」ことが実証された。実行 (b) のリセットで失ったのは
  時間のみで、証拠は一切失われていない。
- 解釈ガード: **11×11 空盤・19 central-reply root・二石root・S2・
  class 1/2/4・16371/20421/34908 は全て UNKNOWN。** 本 log は検証
  記録のみで verdict・coverage 主張は無い。nodes・greedy・worklist
  は bookkeeping。
