# n11 S5 frontier census・グローバルcache union監査・reconciliation測定: 単一オーナー宣言ノート

Date: 2026-11-21T14:42Z
Lane: n11 S5 frontier census + global s5verdict cache union audit + backlog reconciliation 測定レーン
Declaration HEAD at write time: `a423c2f01c4e23874a2bf668cfa019bc244d188d`（2026-11-21T14:38Z時点の最新main）。
Prior snapshot base: codeload tarball HEAD `0a76535f98f9df883b376b2987fd44780b542fc3`（union audit の入力スコープはこのtree時点で固定）。

## 宣言する作業（first-published-priority）

本レーンは、他のどの並走レーンにも現時点で宣言されていない**測定・監査**作業を排他的に担当する。

(a) **S5 frontier census**: 現行の published chain（reply27 S5 JS-replica probe-1〜13 merged cache）を固定入力とし、(i) 13段のcache chain形式検証（行数単調・挿入鍵記録・strict sort・SHA-256 pin一致）、(ii) active候補クラスのclosure距離表と単一/複数live親供給のdegree分布、(iii) quarantine registryに基づく供給blocker検査、(iv) focusレーン宣言35鍵の機械的3点検証、を計算する。

(b) **グローバルs5verdict cache union監査**: snapshot `0a76535f` 時点のtreeに存在する全s5verdict cacheファイル（326ファイル・760,504行）を走査し、ファイル内同一鍵verdict矛盾・グローバルWIN/LOSS衝突・quarantine鍵の現行chain不在を検査する。判定・merge・rehabは一切しない。

(c) **backlog reconciliation測定**: 現行chainにもquarantineにも存在しないが過去のpublished exact/merged cacheに存在する行（"backward-only"行）を特定し、現行active供給への帰属・クラス別減算・採用仮定（if-adopted）の候補分布変化・再計算費用概算を測定する。**歴史行の採否・判定は行わない。**判定は証拠オーナー（reply27 two-targetレーン、focus-classレーン、K0414/K0416の系譜所有者）に付託する。

(d) **proxy較正**: published probe raw（2M/15M段階）とcensusのtruncated-cost proxyを対照し、nodes/proxy比の分布を記録する。

(e) **出版**: 実験dir（scripts 3 + output 3 + README）・本宣言ノート・session log・`research/experiments/n11-search-methods/README.md` への参照行1行追加。K itemは作成しない（worker-partition測定レーンの先例に従う）。車輪の再発明防止のためREADMEで上記オーナー付託を明記する。

## 触れないもの（他レーンの焦点）

- reply27 two-target S5 probeレーンの13 probe dir・merged cache・今後のprobe（live_parents>=2鍵）には書き込まない。
- focus-class exclusive single-live-parent S5 probeレーン（宣言済み35鍵）の鍵は**検証のために読むのみ**で、探索・進行はしない。
- K0414/K0416/K0374/K0379/K0355 等、knowledge itemsの本文・status・relationsは変更しない。
- `n11-s4-boundary-direct-20261012` および Oct 11〜12のpublished cache群は入力として読むのみ。
- いかなるs5verdict cache・merge・quarantine registryへの書込も行わない。

## 受入条件（fail-closed）

1. 全入力はSHA-256 pinで検証し、不一致は即時abort（rc!=0）。chain cacheの行verdict反転のような入力改変にもfail-closedであること（負対照で確認済み: 反転→rc=1）。
2. 3スクリプトとも fresh 2回実行で output byte 一致（決定性）。
3. `py_compile` 全PASS。
4. push後、commit固定raw URLでfetch-backし、sha256がローカル正本と byte 一致すること。`n11-search-methods/README.md` は既存行を1行も変えず末尾に1行（節見出し含む最小追加）のみ。
5. pushは最新main再取得後に行い、競合・同時書込みが起きた場合は無理せず記録して次回に回す。

## 勝敗の取り扱い

本レーンはいかなる勝敗も主張しない。node数・proxy・closure距離はscheduling測定であり判定ではない。標準11×11空盤・二石root {60,27}・第三手100/108は本レーンの後も UNKNOWN のまま。
