# 2026-11-17：head-1452折り込みWIN receipt root 775件の証明書被覆census（v2訂正版）— 695 certified（V 241 / R 454）・80 uncertified（verdict-only 74）を確定

開始時の最新mainは `96b323c0a2559c5feeff17835eb47ff8cc440daa`（cost65n/66c両行のv17全行再検査は並走により着地済みのため本エントリでは重複回避）。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

76c bit 113の偽陽性（fbtOR cache飽和によりWIN→REFUTEDが反転しうる engine 欠陥、証明書の独立検証が最終防壁であることの実証）を受け、**head-1452基底（canonical 1452/174/6396/506144/4669/370058）に折り込まれたWIN receipt root全体の証明書被覆**を機械照合した。「fold済みだから安全」ではなく、rootごとに証明書証拠の有無・レベルを確定し、未整備rootを優先順位付きでリスト化することが目的。

## 実施内容

1. **基底再現**: `fold_projection_head1450_tool_20261116.reconstruct()` で771 basis rootsを全assert付きで再現（入力blob pin 136/136照合）。76d/77e receipts recomputeの `totals.root_hexes` 4件（popcount 7 assert）を加え**775 roots**。provenance（出所帰属）は775全rootで完全性assert済み。
2. **証明書証拠スキャン**: 出力アーティファクト一式（`output/*.json`・`output/tmp-cost*/bit*.json`・`output/class2-lane-cost*-certificates/*`・69c manifest）を走査し、15種のkind（bareiss / bigint / tsverify / bigintaudit / verified / verdictverify / orbitverify / receipt / receiptcert / summary / certpart / manifest / warmcert / class4cert / certbacked）に分類。tier V（生の独立検証アーティファクトあり）とtier R（検証を記述する出版証明書記録）を区別。
3. **v1→v2訂正**: v1（commit `3020c5aa`、当日数十分前に出版）は「receipt/fold recomputeファイルはprovenance専用」ルールで臨んでいたが、精査の結果これが**過少申告**であることが判明した。cost-58c receipts recomputeは折り込み33件全てに `certified: true` + rows + md5 + `sub_roots_pass` のper-entry証明書ドキュメントを持ち、method欄で「全34証明書を出版bytesに対してmd5/rows/sub-roots検証、BigInt/Number Bareiss verifier PASS / union 0/0」まで再assertしている（62a/63h/63i/63j/65m/67d/70g/84a/63cd系列のmergedファイルも同様）。v1は69f certificate-backed（`certified:true` entry計上）だけを特別扱いしており、構造的に同一の証拠クラスの取り扱いが不整合だった。**v2では構造ベースの `receiptcert` kind**（root_hexを持つentryが `certified: true` かつ rows・md5・`sub_roots_pass` を持つ）を全走査ファイルに適用し、certifiedは588→**695**に訂正した（+107 roots）。
4. **保守的スコープ（不変）**: WIN言及だけでは証拠にしない（per-entry証明書ドキュメントのみ計上）。popcount 7 + WIN7系verdictのみ計上。win23/win13/win6/win3/win2/win1記録はpopcount filterで除外。**uncertifiedは過大申告方向にのみ誤りうる**（リスク側に安全）。
5. ** uncertifiedのリスク階層化**: 未認証rootのreceipt entryを精査し、(a) rows+md5付きで証明書ファイルが参照されるが走査集合内に検証記録がない**level-1**、(b) 証明書アーティファクトへの参照が一切ない**level-2 (verdict-only)** を区別した。併せて全未認証rootの (band, bit) 参照をJSONに収録し、証明書抽出の直接的なターゲットリストとした。

## 結果

