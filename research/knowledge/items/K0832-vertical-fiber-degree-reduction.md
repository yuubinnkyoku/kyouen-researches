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
- path: research/experiments/vertical-fiber-single-token-residual-closed-form-20261116/report.md
  role: proof
  note: 単一未飽和ファイバー残余閉形式の全称証明・空ファイバー/cap補題・U座標の注意・全1族の有限観察
- path: research/experiments/vertical-fiber-single-token-residual-closed-form-20261116/verify_single_token.py
  role: verifier
  note: 2エンジン独立実装・全グリッド照合・広域mex恒等式・cap補題・構造一貫性の検証器（V0..V5+V3b）
- path: research/experiments/vertical-fiber-single-token-residual-closed-form-20261116/output/audit.json
  role: data
  note: 8,706,159照合・不一致0・二回実行byte-identicalの監査集計
- path: research/log/2026-11-16-vertical-fiber-single-token-residual-closed-form.md
  role: log
  note: 残余閉形式第一段階（κ=1）の選定・証明・誤帰納の検出と修正・限界
- path: research/experiments/vertical-fiber-all-ones-residual-structure-20261116/report.md
  role: proof
  note: 全1族残余構造の報告（2位置閉形式予想・スライス閉形式・補題P・tail系・R*安定化データ）
- path: research/experiments/vertical-fiber-all-ones-residual-structure-20261116/verify_all_ones.py
  role: verifier
  note: 坍縮/一般多重集合2エンジン・W1..W5閉形式監査器（35,004照合・不一致0）
- path: research/experiments/vertical-fiber-all-ones-residual-structure-20261116/output/audit.json
  role: data
  note: W0..W5監査集計（不一致0・二回実行byte-identical）
- path: research/log/2026-11-16-vertical-fiber-all-ones-residual-structure.md
  role: log
  note: 全1族解析の選定・重複回避確認・機械検証・限界の記録
- path: research/experiments/vertical-fiber-all-ones-induction-proof-20261116/report.md
  role: proof
  note: 全1族残余mexの全称定理 h=U の機械支援帰納証明（基底・z=0ステップ・15比較族アトム表・シグネチャ決定性・被覆補題・3,803類完全列挙）と系A・系B
- path: research/experiments/vertical-fiber-all-ones-induction-proof-20261116/verify_induction_proof.py
  role: verifier
  note: published U とアトム表転写 U_tab の二重経路で全実現シグネチャのステップ恒等式を検証する計約330万照合の検証器
- path: research/experiments/vertical-fiber-all-ones-induction-proof-20261116/output/audit.json
  role: data
  note: B0/S2/S3/C1/E1..E7監査集計（C_box=C_wit=C_sat=3,803種・双方向包含0/0、全照合不一致0・二回実行byte-identical）
- path: research/log/2026-11-16-vertical-fiber-all-ones-induction-proof.md
  role: log
  note: 機械検証済み予想から全称定理への昇格の判断・証明構造・独立検証の記録

- path: research/experiments/vertical-fiber-high-z-multiset-merge-20261116/report.md
  role: proof
  note: κ=1の一般残余ゲームでz≥ΣX+R−1なら任意多重集合が総和Sの単一トークンへ縮約される全称帰納証明と既知高Rレジームとの有限中間帯
- path: research/experiments/vertical-fiber-high-z-multiset-merge-20261116/verify_high_z_merge.py
  role: verifier
  note: ソート済み多重集合再帰と順序付きトークン再帰の独立照合器
- path: research/experiments/vertical-fiber-high-z-multiset-merge-20261116/output/audit.json
  role: data
  note: 8,568全列挙照合・120固定seed照合・領域外反例の監査結果
- path: research/log/2026-11-16-vertical-fiber-high-z-multiset-merge.md
  role: log
  note: 最新main・既存未解決事項との照合、高余裕領域縮約の選定・証明・有限監査・次課題
- path: research/experiments/vertical-fiber-height-only-collapse-20261116/report.md
  role: proof
  note: κ=1の一般多重集合でR≤z+1なら総和Sの単一トークンへ縮約する全称証明、R≤2の全z例外、R≥3での一様条件の鋭さ
- path: research/experiments/vertical-fiber-height-only-collapse-20261116/verify_height_only_merge.py
  role: verifier
  note: ソート済み多重集合再帰・順序付き再帰・単一トークン閉形式の独立照合器
- path: research/experiments/vertical-fiber-height-only-collapse-20261116/output/audit.json
  role: data
  note: 高さ安定性8,364件・全列挙4,788件・小R全z 3,780件・散点160件・鋭さ証人38件、全て不一致0
- path: research/log/2026-11-16-vertical-fiber-height-only-collapse.md
  role: log
  note: 最新main・未解決事項との照合、低R縮約の発見・証明・監査・中間帯縮小
- path: research/experiments/vertical-fiber-two-token-residual-2positions-20261116/report.md
  role: source
  note: 2トークン族残余2位置集合の閉形式予想（ラダー・家族B・家族A）の命題・抽出過程・43,241照合の出典
- path: research/experiments/vertical-fiber-two-token-residual-2positions-20261116/verify_two_token.py
  role: verifier
  note: 素朴・ラベル付き・cap付き3エンジン相互照合と閉形式・系A・高余裕帯・tailレジームとの整合検証器
- path: research/experiments/vertical-fiber-two-token-residual-2positions-20261116/output/audit.json
  role: data
  note: 43,241照合・不一致0・二回実行byte-identicalの監査結果
- path: research/log/2026-11-16-vertical-fiber-two-token-residual-2positions.md
  role: log
  note: 閉形式予想の抽出・修正過程・破損出力の教訓・未証明範囲と次課題
- path: research/experiments/vertical-fiber-two-token-z0-slice-20261116/report.md
  role: proof
  note: 2トークン族X=(x,y)のz=0スライスで全Grundy値を閉形式決定するR強帰納証明
- path: research/experiments/vertical-fiber-two-token-z0-slice-20261116/verify_z0_slice.py
  role: verifier
  note: cap付き正準多重集合再帰とcapなし順序付きラベル再帰の独立有限照合器
- path: research/experiments/vertical-fiber-two-token-z0-slice-20261116/output/audit.json
  role: data
  note: x≤60・全y≤x・R≤x+y+4の120,780状態照合、不一致0、二回実行byte-identical
- path: research/log/2026-11-16-vertical-fiber-two-token-z0-slice.md
  role: log
  note: 既存2トークン予想のz=0スライスを選定・証明・独立監査した判断記録
- path: research/experiments/vertical-fiber-ceiling-stable-2positions-20261116/report.md
  role: source
  note: 天井トークン付き残余ゲームの値2位置分類予想（ラダー＋再帰位置族）の命題・抽出過程・11,212照合の出典
- path: research/experiments/vertical-fiber-ceiling-stable-2positions-20261116/verify_ceiling.py
  role: verifier
  note: cap付き正準多重集合エンジンとcapなし順序ラベルエンジンの相互照合・証明済み単一トークン閉形式照合・2/3トークン元ゲームブリッジを含む独立検証器
- path: research/experiments/vertical-fiber-ceiling-stable-2positions-20261116/output/audit.json
  role: data
  note: m≤7全グリッド・all-ones・遠方tail・高z・エンジン相互照合・cap補題・Theorem T・ブリッジを含む11,212照合、全て不一致0・二回実行byte-identical
- path: research/log/2026-11-16-vertical-fiber-ceiling-stable-2positions.md
  role: log
  note: 3トークン安定コア抽出から全m再帰位置族の確定までの判断記録・テスト側順序バグの教訓・次課題
- path: research/experiments/vertical-fiber-three-token-transient-band-20261116/report.md
  role: source
  note: 3トークン過渡帯の値2位置予想（対角線・c≤−(2k+1)スライス統一形・OK表m=2..8）の命題・抽出過程・36,958照合の出典
- path: research/experiments/vertical-fiber-three-token-transient-band-20261116/verify_transient.py
  role: verifier
  note: cap付き正準多重集合エンジンとcapなし順序ラベルエンジンの相互照合・予想U・A/B/C・対角線OK表の双方向検証器
- path: research/experiments/vertical-fiber-three-token-transient-band-20261116/output/audit.json
  role: data
  note: E1..E6監査集計（36,958照合・不一致0・二回実行byte-identical）
- path: research/log/2026-11-16-vertical-fiber-three-token-transient-band.md
  role: log
  note: 過渡帯掃引の選定・旧m=4観察行の訂正・統一形の発見過程・次課題
- path: research/experiments/vertical-fiber-transient-band-extension-20261116/report.md
  role: source
  note: 予想Uのk=1..8拡大・対角線OK表のm=9/m=10確定・偶数統一形の発見の命題と41,575照合の出典
- path: research/experiments/vertical-fiber-transient-band-extension-20261116/verify_extension.py
  role: verifier
  note: 前報2エンジンを再利用したk=4..8全グリッド・m=9/m=10抽出グリッド・偶数統一形双方向の検証器
- path: research/experiments/vertical-fiber-transient-band-extension-20261116/output/audit.json
  role: data
  note: G1..G5監査集計（41,575照合・不一致0・二回実行byte-identical）
- path: research/log/2026-11-16-transient-band-extension.md
  role: log
  note: 成果選定・偶数統一形の発見経緯・m=8全1特例の位置づけ・次課題

- path: research/experiments/vertical-fiber-two-token-z1-slice-20261116/report.md
  role: proof
  note: 2トークン族X=(x,y)のz=1スライスで全Grundy値を閉形式決定するR強帰納証明
- path: research/experiments/vertical-fiber-two-token-z1-slice-20261116/verify_z1_slice.py
  role: verifier
  note: cap付き正準多重集合再帰とcapなし順序ラベル再帰の独立有限照合器
