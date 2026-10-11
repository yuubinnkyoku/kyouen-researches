# 11×11 S5階層分割の費用比較と証拠対応ルーター

## 結果の要約

最新main `d0d54863df2034f12821e6e2ec81afbbe868f32b` とK0374を確認し、保存済みrawだけで比較を再構成した。対象にした難S5は
`(1188950301626859520,603979776)` で、独立幾何から90個のcanonical S6子を再生成した。

- 直接S5 DFPNは15,000,000 nodesでUNKNOWN。
- S6分割は初回85 WIN / 5 UNKNOWN、残る5子を15M上限で再試行して全WIN。
- 90子を閉じた総探索量は**29,794,287 nodes**。S5のAND則でS5 WINを導けるが、直接15Mの約1.99倍の節点を使った。
- 同じ15M-node予算に切った分割順序の再構成では、60子exact、2回のUNKNOWN終了、次の子を途中打切りし、S5はUNKNOWNのまま。これは保存rawから作った反実仮想の予算切りで、追加solver runではない。
- 直接rawの行時間は47秒、分割のrun footer合計は83秒だが、分割報告はDebian / Intel i5-9400T、直接rawは実行hostを特定できない。wall timeは比較不能。両方とも最大RSSを保存していない。

したがって、この対象では階層分割が15M直接探索より**少ない計算量で解決したとは実証できない**。同じ15M節点では両方UNKNOWN、分割が解決するには29.79M節点を要した。S6 rawはsource/binary hashを持つが、直接rawはどちらのhashも持たない。直接rawの実行hostも特定できず、厳密な同一環境paired benchmarkではない。これ以上の比較目的で解決済みS5を再探索していない。

K0374の90 S6 exact値はsolver-trustedである。S5/S4親への幾何境界とAND/OR伝播は独立検査済みだが、90子それぞれのterminal-only minimax証明を意味しない。

## 適応ルーター

`scripts/strategy.py` はA〜Eを証拠状態・証明極性・測定済み費用で選ぶ。

1. **E**: trusted leaf 0の検証済み独立DAGがあればそれを再利用する。trusted leafが1以上のDAGは独立証明扱いしない。
2. **A**: exact direct S5 raw/cacheがあれば再利用する。新しい探索ではない。
3. **C**: 保存済みS6境界を再集約する。S5はS6 LOSSが一つあればLOSS、全合法S6がWINならWIN。途中のS6 WINだけでは判定しない。
4. **D**: S5 LOSSが目的なら、未解決S6を一つずつ探査し、exact S6 LOSS証人で停止する。既知のnode-cost hintは順序付けにだけ使い、WIN確率の予測には使わない。S6 WINが一件あってもS5 LOSS/WINを導かない。
5. **A/B比較**: S5 WINには全合法S6 WINが必要。directとfull splitの完了費用が同じ環境で測られた場合のみ低い方を選ぶ。そうした比較がなければ方式を自動断定せずpaired benchmarkを要求する。

S6 LOSSへの集約は固定先手視点で「S6 OR: すべてのS7子LOSS」。S7 LOSSを一つ見つけただけでS6 WINへ反転しない。UNKNOWNや打切り値はexact集合へ入れない。

最新mainの最有力S4 `(1297036692683752448,0)` は、追跡済み最新cacheと独立幾何からLOSS40 / WIN0 / UNKNOWN66を再構成した。11×11二石root `{60,27}` は117/119のままである。旧K0374対象S5は現最有力S4の子ではない。比較でnode削減が確認されず、新しいS5を選ばず、現在境界へ探索をdispatchしていない。

## 再現

K0374のS6 rawと既存のdirect S5 15M rawを`input/raw/`へgzip格納した。gzip展開後のバイト列は元rawと一致し、出所SHA-256とgzip blobのSHA-256を`output/source-manifest.json`へ記録する。rawをhash・合法子集合・合法手数・全子数・budget・verdict・固定先手極性まで監査する。

```powershell
uv run --locked python research/experiments/n11-s5-hierarchical-adaptive-20261011/scripts/analyze.py
uv run --locked python -m unittest discover -s research/experiments/n11-s5-hierarchical-adaptive-20261011/tests -v
```

再生成物は`output/strategy-audit.json`と`output/source-manifest.json`。テストは未完了境界、空子集合、S5/S6極性、zero-trusted-leaf制約、raw改ざん、15M同一node-cap再構成を検査する。

## 適用条件と限界

- Dが直接法より安いという測定結果はまだない。S5 LOSSの存在証人探索では論理的に早期停止できるが、未知のどのS6がLOSSかはrawからは予測できない。
- K0374例はS5 WINなので全90 S6を閉じる必要があった。S5 LOSSを探すDの効率を裏付ける標本ではない。
- Cは既に保存されたexact S6/S7証拠を再利用するとき追加探索を省くが、元の探索生成費用を消さない。
- A〜Eのnode count以外のメモリ・ストレージ費用は元rawにない。最大RSS・同一host wall timeの比較は今後の新規paired benchmarkで計測する。
- 現S4へ方式を適用するには、候補S5を選ぶ前に最新main/cache/raw・S6/S7境界・他担当のdispatch対象を再照合する。UNKNOWNをexactにせず、既存成果や他作業の未コミットrawを上書きしない。
