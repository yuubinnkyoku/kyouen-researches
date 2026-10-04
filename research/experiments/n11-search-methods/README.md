# 11盤の探索方式・memo・frontierの既存実験

現在の結論の正本は[knowledge](../../knowledge/README.md)です。この単位は当時の実験・証明・検算の一次資料を保存します。
旧reportのSUPPORTED等は当時の判定であり、現在のstatusとして並行維持しません。

## 資産と範囲

- [scripts](scripts/)：実験固有コード。共有solverを複製しない。
- [output](output/)：入力・raw出力・実行ログ・hash・監査metadata。ファイル名と保存条件をreportから辿る。
- [reports](reports/)：当時のpreregistration・result summary・audit・解析証明。

共有実装は[cpp](../../../cpp/)、[scripts](../../../scripts/)、[共有研究ライブラリ](../../../scripts/research/)、[Rust verifier](../../../rust/independent-verifier/README.md)を参照します。
chronologicalな発見・判断は[log](../../log/README.md)、旧統合・計画は[archive](../../archive/README.md)です。

複数roundの対照実験は共有する入力や内部module importを持つため、この単位内でコードを集約しています。各実行の条件・CLI・入力・保存範囲はreportとscriptの引数に従います。古いWSL runnerには当時の外部build/cache条件が残るものがあり、汎用再現runnerとして無条件には実行しません。
