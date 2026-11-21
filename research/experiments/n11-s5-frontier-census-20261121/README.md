# n11 S5 frontier census・グローバルcache union監査・reconciliation測定（2026-11-21）

単一オーナー宣言: `research/log/2026-11-21-n11-s5-frontier-census-union-audit-single-owner-note.md`（14:42Z・宣言時HEAD `a423c2f0`、測定スナップショットbase `0a76535f`）。

## 範囲

**測定レーンである。** game search・証明書作成・cache merge・quarantine rehab・判定主張のいずれも行わない。標準11×11空盤・二石root {60,27}・第三手100/108は本実験の後も UNKNOWN のまま。

本実験が答えるのは3つの測定問いである:

1. 現行のreply27 S5 merged chain（Nov 21の13 probe）は過去のpublished corpusと比べて何を含み、何を含まないか。active候補クラスのclosureに必要な供給と距離はどう分布するか。
2. repo内の全s5verdict cacheファイル（snapshot `0a76535f` 時点・326ファイル）のunionに矛盾はないか。
3. 現行chainが意図せず除外した歴史published行（backward-only行）は何で、採用したなら closure 状態はどう変わるか。

## 入力（すべてpublished・SHA-256はスクリプト内でpin）

- `research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz`（sha256 `146be80b…100b54`）・同 `history.json`・同 `historical-cost-profile.json`
- `results/n11-s5-evidence-quarantine.json`（sha256 `81d23160…d17fe9`）と `research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py`（quarantine鍵集合の正規源）
- reply27 S5 JS-replica merged chain: probe-1 `…merged-exact-s5-after-js-probe-1.cache`（5,744行・`6ab46ac6…`）〜 probe-13 `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache`（5,756行・`60e0dc34…`、出版ピンと一致）
- focus-class S5 probeレーンの宣言35鍵（published宣言ノート）
- snapshot `0a76535f` 時点のtree上の全s5verdict cacheファイル（326ファイル。**本監査の入力スコープはこのtree時点で固定**。push時点の最新main `a423c2f0` との差分はfour-row q4宣言ノートのみでs5verdict cacheの増減なし）

## 方法

- `scripts/census_closure.py`（sha256 `81619dcf…`）: chain 13段の形式検証（行数・挿入鍵・strict sort・sha pin・verdict一貫性）、active候補クラスのclosure距離表、供給degree分布、quarantine blocker検査、focus宣言35鍵の3点検証。
- `scripts/audit_global_union.py`（sha256 `417caa5b…`）: 326ファイル・760,504行の全走査。ファイル内同一鍵verdict矛盾・グローバルWIN/LOSS衝突・quarantine鍵の所在を検査。
- `scripts/reconciliation_findings.py`（sha256 `4c613743…`）: backward-only行の特定・帰属・if-adopted差分・再計算費用、published probe raw（2M/15M）によるproxy較正。入力のchain cache shaとunion audit出力shaをpin。

検証: 3スクリプトとも fresh 2回実行で output byte 一致（決定性）。`py_compile` 全PASS。**負対照**: chain cacheの1行のverdictを反転してcensusに与えると verdict 一貫性ゲートが rc=1 で即時fail（fail-closed確認済み・原状復元後 pin sha一致を再確認）。

## 結果

### 1. reply27 JS-replica chain 13段検証: PASS

probe-1（5,744行・LOSS 5,586/WIN 158）から probe-13（5,756行・LOSS 5,598/WIN 158）まで、12段すべての差異は挿入1行のみ（挿入鍵は `output/census-closure.json` の `chain_verify[].inserted_keys` に段階ごと記録）、行削除なし、全段 strictly sorted、probe-12（`0e4016ae…`）・probe-13（`60e0dc34…`）は出版ピンと sha 一致。quarantine清浄。

### 2. closure距離表・供給（現行chain基準・scheduling測定であって判定ではない）

- active候補クラス: UNKNOWN 62 / WIN 53。active unknown S5供給は unique 4,562鍵（単一live親 2,688 / 複数live親 1,874）。
- closure距離表の首位は focus class `1188950301626859520:536870912`（93 unknown・うちfocusレーン専有35・共有58・children 109・LOSS 16・WIN 0）。次点 `1152921504612089856:536870912` と `1297036692683752448:0` が99。
- 単一live親のうちfocusレーン宣言済み35鍵を除く claimable pool は 2,653鍵、最安 min-child proxy 5,041,584.58。
- quarantine blocker: 供給・全62クラスとも 0。
- focusレーン宣言35鍵の機械的3点検証: 35検出・欠落0・余分0・proxy band multiset 一致（5,234,938.34×22 + 5,932,111.75×13）。

### 3. グローバルunion監査: 矛盾ゼロ

