# 2026-11-18 N11 上位4安価parentのcross-parent証明書共有の定量分析

## 成果

出版済み最小coverコスト表（`parent-minimum-cover-cost-table-20261118.json`）で最も安い4 parent — top parent `00000000000000403800000008000000`（cost 6・11行）、`00000000000000821082000000000000`（cost 9・18行）、`00000000000000003800000008002000`（cost 12・23行）、runner-up `00000000000000003800000009000000`（cost 15・29行）— の**全15非空部分集合についてjoint最小coverコストを厳密決定**し、個別コスト合計との差（証明書共有利益）を定量した。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/joint_parent_cover_sharing_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/joint-parent-cover-sharing-20261118.json`
- 41 checks all PASS。二重実行 byte-identical。実行約2秒。

## 方法

per-parent表と同一のcover semantics（rootは自分を1石D4正準拡張として生成する行を被覆する。phase-1全行候補列挙を再利用するためcross-parentな被覆も自然に現れる）。joint対象 = 部分集合のparent群の対象行の和集合、joint宇宙 = その候補root。下界 ceil(r/maxspan) + 機械検証済みwitnessで厳密確定（決定的greedy matching・seed固定）。cover table（blob `4e4a911d`）をpin検証して4 parent選択が表上の最安4件であることも検証。

## 主要な新所見

1. **4 parentの対象行は互いに素**（2行和集合はすべて r1+r2、4行和集合81 = 11+18+23+29）。行レベルの共有なし。
2. **joint最小コストは個別合計から最大1本の節約**（4-way: 41 vs 42 = 2.4%）。節約の源泉は偶奇償却（奇数行のparentが個別には1本singletonを要する分を、jointではcross-parent pair rootで潰せる）。実現にはcross-parent span-2 rootが必要で、実際に top×cost12間8本・top×runner-up間8本・cost12×runner-up間9本・4-way計24本が存在し、全15組み合わせで maxspan=2 のまま（3行以上を被覆するrootはcross-parentでも出現しない）。
3. **共有クラスター構造**: `…821082…`（cost 9・18行）は他3 parentとのcross-parent rootが0本で完全に孤立。top・cost12・runner-upの3者が相互に共有（3ペアすべてbenefit 1）。**coordinatorにとって、この4件を束ねても証明書節約は1本のみで、per-parentコスト順の優先順位付けはjoint計画下でもほぼ保存される**。
4. 各組み合わせのjoint witness（root hex列）は全15件同梱・機械検証済み（被覆過不足なし・root重複なし）。

## 解釈上の注意

joint coverコストは「選んだrootすべてが証明書として成立するなら」の計画上の計数。rootの妥当性・WIN/REFUTEDは一切主張しない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
