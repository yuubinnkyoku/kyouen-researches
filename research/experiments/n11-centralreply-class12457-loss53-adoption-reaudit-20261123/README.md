# n11 central-reply batch-20 (class 12457) 53-LOSS canonical adoption reaudit (Part BI, 2026-11-23)

単一オーナーとして本hostが実行した、batch-20 (class 12457) の53 LOSS行
(x001..x053) をcanonical exact-S5 verdict cacheへ計上する採用・再監査実験
(Part BI declaration = note Part BI amendment `879e898c`)。

Part BG (batch-20完走: 53/53 two-pass node-exact、53 honest label result=2
(LOSS)、WIN 0・枯損 0・不一致 0・総ノード175,842,846/pass×2-pass・
14 truncated断片はfresh-cold再実行・row-audit
`1dcb7fb8`・出版 A `358cac13` / B `564cc66a` / C `928546df`) の必須次工程
(「53 LOSS行の採用は別宣言adoption Partがpinned fail-closed mergerで実行」)
を履行する。batch-20にWIN行・枯損行は1行も存在しないため (「不在のgate」と
して機械検証)、採用パケットは完全解決パケットと一致する (full == loss・
機械主張)。すべて機械表明・機械検査:

1. **publish-then-execute順序** (宣言どおり): 計算機材4 scriptを先に
   mainへ出版 (commit `7bdf327a`): maker `scripts/make_increments_batch20.py`
   (sha256 `81a6b7ec…`) / delta extractor
   `scripts/compare_deltas_batch20_adoption.py` (sha256 `605e040a…`) /
   sha-pinned fail-closed union merger `scripts/s5_union_merge.py`
   (byte-copy pin, sha256 `90711961…`) / refresh
   `reaudit/scripts/refresh_adoption_12457.py` (sha256 `2f77a8bb…`)。
   出版bytesをcommit-pinned raw fetchで本hostに取得しsha照合の上、
   4段階すべてを出版後に再実行した (出版前にも同一hostで同一機材の
   通し実行・byte一致を確認済みのため、二重実行・両方byte一致)。
2. increments maker: 全fail-closed gate PASS。53行の2-pass raw独立再検証
   (p1==p2 node-exact・`# replay_done`・budget 15M・status.log 53 PASS行
   each-once・最終行 x053 PASS 15000000,2,6402333・合計ノード
   175,842,846/pass両pass一致)・batch-keys (sha256 `efb40b1b…`) の
   legal/(lo,hi)照合・row-audit (`1dcb7fb8`) 一致・WIN行不在absence gate・
   枯損行不在absence gate・14 truncated断片はverdict行なし・BASE cache
   6,182行 (`0b594f7e…`) に53キー不在 (overlap 0)・quarantine 0・kit
   191/191 MANIFEST (`d0ef293b`) 再検証。increment 53行 (sha256
   `554f726129cce48b09fcbc5edaf4b40fb6dd4332182e4c62594455c47bc0a163`,
   manifest sha256 `82a5f866…`) を出版。実行2+1回・byte一致。
