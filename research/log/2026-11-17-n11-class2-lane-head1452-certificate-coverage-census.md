# 2026-11-17：head-1452折り込みWIN receipt root 775件の証明書被覆census — 588 certified（V 241 / R 347）・187 uncertified（完全未被覆181）を確定

開始時の最新mainは `96b323c0a2559c5feeff17835eb47ff8cc440daa`（cost65n/66c両行のv17全行再検査は並走により着地済みのため本エントリでは重複回避）。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

76c bit 113の偽陽性（fbtOR cache飽和によりWIN→REFUTEDが反転しうる engine 欠陥、証明書の独立検証が最終防壁であることの実証）を受け、**head-1452基底（canonical 1452/174/6396/506144/4669/370058）に折り込まれたWIN receipt root全体の証明書被覆**を機械照合した。「fold済みだから安全」ではなく、rootごとに証明書証拠の有無・レベルを確定し、未整備rootを優先順位付きでリスト化することが目的。

## 実施内容

1. **基底再現**: `fold_projection_head1450_tool_20261116.reconstruct()` で771 basis rootsを全assert付きで再現（入力blob pin 136/136照合）。76d/77e receipts recomputeの `totals.root_hexes` 4件（popcount 7 assert）を加え**775 roots**。
2. **provenance構築**: 775全rootを出所basis ファイル（BASE_WIN7_ONLY・class-frontier-* basis blobs・NAMED_FRONTIER・66c fold JSON・76d/77e receipts recompute）に帰属。完全性assert済み。
3. **証明書証拠スキャン**: 出力アーティファクト一式（`output/*.json`・`output/tmp-cost*/bit*.json`・`output/class2-lane-cost*-certificates/*`・69c manifest）を走査し、14種のkind（bareiss / bigint / tsverify / bigintaudit / verified / verdictverify / orbitverify / receipt / summary / certpart / manifest / warmcert / class4cert / certbacked）に分類。tier V（生の独立検証アーティファクトあり）とtier R（検証を記述する出版証明書記録）を区別。
4. **保守的スコープ**: frontier/receipt recompute ファイルはprovenanceのみ扱い（WIN言及は証明書証拠にしない）。popcount 7 + WIN7系verdictのみ計上。win23/win13/win6/win3/win2/win1記録はpopcount filterで除外。**uncertifiedは過大申告方向にのみ誤りうる**（リスク側に安全）。
5. **実装中の分類漏れ修正**: 当初のkind分類は `*win7-certificates*` 系を対象化していたが、走査から116ファイルがkind判定漏れしていることを検出。精査の結果、**warm certificate rebuilds（60b/63e/65g）・class4-batch bit記録（bit7/25/37）・warm17 BigInt independent audit・69f certificate-backed recompute** が本物の検証済み証明書記録（sub-roots全PASS・all_pass・BigInt 3x3余因子・git blob sha）であることを確認し、4 kind（warmcert / class4cert / bigintaudit / certbacked）を追加。これによりcertifiedは566→**588**に訂正（未追加なら過少申告になっていた）。

## 結果

- **775 roots = 588 certified + 187 uncertified**。
- tier内訳: **V 241**（生の独立検証アーティファクト所持）・**R 347**（出版証明書記録のみ・生検証出力は走査集合外）。
- uncertified 187のうち**6件はorbit被覆**（対称性姉妹rootがcertified）・**181件は完全未被覆**。
- kind組合せhistogram（上位）: manifest単独311 / bigint+receipt 74 / verified 70 / bareiss+summary+manifest 30 / bareiss+receipt+summary+manifest 18 / bigintaudit+warmcert 16 / bigint+manifest 16 ほか。
- uncertifiedの出所別集計（上位・重複あり）: unified-merge 37 / **58c receipts 33** / warm-multiband 33 / warm-multiband2 31 / **63j receipts 29** / **63i receipts 18** / 65m receipts 8 / 70g receipts+reconciled 7+7 / 62a receipts 6 / 68d 5 / 84a receipts 4 / merged 63h-63i-63j-65m-67d 2 ほか。

## 含意

1. **187 uncertified rootsが76c bit113型の簿記リスク母集団**である。証明書の出版と独立検証（BigInt余因子 / Bareiss / 円方程式）までは、engine verdictに依存する弱い証拠のままplanning入力に使うべきでない。fbt飽和欠陥はnode数では事前判定不能（66c bit 112の12.57M nodes非飽和 vs bit 117の3.12M nodes飽和）であるため、node数による除外はできない。
2. **receipts-recompute lanes（58c/62a/63i/63j/65m/67d/70g/84a）のWIN receiptが証明書未整備のままhead-1452に折り込まれていた**ことが確定した。単一laneとしての最大ブロックは58c（33 roots）。証明書抽出の優先順位は本censusの `uncertified_by_provenance_source` が直接与える。
3. 並走のpast-lane v17再検査キュー（65n/66c着地済み・64d/64f/64g/65f/65j/76d/77e等が残件）と本censusは**互补**である: v17はengine-consistencyの簿記、証明書は数学的独立検証。uncertified rootに対しては証明書構築が第一選択（v17再検査のみでは76c bit113型の反転を数学的に排除できない）。
4. 本censusはhead-1452のfrontier数字を一切変更しない。solved 1452はmanifest被覆の簿記のままである。

## 保存物

- census script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/certificate_coverage_census_head1452_20261117.py`（stdlibのみ・基底再現とprovenance完全性をassert・2回実行byte-identical確認）
- census JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/n11-class2-lane-head1452-receipt-certificate-coverage-census-20261117.json`（schema `n11-class2-lane-head1452-receipt-certificate-coverage-census-20261117-v1`・775 roots全件のroot_hex / tier / kinds / cert_files数、uncertified 187件のcanonical hex・orbit被覆flag・provenance sources、kind histogram・出所別集計・interpretation guard）
- 出力JSON 136,743 bytes・md5 `4d5e282007d99ecacf7c4bc4e9f945ef`

## 信頼境界

tier Rは「走査集合内に生の検証出力がない」ことを意味し、main上の当該証明書記録自体の検証主張（verify_bit7_win7_cert.ts等によるsub-roots全PASS記録）を否定するものではない。certifiedの判定は走査した出版アーティファクト集合に対するものであり、走査集合外の追加証拠の存在可能性はcertified側にのみ作用する（uncertified側は過大申告方向に安全）。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明し、REFUTED-D10はLOSS証明ではない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
