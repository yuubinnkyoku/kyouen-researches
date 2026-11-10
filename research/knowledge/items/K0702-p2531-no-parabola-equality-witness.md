---
id: K0702
title: p=2531でも剰余放物線の等号A(p)=(p+3)/2を達成する証人が存在しない（2例目・監査待ち）
kind: proposition
status: needs-review
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
  target: K0693
  note: 等号不達成がp=2207に限らないことを示す2例目
- type: supports
  target: K0101
  note: 全奇素数での等号を否定する2番目の反例候補
artifacts:
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/batch142-180/plan.json
  role: manifest
  note: 既被覆d=141,161を除く38件の計画。前段200 dとsource hashを固定
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/batch142-180/coverage.json
  role: manifest
  note: 前段200 dと新38 dに重複なし、被覆和238/1265、残り1027。未完了・失敗・UNKNOWNはなし
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/certificates142-180.json
  role: manifest
  note: 新38件の採用CNF・LRAT gzipのpathとhash、ローカル保持する原DRATのpathとhash
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/verification142-180.json
  role: data
  note: 新38件の独立投影schema、保存圧縮証明の実再生、原DRAT hashと前段台帳のhash連鎖を照合
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/batch142-180/README.md
  role: source
  note: d=142..160,162..180の独立監査と保存証拠再生の固定再現手順
- path: research/experiments/parabola-p2531-lrat-batches-20261110/audit.py
  role: verifier
  note: 前段被覆を引き継ぎ、既被覆・重複dを拒否してcase分離した並列LRAT監査と再開可能な集計を行う
- path: research/experiments/parabola-p2531-lrat-batches-20261110/verify_saved.py
  role: verifier
  note: 前段manifestのhash連鎖、新入力の独立投影schema、圧縮証明の実再生を照合
- path: research/experiments/parabola-p2531-lrat-batches-20261110/regression.py
  role: verifier
  note: 7不正planと、UNKNOWN・失敗・未完了・既存coverage上書きの制御を再現
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/controller-regression.json
  role: data
  note: 重複・既監査dなどの拒否と、未確定や失敗を被覆へ加えない合成制御の成功
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/batch102-140/plan.json
  role: manifest
  note: 既被覆d=121を除いた38件の新規計画。前段162 d・source hash・4 process設定を保存
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/batch102-140/coverage.json
  role: manifest
  note: 前段162 dと新38 dは重複なし、被覆和200/1265、残り1065。未完了・失敗・UNKNOWNはなし
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/certificates102-140.json
  role: manifest
  note: 採用CNFとLRAT gzip38件のpath・hash、ローカル保持した原DRATのpathとhash
- path: research/experiments/parabola-p2531-lrat-batches-20261110/output/verification102-140.json
  role: data
  note: 新38件の独立投影schemaと圧縮証明実再生、原DRAT hash、前段履歴のhash連鎖を照合
- path: research/experiments/parabola-p2531-lrat-batches-20261110/README.md
  role: source
  note: case分離、計画と集計、保存証拠の独立再生と被覆の範囲
- path: research/experiments/parabola-p2531-lrat-20261110/audit.py
  role: verifier
  note: 既存147 dとの重複を避けてd=86..100を生成し、整数幾何・投影schema・DRAT-trim・修正LRATで検査
- path: research/experiments/parabola-p2531-lrat-20261110/verify_saved.py
  role: verifier
  note: 省略辺の構造、前段4入力のbyte一致、新15入力の独立投影、圧縮CNFとLRATの実再生、被覆履歴を照合
- path: research/experiments/parabola-p2531-lrat-20261110/input/edges.txt
  role: data
  note: 二完全対の自明な799480辺を除いた38160辺。全提供辺の整数幾何を再検査
- path: research/experiments/parabola-p2531-lrat-20261110/output/batch86-100/geometry.json
  role: data
  note: 38160辺をgeneric整数4×4で受理。完全性ではなく健全性をUNSATの根拠に使う
- path: research/experiments/parabola-p2531-lrat-20261110/output/batch86-100/coverage.json
  role: manifest
  note: 前段147 dと新15 dは重複なし、独立被覆和162/1265、残り1103。前段manifestのhash付き
- path: research/experiments/parabola-p2531-lrat-20261110/output/certificate-manifest.json
  role: manifest
  note: 新15件のGit管理CNF・採用LRAT gzipのpathとhash。原DRAT gzipはローカル保持しhashを記録
- path: research/experiments/parabola-p2531-lrat-20261110/output/saved-verification.json
  role: data
  note: 全15圧縮証明を修正LRATで再生し、独立投影schema・原DRAT15 hash・162 dの被覆和も照合
- path: research/experiments/parabola-p2531-lrat-20261110/README.md
  role: source
  note: 有用辺への入力縮約、証拠の保存範囲、独立再生と被覆履歴の再現手順
