# Grundy・misère・残局・複体の再現

現在の結論の正本は[knowledge](../../knowledge/README.md)です。この単位は当時の実験・証明・検算の一次資料を保存します。
旧reportのSUPPORTED等は当時の判定であり、現在のstatusとして並行維持しません。

## 再現

repo rootから、Python標準ライブラリとg++（C++17/20）で実行します。

```sh
python research/experiments/game-structure/scripts/check_game_structure_20261003.py
```

既定は小盤mex再計算、9盤のprimitive検査、8盤2実装のビルドです。大盤のroot探索は実行しません。

## 資産と範囲

- [scripts](scripts/)：実験固有コード。共有solverを複製しない。
- [output](output/)：入力・raw出力・実行ログ・hash・監査metadata。ファイル名と保存条件をreportから辿る。
- [reports](reports/)：当時のpreregistration・result summary・audit・解析証明。

共有実装は[cpp](../../../cpp/)、[scripts](../../../scripts/)、[共有研究ライブラリ](../../../scripts/research/)、[Rust verifier](../../../rust/independent-verifier/README.md)を参照します。
chronologicalな発見・判断は[log](../../log/README.md)、旧統合・計画は[archive](../../archive/README.md)です。
