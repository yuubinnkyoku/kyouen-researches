---
id: K1146
title: 残余23行の代替9根depth-10掃引: WIN8-D10 candidate 1根・REFUTED-D10 fact 8根（累計WIN候補17根・第5ラウンドpool P⁗ 120,416根・行閉鎖0）
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - both-AND-order depth-10 verdict sweep (18 probes, runner v17 git blob c132cc64…) of the K1097 scope1 greedy 9 replacement roots covering the residual-23 rows (plan minimality over pool P''' established by the eight-root-cover-decision experiment)
  - WIN8-D10 candidate 00000000010000809002000040002001 (uncapped loss=true in both orderings, 608,293/691,784 nodes, claimed 3 rows of the residual 23)
  - REFUTED-D10 facts 8 roots (claimed 20 rows); cumulative REFUTED-D10 pool 16+13+12+9+8 = 58, round-5 pool = safe8 120,474 - 58 = 120,416 roots; zero row closure in this sweep
relations:
  - type: depends_on
    target: K1097
    note: 置き換え対象9根（scope1_refsolve_residual23.greedy_selection）と残余23行の供給源。scope1==scope2同一選定のcrosscheckに使用
  - type: depends_on
    target: K1095
    note: K1095 verdict join・残余23行（WIN3根主張7行+REFUTED9根主張23行）の連鎖再導入元
  - type: depends_on
    target: K1091
    note: 残余30行の連鎖再導入元（replace15掃引）
  - type: depends_on
    target: K1089
    note: 残余40行の連鎖再導入元（replace16掃引）
  - type: depends_on
    target: K1086
    note: 残余49行の連鎖再導入元（addtwo greedy23掃引）
  - type: depends_on
    target: K1085
    note: 残余72行base state・add-two-stones census
artifacts:
  - path: research/experiments/n11-residual72-replace9-d10-sweep-20261120/README.md
    role: source
    note: 対象・入力pin・再現方法・解釈上の制限
  - path: research/experiments/n11-residual72-replace9-d10-sweep-20261120/scripts/replace9_d10_sweep_20261120.py
    role: verifier
    note: 掃引機械（run/assemble・20 gate・SHA-256 pin・resume-safe）
  - path: research/experiments/n11-residual72-replace9-d10-sweep-20261120/output/replace9-d10-sweep-20261120.json
    role: data
    note: 正本JSON（SHA-256 e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e・20 gate PASS・byte-identical 3実行）
  - path: research/experiments/n11-residual72-replace9-d10-sweep-20261120/output/probe-records-replace9.jsonl
    role: data
    note: 18 probe記録（pilot_d6制御つき・resume-safe正本の入力）
  - path: research/experiments/n11-residual72-replace9-d10-sweep-20261120/runner_v17.ts
    role: verifier
    note: runner v17 repo原本固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・SHA-1一致検査済み）
  - path: research/log/2026-11-20-n11-residual72-replace9-d10-sweep.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 51bbb938・先行出版）
scope: >-
  K1097残余23行をleftover 0で完全被覆するgreedy代替9根（P‴上で候補根数最小と
  判定実験で確定済みの計画）に対するdepth-10 verdict探査18 probes（両AND順序・
  runner v17・cap 30M・timeout 280s・pilot_d6制御必須）のみを対象とする。
  残余23行宇宙はK1085→K1086→K1089→K1091→K1095の連鎖から本機械内で独立に
  再導入する。行の閉鎖claim・receipt fold・証明書抽出は対象外。
  REFUTED-D10はLOSS証明ではなく、node数を勝敗として読まない。
evidence: >-
  18/18 probes完走・capped 0・error 0・順序間矛盾0・全20 gate PASS
  （入力6正本SHA-256 pin・runner git blob pin・残余49/40/30/23行の連鎖独立再導入・
  K1097帳簿との23行一致・scope1==scope2選定一致・9根popcount8・quadruple-free・
  D4 min-canonical・claimsのD4方位と部分集合・23行exactly-once被覆・
  gains hist {3:6,2:2,1:1}・child=root−最小セットビット再構成・全probe
  pilot_d6制御PASS）。WIN8-D10 candidateは
  00000000010000809002000040002001ただ1根（両順序uncapped loss=true・
  nodes 608,293/691,784・terminal [14,18]・gained 3）。REFUTED-D10 8根は
  00000000000000083800040048100000・00000000000000143800000209000000・
  00000000000000821082000000001018・00000000000000821086800000000800・
  00000000000040809002000800100200・00000000000000103800000008080041・
  00000000020000801202000800100001・00000010000000801202000000000448
  （gains {3:5,2:2,1:1}・主張20行）。nodes総計3,574,172。
  probe再実行4件（WIN両順序+REFUTED 1根両順序）でnodes/loss/capped/
  terminalStoneRangeが正本記録と完全一致。assembleは同一cwd2回+別cwd別HOME
  1回の3実行でbyte-identical（正本SHA-256
  e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e・
  15,403 bytes・実行約13.3秒/掃引）。
---

## 結論

K1097第4ラウンドgreedy計画の代替9根のうち、**WIN8-D10 candidateは1根**
（`00000000010000809002000040002001`・主張3行）、**REFUTED-D10 factは8根**
（主張20行）。累計WIN8-D10 candidateは17根（主張52行）、累計REFUTED-D10は
58根となり、第5ラウンド再解決poolは safe8 120,474 − 58 = **120,416根**、
次ラウンドの代替被覆対象は残余23行のうち20行。本掃引で行は1行も閉じない。

## verdict表（正本per_rootから）

| root | gained | andclose1 | andclose0 | verdict |
| --- | --- | --- | --- | --- |
| `00000000000000083800040048100000` | 3 | 11664 / false | 80912 / false | REFUTED-D10 |
| `00000000000000143800000209000000` | 3 | 572204 / false | 292251 / false | REFUTED-D10 |
| `00000000000000821082000000001018` | 3 | 53667 / false | 74966 / false | REFUTED-D10 |
| `00000000000000821086800000000800` | 3 | 42629 / false | 23112 / false | REFUTED-D10 |
| `00000000000040809002000800100200` | 3 | 120916 / false | 81137 / false | REFUTED-D10 |
| `00000000010000809002000040002001` | 3 | 608293 / true | 691784 / true | **WIN8-D10 candidate** |
| `00000000000000103800000008080041` | 2 | 13781 / false | 242618 / false | REFUTED-D10 |
| `00000000020000801202000800100001` | 2 | 11535 / false | 126875 / false | REFUTED-D10 |
| `00000010000000801202000000000448` | 1 | 148782 / false | 377046 / false | REFUTED-D10 |

（nodes / loss。すべてuncapped・順序整合。

## 証明状態の区別

- WIN8-D10 candidate 1根: depth-10内必敗のprobe事実。証明書抽出・独立二重検証・
  8石receipt foldを経るまでは行閉鎖に使えない（別の単一オーナー宣言を要する）。
- REFUTED-D10 8根: depth-10内必勝不存在のprobe事実。LOSS証明ではなく、
  代替候補poolの浸食（120,424→120,416）にしかならない。
- 本掃引のいずれの結果も行のゲーム理論的値を確定しない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
UNKNOWN のまま。** 残余72行は全行open。

## 次の一手

- 第5ラウンド再解決: pool P⁗（120,416根）上での残余20行greedy計画・下界・
  計画最小性の確認（着手時に単一オーナー宣言を要する）。
- 新WIN8-D10 candidate 1根の証明書抽出: 1根単位の宣言と独立二重検証
  （累計17 WIN候補の証明書抽出・receipt foldは並走レーン管轄の個別宣言に従う）。
- 証明書抽出・foldの進捗に応じて残余需要を再計算してから第5ラウンド計画を作る。
詳細は[実験](../../experiments/n11-residual72-replace9-d10-sweep-20261120/README.md)・
[掃引正本](../../experiments/n11-residual72-replace9-d10-sweep-20261120/output/replace9-d10-sweep-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-replace9-d10-sweep.md)。
