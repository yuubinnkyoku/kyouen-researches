# 2026-11-17：cost-60c/69e/70g帯証明書のbytes再検証（head-1452被覆censusフォローアップ）— 3帯19 record全てがmanifest pinとbyte一致・BigInt独立verifier 19/19 PASS・740,931 rows再検証でtier R格上げ

開始時の最新mainは `0b81d0d1763a218caae22f867612b1919eec4f38`（cost65f/65jのv17再検査キュー完走push直後）。head-1452証明書被覆census v3（775/775 certified・tier R 525）の含意3「tier R 525 rootの証明書bytes自体の再検証は今後の強化候補」を受け、既にbytes再検証済みの58c（33 record）とwarm/multiband（82 record）に続き、**receiptcert-only帯の次の3帯 cost-60c（1 record）+ cost-69e（10 record）+ cost-70g（8 record）の計19 record**を対象に、出版証明書bytesの再取得・digest照合・BigInt独立verifier再実行を行った。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 実施内容

1. **bytes再取得とpin照合**: 3帯の証明書ファイル（計19件・約25MB）をmain commit `0b81d0d1` のraw CDNから取得し、出版manifestのdigest pinと照合した。
   - **cost-60c**（manifest `class2-lane-cost60c-win7-certificates-20261116.json`）: bit92のgit blob SHA `b3512889` + whole md5 `d771ef82` + sha256 `33fcd485` + 996,758 bytes 全一致。
   - **cost-69e**（manifest `class2-lane-cost69e-win7-certificates-20261114.json`）: bit 21/99/87/84/76/90/89/94/108の9枚の全ファイルmd5/sha256一致。**bit 116は出版形態がbase64(gzip -9)**のため、in-memoryで `base64 -d | gunzip` 復元し、gz_b64 md5 `9aa8925c`・復元後 md5 `69114048`・sha256 `20c0f5ed`・2,670,116 bytes・74,115 lines の全pin一致を確認してから検証に供した。
   - **cost-70g**（manifest `class2-lane-cost70g-win7-certificates-20261115.json`）: 8枚すべてのper-cert git blob SHA pin（`1877c1c6`/`b2a83239`/`bab4338b`/`e95fcaf5`/`1c023a37`/`d522d9eb`/`63a6c8b4`/`b5a42979`）一致。
2. **BigInt独立verifier再実行**: `verify_win7_certificate_bigint_independent.mjs`（git blob `62b5d941`・ローカルcopyのblob SHA一致をassert）を19証明書全部に4並列で再実行した。

## 結果

- **55 checks全PASS**。19/19証明書がverifier PASS（union missing/extra 0/0・rows sorted unique・root stones 7・safe・terminal range [13,17] 全件）。
- **manifest統計の完全再現**: 全19件で rows / sub-roots / root mobility / terminal_count / winner/loser states / visited states / loser reply edges がmanifest記録値と完全一致（60c bit92: 27,547 rows・45 sub-roots・terminals 8,543・69e bit116: 74,113 rows・59 sub-roots・70g bit34: 56,345 rows・63 sub-roots など）。
- nodes総和（戦略rows）: **740,931 rows**。2回実行で監査JSON byte-identical（決定性確認済み・bit116復元の一時ファイルは実行後に自動削除）。

## 含意

1. **tier R→bytes再検証済みの格上げ**: bytes再検証済みrecordは58c 33 + warm/multiband 82 + 本3帯19 = **134 record**に拡大。69e帯（11 WIN bits中10枚・最大のreceipts bandの一つ）と60c/70g帯の証明書が「manifest記録の検証主張」から「本環境でのbytes+verifier再実行確認」に格上げされた。
2. 76c bit113型リスク（記録はあるがbytesが未検証のWIN receipt）の母集団は、この3帯については消滅。head-1452のfrontier数字は一切変わらない（簿記の強化のみ）。
3. 69e bit116のbase64(gzip)出版形態が**復元round-tripで失なく検証可能**であることを実証（gz_b64/uncompressed両digestの二重pinが効いている）。
4. 残るreceiptcert-only bytes再検証候補: 63h/63i/63j/65m/67d等のreceipts-recompute帯（証明書bytesはmain上に存在）・63c/63d bytes再生成。

## 保存物

- 再検証script: `scripts/reverify_cost60c69e70g_certificates_bigint_20261117.py`（stdlibのみ・manifest digest pin内蔵・55 checks・2回実行byte-identical）
- 再検証JSON: `output/class2-lane-cost60c69e70g-certificates-bigint-reverification-20261117.json`（per-certificateのverifier出力・published digest・checks全件）
- 入力（出版済み・main commit `0b81d0d1` 時点のblob/md5/sha256 pin照合済み）: `class2-lane-cost60c-certificates/bit92-root-00000000100000003800000008008020.cert`・`class2-lane-cost69e-certificates/`（10件）・`class2-lane-cost70g-certificates/`（8件）

## 信頼境界

本再検査は出版証明書bytesの一致性とverifier再実行の確認であり、新規の勝敗判定を含まない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。REFUTED-D10はLOSS証明ではない。BigInt verifier自体は「3×3余因子展開・solver/verdict-cache importなし」の独立実装だが、その健全性は本検査ではさらに別実装と突き合わせていない（repoのBareiss verifierとの二重検証は元band出版時に実施済み）。70g manifestの`fold_status: PENDING`は出版時の歴史的記録であり、その後のchainでfold済み（本検査はfold簿記に影響しない）。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
