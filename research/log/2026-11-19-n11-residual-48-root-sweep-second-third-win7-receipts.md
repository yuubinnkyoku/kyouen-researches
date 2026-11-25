# 2026-11-19 n11: 残余48rootのdepth-10全面スイープ、第2・第3 WIN7-D10証明書、REFUTED除外後の5親target再解決

## 開始時点と入力固定

開始時のmainは c8e974a26629a8b91662f479e1d84e10cae6ddcd（n11: publish first residual WIN7-D10 certificate and receipt fold）。AGENTS.md、research/knowledge/README.md、K0863・K0865・K1029と、49-root残余cover・receipt foldの実験・logを確認した。branch / PRは作らずmainへ直接反映する。

sweep・fold・再解決が使う入力は Git blob SHA-1 で pin している。対象はworklist、fold-chain ledger、STERILE census、global receipt fold、cost78c/79c fold、49-root cover、mobility、runner v17、extractor v16、BigInt verifier、Bareiss verifier、そして第1WIN7 receipt foldのevidence tarball fa5f26a9（tar.gz内のfold JSONはrepo上にplain fileが存在しないため、driver内でzlib gunzip＋tar展開から読む）。一部の入力は現行main（b87a8637）の祖先である c8e974a2 時点のものだが、該当_experiment配下のblobは後続commitで変更されていないことをsha照合で確認した。

## 対象とsweep

head-1410 5親target（112行）の候補rootプールである49-root cover witnessから、第1WIN7-D10 receipt root 00000000000000821082000010800000 を除いた48rootを対象とした。runner v17、depth 10、AND順序 andclose=1/0 の双方を cap 950,000 で実行した（96プローブ）。

950kで少なくとも一方の順序がcappedとなった16rootは cap 4,000,000 に昇格（32プローブ）、4Mでも両順序cappedの3rootは cap 16,000,000 に昇格（6プローブ）。合計134プローブ、全プローブでpilot_d6 control（loss=false, 3,402 nodes）が一致した。最大は 00000000000000003800000409000000 の16M 4,893,243 nodes（未打切り loss=false で完走）。

| 分類 | root数 |
|---|---:|
| WIN7-D10 | 2 |
| REFUTED-D10 | 46 |
| CAPPED（16Mでも未判定） | 0 |
| 順序間WIN/REFUTED矛盾 | 0 |

2つのWIN rootの判定根拠:

| root | 順序 | nodes | 打切り | 結果 |
|---|---|---:|---|---|
| 00000000000000821082000000042000 | andclose1 | 665,812 | なし | loss=true |
| 00000000000000821082000000042000 | andclose0 | 935,332 | なし | loss=true |
| 00000000000000821082000000420000 | andclose1 | 875,721 | なし | loss=true |
| 00000000000000821082000000420000 | andclose0 | 950,001 | 950k cap | 未判定（反証なし） |

46 REFUTEDはすべて少なくとも一方の順序で未打切り loss=false の完全探索であり（うち25rootは両順序で完全探索）、CAPPED 0 なので48rootすべてに depth-10 verdict がついた。sweep監査（audit_residual_48root_sweep_20261119.mjs）は7チェック全pass（48rootがpublished 49-cover witness差し引き集合と一致、control全件一致、両順序950k実行、昇格は950k-capped rootのみ、順序間矛盾0、総数48、WIN rootに0-drop抽出サマリ随伴）。

## 証明書抽出と独立検査

2つのWIN rootに class4_child1_cert_extractor_exact_v16.ts を適用した。

| 項目 | 00000000000000821082000000042000 | 00000000000000821082000000420000 |
|---|---:|---:|
| 合法次手数 | 55 | 59 |
| extraction nodes | 1,234,586 | 1,648,689 |
| unique strategy rows | 34,003 | 42,896 |
| fbt_drops | 0 | 0 |
| 終局石数 | 13〜17 | 13〜17 |
| 証明書bytes | 1,225,478 | 1,547,948 |
| SHA-256 | 1af547c0772eab4f5ffb7925a732b01960ffeb7bb0f970d67ee551143b34acf5 | aad19dff25c1ee7b74b2e81f0b53f41b21977d50446a52aa9c79a2ab6457205 |

BigInt 3×3余因子展開検査は root安全性・mobility（55/59）・全 subroot PASS・証明書行と消費行集合の差分0（union missing=0 / extra=0）。4×4 Bareiss 検査も同数の subroot で全PASS（1af5.. root: seen 74,991・terminals 11,592・opponent edges 67,586・consumed unique 34,003。aad1.. root: seen 96,504・terminals 15,338・opponent edges 87,272・consumed unique 42,896）。両方式の状態流量が完全一致し、cross-method agreement を確認した。証明書行の重複は両root内0（行集合の disjoint 性も全d4像から再導出で確認）。

