# 2026-11-16：cost-65f WIN 13 bits（4/15/18/20/21/23/25/28/66/79/91/101/109）の証明書抽出・出版完結 — 65j fold v2の全17 WIN receiptsがcertifiedに（65f 13枚+65j 4枚）・BigInt+Bareiss二重検証・head 1419不変・11×11等はUNKNOWN

開始時点: cost-65j fold v2着地済み（head 1419・claim v5 `7a4c9007`）。foldが閉じた9行のうち65j証明書4枚（bits 112/116/118/119・manifest `d4981d7e`）はcertified。65f v15由来の13 receiptは証明書なし（certified:false）だった。本セッションで**65f 13枚すべてを抽出・二重検証・出版し、head 1419にfoldされた全17 WIN receipts（65f 13+65j 4）の証明基盤を独立検証可能な証明書で完結**させた。

## 実施内容

### 1. 盲抽出（`scripts/cert_driver65j.ts`・repo-verbatim v16 engine・空kill table）

- root=child|1<<bit（child `00000000000000809102000080000000`）。**全13rootがfold receipt（`class-frontier-cost65j-receipts-recompute-20261116.json`）のroot_hexとbyte-identical事前確認済み**（assert付き）。driver moves == legal_candidates(root) mobility（assemble scriptがassert）。
- 抽出結果（全てfatal 0・fbt_drops 0・perMove capped 0・合計約3.2分）:

| bit | root（頭部省略=`000…809102000080`+下略） | rows | nodes | sub-roots | ms | 備考 |
|-----|-----|-----|-----|-----|-----|-----|
| 4 | `…000010` | 56,237 | 5,974,156 | 56 | 13,088 | mim=1 |
| 15 | `…008000` | 42,135 | 3,403,564 | 54 | 8,624 | zero-mim |
| 18 | `…004000` | 68,379 | 11,037,457 | 61 | 20,875 | mim=1・最重 |
| 20 | `…100000` | 43,119 | 3,272,794 | 52 | 9,230 | mim=1・cost-64行 |
| 21 | `…200000` | 50,284 | 4,025,789 | 52 | 10,743 | mim=1・cost-64行 |
| 23 | `…800000` | 32,606 | 1,232,884 | 48 | 4,617 | zero-mim |
| 25 | `…820000` | 44,299 | 4,387,529 | 51 | 10,356 | zero-mim・72b rootとbyte-identical |
| 28 | `…900000` | 51,248 | 3,641,657 | 54 | 10,268 | mim=1 |
| 66 | `00…084910…` | 45,193 | 4,127,663 | 51 | 10,464 | zero-mim |
| 79 | `…808091…` | 39,574 | 3,246,377 | 49 | 8,909 | zero-mim・63a bit-97と同orbit |
| 91 | `…80000…` | 31,769 | 1,623,250 | 47 | 5,703 | zero-mim・72b bit-91と同orbit |
| 101 | `…02000…` | 25,467 | 1,241,255 | 46 | 4,332 | zero-mim・69i bit-101と同orbit |
| 109 | `0020…` | 57,527 | 6,823,357 | 57 | 14,484 | mim=1・D4非自明canon `00000000020000811202000000000800` |

- v15 raw sweep nodes比は0.18〜0.33×（v16 node計数差によるもの・検証は独立実施）。

### 2. 組立・二重検証（`scripts/assemble_cost65f_certificates_20261116.py`・65j版の13 bits変種）

- **全13枚BigInt union missing 0 / extra 0（sub-roots全PASS・terminals [13,17]）+ Bareiss全PASS（`verify_bit7_win7_cert.ts --root-check`・stones 7）の二重検証**。
- whole certは1,178,881〜2,467,325 bytes。**10枚が1,200,000-byte publication split閾値超過 → part1of2+part2of2+join receipt、bits 23/91/101は閾値下→whole certのまま出版**（1,178,881/1,148,784/918,310 B）。cat再構成のbyte-exact性はreceiptが保証。
- **assemble script再実行で全出力byte-identical確認済み**（raw chunk・manifest・verify 26枚・parts・receipts全blob sha一致・複数回）。

### 3. manifest

`output/class2-lane-cost65f-win13-certificates-20261116.json`（schema `n11-class2-lane-cost65f-win13-certificates-20261116-v1`・blob `617d3d8d`・26,542 bytes）。totals: **13 certs・587,837 rows・54,037,732 extraction nodes・678 sub-roots・winner 819,397・loser 246,001・terminals 203,995・21,234,753 bytes**。target.noteは「6 mim=1 receipt（各1行閉鎖・bits 20/21はcost-64行）+7 zero-mim receipt。65j 4枚（`d4981d7e`）と合わせhead 1419にfoldされた全WIN receiptがcertified。bits 25/79/91/101は他lane folded roots（72b/63a/69i）とorbit一致・全WIN/WIN・conflict 0」を明記。

**出版順序**: bits 20/21（win2 manifest `4ad01f58`・commit `0f551304`）→ 6 bits版（win6 manifest `5666d730`・rev2 `5028331d`・commit群 `147b221b`/`314f4269`）→ **13 bits完結版（win13 manifest `617d3d8d`・本commit群）**。旧manifestはgit historyに残る。bits 4/18/20/21/28/109のparts/verify 24ファイルは不変（同一blob・win13に同一pinが入る）。

### 4. 出版commits（本commit群まで）

- `0f551304`+`ebdf8cf9`/`0959546c`+`19465182`/`f5fd1231`: bits 20/21（win2）
- `147b221b`+bit4/18/28/109の8 parts個別commit群+`314f4269`: 6 bits版（win6・rev2）
- 本commit群: bits 15/23/25/66/79/91/101（win13 manifest・assemble script 13 bits版・verify/receipt/summary・parts 8枚+whole 3枚）

## 意味

- **head 1419にfoldされた全17 WIN receiptsの証明基盤が独立検証可能な証明書で完結**（65f 13枚 + 65j 4枚・計17枚・抽出nodes計90,819,037（54,037,732+36,781,305）・証明書計29,616,130 bytes（21,234,753+8,381,377））。WIN7証明書は「個別7石root（相手初手すべてに対するfirst-player win・depth 10以内）」のみを証明する。fold閉鎖の簿記（head 1419）は不変。
- bits 25/79/91/101の証明書は、他lane folded roots（72b bit-25 root byte-identical・63a bit-97 orbit・72b bit-91 orbit・69i bit-101 orbit）とverdictがWIN/WIN一致することの追い証拠でもある（conflict census 0・`96e0d14d`参照）。
- **claim v5のreceipts欄certified:false表記の更新は次回claim改訂（v6）時にまとめて実施**（recompute scriptがCLAIM_BLOB=7a4c9007をpinしているため、claim単独更新はfold script再現assertを壊す — claim v6化はscript pin更新とセットで）。

## UNKNOWN guard

- **solved 1419はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWNのまま**。
