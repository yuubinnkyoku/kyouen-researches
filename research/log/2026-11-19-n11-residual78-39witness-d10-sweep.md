# 2026-11-19 n11 長期レーン: resolve5条件付き計画の実行（39-witness depth-10掃引、WIN 0 / REFUTED 39）

## 経緯

- K1057 の最終段階（resolve5）で残余78行が39本のfresh pair witnessで完全被覆され
  （stranded 0）、「39 witnessは次回depth-10掃引の条件付き計画」として本実験は
  予備登録された（README.txt・roots.json・driver.py を先行出版）。
- 予備登録と同一セッション内で掃引を実行し完走した。

## 予備登録と分解規則

- witness 39 rootは resolve5 正本（SHA-256 5a2f4815…）の witness_full そのまま。
- driverとrunnerは既存pinをそのまま使用: runner v17 git blob
  c132cc6425eee3feaeef1d697dd74f968cfedb59（repo内 n11-s2-5960-ms5-s7-reuse-20261113）、
  depth 10・cap 30M・両AND順序・pilot_d6制御・生maxbit child。
- roots.jsonの(child, bit)分解は「child = root − 最小セットビット」とした。
  分解の取り方はprobeに非依存であることを実験確認した: sweep43 root
  `00000000000000003800000008001081` を出版時分解(bit 61)と代替分解(bit 0)の
  両方で両順序probeし、nodes 3,164,139 / loss=false / capped=false が完全一致。
  （runnerはchild+bitのcell集合として同一盤面を解くため。）
- 39 root × 2順序 = 78 probe。pilot_d6（3,402 nodes・loss=false）は全78 probeで合格。

## 結果（output/witness-39-root-depth10-sweep-20261119.json が分類正本）

- **WIN 0 / REFUTED 39 / CAPPED 0 / 順序矛盾 0**。総nodes **115,940,695**。
  最大単一probe 9,930,490 nodes。worker0: 40 probe・worker1: 38 probe、両worker完走。
- 分類はdriver書き出しの生記録（probe-records-w0/w1.jsonl・78 record）から
  assemble39.py で独立組立しGATE（両順序・uncapped・pilot・partition一致）を通過。

## 解釈と帰結

- REFUTED-D10はLOSS証明ではなく、各root がdepth-10内で先手勝ちを持たないことのみを
  意味する。したがって**78行は一切閉じず、frontier・5親targetは K1057 fold後の
  まま（6,213行/492,021・solved S6 1,635・5親target 34/112・残余78行）**。
- 構造的観察: K1057で「43 pair → 4 WIN（8行閉鎖）+39 REFUTED」のdeflation後に
  再結合された39 fresh pair が全てREFUTEDになった。**残余78行に対する
  add-one-stone・depth-10レーンのfresh候補供給は、このスコープで枯渇した**
  （全78行の被覆候補が確実に全滅した初めての波）。
- 次回以降の選択肢: (1) depth>10での再probe（まず数rootで深さ別コスト測定）、
  (2) add-two-stones拡張census（universe急増。既存blossom/ILP資産で計画、
  安全フィルタ・既知verdict結合は同規約）、(3) 残余78行の幾何構造解析
  （閉鎖にくい行の共通因子）、(4) 並走n11-residual-86-row-min-coverレーン
  （K0863系census資産）との視点統合。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 運用記録（実験事実）

- 本セッション中に実行環境のリセットが1回発生し、未出版のローカル scratch
  （sweep39予備・replica検証作業dir）を一喪失した。**repo既出版のpin
  （resolve5正本sha・runner v17 blob sha・census規約）のみから復旧でき、
  runnerの git blob sha1 照合（c132cc64…完全一致）で同一性を確認して掃引を
  実施した。**「重要証拠をrepoに置く」運用の有効性を示す実例。
- K番号: 並走レーンがfinite-field研究をK1057→K1058へ繰り下げたため、
  本項は **K1059**（K1057のfollow-upとして_relation移し直し）。
