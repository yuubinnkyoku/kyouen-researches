---
id: K0378
title: 11×11の独立検証済みS5証明6根を段階統合、群間重複なし
kind: verification
status: verified
topics: [square-outcomes, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0372
  note: K0372の信頼境界、終局leaf規則、固定先手視点AND/OR極性を維持
- type: depends_on
  target: K0375
  note: SHA拘束された独立検証済みS5三根証明DAG二組を入力として使用
- type: depends_on
  target: K0377
  note: 三根のwitness-switch compact variantを増分統合の開始証明として再現
- type: supports
  target: K0375
  note: 6根の独立終局閉包と、二つの入力DAG間にcanonical局面重複がないことを検査
artifacts:
- path: research/experiments/n11-proof-dag-incremental-20261011/README.md
  role: source
  note: 増分統合、最適化比較、資源測定、限界、再現手順
- path: research/experiments/n11-proof-dag-incremental-20261011/scripts/integrate.py
  role: source
  note: K0375の証明DAGだけをinternし、共有後の閉包費用で根証人を選択
- path: research/experiments/n11-proof-dag-incremental-20261011/scripts/benchmark_integration.py
  role: verifier
  note: 統合のwall time、process-tree peak RSS、出力・一時DB peak容量を測定
- path: research/experiments/n11-proof-dag-incremental-20261011/scripts/build_audit.py
  role: verifier
  note: 計画、certificate SHA、独立検証receipt、境界reportを照合して監査JSONを構築
- path: research/experiments/n11-proof-dag-incremental-20261011/tests/test_integration.py
  role: verifier
  note: 貪欲、局所改善、root-level厳密列挙、列挙上限のfail-closedを検査
- path: research/experiments/n11-proof-dag-incremental-20261011/output/integration-plan.json
  role: data
  note: 入力hash、候補union、greedy/local/exact比較、出力節点・辺数
- path: research/experiments/n11-proof-dag-incremental-20261011/output/integration-audit.json
  role: manifest
  note: 6根LOSSの独立検証receipt、certificate SHA、RSS・wall time・scratch監査
scope: K0375の二つの独立検証済みS5三根LOSS proofを統合した6根compact証明だけを対象とする。親S4の完全子境界、第三手117/119全体、11×11二石root {60,27}、10根以上の拡張は含まない。
evidence: 入力二DAGは2,337,747節点と1,002,511節点で、intern後も3,340,258節点となりcanonical局面重複は0だった。K0377の三根witness switch結果をSHA-256 478fc29e51ffd7e18158f74f0032b7e7756446e11c5d0819b000e19e79474fc2まで再現した後、6根証明を2,720,770節点・4,065,013辺・終局376,370件へ出力した。compact SHA-256 44bacf049ee693fa4dd11be1db64c2eec066ee444ddf29f1c94118a25a148e22を既存の独立検証器で検査し、6根すべてLOSS、trusted leaf 0を確認した。増分variantと共同最適化variantは同一SHAで、K0377のwitness switchを超える追加縮約はなかった。
---

# S5 LOSS証明DAGの6根増分統合

K0375の二つの三根証明DAGをSHA拘束で読み込み、canonical局面をinternして6根の
KYPRFDG v1 compact証明を作った。K0377の三根witness switchを同じSHAで再現し、
その結果を保持して三根を追加した。

独立検証器が6根すべてのLOSSを確認した。節点は2,720,770、辺は4,065,013、終局は
376,370件で、trusted leafは0だった。入力二群の局面重複は0であり、greedy・局所改善・
2通りのroot-level厳密選択は同じ6根DAGを選んだ。したがって、このroot集合では
K0377の既知縮約を超える共同最適化効果は観測されない。最大RSS、wall time、scratch、
証明サイズの測定は実験のintegration auditを参照する。

最新対象S4の106子はLOSS 40 / WIN 0 / UNKNOWN 66のままである。solver/cache結果は
取り込まず、S4全子や{60,27}を閉じたとは主張しない。独立終局閉包済みの追加根が
得られなかったため10根測定も行っていない。
