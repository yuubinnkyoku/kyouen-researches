# 現在の知識

`items/Knnnn-content-slug.md` が現在の知識の正本。過去の研究記録は出典として残す。
命題の証明・再検証が増えたら同じ項目を更新する。反証した命題は残し、異なる修正版は別項目にする。
有限計算の支持を無界命題の証明に昇格させない。未監査と数学的未解決も区別する。

- [項目・topic一覧](generated/index.md)
- [解決状況](generated/solutions.md)
- [旧ID逆引き](generated/aliases.md)
- [artifact逆引き](generated/artifacts.md)
- [関係一覧と逆リンク](generated/relations.md)
- [集計・未解決・警告](generated/summary.md)
- [schema](SCHEMA.md) / [語彙](VOCABULARY.yaml) / [template](templates/item.md)
- [移行範囲と残件](../MIGRATION.md)

## 現在の研究を読む順序

まず[規則](items/K0001-complete-call-rules.md)、[Grundy・勝敗の定義](items/K0002-grundy-and-first-move-conventions.md)、[解決段階の区別](items/K0003-solution-and-evidence-levels.md)を読む。
「計算済み」「証明書を検査済み」「全安全局面を分類済み」は別の情報として扱う。

- 正方形盤: [1〜6の全Grundy](items/K0004-n1-n6-all-safe-grundy.md)、[7の全Grundy](items/K0005-n7-all-safe-grundy-audit.md)、[8の全Grundy計算と検証境界](items/K0006-n8-all-safe-grundy-computed.md)、[9の全81初手](items/K0021-n9-all-81-first-moves-win.md)、[10の全100初手と検証境界](items/K0022-n10-all-100-first-moves-classified.md)、[11の厳密列挙と未確定勝敗](items/K0023-n11-exact-safe-layers-and-unknown-winner.md)。空盤勝敗と全局面分類の一覧は[生成表](generated/solutions.md)。
- 証拠の信頼境界: [AND/OR方式](items/K0007-ranked-and-or-certificates.md)、[C++独立検査](items/K0008-n1-n9-independent-cpp-certificate-checks.md)、[Leanの一般的健全性](items/K0009-lean-soundness-trust-boundary.md)、[KYOENC4の範囲](items/K0010-kyoenc4-selected-position-certificates.md)、[Rust・CSV検査の範囲](items/K0280-independent-rust-verification-boundaries.md)。[10の空盤全体を覆う単一証明書](items/K0103-n10-single-empty-root-certificate-open.md)と[巨大証明書のLean内具体検査](items/K0102-concrete-lean-certificate-checker-open.md)は未完了。
- 固定幅・ルール変種: [条件付き一般定理](items/K0024-fixed-width-q-point-threshold.md)、[q>2w](items/K0025-q-above-two-width-all-lengths.md)、[標準ルールの十分な高さ](items/K0068-standard-fixed-width-parity-threshold.md)、[2行の全高さ](items/K0069-two-row-all-lengths-strong-solution.md)、[q=6・幅3](items/K0070-width-three-q6-stabilization.md)、[q=5・幅3の留保](items/K0071-width-three-q5-bounds-and-solved-ranges.md)、[整数座標の合同式による拡張](items/K0072-mod9-integer-row-separation.md)。
- 最大と極大: [定義](items/K0026-maximum-versus-minimum-maximal.md)、[最大安全サイズ](items/K0029-n1-n9-maximum-safe-sizes.md)、[小盤面の極大サイズ分布](items/K0030-n3-n6-maximal-safe-size-distributions.md)、[7の最小極大](items/K0031-n7-minimum-maximal-size.md)、[10の最小極大の境界](items/K0034-n10-minimum-maximal-bounds.md)、[10の最大安全の境界](items/K0035-n10-maximum-safe-bounds.md)。[最適終局T*とWFT](items/K0295-n1-n7-full-tstar-and-wft.md)は固定証明書の終局一覧とは異なる。
- 幾何と配置構造: [禁止4点組の個数](items/K0057-forbidden-quadruple-counts.md)、[共線4点組の漸近式](items/K0054-collinear-quadruple-asymptotics.md)、[共円4点組のオーダー](items/K0056-cocircular-quadruple-asymptotics.md)、[被覆の上界](items/K0107-sharp-point-cover-bound.md)、[最小極大の一般下界](items/K0106-minimum-maximal-exponent-lower-bound.md)、[素数盤の構成](items/K0095-split-prime-safe-quadratic-construction.md)、[整数放物線の有限検査と未解決の一般化](items/K0097-integer-residue-parabola-bounds.md)。
- 7の結晶と再配置: [全16最大配置](items/K0051-n7-maximum-configurations-two-phases.md)、[占有骨格の分類](items/K0268-n7-six-orbit-skeleton-exclusive-extensions.md)、[容量12での成分](items/K0270-n7-g12-maximum-containing-components.md)、[第4隅が必須なゲート](items/K0271-n7-fourth-corner-global-gate.md)、[静的集合Uの幅11](items/K0272-n7-union-width-eleven-static-barrier.md)。[G11での全最大成分連結](items/K0282-n7-g11-global-connectivity-open.md)は未解決。
- 探索実験: [監査済みcache-aware再現](items/K0090-n10-cache-aware-capacity-rerun.md)、[旧固定median規則の撤回](items/K0086-blind-probe-median-improvement-withdrawn.md)、[ASCの限定的再現](items/K0284-independent-memo-ascending-rank-replication.md)、[staged分類器](items/K0285-staged-v3-loss-shortlist-recall.md)、[実solver速度の不成立](items/K0286-native-parent-solver-speedup-gate-failed.md)。分類精度を速度改善に読み替えない。

重要な反証には[2n−1予想](items/K0027-two-n-minus-one-conjecture-refuted.md)、[勝者が常に終局サイズを固定できるという予想](items/K0050-fixed-terminal-guarantee-refuted.md)、[5の最適終局から5を除く旧主張F-Y](items/K0296-n5-five-stone-optimal-terminal-exclusion-refuted.md)がある。
[11の旧勝敗主張](items/K0028-n11-truncated-dp-winner-withdrawn.md)は根拠撤回であり、反対の勝敗を証明したわけではない。
数学的未解決・要監査・量化範囲不明は[集計](generated/summary.md)で分けて列挙する。

rootのuv環境で実行する。

```sh
uv sync
uv run --locked python tools/knowledge/check.py
uv run --locked python tools/knowledge/build.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
```

生成物はGit管理するが直接編集しない。CIは再生成後の差分を検出する。
原文監査索引の旧SUPPORTED/REFUTEDを機械的に採用せず、量化範囲と根拠を本文に記す。
