# 現在の知識

`items/Knnnn-content-slug.md` が現在の知識の正本。過去の研究記録は出典として残す。
命題の証明・再検証が増えたら同じ項目を更新する。反証した命題は残し、異なる修正版は別項目にする。
有限計算の支持を無界命題の証明に昇格させない。未監査と数学的未解決も区別する。

再採番で移動した参照のうち、証明のhashに結び付く実験READMEは元のbytesを保持する。
その歴史的リンクは`frozen_links.json`で元ファイルのSHA-256・旧path・現行正本を明示し、検査器はhash一致と移動先の実在を確認する。
これは過去の参照を認識するための対応表であり、通常のリンクや生成物の参照切れは引き続きエラーとする。

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
- 高次元平行列盤: [任意底面の超平面跡容量への厳密縮約（K0824）](items/K0824-higher-dimensional-fiber-trace-reduction.md) は q>2|B| で占有数へ厳密縮約し、この一様条件が q=2|B| で鋭いことを標準単体底面の反例で示す。[K0832](items/K0832-vertical-fiber-degree-reduction.md) は底面係数次数無制限・各ファイバー非零の全多項式族について、最大共存数が厳密に Σ_b min(c_b,t) となることをラグランジュ補間で証明し、安全性を底面跡容量条件と Σ_b min(c_b,t)≤q−1 で完全判定する。q>t|B| はその一様系。さらに底面跡制約のない境界層 Σ_b min(c_b,t)=q−1 では、Grundy値が飽和ファイバーの残り手数の偶奇の排他的論理和になる。特に t=1 では全局面で G(S)=(m·min(|B|,q−1)−|S|) mod 2（全終局が同じ rm 石に達するため）。底面跡制約ありでは全飽和後も全跡容量を保つ場合に限る十分系。さらに t=2,q=3,|B|≥2,m≥2 の純ファイバーゲームでは全安全局面のGrundy値を0,1,2に完全分類し、単独1石ファイバーはm奇数ならGrundy値2となる。さらに底面跡制約なし・t=2,q=4、|B|≥2、|A|≥2の純ファイバーゲームでは全安全局面を閉形式分類し、|B|=2では最大Grundy値1、|B|≥3ではm偶数で最大1・奇数で最大2（最小のGrundy値2の証人はw=m=3,c=(1,1,0)）。さらにt=2,q=5、|B|≥3、|A|≥2では全安全局面を9型で分類し、最大値はm偶数で1・奇数で3。さらに底面跡制約なし・t=2・q=6では、w=2は二鎖の直和、w=3またはm偶数は全Grundy値が0/1、w≥4かつm奇数は全占有型を閉形式分類して最大値3（最小証人w=4,m=3,c=(2,1,1,0)）。さらに底面跡制約なし・t=2の任意q純ファイバーゲームでは、m偶数なら全Grundy値≤1、m奇数なら≤3。特にq=7ではw≤3またはm偶数で最大1、w≥4かつm奇数で最大3（最小証人w=4,m=3,c=(3,2,1,0)）。さらにt=3,q=4,5,6、|B|≥2、|A|≥2の純ファイバーゲームでは全安全局面を閉形式で完全分類し、最大値はいずれも2（最小証人はq=4: w=2,m=4,c=(2,0)、q=5: w=2,m=4,c=(1,0)、q=6: w=3,m=4,c=(1,1,0)）。さらに底面跡制約なし・t=3・q=7・w≥1・m≥2では全安全局面のGrundy値を閉形式で完全分類する（m奇数は鎖XOR xと残余固定手数min(R,L) mod 2、m=2はmin(6−|S|,2w−|S|) mod 2、m≥4偶数は鎖XORとm・wに非依存な64状態の普遍残余テーブルEの組合せ、w=1は(m−c_1) mod 2）。Grundy値3の局面は占有型(a,2,0,…)(a≥3奇数、w≥3、m≥4偶数)ちょうどに限り、値3計数は先行最大値監査の2490と一致。先行の最大値定理（max G=3 iff w≥3かつm≥4偶数）は系として回収された。さらに底面跡制約なし・t∈{2,3}の任意q≥2・任意幅w≥1・任意高さm≥1では、全安全局面のGrundy値の最大値が完全決定された（cap=q−1、M=min(t,m)、p=(m−M) mod 2として、cap=0で0、p=0またはq≥twで1、p=1かつq≤tw−1でmin(3,⌊cap/t⌋+1)。t=3のp=1ではD=cap−3s≤6の閉ボックス500状態mex固定点とe_0飽和で残余H≤2が全称証明され、(0,3)経由の値3はcap≤5で排除される）。さらに任意の次数上限t≥2・任意q≥2・任意幅w≥1・任意高さm≥1でも全安全局面のGrundy値の最大値が完全決定された（cap=q−1、M=min(t,m)、p=(m−M) mod 2として、cap=0で0、p=0またはq≥twで1、p=1かつq≤tw−1でmin(3,⌊cap/t⌋+1)。残余mex Hはt・Mに非依存で常にH≤2（Theorem T）、任意のt≥2で普遍的にG≤3、値3はp=1かつcap≥2tで初めて現れ、固定t,capでそれを実現する最小幅はceil((cap+2)/t)（m>t・p=1の3剰余場合分けで達成）である）。さらに残余mex H(R;X;z)の単一未飽和ファイバー（単一トークンx）の場合が全称閉形式で完全決定され、残余値2は奇数RかつR≤μ(x,z)（z=xでμ=2x−1、それ以外はmin(x,z)以下の最大奇数）ちょうどに限ることが証明された。一般多重集合へのcap補題 H(R;X;z)=H(R;cap_{R+1}(X);z) も証明され、各固定Rの残余状態空間は有限になる。さらに全1族 X=(1^k)（複数トークンで状態が(k,z,R)に坍縮する最初の族）では全(k,z,R)の残余mexが統一スライス閉形式 U(k,z,R)（z=0はU0）として全称決定された（R前進帰納・15比較族アトム表のシグネチャ決定性・3,803シグネチャ類の完全列挙と被覆補題による機械支援全称証明）。プレイ長=min(R,2k+z)とtail閉形式 R≥2k+z−1⟹k mod 2 はその証明済み構成要素であり、値2位置集合の全(k,z)閉形式（z奇: {1,3,…,q(k)}、z偶: {1,3,…,q(min(k,z))}∪{2k−z+1}）とスライスz=1,2の全プロファイル閉形式はその系A・系Bとして昇格された。t=3では未飽和の単独ファイバーがm偶数でGrundy値2を取る、t=2に現れない現象がある。固定底面次数・既約性制約付きの部分族は別問題。高さ対和が一意な場合の q=2|B| 境界の必要十分条件は [K0828](items/K0828-sidon-height-boundary-reduction.md)。一般位置の閉形式分類は [K0352](items/K0352-general-dimensional-parallel-columns.md)。
  さらにκ=1の一般残余ゲームでは、S=ΣXとしてR≤z+1ならH(R;X;z)が総和Sの単一トークン閉形式へ厳密に縮約される。R≤2では全zで成立し、R≥3ではz≥R−1が一様条件として鋭い。既知tail R≥S+|X|+z−1と合わせ、X≠∅で追加解析が必要なRはz+2≤R≤S+|X|+z−2の幅S+|X|−3の有限帯に限られる。
  さらに2トークン族X=(x,y)（x≥y≥1）の残余2位置集合は、ラダー（奇数R≤q_o(min(S,z))）・家族B（PT角と、z+d≡2 (mod 4)でのEXT δ=(z+d)/2・対角線特殊点を統一）・家族A（ランと定常）の3族閉形式として予想されている（3エンジン相互照合を含む43,241照合の有限監査・不一致0・全称性は未証明）。 ただし z=0 スライスは全Grundy値が全称証明済みで、S=x+y とすると R≤2y で R mod 2、x>y かつ R=2y+1 で2、x>y かつ 2y+2≤R≤S で 1−(R mod 2)、R≥S+1 で S mod 2。z≥1 の全位置予想は未証明。
