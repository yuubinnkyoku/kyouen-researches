---
id: K0787
title: 貪欲＋破壊再構成と温暖開始の反復でQ_2531は1258点以上、Q_3251は1606点以上の安全集合を持つ（独立整数幾何監査済み）
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線・共円四点を含まない安全集合の定義
- type: depends_on
  target: K0771
  note: 禁止四点リストが健全・完全・重複なしであることを前提に、辺の非包含で安全性を判定
- type: supports
  target: K0781
  note: A(2531)<=1265 と合わせて 1258 <= A(2531) <= 1265
- type: supports
  target: K0775
  note: A(3251)<=1625 と合わせて 1606 <= A(3251) <= 1625
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/build_safe.cpp
  role: solver
  note: 貪欲＋ruin-and-recreate（探索器。出力は証人であり最適性の証明ではない）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/audit_safe_set.py
  role: verifier
  note: 辺の非包含と独立generic 4x4 Leibniz検証器の二重検査、入出力hash保存
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_2531.json
  role: certificate
  note: 1246点（形状(1,1,21)、辺0件）。点は(t,t² mod 2531)
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_3251.json
  role: certificate
  note: 1598点（形状(1,1,29)、辺0件）。点は(t,t² mod 3251)
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_2531_1258.json
  role: certificate
  note: 1258点（形状(1,1,9)、辺0件、完全対1061）。温暖開始SATの反復でさらに2点伸ばした最新形
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_2531_extended.json
  role: certificate
  note: 1256点（形状(1,1,11)、辺0件）。貪欲1246を温暖開始SATで10点伸ばした最終形
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_3251_1606.json
  role: certificate
  note: 1606点（辺0件）。温暖開始SATの反復で1603からさらに3点伸ばした最新形
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_3251_1603.json
  role: certificate
  note: 1603点（辺0件）。温暖開始SATの反復で1601からさらに2点伸ばした最新形
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/witness_3251_extended.json
  role: certificate
  note: 1601点（形状(1,1,26)、辺0件）。貪欲1598を3点伸ばした最終形
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/audit_2531.json
  role: data
  note: 2531の監査生出力（99,946,516,285四点を被覆、39,548,349候補の行列式が非零）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/greedy-lower-bounds/audit_3251.json
  role: data
  note: 3251の監査生出力（270,684,896,405四点を被覆、83,362,522候補の行列式が非零）
- path: research/log/2026-11-13-greedy-lower-bounds-2531-3251.md
  role: log
  note: 手法・較正（2207/2647）・限界
scope: p=2531 と p=3251 の二点集合。下界のみで、A(p) の正確な値は主張しない。
evidence: 4素数で同じ構成器を走らせ、2207は1085（既知の最大1104の98.2%）、2647は1292（既知の下界1303の99.2%）と較正した上で、2531は1246・3251は1598（その後、温暖開始SATの反復で1258・1606へ）。両方とも辺0件かつ独立検証器が受理（verifier_rc=0）。
---

## 主張

- `A(2531) >= 1246`
- `A(3251) >= 1598`

## 手法

禁止四点は4一様超グラフとして非常に疎（p=2531 で 837,640 辺 / C(2531,4) ≈ 1.7×10¹²）なので、
「辺を完成させる点を拒否する」貪欲だけで最大値の98%前後に届く。そこへ **ruin-and-recreate**
（無作為に k 点を除いて貪欲で埋め直し、良ければ採用）を重ねる。実装は `build_safe.cpp`。

| p | 得られたサイズ | 形状 `(x,c,e)` | 既知の上界 | 到達率 |
|---|---|---|---|---|
| 2207 | 1085 | `(1,1,20)` | 1104（K0722） | 98.2% |
| 2647 | 1292 | `(1,1,33)` | 1322（K0711） | 97.7%（既知下界1303は別手法） |
| **2531** | **1246** | `(1,1,21)` | 1265（K0781） | 98.5% |
| **3251** | **1598** | `(1,1,29)` | 1625（K0775） | 98.3% |

- 2207 と 2647 は真値（または最良の既知下界）が分かっている較正用。2531・3251 の数値は新規。
- パラメータは 20,000 ラウンド・ruin 80・seed 13 で固定。1 素数あたり 2〜5 分。

## 独立監査

`audit_safe_set.py` が二重に検査する:

1. 禁止四点リスト（K0771 で健全・完全・重複なしが証明済み）に全包含する四点が無いこと。
2. `parabola-local-repair-20261109/verify_subset.cpp`（generic 4×4 Leibniz 整数行列式・
   探索器とコード非共有）が受理すること。

4 素数すべてで `edges_inside=0`、`verifier_rc=0`。2531 は 99,946,516,285 四点を被覆し
39,548,349 候補の行列式が非零、3251 は 270,684,896,405 四点を被覆し 83,362,522 候補が非零。

## 限界

- 下界のみ。`A(2531) <= 1265`・`A(3251) <= 1625` との間に 19・27 の幅が残る。
- 出力はヒューリスティックの到達点であり、最適性の証明ではない（ラウンドを増やせば伸びうる）。
- 形状はいずれも `(1,1,e)`（原点＋一完全対＋e 空対）。目標サイズ `h` には `e=2` が必要なので、
  今の貪欲が自然に選ぶ `e≈20` からは構造的に遠い。SAT の温暖開始で詰めるのが次の一手。