## receipt fold

第1WIN7 receipt foldがchainしているfrontier（unique remaining S6 6,236行 / 残cost 493,703 / solved S6 1,612）に対し、今回の2 receiptをfoldした。全gate（base frontier再計算、第1fold chain、receipt行の8 d4像再導出、target行のpublished 49-cover一致、receipt行の事前open性、二rootのBigInt+Bareiss二方式独立検証、cross-method state-flow、receipt行disjoint、WIN/LOSS conflict）がpass。

| frontier項目 | fold前 | fold後 |
|---|---:|---:|
| solved S6 in manifest | 1,612 | 1,619 |
| unique remaining S6 | 6,236 | 6,229 |
| remaining S5 orbit | 173 | 173 |
| remaining cost | 493,703 | 493,184 |
| parent row incidence | 11,876 | 11,859 |

閉じたS6行は7行（edge cost合計519）。うち5親target内は4行: 00000000000000821082000000002000・00000000000000821082000000004000（第2receipt root）と 00000000000000821082000000008000・00000000000000821082000000400000（第3receipt root）。完全閉鎖されたparentは0、影響parentは9個。

solved S6 1,619 はmanifestのreceipt bookkeepingであり、勝敗確定数ではない。

## REFUTED除外後の5親target再解決

sweepで49-root witnessのうち46本が REFUTED-D10、3本がWIN receipt（第1+第2+第3）、既知verdict 5本 refuted になったことが確定したため、117root候補プールの需要を再解決した（audit_refuted_excluded_cover_resolve_20261119.mjs、8チェック・root監査全pass）。

| 段階 | 行数 |
|---|---:|
| 5親target総行 | 112 |
| 既存receiptで閉鎖済み（global 13 + cost78c/79c 2 + 第1WIN7 2） | 17 |
| 第2・第3WIN7 receiptで追加閉鎖 | 4 |
| 累計閉鎖 | 21 |
| 残余行 | 91 |
| 残余行のうちプール63候補でカバー可能 | 53 |
| stranded（どの残余候補でもcover不可） | 38 |

プール内訳: refuted 51（既知5+sweep46）+ WIN 3 を除外した残り63候補（うち3本は自身の残余行が既に閉鎖済みのためzero-residual）。残余91行のcoverage graphは pair edge 44・singleton適合行14で、Edmonds blossom による厳密最大マッチングは25（50行分）+ singleton対応3行 = 53行を28root witnessで覆う（lower bound 46）。witness 28rootは refuted/win除外後の実効pool上で初めて計算可能になった実効値であり、sweep前の推定ではない。

stranded 38行は「この117root候補プール内のいかなる残depth-10 WIN7候補（各行のd4像候補に一致する7石root、span≤2）でも閉じられない」を意味する。数学的に閉じられないことの証明ではなく、候補生成の拡張（別のparent構成・別の削除ビット）、depth 11+ の探索、または別の閉鎖機構が必要である。stranded 38行のhex一覧は cover-resolve JSON に全文を記録した。

## 結論と境界

- 残余48rootの depth-10 verdict が全面確定し（WIN 2 / REFUTED 46 / CAPPED 0）、第2・第3のWIN7-D10戦略証明書を2方式の独立検査で確定・出版した。
- 5親targetは累計21/112行、frontier は6,229行/493,184となった。
- 残る91行のうち53行は witness 28root の実際のsweepで depth-10 閉鎖が可能な見通し、38行は当該プールでは stranded と確定した。
- REFUTED-D10 は「その7石rootから depth-10 内に先手勝ちなし」の完全探索証明であり、それ以前の局面のLOSS証明ではない。
- verdict joinは明示的ソース（published verdict index 236 REFUTED/156 WIN の再現 と 今回sweep・3 receipt）限定であり、8,964件全verdict cacheの完全joinではない。
- 標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はいずれも **UNKNOWN** のままである。

## 次の一手

1. 再解決 witness 28root（53行分）を優先的に sweep する。残余91行は53 coverable + 38 stranded に完全二分されるため、witness sweepが全てWINなら5親targetは74/112行、全てREFUTEDなら21/112行から候補プール拡張の検討に移る。
2. stranded 38行は候補root生成の拡張か depth 11+ の探索が必要。stranded行のparent需要（c1/c2/c4）分析を優先する。
