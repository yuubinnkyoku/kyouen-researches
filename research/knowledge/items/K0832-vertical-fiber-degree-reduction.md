---
id: K0832
title: 垂直ファイバー補間による厳密占有縮約 — Σ min(c_b,t)≤q−1
kind: proposition
status: proved
topics: [variants, geometry, grundy]
aliases: []
relations:
- type: generalizes
  target: K0824
  note: K0824の超平面・球面に対するq>2|B|縮約を、各ファイバー上の次数が高々tである多項式超曲面へ一般化する。K0824のq=2|B|境界反例や超平面跡列挙補題を置き換えるものではない
- type: supports
  target: K0504
  note: 底面係数次数を制限しない全多項式族ではΣ min(c_b,t)≤q−1が厳密条件。K0504のdeg f≤kなど底面方向の次数制限付きグラフは別問題であり、補間多項式の底面次数は一般に|B|−1程度まで上がるため未解決
artifacts:
- path: research/experiments/vertical-fiber-interpolation-exact-20261115/report.md
  role: proof
  note: ファイバー根数上界とラグランジュ補間による最大共存数の厳密公式・ゲーム縮約・適用限界
- path: research/experiments/vertical-fiber-interpolation-exact-20261115/verify_interpolation.py
  role: verifier
  note: Fractionによる全4096配置×t=1,2,3の補間達成監査と退化ファイバー障害の確認
- path: research/experiments/vertical-fiber-interpolation-exact-20261115/output/audit.json
  role: data
  note: 12,288配置・768占有ベクトル出現の有限監査結果
- path: research/log/2026-11-15-vertical-fiber-interpolation-exact.md
  role: log
  note: K0832の一様閾値を局面ごとの厳密占有条件へ強化した判断・証明・限界
- path: research/experiments/vertical-fiber-degree-reduction-20261115/report.md
  role: proof
  note: ファイバーごとの根数上界から導く全称縮約定理・適用条件・鋭さの境界例
- path: research/experiments/vertical-fiber-degree-reduction-20261115/verify_boundary.py
  role: verifier
  note: r=1..8・t=1..8の整数単体境界例64件と、次数1..3の既約整数例を検査
- path: research/log/2026-11-15-vertical-fiber-degree-reduction.md
  role: log
  note: 最新main・未解決一覧との照合、定理の選定、有限検証と限界
- path: research/experiments/vertical-fiber-boundary-grundy-20261115/report.md
  role: proof
  note: 境界層が飽和ファイバーの鎖の直和となる全称証明と、底面跡制約付きの十分条件
- path: research/experiments/vertical-fiber-boundary-grundy-20261115/verify_boundary_grundy.py
  role: verifier
  note: 小パラメータの全境界占有ベクトルを再帰mexと排他的論理和公式で照合
- path: research/experiments/vertical-fiber-boundary-grundy-20261115/output/audit.json
  role: data
  note: 64パラメータ組・5,080境界状態の有限完全監査結果
- path: research/log/2026-11-15-vertical-fiber-boundary-grundy.md
  role: log
  note: K0832の境界層Grundy値を鎖分解で厳密化した判断・証明・限界
- path: research/experiments/vertical-fiber-t1-fixed-length-grundy-20261115/report.md
  role: proof
  note: t=1純ファイバーゲームで全終局石数がrmに固定されることから導く全局面Grundy公式
- path: research/experiments/vertical-fiber-t1-fixed-length-grundy-20261115/scripts/verify_t1.py
  role: verifier
  note: 小パラメータ100組・17,368安全状態の再帰mexと固定終局長公式の有限完全照合
- path: research/experiments/vertical-fiber-t1-fixed-length-grundy-20261115/output/audit.json
  role: data
  note: t=1全局面Grundy監査の集計結果
- path: research/log/2026-11-15-vertical-fiber-t1-fixed-length-grundy.md
  role: log
  note: 境界層からt=1全局面へGrundy公式を拡張した判断・証明・限界
- path: research/experiments/vertical-fiber-t2-q3-grundy-20261115/report.md
  role: proof
  note: t=2・q=3・|B|,|A|≥2の純ファイバーゲームにおける全安全局面Grundy分類の全称証明
- path: research/experiments/vertical-fiber-t2-q3-grundy-20261115/verify_t2_q3.py
  role: verifier
  note: 容量上限2の再帰列挙と再帰mexを用いたw,m=2..12の独立照合器
- path: research/experiments/vertical-fiber-t2-q3-grundy-20261115/output/audit.json
  role: data
  note: 121パラメータ組・9,196安全状態の有限監査
- path: research/log/2026-11-15-vertical-fiber-t2-q3-grundy.md
  role: log
  note: t=2・q=3の全分類を選定・証明・検証した判断と限界
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/report.md
  role: proof
  note: t=2,q=5,w≥3,m≥2の純ファイバーゲームにおける全安全局面Grundy値の閉形式分類とmex帰納証明
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/verify_t2_q5.py
  role: verifier
  note: ラベル付き占有ベクトルを直接列挙する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/verify_t2_q5_canonical.py
  role: verifier
  note: 正占有数の多重集合だけで独立に状態・遷移を生成する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q5-grundy-20261115/output/audit.json
  role: data
  note: 150パラメータ組・723,780ラベル状態・11,135多重集合状態の二方式監査集計
- path: research/log/2026-11-15-vertical-fiber-t2-q5-grundy.md
  role: log
  note: K0832の既存成果と最新mainを照合し、t=2,q=5分類を証明・独立監査した記録

- path: research/experiments/vertical-fiber-t2-q4-grundy-20261115/report.md
  role: proof
  note: t=2,q=4,w≥2,m≥2の純ファイバーゲームにおける全安全局面Grundy値の閉形式分類とmex帰納証明
- path: research/experiments/vertical-fiber-t2-q4-grundy-20261115/verify_t2_q4.py
  role: verifier
  note: ラベル付き占有ベクトルと正占有多重集合を独立生成する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q4-grundy-20261115/output/audit.json
  role: data
  note: 209パラメータ組・144,001ラベル状態・4,997多重集合状態の有限監査
- path: research/log/2026-11-15-vertical-fiber-t2-q4-grundy.md
  role: log
  note: K0832のq=3/q=5成果の間を埋めるq=4分類の証明・監査・限界
- path: research/experiments/vertical-fiber-t2-q6-grundy-20261115/report.md
  role: proof
  note: t=2,q=6,w≥2,m≥2の純ファイバーゲームにおける全安全局面Grundy分類と終局偶奇・mex帰納証明
- path: research/experiments/vertical-fiber-t2-q6-grundy-20261115/verify_t2_q6.py
  role: verifier
  note: ラベル付き占有ベクトルと正占有多重集合を独立生成する再帰mex検証器
- path: research/experiments/vertical-fiber-t2-q6-grundy-20261115/output/audit.json
  role: data
  note: 209組・36,860多重集合状態と56組・137,004ラベル状態の監査結果
- path: research/log/2026-11-15-vertical-fiber-t2-q6-grundy.md
  role: log
  note: K0832の既存q=3/4/5成果と重複しないq=6分類の選定・証明・監査・限界
- path: research/experiments/vertical-fiber-t2-q7-grundy-20261115/report.md
  role: proof
  note: 任意qのt=2純ファイバーGrundy上界とq=7の全幅・全高さでの最大値の全称証明
- path: research/experiments/vertical-fiber-t2-q7-grundy-20261115/verify_t2_q7.py
  role: verifier
  note: ラベル付き占有ベクトルと正占有多重集合を独立生成するq=7再帰mex監査
- path: research/experiments/vertical-fiber-t2-q7-grundy-20261115/output/audit.json
  role: data
  note: w=1..10,m=2..12の110組・3,809,674ラベル状態・18,117多重集合状態の監査集計
- path: research/log/2026-11-15-vertical-fiber-t2-q7-grundy.md
  role: log
  note: 最新main・既存q=3..6成果との照合、残余ゲーム分離の発見・証明・監査・適用境界
- path: research/experiments/vertical-fiber-t3-q4-q6-grundy-20261115/report.md
  role: proof
  note: t=3・q=4,5,6・w,m≥2の純ファイバーゲームにおける全安全局面Grundy値の閉形式分類とmex帰納証明
- path: research/experiments/vertical-fiber-t3-q4-q6-grundy-20261115/t3_formulas.py
  role: verifier
  note: q=4,5,6の閉形式Grundy値の実装（二方式監査の被検証側）
