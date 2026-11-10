---
id: K0693
title: p=2207では剰余放物線の等号A(p)=(p+3)/2を達成できない（単一CNF独立監査済み）
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2と等号集合の完全対構造
- type: depends_on
  target: K0334
  note: 等号 ⟺ あるdについてsigned NAE3/4と原点節のCNFが充足可能（全奇素数で証明済み）
- type: supports
  target: K0101
  note: p=2207の単一CNF独立監査による等号不達成が、全奇素数での等号への反例を与える
artifacts:
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/schema.py
  role: verifier
  note: CardEncと探索builderを使わずone-hot・明示Sinz counter・NONE単位節・点定義を再構成し、残余幾何節を分離
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/audit.py
  role: verifier
  note: 保存CNFの独立schemaと全提供幾何節、元DRATのRUP限定検査と空節処理修正版LRATを実検査
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/replay.py
  role: verifier
  note: 配布するCNF・LRAT gzipを別処理で実再生し、source・schema・幾何・証拠hashと既存下界を照合
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/schema.json
  role: manifest
  note: 7720変数・50616節を18748構造節と31868幾何節へ全分離し、予約ID範囲と元証拠hashを保存
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/geometry.json
  role: data
  note: 全31868提供辺をgeneric整数4x4行列式で禁止四点と確認。辺集合の完全性はUNSAT排除に不要
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/rup.json
  role: data
  note: 元497179行DRATを固定DRAT-trim -Uで受理し、RUPだけのcoreを抽出
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/lrat.json
  role: data
  note: 空節処理修正版LRATで187955行の抽出証明を実検査して受理
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/manifest.json
  role: manifest
  note: Git管理する採用CNF・LRAT gzipと保持した元DRATの所在、raw・gzip hashと検査器source hash
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/replay.json
  role: data
  note: 採用圧縮証明の別処理での実再生、全bindingの照合と独立上界1104
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/regression.py
  role: verifier
  note: 小素数で状態とcounter補助変数を全列挙し、schema改変6件と独立幾何の正負制御を検査
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/regression.json
  role: data
  note: 1104状態の存在射影と6改変拒否、schemaだけでは通る非辺を幾何検査で拒否
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/README.md
  role: source
  note: 全1105点安全集合からCNFモデルを構成する論理、独立監査・再生と信頼境界
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/README.md
  role: source
  note: 反例候補の方法・証拠・信頼境界・次の監査
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/build_inventory.py
  role: verifier
  note: d=1..1103の判定表を生成し、タイムアウト分は衝突予算2000万で再判定する
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207_d_verdicts.json
  role: data
  note: 全1103 dのUNSAT判定と出所（cadicalログ／マルチプロセス／再判定）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/validate_reduction.py
  role: verifier
  note: p<=23の全安全集合を列挙し、完全対dの集合とCNFのSAT/UNSATを全dで比較する
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/reduction_validation.json
  role: data
  note: 7素数の突合結果（全一致）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2143_2500.json
  role: data
  note: 隣接63素数では同じ実装がSAT側で証人を返し独立検証も通っている
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp
  role: verifier
  note: 増分DRATチェッカー（RUP＋RAT、決定レベルとtrail）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/audit_all_d.py
  role: verifier
  note: dごとにCNFとDRAT証明を生成しチェッカーで監査する再開可能ドライバ
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full.json
  role: data
  note: 旧チェッカーの標本21 dの受理記録。K0707の偽受理発見により独立証拠への採用を保留
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2207_34249932790a9e9d.json
  role: data
  commit: 87e28af3c927d640bde3fbc8a20238efc30bccb8
  note: 修正版の受理記録5 d。全1103 dのうち1098 dは本snapshotの監査範囲外
- path: research/experiments/parabola-audit-coverage-20261109/inventory.json
  role: data
  note: 固定commitのレシート整合性と被覆の検査。DRATの再実行ではない
- path: research/experiments/parabola-audit-coverage-20261109/inventory.py
  role: verifier
  note: 重複・未被覆・計画標本の照合と13制御。証明内容の検査器ではない
- path: research/experiments/parabola-audit-coverage-20261109/inventory-20261109T1016.json
  role: data
  note: 最新mainの保存レシートも21/1103 dと確認。残り1082 d、旧固定snapshot5 dと区別。DRAT再生ではない
