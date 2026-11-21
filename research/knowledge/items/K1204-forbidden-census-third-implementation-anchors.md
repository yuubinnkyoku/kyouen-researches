---
id: K1204
title: 禁止四点組センサスの第三実装（正準化円キー＋Cramer整数算術）はn=5..13の全出版アンカーに全面一致 — F・D/C分解・曲線カタログ規模・円グループ一貫性の9/9行PASS
kind: verification
status: verified
topics: [geometry, verification, maximal-safe]
aliases: ["s12/s13 lane census gate", "census third implementation"]
relations:
- type: verifies
  target: K0057
  note: "全ての非共線3点組から円方程式x^2+y^2+Dx+Ey+F=0の(D,E,F)/detをZ上で既約正準化してキー化・グループ化する第三実装（Node.js、全整数算術）が、F_5..F_13（826..252,362）、D/C分解n=9..13（3,156/25,996..27,340/225,022）、ライン/円カタログ規模n=10..12（154/232/326本・12,170/20,847/34,031個）、段階的曲線カタログのC(m,3) triples一貫性ゲートをすべて再現（9/9行、anchorIssues空配列）。K0057の本文・statusは不変"
- type: related
  target: K0320
  note: "本項のcensusはs12/s13上界レーンの全機械（quartet展開・Stateカウンター・ nets/probe2/SLS）の較正ゲートとして機能した。1つでもアンカー乖離があればレーンの探索結果はすべて無効化されるfail-closed設計"
artifacts:
- path: research/experiments/s12-s13-upper-witness-20261121/scripts/census.mjs
  role: verifier
  note: "第三実装正本。原始方向のみの最大直線列挙＋正準化円キーによる3点組→円グループ化＋quartetList（F_nとの|Q|一致を表明）＋K0057出版アンカー照合"
- path: research/experiments/s12-s13-upper-witness-20261121/records/census_check_n5_13.json
  role: data
  note: "n=5..13の9行全フィールド（F/D/C/lines/circles/triples/circleConsistency/anchorIssues/ヒストグラム）機械可読出力。anchorIssues 9/9で空配列"
- path: research/experiments/s12-s13-upper-witness-20261121/README.md
  role: source
  note: "検証方式・限界・開発中にアンカーゲートが検出した2バグ（水平方向(a,0)の非原始重複、gcd(0,0)=0正準化）の誠実記録"
---

# 禁止四点組センサスの第三実装: n=5..13全出版アンカー一致

## 検証対象と範囲

K0057の出版アンカー集合（F_n n=5..13、D/C分解 n=9..13、4点以上曲線カタログ規模 n=10..12）を、独立に書いた第三の実装で全再現した。手法は3点組→円方程式の正準有理数キー化（(D,E,F)/det を Z 上で既約化し det>0 に正規化、原点中心円で gcd(0,0)=0 の扱いが正準性に必須）で、キーの衝突・非正準化は即F/D/Cのどれかの乖離として現れる。直線は原始方向 (a,b) の families a·y−b·x の最大点集合として一度だけ数え、部分線分の重複排除は出版方式と同一。

結果: 9/9行で全比較フィールドが出版アンカーと厳密一致、円グループのpoint数mとtriples数の恒等式 C(m,3)=triples は全nで成立（circleConsistency true、開発中にこのゲートが2件の実装バグ (a)水平方向の非原始重複によるD_9過大計数、(b)gcd(0,0)誤りによる原点中心円キー非正準化とF_9過大 +2 を検出・修正済み）。

## 限界（検証水準の明示）

- 第三実装は「3点組→円方程式→グループ化」という系A系譜の別実装であり、s11レーンのcensus_a.pyと手法系統を共有する。同一系譜の共通誤りはアンカー一致で検出できない。真に手法が独立なのは半格子中心スキャン（circ_catalog_scan.py、中心×半径族から円を作る）であり、7点以上円のn≤12一致はK0057本文の既出版検証のまま。本項はこの独立系を再実行していない。
- 算術はすべてn≤13で2^53未満の整数積に収まるため倍精度浮動小数点でも厳密だが、実装は整数のみを使用する。
- n≥14の走査は本レーンの非目標（データ取得のみで記録していない）。n=12,13はレーンの探索機械に直接便宜する範囲として較正した。
- 本項はいかなるs_n値も・単調性も主張しない。checked・ms数は判定ではない。