- path: research/experiments/vertical-fiber-two-token-z1-slice-20261116/output/audit.json
  role: data
  note: x≤80・全y≤x・R≤x+y+7の288,360状態、偶奇301,320点、tail32,400点の監査
- path: research/log/2026-11-16-vertical-fiber-two-token-z1-slice.md
  role: log
  note: z=1スライスの選定・全称証明・独立監査・z≥3への引継ぎ
- path: research/experiments/vertical-fiber-diagonal-m11-m16-20261116/report.md
  role: source
  note: 対角線OK表のm=11..16外挿・偶数統一形のmod 4修正・all-ones族プロファイルの命題と14,638照合の出典
- path: research/experiments/vertical-fiber-diagonal-m11-m16-20261116/verify_diag_m11_m16.py
  role: verifier
  note: 前報2エンジン再実装・奇数族/修正統一形/all-ones族の双方向監査器（D1..D9・グループ間メモ解放）
- path: research/experiments/vertical-fiber-diagonal-m11-m16-20261116/output/audit.json
  role: data
  note: D1..D9監査集計（14,638照合・不一致0・二回実行byte-identical）
- path: research/log/2026-11-16-diagonal-m11-m16.md
  role: log
  note: mod 4特例の発見経緯・all-ones族の単一化・OOMと偽陽性誤読の教訓・次課題

