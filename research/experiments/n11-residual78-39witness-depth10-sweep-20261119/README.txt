# n11-residual78-39witness-depth10-sweep-20261119

K1057 resolve5 の条件付き計画（39 pair witness・残余78行完全被覆）の実行部。

## 前提（全てrepo既出版のpin）

- resolve5 正本: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json
  SHA-256 5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e
- witness 39 root: 上記JSON witness_full（39 root・covered rows の和集合 = 残余78行・matching 39）。
- runner v17: git blob c132cc6425eee3feaeef1d697dd74f968cfedb59
  （research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts）
- depth 10・cap 30M・両AND順序・pilot_d6 制御・生maxbit child（canon_hex被せ禁止・K1046事故規約継承）。

## roots.json の構成

- 各 witness root R（7石D4正準形）について、child = R − (最小セットビット b)、bit = b。
  つまり child | (1<<bit) == R を満たす分解で、R のどの石を「最後に置かれた一手」と見るかは
  probe結果に非依存であることを実験確認済み: sweep43[0] root `00000000000000003800000008001081`
  を出版時の(child,bit=61)と代替分解(child',bit=0)の両方で両順序probeしたところ、
  nodes 3,164,139 / loss=false / capped=false が完全一致した（runnerはchild+bitの
  cell集合として同一盤面を解くため分解の取り方と無関係）。
- covered rows（各2行）はresolve5のcoveringをそのまま記録。

## 実行方法

- python3 driver.py <worker_id> （probe 285s単位timeout・中断してもrecordsから再開）
- 分類組立: assemble39.py（43版assembleの件数合わせ・下記出版後に配置）
- 予算: 39 root × 2順序 = 78 probe・sweep43実績平均8.6秒/probe。

## 注意

- 39 root は全て depth-10 未判定（resolve5 gate: 前回43 witnessの39 REFUTEDは
  universe内で struck 済み、4 WIN witnessは閉鎖済み行のみを被覆）。
- 結果の解釈: WINが出たrootは証明書抽出候補。REFUTED-D10はLOSS証明ではなく、
  78行の閉鎖はWIN証明書のfoldでのみ進む。CAPPED/conflictは記録次第で再試行。

## 結果（2026-11-19 掃引完了・分類正本は output/witness-39-root-depth10-sweep-20261119.json）

- 78 probe 完走（worker0 40・worker1 38）。pilot_d6 は全 probe で合格（3,402 nodes・loss=false）。
- **WIN 0 / REFUTED 39 / CAPPED 0 / 順序矛盾 0**、総nodes 115,940,695、最大単一probe 9,930,490 nodes。
- 帰結: 78行は1行も閉じず、frontier 6,213行/492,021・solved S6 1,635・5親target 34/112不変
  （K1057 fold後のまま）。43-pair掃引のdeflation後に再結合した39 fresh pairの全滅により、
  残余78行へのadd-one-stone・depth-10レーンのfresh候補供給はこのスコープで枯渇。
- 分類は assemble39.py（生記録から独立組立・GATE: 両順序・uncapped・pilot・partition一致）。
- K1059 item / research/log/2026-11-19-n11-residual78-39witness-d10-sweep.md 参照。
- 次の選択肢: depth>10コスト測定（数rootの深さ別nodes傾向）、add-two-stones拡張census、
  残余78行の幾何構造解析、並走 n11-residual-86-row-min-cover レーンとの視点統合。