- **775 roots = 695 certified + 80 uncertified**。
- tier内訳: **V 241**（生の独立検証アーティファクト所持）・**R 454**（出版証明書記録・うち107 rootsはreceiptcertが唯一の証拠kind）。
- uncertified 80の内訳: **orbit被覆6**（対称性姉妹rootがcertified）・完全未被覆74。うち**level-1が6件**（すべてcost-70c warm: bits 8/11/24/40/92/105、rows 33,992〜52,755、md5付きで証明書出版済み・検証記録は走査集合外）・**level-2 (verdict-only) 74件**。
- level-2のband別集計（重複あり）: **cost65e 14** / **cost64b 11** / **cost62a 10** / **cost63a 9** / cost61e 8 / cost61d 7 / cost61f 5 / cost71b 5 / cost70c 3 / cost72 1（ほかband参照なし数件）。いずれも2026-11-14期の初期sweep lanesで、証明書pipeline整備以前のWIN verdictがwarm/multiband/unified-merge経由でhead-1452に折り込まれたもの。
- kind組合せhistogram（上位）: manifest単独263 / bigint+receipt+receiptcert 72 / verified 70 / receiptcert+manifest 48 / bareiss+receiptcert+summary+manifest 22 / bigintaudit+warmcert 16 / bigint+receiptcert+manifest 16 ほか。

## 含意

1. **80 uncertified roots（特にlevel-2の74件）が76c bit113型の簿記リスク母集団**である。fbt飽和欠陥はnode数では事前判定不能（66c bit 112の12.57M nodes非飽和 vs bit 117の3.12M nodes飽和）のため、node数による除外はできず、証明書の出版と独立検証（BigInt余因子 / Bareiss / 円方程式）が必要。level-1の6件は証明書検証の仕上げ（verify記録の出版）のみで閉じられる。
2. **v1の過少申告は58c/62a/63i/63j/65m/67d/70g/84a等のreceipts lane全体に及んでいた**（58cは33/33、63jは29/29、63iは18/18がper-entry証明書ドキュメント付き）。これらのlanesは証明書整備済みであり、head-1452折り込みの実質的な裏付けはv1が示すより強い。訂正後の未認証は古いwarm/multiband/unified-merge系列と63cdに集中する。
3. 並走のpast-lane v17再検査キュー（65n/66c着地済み・64d/64f/64g/65f/65j/76d/77e等が残件）と本censusは**互补**である: v17はengine-consistencyの簿記、証明書は数学的独立検証。level-2 rootは証明書構築が第一選択（v17再検査のみでは76c bit113型の反転を数学的に排除できない）。なおlevel-2の74件はv15/v16初期sweep由来のWIN verdictであり、76c bit113と同世代のengine出力である点でリスクはむしろ高い。
4. 本censusはhead-1452のfrontier数字を一切変更しない。solved 1452はmanifest被覆の簿記のままである。

## 保存物

- census script（v2）: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/certificate_coverage_census_head1452_20261117.py`（stdlibのみ・基底再現とprovenance完全性をassert・2回実行byte-identical確認）
- census JSON（v2）: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/n11-class2-lane-head1452-receipt-certificate-coverage-census-20261117.json`（schema `...-v2`・775 roots全件のroot_hex / tier / kinds / cert_files数、uncertified 80件のcanonical hex・orbit被覆flag・level-1/2階層・(band, bit, rows, md5) receipt参照・provenance sources、kind histogram・出所別集計・interpretation guard）
- v1はcommit `3020c5aa` で本日出版済み。v1の出力JSONは同一pathでv2に置き換わる（revision欄に経緯を記録）。

## 信頼境界

tier Rは「走査集合内に生の検証出力がない」ことを意味し、main上の当該記録自体の検証主張（verify_bit7_win7_cert.ts等のsub-roots全PASS・BigInt/Number Bareiss PASS記録）を否定するものではない。receiptcertはper-entry証明書ドキュメント（certified:true + rows + md5 + sub_roots_pass）という構造シグネチャによる計上であり、個別の証明書bytesそのものの再検証は含まない。certifiedの判定は走査した出版アーティファクト集合に対するものであり、走査集合外の追加証拠の存在可能性はcertified側にのみ作用する。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明し、REFUTED-D10はLOSS証明ではない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
