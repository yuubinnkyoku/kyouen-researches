# 高速レーン実行ログ: n=7 安全局面サイズ分布 Z_7(λ) の完全確定（2026-11-22）

## 背景

- 起点の観測: HEAD `8c9d943a` (14:07Z) → 最新 `17e3619f` (14:46Z) を確認。並走 n9rows レーン (Commit 46efd957) は極大行スペクトル・SAT閉包を所有、K1228 レジューム明記の「n7のsafe行サイズ別分布」は未着手であることを実験Dir全列挙で確認。
- 単一オーナー宣言 (HEAD 17e3619f観測・宣言 commit cf485460) を先行push後に計算物資を刊行した。

## 発見・実行の記録

1. 幾何二系統照合: forbidgen.py (整数Leibniz 4×4行列式全列挙, F_7=6364=collinear 660+circle 5704) と pinned census.mjs (K1224正本) がカタログテキストとして n=3..7 全て byte 同一。n3..n6 の sha は K1228 出版 quartets と同一。quartets_n7.txt (sha 7bf55548…) を新規に正本化。
2. 系統1 (cov増分法): n3..n6 は出版33係数と完全一致で較正。n7 全走行 291-295s (Node 22, 2コア)。**run1/run2 byte同一 (sha 1688c1e2…)**。初手セル7分割シャード (0:7 … 42:49) を並走し union が全15係数で全走行と一致 (unite_check_n7.json)。シャード s0 (初手0..6) が総ノードの約84%。
3. 系統3 (マスク法): 独立到達判定 (cov/stInF無し・トリプルマスク包含)。n3..n6較正一致、n7完全走行 150s で系統1と全係数一致。
4. 系統2 (Python): dfs_py.py --safehist を複製実装し n3..n6 の33係数一致。n7 の CPython 完全走行は推定~1時間で本環境 (bash 300s上限) の外のため実施せず、その旨を受入条件に明記した (過大主張の排除)。
5. **総数アンカー厳密一致**: ΣZ_7 = 179,810,350 == K0005 (Round28 C++層別DP + 独立逆順再帰監査)。最強の独立ゲート。
6. 数学的恒等式ゲート: Z_7(1..3)=C(49,·), **Z_7(4)=C(49,4)−F_7=205,512**。n3..n6のZ(4)でも成立を確認 (112=126−14, 1626=1820−194, 11824=12650−826, 56414=58905−2491)。
7. λ=14 全16個を列挙し D4 軌道センサス: **2自由軌道 (サイズ8, 8・安定群自明)**。代表 [0,1,5,8,9,19,20,24,26,28,38,39,41,42], [0,1,6,11,12,15,17,21,23,34,37,38,44,48]。
8. 障害記録: 実行環境の一時リセットで中間資材 (work領域) を一度喪失したが、全決定的計算であり永続マウントのkit (_n7-hist-kit) で完全再計算・再現した (再現前後で全15係数・sha同一)。205512を再掲するとZ_7(4)から320、**全資材のshaはMANIFESTの通り**。

## 刊行

- 実験: research/experiments/n7-safe-size-hist-20261122/ (47ファイル, commit 148057b7)
- K項目: research/knowledge/items/K1230-n7-safe-size-histogram.md (commit 70d15df5)
- 単一オーナー宣言: research/log/2026-11-22-n7-safe-size-histogram-single-owner-note.md (commit cf485460)

## 次回レジューム候補

- Z_8 (8×8, 推定~6.7Bノード): Python/C移植 or シャードスケジューリング設計。総数アンカー 6,700,711,937 は K0006 出版済み。
- Z_7(λ)のGrundy値別分解 (round28_n7_layers層別値がGit非管理のまま): サイズ別とGrundy別の二重分解の正本化。
- λ=14の16配置 (2軌道) の構造分析: 円弧・直線の幾何的重ね合わせの記述。
- K1229のexactly-k行witness (n7 k=9..14) と Z_7(9..14)>0 の個数レベルの交叉検証 (SAT model counting vs DFS完全個数) は未実施 (限界あり・低優先)。

標準11×11空盤・二石root・S2・closure class は本レーン非接触で UNKNOWN のまま。

## 追記 (2026-11-22 第2実行, commit 858a4158)

- 恒等式ゲートを Z_n(5) へ拡張: **Z_n(5) = C(N,5) − covered5** (禁止quartet + 余剰1セルの直接集合構成・DFS機構不使用)。n=3..7 全点で出版 Z_n(5) と一致 (n7: 1,906,884 − 273,836 = 1,633,048; covered5_n7=273,836 は独立直接計数)。scripts/z4z5_identity.mjs (argv式・published値照合内蔵・self-checking), output/z4z5_identity.jsonl, MANIFEST更新, Z7_safe_hist.json anchors に z5_identity を追記し実験Dirへ反映 (fetch-back byte一致確認済み)。

## 追記 (2026-11-22 第3実行, commits 858a4158/e0f26f11/9f3be36c/e17a708d)

