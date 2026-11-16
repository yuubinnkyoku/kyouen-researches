# 2026-11-16：cost-65f WIN bits 21/20の証明書抽出・出版 — cost-64行2件のfold閉鎖をcertifiedに格上げ（BigInt+Bareiss二重検証）・head 1419不変・11×11等はUNKNOWN

開始時点: cost-65j fold v2着地済み（head 1419・claim v5 `7a4c9007`）。foldが閉じた9行のうち2行（cost-64行 `00000000000000003800000008002002`〔bit 21〕・`00000000000000003800000008003000`〔bit 20〕）は、65f v15 raw batch 2（2026-11-14・blob pin済み）由来のWIN7-D10 receiptに基づくclosingで**証明書が存在しない**（certified:false）状態だった。本セッションでこの2枚を抽出・二重検証・出版し、**cost-64行2件の閉鎖をcertified receiptに格上げ**した。残り11本の65f WIN bits（4,15,18,23,25,28,66,79,91,101,109）は引き続き証明書なし（blob-pin済みraw sweep記録ベース）。

## 実施内容

### 1. 盲抽出（`scripts/cert_driver65j.ts`・repo-verbatim v16 engine・空kill table）

- rootはfold receipt（`class-frontier-cost65j-receipts-recompute-20261116.json`）のroot_hexとbyte-identical事前確認済み: bit 21 → `00000000000000809102000080200000`、bit 20 → `00000000000000809102000080100000`（root=child|1<<bit・child `00000000000000809102000080000000`）。両rootともD4-canonical（d4_canonical_hex == root_hex）。
- driver moves == legal_candidates(root) mobility（52手×2・assemble scriptがassert）。
- bit 21: **50,284 rows / 4,025,789 extraction nodes / 52 sub-roots / 10.7s**（v15 sweep 12,104,576 nodes比0.33×・v16 node計数の違いによるもので検証は独立実施）。
- bit 20: **43,119 rows / 3,272,794 extraction nodes / 52 sub-roots / 9.2s**（v15 sweep 12,621,100 nodes比0.26×）。
- fatal 0・fbt_drops 0・perMove capped 0。

### 2. 組立・二重検証（`scripts/assemble_cost65f_certificates_20261116.py`・65j版のbits 20/21変種）

- rows sorted-unique（exact byte order）+ header/root行prepend。
- **両枚ともBigInt union missing 0 / extra 0（52/52 sub-roots・terminals [13,17]）+ Bareiss 52/52全PASS（`verify_bit7_win7_cert.ts --root-check`・stones 7・loserMobility 52）の二重検証**。root mobilityはlegal_candidates.pyと一致。
- whole cert: bit 21 = 1,817,363 bytes（md5/sha256/git blob `04293ea2…`）・bit 20 = 1,558,820 bytes（`2759f1aa…`）。**両枚とも1,200,000-byte publication split閾値超過 → part1of2+part2of2+join receiptで出版**（bit21: 908,701/908,662・bit20: 779,413/779,407）。cat再構成のbyte-exact性はreceiptが保証。
- **assemble script再実行で全出力byte-identical確認済み**（raw chunk・manifest・verify 6枚・parts・receipts全blob sha一致）。

### 3. manifest

`output/class2-lane-cost65f-win2-certificates-20261116.json`（schema `n11-class2-lane-cost65f-win2-certificates-20261116-v1`）。totals: **2 certs・93,403 rows・7,298,583 extraction nodes・104 sub-roots・winner 136,191・loser 41,060・terminals 33,278・3,376,183 bytes**。per-bit: bit 20 = 43,119 rows/63529 winner/19370 loser/15287 terminals・bit 21 = 50,284/72662/21690/17991。target.noteは「bits 21/20は65j fold v2でcost-64行2件を閉じたreceipt・本manifestでcertifiedに格上げ。残11 bitsはraw sweep記録ベースのまま」を明記。

## 意味

- fold v2の9行閉鎖のうち、**costが最も高い2行（edge cost 64）の証明基盤が独立検証可能な証明書に置き換わった**。WIN7証明書は「個別7石root（52の相手初手すべてに対するfirst-player win・depth 10以内）」のみを証明する。fold閉鎖の簿記（head 1419）は不変。
- 65fの残り11 WIN bitsの証明書抽出は残課題（v15 raw nodes順に重い順: bit 20/21を除くと最大はbatch内の他bits・いずれも同driverで数分以内と推定）。
- claim v5のfold receipts欄のbits 20/21 certified:false表記の更新はfollow-up（claim更新は次回のclaim改訂時にまとめて実施し、本manifestを参照させる）。

## UNKNOWN guard

- **solved 1419はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWNのまま**。
