# 2026-11-18 remo-firsthit-extreme（K0959）作業ログ

目的: K0956が残したOPEN「F(M)の遠域平坦化の機構」を、F表（303素数）と
firsthit_rows（1,546クラス）の極値統計で解決する。

## 発見順

1. **F恒等式の確認**: F=(M+1)F_t+F_kappaが303/303、F_type=branchが303/303、
   κ*偶数が303/303（K0949 PARITYの系）。Fは単調でない（137/302隣接ペアで
   減少・max F=220,140）。漸近議論は点別でなく統計的にするしかない。
2. **平坦化のsurrogate実験（FLAT-ARTIFACT）**: 指数ドリフト
   1.5088→1.3861→1.2798に対し、純粋決定論的法則g_d(M)=M ln^d Mを
   同じ3 gridで冪フィットすると同じ減衰パターンが出ることを発見
   （d=1.8で大きい2 gridはobservedと0.006以内）。指数ドリフトはgridの
   長さの関数であってレジーム変化の証拠でない。逆に固定(α,d)は3 gridを
   同時に当てはめられない（slope-1 R² 0.886/0.924/0.745）ので、
   この範囲でF~αM ln^d Mという形も棄却できない範囲で保留。
   安定量はF_t/ln²Mのbucket median ∈[0.856,0.976]。
   K0956のOPENを「機構: フィッティング産物」として解決。
3. **BHの再解釈（BH-EXTREME）**: pooled Spearman 0.1619はノイズ支配のまま、
   top-decile 0.5633・top-3 overlap 0.9302・argmax一致9/43・worst classの
   BH正規化rank median 0.273。修正from-start BHモデルはbulkの順序を
   予測しないが極値（どのクラスが遅いか）はよく当てる「極値モデル」。
4. **EV増幅（EV-AMP）**: t*/median(t_first)がiid指数baseline ln(2n)/ln2を
   median 1.363倍上回る。M=181は5.66倍。クラスレートの非一様性が
   最悪値を約1.4倍増幅する構造。
5. **ENGINE-F**: 全303 F行をピン済みengineで直接照合（σ_Z(M,F)=1・
   0失敗・3.4秒）。K≤220,140で、K0956のengine錨（K≤7,440）を
   大幅に拡大した有限アンカー。

## 機械結果の要約

- F-IDENTITY: 303/303（identity・branch型・κ*偶数）。max F=220,140。
- FLAT-ARTIFACT: surrogate β（d=1.8）1.6282/1.3900/1.2736 vs observed
  1.5088/1.3861/1.2798。bucket median F_t/ln²M: 0.8696/0.9761/0.8949/
  0.9126/0.9351/0.8560。
- BH-EXTREME: pooled 0.1619・top-decile 0.5633・top-3 overlap 0.9302・
  argmax 9/43・worst norm rank median 0.273/mean 0.399。
- EV-AMP: median excess 1.3632・mean 1.6092・n_M=41（M≥50でmedian 1.385）。
- ENGINE-F: 303照合0失敗。
- F_C: 2が68/303・C>100が55件・C=(M+1)/2が20件（最悪クラスはC単独で
  特徴づけられない）。
- 監査は決定的（2回cold実行byte同一）。output/audit.json sha256 75063f46…。
  K0956 output（audit.json d7273718…・firsthit_rows.json e7df3eae…）は
  相対path+shaピンで参照（repo上の原本を直接読む）。

## 次課題

- F_t/ln²Mのbucket medianのM→∞挙動（2,000<MでのF表拡張には
  K0956 FIRSTHITのt_cap掃引延長が必要）。
- EV増幅の定量モデル化（クラスレートの異質性の分布をBHパラメータから
  復元し増幅因子1.4を導出できるか）。
- BH極値モデルの正当化（極値統計としての補題化。有限観察のまま）。
- F_type=branchがMで普遍か（smooth最悪クラスの非存在をΩ≥4統計と
  接続して説明できるか・K0958の2集団構造が鍵）。