326ファイル・760,504行・unique 5,866鍵。**ファイル内verdict矛盾 0・グローバルWIN/LOSS衝突 0**。5,705鍵は全出現箇所でLOSSのみ、161鍵はWINを少なくとも1箇所で含む。quarantine 2鍵（`10448351135499552768:128`, `1152925911243358208:536870912`）は歴史ファイル群にのみ存在し、現行chainには不在（現行active供給への再流入なし）。

### 4. reconciliation: backward-only 108行の特定（判定はしない・オーナーへの付託）

現行chain（5,756行）にもquarantineにも存在しないが、過去のpublished exact/merged cacheに存在する行が108行（**107 LOSS + 1 WIN**）。出所は `n11-s4-boundary-direct-20261012`（Oct 12完了corpus・final cache 5,851行・`c469eff0…`）と `n11-reply27-20more-20261011`・`n11-reply27-next-candidate-20261011`・`n11-reply27-next-class-1188950301626859520-536870912-20261010`・`n11-reply27-ten-loss-20261011`。**108行すべてが現行active供給（62 live候補クラスの子）に属する。**

クラス別の内訳（if-adopted減算、採用はしない）:

| live class | backward-only行数 | 備考 |
|---|---|---|
| `1297036692683752448:0` | 99 | Oct 12実験の完了corpusそのもの（106 canonical S5子全LOSS→クラスLOSS）。**K0414（status: computed「二石root {60,27}は元先手固定視点でLOSS」）のsolver-trusted系譜が依存する決定クラス** |
| `1188950301626859520:536870912`（focus class） | 9 | WIN行 `1188950301626859520:603979776`（K0374 S6 universal closure由来・K0379独立生raw再構成published）を含む |
| `1152921504606852096:536870912` | 2 | |
| `1297036692683751424:32768` | 2 | |
| `1297107061427929088:0` | 2 | |
| `1152921504606851584:536870912` | 1 | |
| 残り19 class ×1ずつ | 19 | `1152921504607895552` 系6・`1152921504607…` 以降の系5・`1297036692683751424` 系8。全25 class・減算合計134。減算合計が108行を超える分は共有鍵の複数live親への重複計上 |

*（全108行の鍵・出所cache・verdict、全62 live classの減算明細は `output/reconciliation-findings.json` 収録。）*

採用仮定（if-adopted・**本レーンは採用しない**）: 候補分布は {LOSS: 1, UNKNOWN: 60, WIN: 54}、第三手 {100,108} が再度被覆され、focus classはUNKNOWN→WINに変わる。degree分布は {1: 2,688→2,671, 2: 1,874→1,755}。108行を一から再探索する場合のproxy費用合計概算は 594,074,563 nodes（採用の代わりに再計算する際の参考値）。

**系譜上の論点（本レーンは判定しない）**: Nov 21のreply27ブート（two-target design Oct 10時点の5,741/5,743行ベースから再開）はこのOct 11〜12 corpusを基底から除外しており、K0414のsolver-trusted系譜と現行レーンのstatus guard（UNKNOWN維持）は矛盾したまま共存している。歴史行は自前のtrust labelを持つ（S6-split WINはK0374/K0379の再構成、LOSS行はOct 11〜12の実験batch）。**採否の判定は証拠オーナー（reply27 two-targetレーン・focus-classレーン・K0414/K0416系譜所有者）に付託する。**本測定は判定材料の整備のみを行う。

重複測定（二重計算防止）: focusレーン宣言35鍵との重複 7鍵（WIN鍵 `1188950301626859520:603979776` を含む）。reply27 13 probe target との重複 0。

### 5. proxy較正

published probe raw（13 probe各2M/15M + two-target design 2M/15M×2鍵、計42行）のうち、2M段階の15行は全てUNKNOWN（budget切れ）、15M段階で決着した27行（全て result=2=LOSS; 内訳: 12 probe×2 run + probe #1×1 + two-target×2）について nodes/proxy 比は min 0.698 / mean 1.347 / max 2.490。15M打ち切り完了proxyの設計と整合する実測較正である。全行明細は `output/reconciliation-findings.json` の `proxy_calibration.rows`。

## 再現手順

```
python3 scripts/census_closure.py
python3 scripts/audit_global_union.py
python3 scripts/reconciliation_findings.py
```

依存はPython標準ライブラリのみ。全入力はrepo内publishedファイルのSHA-256 pin（不一致は rc!=0 で fail-closed）。実行順序は census → audit → reconciliation（最後のスクリプトは前2出力のshaをpinする）。

## 解釈規約

- nodes数・proxy・closure距離・unknown数は **scheduling測定であり、いかなる局面の勝敗でもない**。
- 本実験はいかなるS5/S4/rootの判定も主張しない。cacheへの書込・merge・quarantine rehabは行わない。
- **標準11×11空盤・二石root {60,27}・第三手100/108は本実験の後も UNKNOWN。**