- path: research/experiments/vertical-fiber-t3-q4-q6-grundy-20261115/verify_t3_q456.py
  role: verifier
  note: ラベル付き占有ベクトルと正占有多重集合を独立生成する再帰mex検証器
- path: research/experiments/vertical-fiber-t3-q4-q6-grundy-20261115/output/audit.json
  role: data
  note: 627組・18,354多重集合状態と168組・55,692ラベル状態の二方式監査集計
- path: research/log/2026-11-15-vertical-fiber-t3-q4-q6-grundy.md
  role: log
  note: t=3・q=4..6分類の選定・証明・監査・限界と次の課題
- path: research/experiments/vertical-fiber-general-t-grundy-bound-20261116/report.md
  role: proof
  note: 任意次数上限t・任意禁止点数qの純ファイバーゲームで、mとtの偶奇に応じたGrundy一様上界を飽和鎖分離と残余mexで証明
- path: research/experiments/vertical-fiber-general-t-grundy-bound-20261116/verify_general_bound.py
  role: verifier
  note: ラベル付き占有ベクトルと正準占有多重集合を独立生成する再帰mex監査器
- path: research/experiments/vertical-fiber-general-t-grundy-bound-20261116/output/audit.json
  role: data
  note: t=1..5,w=1..4,m=1..7,q=1..tw+2の1,330組・306,979ラベル状態・36,844正準状態の有限監査
- path: research/log/2026-11-16-vertical-fiber-general-t-grundy-bound.md
  role: log
  note: K0832既存のt=2任意q・t=3,q=7結果を一般tへ統一した選定・証明・監査・未解決点
- path: research/experiments/vertical-fiber-t3-q7-full-classification-20261115/report.md
  role: proof
  note: t=3・q=7・w≥1・m≥2の純ファイバーゲーム全安全局面の閉形式Grundy分類の全証明と64状態普遍残余テーブル
- path: research/experiments/vertical-fiber-t3-q7-full-classification-20261115/t3q7_formulas.py
  role: verifier
  note: 分類閉形式の実装（E_TABLEリテラル内蔵・二方式監査の被検験側）
- path: research/experiments/vertical-fiber-t3-q7-full-classification-20261115/verify_t3_q7_full.py
  role: verifier
  note: 多重集合・ラベル付き両エンジンの独立再帰mex監査と閉ボックス230状態mex固定点の完全検査器
- path: research/experiments/vertical-fiber-t3-q7-full-classification-20261115/output/audit.json
  role: data
  note: 228+88組・26,334+179,740状態の二方式監査集計
- path: research/log/2026-11-15-vertical-fiber-t3-q7-full-classification.md
  role: log
  note: t=3・q=7全局面分類の選定・証明・監査と並走の任意t上界との整合確認
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/report.md
  role: proof
  note: t∈{2,3}・全q・全幅・全高さのGrundy最大値定理の証明（d不変量・レジーム閉形式・spawn補題・周期witness族・D≤6閉ボックスH≤2）
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/verify_maxvalue.py
  role: verifier
  note: 分解・p=0/レジーム閉形式・最大値グリッド・witness・sup Hの独立再帰mex監査器（V1..V6）
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/verify_box_h2.py
  role: verifier
  note: D≤6閉ボックス500状態の閉性・mex固定点・値集合・飽和・q=7分類テーブル相互検証・盤面グリッドの検証器（B1..B6）
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/scan_h3_absence.py
  role: verifier
  note: M=3・p=1のD非制約広域boxでのH=3不在走査（61,811状態、D≥7一般予想の有限証拠）
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/output/audit.json
  role: data
  note: V1..V6監査集計（10,734分解照合・516+213組グリッド・269 witness・9,933状態走査、全PASS）
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/output/box_h2.json
  role: data
  note: B1..B6閉ボックス監査集計（500状態固定点・64行テーブル一致・44盤面組673状態、全PASS）
- path: research/experiments/vertical-fiber-t2-t3-all-q-max-20261115/output/h3_scan.json
  role: data
  note: H=3不在広域走査結果（sup H=2）
- path: research/log/2026-11-15-vertical-fiber-t2-t3-all-q-max.md
  role: log
  note: 全q最大値定理の選定・証明・閉ボックスによる残余ケース解消・並走2報告との整合確認
- path: research/experiments/vertical-fiber-all-t-grundy-max-20261116/report.md
  role: proof
  note: 全t・全q・全幅・全高さの純ファイバーゲームGrundy最大値定理の全称証明（t非依存残余座標・Theorem T・完了予算・レジーム補題・witness族）
- path: research/experiments/vertical-fiber-all-t-grundy-max-20261116/verify_all_t_max.py
  role: verifier
  note: 2エンジン独立実装・分解照合・最大値グリッド・Theorem Tパリティ構造・witness・レジーム閉形式の検証器（V0..V6）
- path: research/experiments/vertical-fiber-all-t-grundy-max-20261116/output/audit.json
  role: data
  note: V0..V6監査集計（5,679+200,255状態照合・2,448組グリッド・48,048状態パリティ監査・113 witness、全PASS）
- path: research/log/2026-11-16-vertical-fiber-all-t-grundy-max.md
  role: log
  note: 全t最大値定理の選定・証明・監査・実装バグ2件の発見修正・反映の記録
- path: research/experiments/vertical-fiber-all-t-minwidth-witness-20261116/report.md
  role: proof
  note: 全t値3 witnessの最小幅を3剰余場合に分けて構成し、旧構成の余分な空ファイバーを訂正する全称証明
- path: research/experiments/vertical-fiber-all-t-minwidth-witness-20261116/verify_minwidth_witness.py
  role: verifier
  note: 元の占有多重集合ゲームの再帰mexで810 witnessと60個の最小幅直前盤面を検査
- path: research/experiments/vertical-fiber-all-t-minwidth-witness-20261116/output/audit.json
  role: data
  note: 810 witness・60境界検査・13,001状態訪問の監査結果（全PASS）
- path: research/log/2026-11-16-vertical-fiber-all-t-minwidth-witness.md
  role: log
  note: 旧V5の未検査剰余境界を特定し、最小幅構成を補正・独立監査した判断記録

