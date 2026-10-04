# 再現可能な実験の入口

現在の結論・status・未解決問題の唯一の正本は[knowledge](../knowledge/README.md)です。
ここではpreregistration、実験固有コード、固定入力、raw出力、実行ログ、独立検算、hash/auditを研究単位の近くに保存します。
実験reportは当時何を得たかの一次資料で、現在の結論を並行更新しません。

| 実験単位 | 内容 |
|---|---|
| [fixed-width](fixed-width/README.md) | 固定幅q点版・厳密閾値 |
| [geometry](geometry/README.md) | 格子円・strip・分母・漸近の独立検算 |
| [game-structure](game-structure/README.md) | Grundy・misère・残局・複体の再現 |
| [saturation](saturation/README.md) | 最大・極大安全配置の証人と有限排除 |
| [structural-discovery](structural-discovery/README.md) | 小盤面・最大配置・骨格・再配置の対照実験 |
| [original-claims](original-claims/README.md) | 600原文仮説の有限検算・証人・round別監査 |
| [n11-search-methods](n11-search-methods/README.md) | 11盤の探索方式・memo・frontierの既存実験 |
| [fact-discovery](fact-discovery/README.md) | 10盤を含む探索的列挙と事実発見 |
| [solver-benchmarks](solver-benchmarks/README.md) | 9/10盤solverのprobe・memo・順位・速度対照 |
| [8x8-replication](8x8-replication/README.md) | 8盤O層の事前登録・独立replication |
| [9x9-factorial](9x9-factorial/README.md) | 9盤pair/mobility factorialの設計・監査・実行記録 |
| [certificate-validation](certificate-validation/README.md) | 公開証明書の独立検査実行記録 |
| [structural-lemmas-2026-10-02](structural-lemmas-2026-10-02/README.md) | 3手情報・二次構成・有限パスの独立replication |
| [9x9-factorial-execution-base](9x9-factorial-execution-base/README.md) | 9盤factorialの固定入力・manifest |
| [9x9-pair-mobility-confirmatory](9x9-pair-mobility-confirmatory/README.md) | 9盤pair-mobilityのconfirmatory bundle |

共通solver/verifierはcpp・scripts・rustに置きます。[共有研究ライブラリ](../../scripts/research/README.md)は実験間で使用する整数幾何を保持します。
公開横断集計は[results](../../results/README.md)、発見過程は[log](../log/README.md)、旧索引と計画は[archive](../archive/README.md)です。
hash付きの旧監査は当時のpathを保持します。[移行のprovenance説明](../archive/physical-ssot-2026-10-04/README.md)とpath対応表から現在の資料を辿ってください。