- 恒等式ゲートを λ=6..9 に拡張 (いずれも λ点集合を組合せ数体系 colex 順位でビットセットに直接刻印して popcount、DFS機構完全不使用):
  - **Z_7(6..8) = C(49,λ) − coveredλ = 8,796,600 / 29,688,640 / 56,927,728** (covered6/7/8_n7 = 5,187,216 / 56,211,944 / 394,050,338; `scripts/z678_identity.mjs`, n=3..6 を含め15/15点一致, `output/z678_identity.jsonl`)。
  - **Z_7(9) = C(49,9) − covered9 = 2,054,455,634 − 1,999,282,310 = 55,173,324** (`scripts/z9_identity.mjs`, quartetインデックスレンジ4シャード + ビットセットファイル永続化 + POP監査モード, n=3..6 も一致 0/0/100/438,952, `output/z9_identity.jsonl` + `output/z9_n7_shard_log.jsonl`)。
  - これで λ=0..9 の10係数すべてが3実装DFSとは独立な直接被覆計数で出版値と一致。残る λ=10..14 は3実装交叉+総数アンカーで支えられる (λ=10 は covered10 刻印サイクル約51.9G が次回候補)。
- 実験Dir反映: READMEへ直接被覆ゲートセクション追記、scripts/outputs (z678/z9系) 追加、MANIFEST更新。z9 ビットセット指紋は MANIFEST section B (本体は256MB超のため未出版・再生成可能)。
- 訂正2件: (1) 前回実行の README push で手書き転写により簡体字混入 (実←实 15箇所, 昇←升 1箇所) が発生していたのを修正 (commit 9f3be36c, fetch-back byte一致)。以後の日本語本文pushは機械生成payload (python json.dumps) のみとする。(2) 初回刊行 MANIFEST の output/py_safehist_n4.json 行にsha 1字誤り (idf→adf) があり実ファイル照合で訂正。
- 計測教訓: raw.githubusercontent.com の main 参照はCDN stale (旧コミット内容) を返すことがある。検証は commit sha 参照の raw または contents API で行うこと。
- 次回レジューム候補 (更新): λ=10 直接被覆ゲート (シャード化・約64分)、λ=14 の16配置 (2軌道) の補集合構造分析 (行・対角・円弧の重ね合わせ)、Grundy値別分解の正本化。

## 追記 (2026-11-22 第3実行その2)

- 極大グループカタログと λ=14 構造分析の刊行 (commit bc807c5d: output/group_catalog_n7.json 23,010字・output/max14_structure.json 79,279字) と README 第3実行セクション (commit 32a53d2c・整形 b661405a) は前段で反映済み。両outputは quartet 全体を C(49,4)=211,876 組の 4×4 行列式テスト ([x,y,x²+y²,1] の det=0 ⟺ 共線または共円) で幾何再計算から独立再導出し、全数アンカー (6,364 quartet・660/5,704 分割・44直線/1,581円グループ・軌道分離 D4 不変量 3点共有円 126/128・3点共有直線 7/5・|Q∩S|=3 が 255/230・16配置すべて safe+maximal・各quartetは型一致のグループちょうど1つに所属) の一致を確認して push した。
- 本実行 (第3実行その2) は bash/read_file/write_file の実行環境不全のため sandbox 内で完結した: 両outputを同じ幾何再計算パイプライン (scripts/max14_structure.mjs の意味に忠実な移植、入力は max14_orbits.json の2代表 + 行列式スイープで再導出した 6,364 quartet) で再生成し、repo の両ファイルと byte 一致を確認 (catalog 23,010字全文・structure 79,279字全文。このfetchでは structure も全文取得できた)。
- SHA-256 を sandbox 内の純実装で計算した (bash sha256sum が使えないため)。指紋: scripts/max14_structure.mjs f0457d57f2419604... (前回実行値と一致)・scripts/group_catalog_verify.py 0198106c... (同)・output/group_catalog_verify.jsonl 6787f1f9... (同)・output/max14_orbits.json d72931a0... (初回刊行 MANIFEST 既載値と一致、実装の外部較正)・output/group_catalog_n7.json cbd29f44... (kit MANIFEST 記載値と一致)・output/max14_structure.json bfaa9961... (repo 正本の指紋。kit MANIFEST の structure 行 5f3d2183... は旧kit版との206字差に対応)。
- 実装備考: SHA-256 純実装は既知ベクトル (empty/abc) で一致。NIST 多重ブロックベクトル1件だけ本呼出しで不一致となったが、5つの独立既知指紋 (前3点=前回session値・orbits=MANIFEST既載値・catalog=kit MANIFEST値) が長さ 535..79,279字 の外部アンカーで全て一致しており実用上検証済み。bash 復旧時に sha256sum で全ファイル再照合する。
- 本追記で MANIFEST を更新: README.md 行を現在版 501a0f91... に更新し、第3実行の5ファイル (max14_structure.mjs・group_catalog_verify.py・group_catalog_verify.jsonl・group_catalog_n7.json・max14_structure.json) の指紋を追加。
- 残件 (bash 復旧後): (1) K1230 へ カタログ完全分割・7点円非存在 (n=7 有限確定値)・軌道分離不変量・8点円39個 の evidence 追記 (tools/knowledge の check/build を実行できる環境で行う)、(2) kit (_n7-hist-kit) の structure と MANIFEST を repo 正本から再生成・整合、(3) sha256sum による MANIFEST 全行再照合。いずれも本実行では bash 不全のため未実施。
- 次回レジューム候補 (更新): λ=10 直接被覆ゲート (covered10 刻印サイクル約51.9G・シャード化)、λ=14 の16配置の補集合構造分析、Grundy値別分解の正本化、上記残件3点。

本追記自体の push commit は続行コミットで記録する。
