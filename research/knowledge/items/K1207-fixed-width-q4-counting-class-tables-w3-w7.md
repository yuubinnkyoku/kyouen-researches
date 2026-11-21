---
id: K1207
title: "固定幅q=4のw=3..7ブロッキング計数クラス表と需要供給不等式の第一原理証明 — B_max(w)+1 = T_w（M_{4,4}≤237・M_{5,4}≤567・M_{6,4}≤1113・M_{7,4}≤1929）、m≥35で15/34クラス・m≥200で(2,3,3,3)単独の生存band、91盤census・105 witness再検証のfail-closed検証器"
kind: proposition
status: proved
topics:
- rectangles
- maximal-safe
- fixed-width
aliases: []
relations:
- type: depends_on
  target: K1202
  note: 機構の前例。本項の証明は第一原理のみに依りK1202の証明には訴えない。K1202は較正対象（公表w=3の19クラス値と完全一致）として使用し、需要供給不等式の独立再導出にもなる
- type: depends_on
  target: K0068
  note: B_max(w)+1 = T_w（w=3..7）を本項の計数クラス経路から導出（K0068の偶奇式機構とは独立な第二の自己完結証明書。改善ではなく同値の再確認）
- type: depends_on
  target: K0833
  note: 再検証対象の公表witness銀行4種（(4,4)m=4..34・(5,4)m=5..36・(6,4)m=6..31・(4,5)m=5..20）と、盤censusアンカー（4×35=41,607を含む8ケース）
- type: related_to
  target: K0318
  note: topクラスBの値がcurve-packing上界と一致（本文の整合説明のみ。K0318の証明自体には触れない）
artifacts:
- path: research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/README.md
  role: proof
  note: 主張・機構・較正・バンド表・何でないか・part 2計画（委細は本文）
  commit: ea67e399ae4f57535178884dbce219e393ab8cec
- path: research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/scripts/verify_counting_wq4_20261121.py
  role: verifier
  note: fail-closed決定的検証器（stdlibのみ・sha固定入力・2実装・負対照・--fast/--tamper）
  commit: fb3b16df50e139afbfcaefcd82b7f778a68fb308
- path: research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/scripts/captable_q4.py
  role: code
  note: クラス表生成器（2実装一致assert付き）
  commit: 33d49a09b9f31a52af060f5664584664ee24b037
- path: research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/output/captable_q4.json
  role: data
  note: 計算済み全クラス表（w=3..7）
  commit: f4c7a56c75e2e04a055f5b7c1dd5f51701a02813
- path: research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/output/audit.json
  role: data
  note: full-mode監査（全ゲートPASS・91盤census再計算・105 witness・バンド・digest）
  commit: b45c403a132e9758ab28a932d0f8e247bfbc77fa
- path: research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/output/reproduction.log
  role: data
  note: 再現バッテリー（full x2 同一digest・PYTHONHASHSEED=random fast・tamper陰性対照）
  commit: 919d1b2fd5e2c9a0eef6b5a79a907a41cea51908
---

## 定理（第一原理証明）

設定: w×m盤（w行）、q=4。石配置 S が安全（どの直線・円上にも石は4個未満）
かつ極大（どの空セルを追加しても安全でない）、行石数プロファイル
r = (r_1..r_w)（各行石数、SSOT規約により3以上は3に切り詰め）、欠損行
D = {i : r_i ≤ 2}、d = |D| とする。

**補題1（被覆の割当）**: 極大性より、各空セル c は何らかの曲線上にあり、
その曲線は「c 以外に S の石3個」を乗せる。c の属する行が欠損行 i のとき、
このカバー三つ組 T(c) は非水平である。実際、T の石3個が同一行にある
とき、その行を j とすると曲線は行 j の水平線であって c（∈行 i）を通れず、
また j = i は r_i ≥ 3 に矛盾する。各欠損行空セルに T(c) を1個割り当てる。

**補題2（三つ組ごとの被覆上界）**: 石三つ組 T に対し、その構成曲線が
円なら行 i との交点は高々2個、（非水平）直線なら高々1個（wに依らない）。
そのうち T の石であるものが u_i 個だから、T の曲線が行 i の空セルのうち
被覆し得るものは高々 max(0, 2−u_i)（直線なら高々 max(0,1−u_i) でさらに小さい）。

**定理（需要供給不等式）**: 各非水平三つ組 T（行占有 u(T)）について
占有率パターン {1,1,1}・{2,1} のものを数えると、プロファイル r における
非水平石三つ組の総貢献は

CAPS(r) = Σ_{非水平T} Σ_{i∈D} max(0, 2−u_i(T))
       = Σ_{u=1,1,1} ∏_i C(r_i,u_i)·cap(u) + Σ_{u=1,2} ∏_i C(r_i,u_i)·cap(u)

であり、割当 c ↦ T(c) と補題2より

d·m − Σ_{i∈D} r_i  =  #（欠損行の空セル） ≤  CAPS(r)。

行占有パターンごとの石三つ組数が ∏_i C(r_i,u_i) であること（各行から
u_i 個を選ぶ組合せ）から、CAPS はプロファイル r だけで決まる。よって

