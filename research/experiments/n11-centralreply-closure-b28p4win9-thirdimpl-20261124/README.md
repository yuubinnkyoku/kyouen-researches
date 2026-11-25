# batch-28 (closure class 5343) b28-win46 thirdimpl queue registry P4パッケージ9行 (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050) 第三実装交叉検証 — Part DH (2026-11-24)

Part DH (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-dh-b28p4win9-thirdimpl-declaration.md` 出版・observed HEAD
`014a0361` = Part DG 完了log commit)。
b28-win46 thirdimpl queue registry (REVISION 3・実験
`n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`・queue-registry.json
`334f6209…` / README-queue `4b20c6a0…`) 上の open 25 WIN行のうち**P4パッケージ9行**
(pinned nodes昇順 aa011→aa050) に対するpinned第三実装 (非df-pn AND/ORミニマックス
`third_impl.js` `08ea958f…`) による verdict-level交叉検証 + 本host pinned-replica
(`jsreplay.js` `84585617…`) 2-pass fresh-cold再現。

9行の内訳 (per-key決定probe条件が本Partの特徴):
- **5行 (aa011/aa054/aa022/aa034/aa037)** は drive-4/drive-5 experiments
  (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) の 15M-probe
  (budget 15,000,000) で解決した WIN rows (rc=1)。aa011/aa022 は drive-4決定
  (決定的2行は drive-5 logでも byte同一・cross-log gate実施)、残り3キーは drive-5決定。
- **4行 (aa032/aa028/aa021/aa050)** は base 15M-probe では CO時点で EXHAUSTED
  (Part CO manifest exhausted_excluded_ids 11行の内員 = CO-time honest labels) だったが、
  その後の reprobe experiments
  (`n11-centralreply-class5343-b28exhausted-reprobe25m-20261123` /
  `…-reprobe30m-…`) の 25M/30M-probe で解決した WIN rows。aa032/aa028/aa021 は
  cs-25m (budget 25,000,000)・aa050 は ct-30m (budget 30,000,000) 決定。
  これら4行は Part CO win roster外 (CO時点のhonest labelは exhausted)。
- pinned nodes合計 **158,393,401**・registry est_crossimpl_2pass_nodes合計 **373,808,426**
  (全9行 thirdimpl state=open・本Partが最初の交叉検証)。

anchors k02a (1297036692683751424, 68157440) expect 1 / l1a (13019119616, 16448)
expect 2、negatives ng1 (legal+1) / ng2 (stones 6) はBF chain byte-clone。

## 対象 9行 (published・全てUNCONSUMED honest labels・rows.json `6a0e4012…`・maker ×2 byte-stable)

| key | key (lo,hi) | s5 | legal | verdict | pinned nodes | 決定log (budget) |
| --- | --- | --- | --- | --- | --- | --- |
| aa011 | 1171516445255796736,0 | 147632 | 90 | WIN | 12,424,953 | drive4-15m (両drive log一致) |
| aa054 | 1152921504606863360,4228 | 199739 | 95 | WIN | 13,227,570 | drive5-15m |
| aa022 | 1171516479615533056,0 | 191399 | 87 | WIN | 14,044,375 | drive4-15m (両drive log一致) |
| aa034 | 1152921504606846977,4228 | 199719 | 94 | WIN | 14,097,048 | drive5-15m |
| aa037 | 1152921504606846980,4228 | 199722 | 87 | WIN | 14,239,714 | drive5-15m |
| aa032 | 1171516445255794688,4 | 199717 | 91 | WIN | 20,312,294 | cs-25m |
| aa028 | 1152921504606879744,4228 | 199713 | 95 | WIN | 21,563,925 | cs-25m |
| aa021 | 1171516462435663872,0 | 188751 | 90 | WIN | 22,942,323 | cs-25m |
| aa050 | 1152921504640401408,4228 | 199735 | 94 | WIN | 25,541,199 | ct-30m |

全行 membership 4・batch-28 base batch-keys budget 15,000,000 (メタデータ不変 gate)。
aa034/aa050 は published raw p1==p2 byte同一 (出版事実・pin重複は意図的)。
drive log内のCO-time 15M EXHAUSTED行 (aa021/aa028: 両drive log byte一致 /
aa032/aa050: drive5のみ) と P1/P2-TRUNCATED-RETRY行 (aa034 18:49:33Z・aa050) は
honest historyとして許容gateで機械検証 (それ以外のTRUNCATEDはfail-closed)。

## kit構成 (A1 scripts 7 + input 14 + val-gate 8 + README / A2 sources 44)

- `scripts/` 7: make_inputs_dh.py (`8036d0e5…`・DG maker適応系譜・per-key budget/
  新status battery/CO split battery/QREG rev3文脈gate込み) / audit_dh.py
  (`88e25e0e…`・DG audit適応・PIN_RAW_DH 18 pin・per-key replica budget gate・
  `.dh-host.out` suffix・G6 CO split battery) / run_replica_dh.sh (`4dae72ac…`・
  **1呼び出し1パス**設計・per-key budget/timeout表 15M→260s/25M→288s/30M→295s) /
  run_thirdimpl.sh (`a0b77d83…` byte-clone) / third_impl.js (`08ea958f…`) /
  verify_tbl.js (`c8c52528…`) / jsreplay.js (`84585617…`) — 下4つはpinned byte-clone。
- `sources/` 44: raw 18 (9キー×p1/p2・決定drive/reprobe experiment正本) +
  published-input 9 + published-input-bf 4 (DG Kitからbyte-clone) +
  status-drive4.log `59817444…` (61行) + status-drive5.log `ca1e98cc…` (109行) +
  status-cs25m.log `cea47a0c…` (12行: PASS6/WH4/EXH1/P2TR1) +
  status-ct30m.log `efd18b3c…` (6行: PASS3/WH2/P2TR1) + batch-keys-b28.json
  `af19208f…` + queue-registry.json (rev3) `334f6209…` + README-queue.md (rev3)
  `4b20c6a0…` + Part CO 7-LOSS adoption出版物 (merged canonical cache `854800f3…`
  6,301行 / increment `bd5ef7d7…` / increments-manifest `b47e07ca…`) + Part DB
  37-LOSS re-adoption出版物 (merged canonical cache `04b0a239…` 6,354行・現canonical
  chain head / increment `85bd4469…` / increments-manifest `1b51f30d…`)。
- `input/` 14: rows.json + 9対象 + anchors k02a/l1a + negatives ng1/ng2のinput CSV。
- `val-gate/` 8: at2m×2 + first-15m/second-15m published baselines + inputs
  (CW→DGから不変byte-clone・host出力は `.dh-host.out` として生成)。

## 宣言済み検証計画 (D1-D8・publish-then-execute)

- D1 rules-gate (verify_tbl.js・quads 95,670/triples 195,044 mismatches 0)
- D2 val-gate fresh 4 (2M/2M/15M/15M・`.dh-host.out`・baselines node-exact)
- D3 negatives (ng1/ng2 fail-closed) / D4 anchors k02a/l1a (exp 9,106,337/7,660,202)
- D5 replica 18 pass (9キー×p1/p2・**per-key budget**・audit G2bで p1==p2 +
  published node-exact)
- D6 thirdimpl 18 run (9キー×a/b・wallcap240・est pass-one最大 aa050 ~30M)
- D7 audit ×3 (audit_dh.py・全gate PASS・summary byte-identical)
- D8 tamper battery (宣言前実行済み: byte層T1-T8 + 意味層S-a/S-b/S-c = 11/11捕捉 +
  復帰green)

verdicts不消費・採用はscrutiny owner C++ gate (`9193f5b6…`・pinned merger
`90711961…`経由)専権。**標準11×11空盤・19 central-reply roots・二石root
{49,60}/{59,60}・S2 {59,60}・class 5343 (全54キー) はUNKNOWNのまま**。本実験の
WIN labelsは unadopted honest labels であり勝敗確定ではない。