scope: r≥1、有限非空B⊂R^r、有限A⊂R、盤B×A。底面跡族Tの柱T×Aと、deg_z(F)≤tかつ全b∈BでF(b,.)≢0を満たす全多項式族（底面係数次数は無制限）を禁止対象とする。配置Sの多項式族との最大共存数はΣ_b min(c_b,t)と厳密に一致し、安全性は底面跡容量条件とΣ_b min(c_b,t)≤q−1の同時成立と同値。境界層Grundy公式はT=∅の純多項式ルールで全称、T≠∅では飽和ファイバー全充填後も全跡容量が保たれる場合の十分系。さらにT=∅かつt=1では全局面でG(S)=(m·min(|B|,q−1)−|S|) mod 2。さらにT=∅、t=2、q=3、|B|≥2、|A|≥2では全安全局面のGrundy値を占有ベクトルの形状とmの偶奇で完全分類する。 さらに底面跡制約なし・t=2・q=4・|B|≥2・|A|≥2では全安全局面のGrundy値を閉形式で完全分類し、|B|=2では最大1、|B|≥3ではm偶数で最大1・奇数で最大2となる。さらに底面跡制約なし・t=2・q=5・|B|≥3・|A|≥2では、全安全局面のGrundy値を占有多重集合の9型に分けて閉形式で完全分類し、m偶数で最大1、m奇数で最大3となる。 さらに底面跡制約なし・t=2・q=6では、w=2は二鎖の直和、w=3またはm偶数は全終局石数の偶奇固定により全Grundy値が0/1。w≥4かつm奇数は容量5の全占有型を閉形式分類し、最大値3（最小証人w=4,m=3,c=(2,1,1,0)）。 さらに底面跡制約なし・t=2の任意q純ファイバーゲームでは、m偶数なら全Grundy値≤1、m奇数なら≤3。特にq=7ではw≤3またはm偶数で最大1、w≥4かつm奇数で最大3（証人c=(m,m−1,1,0,…,0)）。 さらに底面跡制約なし・t=3・q=4,5,6・|B|≥2・|A|≥2では全安全局面のGrundy値を閉形式で完全分類する。最大値はq=4ではm偶数かつm≥4で2（未飽和単独ファイバー(2)が値2を取る、t=2に現れない現象）、q=5ではm偶数かつm≥4で2（m奇数またはm=2では全系でG=|S| mod 2）、q=6ではw=2またはm奇数・m=2で1、w≥3かつm偶数≥4で2。 さらにT=∅・t=3・q=7・w≥1・m≥2では全安全局面のGrundy値を閉形式で完全分類する。w=1は純鎖でG=(m−c_1) mod 2、w≥2では鎖XOR x=⊕_{c_b≥3}((m−c_b) mod 2)と残余ゲームへの分解G=x⊕H(ρ)を用い、m奇数はG=x⊕(min(R,L) mod 2)、m=2はG=min(6−|S|,2w−|S|) mod 2、m≥4偶数はG=x⊕E(R,min(e_0,R),e_1,e_2)（Eはm・wに非依存な64状態の普遍残余テーブル、値は0/1/2）。値3の局面は占有型(a,2,0,…,0)（a≥3奇数、w≥3、m≥4偶数）ちょうどに限り、先行の最大値定理（max G=3 iff w≥3かつm≥4偶数）は系として回収される。 さらに底面跡制約なし・純ファイバーゲームの任意次数上限t・任意qについて、m<tまたはm≡t (mod 2) なら全局面Grundy値≤1、m>tでm≠t (mod 2) なら奇数tで≤t・偶数tで≤t+1。t=2の既知任意q上界とt=3のq=7上界を含む一般定理。t≥4の鋭さは未確定。 さらに底面跡制約なし・t∈{2,3}の任意q≥2・任意w≥1・任意m≥1では、全安全局面のGrundy値の最大値が完全決定される：cap=q−1、M=min(t,m)、p=(m−M) mod 2として、cap=0で0、p=0またはq≥twで1、p=1かつq≤tw−1でmin(3,⌊cap/t⌋+1)（すなわちcap≤t−1で1、t≤cap≤2t−1で2、cap≥2tで3）。t=3のp=1ではD=R+e_1+2e_2=cap−3s≤6の閉ボックスとe_0飽和により残余H≤2が全称成立し、(0,3)経由の値3はcap≤5で排除される。 さらに底面跡制約なし・純ファイバーゲームの任意次数上限t≥2・任意q≥2・任意幅w≥1・任意高さm≥1でも全安全局面のGrundy値の最大値が完全決定される：cap=q−1、M=min(t,m)、p=(m−M) mod 2として、cap=0で0、p=0またはq≥twで1、p=1かつq≤tw−1でmin(3,⌊cap/t⌋+1)。残余mex Hはt・Mに非依存で常にH≤2（Theorem T）であり、任意のt≥2で普遍的にG≤3、値3はp=1かつcap≥2tでのみ現れる。
evidence: 全称数学的証明。各ファイバーの根数上界Σ min(c_b,t)と、分離線形形式に沿うラグランジュ補間による上界達成から、全多項式族に対する最大共存数を厳密決定。底面跡容量条件と合わせて安全性・合法手・Grundy値を占有ベクトルへ厳密縮約する。境界層C(c)=q−1では飽和ファイバーの鎖分解からGrundy値の排他的論理和公式を全称証明し、底面跡制約付きの十分条件も証明。2×2底面・3高さの補間監査に加え、w,m,t≤4の64組・5,080境界状態を独立再帰で有限監査。t=1の固定終局長補題から全局面Grundy公式を全称証明し、w≤5,m≤4,q≤w+2の100組・17,368安全状態を再帰mexで有限監査。t=2・q=3の全分類は容量2の三状態型への場合分けとmexによる全称証明。w,m=2..12の121組・9,196状態を専用再帰検証器で有限監査し、不一致0件。 t=2,q=5の分類は容量4の安全占有型（空・単独列・二列・(a,1,1)・四単独列）を網羅し、各型の合法子とmexを後ろ向きに解く全称証明。w=3..12,m=2..16の150組でラベル付き723,780状態と独立な多重集合11,135状態を再帰mex照合し、不一致0。有限監査は証明の代替ではない。 t=2,q=4の分類は容量3の安全占有型（空・単独列・(1,b)・三単独列）を網羅し、各遷移とmexを全称的に場合分けした。w=2..12,m=2..20の209組でラベル付き144,001状態と独立な多重集合4,997状態を再帰mex照合し、不一致0。有限監査は証明の代替ではない。  t=2,q=6の全分類は、w=2の独立鎖・w=3またはm偶数の終局偶奇補題・w≥4かつm奇数の占有型mex帰納証明による。209組・36,860多重集合状態と56組・137,004ラベル状態の独立再帰監査で不一致0。有限監査は全称証明の代替ではない。 任意qの上界は、占有数2以上のファイバーを長さm−c_bの独立鎖へ分離し、空数e・単独石数ℓ・残容量Rの残余ゲームH_pへ帰着する全称証明。m偶数ではH_0=min(R,2e+ℓ) mod 2、m奇数ではH_1の相異なる子値が高々2個。q=7の正確な最大値はこの分解・終局偶奇・明示証人から全称証明。w=1..10,m=2..12の110組・3,809,674ラベル状態・18,117多重集合状態の二方式再帰mex監査は不一致0で、有限監査は証明の代替ではない。 t=3・q=4..6の分類は、鎖成分高々1個と1・2の成分列という安全型制限・終局特徴づけ・終局偶奇補題・純鎖補題による場合分けmex帰納証明。w=2..12,m=2..20の627組・18,354多重集合状態とw=2..8,m=2..9の168組・55,692ラベル状態の独立2方式再帰mex監査で不一致0。有限監査は全称証明の代替ではない。 t=3・q=7の全局面分類は、飽和ファイバーの鎖分離とXOR-mex補題による分解定理G=x⊕H(ρ)（x=1なら可動な奇数鎖が必ず存在する）、m奇数とm=2の固定残余手数閉形式、e_0≥Rでの飽和補題E(R,e_0,·)=E(R,R,·)、閉ボックス230状態でのmex固定点の機械的完全検査とRに関する普遍性帰納による全称証明。多重集合エンジンw=1..12,m=2..20の228組・26,334状態とラベル付きエンジンw=1..8,m=2..12の88組・179,740状態を独立再帰mexで照合し不一致0、値3計数2,490=15×166は先行最大値監査のヒストグラムと完全一致。有限監査は全称証明の代替ではない。 任意t上界は飽和ファイバーを残り長m−c_iの独立鎖へ分離し、未飽和占有レベル0..t−1の相異なる手型が高々tであることから残余mex H≤tを得る全称証明。m≡tでは残容量Rと未飽和残り増加数Lが全手で同時に1減り、残余プレイ長min(R,L)固定からH≤1。m<tでは全終局石数min(q−1,wm)固定。t=1..5,w=1..4,m=1..7,q=1..tw+2の1,330組・306,979ラベル状態・36,844正準状態を独立再帰mexで監査し不一致0。有限監査は無界証明の代替ではない。 t∈{2,3}全q最大値は、全安全局面でR−L=cap−twが一定というd不変量、レジームR≥L−1での閉形式H=(L−n) mod 2（系としてq≥twでは最大値1）、spawn到達不能ならH=R mod 2（系としてH≥2⇒cap≥t）、G=3が(1,2)経由ならcap≥2t、cap周期2tの明示witness族、およびt=3・p=1・cap≤6でのD≤6閉ボックス500状態mex固定点完全列挙＋e_0飽和補題によるH≤2の全称証明から決定される。V1..V6（10,734状態分解照合・516+213組最大値グリッド・269 witness・9,933状態sup H走査）とB1..B6（500状態固定点・q=7分類の64行普遍テーブルとの完全一致・44盤面組673状態）の独立再帰mex監査は不一致0。有限監査は全称証明の代替ではない。 全t全q最大値は、残余座標(R;X;z)への分解G=x⊕H（完了手はκ=(m−M) mod 2の鎖をspawnし、残余再帰からtとMが消える）、Theorem T（偶数Rでは値0と値1の選択肢が共通の合法な孫を持つことのケース分析により0と1を同時に含まない、奇数Rでは選択肢⊆{0,1}、強帰納で全t一挙にH≤2）、完了予算補題（D'=cap−t·s<tなら以後完了不可で残余プレイ長min(R,L)固定、H≤1、cap<tなら最大値1）、p=0の固定残余長H=min(R,L) mod 2、レジーム補題（R≥L−1でH=(L−n) mod 2、不変量R−L=cap−Mw、系としてq≥twでは最大値1）、x=1が飽和鎖の存在を要求することによるG=3⟹cap≥2t、およびH(1;X;z)=2のwitness状態と必要幅⌈(cap+2)/t⌉がq≤tw−1と丁度一致する陽明証人族による全称証明。t∈{2,3}先行定理の完全一般化であり、t≥4の普遍的G≤3はここで初めて証明された。V0..V6監査（5,679ラベル照合・200,255状態分解照合・2,448組最大値グリッド・48,048状態Theorem Tパリティ監査・113 witness・748点レジーム閉形式）は不一致0、二回の実行でbyte-identical。有限監査は全称証明の代替ではない。
---