**系（クラス上界）**: m ≤ B(r) := (CAPS(r) + Σ_{i∈D} r_i) / d（床）。
CAPS(r) = 0 となるクラスはどの m ≥ 1 でも生存不能（r の石では非水平
三つ組が足りず、補題1の割当が存在しない）。ただし d = 0（全行飽和）は
対象外。証明終。
（証明は上記3ステップのみで、K1202/K0318/K0068のいずれの証明にも
訴えていない。w=3 ではこの表は K1202 公表19クラス値と完全一致する。）

## 計算結果（w=3..7 全クラス・2実装一致）

w=4: 34 / w=5: 55 / w=6: 83 / w=7: 119 クラス
（output/captable_q4.json、生成器 captable_q4.py、検証器でも閉形式A・
リテラルB両実装が全クラス一致・隣接互換生成の全順列不変性を確認）。

**帰結1（上界・第二自己完結証明書）**: トップクラスは (2,3^{w−1})、
B(w) = 236 / 566 / 1112 / 1928（w=4..7）より
M_{4,4} ≤ 237、M_{5,4} ≤ 567、M_{6,4} ≤ 1113、M_{7,4} ≤ 1929。
B_max(w)+1 = T_w = 3+2{C(3w−2,3)−(w−1)}（K0068）が w=3..7 で厳密に成立
（w=3 は K1202 公表値との較正、top B=68 → T_3=69）。K0318 の curve-packing
代入上界とも同一値。既刊値の改善ではなく独立経路による再導出である。

**帰結2（クラス解像度のバンド帰結・新規）**: w=4 の全34クラス表から、
行欠損極大安全配置の m ≥ t における生存クラス（B ≥ t）の完全リスト:
t=200 なら (2,3,3,3) 単独、167 で2、163 で3、124 で4、113 で5、89 で6、
73 で9、50 で11、37 で14、36 と 35 で15クラス。
**(4,4) m=35/36 の witness はこの15クラス以外には存在し得ない**
（34クラス中19クラスが機械的に除外され、m≥35 のクラス分割掃引・
近傍witness探索の枝刈りに直結。m≥200 ならプロファイルは単一欠損{2}に
確定）。m ≤ 34 の公表 witness 帯（K0833）はこの帰結と整合
（m=34 witness のクラスは (2,3,3,3)、B=236、実例不等式 m ≤ B は全31+32+26件で成り立つ）。

## 検証（fail-closed・決定的・stdlibのみ・単プロセス・実行時ネットなし）

検証器 verify_counting_wq4_20261121.py のゲート:
(1) 入力7ファイル sha256 固定。(2) 独立 census（降下斜線込みの原始方向
直線走査・既約整数外心による円の正準化・同心円は2乗距離で分離）が公表
census を全再現（4ケース相互チェックファイル、(4,35,4): 直線413+円41,194=
41,607、(3,24,4)=6,413、(4,10,5)=89・(4,20,5)=491、レコード埋め込み census
は full mode で91盤再計算・残り14盤は公表値と重複レコード間整合のみ誠実
deferred 記載）。(3) クラス表2実装+順列不変性+ピン期待表+K1202 w=3 較正
19値+top主張+B_max+1=T_w。(4) 公表 witness 銀行4種105件全部の整数幾何
再検証（安全性・極大性・行ヒストグラム・q=4 では実例不等式 m ≤ B(class)、
正準円キーによる幾何）。(5) バンド完全一致。(6) 負対照（誤バンド拒否・
--tamper の4種汚染〔表値/バンド/censusアンカー/witness石〕すべて検証失敗
で検出・audit不書込）。再現: full x2 同一 content_digest（cd7631a5…）、
class表 table_digest（55f9df70…）、PYTHONHASHSEED=random の fast も同一
digest。full ~136s / fast ~5s（CPython 3.12.14）。全ゲートPASS時のみ
audit.json を書く。

## 何でないか

- (4,4) m=35/36 の**不在も存在も主張しない**。近傍witnessエンジン
  （このレーンの part 2）は本項では未実行。
- 上界の数値は既刊（K0068 偶奇式・K0318 curve-packing）と同一で、
  改善ではない。新規なのは全クラス分解（バンド帰結）と独立証明書・
  検証基盤。
- 全行飽和プロファイル（d=0）と、石数0の行だけの特殊形は表の対象外。
- 標準11×11のroot/bin石/S2とclass 1/2/4の状況は本項と無関係で一切
  触れていない。

## 次課題

- part 2: (4,4) m=35（ついで m=36）近傍witnessエンジン（Node BigInt・
  公表witnessベース×平行移動×D4像・essential-reduceレイヤ合成）。本項の
  生存15クラスと正準円キー幾何をそのまま使用する。
- m≥35 のクラス分割掃引レーンが再開された場合: 19クラスは走査不要。
- w≥8 の表も同じ生成器・検証器で直ちに作れる（本項では w≤7 に絞った:
  T_w との対比対象として十分）。w=8 のクラス数は 164
  （長さ8の非減少プロファイル C(11,3)=165 から全3を除く。組合せ生成で確認）。