scope: r≥1、有限非空B⊂R^r、有限A⊂R、盤B×A。底面跡族Tの柱T×Aと、deg_z(F)≤tかつ全b∈BでF(b,.)≢0を満たす全多項式族（底面係数次数は無制限）を禁止対象とする。配置Sの多項式族との最大共存数はΣ_b min(c_b,t)と厳密に一致し、安全性は底面跡容量条件とΣ_b min(c_b,t)≤q−1の同時成立と同値。境界層Grundy公式はT=∅の純多項式ルールで全称、T≠∅では飽和ファイバー全充填後も全跡容量が保たれる場合の十分系。さらにT=∅かつt=1では全局面でG(S)=(m·min(|B|,q−1)−|S|) mod 2。さらにT=∅、t=2、q=3、|B|≥2、|A|≥2では全安全局面のGrundy値を占有ベクトルの形状とmの偶奇で完全分類する。 さらに底面跡制約なし・t=2・q=4・|B|≥2・|A|≥2では全安全局面のGrundy値を閉形式で完全分類し、|B|=2では最大1、|B|≥3ではm偶数で最大1・奇数で最大2となる。さらに底面跡制約なし・t=2・q=5・|B|≥3・|A|≥2では、全安全局面のGrundy値を占有多重集合の9型に分けて閉形式で完全分類し、m偶数で最大1、m奇数で最大3となる。 さらに底面跡制約なし・t=2・q=6では、w=2は二鎖の直和、w=3またはm偶数は全終局石数の偶奇固定により全Grundy値が0/1。w≥4かつm奇数は容量5の全占有型を閉形式分類し、最大値3（最小証人w=4,m=3,c=(2,1,1,0)）。 さらに底面跡制約なし・t=2の任意q純ファイバーゲームでは、m偶数なら全Grundy値≤1、m奇数なら≤3。特にq=7ではw≤3またはm偶数で最大1、w≥4かつm奇数で最大3（証人c=(m,m−1,1,0,…,0)）。 さらに底面跡制約なし・t=3・q=4,5,6・|B|≥2・|A|≥2では全安全局面のGrundy値を閉形式で完全分類する。最大値はq=4ではm偶数かつm≥4で2（未飽和単独ファイバー(2)が値2を取る、t=2に現れない現象）、q=5ではm偶数かつm≥4で2（m奇数またはm=2では全系でG=|S| mod 2）、q=6ではw=2またはm奇数・m=2で1、w≥3かつm偶数≥4で2。 さらにT=∅・t=3・q=7・w≥1・m≥2では全安全局面のGrundy値を閉形式で完全分類する。w=1は純鎖でG=(m−c_1) mod 2、w≥2では鎖XOR x=⊕_{c_b≥3}((m−c_b) mod 2)と残余ゲームへの分解G=x⊕H(ρ)を用い、m奇数はG=x⊕(min(R,L) mod 2)、m=2はG=min(6−|S|,2w−|S|) mod 2、m≥4偶数はG=x⊕E(R,min(e_0,R),e_1,e_2)（Eはm・wに非依存な64状態の普遍残余テーブル、値は0/1/2）。値3の局面は占有型(a,2,0,…,0)（a≥3奇数、w≥3、m≥4偶数）ちょうどに限り、先行の最大値定理（max G=3 iff w≥3かつm≥4偶数）は系として回収される。 さらに底面跡制約なし・純ファイバーゲームの任意次数上限t・任意qについて、m<tまたはm≡t (mod 2) なら全局面Grundy値≤1、m>tでm≠t (mod 2) なら奇数tで≤t・偶数tで≤t+1。t=2の既知任意q上界とt=3のq=7上界を含む一般定理。t≥4の鋭さは未確定。 さらに底面跡制約なし・t∈{2,3}の任意q≥2・任意w≥1・任意m≥1では、全安全局面のGrundy値の最大値が完全決定される：cap=q−1、M=min(t,m)、p=(m−M) mod 2として、cap=0で0、p=0またはq≥twで1、p=1かつq≤tw−1でmin(3,⌊cap/t⌋+1)（すなわちcap≤t−1で1、t≤cap≤2t−1で2、cap≥2tで3）。t=3のp=1ではD=R+e_1+2e_2=cap−3s≤6の閉ボックスとe_0飽和により残余H≤2が全称成立し、(0,3)経由の値3はcap≤5で排除される。 さらに底面跡制約なし・純ファイバーゲームの任意次数上限t≥2・任意q≥2・任意幅w≥1・任意高さm≥1でも全安全局面のGrundy値の最大値が完全決定される：cap=q−1、M=min(t,m)、p=(m−M) mod 2として、cap=0で0、p=0またはq≥twで1、p=1かつq≤tw−1でmin(3,⌊cap/t⌋+1)。残余mex Hはt・Mに非依存で常にH≤2（Theorem T）であり、任意のt≥2で普遍的にG≤3、値3はp=1かつcap≥2tでのみ現れる。 さらに残余mex H(R;X;z)の単一未飽和ファイバー（X=(x)）の場合が全パラメータx≥1,z≥0,R≥0で閉形式決定された：z=0はmin(R,x) mod 2、1≤z≤x−1はm=q(z)、z≥x+1はm=q(x)（q(k)はk以下最大の奇数）として奇数R≤mで2・偶数R≤mで0・z<xの中間帯m<R<L−1=x+zで(R+z) mod 2・それ以外はx mod 2、z=xは奇数R≤2x−1で2・偶数R≤x−1で0・それ以外x mod 2（L=x+z+1）。残余値2は奇数RかつR≤μ(x,z)（z=xでμ=2x−1、z≠xでμ=min(x,z)以下の最大奇数）ちょうどに限り、全t最大値定理が未決定として残した「どの(R;X;z)でH=2となるか」の単一トークン切片が閉じた。空ファイバーは恒等的に0、一般多重集合ではcap補題H(R;X;z)=H(R;cap_{R+1}(X);z)（トークン値≥R+1はR+1に置換可能）が成立し、各固定Rの残余状態空間は有限になる。 さらに残余mexの全1族 X=(1^k)（複数トークン・状態(k,z,R)に坍縮）では、全(k,z,R)の値が統一スライス閉形式 U(k,z,R)（z=0はU0(k,R)）として全称決定された（R前進帰納・15比較族アトム表によるシグネチャ決定性・3,803シグネチャ類の完全列挙と被覆補題による機械支援全称証明）。プレイ長=min(R,2k+z)・tail閉形式（R≥2k+z−1ならk mod 2）はその証明済み構成要素であり、値2位置集合の全(k,z)閉形式（z=0：空、z奇：{1,3,…,q(k)}、z偶：{1,3,…,q(min(k,z))}∪{2k−z+1}）とスライスz=1,2の全プロファイル閉形式は主定理の系A・系Bとして昇格された。 さらにκ=1の一般残余ゲームでS=ΣXと置くと、z≥S+R−1では任意の有限多重集合Xが総和Sの単一トークンへ厳密縮約され、Hは奇数R≤q_o(S)で2・偶数R≤q_o(S)で0・それ以外S mod 2となる。既知の高Rレジームと合わせ、固定X,zで追加解析が必要なRは幅2S+|X|−3の有限中間帯に限られる。 さらに2トークン族X=(x,y)（x≥y≥1）の残余2位置集合については、ラダー（奇数R≤q_o(min(S,z))）・家族B（PT角 y=y*=(z−d)/2 上の区間と、z+d≡2 (mod 4)・y≥y* でのEXT δ=(z+d)/2）・家族A（d=z+1のランとd≥z+2の定常 δ_A=最小奇数≥z）の3族からなる閉形式が予想として提案された（有限監査43,241照合・不一致0・全称性は未証明）。 さらに天井トークン付き残余ゲーム T_inf(X;z)={R≥1: H(R; X∪{R+1}; z)=2}（Xはm個のトークン多重集合・昇順t_0≤…≤t_{m-1}）では、値2位置集合がラダー{奇数R≤z+1}からR=z+1を除いた集合と再帰位置族 p_0=2t_0+δ_A(z)、p_1=2t_1+δ_A(z+1)、p_j=2t_j+p_{j-2}+2 の和集合に一致することが予想された（m≤7・11,212照合・不一致0・全称性は未証明）。ラダー部分は証明済み単一トークン閉形式・高さのみ縮約・cap補題からの系として全称に成立し、系として2トークン・3トークン元ゲームのcap境界内側 R∈[max(z+2,y), x−1] の値2位置はそれぞれ 2y+δ_A(z)、{2w+δ_A(z), 2y+δ_A(z+1)} と一致する（同じ有限監査による支持）。 さらに3トークン族X=(x,y,w)の過渡帯（x<R<S+z+2）の奇数スライス R=2x−(2k+1) では、x=y+w+z+j と置くと帯条件内の値2位置が統一形（k≥1: (j=0∧w=1) は z≥2k、それ以外は 2(k+1−j−w)≤z≤2(k+1−j−w)+1、いずれもy非依存。k=0 は j∈{0,2} が全OK・j=1 は z=0 のみ・j≥3 は帯外の特異形）に従うことが予想され、対角線 2x_max=S+z・R=2x_max−1 におけるOK条件は m=2..8 で有限表化された（36,958照合・不一致0・全称性は未証明）。 拡張監査では予想Uのスライス範囲がk=1..8で反例なく拡大し、対角線OK条件はm=9（rest[:7]=(1⁷)・z任意）とm=10（z=1: rest[:8]=(1⁸)、z=0: (rest[:7]=(1⁷)∧rest[7]=2)∨(rest[:6]=(1⁶)∧rest[6]=2∧rest[7]=2)、z≥2なし）まで確定、奇数族（m≥5: rest[:m−2]=(1^{m−2})・z任意）と偶数統一形（m=2r≥6: z=1ならrest[:2r−2]=(1^{2r−2})、z=0なら接頭辞長2r−3か2r−4で2が現れる2項・m=8のみrest=(1⁷)特例、z≥2なし）が予想として提案された（41,575照合・不一致0・全称性は未証明）。 外挿監査では奇数族がm=11,13,15で反例なく拡大（支持点m=5,7,9,11,13,15の6点）、偶数統一形のall-ones特例はm≡0 (mod 4)でちょうど現れることが確定し（m=12,16陽性・m=6,10,14不在）、修正統一形（z=0のc1∨c2にm≡0 mod 4ならrest=(1^{m−1})を追加）とall-ones単一族プロファイル H(2k−1;(k,1^k);0)=1 (k≡1 mod 4) / 2 (その他)（k=1..25）が予想として提案された（14,638照合・不一致0・全称性は未証明）。
evidence: 全称数学的証明。各ファイバーの根数上界Σ min(c_b,t)と、分離線形形式に沿うラグランジュ補間による上界達成から、全多項式族に対する最大共存数を厳密決定。底面跡容量条件と合わせて安全性・合法手・Grundy値を占有ベクトルへ厳密縮約する。境界層C(c)=q−1では飽和ファイバーの鎖分解からGrundy値の排他的論理和公式を全称証明し、底面跡制約付きの十分条件も証明。2×2底面・3高さの補間監査に加え、w,m,t≤4の64組・5,080境界状態を独立再帰で有限監査。t=1の固定終局長補題から全局面Grundy公式を全称証明し、w≤5,m≤4,q≤w+2の100組・17,368安全状態を再帰mexで有限監査。t=2・q=3の全分類は容量2の三状態型への場合分けとmexによる全称証明。w,m=2..12の121組・9,196状態を専用再帰検証器で有限監査し、不一致0件。 t=2,q=5の分類は容量4の安全占有型（空・単独列・二列・(a,1,1)・四単独列）を網羅し、各型の合法子とmexを後ろ向きに解く全称証明。w=3..12,m=2..16の150組でラベル付き723,780状態と独立な多重集合11,135状態を再帰mex照合し、不一致0。有限監査は証明の代替ではない。 t=2,q=4の分類は容量3の安全占有型（空・単独列・(1,b)・三単独列）を網羅し、各遷移とmexを全称的に場合分けした。w=2..12,m=2..20の209組でラベル付き144,001状態と独立な多重集合4,997状態を再帰mex照合し、不一致0。有限監査は証明の代替ではない。  t=2,q=6の全分類は、w=2の独立鎖・w=3またはm偶数の終局偶奇補題・w≥4かつm奇数の占有型mex帰納証明による。209組・36,860多重集合状態と56組・137,004ラベル状態の独立再帰監査で不一致0。有限監査は全称証明の代替ではない。 任意qの上界は、占有数2以上のファイバーを長さm−c_bの独立鎖へ分離し、空数e・単独石数ℓ・残容量Rの残余ゲームH_pへ帰着する全称証明。m偶数ではH_0=min(R,2e+ℓ) mod 2、m奇数ではH_1の相異なる子値が高々2個。q=7の正確な最大値はこの分解・終局偶奇・明示証人から全称証明。w=1..10,m=2..12の110組・3,809,674ラベル状態・18,117多重集合状態の二方式再帰mex監査は不一致0で、有限監査は証明の代替ではない。 t=3・q=4..6の分類は、鎖成分高々1個と1・2の成分列という安全型制限・終局特徴づけ・終局偶奇補題・純鎖補題による場合分けmex帰納証明。w=2..12,m=2..20の627組・18,354多重集合状態とw=2..8,m=2..9の168組・55,692ラベル状態の独立2方式再帰mex監査で不一致0。有限監査は全称証明の代替ではない。 t=3・q=7の全局面分類は、飽和ファイバーの鎖分離とXOR-mex補題による分解定理G=x⊕H(ρ)（x=1なら可動な奇数鎖が必ず存在する）、m奇数とm=2の固定残余手数閉形式、e_0≥Rでの飽和補題E(R,e_0,·)=E(R,R,·)、閉ボックス230状態でのmex固定点の機械的完全検査とRに関する普遍性帰納による全称証明。多重集合エンジンw=1..12,m=2..20の228組・26,334状態とラベル付きエンジンw=1..8,m=2..12の88組・179,740状態を独立再帰mexで照合し不一致0、値3計数2,490=15×166は先行最大値監査のヒストグラムと完全一致。有限監査は全称証明の代替ではない。 任意t上界は飽和ファイバーを残り長m−c_iの独立鎖へ分離し、未飽和占有レベル0..t−1の相異なる手型が高々tであることから残余mex H≤tを得る全称証明。m≡tでは残容量Rと未飽和残り増加数Lが全手で同時に1減り、残余プレイ長min(R,L)固定からH≤1。m<tでは全終局石数min(q−1,wm)固定。t=1..5,w=1..4,m=1..7,q=1..tw+2の1,330組・306,979ラベル状態・36,844正準状態を独立再帰mexで監査し不一致0。有限監査は無界証明の代替ではない。 t∈{2,3}全q最大値は、全安全局面でR−L=cap−twが一定というd不変量、レジームR≥L−1での閉形式H=(L−n) mod 2（系としてq≥twでは最大値1）、spawn到達不能ならH=R mod 2（系としてH≥2⇒cap≥t）、G=3が(1,2)経由ならcap≥2t、cap周期2tの明示witness族、およびt=3・p=1・cap≤6でのD≤6閉ボックス500状態mex固定点完全列挙＋e_0飽和補題によるH≤2の全称証明から決定される。V1..V6（10,734状態分解照合・516+213組最大値グリッド・269 witness・9,933状態sup H走査）とB1..B6（500状態固定点・q=7分類の64行普遍テーブルとの完全一致・44盤面組673状態）の独立再帰mex監査は不一致0。有限監査は全称証明の代替ではない。 全t全q最大値は、残余座標(R;X;z)への分解G=x⊕H（完了手はκ=(m−M) mod 2の鎖をspawnし、残余再帰からtとMが消える）、Theorem T（偶数Rでは値0と値1の選択肢が共通の合法な孫を持つことのケース分析により0と1を同時に含まない、奇数Rでは選択肢⊆{0,1}、強帰納で全t一挙にH≤2）、完了予算補題（D'=cap−t·s<tなら以後完了不可で残余プレイ長min(R,L)固定、H≤1、cap<tなら最大値1）、p=0の固定残余長H=min(R,L) mod 2、レジーム補題（R≥L−1でH=(L−n) mod 2、不変量R−L=cap−Mw、系としてq≥twでは最大値1）、x=1が飽和鎖の存在を要求することによるG=3⟹cap≥2t、およびH(1;X;z)=2のwitness状態と必要幅⌈(cap+2)/t⌉がq≤tw−1と丁度一致する陽明証人族による全称証明。t∈{2,3}先行定理の完全一般化であり、t≥4の普遍的G≤3はここで初めて証明された。V0..V6監査（5,679ラベル照合・200,255状態分解照合・2,448組最大値グリッド・48,048状態Theorem Tパリティ監査・113 witness・748点レジーム閉形式）は不一致0、二回の実行でbyte-identical。有限監査は全称証明の代替ではない。 単一未飽和ファイバー残余閉形式はR強帰納による全称証明で、2エンジン独立照合642,514点（V0/V1/V2）・閉形式のみのmex恒等式7,447,610点（V3/V3b）・cap補題51,975状態（V4）・構造一貫性479,460点（V5）の計8,706,159照合が不一致0、二回の実行でbyte-identical。有限監査は全称証明の代替ではない。 全1族の補題P（プレイ長）とtail系は全称証明（レジーム補題の系）。統一スライス閉形式への全称定理 h=U はR前進帰納（基底R=0・z=0ステップ・z≥1ステップ恒等式）を、評価4点の全分岐を15比較族（witness座標 s=R−k, s2=R−z で αs+βs2+γR≤t、|t|≤5）と合同剰余のアトム表に分解するシグネチャ決定性と、全実現シグネチャが |s|,|s2|≤48・R≤152 の到達可能点で実現される被覆補題によって3,803類の完全列挙に帰着させた機械支援全称証明による（C_box=C_wit=C_sat=3,803種・双方向包含0/0・ステップ恒等式318,930点・転写1,273,760照合・系A/B機械演繹1,681+7,686点を含む計約330万照合・二回実行byte-identical）。有限監査は全称証明の代替ではなく、全称性は帰納構造と類の完全列挙による。2位置閉形式・スライス閉形式は系A・系Bとして主定理から昇格された。 2トークン族の全z閉形式は未証明だが、z=0スライスの全Grundy値はR強帰納で閉形式証明された。z≥1の2位置予想は、素朴・ラベル付き・cap補題付き3エンジンの相互照合、全グリッド8,398状態・境界標的・ランダム1,494状態・系A（全1族k=2・z≤40）・高余裕帯・tailレジーム・Theorem Tとの整合を含む43,241照合（二回実行byte-identical）による有限監査のみで支持される。有限監査は全称証明の代替ではない。 天井トークン付き残余ゲームの値2分類予想（ラダー＋再帰位置族）は、cap付き正準多重集合エンジンとcapなし順序ラベルエンジンの相互照合、m≤7全グリッド・all-ones・遠方tail（マージン150）・高z（z≤40）・証明済み単一トークン閉形式・cap補題・Theorem Tパリティ・2/3トークン元ゲームブリッジを含む11,212照合の有限監査のみで支持される（二回実行byte-identical）。有限監査は全称証明の代替ではない。 3トークン過渡帯の値2位置予想（統一形・対角線OK表）は、cap付き正準多重集合エンジンとcapなし順序ラベルエンジンの相互照合、予想U（k=1,2,3全グリッド双方向）・予想A/B/C（陽性・陰性両面）・対角線OK表m=2..8の完全抽出グリッド双方向を含む36,958照合の有限監査のみで支持される（二回実行byte-identical）。有限監査は全称証明の代替ではない。 拡張監査（予想U k=4..8全グリッド35,764照合・m=9広域1,650＋高z族44・m=10の440＋165・偶数統一形m=6/8/10直接双方向2,520＋252＋440・エンジン相互照合300の計41,575照合・二回実行byte-identical）も同様に有限監査であり、全称性は未証明である。 外挿監査（m=11/13広域2,860＋4,550・m=12/14/16の728＋1,120＋408・m=15の840・高z族・修正統一形のm=6/8/10再監査3,212・all-ones族プロファイル25・エンジン相互照合120の計14,638照合・二回実行byte-identical）も同様に有限監査であり、全称性は未証明である。
- path: research/experiments/vertical-fiber-two-token-z3-slice-20261116/report.md
  role: proof
  note: 2トークン族z=3全Grundy閉形式の強帰納証明と奇数・偶数選択肢表
