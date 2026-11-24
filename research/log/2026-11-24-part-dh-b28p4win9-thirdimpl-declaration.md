# Part DH宣言: b28 P4パッケージ9行 (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050) 第三実装交叉検証 (publish-then-execute)

- 2026-11-24 (Part DH 宣言・実験dir `research/experiments/n11-centralreply-closure-b28p4win9-thirdimpl-20261124/`)
- 方式: publish-then-execute・単一オーナー。本宣言は実行前に出版する。kit (scripts+input+val-gate+README=A1, sources 44=A2) 出版後、D1-D8を実行し結果をB commit (output)・C commit (README最終+MANIFEST) で反映する。

## observed HEAD・対抗宣言機械確認

- observed HEAD (kit disk sources取得 + 宣言直前確認): `014a0361e659c74fcbd10ae9492d0a843388c401` (Part DG 完了log commit = 現main HEAD)。
- 対抗宣言: GitHub search API `q=repo:yuubinnkyoku/kyouen-researches+Part+DH` total_count **0** (2026-11-24T06:06:32Z時点・宣言log執筆直前に再確認)。`research/log/2026-11-24-part-dh-…` 既存log 0件・実験dir `n11-centralreply-closure-b28p4win9-thirdimpl-20261124` 未存在 (GitHub contents API確認済み)。
- 前回レーン状況: Part DG (P3パッケージ8行) 当レーン完結済み (`014a0361`)・Part DA (b29d2loss15 thirdimpl) 他レーンtakeover済み (`f2b36862`, 非接触)・Part DF (P2) 未完でもP4 scopeは独立。

## 対象 (queue registry rev3 P4パッケージ・全54行中の9 WIN行)

b28-win46 thirdimpl queue registry (REVISION 3, `334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9` / README-queue `4b20c6a0f98b399dcbfd86386134cab9d1258a7dbcb1690387dcb2f46d1a793e`) のP4パッケージ9行。全行 membership 4・thirdimpl state=open・pinned honest label WIN (rc=1)・**UNCONSUMED**:

| key | lo,hi | s5 | legal | budget | nodes | 決定log |
| --- | --- | --- | --- | --- | --- | --- |
| aa011 | 1171516445255796736,0 | 147632 | 90 | 15,000,000 | 12,424,953 | drive4-15m (両log一致) |
| aa054 | 1152921504606863360,4228 | 199739 | 95 | 15,000,000 | 13,227,570 | drive5-15m |
| aa022 | 1171516479615533056,0 | 191399 | 87 | 15,000,000 | 14,044,375 | drive4-15m (両log一致) |
| aa034 | 1152921504606846977,4228 | 199719 | 94 | 15,000,000 | 14,097,048 | drive5-15m |
| aa037 | 1152921504606846980,4228 | 199722 | 87 | 15,000,000 | 14,239,714 | drive5-15m |
| aa032 | 1171516445255794688,4 | 199717 | 91 | 25,000,000 | 20,312,294 | cs-25m |
| aa028 | 1152921504606879744,4228 | 199713 | 95 | 25,000,000 | 21,563,925 | cs-25m |
| aa021 | 1171516462435663872,0 | 188751 | 90 | 25,000,000 | 22,942,323 | cs-25m |
| aa050 | 1152921504640401408,4228 | 199735 | 94 | 30,000,000 | 25,541,199 | ct-30m |

- pinned nodes合計 158,393,401・est_crossimpl_2pass_nodes合計 373,808,426 (registry rev3から機械取得)。
- 5行 (TIER15: aa011/aa054/aa022/aa034/aa037) はPart CO win roster (unadopted_win_rows) node-exact内員。4行 (REPROBE: aa032/aa028/aa021/aa050) は**CO時点 EXHAUSTED** でPart CO exhausted_excluded_ids (11行) 内員・win roster外・WIN labelの出どころはreprobe decisive logs (cs-25m/ct-30m) + registry rev3。
- CO-time 15M EXHAUSTED rows: aa021/aa028 は両drive log byte一致・aa032/aa050 はdrive5のみ (honest historyとして許容gate)。aa034 (drive5 18:49:33Z)・aa050 (ct-30m) のP2-TRUNCATED-RETRYも許容gate (fail-closed otherwise)。

## 出版物とpin (A1 = scripts 7 + input 14 + val-gate 8 + README / A2 = sources 44)

- scripts: make_inputs_dh.py `8036d0e58180dcc1ab0d436ff9da0225697bebaf36f581943b4c0af37e388cad` / audit_dh.py `88e25e0ef78d3680a85fbdeb800c6d745835546cbed6ebf46f59b8a66d1db92e` / run_replica_dh.sh `4dae72ac33cca0adb28bb5c3a29f5591595d49bace303947700788b6d2c05491` / run_thirdimpl.sh `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41` (DG byte-clone) / third_impl.js `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` / verify_tbl.js `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251` / jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (下3つDG Kitからbyte-clone・sha検証済み)
- input/rows.json `6a0e40126474c57f691108b488fa843719664b94700b22d6f29db4c11a410afb` (maker ×2 実行 byte-stable・stdout byte-identical)
- sources 44: raw 18 pin (aa011.p1 `171d6381…` / aa011.p2 `9864d2b0…` / aa022.p1 `5feb0353…` / aa022.p2 `da703e37…` / aa054.p1 `d79d24f7…` / aa054.p2 `997a0aae…` / aa034.p1 = aa034.p2 `42580df2c86f7b602880d0fe453c8fb0af3c315e2cc989a1e3df6bf2fa2d82e9` (byte同一・出版事実) / aa037.p1 `4defd77a…` / aa037.p2 `5bc188380b8d89c0dc3ca304622d21264c24a0bccc130628cdc590e2f3f89712` / aa021.p1 `0082e9d0…` / aa021.p2 `35a98fda…` / aa028.p1 `d57f3c07…` / aa028.p2 `c41b5ab4…` / aa032.p1 `85a787a9…` / aa032.p2 `31227164…` / aa050.p1 = aa050.p2 `aada66cf31f2f99a04433d04c237cac3e3b22a02cd5a6514c75a440073d099c8` (byte同一・出版事実))、published-input 9・published-input-bf 4 (DG Kit byte-clone・maker pin gate済み)、status-drive4 `59817444…` / status-drive5 `ca1e98cc…` / status-cs25m `cea47a0c…` / status-ct30m `efd18b3c…`、batch-keys-b28 `af19208f…`、queue-registry `334f6209…`、README-queue `4b20c6a0…`、CO cache `854800f3…` / CO increment `bd5ef7d7…` / CO manifest `b47e07ca…`、DB cache `04b0a239…` / DB increment `85bd4469…` / DB manifest `1b51f30d…`
- val-gate 8 (CW→DG byte-clone・全pin maker gate済み)

