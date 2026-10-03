# 現在の知識

`items/Knnnn.md` が現在の知識の正本。過去の研究記録は出典として残す。
命題の証明・再検証が増えたら同じ項目を更新する。反証した命題は残し、異なる修正版は別項目にする。
有限計算の支持を無界命題の証明に昇格させない。未監査と数学的未解決も区別する。

- [項目・topic一覧](generated/index.md)
- [解決状況](generated/solutions.md)
- [旧ID逆引き](generated/aliases.md)
- [artifact逆引き](generated/artifacts.md)
- [関係一覧と逆リンク](generated/relations.md)
- [集計・未解決・警告](generated/summary.md)
- [schema](SCHEMA.md) / [語彙](VOCABULARY.yaml) / [template](templates/item.md)
- [移行範囲と残件](../MIGRATION.md)

## 現在の研究を読む順序

まず[規則](items/K0001.md)、[Grundy・勝敗の定義](items/K0002.md)、[解決段階の区別](items/K0003.md)を読む。
「計算済み」「証明書を検査済み」「全安全局面を分類済み」は別の情報として扱う。

- 正方形盤: [1〜6の全Grundy](items/K0004.md)、[7の全Grundy](items/K0005.md)、[8の全DP報告と監査留保](items/K0006.md)、[9の全81初手](items/K0021.md)、[10の全100初手と検証境界](items/K0022.md)、[11の厳密列挙と未確定勝敗](items/K0023.md)。空盤勝敗と全局面分類の一覧は[生成表](generated/solutions.md)。
- 証拠の信頼境界: [AND/OR方式](items/K0007.md)、[C++独立検査](items/K0008.md)、[Leanの一般的健全性](items/K0009.md)、[KYOENC4の範囲](items/K0010.md)、[Rust・CSV検査の範囲](items/K0280.md)。[10の空盤全体を覆う単一証明書](items/K0103.md)と[巨大証明書のLean内具体検査](items/K0102.md)は未完了。
- 固定幅・ルール変種: [条件付き一般定理](items/K0024.md)、[q>2w](items/K0025.md)、[標準ルールの十分な高さ](items/K0068.md)、[2行の全高さ](items/K0069.md)、[q=6・幅3](items/K0070.md)、[q=5・幅3の留保](items/K0071.md)、[整数座標の合同式による拡張](items/K0072.md)。
- 最大と極大: [定義](items/K0026.md)、[最大安全サイズ](items/K0029.md)、[小盤面の極大サイズ分布](items/K0030.md)、[7の最小極大](items/K0031.md)、[10の最小極大の境界](items/K0034.md)、[10の最大安全の境界](items/K0035.md)。[最適終局T*とWFT](items/K0295.md)は固定証明書の終局一覧とは異なる。
- 幾何と配置構造: [禁止4点組の個数](items/K0057.md)、[共線4点組の漸近式](items/K0054.md)、[共円4点組のオーダー](items/K0056.md)、[被覆の上界](items/K0107.md)、[最小極大の一般下界](items/K0106.md)、[素数盤の構成](items/K0095.md)、[整数放物線の有限検査と未解決の一般化](items/K0097.md)。
- 7の結晶と再配置: [全16最大配置](items/K0051.md)、[占有骨格の分類](items/K0268.md)、[容量12での成分](items/K0270.md)、[第4隅が必須なゲート](items/K0271.md)、[静的集合Uの幅11](items/K0272.md)。[G11での全最大成分連結](items/K0282.md)は未解決。
- 探索実験: [監査済みcache-aware再現](items/K0090.md)、[旧固定median規則の撤回](items/K0086.md)、[ASCの限定的再現](items/K0284.md)、[staged分類器](items/K0285.md)、[実solver速度の不成立](items/K0286.md)。分類精度を速度改善に読み替えない。

重要な反証には[2n−1予想](items/K0027.md)、[勝者が常に終局サイズを固定できるという予想](items/K0050.md)、[5の最適終局から5を除く旧主張F-Y](items/K0296.md)がある。
[11の旧勝敗主張](items/K0028.md)は根拠撤回であり、反対の勝敗を証明したわけではない。
数学的未解決・要監査・量化範囲不明は[集計](generated/summary.md)で分けて列挙する。

rootのuv環境で実行する。

```sh
uv sync
uv run --locked python tools/knowledge/check.py
uv run --locked python tools/knowledge/build.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
```

生成物はGit管理するが直接編集しない。CIは再生成後の差分を検出する。
原文監査索引の旧SUPPORTED/REFUTEDを機械的に採用せず、量化範囲と根拠を本文に記す。
