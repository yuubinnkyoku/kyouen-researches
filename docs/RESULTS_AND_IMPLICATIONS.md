# 結果の読み方

勝敗・全状態計算・極大配置・幾何の現在値は[knowledge](../research/knowledge/README.md)を参照してください。
ここでは結果を比較するときの注意を説明します。

盤の奇偶や最大安全配置の石数だけで空盤勝敗を決めることはできません。
合法手を選ぶ過程と到達可能な極大配置を区別して読む必要があります。
[P/NとGrundy数](../research/knowledge/items/K0002-grundy-and-first-move-conventions.md)は手番側から見た量です。
[最大と極大](../research/knowledge/items/K0026-maximum-versus-minimum-maximal.md)も異なり、
固定証明書の終局一覧は[全最適戦略のT*・WFT](../research/knowledge/items/K0295-n1-n7-full-tstar-and-wft.md)を意味しません。
T*・WFTの正本は[K0295](../research/knowledge/items/K0295-n1-n7-full-tstar-and-wft.md)です。

固定幅では[一般証明と有限検算](FIXED_WIDTH.md)、solver評価では分類精度・探索順位・実行速度の別を見ます。
旧実験の当時の判定は履歴として読むもので、現在のstatusを更新する場所ではありません。
撤回・反証・未監査の違いと未解決問題は[正本の集計](../research/knowledge/generated/summary.md)から辿れます。
