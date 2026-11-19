---
id: K1063
title: "残余78行のresolve6再照合: K0863 8,964-root全体cacheとのroot単位結合・39 dead root除外後の候補再計算（judged REFUTED 446/WIN 4・fresh-safe 4,417・pair辺667・最大matching 39・stranded 0）。cache由来4 WIN-D10 rootの残余4行被覆をpending receipt候補として出典付きで確定、39 live witness計画は78行を独立に完全被覆"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - execution of the K1059-declared resolve6 (39 dead roots excluded, full K0863 canonical verdict cache joined at root level)
  - corpus-verified rebuild of the K0863 engine map (1,272/1,279 manifest sha256 match, 133 target children exact vs published scan, 115 transfers, 0 WIN/REFUTED conflicts)
  - post-join cover re-solve of the 78 residual rows (fresh-safe 4,417, 667 pair edges, 78 singleton-eligible rows, maximum matching 39, stranded 0)
  - winCOVER windfall: 4 cache WIN7-D10 roots (cost65h child bits 40/43/99/118) cover 4 residual rows as pending receipt candidates with raw-line provenance recorded
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1057
  note: resolve5正本（SHA-256 5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e）のuniverse 7,969・残余78行・fresh-safe候補集合が本項の入力
- type: depends_on
  target: K1059
  note: 39 dead root（深さ飽和で閉鎖witnessとして永久使用不能）の除外とsweep39正本（SHA-256 f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246）
- type: depends_on
  target: K0863
  note: 正準形verdict cache体系（corpus 1,279ファイル・出版scanスクリプト・115 transfers）が結合対象
- type: depends_on
  target: K1060
  note: resolve5入力の第三方法検証済み正本群（fold記録・receipt roots chain）
artifacts:
- path: research/experiments/n11-residual78-cache-join-resolve6-20261120/resolve6.py
  role: verifier
  note: resolve6本体（stdlibのみ・決定的・repoルートから1コマンドで約25秒・2回実行byte一致）。K0863出版scanスクリプトをimportしてcache再構築、fold正本からreceipt root chainを再構築しfail-closedで全12 gate検査
- path: research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json
  role: data
  note: 再照合正本（SHA-256 e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a）。全12 gate PASS・join conflict 0・witness_full 39 live root・win_cover_detailにwindfall 4根のraw出典（bit行・pilot行・lane context・determinism再現）
- path: research/experiments/n11-residual78-cache-join-resolve6-20261120/README.md
  role: data
  note: 実験README（入力pin・結合構成・結果・決定論性・解釈規約・次の一手）
- path: research/experiments/n11-residual78-witness39-candidate-supply-scope-audit-20261120/output/candidate-supply-scope-audit-20261120.json
  role: data
  note: 事前の範囲監査（fresh-safe 4,689本/pair 667辺が残るとの予測値は本項で全て再計算され確定: fresh-safe 4,417・pair辺667。sweep39外のfresh-safeはjoin後に判定済み分を含む）
scope: >-
  K0863全体cache・post-cache掃引・published receiptをroot単位で結合した
  resolve5 universe 7,969の再照合まで。39 dead rootの除外、既知WINの残余行
  被覆の出典確定、fresh-safe候補・pair辺・最大matchingの再計算が対象。
  witnessのdepth-10掃引・4 WIN rootの証明書抽出・receipt fold・行の閉鎖・
  二石root・空盤の勝敗確定は対象外。