# 垂直ファイバー次数による一般縮約

## 一様閾値の定理（従来結果）

有限集合 B⊂R^r、|B|=w、有限高さ集合 A⊂R、|A|=m とし、盤を X=B×A とする。各 b∈B のファイバーを {b}×A と呼ぶ。

底面の指定された跡族を T とし、各 T∈T に対して柱 T×A 上の q点共存を禁止する。さらに、多項式超曲面 F(x,z)=0 上の q点共存も禁止する。ただし各 F は、全ての b∈B について一変数多項式 F(b,z) が零多項式ではなく、その z次数が高々 t であると仮定する。特に、zについてmonicな多項式はこの条件を自動的に満たす。

q>tw なら、多項式超曲面による禁止条件は一度も発生しない。したがって安全性は、底面跡容量条件だけで完全に判定できる。

配置 S⊂B×A の各ファイバー占有数を c_b=|S∩({b}×A)| と置くと、

\[
S\text{ が安全}
\iff
\sum_{b\in T}c_b\le q-1
\quad(\forall T\in\mathcal T).
\]

合法手は、ある一成分 c_b を1増やして全容量制約を保つ操作と一致する。従って同じ占有ベクトルを持つ全てのセル配置は同じ子占有ベクトル集合を持ち、Grundy値も一致する。状態数は高々 (m+1)^w である。

## 証明

固定した F と b∈B を取る。F(b,z) は零多項式ではない次数高々tの一変数多項式だから、異なる実根は高々t個である。従ってファイバー {b}×A と F=0 の交点は高々t点であり、盤全体では

\[
|(B\times A)\cap\{F=0\}|
\le\sum_{b\in B}t=tw.
\]

q>tw なので、どの配置も F=0 上に q点を含めない。多項式超曲面による禁止は消え、柱 T×A にq点を含むかどうかだけが残る。その点数は正確に Σ_{b∈T}c_b である。

また、柱の条件は占有ベクトルだけで決まる。あるファイバーに空きがあれば、そのファイバー内のどの空き高さへ石を置いても同じ子占有ベクトルになる。従って同じ c を持つ配置の子状態集合は一致し、終局からの帰納法でGrundy値も一致する。

## 既存の共円ゲームへの系

- 長軸に平行でないアフィン超平面は、各ファイバーと高々1点で交わる。したがって t=1。
- 通常の球面は、各直線ファイバーと高々2点で交わる。球面方程式は高さ z についてmonicな二次式なので t=2。
- より一般に、各ファイバー上で零多項式にならない z次数t以下の多項式超曲面を追加しても、q>tw ならゲームは変わらない。

従ってK0824の q>2w 縮約は t=2 の場合として回収される。K0824が別途示した超平面跡の個数上界や q=2w の球面反例は、本項目では置き換えない。

## 補間による正確な占有条件（q≤t|B|も含む）

従来の \(q>tw\) は全配置に対する一様十分条件だが、個々の配置ではもっと鋭い判定ができる。全ての底面係数多項式を許し、各ファイバー上では零多項式にならない全族 \(\mathcal F_t(B)\) に対し、

\[
\boxed{\max_{F\in\mathcal F_t(B)}|S\cap\{F=0\}|=\sum_{b\in B}\min(c_b,t)}
\]

が成立する。上界は各ファイバーの根数から従う。達成は、各ファイバーで選んだ石を根に含むモニック次数t多項式 \(P_b\) を作り、そのt未満の係数をB上のラグランジュ補間で一斉に実現すればよい。得られるFは全ファイバーでモニックなので、零多項式となるファイバーはない。

従って、底面跡容量条件に加えて

\[
\boxed{\sum_{b\in B}\min(c_b,t)\le q-1}
\]

を課すことが、全多項式族版の安全性の必要十分条件になる。合法手・子占有ベクトル集合・Grundy値もこの条件だけで決まる。

この等式は、係数の底面次数を制限しない全族についてのもの。固定底面次数や既約性を課した部分族では、補間による上界達成を保証しない。

## 境界層のGrundy値

底面跡制約を持たない純粋なファイバー多項式ルールでは、境界層
\[
\sum_{b\in B}\min(c_b,t)=q-1
\]
の全局面は、その層の中だけに子を持つ。Grundy値は
\[
\boxed{
G(c)=\bigoplus_{\substack{b\in B\\c_b\ge t}}
\bigl((m-c_b)\bmod 2\bigr)
}
\]
である。

実際、未飽和ファイバー \(c_b<t\) への追加は容量和を1増やして不合法になる。一方、飽和済みファイバー \(c_b\ge t\) への追加は容量和を変えず、\(c_b<m\) なら合法である。飽和済みファイバーはその後も飽和済みのままなので、境界層のゲームは長さ \(m-c_b\) の一方向の鎖の直和となる。長さ \(h\) の鎖のGrundy値は \(h\bmod2\) であり、直和の値は各成分の排他的論理和である。∎

底面跡族 \(\mathcal T\) も同時に課す場合、さらに
\[
\sum_{b\in T}c_b+
\sum_{\substack{b\in T\\c_b\ge t}}(m-c_b)
\le q-1
\quad(\forall T\in\mathcal T)
\]
が成立すれば、飽和済みファイバーを全て満杯にしても全跡容量を超えない。この場合は全ての鎖の手が最後まで合法で、同じGrundy公式が成立する。この条件を満たさない一般の跡制約付き局面には公式を適用しない。

## t=1 の全局面Grundy値

底面跡制約を持たない純ファイバー多項式ルールで t=1 とする。安全条件は非空ファイバー数が
\[
r=\min(|B|,q-1)
\]
以下であることに等しい。終局はちょうど r 本のファイバーを全て満杯にした局面であり、全終局の石数は rm で一定となる。

各着手は石数を1増やすので、任意の安全局面 S から終局までの全ての最大長着手列は rm−|S| 手である。一般に、全ての最大長着手列の長さが L で一定の有限通常プレイゲームでは、帰納法によりGrundy値は L mod 2 となる。従って
\[
\boxed{G(S)=(rm-|S|)\bmod2.}
\]
これは境界層だけでなく、t=1の全内部層を含む。底面跡制約を同時に課す場合や t≥2 の内部層には、この固定終局長の議論を適用しない。

## 境界 q=tw の鋭さ

任意の t≥1 について、一般の多項式超曲面族では q>tw の不等号を弱められない。r次元単体の頂点

\[
B=\{0,e_1,\ldots,e_r\},\qquad w=r+1
\]

を底面に取り、高さ A={1,...,t} とする。多項式

\[
F(x,z)=\prod_{j=1}^{t}(z-j)
\]

は次数tでmonic、盤 B×A の全tw点を含む。一方、Bのどのアフィン超平面跡 T も |T|≤r=w−1 なので、全ファイバーにt点ずつ置いた占有ベクトル c_b=t は

\[
\sum_{b\in T}c_b=t|T|
\le t(w-1)=tw-t\le tw-1=q-1
\]

を満たす。従って底面跡容量判定は安全と判定するのに、実際にはF上にq点がある。Fはt>1では可約だが、次数t以下の多項式超曲面を許す一般定理の境界反例として十分である。

さらに次数1〜3については、既約な整数係数の境界例もある。Bを同じ単体とし、x₁を第一底面座標とする。

- t=1: F=z−x₁。x₁=0のファイバーでは高さ0、x₁=1では高さ1を選ぶ。
- t=2: F=z(z−3)+2x₁。x₁=0では高さ {0,3}、x₁=1では {1,2} を選ぶ。
- t=3: F=z(z−4)(z−5)−12x₁。x₁=0では {0,4,5}、x₁=1では {1,2,6} を選ぶ。

