# 2026-11-18 N11 cost-16 生存曲線 k=16〜k=21 出版の検証側クロスチェック（値レイヤ + 構造レイヤ独立再導出 + k21コールド再実行）

## 背景

このセッション開始時点（HEAD `52501cad`・k=20出版）で次の拡張としてk=21を準備していたところ、並走実行が08:49にk=21拡張を出版した（commit `e3efa46a`・kill(21)=2,023,551,149,781,659,842 = 68.2146%）。重複出版を避け、検証側レーンの本来の役割である**新規出版の独立クロスチェック**に切り替えた。対象は未クロスチェックのk=16〜k=21の6出版（k13/k14/k15はcommit `8634e02d`で実施済み）。

## 1. crosscheck scriptの拡張（k13/k14/k15 → k13〜k21・21→27 checks）

`cost16_survival_k13_k14_crosscheck_20261118.py` を拡張した。2層構成で、experiment scriptを一切importしない:

- **値レイヤ（BigInt厳密演算）**: 9出版JSONのall_pass・grand total k=1..21一定（2,966,450,341,680,481,356）・kill/A_survive/B_survive単調性・marginal chain k=2..21が出版detailと全点一致・**mNをpinned aggregate（blob `31bdefdb…`）から独立照合して marginal ≤ mN**・direct再計算錨 k=4/8/10（commit `33abfdb8`のper-d-slice survive totals）・kill_A+kill_B恒等式 k=1..21・B/kill share percent・mixed k14 endpoint = B_survive(14)・reproduce anchors（k13〜k21の各出版が直前出版を reproducing）・quints出版錨 k15〜k21・**kill系列のcross-publication一貫性**（k13〜k21全JSONの全点がk21系列と一致 = 履歴書き換えなし）。
- **構造レイヤ（新規・独立実装）**: pinned phase-B aggregateから行被覆多重度分類器（3x行 or 2行2x→zero・ちょうど1行2x→b_only・無共有→disjoint）を再実装し、k16〜k21の rank root rows/membership/a_part/b_part・新pair shared/disjoint census・**全triple census C(n,3)**（352/145/63…836/314/180）・新quad census b_only/zero/disjoint=0・**5-subset全ゼロの再分類**（C(15,5)=3,003〜C(21,5)=20,349・計約90,000個を再列挙）を再導出。すべて出版構造と一致。

27 checks all PASS（local/network両モード・network 5.5秒・quints再導出込み0.2秒）。

## 2. k21出版のコールド再実行（決定論性の追加実測）

- 出版k20 scriptから **独立に機械変換でk21 scriptを再生成**した。変換途中で `quads.complete_4845 → complete_5985`（C(21,4)=5,985）の置換1件が抜けていたのを、出版k21 scriptとのdiffで計算前に検出・修正し、最終的に**出版scriptとbyte同一に収束**（独立変換の再現性）。
- 全レコードをコールド再計算: pairs 20本（58.7秒）・triples 190本（5 slice・115秒）・quads 1,140本（19 slice・約110秒）・cross 4本。**出版JSONL 1,354レコード（pair 20 + triple 190 + quad 1,140 + cross 4）と値レベルで0不一致**（sec/memo_states計時計測フィールドを除く全フィールド）。
- finalize 27 checks all PASS・二重実行byte-identical（sha256 `812f80b8…`）・**出版JSON（blob `5631e3f3…`）とbyte-identical**。
- 構造censusは出版前にpinned aggregateから独自に事前計算済みであった点も独立照明: 新pair 20〔shared 9/disjoint 11〕・新triple 190〔b_only 126/zero 43/disjoint 21〕・全C(21,3)=1,330〔b_only 836/zero 314/disjoint 180〕・新quad 1,140〔b_only 231/zero 909/disjoint 0〕・5-subset 20,349個すべて構造的ゼロ。出版と完全一致。

## 3. 供給網の確認

非出版ローカル入力 `global-candidate-roots-20261118.jsonl`（tj.load_parent が HERE/output/ から直接読む）を、3つのpinned入力（worklist CSV `2fee1d07…`・unclosability census `9c251da3…`・fold-chain ledger `e8785d50…`）から同梱の `enumerate_global_candidate_roots_20261118.py` で再生成した（6,337行・40秒・各行で cands 数 == worklist cost assert）。親構築（425 pair root）の前提がpinned入力のみから再現できることを確認。

## 解釈上の注意

生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもWIN/REFUTED verdictでもない。k=21点（68.2146%・B_survive 198,443,463,159,486,237 = 6.6896%）もSTERILE判定の需要側には何も含意しない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。

## レジューム

- rank-22以降の拡張候補（k22変換は同一パターン・K21_JSON_PIN=`5631e3f307119cdc067e7c6de24a305cd09a1109`・K21_JSON_COMMIT=`e3efa46a`）。C(22,5)=26,334個の機械確認が必要。次回の並走出版後は本crosscheck scriptのPINSにk22を追加するだけで同じ機械検証が走る。
- A/B分割のdirect再計算（per-d slice 19分/点）による第三検証は引き続き未完。
