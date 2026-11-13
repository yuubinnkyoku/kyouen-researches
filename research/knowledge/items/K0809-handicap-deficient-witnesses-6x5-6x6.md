---
id: K0809
title: "行capハンディキャップ貪欲による欠損witness — M_{6,5}≥22・M_{6,6}≥17（下界更新）"
kind: computation
status: computed
topics: [rectangles, maximal-safe, verification, geometry]
aliases: []
scope: "6×m整数格子・q∈{5,6}。(6,5) m=20,21 に23石・(6,6) m=16 に29石の極大安全配置（石数<満容量・欠損witness）の実在。独立検証による存在証明であり、不在は主張しない"
evidence: "行capハンディキャップ貪欲+shake（K0808機のcensus・独立検証ロジックはverbatim）で発見し、census不使用の独立検証（石ペア直線・石3点組外心の全列挙・厳密整数演算）で全witnessが safe+maximal PASS。制御: (6,6) m=15 で29石witness再発見"
relations:
- type: extends
  target: K0808
  note: K0808の貪欲では発見できなかった m=20,21（6,5）と m=16（6,6）に行capハンディキャップで到達し、下界 M_{6,5}≥20→22・M_{6,6}≥16→17 を更新
- type: supports
  target: K0806
  note: (6,5)/(6,6) の境界を [22,658]/[17,495] に更新
- type: depends_on
  target: K0808
  note: census（3点組外心完全列挙）と独立検証器の実装をverbatim流用
artifacts:
- path: research/experiments/handicap-deficient-witnesses-20261113/scripts/handicap_deficient_machine.ts
  role: source
  note: 行capパターン付きハンディキャップ貪欲機（freeリスト保守でのcap再チェック必須という教訓込み）
- path: research/experiments/handicap-deficient-witnesses-20261113/output/scan_results.json
  role: data
  note: witness座標・独立検証詳細・抵抗記録・制御
- path: research/experiments/handicap-deficient-witnesses-20261113/report.md
  role: proof
  note: 主結果表・抵抗表・候補予想・レジューム
- path: research/log/2026-11-13-handicap-deficient-witnesses.md
  role: log
  note: 発見順・バグ1件・抵抗の経緯
---

## 命題（計算された事実）

6×m 整数格子・q点共円共線禁止版において:

1. **(6,5)**: 6×20 と 6×21 の各々で石数 23 < 24（満容量）の極大安全配置が存在する
   （独立検証 safe+maximal・worstLine=worstCirc=4・unblocked=0）。
   K0808 の m=8..19 と合わせて m=8..21 の連続 witness 鎖となり、
   真の安定化長 **M_{6,5} ≥ 22**。
2. **(6,6)**: 6×16 で石数 29 < 30 の極大安全配置が存在する（同様に独立検証 PASS）。
   K0808 の m=8..15 と合わせて **M_{6,6} ≥ 17**。

K0806 の上界と合わせて M_{6,5} ∈ [22,658]・M_{6,6} ∈ [17,495]。

## 根拠

- 手法: 極大化の際に一部の行の石数を q-2 以下に制限するハンディキャップ貪欲+shake。
  満容量は全行 q-1 石でのみ達成されるため、制限が機能すれば成功配置は自動的に欠損になる。
- 全witnessは census内蔵成功条件に加え、census不使用の独立検証（石ペアの直線・
  石3点組の円の全列挙・厳密整数演算）で safe+maximal を確認。
- 制御: (6,6) m=15 で29石witnessを再発見（K0808 witness域）。
  初期実装のバグ（freeリスト保守で行capを再チェックしない→cap行が q-1 石まで埋まり
  満容量30石の「偽witness」を成功計上）をこの制御が捕捉し、修正後に全結果を取り直した。

## 限界・スコープ

- **非発見は不在証明ではない**: 抵抗記録（いずれもヒューリスティック）:
  (6,5) m=22（1500 restarts・minLeftover=3）・(6,6) m=17（4000・1）・
  (6,8) m=12（欠損1..4・8500・1〜2・6×12には行以外の≥8点直線が存在しない）・
  (5,6) m=16（4700・1〜3）・(5,7) m=19（2200・8）。
  witness鎖の途切れ位置から M_{6,5}=22・M_{6,6}=17・M_{6,8}=12・M_{5,6}=16・M_{5,7}=19
  が**候補**だが、昇格には各 m での不在証明（全極大安全配置が満容量）が必要。
- (6,5) の成功率は m に対して非単調（m=20: 1/1800 → m=21: 49/1800）。
  「難しさは m 単調」という仮定は貪欲探索の設計に使えない。
- M 値の確定（上界との一致）はどこも主張しない。

## レジューム

1. 抵抗5件の不在証明レーン: (6,8) m=12（危険曲線92本のみで構造が最も単純）と
   (5,6) m=16 が最有望。
2. (6,5) m=22 以降の再攻撃（SA・列シフト）。
3. M_{6,7} 上界402の算術的縮小（K0808レジューム・未着手）。