evidence: >-
  （1）入力: resolve5正本（SHA-256 5a2f4815…）とpublished sweep39正本
  （SHA-256 f8608d0a…）をpinとしてSHA照合。K0863出版scan JSONのmanifest
  （1,279エントリ）でcorpus 1,272/1,279のsha256一致、差7ファイルはpost-scan
  修復系（現main上に欠損・既知のgap、verdict-claimed-identical）。K0863出版
  scanスクリプトをimportしてengine mapを再構築: engine bits 8,960（出版
  8,964との差4bitは非target系）、133 target child全て出版値と分布完全一致、
  115 published transfers、WIN/REFUTED同一root衝突0でfail-closed。
  sweep6の両順序probe・全published receipt fold正本からのreceipt root chain
  再構築（global fold tarballを含む）・post-cache掃引7系統を結合。
  （2）resolve5整合: universe再構築7,969 ==出版値（gate PASS）。39 dead root
  は全て結合後judged REFUTEDに含まれる（gate PASS）。
  （3）再照合結果: universe 7,969内 judged REFUTED 446（dead 39を含む）/
  judged WIN 4 / fresh 7,519 / fresh-safe 4,417 / fresh-unsafe 3,102。
  pair辺は706（事前監査）→667に減り、78行すべてにsingleton候補が残り、
  最大matching 39・matched 78行・stranded 0。新規39本のlive witness
  計画が残余78行を1回被覆で完全に覆う（witness_fullに根・被覆行・safe
  フラグを記録）。
  （4）windfall: verdict-joinのWIN 4根（class2-lane-cost65h child
  00000000000000803202000000001000 のbit 40・43・99・118。rootは
  00000000000000803202010000001000・00000000000000803202080000001000・
  00000008000000803202000000001000・00400000000000803202000000001000）
  が残余4行を被覆。全根7石・D4正準形・unsafe 0。出典はraw batch行
  （batch3/4/7/8・loss=true・uncapped・terminalStoneRange [13,17]・
  andclose=true）とバッチ内pilot_d6対照行（3,402 nodes・loss=false）、
  lane sweep正本のwin7ビットリスト一致・bit 43は別プロセスnode-exact再現
  （3,269,824 nodes）。engineはrepo-verbatim v16 runner（depth 10・
  andclose=1・cap 1e9）。単一順verdictのためreceipt化には証明書抽出
  （child=root−最小セットビット・生整数hex）とBigInt 3x3 / Bareiss 4x4
  による独立二重検証が必須で、それまでは4行は閉鎖扱いにしない
  （39 live witness計画が78行を独立に完全被覆するため被覆簿記はwindfall
  に依存しない）。
  （5）決定論性: stdlibのみ・repoルートから1コマンド（約25秒）・2回実行で
  byte-identical（出力SHA-256 e85d4bfb…）。全12 gate PASS。
  （6）解釈規約: REFUTED-D10はLOSS証明でない。fold・被覆は行の簿記であり
  ゲーム理論的値に言及しない。witness rootは条件付き掃引計画、windfallの
  WINはpending receipt候補であり確定閉鎖ではない。stranded 0は本scopeの
  候補集合に限る観察でscope外閉鎖機構を否定しない。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**
---

## 詳細

K1059の追記が「次の一手は39 dead root除外後の再照合（resolve6: 未選択667
pair辺・fresh-safe 4,689本のK0863 8,964-root全体cacheとの結合を含む）」と
宣言した通り、事前のcandidate-supply-scope-auditの予測値（fresh-safe
4,689本・未選択pair 667辺・78 singleton候補未使用）を入力に、全体cacheを
D4正準形root単位で再構築して結合し全数値を確定した。join後の確定値は
fresh-safe 4,417・pair辺667・singleton候補は78行すべてに残存。前回監査の
記述（「4,689本が現在も全て未判定とも、別matchingが必ず残るとも主張しない」）
は本項で数値として解消された: 4,689本のうち272本（268 REFUTED+4 WIN）が
cache joinで既に判定済みであり、残り4,417本がlive candidateとして残る。

windfall 4根の被覆行は出力JSONの`win_cover_detail.evidence`にroot単位で
記録済み（engine_entriesにchild/bit/raw batchファイル名/pilot行/bit行/lane
context）。receipt foldによる閉鎖計上は証明書抽出と二重検証の後に行う
（fold機械の入力chain再構築を含む）。詳細は[実験](../../experiments/n11-residual78-cache-join-resolve6-20261120/README.md)・[研究ログ](../../log/2026-11-20-n11-residual78-cache-join-resolve6.md)。
