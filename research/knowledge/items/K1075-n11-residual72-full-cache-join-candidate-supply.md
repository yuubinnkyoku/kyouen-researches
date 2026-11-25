---
id: K1075
title: "残余72行のresolve6-verbatim full cache join候補供給再構築: stage-1がpublished resolve6正本と全数値一致・新規判定ちょうど39 root（WIN 1二重出典+38 REFUTED）衝突0・universe 7,448（judged WIN 0）でfresh-safe 4,109・最大matching 36が残余72行を完全1回被覆（stranded 0・全行singleton候補・1行最少52本）・windfall型第18証明書候補0根・既receiptの追加被覆0行・retire後38 live根の38/38がopen行被覆のままREFUTED-D10（resolve7の供給ゼロを行単位裏付け・34×2+4×1割当の幾何独立再検査PASS）"
kind: computation
status: computed
topics: [residual-games, search-methods, statistics]
aliases:
  - candidate-supply rebuild over the residual 72 rows (resolve6-verbatim corpus/join/universe rebuild, single-owner lane)
  - fresh-safe pool 4,109 over universe 7,448; maximum matching 36 exactly covers the 72 residual rows, stranded 0
  - "windfall-type 18th-certificate candidates: 0 roots; receipted-WIN still covering open rows: 0 rows"
  - per-row fresh-safe candidate demand ranges 52..76 for every one of the 72 rows
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1063
  note: resolve6正本（e85d4bfb…）のjoin stats・universe hits・win cover hitsがstage-1再現の直接比較対象
- type: depends_on
  target: K1066
  note: windfall4証明書群（fold9正本のReceipt root群・閉鎖4行の幾何再導出）
- type: depends_on
  target: K1067
  note: windfall4 receipt fold（fold9）正本（24db2352…）の残余74行リスト
- type: depends_on
  target: K1069
  note: 39 live witness depth-10掃引正本（22953ae1…・WIN 1/REFUTED 38）のphase-2 join結合
- type: depends_on
  target: K1070
  note: 十七証明書38 gate正本（c1073bae…）・証明書SHA（21dd2f0e…）のcross pin
- type: depends_on
  target: K1071
  note: fold10正本（bed7d331…）の残余72行リスト・閉鎖2 target行
- type: depends_on
  target: K1072
  note: resolve7正本（207f4094…）のpost-retire割当表34×2+4×1の幾何独立再検査
artifacts:
- path: research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/candidate_supply_rebuild_20261120.py
  role: verifier
  note: 8正本SHA-256 pin・stage-1 resolve6 verbatim再現・phase-2 join衝突fail-closed・残余72行universe再構築・候補供給計算機（全25 gate）
- path: research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json
  role: data
  note: 候補供給正本（SHA-256 49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa）・2回実行+別cwd別プロセスでbyte-identical
- path: research/log/2026-11-20-n11-residual72-full-cache-join-candidate-supply.md
  role: log
  note: 研究ログ（単一オーナー宣言・結果・次の一手）
scope: >-
  出版済み正本（SHA-256 pin）とmain上corpus 1,272ファイルのみから残余72行の
  候補供給を再構築する。1行も閉じず、いかなるrootの新規掃引判定も行わず、
  depth-saturation audit・証明書抽出・二石root・空盤の勝敗確定は対象外。
  閉じた行と残った行のゲーム理論的値は主張しない。
evidence: >-
  （1）入力は8正本をSHA-256 pinしてfail-closedに読む（resolve5 5a2f4815…・
  published resolve6出力 e85d4bfb…・39掃引 f8608d0a…・fold9 24db2352…・
  fold10 bed7d331…・sv17 c1073bae…・live掃引 22953ae1…・resolve7 207f4094…）。
  （2）stage-1はresolve6機械をverbatim再実行し、corpus 1,279 manifest中1,272
  sha一致（7ファイルはpublished resolve6と同様に除外・信頼境界一致）、join
  stats（judged 7,493・REFUTED 6,707・WIN 786・衝突0）・universe 7,969・
  universe hits（fresh 7,519・fresh-safe 4,417ほか全数値）・win cover hits
  4根・base 78行がpublished resolve6正本と完全一致（不一致ならfail-closed）。
  （3）phase-2 join: windfall4 receipt 4根（canonical写像gate）・十七 receipt
  1根（sv17のroot・証明書SHA・coverage claim 2行cross pin）・39 live掃引分類
  （WIN 1=十七root〔receiptとlive掃引の二重出典〕・38 REFUTED・order_conflicts
  0・両順序正本）を加え、canonical root合計7,532（REFUTED 6,745・WIN 787）・
  新規判定はちょうど39根のみ・WIN/REFUTED衝突0でfail-closed。
  （4）残余72行の出自: 78−fold9の4行−fold10の2行=72がfold10正本の残余
  リストと完全一致、閉鎖6行は各rootの幾何被覆再導出で確認、fold10の3行目は
  78行計画外のextra行（resolve7の判定と一致）。（5）universe72=7,448
  （78行時7,969のunsafe-equal部分宇宙・coverage部分性gate PASS・両差分0行）。
  U72内の判定済みはREFUTED 468の他は**WIN 0根**。（6）候補供給: fresh
  6,980（fresh-safe 4,109・fresh-unsafe 2,871）・pair辺536・72行すべてに
  singleton fresh-safe候補・multi-cover根0・**最大matching 36が残余72行を
  1回被覆で完全に覆う（stranded 0）**・greedyなら40本・1行あたりfresh-safe
  候補は52〜76本で供給は枯渇していない。retire後38 live根は全38根が72行の
  open行を被覆したままREFUTED-D10（「39-root計画からの供給ゼロ」の行単位
  裏付け）で、phase-2のfresh poolからは除外済み。（7）windfall型（corpus
  judged WIN・未receipt・raw provenance要求）の第18証明書候補は**0根**、
  既receiptのopen 72行追加被覆も**0行**。無償閉鎖供給の枯渇を確定し、
  次の一手はfresh-safe 36本計画のdepth-10両順序掃引（着手時に別途単一
  オーナー宣言）・fresh-unsafe 2,871の構造分類・add-two-stones拡張、
  depth>10のいずれかであることを正本演算で裏付けた。（8）resolve7の
  post-retire割当表34×2+4×1=72行を本レーンの独立幾何で再検査し
  72/72行の被覆幾何一致。（9）決定論: stdlibのみ・repo実験ルートから約47秒・
  2回実行+別cwd別プロセスでbyte-identical（正本SHA-256 49b6f85f…）・
  25 gate全PASS。（10）解釈規約: 本項は1行も閉じず新規判定・掃引を1根も
  実施しない。REFUTED-D10はLOSS証明ではない。witness計画は条件付き計画で
  証明書ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4はすべてUNKNOWNのまま。**
