---
id: K1032
title: "head-1410残余48rootのdepth-10全面判定と第2・第3 WIN7-D10証明書、REFUTED除外後の5親target再解決"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - n11 residual 48 root depth-10 sweep
  - n11 second third WIN7-D10 receipts
  - refuted-excluded five-parent cover resolve
  - residual 38 stranded rows
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0007
  note: ranked AND/OR certificate の構造と検証境界
- type: depends_on
  target: K1029
  note: 第1WIN7-D10 receipt fold に直接 chain する frontier 状態
- type: depends_on
  target: K0865
  note: receipt-unclosability census による parent/demand 簿記
- type: depends_on
  target: K0863
  note: 49候補rootの公開verdict index非所属判定
- type: supports
  target: K0865
  note: 5親target残余の実効 vertex cover を depth-10 候補プールで確定
artifacts:
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/win7-root-00000000000000821082000000042000-20261119.n11
  role: certificate
  note: 34,003行。SHA-256 1af547c0772eab4f5ffb7925a732b01960ffeb7bb0f970d67ee551143b34acf5
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/win7-root-00000000000000821082000000420000-20261119.n11
  role: certificate
  note: 42,896行。SHA-256 aad19dff25c1ee7b74b2e81f0b53ef41b21977d50446a52aa9c79a2ab6457205
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-sweep-20261119.json
  role: data
  note: 48root×2順序（cap 950k/4M/16M昇格含む134プローブ）の全面判定。WIN7-D10 2 / REFUTED-D10 46 / CAPPED 0
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/second-third-win7-root-receipt-fold-20261119.json
  role: data
  note: receipt fold。S6行7件閉鎖、frontier 6229行/493184
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/five-parent-refuted-excluded-cover-resolve-20261119.json
  role: data
  note: REFUTED除外後の再解決。63候補で53行カバー可能、38行stranded
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/
  role: source
  note: extract/verify/fold/sweep-audit/cover-re-solve の5 driver。入力は Git blob SHA-1 で pin
- path: research/log/2026-11-19-n11-residual-48-root-sweep-second-third-win7-receipts.md
  role: log
  note: sweep・証明書・fold・再解決の実行記録と未解決範囲

scope: >-
  head-1410 5親targetの残余候補root（49-root cover から第1WIN7 receipt root
  00000000000000821082000010800000 を除いた48本）に対する depth-10 探索の
  全面判定、うち2本の WIN7-D10 証明書とその receipt fold、および
  REFUTED-D10 46本を候補プールから除外した後の 5親target 再解決。
  7石root個別のdepth-10勝敗判定であり、二石root・空盤・クラスの勝敗は対象外。
evidence: >-
  depth-10 runner v17（cap 950,000、950kで少なくとも一方の順序がcappedの
  16rootを4M、さらに両順序cappedの3rootを16Mへ昇格）で48root・134プローブを
  実行し、pilot_d6 control 全件 3,402 nodes で一致。
  WIN7-D10 は 00000000000000821082000000042000（55応手、両順序で
  loss=trueの完全走破 935,332/665,812 nodes）と 00000000000000821082000000420000（59応手、
  andclose1 875,721 nodesでloss=true、andclose0は950k cappedで反証なし）。
  両rootの証明書を v16 extractor
  で抽出（fbt_drops=0）、BigInt 3×3余因子展開と4×4 Bareiss の独立検査が
  全 subroot PASS、消費集合と証明書行の差分は0、両方式の状態流量が完全一致。
  残る46rootはいずれも少なくとも一方の順序で未打切り loss=false の完全探索
  （うち25rootは両順序で完全探索）で REFUTED-D10。CAPPED は 16M でも 0。
  receipt fold は S6行7件（target内4件）を閉じ、frontier は 6,229行/493,184、
  solved_s6 1,619。REFUTED除外再解決では pool 117root のうち既知5+sweep46の
  51本が refuted、3本がWIN receipt となり、残る63候補のpair edge 44・
  singleton行14で最大マッチング25（50行）+singleton対応3行の計53行のみがカバー可能、
  残る38行は当該117rootプール内のdepth-10候補ではstranded。