- path: research/experiments/vertical-fiber-two-token-z3-slice-20261116/verify_z3_slice.py
  role: verifier
  note: cap付き多重集合再帰・capなしラベル再帰・帰納選択肢表の独立照合器
- path: research/experiments/vertical-fiber-two-token-z3-slice-20261116/output/audit.json
  role: data
  note: 6,300状態・選択肢表6,090点・tail等の有限監査結果、二回実行byte-identical
- path: research/log/2026-11-16-vertical-fiber-two-token-z3-slice.md
  role: log
  note: 最新main・既存未解決事項との照合、z=3全称証明・有限監査・限界の判断記録

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

## 単一未飽和ファイバーの残余閉形式（κ=1）

全t最大値定理の残余mex H(R;X;z) について、未飽和ファイバーが1本（Xが単一トークン）の場合の値を全パラメータで閉形式決定する。残余再帰の定義（A手 x→x−1、B手 トークン1除去でz+1、C手 z→z−1でXOR 1、H(0)=0）は上記定理の分解に従う。

**補題（空ファイバー）** H(R;();z)=0（全R,z）。帰納: 唯一の手Cは 1⊕0=1 を与え、mex{1}=0、手なければ mex∅=0。

**補題（cap）** cap_c(X)で各トークンをmin(x,c)に置換すると H(R;X;z)=H(R;cap_{R+1}(X);z)。R帰納: A手の子のトークンx−1はレベルR−1でcap係数RよりRへ正規化でき、cap前後で子の値集合が一致する。従って各固定Rの残余状態空間は「トークン数≤R・トークン値≤R+1・z≤R」で有限。

**定理（単一トークン閉形式）** x≥1, z≥0, R≥0, L=x+z+1, q(k)=k以下最大の奇数として v(x,z,R)=H(R;(x);z) は:

| 条件 | v |
|---|---|
| z=0 | min(R,x) mod 2 |
| z=x≥1: R奇数∧R≤2x−1 | 2 |
| z=x≥1: R偶数∧R≤x−1 | 0 |
| z=x≥1: その他 | x mod 2 |
| 1≤z≤x−1: R奇数∧R≤m=q(z) | 2 |
| 1≤z≤x−1: R偶数∧R≤m | 0 |
| 1≤z≤x−1: m<R<L−1 | (R+z) mod 2 |
| 1≤z≤x−1: R≥L−1 | x mod 2 |
| z≥x+1: R奇数∧R≤m=q(x) | 2 |
| z≥x+1: R偶数∧R≤m | 0 |
| z≥x+1: R>m | x mod 2 |

**系（H=2の特徴づけ・単一トークン）** H(R;(x);z)=2 ⟺ Rが奇数 ∧ R≤μ(x,z)、μ(x,z)=2x−1 (z=x) / min(x,z)以下の最大奇数 (z≠x)。z=0では値2は不成立。値2はz=xのときR=2x−1まで最も深く現れる。レジーム R≥L−1 では v=x mod 2 で全t定理のレジーム閉形式（L−n=x, n=1+z）と一致し、偶数Rでは常に v≤1・奇数Rでは v≤2 はTheorem Tと整合する。witness条件 H(1;(x);z)=2 は z≥x+1 または z=x で常に成立する。

証明はRに関する強帰納（4ケース×帯ごとの子の値の場合分け）。全証明と補題の証明は[証明報告](../../experiments/vertical-fiber-single-token-residual-closed-form-20261116/report.md)に、有限監査は[検証器](../../experiments/vertical-fiber-single-token-residual-closed-form-20261116/verify_single_token.py)による: 2エンジン独立実装照合2,730点・全グリッド639,584点・ランダム200点・閉形式mex恒等式151,290+7,296,320点・cap補題51,975状態・構造一貫性479,460点、計8,706,159照合で不一致0、二回の実行でbyte-identical（[監査結果](../../experiments/vertical-fiber-single-token-residual-closed-form-20261116/output/audit.json)）。有限監査は全称証明の代替ではなく、全称性は帰納証明による。旧U座標remarkは誤りであり、次の訂正を参照。

**全1族への拡張（全称証明済み）** 上の有限観察（z=2j, k≥2j+1 の部分族）は、全 \((k,z)\) に対する値2位置集合の完全閉形式に拡張され、次節の主定理 h=U により全称証明された（元の k,z≤50 全2,601状態＋ランダム300点の機械検証に加え、主定理から系Aとして機械演繹・1,681状態照合済み）。

一般多重集合Xへの拡張（2トークン閉形式・cap補題ベースの固定R有限状態DP・一般のH=2特徴づけ）は未解決の残課題である。標準二次元幾何ゲームの勝敗は主張しない。

**訂正（2026-11-16・U座標）** 旧単一トークン報告の「mexは一様XORと可換なので、\(U=H\oplus(z\bmod2)\) ではC手の反転が消えB手へ移る」というremarkは誤りである。mexは一様XORと可換ではない。最小反例は \((R,X,z)=(1,(1),1)\): 元の選択肢は \(\{0,1\}\) なので \(H=2\)、従って \(U=3\)。旧変換再帰は選択肢 \(\{1,0\}\) のmexを2とする。正しい代入式と独立監査は[訂正報告](../../experiments/vertical-fiber-u-coordinate-erratum-20261116/report.md)、[検証器](../../experiments/vertical-fiber-u-coordinate-erratum-20261116/verify_u_coordinate.py)、[監査結果](../../experiments/vertical-fiber-u-coordinate-erratum-20261116/output/audit.json)に記録した。単一トークン閉形式の強帰納証明・cap補題・全1族の直接H再帰による有限監査はこのremarkに依存しないため、変更しない。

## 全1トークン族の残余mexの全称決定（κ=1・h=U）

残余ゲームで \(X=(1^k)\)（全トークンが1）とするとA手が消え、状態は \((k,z,R)\) に坍縮する:
\[
h(k,z,R)=\operatorname{mex}\{\,h(k-1,z+1,R-1)\ [k\ge1],\ \ 1\oplus h(k,z-1,R-1)\ [z\ge1]\,\},\qquad h(\cdot,\cdot,0)=0 .
\]
これは最初の本格的な複数トークン族の完全解析である（単一トークン閉形式の直後・全t定理の残課題「\(H=2\) の特徴づけ」の多トークン候補）。

**補題P（プレイ長・証明済み）** 一般残余ゲームで \(L=\sum X+|X|+z\) はA/B/Cいずれの手でもちょうど1減り、\(L\ge1\) なら合法手が常に存在する。従ってプレイ長は手順によらず \(\min(R,L)\)。全1族では \(L=2k+z\)。

**系（tail・証明済み）** 全t定理のレジーム補題（κ=1）より
\[
R\ \ge\ 2k+z-1\quad\Longrightarrow\quad h(k,z,R)=k\bmod2 .
\]

