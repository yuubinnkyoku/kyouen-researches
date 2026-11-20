# n11 WIN8 4親行・K1096単独証明根の二手応答被覆（2026-11-20）

## 目的

既存の4親行二手応答被覆計画を、**証明書が検証済みの固定根はK1096の1本だけ**とする形で独立再検証する。K1095 rootはWIN8-D10候補だが証明書未抽出なので、固定済み根には数えず、追加証明が必要な148候補の1本として扱う。

本実験は幾何・組合せ被覆の検証であり、DFPNを実行せず、候補rootに新しい勝敗判定を付けず、S6行を閉じない。

## 結果

<badge>19/19 gates PASS</badge>

| 指標 | 結果 |
|---|---:|
| 対象S6親行 | 4 |
| 合法初手数 | 79 / 82 / 69 / 74 |
| 初手義務 | 304 |
| K1096証明根の被覆 | 8 |
| K1096を除く残義務 | 296 |
| 2石追加のraw pair | 26,220 |
| safe8 raw extension | 9,744 |
| safe8 D4軌道（既知REFUTED除外前） | 9,490 |
| 既知REFUTED-D10との交差 | 1 |
| 使用可能safe8 D4軌道 | 9,489 |
| 非固定候補の残義務被覆数 | 全9,488根がちょうど2 |
| 追加根の下界 | 148 |
| 構成した追加根 | 148 |
| K1096込みの総根数 | 149 |

K1096 root `00000000000000003800000008003180` の既存証明書は1,251,923 bytes・34,529戦略行で、既存監査は18/18 gates PASS。今回の検証器は証明書・監査のSHA-256とGit blob SHA-1を照合したが、戦略木の三重検証そのものを再実行してはいない。

K1096の8義務を除く296義務について、既知REFUTED-D10を除外した全9,488非固定候補を調べると、どの候補も残義務をちょうど2個覆う。したがって追加根は少なくとも `ceil(296/2)=148` 本必要である。

構成側は、既存計画の147追加根にK1095 root `0000000800000000380000000810000a` を加えた148本。K1095 rootの2義務と147追加根の294義務は互いに重ならず、296義務をちょうど一度ずつ覆う。よって、この4親行・この二手応答方式に限った最小値は、K1096を含め149根である。

### 148追加根の証明状態

- K1095 root 1本: WIN8-D10候補だが証明書未抽出・未検証。
- 既存計画の147 root: safe8候補のみ。WIN/LOSS verdictも証明書もない。
- **148本すべてが追加証明を要する。** 被覆計画が最小であることは、各rootが実際にWIN8であることを意味しない。

## 独立再導出の方法

再現器はNode.js標準機能のみを使う。

- 4点の共円・共線判定: 4×4整数行列式をBareiss分数なし消去で計算。
- 候補生成: 各親行の空点から2点を選ぶ全26,220組を列挙し、最終8石局面の安全性を直接検査。
- D4正準化: 8変換の最小bitmask。
- 応答被覆: 8石rootのD4像が6石親行を含み、差分が2石である場合、その2点を双方の合法初手義務として記録。
- 既知WIN8候補16本・REFUTED-D10 50本はK1097正本から再導入し、4親行候補宇宙との交差を照合。
- 既存のPython検証器とは異なり、逐次合法手生成や24項行列式展開を使わない。

### 入力pin

| 入力 | SHA-256 |
|---|---|
| K1085 residual72/add-two census | `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e` |
| K1097 safe8/refuted50 refsolve | `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40` |
| 既存response-cover plan JSON | `125c9746b93f65f1f48eef18628f440c264c5f7dace4e98ed32e672295a16530` |
| K1096 certificate | `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c` |
| K1096 verification audit | `ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da` |

既存response-cover READMEに記録されていたplan JSONのSHA-256 `633c1171…` は現物と一致しなかったため、raw bytesから再計算した `125c9746…` に訂正した。

## 再現

リポジトリrootで実行する。

```sh
node research/experiments/n11-win8-four-row-one-certified-root-response-cover-20261120/scripts/verify_one_certified_root_response_cover_20261120.mjs
```

出力は `output/one-certified-root-response-cover-second-verification-20261120.json`。Node v20.19.2で同一作業場所の再実行と別作業場所での再実行を行い、3回のJSONがbyte-identicalになった。

- 出力SHA-256: `0352b72e78d806984f1331cdc33a79f8a6f6a9dd6e822e18a216023a21479d22`
- 検査: 19/19 PASS
- 再現実行: 3回、出力一致

## 解釈上の制限

1. 149根は、この4親行・二手応答・safe8候補宇宙・既知REFUTED除外という構成に限った最小値である。別の証明方式や深さを延ばした証明全体への下界ではない。
2. K1096以外の148根がすべて独立検証済みWIN8証明書になり、応答戦略をfoldして初めて4親行を閉じられる。
3. K1095はWIN8-D10候補であり、証明書ではない。残る147根もsafe8候補にすぎない。
4. receipt fold・S6 manifest/frontier更新は未実施。S6行の閉鎖数は0。
5. REFUTED-D10はLOSS証明ではない。nodes・solved数を勝敗と読まない。

**標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWNのまま。**

## 関連資料

- [K1103: 独立第二検証](../../knowledge/items/K1103-n11-four-row-one-certified-root-response-cover-second-verification.md)
- [研究ログ](../../log/2026-11-20-n11-win8-four-row-one-certified-root-response-cover-second-verification.md)
- [単一オーナー宣言](../../log/2026-11-20-n11-win8-four-row-one-certified-root-response-cover-second-verification-single-owner-note.md)
- [元のresponse-cover plan](../n11-win8-four-row-two-ply-response-cover-20261120/README.md)
