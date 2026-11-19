---
id: K1079
title: 出版済みK1076 z=17・y=4境界切片の独立第二検証: 二つの独立導出の全行一致・第三実装census一致・K1076パッケージのbyte-pin不整合の検出報告
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - independent second verification of the published K1076 two-token z=17 y=4 boundary slice
  - two fully independent same-day derivations of the z=17 y=4 slice agree on every row
  - third-implementation census (dict-memo, closed-form-free) matches the published forms at 2,961 points
  - the committed K1076 verifier (sha256 a7878b8e...) cannot reproduce the committed K1076 audit.json, whose verifier_sha256 field pins a non-existent older build (388e1a47...)
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約（R<=18証明済み域）と一般tailの両導出で使用
- type: depends_on
  target: K1067
  note: B子閉形式。第二検証では出版済み転写を子局面の生再帰と照合
- type: depends_on
  target: K1064
  note: C子閉形式（1 xor）。第二検証では出版済み転写を子局面の生再帰と照合
- type: depends_on
  target: K1076
  note: 検証対象。repo main 412d75b9 の検証器（blob 911dc4bf・sha256 a7878b8e…）閉形式ブロックをbyte-exactに固定ターゲットとして使用
artifacts:
- path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/report.md
  role: proof
  note: 二導出の一致・表現差の同集合確認・K1076 byte-pin不整合の報告
- path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/verify_z17_y4_second.py
  role: verifier
  note: K1076閉形式ブロック（byte-exact splice）を固定ターゲットに、生再帰二方式・子アンカー・署名帯表・閉包掃引・深域一致・散点の第二検証
- path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/census_z17_y4_second.py
  role: verifier
  note: 第三の独立実装（着手を値ごとに列挙する明示dict memo・閉形式を知らない生再帰）によるx<=45・R<=x+45の全分類とK1076閉形式との照合
- path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/output/audit.json
  role: data
  note: 17,254,465照合・不一致0の決定論的監査結果（2回実行・別cwd byte-identical）
- path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/output/census.txt
  role: data
  note: 第三実装census 2,961点・K1076閉形式と不一致0（2回実行・別cwd byte一致）
- path: research/log/2026-11-20-vertical-fiber-two-token-z17-y4-second-verification.md
  role: log
  note: 単一オーナー宣言と並走出版の競合検出・重複出版の回避・第二検証への転用・K1076 pin不整合・CI観察の記録
scope: >-
  出版済みK1076（z=17・y=4・全x>=4・全R>=0のGrundy分類）の独立第二検証。
  固定ターゲットはrepo main 412d75b9のK1076検証器閉形式ブロック
  （byte-exact splice、sha256 a7878b8e…）。オラクルは同じ日の別セッションで
  K1076と独立に構築された二種の生再帰・第三実装census・第一導出の閉形式。
  新しい全称主張は行わない。K1076の定理・証明・パッケージの改変は対象外。
evidence: >-
  （1）二つの独立導出が全行で一致: 第一導出（K1076出版と独立に当日導出・
  出版前の監査で15,573,034照合・不一致0を確認済み）とK1076の閉形式を
  x<=2000・R<=x+46の2,094,853点およびx<=200,000の帯端・pin・基底点・
  tail計2,499,725点で照合し不一致0。表現差（P(13)/P(15)の{18,20}∪I[22,
  vs {18,20,22}∪I[23,、P(17)/P(19)の同型）はすべて同集合。
  （2）生再帰オラクル: 順序保持・降順正準化の再帰がK1076閉形式と
  x<=60・R<=x+46で一致（各4,503）。K1067/K1064の出版済み子転写は
  子局面の生再帰とx=3..60/x=4..60で一致（9,106/9,006点・転写リスクの遮断）。
  （3）K1076署名帯表は生再帰署名とx<=95・R<=x+21の6,486点で一致し、
  帯の構造的被覆（隣接・上端・行×偶奇184）も成立。mex対応がK1076閉形式
  と全域一致。（4）帰納ステップ閉包掃引（K1076形式でx<=5000・R<=x+21・
  12,607,406点）と閉包基底（x=4・多重度合流・25点）が成立。
  （5）高さのみ縮約はK0832証明済み域R<=18（1,748点）で成立し、R=19..21は
  観察として成立（276点）、最初の反例はx=14行R=22（Witness照合込み）。
  tailはR>=x+22で(x+4) mod 2（4,140点）。（6）第三実装census
  （明示dict memo・着手を値ごとに列挙・lru_cacheなし・閉形式を知らない）
  がx=4..45・R<=x+45の2,961点を全分類しK1076閉形式と不一致0。
  （7）検証器の決定論: 2回実行+別cwd別プロセスでaudit.jsonがbyte-identical、
  census.txtもbyte一致。合計17,254,465照合・不一致0。
  （8）K1076パッケージ自体の再実行: repo HEADのK1076検証器をbyte-exactに
  取得して実行すると監査の数学的内容（12,693,293照合・status pass・
  不整合リスト空）は完全再現する。しかしコミット済み検証器の実SHA-256
  はa7878b8e…であり、コミット済みaudit.jsonのverifier_sha256フィールドと
  report.mdのpin（388e1a47…）は不一致。すなわち現HEADではCIのK1076監査
  ステップは原理的に通らず、コミット済み監査はrepoに存在しない版の検証器
  が生成したもの。数学的監査内容は現行検証器でも再現するためK1076の定理
  健全性への影響はない。修正はK1076レーンの管轄。なおKnowledge integrity
  の完了実行は2026-11-19 20:19-20:34Zで15連続failure（K1076出版前から
  別系統の障害が存在、fail stepの特定は行っていない）。有限監査は全称
  証明の代わりではなく、K1076の全称性は引き続きx外帰納と全R署名帯表による。
---

## 詳細

本レーンは z=17・y=4 の単一オーナー宣言ノート（commit 71485e4c）を出版後、
並走実行が同じ切片を K1076 として出版したことを検出した。本レーンが独立に
導出・監査まで完成させていた成果の、K1076 との全行一致（表現差はすべて
同集合）と、第三実装による 2,961 点の再導出一致を第二検証として計上した。
重複itemの出版は行っていない。あわせて、K1076 パッケージの byte-pin
不整合（コミット済み検証器 a7878b8e… vs コミット済み監査の pin 388e1a47…）
を検出・報告した。出版済み K1076 検証器の再実行で監査の数学的内容は
完全再現するため、定理の健全性への影響はない。新しい全称主張はない。
次の候補は z=17・y=5（B=K1076・C=1⊕K1074）、z=18・y=4（B=K1078・
C=1⊕K1076）。着手前に単一オーナー宣言の有無を確認する。
詳細は[報告](../experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/report.md)・
[研究ログ](../log/2026-11-20-vertical-fiber-two-token-z17-y4-second-verification.md)。
