# 共円ゲーム11×11：空盤弱解決の証明戦略比較（2026-10-12）

K0417の19二石root共同証明計画（上界31,546・分数下界6,573.146）を基準に、先手WIN側と後手WIN（初手LOSS）側の証明経路を比較した。新規の大規模solver探索は行わず、既存exact-S5 cacheと独立整数幾何Board、有限組合せ最適化だけを使う。

## 課題1：K0417上下界の検証と下界の確定

- 31,546計画の独立再検証（`verify_plans.py` 再実行）は現行main上で通過（失敗0、19 root・2,261 third手・34,948 S4再計算）。
- element-only分数双対を厳密有理数で再計算し証明書化した（`scripts/dual_certificate.py`、`output/element-dual-certificate.json`）。deg 962,469要素の再集計、869群のalpha厳密和、総和 **2024529/308 = 6573.1461…** を `--verify` で再確認済み。
- 整数下界 **6,574** の採用条件は2点のみ。(i) 双対実行可能性（証明書のdeg再集計＋alpha不等式の厳密検査）。(ii) 真の最適値が和集合濃度ゆえ整数であること。よって OPT ≥ ceil(6573.1461…) = 6574。
- element-only重み族では `w[e] = 1/deg[e]` が族内最適であることを確認した（目的関数が各重みに単調非減少なため、重み調整での改善余地なし。改善には族の拡張が要る）。
- 独立な整数証明書としてpool-disjoint packing（`scripts/disjoint_pool_packing.py`）を試したが346に留まり、6,574を上回らず。grouped双対1,586.75・LP緩和双対728も及ばない。上下差（6,574対31,546、約4.8倍）は未解決のまま残し、869群への分枝限定は今回行わない。

## 課題2：非中央後手応手の比較（初手49・16・38）

各初手の非中央応手27・93のrootを中央グラフと同一index空間で構築した（`scripts/build_alt_roots.py`、6 root・39.1秒）。結果（`output/alt-reply-comparison.json`）：

| root | 個別UB | 中央UB | 個別LB | 無料third | S4再利用率 |
|---|---:|---:|---:|---:|---:|
| 49/27 | 3,234 | 2,055 | 878.1 | 2 | 0.86% |
| 49/93 | 3,208 | 2,055 | 865.4 | 2 | 1.09% |
| 38/27 | 3,206 | 2,155 | 864.2 | 2 | 1.04% |
| 38/93 | 3,161 | 2,155 | 855.7 | 2 | 1.14% |
| 16/27 | 3,227 | 2,084 | 858.4 | 2 | 1.19% |
| 16/93 | 3,152 | 2,084 | 872.8 | 2 | 0.35% |

- 中央応手を下回る応手はなし（約1.5倍悪い）。無料thirdも中央10に対し各2。
- S4再利用率は約1%で幾何的重なりがほぼなく、代替プランとK0417共同計画のS5重なりも0〜1個（共有効果なし）。
- joint-swap（18中央＋代替1）は中央共同31,546に対し+3,065〜+3,349悪化し、相異なる群も948→1,007に増える。
- 判断：非中央応手への拡大は行わない。中央応手が3初手すべてで支配的である。

## 課題3：初手WIN証明計画（初手49）

元先手固定視点で、初手WINには全65応手軌道（初手49の安定化群でD4縮約）それぞれに第三手が必要で、選んだ第三手の全fourth手S4が先手WINでなければならない。既存cacheでのS4分類は free（cache LOSS子あり）／dead（全子cache WIN）／open（未知子あり→楽観的証人1個で使用可）。結果（`output/win-side-analysis.json`）：

- 65応手軌道すべて閉鎖可能。各応手で119 third手すべて viable（dead S4は到達133,924クラス中に0個）。
- 無料で閉じる応手5、証人を要する応手60。
- AND境界：選択thirdのfourth手 合計7,503 S4分岐。
- 楽観的証人frontier：約1.74k相異なるS5（貪欲被覆のtie-break依存で±1%の幅。再計算1,739、マスク保存 `output/win-witness-masks.json`）。
- 各証人は単独では証明にならず、全sixth手のLOSS閉包（S5 LOSS ⟺ 全S6先手WIN）が別途要る。ここは未計測。
- dead S4が0個のため、LOSS側へ転用できる確定資産はなし。
- WIN証人とLOSS側共同計画の要求集合の重なりは16/1,739、中央S5宇宙内にある証人も235のみ。両frontierはほぼ無共有。