- path: research/experiments/parabola-p2531-lrat-20261109/audit.py
  role: verifier
  note: 未被覆d=82..85の新しいDRAT生成、全提供辺の整数幾何、独立投影schema、DRAT-trimと修正LRAT検査
- path: research/experiments/parabola-p2531-lrat-20261109/verify_saved.py
  role: verifier
  note: SATソルバや元generatorを使わず、保存辺の独立投影・入力と証拠hash・旧143件との被覆和を照合
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/edges.txt.gz
  role: data
  note: ヘッダ2531 837640と全提供禁止四点。UNSATに完全性は不要で全辺の健全性を実検査
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/geometry.json
  role: data
  note: 837640辺をgeneric整数4×4行列式で受理。wrapper・generic sourceとinput hash付き
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/coverage.json
  role: manifest
  note: 修正版DRAT143 dと新LRAT4 dは重複なし、独立被覆和147/1265、残り1118 d
- path: research/experiments/parabola-p2531-lrat-20261109/output/saved-verification.json
  role: data
  note: 全4入力を各1265変数・38160節の独立投影schemaへ照合し、保存LRAT・原DRAT・被覆を検査
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/d82/core.lrat.gz
  role: certificate
  note: d=82の修正LRAT検査器で受理した反駁。原DRAT・CNFとreceiptは同じexperimentへ保存
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/d83/core.lrat.gz
  role: certificate
  note: d=83の修正LRAT検査器で受理した反駁
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/d84/core.lrat.gz
  role: certificate
  note: d=84の修正LRAT検査器で受理した反駁
- path: research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2/d85/core.lrat.gz
  role: certificate
  note: d=85の修正LRAT検査器で受理した反駁
- path: research/experiments/parabola-p2531-lrat-20261109/README.md
  role: source
  note: 入力・証拠・各検査の再現、異なる検査方法の被覆和と全数未完了の区別
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/deep_scan_2531.json
  role: data
  note: d=1265..1の全数走査（UNSAT 1265・unknown 0・SAT 0）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/scan_mp.py
  role: verifier
  note: マルチプロセス衝突予算スキャナ（8並列、dごとに独立なCNF）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/validate_reduction.py
  role: verifier
  note: p<=23で符号化と完全対構造の全数照合
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2503_2700.json
  role: data
  note: 浅いd走査で2531が最初に落ちた記録
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2531.json
  role: data
  note: 旧チェッカーの受理記録。K0707の偽受理発見により独立証拠への採用を保留
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp
  role: verifier
  note: 増分DRATチェッカー（RUP＋RAT）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2531_34249932790a9e9d.json
  role: data
  commit: 87e28af3c927d640bde3fbc8a20238efc30bccb8
  note: K0707修正版で143 dの受理記録。計画標本63/63を含むが、全1265 dの監査ではない
- path: research/experiments/parabola-audit-coverage-20261109/inventory.json
  role: data
  note: 固定commitの被覆検査。修正版143/1265 d、未被覆1122 d
- path: research/experiments/parabola-audit-coverage-20261109/inventory.py
  role: verifier
  note: 件数と計画標本63件の集合包含を区別して照合する再現コード
scope: 奇素数p=2531のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。他素数への一般化は主張しない。
evidence: 全1265 dでCNF UNSAT（cadical、衝突予算20万、unknown 0）。旧DRAT受理記録はK0707により独立証拠に採用しない。修正版の固定commitの143 dと独立LRAT受理95 dは重複なしで合計238/1265。全数再監査は未完了。
---

## 現在の監査上の制限（2026-11-09）

[K0707](K0707-incremental-drat-deletion-unsoundness.md) で旧増分DRATチェッカーの偽受理を再現した。
観測時点の全数出力は1263件が `VERIFIED`、d=393,395が入力読み込みエラーだったが、
旧実装の受理件数を独立検証済み件数とは数えない。
以下の旧標本・373件という記録も同じ制限を受ける。
CNF UNSAT のソルバ主張と幾何への還元はこの反例で否定されないが、
旧レシートを再利用しない全数再監査が必要で、statusは `needs-review` のまま。
修正版（ソースSHA-256 `34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`）で
d=393,395から再監査を開始し、commit `87e28af3c927d640bde3fbc8a20238efc30bccb8` では
重複のない**143 d**のUNSAT・終了コード0・出力VERIFIEDの受理記録がある。
計画標本 `d=1,21,...,1241` の63件を全て含むが、全1265 dのうち1122 dは未被覆。
「標本完了」は「全数監査完了」ではない。
inventoryは保存レシートの整合性・被覆のみを検査し、今回DRATを再生していない。
修正版の一般健全性は有限回帰からは導かれない。