いずれも各ファイバーにちょうどt点ずつ置き、全tw点が同一超曲面上に載る。各式はx₁について一次で、その係数が非零定数なので多項式環上既約である。高さは全て整数である。

## t=2・q=3 の全局面Grundy値（|B|,|A|≥2）

底面跡制約のない純ファイバー多項式ゲームで、ファイバー次数上限を \(t=2\)、禁止点数を \(q=3\) とする。K0832の厳密占有条件は

\[
\sum_{b\in B}\min(c_b,2)\le2
\]

となる。\(w=|B|\ge2\)、\(m=|A|\ge2\) のとき、安全局面は次の三種類しかない。

1. 空局面。
2. 一つのファイバーだけが非空。
3. 異なる二つのファイバーに1個ずつ石がある。

全局面のGrundy値は

\[
G(c)=
\begin{cases}
0,&\operatorname{supp}(c)=\varnothing,\\
(m-c_b)\bmod2,
 &\operatorname{supp}(c)=\{b\},\ c_b\ge2,\\
1,&\operatorname{supp}(c)=\{b\},\ c_b=1,\ m\text{ 偶数},\\
2,&\operatorname{supp}(c)=\{b\},\ c_b=1,\ m\text{ 奇数},\\
0,&\operatorname{supp}(c)=\{b_1,b_2\},\ c_{b_1}=c_{b_2}=1.
\end{cases}
\]

証明は三種類の分類に帰着する。一つのファイバーに2個以上ある局面は残り \(m-c_b\) 手の鎖。二つの単独石の局面は終局。一つの単独石の局面では、同じ列を2個にする鎖型局面と、別の列を開始する終局の二種類へ移るため、

\[
G=\operatorname{mex}\{0,(m-2)\bmod2\}
=
\begin{cases}
1&m\text{ 偶数},\\
2&m\text{ 奇数}.
\end{cases}
\]

空局面の全ての子は同じGrundy値1または2を持つので、空局面の値は0。従って全安全局面のGrundy値は0,1,2に限られる。

特に \(w=2,m=3,c=(0,1)\) では、二つの子のGrundy値が0と1となり、\(G(0,1)=2\)。これは \(t=1\) の全局面公式を \(t=2\) に単純延長できない反例である。

有限監査として、\(2\le w,m\le12\) の121組・9,196安全状態を再帰mexと照合し、不一致0件。全称性は上記の数学的証明による。

## 限界

- F(b,z)≡0を許し底面次数を制限しない場合、Bを分離する線形形式ℓに対するG(x)=∏_{b∈B}(ℓ(x)−ℓ(b))が全Bで消え、F=Gは盤全体を含む。従って非零ファイバー条件は非自明な分類に必要。底面次数制限付きで退化ファイバーを許す場合は別問題。
- 全多項式族・底面係数次数無制限・各ファイバー非零という範囲ではq≤twも上のΣ min(c_b,t)条件で完全分類した。K0504のdeg f≤kの固定次数グラフは補間次数が制限を越え得るため未解決。
- 有限検証は境界例の確認であり、全称縮約の証明は根数上界による。
- K0504の共多項式変種のうち、底面係数次数無制限の任意グラフ z=f(x) はt=1として占有ファイバー数で完全分類できる。K0504が提案するdeg f≤kの固定次数版は本項目の補間次数制限を満たすとは限らず、必要十分条件は未解決。


## t=2・q=4の純ファイバー全局面Grundy分類

底面跡制約なし、\(t=2,q=4,w=|B|\ge2,m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,2)\le3.
\]
安全占有型は空、単独列 \((a)\)、二列 \((1,b)\)、三単独列 \((1,1,1)\) に限られる。

全局面のGrundy値は次である。
\[
G(())=(m+1)\bmod2,\qquad G((a))=(m-a+1)\bmod2,
\]
\[
G((1,b))=(m-b)\bmod2\quad(b\ge2),
\]
\[
G((1,1))=
\begin{cases}
(m+1)\bmod2&w=2,\\
1&w\ge3,\ m\text{ 偶数},\\
2&w\ge3,\ m\text{ 奇数},
\end{cases}
\qquad G((1,1,1))=0.
\]
従って最大Grundy値は、\(w=2\) では常に1、\(w\ge3\) ではm偶数で1・m奇数で2。Grundy値2の最小証人は \(w=m=3,c=(1,1,0)\) であり、子の値は1と0。

証明は、\((1,b)\ (b\ge2)\) が一方向の鎖、三単独列が終局、二単独石は第三列開始の有無で分岐することを使う。単独列と空局面はその後ろ向きmexから確定する。全証明と適用限界はartifactのreport.mdに記載した。

有限監査はw=2..12,m=2..20の209組。ラベル付き144,001状態と独立な多重集合4,997状態を再帰mexで照合し、不一致0。これは有限監査であり、全称性は上記の帰納証明による。

## t=2・q=5の純ファイバー全局面Grundy分類

底面跡制約なしの純ファイバーゲームで \(t=2,q=5\)、\(w=|B|\ge3,m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,2)\le4.
\]
安全占有多重集合は \(()\)、\((a)\)、\((a,b)\)、\((a,1,1)\)、\((1,1,1,1)\) に限られる。\(p_a=(m-a)\bmod2\) と置くと、Grundy値は次で完全分類される。

| 占有型 | Grundy値 |
|---|---|
| 空 | \(1\) iff \(w=3\) かつ \(m\) 奇数、その他0 |
| \((1)\) | \(m\) 偶数なら1。奇数なら \(w=3\) で0、\(w\ge4\) で2 |
| \((a),a\ge2\) | \(p_a\) |
| \((1,1)\) | \(m\) 奇数かつ \(w=3\) のとき1、その他0 |
| \((1,b),b\ge2\) | \(m\) 偶数なら \(b\) 偶数で1・奇数で0。\(m\) 奇数なら \(b\) 偶数で3・奇数で2 |
| \((a,b),a,b\ge2\) | \(p_a\oplus p_b\) |
| \((1,1,1)\) | \(m\) 偶数なら1。奇数なら \(w=3\) で0、\(w\ge4\) で2 |
| \((a,1,1),a\ge2\) | \(p_a\) |
| \((1,1,1,1)\) | 0 |

従って
\[
\boxed{\max G=
\begin{cases}
1&m\text{ 偶数},\\
3&m\text{ 奇数}.
\end{cases}}
\]
最小のGrundy値3の証人は \(w=m=3,c=(2,1,0)\)。三つの子 \((3,1,0),(2,2,0),(2,1,1)\) の値がそれぞれ \(2,0,1\) なので、親の値は \(\operatorname{mex}\{0,1,2\}=3\)。

証明では、二飽和列は二つの鎖の直和、\((a,1,1)\) は一つの鎖、\((1,b)\) は \(x_b=\operatorname{mex}\{p_2\oplus p_b,p_b,x_{b+1}\}\)（終端では \(x_m=\operatorname{mex}\{p_2\}\)）を後ろ向きに解く。\((1,1,1)\)、\((1,1)\)、単独列、空局面を順にmexで確定する。詳細な全証明は上記report artifactに保存した。

有限監査は \(3\le w\le12,2\le m\le16\) の150組。ラベル付き占有ベクトル723,780状態と、正占有数の多重集合11,135状態を別々の再帰mexで検査し、閉形式との不一致は0。これは有限範囲の監査であり、全称性は場合分け証明による。対象は抽象ファイバー多項式ゲームで、標準二次元の3×m・q=5幾何ゲームとは別である。


## t=2・q=6の純ファイバー全局面Grundy分類

底面跡制約なし、\(t=2,q=6,w=|B|\ge2,m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,2)\le5.
\]
幅2では二つの独立鎖なので \(G(S)=|S|\bmod2\)。幅3では全終局が \((m,m,1)\) で石数が奇数、また \(m\) 偶数なら幅3以上の全終局型 \((m,m,1),(m,1,1,1),(1,1,1,1,1)\) の石数が全て奇数である。従って \(w=3\) または \(m\) 偶数では \(G(S)=(|S|+1)\bmod2\)。

\(w\ge4,m\) 奇数では、Grundy値は正占有多重集合で次のように完全分類される。

