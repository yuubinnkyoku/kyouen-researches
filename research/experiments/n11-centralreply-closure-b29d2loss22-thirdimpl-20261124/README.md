# batch-29 (closure class 2251) Part CI takeover drive-2 ckpt-3/3 LOSS 22行 (ab033..ab054) 第三実装交叉検証 — Part DC (2026-11-24)

Part DC (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-dc-b29d2loss22-thirdimpl-declaration.md`・commit
`262a631e`・observed HEAD `d2d60645`)。Part CI takeover drive-2
(batch-29 全54キー probe-complete・完了log commit `141cf80c`) で **15M
fresh-cold 2-pass条件で解決した drive-2 ckpt-3/3 LOSS 22行 (ab033..ab054)**
に対する pinned第三実装 (非df-pn AND/ORミニマックス `third_impl.js`
`08ea958f…`) による verdict-level 交叉検証 + 本host pinned-replica
(`jsreplay.js` `84585617…`) 2-pass fresh-cold再現 (`run_replica_dc.sh`
`8ddf1ef4…`・budget 15M) + **Part CU出版物** (canonical merged cache
CU snapshot 6,317行 `30ddad9d…`) に対する unadopted補強機械gate (G6) +
**Part DB出版物** (37-LOSS adoption・increment `85bd4469…` 37行・
post-adoption canonical merged cache `04b0a239…` 6,354行) に対する
canonical事後補強機械gate (**G6b・本Part追加設計**)。

**verdict不消費**: 本Partはいかなるadoption・解放・閉鎖も行わない
(読みのみ)。22行のLOSSはhonest labelであり、canonical chainへの採用は
宣言時点で Part DB (`10a79660`・2026-11-24T02:40:07Z完了) が実施済み
(本PartのG6bはその出版物とのbyte照合であり新しいverdict主張ではない)。
WIN行 ab028 の採用は引き続き scrutiny owner C++第二実装 gate
`9193f5b6…` 経由。閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11空盤・central-reply roots・class 2251・全キー (batch-29
54キーを含む) は UNKNOWNのまま**。nodes数・expansions数を勝敗として
読まない。

## 実行結果サマリ (D1-D7 全green)

- **D1 rules gate** (`verify_tbl.js` `c8c52528…`): replica quads 95670 ==
  mine quads 95670・triples checked 195044 mismatches 0
  (`output/rules-gate.txt`)。
- **D2 val-gate fresh 4** (`.dc-host.out`): 4/4 published baseline node-exact
  (2M×2 result 0 / 15M×2 result 2 nodes 3,651,923・5,040,200)。
- **D3 negatives**: ng1 (legal 88 declared vs 87 derived)・ng2 (stones 6
  declared vs 5 bits) とも **GATE_FAIL設計どおり** fail-closed。
- **D4 anchors**: k02a WIN expansions 9,106,337・ttHits 4,991,527 /
  l1a LOSS expansions 7,660,602・ttHits 3,951,175 — published値と
  node-exact・a/b det-pair一致。
- **D5 pinned-replica 22キー×p1/p2** (budget 15M fresh-cold): 全22キー
  (result 2, published nodes) と **node-exact** (合計 95,516,023
  nodes/pass・2-pass合計 191,032,046 nodes再実行)・p1==p2 determinism
  (wall_sを除く全field一致)。
- **D6 第三実装 22キー×a/b** (cap 300M・wallcap 240): **22/22 verdict = 2
  (LOSS)** で df-pn (batch-29 solver) / pinned replica / third impl の
  **three-implementation corroboration 成立**。全run clean・det-pair一致
  (expansions/ttHits完全一致)・WALL-INCONCLUSIVE 0件・pass-one
  expansions合計 109,838,511。**nodes数を勝敗としては読まない**
  (verdict-level一致のみが主張)。
- **D7 audit** (`audit_dc.py` `e60630ac…`) **×3 byte-identical** (stdout
  32hex `78d9e4956d81da5b…`): **ALL 652 GATES PASS**・verdict agreements
  22/22 (WIN=0 LOSS=22)・inconclusive 0 (`output/audit-run1/2/3.txt`・
  `output/audit-summary.json`)。G6 (CU snapshot: 22行row不在・fileless
  roster在籍) と G6b (DB increment 37行・DB merged 6,354行のpin + 22
  target行のbyte一意存在 44 gate) とも全PASS。

## run record (実時間 UTC)

- 宣言 push `262a631e` 02:49:21Z → A1 scaffold `533a93bd` 02:50:50 →
  A2 sources `b3e20e53` 02:51:18 → A3 raw/val-gate `5cf0d233` 02:51:38
  (各push後に fetch-back byte全検証: 計122ファイル完全一致)。
- D1-D2 02:52-02:53 → D3 02:53 → D4 02:53-02:55。**incident-1**: 02:55-03:00
  D5 wave実行中に実行環境リセット発生 (下記「incident」節) → published
  kitから再取得し D1-D7を最初から再実行: D1-D2 03:07-03:08 → D3+D4
  03:08-03:09 → D5 wave ×6 03:10-03:27 (22キー完全) → D6 wave ×6
  03:27-03:40 (22キー×a/b完全) → D7 ×3 03:40。
- B1 `9ca01707` 03:40:57 → B2 `04d4b890` (初回pushは並走pushとの
  競合 "Reference cannot be updated"・即時再試行で成功) → B3 `d37eaaad`
  → C (本README + MANIFEST-sha256) → fetch-back byte全検証 104/104。
- 完了log科学研究: `research/log/2026-11-24-part-dc-b29d2loss22-thirdimpl-completion.md`。

## incident (誠実記録)

1. **実行環境リセット (03:00Z頃)**: D5のwave wrapperをbudget 230sで実行
   したところ、deadline超過後も実行中キーの worker待ち (`wait`) が続き
   外側の1バッシュ呼び出し300s capを超過 → 実行環境が棄却され、ローカル
   作業ディレクトリ (初期kit、D1-D4出力、D5完了6キー分のreplica出力)
   を喪失。kit Aは全122ファイル出版済みかつfetch-back byte検証済み
   だったため、published正本から実行kitを再取得し (maker全gate PASS・
   rows.json `64bc4b78…` byte一致で再取得整合を機械検証) D1-D7を
   最初から fresh-cold で再実行した。D1-D4は喪失前と同一のnode-exact
   結果を再現 (決定性の追加傍証)。wave wrapperはbudget 110sに再設計し
   以降の全waveは300s未満で完走。**publish-then-execute設計の有效性が
   実証された事故**でもある (重要証拠が再現可能なpublished bytesのみに
   依存していたため損失ゼロ)。wrapper script (wave_replica.sh /
   wave_third.sh) はsession-localであり出版対象外 (pinned runner
   `8ddf1ef4…` / `run_thirdimpl.sh` `a0b77d83…` のみが本実験の正式
   runner)。
2. **B2 push一時失敗**: 並走レーンの連続push (Part DE path repair・
   完了 / K1279) と競合した "Reference cannot be updated" — 即時再試行
   で成功・内容変更なし。

## 対象 (published正本から機械導出・maker `make_inputs_dc.py` `94dfd45f…`)

22行 ab033..ab054 (lo, hi, legal, s5, membership, result 2, nodes) の
全表は宣言ノート・`input/rows.json` (sha `64bc4b78…`・maker ×2回実行
byte-stable PASS) 参照。sources pin: batch-keys-b29 `330c0b9f…`・
status-b29.log `b49322d9…` (55行 = 54 PASS + WIN-HALT ab028)・drive-2
raw p1/p2 44正本 (`sources/raw/`・p1==p2 determinism機械検証済み)・
CU出版物 (merged-cache-cu `30ddad9d…` 6,317行 / increment-b29loss16
`bab011e3…` / increments-manifest-cu `f9f58ee1…`)・DB出版物
(increment-b29loss37 `85bd4469…` 37行 / merged-cache-db-b29loss37
`04b0a239…` 6,354行 = CU 6,317 + 37)。

## canonical chain に対する位置づけ

現行 canonical merged chain は Part DB C以降 6,354行 `04b0a239…`
(WIN 158 / LOSS 6,196)。class 2251 の canonical unknown は DB後に
38→1 (残1行は未消費WIN ab028・Part DB完了log `10a79660` 記載)。本Part
はこのcacheに読みのみで書き込まず・coverage/class statusを一切変化させ
ない。drive-2 ckpt-1/3 16行 (Part CV `3b6ad066`)・ckpt-2/3 15行
(Part DA・宣言済みoutputs未出版の進行中レーン)・WIN行 ab028 (Part CZ
`68751fd7`) は本Part対象外・非接触 (対抗レーンなしを宣言時に機械走査)。

## verdict不消費の再明記

標準11×11空盤の勝敗は **UNKNOWN**。central-reply 19 roots・二石root・
class 2251・batch-29全54キーも **UNKNOWN**。本実験の全nodes/expansions
数は照合・検証の指標であり勝敗の主張ではない。
