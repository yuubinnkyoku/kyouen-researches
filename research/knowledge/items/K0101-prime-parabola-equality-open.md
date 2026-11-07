---
id: K0101
title: 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0097
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: 禁止四点の完全対分類とNAE・原点節の厳密な分解。全素数の充足可能性は未証明
- path: research/experiments/frontier-geometry-2026-10-05/recovered-witnesses.json
  role: certificate
  note: 131..251拡張の追跡されていなかった証人を回復・保存
- path: research/experiments/frontier-geometry-2026-10-05/density-probe-witnesses.json
  role: certificate
  note: 509,1009の追加有限等号証人
- path: research/experiments/parabola-equality-extension-20261016/README.md
  role: source
  note: 521..2000への有限拡張。全奇素数の等号は依然未証明
- path: research/experiments/parabola-equality-extension-20261016/output/witnesses_521_2000.json
  role: certificate
  note: 521..1999の全206素数の等号証人
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2143_2500.json
  role: certificate
  note: 2003..2477の64素数のうち63の等号証人。2207は深いd走査中
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit.txt
  role: data
  note: generic 4×4 Leibnizによる全63証人の独立検証出力（共円0件）
scope: 奇素数 p における等号 A(p)=(p+3)/2 の有限検証範囲と d=h 例外の記述。
evidence: finite computation; no counterexample to equality found through 2477; 5..2203 は穴なし、2213..2477 も 2207 を除き証人あり; all-prime proof unknown
---

# 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定

Q_p内の一般上界は証明済みで、5..2000の全奇素数で安全証人が等号を達成する。
5..127の29素数は既存独立検算。131..251の23素数については追跡されていなかった証人を回復し、
generic 4×4 Leibniz展開で全選択四点を再検査した。257..439の31素数と443..503の11素数も、証明済み必要合同式で全候補を絞った後に直接整数行列式で独立検査した。521..1999の全206素数は
research/experiments/parabola-equality-extension-20261016 で構成し、同じ独立検証器で検査した
（必要合同式を満たす総計2,196,275,194,090四点組のうち1,385,691,858候補に直接整数行列式、共円0件）。
したがって5..2000は穴なく有限確認済み。1009を超える範囲の等号も有限に確認している。

**全奇素数に同じ達成構成があるかは未証明**。2000を超える反例素数も未発見。

K0334は、等号問題をある完全対dについてsigned NAE3/4と原点由来2/3リテラル節の
同時充足可能性へ正確に帰着した。その全称充足可能性も反例素数も未確定。
認証方式の上界や全盤K_pの既知下界とは別の問い。

## 2026-10-17 bounded advance

New finite evidence: `d=h` is sufficient for all primes 5..443 and (newly) 2003..2143, except `d=h-1` for 1087, 1091, 1367, 1523, 1847, 2027 and `d=h-66` for 1861; p=2027 independently verified with `verify_witnesses.cpp`. All 302 odd primes up to 2000 already had equality witnesses; new runs add independently checked witnesses for 2003..2053 and 2069..2143. No counterexample prime to equality found.

Scope clarification: K0101 is not resolved by the `d=h` construction alone; `d=h` works for most primes but has exceptions, so a uniform construction remains unknown.

Next steps: characterize the `d=h` exception pattern; extend finite verification beyond 2143; seek an all-prime proof. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
## 2026-11-07 有限証人の保存拡張（2003..2477）

`research/experiments/parabola-equality-extension-2143-2500-20261107` で 2003..2477 の奇素数 64 個を走査し、
63 個で等号証人を構成・保存した（`d=h-1` は 2027, 2399, 2477、他の 60 は `d=h`）。
2351 は既定設定の cadical がタイムアウトしたが SAT 向け設定（`--sat -L1000`）で `d=h` の解を得た。
証人は探索と独立な generic 4×4 Leibniz 検証器で全件監査済み（共円 0 件）。
これで **5..2203 の全奇素数**と **2213..2477** に証人が存在する。
2207 は `d=h..h-528` の走査で未発見であり（深い d を走査中）、等号不成立の証拠ではない。
2017 の記録が挙げた 2003..2143 の証人も本実験で再構成・保存した。

Scope clarification: 有限範囲の保存証人が 2203 まで延びただけで、全奇素数での等号は依然未解決。
`d=h` の例外分布（h-1 が多いが 1861 は h-66）の特徴づけも未解決。