- 拡張ルールの研究課題: [幾何学的禁止条件を変える変種案（K0504）](items/K0504-geometric-rule-variant-comparison.md)。共面のみ・共球のみ・円柱・円錐・長方形・二次曲線・多項式・二次形式係数変化を比較するための未解決課題で、証明済みの結論ではない。
- 固定幅・ルール変種: [条件付き一般定理](items/K0024-fixed-width-q-point-threshold.md)、[q>2w](items/K0025-q-above-two-width-all-lengths.md)、[標準ルールの十分な高さ](items/K0068-standard-fixed-width-parity-threshold.md)、[2行の全高さ](items/K0069-two-row-all-lengths-strong-solution.md)、[q=6・幅3](items/K0070-width-three-q6-stabilization.md)、[q=5・幅3の厳密閾値](items/K0071-width-three-q5-exact-stabilization.md)、[整数座標の合同式による拡張](items/K0072-mod9-integer-row-separation.md)、[7行盤q=4,5,6の行欠損極大witness帯と安定化長下界](items/K0827-seven-row-q4-q6-deficient-witness-lower-bounds.md)。K0827は現在 M_{7,4}∈[60,1929], M_{7,5}∈[38,1142], M_{7,6}∈[32,862]（有限witness下界・閾値未確定）。
- 最大と極大: [定義](items/K0026-maximum-versus-minimum-maximal.md)、[最大安全サイズ](items/K0029-n1-n9-maximum-safe-sizes.md)、[小盤面の極大サイズ分布](items/K0030-n3-n6-maximal-safe-size-distributions.md)、[7の最小極大](items/K0031-n7-minimum-maximal-size.md)、[10の最小極大の境界](items/K0034-n10-minimum-maximal-bounds.md)、[10の最大安全の境界](items/K0035-n10-maximum-safe-bounds.md)。[最適終局T*とWFT](items/K0295-n1-n7-full-tstar-and-wft.md)は固定証明書の終局一覧とは異なる。
- 幾何と配置構造: [禁止4点組の個数](items/K0057-forbidden-quadruple-counts.md)、[共線4点組の漸近式](items/K0054-collinear-quadruple-asymptotics.md)、[共円4点組のオーダー](items/K0056-cocircular-quadruple-asymptotics.md)、[被覆の上界](items/K0107-sharp-point-cover-bound.md)、[最小極大の一般下界](items/K0106-minimum-maximal-exponent-lower-bound.md)、[素数盤の構成](items/K0095-split-prime-safe-quadratic-construction.md)、[整数放物線の有限検査と未解決の一般化](items/K0097-integer-residue-parabola-bounds.md)、[円格子点数の劣加法性・漸近上界・P(83)=34](items/K0817-circle-strip-subadditivity-and-density-bound.md)、[7行窓の10点円分類](items/K0830-seven-row-ten-point-circle-classification.md)、[二重行の正確な分母補題](items/K0831-circle-row-window-denominator-lemma.md)。
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
