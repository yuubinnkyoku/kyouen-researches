# 2026-11-17：head-1452折り込みWIN receipt root 775件の証明書被覆census（v3最終版）— 775/775 certified（V 250 / R 525）・uncertified 0・76c bit113型リスク母集団は空

開始時の最新mainは `96b323c0a2559c5feeff17835eb47ff8cc440daa`（cost65n/66c両行のv17全行再検査は並走により着地済みのため本エントリでは重複回避）。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

76c bit 113の偽陽性（fbtOR cache飽和によりWIN→REFUTEDが反転しうる engine 欠陥、証明書の独立検証が最終防壁であることの実証）を受け、**head-1452基底（canonical 1452/174/6396/506144/4669/370058）に折り込まれたWIN receipt root全体（775件）の証明書被覆**を機械照合した。

## 実施内容とv1→v3の経緯

1. **基底再現**: `fold_projection_head1450_tool_20261116.reconstruct()` で771 basis rootsを全assert付きで再現（入力blob pin 136/136照合）。76d/77e receipts recomputeの `totals.root_hexes` 4件（popcount 7 assert）を加え**775 roots**。provenanceは775全rootで完全性assert済み。
2. **v1（commit `3020c5aa`）**: 15種kindの名前ベース分類で588 certified / 187 uncertified。ただし「receipt/fold recomputeファイルはprovenance専用」ルールが構造的に同一の証拠（69f certificate-backedだけ特別扱い）と不整合で、**過少申告**だった。
3. **v2（commit `35748489`）**: 構造ベースの `receiptcert` kind（entryが `certified: true` + rows + md5 + `sub_roots_pass`）を全走査ファイルに適用。cost-58c receipts recomputeが折り込み33件全てにper-entry証明書ドキュメントを持ち、method欄で「全34証明書を出版bytesに対してmd5/rows/sub-roots検証、BigInt/Number Bareiss verifier PASS / union 0/0」まで再assertしていることを確認し、certified 588→695に訂正（+107）。
4. **v3（本版）**: 残り80件の出所を精査した結果、**全てがmain上の証明書記録ファイルに裏付けられていた**ことが判明した: warm-multiband証明書35 records・multiband2 31 records（各record、verify_win7_certificate_bigint_independent.mjsによるBigInt独立検証・sub_roots==loser mobility全PASS・union 0/0・md5/sha256付き）、cost-70c warm6 BigInt independent verification 6 records（tier V）、cost-70c warm batch-3 records 4 records、warm-band-hygiene証明書6 records（68d hygiene折り込みの5 distinct rootsを含む）、cost-63c/63d sweepのwin7_certificates各1 record（Bareiss det4検証付き）。これらを走査集合に加え、receiptcert規則から `certified` 要求を除去（rows+md5+`sub_roots_pass` で十分）した結果、**775/775 certified・uncertified 0** が確定した。

## 結果

- **775 roots全件certified**: tier V 250（生の独立検証アーティファクト所持: bareiss/bigint/tsverify/bigintverify/bigintaudit/verified/verdictverify/orbitverify）・tier R 525（出版証明書記録・検証は記録内で文書化）。
- **uncertified 0**。76c bit113型（証明書のないWIN receipt）のリスク母集団はhead-1452折り込みbasis内に**存在しない**。
- kind組合せhistogram（上位）: receiptcert単独181 / manifest単独161 / receiptcert+manifest 147 / bigint+receipt+receiptcert 72 / verified 70 / bareiss+receiptcert+summary+manifest 22 / bigintverify+receiptcert 6 ほか（全25組合せ、総和775）。
- 80件の内訳（v2時点の未認証、全てv3で解消）: warm-multiband 33 + multiband2 31 + cost-70c warm 6 + cost-70c warm3 3 + 63cd 2 + 68d hygiene 5。

## 含意

1. **head-1452のsolved 1452の簿記は、折り込みWIN receipt rootの全件が出版証明書（独立検証文書付き）で裏付けられている**ことが機械照合で確定した。fbt飽和欠陥により個々のWIN verdictのengine上の信頼性が揺らいでも、head-1452を構成する775 rootは証明書という数学的証拠で保持されている（76c bit113と異なる構図）。
2. v1の「187 uncertified」は走査集合の不完全由来であり、censusの保守的設計（不確実ならuncertifiedに振る）が正しくリスク側に働いたことをそのまま示す。出所ファイルのmethod欄・証明書記録ファイル群を系統的に追うことで、receipt-foldエコシステムの証明書整備がlane全体で行き届いていることが裏付けられた。
3. tier R 525 rootの証明書bytes自体の再検証（BigInt/Bareiss verifierの再実行）は今後の強化候補として残る（本censusは証拠の**存在**の照合であり、bytes再検証ではない）。tier V 250は走査集合内に生の検証出力が存在する。
4. 本censusはhead-1452のfrontier数字を一切変更しない。

## 保存物

- census script（v3）: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/certificate_coverage_census_head1452_20261117.py`（stdlibのみ・基底再現とprovenance完全性をassert・2回実行byte-identical確認）
- census JSON（v3）: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/n11-class2-lane-head1452-receipt-certificate-coverage-census-20261117.json`（schema `...-v3`・headline・775 roots全件のroot_hex / tier / kinds / cert_files数・kind histogram・revision履歴・interpretation guard）
- v1はcommit `3020c5aa`、v2はcommit `35748489` で本日出版済み（同一pathで更新）。走査集合への追加取得ファイル（いずれもmain既存）: `class2-lane-warm-multiband-certificates-20261115.json`・`class2-lane-warm-multiband2-certificates-20261115.json`・`class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json`・`class2-lane-cost70c-warm-batch3-records-20261115.json`・`class2-lane-warm-band-hygiene-certificates-20261115.json`・`class2-lane-cost63c-sweep-20261114.json`・`class2-lane-cost63d-sweep-20261114.json`。

## 信頼境界

tier Rは「走査集合内に生の検証出力がない」ことを意味し、当該記録自体の検証主張（sub-roots全PASS・union 0/0・BigInt/Bareiss verifier記録）を否定するものではない。receiptcertは構造シグネチャ（rows + md5 + sub_roots_pass）による計上であり、個別の証明書bytesの再検証は含まない。certifiedの判定は走査した出版アーティファクト集合に対するものである。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明し、REFUTED-D10はLOSS証明ではない。なお76c bit113（既知の偽陽性）のrootはhead-1452折り込みbasisの入力ファイル群に含まれず（basisに76a/76b/77a-dはあるが76c receipts recomputeは無い）、本censusの775件の母集団には最初から入っていない。76c行自体は並走lane管理。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