## 宣言済みdelta (DG機構に対する適応・全て事前宣言)

1. 対象をP3 8行→P4 9行へ (per-key decisive budgets: 15M×5 / 25M×3 / 30M×1)。batch-keys base budget 15Mは不変gate。
2. 新status battery: status-cs25m.log (12行: PASS6/WH4/EXH1/P2TR1) と status-ct30m.log (6行: PASS3/WH2/P2TR1) を pin + 辞書比較。
3. decisive log内 P1/P2-TRUNCATED-RETRY 許容 (aa034/aa050のみ該当行pin付き、他はfail-closed)。
4. CO split battery: TIER15_KEYS 5行 = CO win roster node-exact / REPROBE_KEYS 4行 = CO exhausted_excluded_ids内員かつwin roster・uwr外 (registry rev3のscope的事実をそのまま機械検証)。
5. CO-time EXHAUSTED行 (aa021/aa028両log・aa032/aa050 drive5) をdrive log battery側で許容tie。
6. audit_dh.py: target 9・PIN_RAW_DH 18 pin・per-key replica budget gate・val-gate host suffix `.dh-host.out`・G6 CO split battery。G0-G5/G7論理はDG機構不変。
7. run_replica_dh.sh: **1呼び出し1パス**設計 (引数 `<key> <pass>`)・per-key budget/timeout表 (15M→260s / 25M→288s / 30M→295s)。重いパスが外側tool cap (300s) 内で完走するための構造変更。
8. anchors/negativesはDG Kit byte-clone (k02a exp 9,106,337 / l1a exp 7,660,202・fail-closedモデル不変)。

## 事前機械検証 (宣言前・未出版状態で実施)

- maker gates PASS ×2・stdout byte-identical (`9a38606e…` = `/tmp/m1.txt` 基準)・input 14 file byte-stable。
- audit_dh.py全pin機械照合 (maker pin dict と実ファイルsha・両側一致・bad=0)。
- 事前tamper battery **11/11捕捉 + 復帰green** (byte層: raw nodes改竄 / published-input legal+1 / qreg byte / CO manifest byte / DB cache forge行 / cs25m aa021 PASS行削除 / batch-keys s5_index / ct30m nodes改竄 → 全rc=1。意味層: raw aa011 nodes+1+pin更新 (p1/p2 determinism gate) / CO exhausted roster aa050→aa099+manifest pin更新 (member/split battery) / qreg aa050→aa099+pin更新 (P4 keys battery))。復帰後 clean maker rc=0・sources byte-exact復元確認。

## 誠実記録 (incident・宣言前に検出・修正済み・誤 publics なし)

1. audit_dh.py執筆時に PIN_INCREMENT_CO_ROWS を誤って3行まで欠落して書いた (DGの7行正本に対する手打ち転写ミス)。機械照合 (実ファイル7行 vs pin) が即検出し、7行正本へ修正済み。
2. audit_dh.pyの PIN_RAW_DH["aa037.p2"] に手打ちtypo (`…c24a5bccc…` vs 正 `…c24a0bccc…`)。全pin機械照合が検出し修正済み (実ファイルshaで照合)。
3. 事前tamper batteryのT6実装で、python lambda内で `open(p,'w')` がジェネレータ読み取りの前にファイルをtruncateし、意図せず空ファイルsha (`e3b0c442…`) でpin gateが発火した。空ファイル改竄としてもfail-closedには違いないが意図した「1行削除」ではなかったため、read-then-writeでやり直し、意図どおりの1行削除でpin gate発火を確認 (`5841d0b4…` ≠ pin)。上記2・3とも宣言前に修正・検証済みで、誤った状態のkitは1 byteも出版していない。

## 検証計画 D1-D8 (publish-then-execute)

D1 rules-gate (quads 95,670 / triples 195,044 / mismatches 0) → D2 val-gate fresh 4 (`.dh-host.out`・baseline node-exact) → D3 negatives → D4 anchors → D5 replica 18 pass (per-key budget・p1==p2) → D6 thirdimpl 18 run (wallcap240・est最大 aa050 pass-one ~30M・runlimit時はWALL-INCONCLUSIVEとしてhonest記録しverdictとはしない) → D7 audit ×3 (全gate PASS・byte-identical) → D8 tamper。

## 不変事項

- verdicts不消費・9行とも unadopted honest labels。採用・解放・閉包はscrutiny owner C++ second-implementation gate pin `9193f5b6…` (pinned merger `90711961…`経由) 専権。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 5343 (全54キー) はUNKNOWNのまま**。本実験の途中結果から勝敗を断定しない。拡張数やcache hitを勝敗として読まない。