**主定理（h=U・機械支援全称証明）** \(U(k,z,R)\) を統一スライス閉形式（\(z\ge1\)、場合分けは \((z\bmod2,k\bmod2)\) の4通り・前報W6と証明報告付録に全文）、\(U_0(k,R)=\)（\(k\ge1\wedge R\ge1\) なら \([U(k-1,1,R-1)=0]\)、他は0）とすると、
\[
\forall k,z\ge0,\ \forall R\ge0:\quad h(k,z,R)=\begin{cases}U(k,z,R)&z\ge1\\ U_0(k,R)&z=0.\end{cases}
\]
証明は \(R\) 前進帰納。(i) 基底 \(R=0\) は \(h=U=U_0=0\)。(ii) \(z=0\) ステップは \(\operatorname{mex}\{v\}=[v=0]\) で自明。(iii) \(z\ge1\) ステップでは、評価4点（親 \((k,z,R)\)・B手子 \((k-1,z+1,R-1)\)・C手子 \((k,z-1,R-1)\)・\(U_0\) 内側 \(G=(k-1,1,R-1)\)）における \(U\)・\(U_0\)・引数ガードの全分岐を、witness座標 \(s=R-k,\ s_2=R-z\) の15比較族 \(\alpha s+\beta s_2+\gamma R\le t\)（\(|t|\le5\)）と \((s,s_2,R)\bmod4\) の合同剰余のアトム表に分解し、シグネチャ（比較ビット列＋剰余）が4点の値を完全に決める（シグネチャ決定性・転写 \(U_{\mathrm{tab}}\) と published \(U\) の二重経路で1,273,760照合・アトム等価1,520,000照合）。被覆補題により全実現シグネチャは \(|s|,|s_2|\le48,\ R\le152\) の到達可能点で実現され、実現集合はちょうど3,803種でボックス掃引・witness掃引・大規模掃引の三尺度が完全に一致する（\(C_{\mathrm{box}}=C_{\mathrm{wit}}=C_{\mathrm{sat}}\)・双方向包含0/0）。全3,803類でステップ恒等式 \(\operatorname{mex}\{U(k-1,z+1,R-1)\ [k\ge1],\ 1\oplus\tilde U\ [z\ge1]\}=U(k,z,R)\)（\(\tilde U\) は \(z\ge2\) で \(U(k,z-1,R-1)\)、\(z=1\) で \(U_0(k,R-1)\)）を published/転写の二重経路で検証（318,930点・0不一致）し、帰納が閉じる。全証明は[証明報告](../../experiments/vertical-fiber-all-ones-induction-proof-20261116/report.md)、[研究ログ](../../log/2026-11-16-vertical-fiber-all-ones-induction-proof.md)参照。前報W7のシグネチャ圧縮検証（2,158種・飽和グリッド5種）は本証明の独立の先駆であり、3,803類のcell分解がその形式ギャップを閉じた。

**系A（2位置閉形式・主定理の系・証明済み）** \(q(n)=n\) 以下最大奇数として、\(h(k,z,R)=2\) となる \(R\) の集合 \(T(k,z)\) は
\[
z=0:\ \varnothing,\qquad
z\text{ 奇}:\ \{1,3,\dots,q(k)\},\qquad
z\ge2\text{ 偶}:\ \{1,3,\dots,q(\min(k,z))\}\cup\begin{cases}\{2k-z+1\}&2k-z+1\ge1\\ \varnothing&\text{else}\end{cases}
\]
で完全に決まる。主定理への代入で機械演繹され（E6・\(k,z\le40\) 全1,681状態・0不一致）、独立の有限監査（\(k,z\le50\) 全2,601状態（窓 \(R<2k+z+2\)、tail系と併せ全領域被覆）＋\(k,z\le80\) ランダム300点）でも不一致0。全要素は奇数でTheorem T（1）と整合し、単一トークン報告の \(z=2j,\ k\ge2j+1\) 有限観察は \(z\) 偶ケースの部分族に一致する。

**訂正注（2026-11-16）** [単一トークン報告](../../experiments/vertical-fiber-single-token-residual-closed-form-20261116/report.md)の全1族観察と11×11接続メモにある例「\((k,z)=(4,6)\) で \(H=2\) の位置が \(R=1,3,5,7\)」は誤りである。正しくは \(R=1,3\) のみ。\(R=0,\ldots,12\) を縮約再帰と一般多重集合再帰の独立2方式で完全計算し、\(R\ge13=2k+z-1\) は証明済みtail補題から値0となる。記載された4点集合は \((k,z)=(6,6)\) では再現する。旧実験報告は履歴資料として変更せず、[訂正監査](../../experiments/vertical-fiber-all-ones-example-erratum-20261116/report.md)に正誤と再現手順を記録した。この訂正は当時の予想Aの証明ではなく、その後の主定理により予想A自体は系Aとして証明された。

**系B（スライス閉形式 z=1,2・主定理の系・証明済み）** \(z\in\{1,2\}\) では全プロファイルが閉形式で書ける（\(k=0\) は全0）。\(z=1,k\) 奇: 2（奇 \(R\le k\)）・0（\(R\equiv0\pmod4,\ R\le2k-2\)）・他1。\(z=1,k\) 偶: 2（奇 \(R\le k-1\)）・1（\(R\equiv2\pmod4,\ 2\le R\le2k-2\)）・他0。\(z=2,k\) 奇: 2（\(R=1,2k-1\)）・0（偶 \(R\le k-1\) または \(R\equiv1\pmod4,\ 5\le R\le2k-5\)）・他1。\(z=2,k\) 偶: 2（\(R=1,2k-1\)）・1（\(R\equiv3\pmod4,\ 3\le R\le2k-5\)）・他0。中間遷移領域は周期4の等差波（AP4）で構成され、この0/1波構造の一般 \(z\) への係数化は統一スライス閉形式 \(U\)（場合分けは \((z\bmod2,k\bmod2)\) の4通り）として完了し、主定理により全称証明された（E7・7,686点の機械演繹照合を含む）。安定化閾値 \(R^*(k,z)\) の実測規則性（\(z\) 偶 \(k\ge z\) で \(2k-z+2\) 等）も[報告](../../experiments/vertical-fiber-all-ones-residual-structure-20261116/report.md)にデータとして記録した（未証明）。

有限監査は[検証器](../../experiments/vertical-fiber-all-ones-residual-structure-20261116/verify_all_ones.py)による: W0 坍縮エンジンと一般多重集合エンジンの照合8,463点・W1 2,601状態・W2 ランダム300点・W3 スライス7,686点・W4 tail 15,554点・W5 プレイ長400プレイ、計35,004照合で不一致0、二回の実行でbyte-identical（[監査結果](../../experiments/vertical-fiber-all-ones-residual-structure-20261116/output/audit.json)）。さらに主定理の帰納監査は[検証器](../../experiments/vertical-fiber-all-ones-induction-proof-20261116/verify_induction_proof.py)による: 基底4,225状態・転写1,273,760照合・アトム等価1,520,000照合・ステップ恒等式318,930点・被覆3,803種（三尺度一致・双方向包含0/0）・エンジン交叉2,925+104,140+7,381点・ランダム400点・系A/B機械演繹1,681+7,686点、計約330万照合で不一致0、二回の実行でbyte-identical（[監査結果](../../experiments/vertical-fiber-all-ones-induction-proof-20261116/output/audit.json)）。検証器SHA-256: ba2896c6497d2d1bc0146dfc918c5d6fbb63dc878af7f0d04a1c409421342504、監査JSON SHA-256: 2585e9f56946e37c6ca889fa5b2b755f05124688754f5a57e83b732280650b85。有限監査は全称証明の代替ではなく、全称性は帰納構造と3,803類の完全列挙による。補題P・tail系・主定理 h=U・系A・系Bが証明済みであり、安定化閾値 \(R^*(k,z)\) の閉形式はデータ規則性として未証明のまま、一般多重集合 \(X\) への拡張（2トークン閉形式・一般のH=2特徴づけ）とともに残課題である。標準二次元幾何ゲームの勝敗は主張しない。


## 残余ゲームの高さ条件だけによる単一トークン縮約（κ=1・全称証明）

\(S=\sum_{x\in X}x\)、\(v(s,z,r)=H(r;(s);z)\)、\(v(0,z,r)=0\) とする。

**定理（高さだけによる縮約）**
\[
\boxed{R\le z+1\quad\Longrightarrow\quad H(R;X;z)=v(S,z,R).}
\]
すなわち \(z\ge R-1\) なら、任意の有限正整数多重集合 \(X\) は総和 \(S\) の単一トークンへ厳密に縮約される。さらに \(R\le2\) では \(z\) に条件を付けず成立する。

**補題（単一トークンの高さ安定性）**
\[
z\ge r\quad\Longrightarrow\quad v(s,z,r)=v(s,z+1,r).
\]
単一トークン閉形式の各枝を比較すればよい。\(z\ge s+1\) では両方とも安定枝、\(z=s\) では特別枝と安定枝が一致する。\(1\le z\le s-2\) では、奇数 \(r\) は両側2、偶数 \(r<z\) は両側0、残る \(r=z\)（偶数）も中間式 \((r+z)\bmod2=0\) と次の閾値枝が一致する。境界 \(z=s-1\) も同じ偶奇比較で一致する。\(r=0\) または \(s=0\) は自明。

**証明。** \(R\) に関する強帰納。\(R=0\) は定義。\(R=1\) は、\(X\ne\varnothing\) ならA/B子の値0があり、\(z\ge1\) のときだけC子の値1が加わるため、分割によらない。\(R=2\) は \(S\ge2\) のとき、\(z=0\) でA/B子値が1または2、\(z=1\) でA/B子値2とC子値0、\(z\ge2\) でA/B子値2とC子値3となり、単一トークン側と同じmex。\(S\le1\) は同一状態または空状態である。

