# n11 WIN8 4親行・K1096単独証明根の二手応答被覆独立第二検証（2026-11-20）

## 背景

既存の4親行二手応答被覆計画は、304個の合法初手義務のうちK1096 rootが8個、K1095 rootが2個を覆い、残り294個を147根で覆う構成だった。ただしK1095はWIN8-D10候補であって証明書ではない。計画JSONの `fixed_roots` に含まれることと、証明済み根であることを混同しないよう、K1096だけを固定済み証明根とする形に再分類した。

K1097の独立第二検証（K1102）と、WIN8証明書抽出の他root担当とは重複しない。今回は幾何・応答被覆だけを担当し、probe・抽出・receipt foldは行わない。

## 独立再導出

単一オーナー宣言ノートのpinから、K1085残余72行、K1097のWIN8候補16根・REFUTED-D10 50根、既存response-cover plan、K1096証明書・監査正本を固定した。

既存Python検証器とは別にNode.js 20.19.2で実装した。4点共円/共線は4×4整数行列式のBareiss分数なし消去、候補生成は各親行の全unordered 2点追加、D4像は直接変換した。既存検証器の逐次legal追加・24項展開はimportしていない。

## 結果

- 4親行の合法初手数: 79 / 82 / 69 / 74、合計304 obligations。
- 2点追加raw pair: 26,220、safe8 raw extension: 9,744、safe8 D4軌道: 9,490。
- K1097のWIN8候補16根との交差はK1096 rootとK1095 rootの2本。
- REFUTED-D10 50根との交差は `00000008000000003800000008100006` の1軌道。
- 既知REFUTED除外後の候補は9,489軌道。
- K1096 root `00000000000000003800000008003180` の被覆は8 obligations。証明書はSHA-256 `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c`、既存監査は18/18 PASS。今回その証明を再検証したのではなく、証明書bytes・既存監査bytes・Git blobをpin照合した。
- K1096を除く296 obligationsに対して、非固定候補9,488軌道の全てがちょうど2 obligationsを覆う。最大被覆数2なので、追加根の下界は148。
- 既存計画の147追加根にK1095候補rootを加えた148根は、296 obligationsを重複なくちょうど一度ずつ覆う。下界と構成が一致し、K1096込み149根がこの構成での最小値となる。

この再分類で、K1095を証明済み根と誤認せずに済む。149という総数は変わらないが、証明責務は「K1096のほかに148根すべてを証明する」と明確になった。

## 実行・再現

- verifier: `research/experiments/n11-win8-four-row-one-certified-root-response-cover-20261120/scripts/verify_one_certified_root_response_cover_20261120.mjs`
- output: `research/experiments/n11-win8-four-row-one-certified-root-response-cover-20261120/output/one-certified-root-response-cover-second-verification-20261120.json`
- 19/19 gates PASS。
- 同じ作業場所での再実行、別作業場所での再実行を含む3回でJSON byte-identical。
- output SHA-256: `0352b72e78d806984f1331cdc33a79f8a6f6a9dd6e822e18a216023a21479d22`。
- CT204（Node v20.19.2、4 vCPU）で単一Nodeプロセスを逐次実行。探索負荷なし。

開発時に既存response-cover READMEのplan JSON SHA-256 `633c1171…` が現物と不一致であることを検出した。raw bytesからの正しいSHA-256は `125c9746b93f65f1f48eef18628f440c264c5f7dace4e98ed32e672295a16530`。元READMEも訂正する。

## 変更範囲と限界

- K1095 rootは追加候補の1本として扱う。WIN8-D10候補であるが、証明書未抽出・未検証。
- 他147根はsafe8候補のみで、WIN/LOSS verdictなし。
- 新規DFPN probe・depth sweep・証明書抽出・receipt fold・S6 manifest/frontier更新は行わない。
- 4親行はすべてopen。S6行の閉鎖数は0。
- これは4親行の二手応答方式の幾何最小計画であり、11×11全体の勝敗や別方式の下界を示さない。

**標準11×11空盤・二石root `{49,60}`・`{59,60}`・S2 `{59,60}`・class 1/2/4はUNKNOWNのまま。**

## Knowledge構造の検査

- K1103単体: front matter・kind/status・topics・artifact role・relation target・8 artifact pathを検査し、すべてPASS。
- `uv sync --locked`: CT204にuvがなく未実行。
- `tools/knowledge/build.py`: sparse checkoutに既存項目が参照する大量のexperiment/log/artifactを含められず、broken local linkで終了。generated/ とroot READMEは変更されていない。
- `tools/knowledge/check.py`: sparse checkout由来のartifact missingに加え、既存項目のfront matter不備を多数検出して長時間実行がtimeout。全体成功とは扱わない。
- `unittest discover -s tools/knowledge/tests`: 31件中30件成功。残る1件はMigrationBoundaryTestsのsetUpClassで既存K項目のaliases欠落によりKeyError。K1103にはaliasesがあり、単体検査はPASS。
- 最新mainのsparse checkoutでK1103の8 artifactすべてが存在し、K1103自身に対するschema/relation validation errorは0。

このため生成物再構築・repo全体CIの成功は主張しない。生成物を手編集することもしていない。
