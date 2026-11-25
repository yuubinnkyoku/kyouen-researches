# 2026-11-19 n11: 28-root witnessから第4 WIN7-D10証明書を取得

## 開始時点と候補の固定

開始時の最新mainは `e9b7882444ae2fb4c67973e6fc29f574fd176fdc`。AGENTS.md、research/knowledge/README.md、SCHEMA.md、K0863・K0865・K1029・K1033、および49-root cover・48-root sweep・28-root再解決の研究記録を確認した。branch / PRは作らず、mainへ直接反映する。

対象候補は、K1033のREFUTED除外後の再解決JSON（Git blob `600b23d39888ea0e693742da4b2ae9c372a9faf0`）にある63 eligible candidatesの28-root witness。28 rootで53行を覆う候補計画であり、証明済みの被覆ではない。元JSONのsource_main_headは `c8e974a26629a8b91662f479e1d84e10cae6ddcd` だが、現行main上の同一blobを固定して使用した。

## 実行環境と入力pin

Proxmox LXC `pve:199`（Debian 13、Node v22.23.5、Python 3.13.5、1 vCPU、4 GiB RAM）。root filesystemは100%使用済みだったため、全入力・中間物・証明書を `/dev/shm` に置いた。実行は単一プロセスで行い、並列workerは起動していない。

- runner v17: `c132cc6425eee3feaeef1d697dd74f968cfedb59`
- extractor v16: `5518d375fc6b4a7a14c22a1a65586f0c1c5731c0`
- BigInt verifier: `62b5d9413daafb172f6e10249976ee6808f7b454`
- 4×4 Bareiss verifier: `2960afabdf7c1a7012d223974b65f1423e6890da`
- 28-root cover-resolve JSON: `600b23d39888ea0e693742da4b2ae9c372a9faf0`

raw GitHubからcommit `e9b7882444ae2fb4c67973e6fc29f574fd176fdc` のbytesを取得し、4ファイルのGit blob SHA-1を照合。Nodeの構文検査も通過した。

## depth-10候補probe

全9回のrunner呼出しでpilot_d6 controlは毎回 `loss=false, nodes=3402` と一致した。

| 7石root | legal moves | 実行結果 | 判定 |
|---|---:|---|---|
| `00000000000000003800000008001021` | 52 | andclose1: 926,192 nodesで未打切りfalse。andclose0: 950k cap後、4M cap内で1,544,910 nodes・未打切りfalse | REFUTED-D10 |
| `00000000000000801202060001000000` | 53 | 両順序とも950kで打切り。4Mではandclose1: 3,294,339 nodes、andclose0: 3,953,563 nodes、いずれも未打切りtrue | WIN7-D10 |
| `00000000020000801222000000100000` | 53 | andclose1: 261,501 nodesで未打切りfalse。andclose0は950kで打切り | REFUTED-D10 |

REFUTED-D10は、その7石rootから深さ10以内の先手勝ちが存在しないという判定であり、親局面のLOSS証明ではない。2つのREFUTED rootについて、打切り側の順序を完全探索したとは扱わない。

## 第4 WIN7-D10証明書

root `00000000000000801202060001000000` は7石・D4正準・unsafe quadruples 0。合法な後手初手53手を全て列挙した。

runner v17の両AND順序で未打切り `loss=true`。extractor v16は53応手すべてを処理し、5,469,581 nodes、50,941 unique strategy rows、`fbt_drops=0`、終局石数13〜17の証明書を抽出した。

- 展開後bytes: 1,843,284
- 展開後SHA-256: `f3fcf274ee72d98f4501d104f694d679cd3301e0e161a06a22c191c89ad94bae`
- Git保存形式: 決定的gzip（mtimeなし）
- gzip bytes: 237,885
- gzip SHA-256: `f9bf9b2489f6bf656837579490d4b67956290132741ebae0f3d3ebe472ee7f91`

### 独立検査

BigInt 3×3余因子展開検査はroot安全性・mobility 53・53 subrootsを確認。証明書50,941行と消費集合が完全一致（missing=0、extra=0）。visited states 101,663、terminal 16,052、opponent reply edges 91,807、終局石数13〜17。

別実装の4×4 Bareiss検査も53/53 subroots PASS。consumed records 65,610、unique 50,941、証明書との差分0。seen 101,663、terminals 16,052、opponent edges 91,807でBigInt方式の状態流量と一致した。

このrootは28-root witness上で次の5親target残余2行に対応する。

- `00000000000000801202020001000000`
- `00000000000000801202040001000000`

## receipt・未解決範囲

今回の公開は証明書と独立検査結果まで。既存S6 manifest/frontierへのreceipt fold、親行incidenceの再計算、WIN/LOSS cacheへの統合はまだ行っていない。したがってK1033時点の簿記（solved S6 1,619、remaining S6 6,229行・cost 493,184、5親target 21/112行閉鎖・残91行）は変更しない。上記2行は「新証明書が幾何学的に対応する未閉鎖候補」であり、fold完了と読み替えない。

28-root witnessのうち、今回試した3 rootはWIN7-D10が1、REFUTED-D10が2、未試験が25。REFUTED-D10の2 rootが覆う4行は、この候補root自身のreceiptでは閉じられないが、別rootや深さ11以上の証拠の可能性は残る。38 stranded行も数学的閉鎖不能を意味しない。

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はすべて **UNKNOWN**。今回得たのは特定7石rootのWIN7-D10であり、二石rootや空盤の勝敗ではない。

## 次の作業

この証明書のreceipt行をD4全像から再導出し、K1033のopen frontierへ接続する。行の事前open性、親行incidence、既存verdictとのWIN/LOSS conflictを検査してからfoldする。その後、未試験25 rootとREFUTED rootの代替候補を含めて残余coverを再解決する。