\(R\ge3,\ z\ge R-1\) とする。A/B/Cの各子は残容量 \(R-1\) で、それぞれの高さ \(z,z+1,z-1\) は帰納条件 \(z'\ge R-2\) を満たす。帰納法によりA子は \(v(S-1,z,R-1)\)、B子は \(v(S-1,z+1,R-1)\)、C子は \(1\oplus v(S,z-1,R-1)\)。単一トークン高さ安定性を \(r=R-1\) に適用するとA/B子値は一致する。\(S\ge2\) なら一般側にはA/B手が少なくとも一つあり、その共通子値は単一トークン \((S)\) の唯一のA手の子値と同じ。C手も両側で一致するので選択肢値集合、従ってmexが一致する。\(S=1\) は \(X=(1)\)、\(S=0\) は空多重集合補題。∎

**一様条件の鋭さ。** \(R\ge3\) で \(z\ge R-1\) は全 \(X\) に一様な条件として鋭い。奇数 \(R\) では \(X=(1^R),z=R-2\) とすると、全1族の証明済み公式で一般値は2、総和 \(R\) の単一トークン値は0。偶数 \(R\ge4\) では \(X=(1^{R-1}),z=R-2\) とすると、全1族の公式で一般値は1、総和 \(R-1\) の単一トークン値は0。従って \(z=R-2\) まで一様に条件を弱めることはできない。これは各 \(X\) に必要条件を課す主張ではない。

**既知tailとの接続。** 既存の
\[
R\ge S+|X|+z-1\implies H(R;X;z)=S\bmod2
\]
と合わせると、\(X\ne\varnothing\) を固定したとき一般多重集合として追加解析が必要な残容量は
\[
\boxed{z+2\le R\le S+|X|+z-2}
\]
だけである。幅は \(S+|X|-3\) で \(z\) に依存しない。2トークン族では幅 \(S-1\)。従来の \(z\ge S+R-1\) より低R側を大きく広げる結果である。

証明・独立監査: [実験報告](../../experiments/vertical-fiber-height-only-collapse-20261116/report.md)、[検証器](../../experiments/vertical-fiber-height-only-collapse-20261116/verify_height_only_merge.py)、[監査結果](../../experiments/vertical-fiber-height-only-collapse-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-vertical-fiber-height-only-collapse.md)。検証器は高さ安定性8,364件、全列挙4,788件、R≤2全zの有限窓3,780件、固定seed散点160件、鋭さ証人38件を独立照合し、不一致0・二回実行byte-identical。全称性は上記帰納証明と既証明の全1族閉形式による。


## 2トークン族の残余2位置集合の閉形式予想（κ=1・z≥4は未証明）

**証明済みスライス:** \(z=0,1,2\) の全Grundy値は各高さスライスで全称証明済み。以下の3族予想で未証明として残るのは \(z\ge3\) の場合である。

2トークン族 \(X=(x,y)\)（\(x\ge y\ge1\)）について \(S=x+y\)、\(d=x-y\)、\(\delta=R-2y\)、\(q_o(k)\)=k以下最大奇数、\(\mathrm{smin}(d)\)=\(d+1\)以上の最小奇数、\(\delta_A(z)\)=\(z\)以上の最小奇数、\(y^*=(z-d)/2\) と置く。2位置集合 \(T(x,y,z)=\{R: H(R;(x,y);z)=2\}\) が次の3族で記述できることが予想される（有限監査による支持のみ・全称性は未証明）:

- **ラダー**: 奇数 \(R\le q_o(\min(S,z))\)。単一トークン閉形式と同じμ型。
- **家族B**（\(d\equiv z \pmod 2\)、\(d\le z\)）: **PT角**は \(y=y^*\ge1\) のとき \(\{2y+\delta: \delta\in I(z,d)\}\)、\(I(z,d)=\{\)奇数\(\delta: \mathrm{smin}(d)\le\delta\le 2\lceil(z+d)/4\rceil-1\}\)。**EXT**は \(z+d\equiv2\pmod4\) かつ \(y\ge y^*\) のとき \(2y+(z+d)/2\)（\(y\ge y^*\) の全行で出現。\(y^*=0\)、すなわち \(d=z\)・z奇の対角線特殊点 \(R=2y+z\) を統一的に含意する。z偶の \(d=z\) は \(z+d\equiv0\pmod4\) で自然に空）。
- **家族A**（\(y\) に非依存）: **ラン**は \(d=z+1\) のとき \(\{2y+\delta:\ \delta_A(z)\le\)奇数\(\delta\le 2z+1\}\)。**定常**は \(d\ge z+2\) のとき \(2y+\delta_A(z)\)（単一位置）。

証明済みレジームとの整合: 高余裕帯 \(z\ge S+R-1\) では家族Aは不活性化し家族Bの全要素は帯外に落ちるため、予想は証明済みの単一トークン縮約公式（奇数\(R\le q_o(S)\)）に正確に帰着する。予想の全位置は証明済みtail境界 \(R\ge S+z+1\) を侵食しない。\(x=y=1\) は全1族 \(k=2\) に一致し、証明済み系A（\(z\le40\) 全スライス）を回収する。監査は素朴・ラベル付き・cap補題付きの3エンジン相互照合、全グリッド8,398状態・境界標的・ランダム1,494状態を含む43,241照合・不一致0・二回実行byte-identical。抽出・定義・監査の詳細は[独立実験報告](../../experiments/vertical-fiber-two-token-residual-2positions-20261116/report.md)を参照。全称証明（R前進帰納＋シグネチャ法）は未解決課題。

## 2トークン族の高さ \(z=0\) スライス（全Grundy値の全称閉形式）

\(h_{x,y}(R)=H(R;(x,y);0)\)、\(S=x+y\)、\(x\ge y\ge1\) とする。任意の \(R\ge0\) について

\[
\boxed{
h_{x,y}(R)=
\begin{cases}
R\bmod2 & 0\le R\le2y,\\
2 & x>y,\ R=2y+1,\\
1-(R\bmod2) & x>y,\ 2y+2\le R\le S,\\
S\bmod2 & R\ge S+1.
\end{cases}}
\]

従って
\[
H(R;(x,y);0)=2\iff x>y\text{ かつ }R=2y+1.
\]

**証明。** \(R\) に関する強帰納。\(x=y\ge2\) では二つのA手が同じ子 \((x,x-1,R-1)\) へ行き、子の値が順に \((R-1)\bmod2\)、特別点の2、tailの1となる3帯を分ければ式が得られる。\(x=y=1\) はB子 \(v(1,1,R-1)\) の単一トークン閉形式から従う。\(y=1<x\) では
\[
h_{x,1}(R)=\operatorname{mex}\{h_{x-1,1}(R-1),v(x,1,R-1)\}
\]
を用い、\(R=1,2,3,4\) と \(R\ge5\) に分ける。\(x>y\ge2\) では二つのA子 \((x-1,y)\), \((x,y-1)\) の値を \(R\le2y-1\)、\(R=2y\)、\(R=2y+1\)、\(R=2y+2\)、\(R\ge2y+3\) に分けて比較する。全場合でmexが表示式と一致する。完全な場合分けは[証明報告](../../experiments/vertical-fiber-two-token-z0-slice-20261116/report.md)に記録した。∎

[独立検証器](../../experiments/vertical-fiber-two-token-z0-slice-20261116/verify_z0_slice.py)は、cap付き正準多重集合再帰とcapなし順序付きラベル再帰の2方式で、\(x\le60\)、全 \(y\le x\)、\(0\le R\le x+y+4\) の120,780状態を照合し、不一致0・二回実行byte-identicalを確認した（[監査JSON](../../experiments/vertical-fiber-two-token-z0-slice-20261116/output/audit.json)）。有限監査は全称証明の代替ではなく、全称性は上記の強帰納による。

この定理は2トークン予想の家族Aの \(z=0\) 場合を証明し、同時にそのスライスの値0/1も決定する。\(z\ge1\) を一括する2トークン閉形式と一般多重集合の \(H=2\) 必要十分条件は引き続き未解決である。

## 天井トークン付き残余ゲームの値2位置分類（全 \(m\) 予想・ラダーは系）

cap補題により値 \(R+1\) 以上のトークンはすべて \(R+1\) に置換可能であり、各レベルで常に1個の「天井」として振る舞う。そこで天井トークン付き残余ゲームを
\[
T_{\infty}(X;z):=\{R\ge1:\ H(R;\,X\cup\{R+1\};\,z)=2\}
\]
と定義する（\(X\) は正整数の有限多重集合、\(m=|X|\)、昇順 \(t_0\le t_1\le\dots\le t_{m-1}\)）。これは元ゲームの「最大トークンがcapされる」対角線スライスであり、2トークン家族Aの定常位置と3トークン安定コアの一般化である。

**系（ラダー・証明済み定理から導出）。** \(R\le z+1\) では高さのみの縮約とcap補題により \(H(R;X\cup\{R+1\};z)=H(R;(R+1);z)\) であり、証明済み単一トークン閉形式（値2 \(\iff\) 奇数 \(R\le\mu(a,z)\)、\(a=R+1\)）から
\[
T_{\infty}(X;z)\cap[1,z+1]=\{\text{奇数 } R\le z+1\}\setminus\{z+1\}.
\]
\(m\) に依らず全称に成立する。

**予想（再帰位置族・有限監査のみで支持）。** \(\delta_A(u)=u\) 以上の最小奇数として
\[
p_0=2t_0+\delta_A(z),\quad p_1=2t_1+\delta_A(z+1),\quad p_j=2t_j+p_{j-2}+2\ (j\ge2)
\]
（同値な閉形式 \(p_j=2(t_j+t_{j-2}+t_{j-4}+\cdots)+\delta_A(z+j)\)）と置くと、任意の \(m\ge0\)、任意の \(X\)、任意の \(z\ge0\) について
\[
T_{\infty}(X;z)=\{\text{奇数 } R\le z+1\}\setminus\{z+1\}\ \cup\ \{p_j:0\le j<m\}.
\]
\(m=0\) では位置族は空でラダーのみ（上の系）。位置はすべて奇数で \(R\ge z+2\)（Theorem T と整合・ラダーと重複なし）。\(m=1\) の位置 \(2y+\delta_A(z)\) は2トークン家族Aの定常位置そのものであり、証明済みの \(z=0\) スライス（\(x>y\) かつ \(R=2y+1\) のみ値2）と \(z=0\) で完全に一致する。天井ゲームでは \(R\ge z+2\) の限り高余裕縮約が発動しないため（\(S\) が \(R+1\) を含み \(R\) とともに増える）、tail定理でも上側が閉じないが、遠方tail監査（マージン150）・高z監査（\(z\le40\)）でも予想位置外の値2位置は現れない。

**ブリッジ（予想の系）。** cap補題から \(H(R;X;z)=H(R;X_{\le R}\cup\{R+1\};z)\)（\(X_{\le R}\) は \(X\) の \(R\) 以下のトークン）。従って2トークン \((x,y)\)・3トークン \((x,y,w)\) の元ゲームで \(R\in[\max(z+2,y),\,x-1]\) の帯の値2位置はそれぞれ \(2y+\delta_A(z)\)、\(\{2w+\delta_A(z),\,2y+\delta_A(z+1)\}\) と一致する。この帯に家族B型の過渡位置は現れないことが同じ監査で確認された。

独立監査: [実験報告](../../experiments/vertical-fiber-ceiling-stable-2positions-20261116/report.md)、[検証器](../../experiments/vertical-fiber-ceiling-stable-2positions-20261116/verify_ceiling.py)、[監査結果](../../experiments/vertical-fiber-ceiling-stable-2positions-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-vertical-fiber-ceiling-stable-2positions.md)。検証器はcap付き正準多重集合エンジンとcapなし順序ラベルエンジンを相互照合し、\(m\le7\) 全グリッド・all-ones・遠方tail・高z・証明済み単一トークン閉形式・cap補題・Theorem Tパリティ・2/3トークン元ゲームブリッジを含む11,212照合で不一致0・二回実行byte-identical。位置族部分の全称証明（R前進帰納・天井A手の自己参照構造と偶奇インデックス2列分解が手がかり）は未解決課題。

## 3トークン過渡帯の値2位置（κ=1・対角線と c≤−(2k+1) スライス・予想）

残余ゲーム H(R;X;z)（κ=1）の3トークン族 X=(x,y,w)（x≥y≥w≥1）について、過渡帯 x<R<S+z+2（R>z+1 を含む）の中で R−2x が奇数となるスライス R=2x−(2k+1)（k≥0）上の値2位置を、j:=x−(y+w+z)（≥0）の座標で分類する。

**予想U（k≥1・有限監査のみで支持）。** 帯条件内で
H(R;(x,y,w);z)=2 ⟺ (j=0∧w=1: z≥2k) または (それ以外: 2(k+1−j−w)≤z≤2(k+1−j−w)+1)。下端が負なら区間は空（不成立）。y に依存しない。k=1,2,3 の全グリッド（20,052ケース）で予想の陽性・陰性両面が完全一致した。

**予想A/B/C（k=0・R=2x−1・有限監査のみで支持）。** A: j=0（x=y+w+z）なら帯内で常に値2。B: j=2（x=y+w+z+2）なら帯内で常に値2。C: j=1 は z=0 のみ値2で z≥1 では帯内で全て値2でない。j≥3 は帯条件 R<S+z+2 を満たす位置が存在しない。k=0 は統一形Uの外の特異ケースであり、k=0 では R+1=2x がちょうど最大トークンの2倍で cap_{R+1}(X)=X になるのに対し k≥1 では R+1=2x−2k<x で最大トークンが cap される構造差に対応すると考えられる（未証明の説明候補）。

**対角線OK表（2x_max=S+z、R=2x_max−1、m=|X|・抽出範囲内の有限観察）。** X=(x_max,)∪rest、x_max=sum(rest)+z、rest は昇順と置く。H(R;X;z)=2 の必要十分条件は
- m=2: z=1
- m=3: 常に成立（rest 任意）
- m=4: (z=0 ∧ (rest[:2]≠(1,1) ∨ rest=(1,1,1))) ∨ (z=1 ∧ rest[:2]=(1,1))
- m=5: rest[:3]=(1,1,1)（z 任意）
- m=6: (z=1 ∧ rest[:4]=(1,1,1,1)) ∨ (z=0 ∧ rest[:2]=(1,1) ∧ ((rest[:3]=(1,1,1)∧rest[3]=2) ∨ (rest[2]=2∧rest[3]=2)))
- m=7: rest[:5]=(1,1,1,1,1)（z 任意）
- m=8: (rest=(1⁷)∧z∈{0,1}) ∨ (z=1∧rest[:6]=(1⁶)) ∨ (z=0∧((rest[:5]=(1⁵)∧rest[5]=2)∨(rest[:4]=(1⁴)∧rest[4]=2∧rest[5]=2)))

である。m奇数では「rest の先頭 m−2 個がすべて1」の族が全 z でOKし、m偶数では z∈{0,1} の2層構造が現れる（m=4 の z=0 層のみ例外形）。抽出トークン上限は m≤5 で7、m=6 で6、m=7 で4、m=8 で3であり、表はこの範囲の完全抽出である（全称主張ではない）。m=5 でOKが rest=(a,1,1,1) 族に限ることが確定したため、「m奇数なら対角線OKが常に成立する」という初期観察（m=1,3 で支持）は反例となった。m=3 の「常にOK」は天井予想の位置族 p_0<p_1 より上の帯に現れる新しい全OK現象で、capブリッジ帯 [max(z+2,y), x−1] の外側に位置する。

独立監査: [実験報告](../../experiments/vertical-fiber-three-token-transient-band-20261116/report.md)、[検証器](../../experiments/vertical-fiber-three-token-transient-band-20261116/verify_transient.py)、[監査結果](../../experiments/vertical-fiber-three-token-transient-band-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-vertical-fiber-three-token-transient-band.md)。検証器はcap付き正準多重集合エンジンとcapなし順序ラベルエンジンを相互照合し、予想U（k=1,2,3・全グリッド双方向）・予想A/B/C（陽性・陰性両面）・対角線OK表m=2..8（完全抽出グリッド双方向）・エンジン相互照合・正規化エッジを含む36,958照合で不一致0・二回実行byte-identical。有限監査は全称証明の代替ではない。全称証明（R前進帰納・スライス族F_{k,j}の連立漸化式・全1族の機械支援帰納と同じ方法論）は未解決課題。

**拡張（第2報・有限監査のみで支持）。** 予想Uはk=4..8の全グリッド（35,764ケース）でも反例がなく、スライス範囲はk=1..8まで支持された。対角線OK条件はm=9（OK ⟺ rest[:7]=(1⁷)・z任意。tmax=4・zmax=9の広域1,650ケース双方向・族の高z（z≤20）も全てOK）とm=10（z=1: rest[:8]=(1⁸)、z=0: (rest[:7]=(1⁷)∧rest[7]=2)∨(rest[:6]=(1⁶)∧rest[6]=2∧rest[7]=2)、z≥2: なし。tmax=4の440＋165ケース）まで確定された。これにより奇数族予想「m≥5奇数のOK ⟺ rest[:m−2]=(1^{m−2})（z任意）」がm=5,7,9の3点で、また偶数の統一形予想「m=2r≥6: z=1ならOK ⟺ rest[:2r−2]=(1^{2r−2})、z=0ならOK ⟺ (rest[:2r−3]=(1^{2r−3})∧rest[2r−3]=2)∨(rest[:2r−4]=(1^{2r−4})∧rest[2r−4]=2∧rest[2r−3]=2)、z≥2はOKなし。ただしm=8のみさらにrest=(1⁷)もOK」がm=6,8,10で支持された。統一形はm=6（2,520ケース）・m=8（252ケース）・m=10（440ケース）でHと直接双方向照合されており、m=6/8では前報OK表と同値になる。m=8のz=0全1特例はm=6・m=10には現れない観察として残る。m=4の例外形は統一形の外（m≥6が対象）。独立監査: [拡張実験報告](../../experiments/vertical-fiber-transient-band-extension-20261116/report.md)、[検証器](../../experiments/vertical-fiber-transient-band-extension-20261116/verify_extension.py)、[監査結果](../../experiments/vertical-fiber-transient-band-extension-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-transient-band-extension.md)（41,575照合・不一致0・二回実行byte-identical）。

**拡張（第3報・有限監査のみで支持）。** 対角線OK条件はm=11（tmax=4・zmax=9の広域2,860照合・高z族44＋族外22。OK ⟺ rest[:9]=(1⁹)・z任意）、m=13（4,550＋66。OK ⟺ rest[:11]=(1¹¹)）、m=15（tmax=3・z≤6の840＋高z70。OK ⟺ rest[:13]=(1¹³)）まで外挿され、奇数族予想の支持点はm=5,7,9,11,13,15の6点になった。偶数では、旧統一形の「m=8のみrest=(1⁷)特例」は孤立ではなく、all-ones特例はm≡0 (mod 4)でちょうど現れることが確定した: m=12（z=0,1・tmax=4の728照合）とm=16（tmax=3・z=0..2の408照合）ではrest=(1^{m−1})・z=0がOKで、m=6（2,520）・m=10（440）・m=14（1,120＋z≥2不在315）では不在。修正統一形は「z=1: OK ⟺ rest[:2r−2]=(1^{2r−2})、z=0: OK ⟺ c1∨c2∨[m≡0 (mod 4) かつ rest=(1^{m−1})]、z≥2: なし」（c1: 接頭辞長2r−3で2、c2: 接頭辞長2r−4で2が2個）であり、D8でm=6,8,10を再監査して旧統一形（m==8ハードコード）と結果不変で一致する。さらにall-ones対角線はrest=(1^{m−1})・z=0のときX=(k,1^k)・R=2k−1（k=m−1）と単一パラメータ化でき、スタンドアロン族プロファイル予想「H(2k−1;(k,1^k);0)はk≡1 (mod 4)で1、それ以外で2（値2 ⟺ k≢1 mod 4）。k=1..25・値1/2の全プロファイル」が提案された。この族は奇数族のall-ones陽性（k偶・k%4∈{0,2}でh=2）と偶数のmod 4特例の有無（k奇・k%4=3でh=2、k%4=1でh=1）を単一の周期4則に統一し、m=4対角線OK表z=0層のall-ones語rest=(1,1,1)（k=3）も合流する。周期4が全1族UのAP4波（系B）と整合する点は説明候補だが厳密な導出は未解決。m=16の走査中にc2形状(1^12,2,2,2)を一時族外陰性と誤ラベルした偽陽性騒動は予想の誤読であり検証器では修正済み。独立監査: [外挿実験報告](../../experiments/vertical-fiber-diagonal-m11-m16-20261116/report.md)、[検証器](../../experiments/vertical-fiber-diagonal-m11-m16-20261116/verify_diag_m11_m16.py)、[監査結果](../../experiments/vertical-fiber-diagonal-m11-m16-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-diagonal-m11-m16.md)（14,638照合・不一致0・二回実行byte-identical）。予想O（奇数族）・E'（修正統一形）・F（all-ones族プロファイル）の全称証明は未解決課題（予想Fが帰納構造上最も単純な候補）。



## 2トークン族の高さ \(z=1\) スライス（全Grundy値の全称閉形式）

\(S=x+y\)、\(d=x-y\)、\(x\ge y\ge1\) とする。任意の \(R\ge0\) で

\[
H(R;(x,y);1)=
\begin{cases}
0&R=0,\\
2&R=1,\\
1&R=2,\\
(R+1)\bmod2&3\le R\le2y,\\
2&R=2y+1,\ d>0,\\
0&R=2y+1,\ d=0,\\
R\bmod2&2y+2\le R\le S,\\
S\bmod2&R=S+1,\ d=1,\\
2&R=S+1,\ d=2,\\
R\bmod2&R=S+1,\ d\ge3,\\
S\bmod2&R\ge S+2.
\end{cases}
\]

従って値2位置は、\(d=0\): \(\{1\}\)、\(d=1\): \(\{1,2y+1\}\)、\(d=2\): \(\{1,2y+1,S+1\}\)、\(d\ge3\): \(\{1,2y+1\}\)。

証明はR強帰納。C子には既証明z=0閉形式、境界y=1のB子には単一トークンz=2閉形式を用い、対角線・非対角線y≥2・境界y=1を場合分けしてmexを一致させる。完全な証明は[実験報告](../../experiments/vertical-fiber-two-token-z1-slice-20261116/report.md)を参照。独立有限監査は[検証器](../../experiments/vertical-fiber-two-token-z1-slice-20261116/verify_z1_slice.py)で288,360状態・不一致0、偶奇301,320点・tail32,400点で違反0、二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性は強帰納法による。\(z\ge3\) の2トークン全位置予想は引き続き未証明。


## 2トークン族の高さ \(z=2\) スライス（全Grundy値の全称閉形式）

\(S=x+y\)、\(d=x-y\)、\(x\ge y\ge1\) とする。値2位置を
\[
T_2=\{1\}\cup
\begin{cases}
\{S+1\}&d=0,\\
\{S,S+2\}&d=3,\\
\{2y+3\}&d\ge4,\\
\varnothing&d=1,2
\end{cases}
\]
とする。奇数R≥3で値1となる集合は
\[
\mathcal O_2=
\begin{cases}
\{3,5,\ldots,S-1\}&d=0,\\
\{3,5,\ldots\}&d=1,\\
\{3,5,\ldots,S-1\}&d=2,\\
\{3,5,\ldots,S-2\}\cup\{S+4,S+6,\ldots\}&d=3,\\
\{3,5,\ldots,2y+1\}&d\ge4\text{ 偶数},\\
\{3,5,\ldots,2y+1\}\cup\{S+4,S+6,\ldots\}&d\ge5\text{ 奇数}.
\end{cases}
\]
偶数R≥4で値1となる集合は
\[
\mathcal E_2=
\begin{cases}
\{S+1,S+3,\ldots\}&d\in\{1,3\},\\
\{2y+4,2y+6,\ldots\}&d\ge5\text{ 奇数},\\
\{2y+4,2y+6,\ldots,S+2\}&d\ge4\text{ 偶数},\\
\varnothing&d\in\{0,2\}.
\end{cases}
\]
ここに現れる各列は偶数列である。

**定理.** 任意のR≥0について
\[
\boxed{
H(R;(x,y);2)=
\begin{cases}
0&R=0,2,\\
2&R\in T_2,\\
1&R\in\mathcal O_2\cup\mathcal E_2,\\
0&\text{それ以外}.
\end{cases}}
\]
特に値2位置はd=0で \(\{1,S+1\}\)、d=1,2で \(\{1\}\)、d=3で \(\{1,S,S+2\}\)、d≥4で \(\{1,2y+3\}\)。既存の2トークン3族値2位置予想のz=2スライスが全称証明された。

**証明.** R強帰納。選択肢値集合を \(\mathcal V_R\) とする。Theorem Tより全状態でH≤2、偶数RではH≤1。奇数Rの親ではR−1が偶数なのでA/B子は0/1、C子も既証明z=1公式と偶数残容量の上界により0/1。従って \(\mathcal V_R\subseteq\{0,1\}\) であり、集合が{0},{1},{0,1}のどれかに応じてmexは1,0,2。偶数R≥4では親の値が高々1なので、H=1は \(0\in\mathcal V_R\) と同値。R=1の選択肢集合は{0,1}、R=2は{2,3}で直接評価する。

A子には帰納仮説、C子にはz=1全Grundy閉形式を使う。y=1のB子は単一トークン(x), z=3の既証明閉形式を使い、x=y=1も含める。代入後の選択肢表は実験報告の奇数・偶数表の通りである。奇数表は選択肢集合が{0,1}となる位置、{0}となる位置、{1}となる位置をそれぞれT₂から1を除いた集合、O₂、残りへ分ける。偶数表は0を含む位置がE₂を与える。従って表示式のmexが全てのRで一致する。∎

独立監査は[実験報告](../../experiments/vertical-fiber-two-token-z2-slice-20261116/report.md)、[検証器](../../experiments/vertical-fiber-two-token-z2-slice-20261116/verify_z2_slice.py)、[監査結果](../../experiments/vertical-fiber-two-token-z2-slice-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-vertical-fiber-two-token-z2-slice.md)。x≤80・全y≤x・R≤S+8の291,600状態、選択肢表288,360点、偶数R146,620点、tail19,440点、値2位置144,980点、固定seed散点200件で不一致・違反0。二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性は上記強帰納法による。z≥4の2トークン全Grundy閉形式・一般値2位置予想は未証明。


## 2トークン族の高さ \(z=3\) スライス（全Grundy値の全称閉形式）

\(S=x+y\)、\(d=x-y\)、\(x\ge y\ge1\) とする。値2位置は
\[
T_3=
\begin{cases}
\{1\},&(x,y)=(1,1),\\
\{1,3,S\},&d=3,\\
\{1,3,2y+3,2y+5,2y+7\},&d=4,\\
\{1,3,2y+3\},&d\ge5,\\
\{1,3\},&d\in\{0,1,2\},\ (x,y)\ne(1,1).
\end{cases}
\]
値1位置は
\[
P_3=P_{\rm low}\cup P_{\rm high},\qquad
P_{\rm low}=\{R\in2\mathbb Z:4\le R\le\min(S,2y+2)\},
\]
\[
P_{\rm high}=
\begin{cases}
\{R:R\ge S+1\},&d\in\{1,3\},\\
\{R:R\text{ odd},\ R\ge2y+5\}\cup\{R:R\ge S+4\},&d\ge5\text{ odd},\\
\{R:R\text{ odd},\ 2y+5\le R\le S+3\},&d\ge6\text{ even},\\
\varnothing,&d\in\{0,2,4\}.
\end{cases}
\]
任意の \(R\ge0\) で
\[
\boxed{H(R;(x,y);3)=2\ \text{if }R\in T_3,\quad
1\ \text{if }R\in P_3,\quad 0\ \text{otherwise}.}
\]

証明はRに関する強帰納。A子にはz=3の帰納仮説、C子にはz=2閉形式、y=1のB子には単一トークンz=4閉形式を用いる。Theorem T（全状態H≤2、偶数RではH≤1）により、奇数親は子値集合{0,1}のmex、偶数親は選択肢に0があるかで分類できる。R=0..4を直接処理し、その後の全d・R帯の選択肢表を報告書に記載した。有限計算を全称性の根拠にはしていない。

独立監査は[実験報告](../../experiments/vertical-fiber-two-token-z3-slice-20261116/report.md)、[検証器](../../experiments/vertical-fiber-two-token-z3-slice-20261116/verify_z3_slice.py)、[監査結果](../../experiments/vertical-fiber-two-token-z3-slice-20261116/output/audit.json)、[研究ログ](../../log/2026-11-16-vertical-fiber-two-token-z3-slice.md)。x≤20・全y≤x・R≤S+8の6,300状態、奇数選択肢表3,095点、偶数選択肢表2,995点、偶奇上界6,300点、tail1,050点、値2位置3,095点、固定seed散点50件で不一致・違反0。二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性は強帰納法による。z≥4の2トークン全Grundy閉形式・全高さの値2位置予想は未証明。
