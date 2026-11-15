# 2026-11-15: published fold-chain全root監査v1系(第一独立実装)の80d endpoint追従拡張 — pins 99・587 roots・canonical line 1305・bit-78簿記統制・8 endpoint heads

開始時状況: canonical head **1305/6542/516793/4812/380516**(cost-80d receipts fold・head JSON blob `289c9337`)。同日の第二独立実装v4拡張([v4 log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-second-independent.md)・全統制PASS)に続き、第一独立実装(v1系・`audit_published_chain_roots_independent_20261115.py`・v3拡張済み: endpoint 75d/1296・95 pins・569 roots)を**cost-80d/1305 endpointまで追従拡張**した。両実装は別々の開発系統で書かれた独立実装であり、同一のpublished corpusに対して同一の統制を異なる実装で満たすことが相互検証になる。

## 成果1: v1系corpusを80d endpointまで拡張 — 全統制PASS

v1系scriptに以下を拡張:

- **git blob pins 95→99**: cost-77d(`d19c96b7`)・merged 75d+77d(`97130384`)・cost-79a(`7dea99ff`)・cost-80d(`289c9337`)の4 head JSONをPOST70E_PINS/ORDERに追加(26 base + 52 chain + 21 post-70e)
- **root inventory 569→587**: own_claimに77d lane-local 577(565+12)・merged 580(569+11)・79a 583・80d 587、own_baselineに77d→77c・merged→75d・79a→merged・80d→79aのfork topologyを追加し、document-order累積・own-branch累積とも**587**でpublished claimと一致
- **D4 orbit構造**: 587 roots / **576 distinct orbits / 11 twin pairs**(twin pair数不変)
- **head arithmetic 73 heads・anomalies 0**: 4新headはいずれもbaseline quote matched(77d→77c 1290・merged→75d 1296・79a→merged 1302・80d→79a 1304)、quote erratumは既知の70f 1件のみ
- **CANONICAL_LINE +3エントリ**: merged 75d+77d(key `cost77d_addition`・11 receipts・75d receiptsの再掲なし)・79a・80dを追加し、**canonical line 1233..1305: mim総和72 = distinct 72 = 1305-1233・multi_claims 0(exactly-once)**。lane-local 77d head(1299)はcanonical line外

出力: [v1系v4 audit JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-v4-20261115.json)(**AUDIT PASSED**・schema v4・2回実行byte-identical・md5 `1156db7d…`・95,881 bytes)。**v3出力JSON(`class2-lane-published-chain-roots-independent-audit-20261115.json`)はpublishedのまま無傷**(raw CDN照合済み)で、v4出力は`supersedes`フィールドで関係を明記。

## 成果2: bit-78重複rootのexactly-once簿記統制(第二実装と同一の統制を第一実装でも新設)

第二実装v4で見つけた逐次marginal規約の統制をv1系にも実装:

- **root同一性**: 77d bit-78 root `00000000100040801202000000200000` == 75d bit-92 receipt root(raw-hex完全一致)
- **covers**: 同一rootのdeletion orbitは77d childと75d childの両軌道をカバー
- **逐次marginal規約**: 同一root・同一1290 baselineでも両headのmarginal recordは1行ずつ異なる(publication orderの逐次差分。77dはbit-7が先に77d childを閉じ、75dはbit-12が先に75d childを閉じる)。両recordは共有hex `00000000000000003800400008004000`で一致し、mimはどちらも2
- **canonical line上のclaim源**: bit-78 recordの2 manifest marginalsはcanonical line上でどちらも75d headからちょうど1回ずつclaim(bit-92とbit-12)
- **inventory**: bit-78 rootは75d経由でちょうど1回inventory入り、77d再掲は新規root 0(77dの新規rootは11)
- **merged receipts**: 11 == 77d receipts minus bit-78

第一・第二両実装が同一の実験的事実(逐次marginal規約)に到達し、同一の統制で検証した。

## 成果3: endpoint heads 4→8 — 77d/79a/80d claim・merged merged_fold crosscheck

- **ENDPOINT_CHECKS +3**: 77d(1299/6548/517249/4818/380972・receipts 12・child bit-7・13,128 bytes)・79a(1304/6543/516873/4813/380596・receipts 3・child bit-9・7,452 bytes)・80d(1305/6542/516793/4812/380516・receipts 4・child bit-48・8,033 bytes)。各completed claim(`class2-lane-cost{77d,79a,80d}-inflight-20261115.json`)のfold記録とpublished head JSONをblob sha + bytes照合
- **merged 75d+77d headのcrosscheck(新形式)**: merged foldのclaimは77d claim JSONの`merged_fold`レコードに存在(独立claimファイルなし)。merged head(1302/6545/517025/4815/380748・receipts 11・child closure不主張・`child_already_closed_by: cost-75d bit-92 (cross-cover)`)と`merged_fold`(before 1296→after 1302・excluded bit-78・head JSON `97130384` + 12,460 bytes)のbyte-exact照合を確認

## 第一・第二実装の数値完全一致

| 統制 | v1系v4(今回) | v4第二実装(同日) |
|---|---|---|
| pins | 99(26+52+21) | 95(26+52+17)※ |
| roots/orbits/twins | 587/576/11 | 587/576/11 |
| receipt records / anomalies | 464 / 0 | 464 / 0 |
| arith heads / anomalies | 73 / 0 | 73 / 0 |
| canonical line | 1233..1305・72/72/multi 0 | 1233..1305・72/72/multi 0 |
| bit-78 root | `00000000100040801202000000200000` | 同一 |
| convention-external | 1(既知75c) | 1(同一) |

※pin数の差はv3時点のpin範囲の違い(v1系v3は77b/77c/75dを先にpin済み、第二実装v2は75dまでで91)によるもので、監査corpusのendpoint(80d・587 roots)は両者同一。

## 解釈境界(重要)

- solved 1305はmanifest被覆の簿記であり、いずの局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1305**。並走laneのcost-82c等、80d以降のfoldにも同じ拡張パターン(pins追加・own_claim/own_baseline・CANONICAL_LINE・ENDPOINT_CHECKS)で両実装を機械追従できる。
- 次回のfold着地後は両系統(v1系v4・第二実装v4)を同時に追従させることで、published fold-chain全root監査の双実装相互検証体制が定常化する。

詳細: [v1系拡張script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_independent_20261115.py)、[v1系v4出力JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-v4-20261115.json)、[第二実装v4 log(同日)](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-second-independent.md)、[v3監査(第一実装・75d endpoint)](./2026-11-15-n11-published-fold-chain-roots-independent-audit.md)。