3. sha-pinned fail-closed union merger (byte-copy pin `90711961…`,
   selftest PASS) でBASE canonical 6,182行 (`0b594f7e…`, Part BC採用正本)
   にincrement 53行をmergeし、**canonical exact-S5 verdict cache 6,235行**
   (WIN 158 / LOSS 6,077・conflict 0・duplicates 0、sha256
   `f6649fe36425f9a4e959b058392746b73e655cda0fcfa223befafd8905d67d26`,
   256,885 bytes) を新path
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-20261123.cache`
   に出版 (本repoの次のcanonical exact-S5 verdict cache)。merge 3回実行・
   byte一致・merge-audit 3回byte一致 (run1=run2=run3, sha256
   `06151e6d…`)。merge後のBASE 6,182行cacheはbyte不変を再検証。
   出版後再実行でもmerge出力はbyte一致、そのaudit (`merge-audit-postpub.json`
   sha256 `d748bbbf…`) は記録される入力path文字列 (絶対/相対) 以外は
   run1と完全一致 (両入力sha・行数・verdict計数・出力sha同一)。
4. Part BC refresh機のadapt `reaudit/scripts/refresh_adoption_12457.py`
   (sha256 `2f77a8bb…`) によりrefresh再監査 (~60s) を実行。
   4出力とも出版前後の実行間でbyte一致: refresh-summary (sha256
   `d9d18fc2…`)・closure-classes (sha256 `d57a7609…`, 807行)・
   per-root-coverage (sha256 `bc409e63…`)・probe-worklist (3.75MB,
   sha256 `3152855d…`。Part AH/AO/AP/AS/AV/BC先例どおり**不出版・
   sha記録のみ**)。
5. delta extractor `scripts/compare_deltas_batch20_adoption.py`
   (sha256 `605e040a…`) 全gate PASS・3回+出版後1回実行・byte一致
   (`output/decomp-deltas-batch20-adoption.json` sha256
   `3107866959fa13b332776a04bf3abe42e97c8881b0b8cc179d009b80a93f05eb`)。
   flips=[]・new_free=[12457]厳密一致・class 12457のBASE-unknown 53子は
   batch-20 key集合と全行一致で解決・holder classのunknown_now減少は
   自身のmembership分のみ・closure候補表の退出は[12457]のみ (進入は空)。
   11個のsha pin gate全PASS (increment・scenario cache・BASE cache・
   BASE summary・scenario summary・BASE closure・BASE prc・scenario closure・
   scenario prc・batch-keys・row-audit)。
6. tamper battery 10種 (出版前に実施): increment verdict flip / raw行
   改変 (orderフィールド) / manifest WIN注入 / refresh-summary差し替え /
   batch-keys差し替え (合法改変にもsha gateで検出) / scenario cache
   verdict flip / merger cross-file WIN-LOSS conflict (出力拒否rc=1) /
   status.log最終行改変 / kit MANIFEST gate / extractor sha pin。
   10/10検出・検出後復元byte一致を再検証。

## 結果: class 12457はBoard検証free class 38番目としてunknown人口から退出 (分類delta・機械確定)

- 機械確定 (refresh再実行・extractor全gate PASS・decomp-deltas json):
  class 12457の費用子54個すべてがcanonical上LOSS (既知子 {126899: LOSS}
  + 採用53行) かつBoard fail-closed子境界検証PASS。class 12457は
  **free_now 37→38** (38番目のBoard検証free class) としてunknown人口から
  退出。class数は**unknown 34,499→34,498**・closure候補表は**808→807**
  (rank 17 class 12457の退出のみ・進入は空・closure gate)。root 27
  (known-loss-baseline) は**119/119不変**。class 23101は両表
  unknown_now 1のまま・class 12643はunknown 53のまま (**rank 18→17に
  繰り上げ**、次のroute-alive closure候補)。
- update8 (簿記): remaining 31,779→**31,726**・resolved 80→**133**・
  joint greedy 38,978→**38,415**・probe worklist 64,872→**64,808**。
  nodes数・worklist数・greedy数を勝敗として読まない。
- verdict不消費 (WIN側不変): 消費は53 LOSS行のみ (fail-closed merger
  経由)。batch-20にWIN行は存在しない (absence gate) のでWIN採用場面は
  ない。19 unconsumed closure WIN候補 (b018/d002/e002/f017/g018/j033/
  h045/z003/n005/n006/p002/p003/r001/r002/q042/v001/v002/w001 (s5 63802)/
  w002 (s5 109169)) は読み書きとも全く不接触。採用判断はscrutiny owner
  C++第二実装 gate pin `9193f5b6…`のまま。
- 誠実な修正記録: outputs commit `04a2335e`のmessageはworklistを
  「直後の別commitで出版」と予告していたが、repo慣例 (Part AH/AO/AP/
  AS/AV/BCの3.7MB probe-worklist不出版・sha記録のみ) に従い不出版と
  した。sha `3152855d…` は本READMEとnoteに記録した (実験dirの
  mirror上のファイルは出版対象外)。
- 並走との不接触: Part BH (batch-19 residual w003..w053・宣言
  `de1383a7`・別オーナー) の採用コミットはmainにまだ無い・本Partは
  非接触。batch-21 (class 12643・将来の別宣言) にも着手していない。
  scripts出版commit後のfast-lane 2コミット (`22dc3dd2`, `ecc96264`)・
  K1058系・sixth-cost系は読み書きとも非接触。
- 標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 12643は本Partのどの時点でも
  **UNKNOWNのまま**。
