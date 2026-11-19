# n11 K1069 nodeコスト台帳の完全再導出（2026-11-20）

## 目的

K1069 39-live witness depth-10掃引は要約統計とroot→ラベル分類のみを出版しており、
per-probeのnode数台帳は非出版だった。本実験は (a) **78 probeを独自に再実行して出版済み集計の
全部（総nodes・最大probe・WIN/REFUTED数・capped・順序矛盾）を厳密再導出・照合**し、
(b) root別nodeコスト台帳を出版する。**コスト台帳と出版記録の十字検証のみ**であり、
判定・分類・行の閉鎖は一切行わない。単一オーナー宣言ノート
（`research/log/2026-11-20-n11-k1069-nodecost-ledger-single-owner-note.md`・commit b47fb91a40）の下で実施。

## プロトコル

- 対象: K1069正本（SHA-256 `22953ae1…`）classification全39根（38 REFUTED-D10 + 1 WIN7-D10）。
  (child, bit)は生child hex規約で機械再導出。
- runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・
  depth 10・cap 30M・timeout 280s・両AND順序・pilot_d6制御必須・逐次・計78 probe。

## 結果（78/78完走・capped 0・error 0・gate 10/10 PASS）

- **再導出summaryがK1069出版値と全項目で厳密一致**:
  総nodes **169,615,508**（完全一致）・最大probe **14,249,420**
  （root `00000000010000809002000040000080`・andclose0）・WIN 1 / REFUTED 38 / CAPPED 0 /
  順序矛盾 0。すなわち**出版済みdepth-10掃引の数値的実体が別環境・別実行で完全再現した**
  （K1069自体が報告したrun-to-run再現に続く三重目の大規模決定論合意、ただし本実験は
  正本の生記録を直接保持しない全数再実行による照合）。
- 出版per-probe値3件（max root ac0 14,249,420・WIN根 ac1 1,576,372 / ac0 2,544,178）厳密一致。
- depth-11標本拡張（`../n11-depth11-cost-scaling-pilot-ext-20261120/`・SHA `8a584be6…`）が測定した
  4根×両順序=8件のD10 node値と厳密一致。
- 39根のラベル整合: REFUTED-D10根は両順序loss=false、WIN7-D10根は両順序loss=true、不一致0。
- 帳簿上の観察（無害な丸め差）: 出版summaryの `avg_nodes_per_probe: 2,174,557` に対し
  169,615,508/78 = 2,174,557.79 であり、本再導出の四捨五入値は 2,174,558。出版側は
  切り捨て丸めと思われ、総和は厳密一致しているので数学的内容への影響はない。

## コスト台帳（上位と傾向）

- rootごとの両順序合計上位: `…01000000809002000040000080` 16,981,079（ac0 14,249,420 +
  ac1 2,731,659）・`…40809002000800100000` 13,014,089・`…801202040000101000` 12,001,381。
- 最小rootは 124,440 + 717,739 など、**root別のnode数は約2桁（10^5〜10^7）の幅を持つ**。
- ac0/ac1の非対称: 39根中ac0が重い根もac1が重い根もあり、順序依存の最大probe比は本台帳で
  約5.2倍（max root: ac0/ac1 = 5.22）。証明掃引の順序設計（どちらのorderingを先に走るか）は
  最大probe抑制の観点でroot別選択の余地がある。
- 完全なroot別台帳は正本JSONの `by_root`（39行）と `ledger`（78 probe行）を参照。

## 再現性

- 正本 `output/k1069-nodecost-ledger-20261120.json`（SHA-256
  `b55e5d83a0d25c06a8dcc8ffa06ce5d077bd6c225f6818423dafdf615fbf48a3`）は生probe記録
  `output/probe-records-k1069ledger.jsonl` から assemble のみで生成され、別cwd・別プロセスで
  byte-identical（2回確認）。gateは10個すべて。
- 再現手順: K1069正本とdepth-11標本拡張正本をraw取得し、
  `python3 scripts/k1069_nodecost_ledger_20261120.py assemble <k1069.json> <ext.json>`。

## 解釈規約

本台帳は出版済み判定の検証とコスト記録であり、いかなる行も閉じない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
