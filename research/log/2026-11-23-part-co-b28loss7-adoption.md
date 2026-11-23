# Part CO 完了log: batch-28 (class 5343) 7-LOSS行 adoption — publish-then-execute 全ステップ完了

- 2026-11-23T20:3xZ 完了。単一オーナー: Vibe長期レーン（Part CO）。
- 宣言: `research/log/2026-11-23-n11-centralreply-class5343-b28loss7-adoption-single-owner-note.md`
  （commit `0ba87be4`、末尾スペースを含む我々の宣言本文の文字化け修正 commit `36827f18`、
  修正版全文sha256 `8eb84ad4890cdd7a2e1d68b6d94167577b1de0f069872f3f83bb4f849cc98d75`・
  fetch-back完全一致）。

## 採用内容（verdict不消費・11×11はUNKNOWN）

- **ADOPTED-CANONICAL 確定**: Part CH正準BASE cache（6,294行・`3124461b…`）＋
  batch-28 の7新規LOSS行（aa015/aa017/aa018/aa023/aa024/aa029/aa036・
  s5 164462/170101/173654/193820/196053/199714/199721・nodes合計 38,784,669/pass）を
  pinned byte-clone union merger（`90711961…`）で統合。
  新 正準 cache: **6,301行（WIN 158 / LOSS 6,143）**・
  `research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache`
  sha256 `854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d`。
- aa003はPart CH採用済み・非再送（makerのBASE一貫ゲートで (2, 4,070,373)≡raw を機械確認）。
- WIN 35行は不採用かつ未消費（scrutiny owner C++ pin `9193f5b6…` 専権・非接触。
  aa006/aa007のPart CG laneは非接触のまま）。EXHAUSTED 11行は honest UNKNOWN。
- **class 5343 は解放されず**: 残46 unknown = 35 WIN + 11 EXHAUSTED のs5集合と
  完全一致を機械ゲートで確認。closure表: unknown 53→46・rank 19→4・
  表807→808行・left={12697}・entered={5233, 5374}（holder起因の純粋再構成）。
  flip 0・新規free 0・free_now 38不変。

## 公式実行（宣言D1-D5・全て宣言ノートの事前登録数値と一致）

- D1 maker ×4 byte-stable（increment `bd5ef7d7…`・manifest `b47e07ca…`）。
- D2 merger selftest PASS・merge ×3 byte-identical・merge-audit 3通とも `06f25f00…`。
- D3 refresh ×3 byte-identical ＋ 隔離実行（env -i・別tree・PYTHONHASHSEED=random）
  byte一致: summary `4727fb2b…`・closure `9d3965d9…`・PRC `8e6fb981…`。
  （非出版 probe-worklist `1691027d…`。）
- D4 extractor ×4 byte-identical ＋ 隔離実行: decomp-deltas json `39b2802d…`。
  holder算術（union 21・5343 own=7・他20クラスown=1）・update8 新規residual
  ちょうど7・metrics pin・anchors pin・churn 431（428 unknown + 3 excluded_now・
  再計算状態不変）すべて緑。
- D5 tamper battery 15種すべてfail-closed捕捉（0見逃し）＋復帰green ×2:
  - pin層: increment改変・BASE改変・BASE append・raw verdict flip・
    kit MANIFEST内repin・batch-keys class改変・scenario cache改変
    → 各sha pin層で捕捉。
  - attacker-repin semantic層: forged 8-row increment（WIN混入）+ extractor
    cache pin repin → manifest loss sha交差ゲート。BASE append + FULL repin
    （extractor）→ manifest BASE-cache意味ゲート。BASE append + FULL repin
    （maker）→ 6,295≠6,294行構造ゲート。class flip + keys/両kit MANIFEST FULL
    repin → drive-4 row-audit header drift 交差ゲート。manifest意味改変 → BASE-cache
    bookkeepingゲート。status junk除去+status pin repin → kit MANIFEST pin層。
  - **実験事実として記録**: battery演者（Vibe）がpin転写を手打ちした結果、
    round1のrepin指定3件が黙Failした（`9ebfdcc`→`9ebdfd0c` 型転写）。いずれも
    原本pin層が改変を捕捉したため battery自体の結論は不変だが、
    「pin転写は必ず機械経由」の規約を演者自身が再検証した形となった。
    round2で正規表現機械repinに全面的に切り替え、FULL-repin 3種で
    semantic層のみで捕捉されることを独立確認した。

## 出版（各push後にfetch-back sha256照合・全部数一致）

- A `f2ab210d`: scripts 4（maker `cef735cc…`・merger `90711961…`・
  refresh `03cb1de9…`・extractor `67b2b3c5…`）。機械転写（sandbox file_system
  read + sha gate + push_files）・fetch-back 4/4。
- B `071f3d8a`: increment・manifest・merge-audit×3 → fetch-back 5/5。
- C `4d48d6a2`: merged cache 259,886B → fetch-back一致。
- D `ef0f34a7`: reaudit outputs 3件 + decomp-deltas json → fetch-back 4/4。
- E `f6716a28`: README + MANIFEST-sha256（15ファイル pinned incl. README）。
  → MANIFEST recorded 15/15 fetch-back一致・MANIFEST自体もbyte一致。
- 実験dir: `research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/`。
  probe-worklist.csv は宣言どおり非出版。

## 周辺観察（非接触・簡潔に）

- Part CG takeover（aa006/aa007 third-impl・宣言 `d5e9acc2` 18:01Z）は
  本Part完了時点でも outputs出版なし（停滞継続）。aa006/aa007 のWIN 2行は
  引き続き unconsumed。
- batch-29 / class 2251（Part CI・scaffold `c6ae987a`）も outputs停滞継続。
- 上記2件は本Partの入力・証明書に非接触。次回以降の優先度判断に回す。

## UNKNOWN guarantee（再掲）

標準11×11空盤・19 central-reply roots・二石roots {49,60}/{59,60}・S2 {59,60}・
classes 1/2/4/10968/23964/5343（aa001..aa054全キー含む）は**すべてUNKNOWNのまま**。
nodes数はbookkeepingであり決してverdictではない。本Partはいかなる
root-coverage/closure/secured/root-outcome主張も行わない。verdictは不消費。
