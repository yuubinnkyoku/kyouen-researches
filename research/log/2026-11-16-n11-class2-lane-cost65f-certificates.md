# 2026-11-16：cost-65f WIN bits 4/18/20/21/28/109の証明書抽出・出版 — 65j fold v2の9行閉鎖のうち65f担当事の6行をcertified receiptに格上げ（BigInt+Bareiss二重検証）・head 1419不変・11×11等はUNKNOWN

開始時点: cost-65j fold v2着地済み（head 1419・claim v5 `7a4c9007`）。foldが閉じた9行のうち65j証明書4枚（bits 112/116/118/119・manifest `d4981d7e`）はcertified。65f v15由来の9 receiptのうち**marginal-in-manifest 1の6本（bits 4/18/20/21/28/109・各1行閉鎖）は証明書なし（certified:false）**だった。本セッションでこの6枚を抽出・二重検証・出版し、**9行閉鎖のうち65f担当事6行をcertified receiptに格上げした（65j 4枚と合わせ9行すべてcertified）**。zero-mimの7本（bits 15/23/25/66/79/91/101）は単独ではopen行を閉じておらず、blob-pin済みraw sweep記録ベースのまま。

## 実施内容

### 1. 盲抽出（`scripts/cert_driver65j.ts`・repo-verbatim v16 engine・空kill table）

- root=child|1<<bit（child `00000000000000809102000080000000`）。**全6rootがfold receipt（`class-frontier-cost65j-receipts-recompute-20261116.json`）のroot_hexとbyte-identical事前確認済み**。driver moves == legal_candidates(root) mobility（assemble scriptがassert）。
- 抽出（全てfatal 0・fbt_drops 0・perMove capped 0）:
  - bit 4（root `00000000000000809102000080000010`）: **56,237 rows / 5,974,156 nodes / 56 sub-roots / 13.1s**
  - bit 18（`…809102000080040000`）: **68,379 rows / 11,037,457 nodes / 61 sub-roots / 20.9s**
  - bit 20（`…809102000080100000`）: **43,119 rows / 3,272,794 nodes / 52 sub-roots / 9.2s**
  - bit 21（`…809102000080200000`）: **50,284 rows / 4,025,789 nodes / 52 sub-roots / 10.7s**
  - bit 28（`…809102000090000000`）: **51,248 rows / 3,641,657 nodes / 54 sub-roots / 10.3s**
  - bit 109（`00002000000000809102000080000000`）: **57,527 rows / 6,823,357 nodes / 57 sub-roots / 14.5s**
- v15 raw sweep nodes比は0.26〜0.33×（v16 node計数差によるもので、検証は独立実施）。

### 2. 組立・二重検証（`scripts/assemble_cost65f_certificates_20261116.py`・65j版の6 bits変種）

- **全6枚BigInt union missing 0 / extra 0（sub-roots全PASS・terminals [13,17]）+ Bareiss全PASS（`verify_bit7_win7_cert.ts --root-check`・stones 7）の二重検証**。root mobilityはlegal_candidates.pyと一致。
- whole cert: bit 4 = 2,035,458 B・bit 18 = 2,467,325 B・bit 20 = 1,558,820 B・bit 21 = 1,817,363 B・bit 28 = 1,850,452 B・bit 109 = 2,077,808 B。**全6枚とも1,200,000-byte publication split閾値超過 → part1of2+part2of2+join receiptで出版**（最大part 1,233,667 B = bit 18 p1）。cat再構成のbyte-exact性はreceiptが保証。
- **assemble script再実行で全出力byte-identical確認済み**（raw chunk・manifest・verify 24枚・parts・receipts全blob sha一致・2回）。

### 3. manifest

`output/class2-lane-cost65f-win6-certificates-20261116.json`（schema `n11-class2-lane-cost65f-win6-certificates-20261116-v1`・blob `5666d730`・14,234 bytes）。totals: **6 certs・326,794 rows・34,775,210 extraction nodes・332 sub-roots・winner 450,022・loser 132,304・terminals 116,447・11,807,226 bytes**。target.noteは「6 bitsはfold v2のmim=1 receipt（各1行閉鎖・bits 20/21はcost-64行）。65j 4枚（`d4981d7e`）と合わせ9行すべてcertified。zero-mim 7 bitsはraw記録ベースのまま」を明記。

**出版順序**: 最初にbits 20/21の2枚を`class2-lane-cost65f-win2-certificates-20261116.json`（blob `4ad01f58`・commit `0f551304`）として出版し、その後6 bits版に拡張した。win2 manifestはwin6に置き換わる（git historyに残る・本logが相互参照）。bits 20/21のparts/verify 8ファイルは不変（同一blobで再出版不要・win6 manifestに同一pinが入る）。

### 4. 出版commits

- `0f551304`: bits 20/21小ファイル一式（log v1 + win2 manifest + assemble script + verify 8枚）
- `ebdf8cf9`/`0959546c`: bit 21 parts（908,701/908,662 B）
- `19465182`/`f5fd1231`: bit 20 parts（779,413/779,407 B）
- （本commit群）: bits 4/18/28/109小ファイル + win6 manifest + assemble script 6 bits版 + log v2 + 8 parts

## 意味

- **fold v2の9行閉鎖の証明基盤が全て独立検証可能な証明書になった**（65f 6枚 + 65j 4枚）。WIN7証明書は「個別7石root（相手初手すべてに対するfirst-player win・depth 10以内）」のみを証明する。fold閉鎖の簿記（head 1419）は不変。
- zero-mim 7 bits（15/23/25/66/79/91/101）の証明書抽出は残課題（fold閉鎖には不要・raw記録ベースで十分）。bit 25/79/91/101は他lane fold rootsとのorbit一致(WIN/WIN)が既にcensus済み（`96e0d14d`のlog参照）。
- claim v5のreceipts欄certified表記の更新はfollow-up（**recompute scriptがCLAIM_BLOB=7a4c9007をpinしているため、claim単独更新はfold script再現assertを壊す — claim v6化はscript pin更新とセットで実施**）。

## UNKNOWN guard

- **solved 1419はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWNのまま**。