---

## 命題・範囲

head-1410 5親targetの残余48候補root の depth-10 判定が確定した。

- 00000000000000821082000000042000 は標準11×11の通常ルールで先手勝ち
  （WIN7-D10）。55個の合法な後手初手を全て含む戦略証明書34,003行。
- 00000000000000821082000000420000 は標準11×11の通常ルールで先手勝ち
  （WIN7-D10）。59個の合法な後手初手を全て含む戦略証明書42,896行。
- 残る46root はいずれも depth-10 で先手の勝ちが存在しない（REFUTED-D10）。
  ただし REFUTED-D10 はそれら7石rootからの「depth-10内の勝ちなし」の証明で
  あり、当該root以前の任意の局面に対するLOSS証明ではない。

これら2枚の receipt で5親targetの行が追加で4行閉じ、累計21/112行となる。
残る91行について、REFUTED 46本を候補から除外して再解決すると、117root
プール内の残候補（63本）でカバーできるのは53行のみで、38行は
この候補プールのどの7石rootでも_span 2以内のWIN7候補としてカバーできない。

## 現在の根拠と限界

探索は runner v17（fbt probe枯渇時の直算fallback修復済み）で depth-10、
AND順序 andclose=1/0 の双方を cap 950,000 で実行し、両順序で cap に達した
16rootのみ cap 4,000,000、さらに両順序で cap に達した3rootを cap 16,000,000
へ昇格した。全134プローブで pilot_d6 control（loss=false, 3,402 nodes）が
一致し、順序間でWIN/REFUTEDの矛盾は0件。46 REFUTEDはすべて少なくとも片側
順序で未打切り loss=false（完全探索）である。

2つのWIN rootの証明書は独立に二方式で検証した。BigInt 3×3余因子展開検査は
root安全性・legal next moves（55/59）・全 subroot 合格・証明書行と消費行
集合の差分0。4×4 Bareiss 検査は同数の subroot で消費連結が完全一致し、
seen/terminals/opponent_edges の総計が両方式で一致した。fbt_drops は抽出
全体で0。

receipt fold は第1WIN7証明書（K1029）の receipt fold が chain している
frontier（6,236行/493,703）に直接接続し、receipt行のopen性・d4再導出行の
一致・target行joinを全て再検証した上で7行を閉じた。
parent incidence は 11,876 → 11,859。

再解決では、これまでの明示的verdictソース（236 REFUTED/156 WIN）の再現、
sweepによる46 REFUTED + 第1receipt rootのWINを追加した際の pool 内訳
（refuted 51・win 3・eligible 63）、111...112行targetの行閉鎖計21行、
残91行について pair edge 44・singleton 14・最大マッチング25・stranded 38行
を Edmonds blossom による厳密最大マッチングで確定した。

限界は次の通り。

- REFUTED-D10 は LOSS 証明ではない。swept root 以前の局面の勝敗は不明のまま。
- 再解決の verdict join は明示的ソース限定であり、8,964件の全verdict
  キャッシュの完全joinではない（これはK1029以前と同一の限界）。
- stranded 38行は「この117root候補プール内の span≤2 の7石候補では
  depth-10 WIN7 receipt として閉じられない」ことを意味する。
  候補生成の拡張、depth 10 を超える証明、または別の閉鎖機構が必要であり、
  行が数学的に閉じられないことが証明されたわけではない。
- manifest の solved_s6 は 1,619/7,860 であり、5親targetは距離の遠い
  到達点にすぎない。

## 11×11 全体への影響

標準11×11の空盤、二石root {49,60}/{59,60}、S2 {59,60}、クラス1/2/4は
いずれも UNKNOWN のままである。本項目の計算は個別7石rootの depth-10
判定であり、空盤の勝敗には直接言及しない。

## 次の一手

- 再解決 witness 28root（53行分）を優先的に sweep すれば、stranded 38行
  以外の行の depth-10 到達可能性が確定する。
- stranded 38行に対しては、候補root生成の拡張（異なる parent 集合・異なる
  初手構造）、depth 11 以上の探索、または行需要の parent 再構成が必要。