その後、修正版143 dに含まれない **d=82,83,84,85** で新しい証明を生成した。
各CNFは1265変数・38160節。入力に使った837640禁止四点すべてを別のgeneric整数4×4検査器で受理し、
全4入力の節集合を元generatorを使わない独立な固定完全対の投影schemaへ照合した。
各原DRATを固定DRAT-trim -Uで受理・LRAT化し、[K0718](K0718-lrat-empty-clause-vacuous-rat-unsoundness.md)の空節処理を修正した別実装で全4 LRATを受理した。
その段階では旧修正版143 dと新LRAT4 dに重複はなく、独立被覆の和は147/1265 d、未被覆1118 dだった。
異なる検証器の受理を同じsource hashの143件へ混ぜず、別manifestで集合和を保存する。
提供辺集合の完全性はUNSAT排除には不要であり、健全な辺の部分集合でも安全テンプレートに対する緩和となる。
これは一部のdの有限反駁検査であり、全数監査や検証器の一般健全性の形式証明ではない。

さらに **d=86..100の15件** を同じ二実装の経路で受理した。
二完全対の自明な辺を除いた38160提供辺を整数幾何で再検査し、前段4入力は縮約後もbyte一致した。
新15入力も独立投影schemaへ全節集合が一致し、Git管理する各CNF・LRAT gzipを展開して修正LRATで実再生した。
その段階の前段147 dと新15 dは重複がなく、独立被覆の和は162/1265 d、未被覆1103 dだった。
修正版DRAT143 dとLRAT19 dを区別し、前段manifestのhashを含む被覆履歴として保存する。
新15件は採用LRATとCNFをGit管理し、生成時の原DRAT gzipはローカル保持してhashをmanifestへ記録した。
原DRATがない別checkoutでも採用LRATの独立再生は可能である。

続いて **d=102..120,122..140の38件** をcaseごとに入力・証明を分離して最大4並列で監査した。
既被覆のd=121は対象から除外し、同じcaseを重複起動しない計画検査を行った。
全38件がDRAT-trim -Uと修正版LRATで受理され、保存したCNFと圧縮LRATの別処理での実再生も全件成功した。
全新入力の独立投影schema・sourceと証拠hash・前段manifestの連鎖も照合した。
その段階の独立被覆の和は200/1265 d、未被覆1065 d。内訳は修正版DRAT143 d、LRAT57 dだった。
7不正planとUNKNOWN・失敗・未完了・既存coverageの上書きに関する制御も期待通りだった。
これは計画と被覆集計の制御であり、一般的な検証器健全性の数学的証明ではない。

さらに **d=142..160,162..180の38件** を既存のcase分離ドライバで監査した。
既被覆のd=141,161を除き、全38件がDRAT-trim -Uと修正版LRATで受理された。
全新入力の独立投影schemaを照合し、保存したCNF・圧縮LRATの別処理での実再生も全件成功した。
前段台帳のhash連鎖と原DRAT38件のローカルhashを確認し、前段200 dとの重複はない。
**現在の独立被覆の和は238/1265 d、未被覆1027 d**。内訳は修正版DRAT143 d、LRAT95 dである。
全数監査や正確な最大サイズ、検証器の一般健全性の形式証明を主張しない。

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 2531 では
`A(2531) < (2531+3)/2 = 1267`**（すなわち `A(2531) <= 1266`）。
K0693（p=2207）に次ぐ**2例目の等号不達成素数**であり、K0101 の「全奇素数で等号」に対する
二つ目の反例候補である。`A(2531)` の正確な値と他素数への一般化は主張しない。

## 根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は `0` と一つの完全対 `{d,p-d}` と他の各対の一側に限られ
   （K0097 の上界証明から初等的に従う）、K0334 が等号を「ある `d` について signed NAE3/4 と
   原点節の CNF が充足可能」と全奇素数で同値に還元している。
2. `scan_mp.py`（マルチプロセス、衝突予算 20 万、8 並列）で **d = 1265..1 の全 1265 個**を走査し、
   **UNSAT 1265・SAT 0・不明 0**（`output/deep_scan_2531.json`、3,109 秒）。
3. 同じ実装は隣接する 63 素数（2003..2477 の 2207 を除く）で SAT 側の等号証人を作り、
   探索と独立な generic 4×4 検証器で共円 0 件を確認している。符号化の全数照合は p<=23 で一致（K0693）。

## 限界

- 旧版の標本8件・途中373件のVERIFIED記録は、K0707により現在の修正版の被覆数には加えない。
  修正版DRAT143 dと新LRAT95 dの和238 d以外はソルバ主張のまま。全数監査は未完了でstatusは `needs-review`。
- `A(2531)` の正確な値は未確定。
- 同時期の走査で p=2539, 2543, 2549 も d=h..h-30 の範囲で証人が見つかっておらず、
  反例素数は 2207, 2531 以外にも存在する可能性がある（未確定）。
