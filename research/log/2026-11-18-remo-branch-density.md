# 2026-11-18 高速レーン — REMO値1尾部の枝密度と特異級数（K0954）

## 出発点

K0952は値1尾部を有限個のe枝（Y_e素数 ∧ e|Q ∧ Q/e素数）に全称分解し、
「e>1枝ごとの局所許容性・特異級数、固定Mの完全密度は未解決」を残した。
K0950はU_2/U_3のHL密度積分を確定したが一般MのU_M密度はOPENのままだった。
本次では枝ごとの一次形式対の局所構造を完全に決め、密度・初回ヒットの帰属を確定する。

## 最初の仮説と修正

最初のU_M密度draftは枝積分に1/eを掛けていた。t側の積分∫dt/(ln Y ln Q)を
n側に書き換えるとJacobian dt=e·dnが剰余類t≡t_e (mod e)の密度1/eとちょうど相殺し、
1/eは二重計上だった。hybrid格子積分とengineカウントの数値照合で過小予測として検出し、
um_sweep.pyの積分・docstringを修正した。修正後のBH比は23行全体で0.9501-1.0242
（U>=1e5で0.9821-1.0155）に乗った。

初回ヒット予測でも、per-M回帰F_hat=12.77·M^1.4814が観測F~1.767·M^1.5088と指数一致した
瞬間は「tailモデルがFIRSTHIT-GROWTHを予測した」ように見えた。しかし大Mでは
F_hat≈(1.10-1.33)·M^2で観測の2.5-22倍大きく、クラス単位の順位相関0.5249はM依存の
反映にすぎず、within-M平均は0.095だった。指数一致は小Mのt_hat≫t0と大Mのt_hat≈t0の
crossover産物と確定し、主張から落とした。

## 発見

- 恒等式 M·Y_e(n)-1=C·e·P_e(n)（全n>=0）が中核。両形式はmod qで決して根を共有しない
  （共通根なら0≡1）。ここから全枝の局所許容性ALL-ADMとν_e(q)の完全分類SS-STRUCTが
  一気に落ちる。SS_e=G(M,C)·Π_{q|e, q∤M(M+1)}(q-1)/(q-2)で、κはCのみ経由
  （DENSITY-CLASSIFY）。
- PRE-TAIL-FIRSTHIT: live 1,546クラス中1,545の初回ヒットがテールシームt0未満
  （唯一の例外(43,20)はシーム上）。出版FIRSTHIT-GROWTH F~1.767·M^1.5088は丸ごと
  pre-tail現象。(M,t)=(3,2)（Y=9合成でengineヒット）が枝構造のpre-tail非適用を実証。
- STARVATION再解釈: 出版sparse 69クラスは全てbh_pred_at_2e5=0。理由はcensus窓
  T=floor(2e5/(M+1))がt0=M（min M=991）に届かないから。疎尾部はpre-tail未達の現象。
- per-κ再集計（385 liveクラス・K<=2e5）でSpearman(count, BH)=0.9825、
  (M,C)群44中35群がPoisson無過散でDENSITY-CLASSIFYと整合。

## 監査

audit_build.py（監査sha256 541d1aca50fd95b1aaa26d63e2ed3ebac99cd497ab105311dde2d655d528c718・
2回cold実行byte同一・all_ok）:

- BRANCH-EXACT: M∈{2,3,5,7,11,13}全κ・t∈[t0,120]の3,898状態で枝分解==engine・不一致0・ヒット213。
- ALL-ADM: live 1,546クラス47,907枝のq<=1000障害走査0・seeded nu_pair全走査54,556照合0。
- SS-FORM: 1,154枝でnu_case==nu_pair（q<=1000）0不一致・129数値SS対照max rel diff 3.48e-7。
- SS/U_M/CENSUS錨: SS_2=3.960971・SS_3=5.281295（K0950一致）・M=3@1e5=3,658・
  @1e6=25,860・M=2@66,666=2,025（2,024+特殊1）・@333,333=7,751・census総数8/8一致・
  seam 943状態不一致0。

## 失敗・限界

- U_M-DENSITY・TAIL-FIRSTHIT-PREDはBateman-Horn条件付き。BH比0.98-1.02の一致は
  有限事実でHLの証拠ではない。
- 1/e二重計上（上記修正）と「指数一致=crossover産物」の2点は、有限fittingの見かけの
  確認を全称主張に結びつけない教訓として記録する。
- pre-tail（t<t0）のσ_Z=1構造・FIRSTHIT-GROWTH冪則の説明は未解決の別レジーム問題。
- P-KILL-TIGHTの無条件無限存在は未解決（e=1枝で十分という点はK0952と不変）。
- 有限盤・11×11への接続はない。uv check/build・unittestは本環境にcloneとuvがなく未実施。