- path: research/log/2026-11-09-drat-reaudit-status-omp.md
  role: source
  note: HEAD時点の修正版再監査の確定状態（2207は12/1103、標本12/21）
- path: research/log/2026-11-09-p2207-sample-reaudit-complete.md
  role: source
  note: 標本残り9点の逐次再監査の完了記録（標本21/21 全点VERIFIED）
scope: 奇素数p=2207のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。任意の他素数への一般化は主張しない。
evidence: 別経路のサイズ1105単一CNFをCardEnc非依存の独立schemaへ全照合し、全31868提供幾何節を整数4x4で検査。元DRATを固定DRAT-trim -Uと空節処理修正版LRATで受理し、採用CNF・LRAT gzipも別処理で実再生した。これにより上界1104を有限計算として独立監査済み。旧d別の修正版被覆は21/1103のままであり、単一CNFの完了と混同しない。
---

## d別旧証拠の信頼境界（2026-11-09）

[K0707](K0707-incremental-drat-deletion-unsoundness.md) で、旧増分DRATチェッカーが
充足可能なCNFの偽UNSAT証明を受理することを再現した。
下記の標本21件の `VERIFIED` は旧実装の受理記録であり、独立検証済み証拠としての採用を保留する。
幾何命題やソルバのUNSAT主張を反証したわけではない。d別の全数再監査は未完了である。
現在の本項は、下記の別経路の単一CNF監査により `computed` とする。旧受理件数を増やしたものではない。
修正版ソースSHA-256 `34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`
のレシートは、commit `87e28af3c927d640bde3fbc8a20238efc30bccb8` で
**d={1,50,100,200,300}の5件**がUNSAT・終了コード0・出力VERIFIEDである。
全1103 dのうち1098 dはこのsnapshotの修正版監査範囲外。
inventoryはレシートの整合性を検査したもので、今回DRATを再生したわけではない。
追記（2026-11-09）: その後レシートはHEAD `a0fcb1f` 時点で12件まで追記され、
さらに同日の逐次再監査で残り9件（d={500,550,600,700,800,900,1000,1100,1103}）が完了し、
標本21件は全点VERIFIEDとなった（21/1103、全数監査は残り1,082 d）。
上記の5件は固定snapshot時点の記録として残す。現況の確定は
[再監査ステータスログ](../../log/2026-11-09-drat-reaudit-status-omp.md) と
[標本再監査完了ログ](../../log/2026-11-09-p2207-sample-reaudit-complete.md) を参照。

## 命題・範囲

`Q_p = {(t, t² mod p) : 0 <= t < p}` の安全集合（共円・共線四点を含まない部分集合）の最大を `A(p)` とする。
標準 q=4 のこの構成について、**p = 2207 では等号 `A(2207) = (2207+3)/2 = 1105` が成立しない**、
すなわち `A(2207) <= 1104`。

K0097 の上界 `A(p) <= (p+3)/2` は一般に証明済みで、p <= 2143 の全奇素数では等号証人が知られていた。
本項はその範囲外で最初の「等号を達成できない」素数を与える（有限計算による独立監査）。
独立幾何検査した1104点の下界と現在の監査済み範囲は[K0722](K0722-p2207-safe-lower-bound-1104.md)を参照する。
本項の上界1104は単一CNF経路で独立監査済みであり、K0722の下界と合わせて正確値1104となる。
任意の他素数への一般化は主張しない。

## 単一CNFによる独立監査（2026-11-10）

安全1105点集合はK0097の完全対構造から、原点を含み、完全対が一つ、空対がない形に限られる。
保存CNFの18748構造節を、探索builderやCardEncを使わない明示schemaと全照合した。
変数はone-hot選択子1..4412、prefix counter 4413..5514、点選択子5515..7720であり衝突しない。
残る31868節は原点が常に選択されることを織り込んだ禁止三点／四点節で、
全てをgeneric整数4x4行列式で実際の禁止四点と確認した。

任意の安全1105点集合から、その対状態・点選択とBOTHのprefix ORを割り当てれば構造節を全て満たす。
安全性により、提供した禁止四点の負節も全て満たす。よって安全集合があればこのCNFはSATである。
提供辺集合の完全性はこの方向の論理に不要である。