---

## 詳細

K1072（resolve7）が「retire済み39-root計画からの残余72行へのdepth-10 witness
供給ゼロ」を出版正本だけで確定したのを受けて、宣言済み単一オーナーレーンとして
resolve6のcorpus/join/universeをverbatim再構築し、**残余72行にまだ実際に使える
候補供給**を計算した。

主結果は4点: (1) stage-1再現がpublished resolve6正本と全数値で完全一致し、
phase-2 join（windfall4・十七receipt・39 live掃引）の新規判定がちょう39根で
衝突0。(2) 残余72行の出自が78−4−2でfold10正本と完全一致し、
universe72（7,448）上のfresh-safe pool 4,109から**最大matching 36本が72行を
1回被覆で完全に覆う（stranded 0・全行singleton候補・1行最少52本）**。
retire後38 live根はopen行を被覆したまま全件REFUTED-D10で、resolve7の
供給ゼロを行単位・割当単位で裏付けた。(3) **windfall型第18証明書候補は0根**、
既receiptの追加被覆も0行で、corpus/receipt系の無償閉鎖供給がこの時点で
枯渇していることを確定。(4) resolve7の34×2+4×1割当表を独立幾何で再検査し
一致。次の一手はfresh-safe 36本計画のdepth-10両順序掃引（着手時に単一
オーナー宣言ノートを先行）か、fresh-unsafe 2,871本・add-two-stones拡張・
depth>10である。
詳細は[実験](../../experiments/n11-residual72-full-cache-join-candidate-supply-20261120/README.md)・
[候補供給正本](../../experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-full-cache-join-candidate-supply.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**


## 独立第二検証（2026-11-20）

K1075の候補供給生成器をimportしない別実装で、出版済み6正本をSHA-256 pinし、残余72行の幾何と36-root witnessを再検査した。**44/44 gate PASS**。

- 72行からadd-one-stone universeを独立再構築し、7,448 rootを再現。4×4 Bareiss determinantで全rootの4点組を厳密検査し、safe 4,577・unsafe 2,871を得た。被覆サイズは1行6,616 root・2行832 rootで、3行以上の被覆rootは0。
- K1075の36 fresh witness rootは全件7石・D4正準形・safe。D4変換後の全単石削除から各rootの2行を再導出し、36本が72行を重複なくちょうど1回被覆することを確認。72頂点の上界36に達するため、**pair matching 36は最適**。
- resolve7のretire後38 rootも独立再検査し、34 root×2行+4 root×1行=72行の割当が幾何的に一致、重複・欠落0。
- fold9/fold10/resolve7/K1075の残余72行リストが完全一致。独立safe/unsafe総数とK1075のfresh-safe 4,109・fresh-unsafe 2,871・judged REFUTED 468・judged WIN 0の個数は算術的に一致。
- 2回の別プロセス実行でbyte-identical。3回目の計測実行37.313秒。検証器SHA-256 `74fd3275baffb576dee2959678b85a655136dd4595fa2d39bf980c7b3a515972`、結果JSON SHA-256 `5511222b5385a2e57845b944e3607d2ac406203e4da827fb4e62b8e362b5a46d`。

**限界**: K0863の1,279-file corpusとphase-2 verdict joinは再構築していない。fresh-safe 4,109のroot identity集合とpair edges 536の全辺集合はK1075正本の集計値をpinして整合確認したもので、本検証で独立列挙していない。WIN/REFUTED判定・depth-10探索・証明書・receipt・foldは新規生成していない。36-root sweepは別のsingle-owner宣言に属するため、本検証では実行していない。

詳細: [独立検証器](../../experiments/n11-residual72-full-cache-join-candidate-supply-20261120/verify_candidate_supply_geometry_second_20261120.py)・[44 gate結果](../../experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/candidate-supply-second-verification-20261120.json)・[研究ログ](../../log/2026-11-20-n11-residual72-candidate-supply-independent-second-verification.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。** 被覆計画は勝敗証明ではなく、REFUTED-D10もLOSS証明ではない。
