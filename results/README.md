# Machine-readable results

公開・横断集計のCSV/JSON、compact table、hash、証明書indexと機械出力を置きます。
現在の命題・未解決・検証境界の唯一の正本は[knowledge](../research/knowledge/README.md)です。
ここにある数値・raw logは計算時の資料で、現在のstatusを並行維持するMarkdownではありません。

- [outcomes.csv](outcomes.csv)：1〜9の共通証明書分類と探索・証明書規模。
- [10盤の完全初手分類CSV](../rust/independent-verifier/evidence-sample/10x10-first-move-classification-complete.csv)。
- [certificates.csv](certificates.csv)：証明書のノード数・サイズ・SHA256。
- [all-certificates-check.txt](all-certificates-check.txt)、[certificate-logs](certificate-logs/)：公開証明書の機械検査標準出力。
- 8/9/10盤の保存結果、cycleの横断集計と原データは既存の盤面別subdirectoryや結果ファイルにある。

実験固有の小出力は[experiments](../research/experiments/README.md)へ集約します。
従来のartifacts、rootの研究JSON、検証experimentのraw dataはexperiment/outputへ移動済みです。
results内のpreregistration・analysis Markdownと図は[solver-benchmarks](../research/experiments/solver-benchmarks/README.md)、
旧certificate logは[certificate-validation](../research/experiments/certificate-validation/README.md)にあります。
再現コード・条件・auditを同じexperimentのREADME/reportから辿ってください。
