---
id: K0377
title: 11×11の三S5共有証明DAGをcompact化し、既知S6証人の共有で縮約
kind: verification
status: verified
topics: [square-outcomes, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0372
  note: 独立証拠とsolver/cacheの信頼境界、未解決frontierを維持
- type: depends_on
  target: K0375
  note: 元となる最新mainの三S5 shared proof DAGと証明規則
- type: supports
  target: K0375
  note: K0375の最新S4配下にある三S5 LOSS proofだけを独立compact検証し、既存閉包共有による局所DAG縮約を確認
artifacts:
- path: research/experiments/n11-proof-compact-20261011/README.md
  role: source
  note: 被覆、形式、性能測定、適用範囲、再現手順
- path: research/experiments/n11-proof-compact-20261011/scripts/bundle_store.py
  role: verifier
  note: SQLite disk-backed JSON/compact検証、相互変換、SHA拘束付き証人差し替え
- path: research/experiments/n11-proof-compact-20261011/scripts/benchmark_verifier.py
  role: verifier
  note: Windows process-tree RSS、wall time、peak scratch測定
- path: research/experiments/n11-proof-compact-20261011/tests/test_bundle_store.py
  role: verifier
  note: binary改ざん、完全子欠落、誤極性、孤立節点、trusted leaf、source辺復元の拒否・回帰
- path: research/experiments/n11-proof-compact-20261011/output/proof-compact-audit.json
  role: manifest
  note: source/compact SHA-256、完全検証receipt集計、被覆と証人差し替え比較
scope: 最新mainの固定された三つのS5 LOSS rootを含む証明DAGと、同じ三rootの一つを既に検証済みS6 LOSS証人へ差し替えたvariant。全S4子、root {60,27}、11×11全体の解決は含まない。
evidence: 元JSONはSHA-256 48edffe570591e7196c2021353342a05ba058d70b141f05128bd17c207d4e922、2,337,747節点・3,484,437辺・trusted leaf 0で独立検証した。KYPRFDG v1 compactはJSON由来graphと完全一致し、trusted leaf 0のまま全検証に成功した。root 2のmove 11からの666,475-node closureを、他rootですでに選択されていた合法move 46の792,830-node closureへ切り替えると、共有を含む到達可能DAGは1,718,259節点・2,547,576辺となった。縮約variantも全ての独立検査を通り、同じ三root LOSS、trusted leaf 0を確認した。compact証明はJSON比77.90%小さく、variant検証はbase compact比26.25%速かった。この縮約は固定三root集合での実測であり、全体最小性を意味しない。
---

# 三S5共有証明DAGのcompact検証と証人差し替え

最新mainの三つのS5 LOSS rootを、元JSONとKYPRFDG v1の両方で検証した。どちらも2,337,747節点、3,484,437辺、終局331,495件、trusted leaf 0で同じgraphを表す。JSON gzip 72,771,052 bytesから22,089,195 bytesへ縮まり、全節点をPythonの巨大な辞書として同時展開しないdisk-backed方式で検証できた。

同じ証明DAGにはroot 2のS6 LOSS証人が二つあった。単独の閉包は保存済みmove 11が666,475節点で、代替move 46は792,830節点だったが、move 46はroot 0が既に使っていた。root 2をmove 46へ切り替え、他rootから到達しない節点・辺を除くと、unionは619,488節点と936,861辺縮んだ。代替証人の単独閉包サイズと全体DAGの増減が異なる実例である。

このvariantは1,718,259節点、2,547,576辺、終局247,842件で、同じ三rootのLOSS判定・trusted leaf 0を独立検証済み。元の三root compact proofに比べ、wall timeは1,853.203秒から1,366.687秒へ、peak scratchは626,414,784 bytesから454,351,644 bytesへ減った。旧JSON検証baselineよりRSSは95.60%低く、wall timeは24.31%短い。

これらは三つのS5 rootまでの検証結果である。親S4の全106子や二石root `{60,27}` の119第三手は証明しておらず、K0372の他30 LOSS classも独立minimax証明へ昇格させない。S4 frontier、K0372の隔離、勝敗伝播規則は変更していない。
