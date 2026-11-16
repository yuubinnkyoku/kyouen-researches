# 2026-11-17：warm-multiband/multiband2/70c-warm/batch3/hygiene計82証明書recordのbytes独立再検証 — 82/82 PASS（rows 3,490,727・sub-roots 4,343・md5全一致）・6件のlayout driftを解消

開始時の最新mainは `427e29fa450482dc5572cdc33a66527a4040f1e9`（前エントリcost-58c 34証明書BigInt独立再検証出版済み）。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

前々エントリのhead-1452 census（tier V 250 / tier R 525）と前エントリのcost-58c再検証（tier R最大ブロック receiptcert単独181のうち58c分33 rootをbytes再検証済みに格上げ）を受け、**残るreceiptcert-onlyブロックの主要部分**、すなわちwarm-multiband（35 records）・warm-multiband2（31）・cost-70c warm6（6）・cost-70c warm-batch3（4）・warm-band-hygiene（6）の**計82 record**について、各recordが参照する証明書bytes（band別certificateディレクトリ内のsingle fileまたは `.part1of2`/`.part2of2` 行境界分割）をmainから取得し、BigInt 3x3余因子verifierで**bytes独立再検証**した。

## 実施内容

1. **record→bytes解決**: 5つのrecordファイルの `storage`（single file / part1of2+part2of2 / `file` テキスト参照）を機械解決し、82 recordが参照する証明書bytesをすべてmain上で特定（103パス中、single指定6件は実体がparts分割であった、後述）。sha-pin URL（main commit `427e29fa`）でダウンロードし、record記載の full bytes / md5、および記載がある場合はper-part bytes / md5と照合。
2. **md5/bytes照合**: 82/82で full md5・bytes 完全一致（per-part md5 mismatch 0）。同一ファイルを共有するrecord重複1件（hygieneのcost-61d bit22とcost-71b bit1が同root `00000000000000803202000000400002` の同一証明書を参照）を確認し、verifier実行はdistinct 81ファイルで実施。
3. **BigInt独立検証**: 出版済み `verify_win7_certificate_bigint_independent.mjs` を81 distinct certificateに実行し、82 recordそれぞれについて verdict・7石・`root_safe`・rows sorted-unique・union 0/0・terminal range 13..17内・`root_hex` 一致・rows・`sub_roots_pass` を全assert。
4. **layout drift の解消**: 6 record（cost63a bits 96/97・cost64b bits 53/116・cost61d bits 114/116）はrecordのstorageが「single file」を宣言するが、repo上の実体は `.part1of2`/`.part2of2` 分割（該当single pathはmain上に存在せず404）。連結したpartsのbytes・md5はrecord記載と完全一致しており、**表示上のdriftであって実質的な不整合ではない**ことを確定し、reverification JSONに `layout_drift_single_declared_parts_found` として明記。

## 結果

- **82/82 PASS・record mismatch 0**: rows総計 **3,490,727**、sub-roots総計 **4,343** がrecord記載と完全一致。再検証bytes総量 **126,089,080 bytes**（distinct 81ファイル、実bytes 124,552,407 + 重複record分）。
- 内訳: warm-multiband 35（rows合計はJSON参照）・warm-multiband2 31・cost-70c warm6 6・warm-batch3 4・warm-band-hygiene 6。全recordのterminal rangeは13..17内、union_missing/extra 0/0。
- 6件のlayout driftを「recordのstorage宣言とrepo実体の乖離」として文書化（bytes/md5は一致、簿記影響なし）。

## 含意

1. **head-1452 censusのtier R主要ブロックがさらに格上げ**: 58c分33 root（前エントリ）に続き、warm-multiband/multiband2の64 roots（censusの80件未認証のうち66相当の母集団からbasis分）、70c warm6+warm3相当の9 record、hygiene 5 distinct rootsの計82 record分が「出版記録」から「bytes独立再検証済み」になった。両エントリ合わせ、**head-1452折り込みbasisのreceiptcert-only母集団のうちbytes再検証済みは115 record分**（censusの receiptcert単独181の主要部分）。
2. 残るbytes再検証候補: 他のreceipts recompute群（60c/63h/63i/63j/65m/67d/70g/65n/66c/69e等、各band certificateディレクトリにbytesが存在）と、63c/63dの証明書bytes再生成（main上にbytesなし）。76d/77e receipts（4 roots）は並走queueのため着手しない。
3. 本再検証はfrontier数字を一切変更しない。

## 保存物

- 再検証script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_warm_multiband_band_certificates_bigint_20261117.py`（repo rootから実行・storage解決は5recordファイルの機械読み取り・全assert込み・2回実行byte-identical確認）
- 再検証JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-warm-multiband-band-certificates-bigint-independent-reverification-20261117.json`（schema `-v1`・82 entries・layout drift/duplicate注記付き）
- いずれも初版のため新規pathで出版。

## 信頼境界

本エントリの「PASS」は個別7石rootのWIN7-D10証明書の数学的検証の再実行であり、solved数やfrontierの変更を意味しない。md5照合の対象はrecord記載の「証明書bytes全体（parts連結後）」である。layout drift 6件はstorage宣言の陳腐化であり、bytes・md5・検証結果への影響はない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