元497179行のDRATを固定DRAT-trimのRUP限定検査で受理し、抽出187955行LRATを
空節処理修正版の別C実装で受理した。Git管理する圧縮CNF・LRATからの別処理での実再生も成功した。
したがって単一CNFはUNSATであり、安全1105点集合は存在せず、A(2207)<=1104である。

## 現在の根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は、`0` と **ちょうど一つの完全対 `{d,p-d}`** と
   他の各対 `{i,p-i}` の一側からなる（二完全対は等脚台形で共円、完全対が一つも無ければ
   `|S| <= 1+h = h+1`）。この完全対構造は K0097 の上界証明から初等的に従う。
2. K0334 は等号 `A(p)=h+2` を「ある `d` について signed NAE3/4 と原点節の CNF が充足可能」と
   全奇素数で同値に還元している（証明済み）。
3. したがって `d = 1..h` の全 `d` で CNF が UNSAT なら `A(p) <= h+1 = 1104`。
   p=2207（h=1103）でこれを全数確認した: **UNSAT 1103 件・SAT 0 件・不明 0 件**
   （`output/p2207_d_verdicts.json`）。うち 4 件（d=289, 297, 312, 324）は 30 秒制限で
   タイムアウトしたため衝突予算 2000 万で再判定した。
4. 実装の全数照合: p = 5, 7, 11, 13, 17, 19, 23 で `Q_p` の全安全集合（サイズ `(p+3)/2`）を
   列挙し、完全対 `d` の集合と CNF の SAT/UNSAT を全 `d` で比較した結果、7 素数すべてで一致
   （`output/reduction_validation.json`）。p=23 では安全集合 8,064 個、両者の `d` 集合は `{1,...,11}`。
5. 同一実装は隣接する 63 素数（2003..2477 のうち 2207 を除く）で SAT モデルから等号証人を作り、
   探索と独立な generic 4×4 検証器で共円 0 件を確認している（`witnesses_2143_2500.json`）。
6. 別ソルバ一致: d ∈ {1, 289, 550, 1103} を Glucose4 と Minisat22（衝突予算 2000 万）でも解き、全て UNSAT。

## 限界と旧d別監査の範囲

- 全dのUNSAT主張と、修正版検査器の21 dのDRAT受理記録を区別する。
  d別の全数監査は未完了だが、現在の上界はそれらを前提にせず単一CNFで監査した。
  有限の回帰・受理記録から検査器の一般健全性は導かれない。
- `A(2207)` の正確値はK0722で1104とする。サイズ `h+1`（1104）の集合は `x+c-e=1`（`x`=0 を含む、`c`=完全対数、`e`=空対数）
  から **3 形**ある: (a) `(1,0,0)`、(b) `(0,1,0)`、(c) `(1,1,1)`（`0`＋完全対一つ＋空対一つ）。
  2026-11-08: (a) の CNF は UNSAT（31,868 節、cadical 26 秒）、(b) は全 d=1..1103 で UNSAT（unknown 0・SAT 0）。
  (c) の全 (d,e) を覆う単一CNFの探索記録は
  `research/log/2026-11-08-p2207-1104-shape-search-and-drat-plan.md`。
  その後保存された(c)の1104点候補は[K0722](K0722-p2207-safe-lower-bound-1104.md)で独立幾何検査に成功した。
  この下界検査と、別の単一CNFによる上界検査を組み合わせる。d別全数監査の完了とは扱わない。
- 2026-11-08 の DRAT 監査: 増分チェッカー（`drat_check_incremental.cpp`、RUP＋RAT）で
  **標本 21 個の d（1, 50, 100, 150, 200, 250, 289, 297, 300, 312, 324, 400, 500, 550, 600, 700, 800, 900, 1000, 1100, 1103）の証明を全て VERIFIED**
  （証明 16〜576,575 行、検査 0.5〜3,223 秒/件、`output/drat_audit_full.json`）。
  これは旧版の歴史的な受理記録であり、現在の修正版の被覆数には加えない。
- 他素数の現在の監査状態はK0702/K0706/K0708を参照する。
  K0101の全奇素数予想は、p=2647の全1323 dを監査したK0706により既に `refuted`。
  p=2207の旧d別監査の未完了とは別の結論である。
