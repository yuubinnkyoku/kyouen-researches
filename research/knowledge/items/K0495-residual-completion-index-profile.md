---
id: K0495
title: completion索引による残余構築は固定局面で従来scanと一致し、構築費用を削減した
kind: computation
status: observed
topics: [residual-games, search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0493
  note: 監査済み残余評価kernelはそのまま用い、入力構築だけを比較
- type: depends_on
  target: K0494
  note: 同じ固定52局面と深い3局面で構築費用を分解して再測定
artifacts:
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: completion索引によるrank 2/3/4列挙、従来scan、仕事量見積もりによる切替と排他的profile
- path: cpp/tests/test_kyouen_residual_builders.cpp
  role: verifier
  note: 全安全4×4占有、64ビット境界、全826保存局面で辺族と子遷移を比較
- path: research/experiments/residual-phase-profile-20261021/README.md
  role: log
  note: 同値性の理由、固定プロトコル、費用の定義、再現手順と限界
- path: research/experiments/residual-phase-profile-20261021/builder-audit.json
  role: certificate
  note: 入力hashと有限比較の完了出力
- path: research/experiments/residual-phase-profile-20261021/comparison.md
  role: data
  note: 保存測定から生成したphase内訳とprofile OFFの3回比較
- path: research/experiments/residual-phase-profile-20261021/verify_outputs.py
  role: verifier
  note: 入力hash・各行勝敗・予算・計測内訳・全保存結果の再集計
- path: research/experiments/residual-phase-profile-20261021/build-provenance.json
  role: manifest
  note: compiler、binary hash、実装commit、測定順と実行条件
---

## 対象と結果

K0494と同じ独立期待値付き52局面と深い3局面を固定し、残余構築、構造処理、
残りのGrundy評価を重複しない区間で計測した。従来scanの構築は、閾値6/12で
52局面では残余評価内訳合計の97.8%/79.3%、深い3局面では98.3%/64.4%だった。

completion索引を用いて、legalに2/3/4点が残る禁止四点組だけを列挙する構築を追加した。
構築時間はこのprofileでは52局面で49.2倍/13.5倍、深い3局面で105.2倍/28.0倍の短縮。
profileの時計呼出し費用を含むため、探索全体の性能比較とは分けて解釈する。

4×4の全65,536占有maskのうち安全な5,811局面、8×8の空盤と1点占有、
11×11の保存済み826局面で、従来scan、索引方式、auto選択のlabelled極小辺族が一致した。
安全な4×4全局面と8×8の1点占有と11×11全826局面では各合法手の子も比較した。
残余playと盤面から直接再構築する子の頂点・辺族も一致。通常buildとUBSanで完了した。

## 時計を外した探索全体の比較

各局面を3回測定し、局面ごとの中央値を合計した（初期化を除く、共有cacheなし）。

| 対象 | 閾値 | 従来scan | 索引方式 | 削減率 |
|---|---:|---:|---:|---:|
| 固定52局面 | 6 | 37.734 ms | 6.308 ms | 83.3% |
| 固定52局面 | 12 | 25.674 ms | 9.532 ms | 62.9% |
| 深い3局面 | 6 | 2671.000 ms | 95.320 ms | 96.4% |
| 深い3局面 | 12 | 8668.751 ms | 3301.431 ms | 61.9% |

両builderのOFF/6/12を3反復、計990根評価で、52局面は全て独立期待値と一致し、
深い3局面は全設定・全反復UNKNOWNだった。同じ設定の探索ノード数も両方式で一致。
内訳profileも含む保存1210行は入力hash・予算・勝敗・再集計を検査済み。

OFFは別時間帯の2測定で52局面6.951/7.094 ms、深い3局面26.198/26.354 ms。
索引方式の閾値6は52局面ではOFFと同程度だったが、深い3局面では約3.6倍の費用が残る。
一行あたり約0.5秒の初期化費用は別途必要で、ここでの改善率を起動からのwall時間の
改善率とは解釈しない。builderごとの測定は時間を交互にせず順に実施したため、
小さい時間差への統計的有意性は主張しない。

## 採用範囲と限界

構築方式は既定autoとし、組合せ数による粗い仕事量見積もりで索引方式またはscanを選ぶ。
残余handoffの既定値は0（OFF）を維持する。構築が速くなっても、完全Grundy計算と
既存の勝敗探索では仕事が異なり、深い局面の時間やUNKNOWNが必ず改善するわけではない。

外側予算は各根5000 nodesで、kernel内部の仕事を数えない。初期化は探索時間から分離。
性能は単一host・固定コーパスの観測で、未知盤全体への一般化や11×11空盤の解決を意味しない。
K0494の測定は旧builderについての歴史的観測として保持する。