## 課題4：先手WIN・後手WINの比較と主軸判断

| 観点 | 後手WIN側（初手LOSS、19初手共同） | 先手WIN側（初手49の1初手） |
|---|---|---|
| 頂点の存在量化 | S1=ANDより初手ごと1応手rootで足りる | S1=ANDより全65応手軌道が必要 |
| 未確定S5 frontier | 31,546（全S5子を強制取得） | 約1.74k（証人を存在選択・共有） |
| AND境界規模 | 有料2,139 third＋31,546 S5 | 65応手＋7,503 S4＋証人 |
| 既知証拠利用 | 32既知LOSS S4で122 third無料 | 5応手が無料、dead 0 |
| 無効化リスク | 要求S5の1個のWIN化は該当S4を殺す（代替S4で修復可） | 証人S5のWIN化は同S4の別子で修復可（子が約110個あり slack 大） |
| 終局 payoff | 19初手全LOSSで空盤後手勝ち確定 | 1初手WINで空盤先手勝ち確定 |

未知局面に確率は置かない。S5数から探索時間も予測しない。両側のfrontier S5は1個あたり同種の∀-閉包（S5 LOSS ⟺ 全S6先手WIN）を要する点で対称であり、差はfrontier規模と量化構造にある。

判断（測定に基づく方針であり証明ではない）：**主軸は後手WIN側の共同計画を維持し、先手WIN側は初手49の証人パイロット閉包で閉包単価を実測する二段構え**とする。理由は (i) WIN側は65/65閉鎖可能で障害ゼロの一方、証人1.74kの各閉包費が未測定で本丸の費用が未知、(ii) LOSS側は31.5kのfrontierが確定済みで1個のS5 LOSS確定がそのまま計画を前進させる、(iii) 両用16 S5など両戦略に資する閉包から着手すればどちらに転んでも無駄が少ない、の3点である。

## 課題5：実探索に移る条件

- frontier 31,546のlegal手数は60〜116手に分布し、微小局面はない（`output/pilot-candidates.json`）。最安10件（60〜70手）と両用16件（78〜104手）をマスク付きで抽出済み。
- 既存exact cacheのLOSS 5,692件のうち直接探索node記録があるのは65件のみ（合計388,074,801、最大11,267,484）。frontier全体の費用はここから外挿しない。
- 大規模探索の開始条件：(1) 最安＋両用パイロット（10件以内）を既存solver手順でnode上限付きで回し単価実測、(2) 閉包成功かつnodeが予算内に収まる、(3) 成功分だけ共同計画の要求集合を縮小して次を選ぶ。(1)なしに大量探索を開始しない。
- solver-trusted exactとterminal-only独立証明の区別（K0416の2,992未閉鎖根）を維持し、パイロットも由来別に記録する。

## 再現

```powershell
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/dual_certificate.py
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/dual_certificate.py --verify research/experiments/n11-proof-cost-comparison-20261012/output/element-dual-certificate.json
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/disjoint_pool_packing.py
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/build_alt_roots.py
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/compare_alt_replies.py
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/win_side.py --firsts 49
uv run --locked python research/experiments/n11-proof-cost-comparison-20261012/scripts/win_witness_masks.py
```

`win_side.py`（初手49）は約30分を要する。他の全手順は合計10分以内。solver探索は起動しない。

## 限界

- 上下差（6,574対31,546）は未解決。最適値の厳密確定はしていない。
- WIN側証人frontierは貪欲被覆のheuristic値で、最適性の主張なし。
- 各証人S5・各frontier S5の∀-閉包費は未測定であり、frontier規模の比較は証明費用の比較ではない。
- 初手49以外のWIN側分析、非中央応手の3初手以外への拡大は未実施。