| 占有型 | Grundy値 |
|---|---:|
| \(()\) | \(1\) |
| \((a)\) | \((m-a)\bmod2\) |
| \((1,1),w=4\) | \(2\) |
| その他の \((a,b)\) | \((a+b+1)\bmod2\) |
| \((1,1,1),w=4\) | \(1\) |
| \((1,1,1),w\ge5\) | \(0\) |
| \((a,1,1),a\ge2\) | \(2+((m-a)\bmod2)\) |
| \((a,b,1),a\ge b\ge2\) | \((a+b)\bmod2\) |
| \((1,1,1,1),w=4\) | \(0\) |
| \((1,1,1,1),w\ge5\) | \(2\) |
| \((a,1,1,1),a\ge2\) | \((a+1)\bmod2\) |
| \((1,1,1,1,1),w\ge5\) | \(0\) |

容量5以下の安全型の網羅と、各型の遷移に対するmex帰納証明は、artifactのreport.mdに記録した。従って最大Grundy値は \(w\le3\) または \(m\) 偶数で1、\(w\ge4,m\) 奇数で3。最小のGrundy値3の証人は \(w=4,m=3,c=(2,1,1,0)\) で、三つの子の値は2,0,1である。

有限監査は \(2\le w\le12,2\le m\le20\) の209組・36,860多重集合状態、および \(2\le w\le8,2\le m\le9\) の56組・137,004ラベル状態。独立再帰mexとの不一致は0。対象は抽象ファイバーゲームであり、標準二次元3×m・q=6の幾何ゲームを解決したものではない。


## t=2・q=7の純ファイバーGrundy最大値と任意q上界

安全条件 Σ_b min(c_b,2)≤6 の純ファイバーゲームでは、全安全局面の最大Grundy値は、m偶数またはw≤3で1、m奇数かつw≥4で3。任意qについても、t=2純ファイバーゲームの全Grundy値はm偶数で高々1、m奇数で高々3。証明と適用境界は上記の証明資料を参照。

## t=3・q=4〜6の純ファイバー全局面Grundy分類

底面跡制約なし、\(t=3\)、\(w=|B|\ge2,m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,3)\le q-1.
\]
容量3を超える寄与は各ファイバー3で打ち切られるため、安全な正占有多重集合は3以上の鎖成分を高々1個と1・2の成分列で構成される（補題1）。終局特徴づけ（補題2）、終局偶奇補題（補題3、t=2版と同一）、純鎖補題（補題4）と合わせて、\(q=4,5,6\) の全安全局面のGrundy値を閉形式で完全分類できる。全証明はartifactのreport.mdに記載した。

**q=4（容量\(3=t\)）** の全局面Grundy値：

| 占有型 | Grundy値 |
|---|---:|
| \(()\) | \(1\) |
| \((1)\) | \(0\) |
| \((2)\) | \(m\) 偶数かつ \(m\ge4\) のとき \(2\)、それ以外は \(1\) |
| \((a),\ a\ge3\) | \((m-a)\bmod2\)（純鎖） |
| \((1,1)\) | \(1\) |
| \((2,1)\) | \(0\)（終局） |
| \((1,1,1)\) | \(0\)（終局、\(w\ge3\)） |

最大値は \(m\) 偶数かつ \(m\ge4\) で2（最小証人 \(w=2,m=4,c=(2,0)\)）。**未飽和の単独ファイバー \((2)\) がGrundy値2を取る**のは、単独列が常に鎖で値高々1の \(t=2\) には現れない現象である。

**q=5（容量\(4=t+1\)）**：終局は \((2,2)\),\((2,1,1)\),\((1,1,1,1)\)（4石）と \((m,1)\)（\(m+1\) 石、\(m\ge3\)）。\(m\) 奇数または \(m=2\) では全終局の石数の偶奇が一致し、全系で \(G=|S|\bmod2\)。\(m\) 偶数かつ \(m\ge4\) では \((1)\) と \((2,1)\) が値2、\((2)\) は1、\((a),a\ge3\) は \((m-a+1)\bmod2\)、\((a,1),a\ge3\) は純鎖 \((m-a)\bmod2\)、\((1,1,1)\) は1、\((1,1)\) は0、\(()\) は0、\((2,2)\),\((2,1,1)\),\((1^4)\) は終局値0。最大値2（最小証人 \(w=2,m=4,c=(1,0)\)）。

**q=6（容量\(5=t+2\)）** は三領域に分かれる。

- \(w=2\)（全\(m\)）と \(w\ge3,\ m\) 奇数：\(G=(m+2-|S|)\bmod2\)。\(w=2\) は終局型 \((m,2)\) が一意、\(m\) 奇数は終局型 \((m,2),(m,1,1)\) と5石型が全て同偶奇。
- \(w\ge3,\ m=2\)：鎖成分が存在せず、終局は全部5石で \(G=(5-|S|)\bmod2\)。
- \(w\ge3,\ m\) 偶数かつ \(m\ge4\)：終局の偶奇が混在するため16型の表で完全分類する（\(()\)=0、\((1)\)=1、\((2)\)=0、\((1,1)\)=2、\((2,1)\)=1、\((2,2)\)=2、\((2,1,1)\)=2、\((1,1,1)\)=0、\((1^4)\)=1、鎖族は \((m-a)\)/(\(m-a+1\)\) パターン、\((2,2,1)\),\((2,1,1,1)\),\((1^5)\) は終局値0）。最大値2（最小証人 \(w=3,m=4,c=(1,1,0)\)）。

有限監査は多重集合エンジンで \(2\le w\le12,2\le m\le20\) の627組・18,354状態、ラベル付きエンジンで \(2\le w\le8,2\le m\le9\) の168組・55,692状態を独立に再帰mex生成して閉形式と照合し、不一致0。有限監査は全称証明の代替ではなく、全称性は場合分けmex帰納による。対象は底面跡制約なしの抽象ファイバー多項式ゲームであり、標準二次元盤や特定の幾何学盤の勝敗は主張しない。\(w=1\)、\(m=1\)、底面跡制約付き、\(q\ge7\)（容量 \(6=2t\)）は本節の範囲外である。


## t=3・q=7の純ファイバー全局面Grundy分類

