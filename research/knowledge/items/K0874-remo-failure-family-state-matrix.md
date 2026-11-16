---
id: K0874
title: 3枝REMO失敗族52キーのr=2..8状態行列と4/10族の位相構造
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO failure-family state matrix]
relations:
- type: depends_on
  target: K0861
  note: 定理E′（atomプロファイルへの軌道簡約・全称）でプロファイル判定が盤に転送される
- type: depends_on
  target: K0862
  note: r=3・cap<=10の非坍縮22キー完全境界と22組の最小witness
- type: depends_on
  target: K0864
  note: r=2,4,5,6境界・補題FL（全称）・r=3,4,5決定プロファイル分割の源
- type: depends_on
  target: K0866
  note: r=7・cap<=10の非坍縮6キー境界・r=7 witness・FATE連鎖値
- type: depends_on
  target: K0867
  note: 4/10族r=8外挿の反証（計数・0決定・集合{3,7}）
- type: depends_on
  target: K0869
  note: r=8・cap<=10の非坍縮10キー境界・FATE・ECHO・出版compactによるr=8全レコード照合
artifacts:
- path: research/experiments/remo-failure-family-matrix-20261116/report.md
  role: data
  note: 52キー×r=2..8の状態行列・MX1〜MX11・連鎖値・限界
- path: research/experiments/remo-failure-family-matrix-20261116/verify_remo_failure_family_matrix.py
  role: verifier
  note: 364セル完全再計算・出版定数埋込み・二重実行バイト同一・stdlibのみの検証器
- path: research/experiments/remo-failure-family-matrix-20261116/output/remo_failure_family_matrix_audit.json
  role: data
  note: 全セル詳細（決定生存者・可能生存者集合・連鎖判定）と機械チェックMX1〜MX11
- path: research/experiments/remo-failure-family-matrix-20261116/matrix_profiles_compact.jsonl
  role: data
  note: 1,392プロファイル×r=2..8の9,744判定レコード
scope: "3枝REMO、枝サイズ1..10の715キーのうち失敗歴または候補履歴のある52キー（44前失敗キー+4/10族8キー）について、r=2..8の7値すべてで全プロファイルの決定性・順位決定性・決定生存者・可能生存者集合・チェーン値を完全計算した有限結果。715キー全体の各r境界はK0862/K0864/K0866/K0869から継承し本項では再計算しない。"
evidence: "K0864検証器のエンジンをverbatim使用した単一検証器（stdlibのみ・決定的・main二重実行バイト同一）で364セルを完全計算。K0862の22キー・22×2 witness、K0864のr=3,4,5,6分割、K0866のr=7分割・6組witness・FATE連鎖値、K0867の4/10計数、K0869のr=8分割・FATE・ECHOを機械抽出定数として全て再現。r=8の1,392レコードはK0869出版compactと全フィールド一致。補題FLの全セルアンカー違反0。今回計算は前セッション独立計算と全364セル一致。"
---

## 主張

cap≤10ドメイン（15,863プロファイル・715キー）のうち、r=2..8でmixedになった44キー（小枝族10・8/9族12・4/8族6・4/9族6・6/8族10）と唯一の候補族4/10族8キーの計52キーについて、r=2..8全7値の状態（D=一様決定・N=一様非決定・M=mixed）が完全決定された（364セル・9,744判定）。

**MX8（新・4/10族の位相構造）**: 4/10族 (4,4,10),(4,10,10)×γ=0..3 はr=2,3,4で一様決定（生存者P_1,P_2,P_3=連鎖値）、r=5..8で一様非決定（可能生存者集合は全プロファイルかつ連鎖でちょうど{3,r−1}）、**r=2..8で一度もmixedにならない**。r=3,4に決定セルを持つ唯一の候補族である。

**MX5新セル（小枝族のr=7）**: 小枝族10キーはr=7で一様非決定だが**族内で構造が一様でない**: (2,3,8)(3,3,8)(3,8,8)は可能生存者集合{{1,2,4},{1,4}}・連鎖{1,4}、(2,8,9)は{{1,2,3,4,5},{1,3,4}}・連鎖{1,3,4}、(3,8,9)は{{1,2,3,4},{1,2,3,4,5},{1,3,4}}・連鎖{1,3,4}。

**MX7（r=2の完全坍縮の明示化）**: 52キー全てがr=2で決定性・順位決定性・決定生存者・順位・可能生存者集合の全水準でチェーン値へ完全坍縮。24キー（4/8・6/8・4/10族）が一様決定P_1、28キーが一様非決定で集合{0,1}=連鎖。

**MX3強化（PIの集合レベル化）**: 8/9族12キーの決定プロファイル集合はr=3,4,5で完全同一（K0864のPIが計数でなく集合レベルで成立）。

**MX6（FATEの再確認）**: r≤7でmixedだった34キーはr=8で全て一様非決定かつ連鎖非決定。

**MX11（活動窓・有限観測）**: 小枝族{3}・8/9族{3,4,5}・4/8族{6}・4/9族{7}・6/8族{8}・4/10族∅。状態分布はuniform_det 40・mixed 68・uniform_ndet 256セル。

出版済みの全定数（K0862の22キーとwitness・K0864のr=3,4,5,6分割・K0866のr=7分割とwitness・K0867の4/10計数・K0869のr=8分割とFATE・ECHO）は検証器に埋め込んだ機械抽出定数として全て再現され、r=8の全1,392レコードはK0869出版compactと全フィールド一致した。

## 限界

本項は52キー×r=2..8の有限完全計算である。715キー全体の「各rのmixedキーはN個ちょうど」という境界はK0862/K0864/K0866/K0869から継承した前提であり本項のスイープ範囲外。枝サイズ≥11・r≥9は未走査で、窓構造・{3,r−1}型連鎖・族交代パターンの一般則は予想しない（K0867の反証の教訓）。一様非決定セル内の可能生存者集合はr・atom配分に依存してよい（小枝族r=7が実例）。11×11空盤はUNKNOWNのまま。
