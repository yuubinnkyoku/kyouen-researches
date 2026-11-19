# 2026-11-20 n11 K1069 nodeコスト台帳の完全再導出（78 probe全数再実行）

## 着手判断

単一オーナー宣言ノート（commit b47fb91a40・先行出版）に従い実施。K1069は要約統計と分類のみ
出版しておりper-probe node台帳が無かった。供給判断（root別コスト分布・順序設計・depth延長見積）
に必要であり、出版済み判定の全数再実行照合として独立に価値がある。36-root fresh witness掃引
（掃引オーナー実行中・結果未出版）とは無関係の出版済み39根のみを対象とし、他レーンと衝突しない。

## 方法

K1069正本（SHA-256 22953ae1…）のclassification全39根を生child hex規約で(child, bit)再導出し、
runner v17固定コピー（git blob c132cc64…）・depth 10・cap 30M・timeout 280s・両AND順序・
pilot_d6制御必須・逐次で78 probe全数を再実行した（sandboxで総nodes 169.6M、逐次実行約7分）。

## 結果（78/78完走・capped 0・error 0・gate 10/10 PASS）

- **再導出summary: 総nodes 169,615,508・最大probe 14,249,420（root …08002000040000080 ac0）・
  WIN 1・REFUTED 38・CAPPED 0・順序矛盾 0。K1069出版summaryと全項目で厳密一致。**
  出版済みdepth-10掃引の数値的実体が別環境の全数再実行で完全再現した。
- 出版per-probe pin 3件厳密一致（max root ac0・WIN根 ac1/ac0）。depth-11標本拡張正本
  （8a584be6…）のD10測定8件とも厳密一致。39根ラベル整合0不一致。
- 無害な丸め観察: 出版avg 2,174,557は169,615,508/78=2,174,557.79の切り捨て。総和は厳密一致。
- コスト分布: root別両順序合計は 10^5後半〜1.7×10^7 の約2桁幅。順序非対称の最大probe比は
  約5.2倍（max root）。root別台帳（by_root 39行・ledger 78行）を正本JSONとして出版。

## 供給判断への含意（提案・実行はしない）

- root別node数が出揃ったことで、証明掃引のworker負荷平準化・順序選択・depth延長見積が
  台帳ベースで計画できる（例: 大型rootのac0/ac1別配置）。
- 出版経路の本掃引が全REFUTEDだった場合、同規模のdepth-11再掃引の総コストはdepth-11測定
  （倍率バンド1.0004〜1.0587）と合わせて 169.6M×(1+6%) ≈ 180M nodes 程度と見積もできる。

## 成果物

- `research/experiments/n11-k1069-nodecost-ledger-20261120/`（README・scripts・output・
  runner固定コピー・生probe記録78行）
- 正本 `output/k1069-nodecost-ledger-20261120.json`（SHA-256
  b55e5d83a0d25c06a8dcc8ffa06ce5d077bd6c225f6818423dafdf615fbf48a3）は別cwd・別プロセスの
  assembleでbyte-identical（2回確認）。

## 解釈規約

本台帳は出版済み判定の検証とコスト記録であり、行を閉じず、判定を変えない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