底面跡制約なし、\(t=3\)、\(q=7\)、\(w=|B|\ge1\)、\(m=|A|\ge2\) とする。安全条件は
\[
\sum_b\min(c_b,3)\le6.
\]
\(s=\#\{c_b\ge3\}\)、\(e_i=\#\{c_b=i\}\ (i=1,2)\)、\(e_0=w-\#\{c_b>0\}\)、\(x=\bigoplus_{c_b\ge3}\bigl((m-c_b)\bmod2\bigr)\)、\(R=6-3s-e_1-2e_2\)、\(L=3e_0+2e_1+e_2\) と置くと、全安全局面のGrundy値は次で完全に決まる。
\[
\boxed{
\begin{aligned}
& w=1: && G=(m-c_1)\bmod2,\\
& w\ge2,\ m\text{ 奇数}: && G=x\oplus\bigl(\min(R,L)\bmod2\bigr),\\
& w\ge2,\ m=2: && G=\min(6-|S|,\,2w-|S|)\bmod2,\\
& w\ge2,\ m\ge4\text{ 偶数}: && G=x\oplus E\bigl(R,\min(e_0,R),e_1,e_2\bigr).
\end{aligned}}
\]
\(E\) は \(m\) にも \(w\) にも依存しない64状態の普遍残余テーブル（値は0,1,2）で、reportの付録に全行を掲載する。

証明は、飽和ファイバーの鎖分離（補題1）、残余ゲームへの分解定理 \(G=x\oplus H(\rho)\)（補題2、XOR-mex補題：\(x=1\) なら可動な奇数鎖が必ず存在し鎖の着手が mex に入る）、\(m\) 奇数の固定残余手数（補題3）、\(m=2\) の固定残余手数（補題4）、\(e_0\ge R\) での飽和 \(E(R,e_0,\cdot)=E(R,R,\cdot)\)（補題5）、閉ボックス230状態での mex 固定点の機械的完全検査と \(R\) に関する普遍性帰納（補題6）による。補題1〜5は paper-and-pencil の全称証明、補題6の本体は有限状態集合の完全機械検査であり、その組み合わせで分類は全称的である。

**系1（値3の完全特徴づけ）.** Grundy値3の安全局面は、\(m\ge4\) 偶数・\(w\ge3\) のとき占有型 \((a,2,0,\ldots,0)\)（\(a\ge3\) 奇数、飽和1本・2石1本・空1本以上）ちょうどに限る。値3の計数はラベル付き \(w=1..8,m=2..12\) で \(15\times166=2490\)（先行最大値監査のヒストグラムと一致）、多重集合 \(w=1..12,m=2..20\) で \(45\times10=450\)。

**系2（占有型別の値表）.** \(m\ge4\) 偶数・\(w\ge2\) の占有型23型についての閉形式値表はreportに掲載した。

**系3（最大値定理の回収）.** 分類より \(\max G=3\) iff \(w\ge3\) かつ \(m\ge4\) 偶数、それ以外で1。先行する最大値定理を系として完全に回収する。

有限監査は多重集合エンジン \(1\le w\le12,\ 2\le m\le20\) の228組・26,334状態とラベル付きエンジン \(1\le w\le8,\ 2\le m\le12\) の88組・179,740状態を独立再帰mexで生成し、閉形式・状態射影・対ごとの最大値の不一致0、二回の実行で監査JSONはbyte-identical。

検証器SHA-256: 618d0548e1fb192f644275ca56216255c10f08f74cd0a4cd2b11ee0b05cfe2a3。数式実装SHA-256: e4afc515668aacff351c3544dd7e2e75b738632d83ba7c86dfb63a7bc27e4a80。監査JSON SHA-256: 8cf377e05715c99a2b99d1a49b65a672cf010f4463da62a78543af4e854eb592。

[証明・監査報告](../../experiments/vertical-fiber-t3-q7-full-classification-20261115/report.md)、
[閉形式実装](../../experiments/vertical-fiber-t3-q7-full-classification-20261115/t3q7_formulas.py)、
[再帰mex検証器](../../experiments/vertical-fiber-t3-q7-full-classification-20261115/verify_t3_q7_full.py)、
[監査結果](../../experiments/vertical-fiber-t3-q7-full-classification-20261115/output/audit.json)、
[研究ログ](../../log/2026-11-15-vertical-fiber-t3-q7-full-classification.md)。

本分類は次節の任意次数上限 \(t\) への一様上界の \(t=3,q=7\) の場合の精密化である：\(m\) 奇数では \(m\equiv t\pmod2\) の上界1と一致し、\(m\ge4\) 偶数では上界 \(t=3\) を恰好に達成し、達成局面を系1が完全に特徴づける。対象はK0832の縮約後の抽象純ファイバーゲームであり、標準二次元幾何ゲームの勝敗は主張しない。


## 任意の次数上限 t に対する純ファイバーGrundy一様上界

底面跡制約なしの純ファイバーゲームで、任意の有限幅 \(w\ge1\)、高さ \(m\ge1\)、次数上限 \(t\ge1\)、禁止点数 \(q\ge1\) を取る。安全条件は
\[
\sum_{i=1}^{w}\min(c_i,t)\le q-1.
\]
全安全局面のGrundy値は
\[
\boxed{
G(S)\le
\begin{cases}
1,&m<t\ \text{または}\ m\equiv t\pmod2,\\
t,&m>t,\ m\not\equiv t\pmod2,\ t\text{ 奇数},\\
t+1,&m>t,\ m\not\equiv t\pmod2,\ t\text{ 偶数}.
\end{cases}}
\]
である。

証明は[独立した証明報告](../../experiments/vertical-fiber-general-t-grundy-bound-20261116/report.md)を参照。飽和ファイバー \(c_i\ge t\) は残り長 \(m-c_i\) の独立鎖となり、その排他的論理和 \(x\) は0/1。未飽和レベル \(0,\ldots,t-1\) の手型は高々t種類なので、残余mex \(H\le t\)。新たに飽和したファイバーの鎖nimberは \((m-t)\bmod2\)。これが0なら残容量と未飽和残り増加数が同時に1減り、残余プレイ長が固定されて \(H\le1\)。これが1なら \(x\oplus H\) から奇数tで上界t、偶数tで上界t+1を得る。\(m<t\) は安全条件が総石数上限に退化し、全終局石数が固定される。

有限監査は \(t=1..5,w=1..4,m=1..7,q=1..tw+2\) の1,330組。ラベル付き306,979状態と正準36,844状態を別々に再帰mex生成し、不一致0。これは有限監査であり、無界定理の証明は上記の帰納議論による。監査範囲での最大観測値は3だったが、\(t\ge4\) の普遍的な \(G\le3\) は、次々節の全t最大値定理により \(t\ge2\) 全般で証明され、最大値自体が閉形式で完全決定された。標準二次元幾何ゲームや底面跡制約付き部分族の勝敗は主張しない。

## t∈{2,3}・全q・全幅・全高さのGrundy最大値

底面跡制約なしの純ファイバーゲームで \(t\in\{2,3\}\)、\(q\ge2\)、\(w\ge1\)、\(m\ge1\) とする。\(cap=q-1\)、\(M=\min(t,m)\)、\(p=(m-M)\bmod2\) と置くと、全安全局面のGrundy値の最大値は
\[
\max_{S\text{ safe}}G(S)=
\begin{cases}
0,&cap=0,\\
1,&p=0\ \text{または}\ q\ge tw,\\
\min\bigl(3,\ \lfloor cap/t\rfloor+1\bigr),&p=1\ \text{かつ}\ q\le tw-1
\end{cases}
\]
と完全決定される（最終行では \(cap\le t-1\) で1、\(t\le cap\le 2t-1\) で2、\(cap\ge2t\) で3）。

証明は[独立した証明報告](../../experiments/vertical-fiber-t2-t3-all-q-max-20261115/report.md)を参照。構成要素は、(1) 全安全局面で \(R-L=cap-tw\) が一定というd不変量、(2) レジーム \(R\ge L-1\) での閉形式 \(H=(L-n)\bmod2\)（全子共通値。系として \(q\ge tw\) では全局面がレジーム内で最大値1、従来の実験的境界 \(tw\ge cap+2\) の証明本体）、(3) spawn到達不能なら \(H=R\bmod2\le1\)、よって \(H\ge2\Rightarrow cap\ge t\)、\(G=3\) が(1,2)経由なら \(cap\ge2t\)、(4) capについて周期 \(2t\) の明示witness族（必要幅は \(cap+2\le tw\) と丁度一致）、(5) \(t=3\)・\(p=1\)・\(cap\le6\) では \(D=R+e_1+2e_2=cap-3s\le6\) の閉ボックス500状態のmex固定点完全列挙と \(e_0\) 飽和補題により残余 \(H\le2\) が全称成立し、(0,3)経由の値3が \(cap\le5\) で排除される。\(t=2\) では手型2種より \(H\le2\) が自明。これで[t=3・q=7全局面分類](../../experiments/vertical-fiber-t3-q7-full-classification-20261115/report.md)の系3（\(\max G=3\) iff \(w\ge3\) かつ \(m\ge4\) 偶数）が任意qの境界として回収され、cap=6のwitness \((3,2)\) は同分類の系1の占有型 \((a,2,0,\ldots)\)（a=3）と一致する。\(D\le6\) 閉ボックスは同分類の補題6（\(D\in\{0,3,6\}\)、cap=6）を独立実装で再導出し、付録の普遍テーブル \(E\)（64行）との完全一致を機械確認した。

有限監査は検証器2基による。[閉形式・最大値監査器](../../experiments/vertical-fiber-t2-t3-all-q-max-20261115/verify_maxvalue.py)（V1分解10,734状態・V2/V3閉形式5,180+8,489状態・V4/V4b最大値グリッド516+213組・V5 witness 269検査・V6 sup H走査9,933状態、全PASS）と[閉ボックス検証器](../../experiments/vertical-fiber-t2-t3-all-q-max-20261115/verify_box_h2.py)（B1閉性・B2固定点500状態・値集合\(\{0,1,2\}\)・B3非制約再帰一致・B4飽和1,470検査・B5 q=7分類テーブル64行完全一致・B6盤面44組673状態、全PASS、2回実行でbyte-identical）。\(D\ge7\) での一般予想「\(M=3,p=1\) なら常に \(H\le2\)」（[広域走査](../../experiments/vertical-fiber-t2-t3-all-q-max-20261115/scan_h3_absence.py)で61,811状態 \(\sup H=2\)）は、次節の全t最大値定理のTheorem T（残余mexは \(t\) にも \(M\) にも依存せず常に \(H\le2\)）により全 \(M\)・全 \(t\) で証明された。標準二次元幾何ゲームの勝敗は主張しない。

## 全t・全q・全幅・全高さのGrundy最大値

底面跡制約なしの純ファイバーゲームで任意の次数上限 \(t\ge2\)、\(q\ge2\)、\(w\ge1\)、\(m\ge1\) とする。\(cap=q-1\)、\(M=\min(t,m)\)、\(p=(m-M)\bmod2\) と置くと、全安全局面のGrundy値の最大値は
\[
\max_{S\text{ safe}}G(S)=
\begin{cases}
0,&cap=0,\\
1,&p=0\ \text{または}\ q\ge tw,\\
\min\bigl(3,\ \lfloor cap/t\rfloor+1\bigr),&p=1\ \text{かつ}\ q\le tw-1
\end{cases}
\]
と完全決定される（最終行は \(cap\le t-1\) で1、\(t\le cap\le2t-1\) で2、\(cap\ge2t\) で3）。\(t=1\) は固定終局長の先行定理に帰着し本式の対象外である。

証明は[独立した証明報告](../../experiments/vertical-fiber-all-t-grundy-max-20261116/report.md)による。構成要素は次の通り。

1. **分解定理** \(G=x\oplus H(R;X;z)\)。飽和ファイバー \(c\ge t\) は残り長 \(m-c\) の独立鎖でそのXORを \(x\)、未飽和ファイバーは余剰 \(M-1-c\) のトークン（\(X\)）とレベル \(M-1\) の計数 \(z\)、\(R=cap-\sum\min(c_b,t)\)。完了手（レベル \(M-1\to M\)）は残り長 \(m-M\) の鎖をspawnし、そのnimber \(\kappa=(m-M)\bmod2=p\) が残余mexに入る。**残余再帰から \(t\) も \(M\) も消える**ため、以降の補題は全tに一挙に適用できる。
2. **Theorem T（残余mexの一様上界）**。任意の \((R;X;z)\) で \(H\le2\)。奇数 \(R\) では選択肢 \(\subseteq\{0,1\}\)。偶数 \(R\) では値0と値1の2つの子が必ず共通の合法な孫 \(d\)（偶数レベル \(R-2\)）を持ち、\(e(d)\ge2\) が帰納仮定 \(H(d)\le1\) と矛盾することから選択肢は0と1を同時に含まない（\(H\le1\)）。共通孫のケース分析は (a) 2つのA手、(b) A手とB手（\(x=2\) と \(x\ge3\) の両サブケースで一致）、(c) A/B手と完了手（\(（R-2;X-x+(x-1);z-1)\) または \(（R-2;X-1;z)\) ）、(d) 完了手どうしは不可能。証明は \(\kappa\) にも \(t\) にも依存せず、従って**任意の \(t\ge2\) で普遍的に \(G=x\oplus H\le3\)**。t2-t3レーンの一般予想「\(M=3,p=1\) なら常に \(H\le2\)」は全 \(M\)・全 \(t\) で解決された。
3. **完了予算補題（spawn補題）**。\(D'=cap-t\cdot s\)（\(s\)=飽和本数）は残余手で不変、完了で \(t\) 減る。\(D'<t\) なら以後完了不可で残余プレイはA/B手のみとなり全プレイ長が \(\min(R,L)\) に固定、\(H\le1\)。特に \(cap\le t-1\) では全到達可能局面で \(G\le1\)。
4. **\(p=0\) の固定残余長**。\(\kappa=0\) なら完了手も通常手になり、残余プレイ長は \(\min(R,L)\) に固定、\(H=\min(R,L)\bmod2\le1\)、\(G\le1\)。既知の「\(m<t\) または \(m\equiv t\pmod2\) なら \(G\le1\)」を余剰座標から再証明する。
5. **レジーム補題**。\(R\ge L-1\) では \(H=(L-n)\bmod2\le1\)（\(n=|X|+z\)、帰納法でA/B手の子は \((L-n)-1\)、完了手の選択肢は \(\kappa\oplus(L-n)\bmod2\)）。不変量 \(R-L=cap-Mw\) と合わせ、\(q\ge tw\)（\(m\ge t\)）では全局面がレジーム内で最大値1。
6. **\(G=3\Rightarrow cap\ge2t\)**。Theorem Tにより \(G=3\) は \(x=1\wedge H=2\) 経由のみ。\(x=1\) は飽和鎖の存在 \(s\ge1\) を、\(H=2\) はspawn補題により \(cap-t\cdot s\ge t\) を要求し、併せて \(cap\ge2t\)。
7. **値3の最小幅 witness族（補正）**。\(p=1\)・\(m>t\) とし、\(cap=2t+\mu t+r\)、\(\mu\ge0\)、\(0\le r<t\) と置く。占有数は常に \(t,t-1\)、さらに \(\mu\) 個の満杯ファイバー \(m\) を置く。残りは次の3場合に分ける。

   - \(r=0\): 空ファイバーを1本残す。幅 \(w=\mu+3\)。
   - \(1\le r\le t-2\): 占有数 \(r\) のファイバーを1本置き、空ファイバーは残さない。幅 \(w=\mu+3\)。
   - \(r=t-1\): 占有数 \(t-1\) のファイバーをもう1本置き、空ファイバーを1本残す。幅 \(w=\mu+4\)。

   いずれも消費容量は \(t+(t-1)+\mu t+r=cap-1\)、従って \(R=1\)。占有数 \(t\) の鎖は残り手数 \(m-t\) が奇数なので \(x=1\)、占有数 \(t-1\) が \(z\ge1\)、空ファイバーまたは中間占有 \(r\) が \(X\ne\varnothing\) を与える。よって \(H(1;X;z)=\operatorname{mex}\{0,1\}=2\)、\(G=x\oplus H=3\)。幅は
   \[
   w=\begin{cases}
   \mu+3 & 0\le r\le t-2,\\
   \mu+4 & r=t-1
   \end{cases}
   =\left\lceil\frac{cap+2}{t}\right\rceil.
   \]
   これより小さい幅 \(w'\) では \(tw'\le cap+1=q\) となり、既証明の \(q\ge tw'\) レジーム補題から全局面 \(G\le1\)。従って \(\lceil(cap+2)/t\rceil\) は値3を実現する最小幅である。

   旧報告・旧V5構成は \(1\le r\le t-2\) でも空ファイバーを余分に確保していたため、この剰余範囲の最小幅証人を直接監査していなかった。定理自体は変わらず、余分な空ファイバーを除いた構成と境界検査を[補正報告](../../experiments/vertical-fiber-all-t-minwidth-witness-20261116/report.md)に記録した。

これにより \(t\in\{2,3\}\) 先行定理は全tへ完全一般化され、任意t一様上界の未解決点（\(t\ge4\) の普遍的 \(G\le3\)）は閉じ、上界 \(t,t+1\) は3に精密化される。\(t=3,q=7\)（\(cap=6=2t\)）では「\(w\ge3\) かつ \(m\ge4\) 偶数で最大3」が \(p=1\)・\(cap\ge2t\)・\(q\le3w-1\) として回収され、cap=6の証人 \((3,2)\) はwitness族（\(j=1\)）の構成そのものである。

有限監査は[検証器](../../experiments/vertical-fiber-all-t-grundy-max-20261116/verify_all_t_max.py)による: V0 ラベル付きと多重集合の2エンジン独立実装照合5,679状態、V1 分解の状態ごと照合200,255状態（\(t\in\{2..6\},w\in\{1..5\},m\in\{2..9\}\)、オーバーシュート状態を含む）、V2/V3 最大値閉形式グリッド2,448組、V4 Theorem Tパリティ構造48,048状態（偶数\(R\)の\(H\le1\)・奇数\(R\)の\(H\le2\)・偶数\(R\)の選択肢への{0,1}共存なし、\(\sup H=2\)）、V5 witness族113検査、V6 レジーム閉形式748点、全て不一致0で二回の実行はbyte-identical。有限監査は全称証明の代替ではなく、全称性は証明による。標準二次元幾何ゲームの勝敗は主張しない。

[証明・監査報告](../../experiments/vertical-fiber-all-t-grundy-max-20261116/report.md)、
[検証器](../../experiments/vertical-fiber-all-t-grundy-max-20261116/verify_all_t_max.py)、
[監査結果](../../experiments/vertical-fiber-all-t-grundy-max-20261116/output/audit.json)、
[研究ログ](../../log/2026-11-16-vertical-fiber-all-t-grundy-max.md)。
