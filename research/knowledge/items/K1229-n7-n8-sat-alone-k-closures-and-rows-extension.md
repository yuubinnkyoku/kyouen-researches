---
id: K1229
title: 7×7・8×8の最大安全サイズ14/15のSAT単独確定とn=7〜9極大行の非空域拡張・at-least閉包
kind: proposition
status: computed
topics:
- maximum-safe
- maximal-safe
- sat-verification
- geometry
aliases: ["K_7=14 SAT alone", "K_8=15 SAT alone", "n7 n8 n9 rows spectrum extension", "dual Sinz v2 start clause", "safe-at-least closures n7 n8"]
relations:
- type: depends_on
  target: K0029
  note: 既知値表・本項は値更新ではなくSAT単独の第三手法再確定 (値は不変)
- type: depends_on
  target: K1221
  note: pinned enc_sat2 v2.1のlex-leader鎖と受入言語規約
- type: depends_on
  target: K0057
  note: 禁止四点組カタログのアンカー (census anchors)
- type: depends_on
  target: K1225
  note: 小盤全行の既刊・n7〜9は本項が拡張
- type: depends_on
  target: K1228
  note: n3-n6のSAT単独確定・本項はそのn≥7側の手法拡張
- type: contrasts
  target: K1169
  note: n8-ge16をSAT (CDCL) でも閉じ別手法交叉確認
- type: depends_on
  target: K0031
  note: s_7=7との行整合 (n7 k=6行のUNSAT再導出)
artifacts:
- path: research/experiments/n7n8n9-sat-alone-kn-closures-20261122/README.md
  role: source
  note: 主張・方法・較正・バグ修正記録・trust boundary
- path: research/log/2026-11-22-n7-n9-sat-alone-kn-closures-session-log.md
  role: source
  note: 発見順の実行記録
---

# 7×7・8×8の最大安全サイズ14/15のSAT単独確定とn=7〜9極大行の非空域拡張・at-least閉包

標準共円盤 (q=4) について、exactly-k極大安全行のSAT判定 (pinned enc_sat2 v2.1 + 双対Sinz at-leastリフト) とsafe集合at-least-k閉包 (S1+LX+双対Sinz v2) により次を確定した。いずれも**有限盤の機械計算**であり形式証明ではない (trust boundaryは実験README)。

## 確定した事実

1. **K_7 = 14・K_8 = 15 をSAT単独で確定** (値はK0029表と同一):
   - 7×7: ≥15石の安全集合は存在しない (UNSAT・独立2符号化一致: default 4.86s/200,082 conflicts・--shuffle=42 5s)。7×7の14石極大安全witness (exactly-k, SAFE+MAXIMAL検証済み) と合わせ K_7=14。
   - 8×8: ≥16石の安全集合は存在しない (UNSAT・2符号化: 199.2s/5,646,514c・181.96s/5,245,460c)。15石witnessと合わせ K_8=15。K1169の分割完全探索 (2026-11-20) と独立に一致する別手法交叉。
   - 手法的意義: K_7/K_8の確定根拠が「CYCLE5完全最大探索」に加え「SAT (CDCL) 単独」でも成立することの機械的実証。K1228 (n3-n6) と同じ到達方法をn=7,8に拡張した。
2. **n=7〜9の極大安全行 (exactly-k) の非空域を拡大**:
   - 7×7: k=9..14 の各行に極大安全配置が存在 (12 witness、default/--shuffle=42両ショット、全て独立整数検証 SAFE+MAXIMAL・石数一致)。k=15以上の行は空 (exactly-k UNSAT×2 + ≥15 safe UNSAT×2)。
   - 8×8: k=10..15 の各行に存在 (12 witness)。行≥16はge16閉包で一括して空。
   - 9×9: k=10..17 の各行に存在 (16 witness; k=17は公開証明書と同レベル)。行18はW9 (第三系検証済・18行目の極大性はaddcost≥3で全空点確認済み) により非空。行≥19はK_9の上界に依存し本項では非主張 (ge19判定はn9-ge19レーンが所有し、本レーンの240s shotはINDET)。
   - n7の行状況は s_7=7 (K0031, 最小行) + 本項の k=9..14 + 既刊のk=7,k=8行 により7×7の極大行の非空域は7..14となり、≥15は閉じた。
3. **W9細部注入陽性対照** (n9 ge18): 18石証人W9の8つのD4像で全セル変数を単位節固定してkissatで解くと、恒等像のみSATISFIABLEで他7像はLX鎖によりUNSATISFIABLE。n9スケールの符号化は既知の18石witnessを受容し、fresh探索の240s INDET (6,118,159 conflicts) は符号化ではなく探索能力の限界。
4. **n4全数較正**: 2^16全列挙 (safe合計5,811・極大 {5:176, 6:688, 7:64}) に対し、修正版の全判定 (sa ge-k k=1..12・exactly-k k=1..8・両ショット) が完全一致。
5. **双対Sinzカウンタのv2修正 (訂正記録)**: 両カウンタ (atleast_lift.mjs・enc_safe_atleast.mjs) にj=1開始節 (x_i, U(i,1)) が欠落していた。セル0が石のときat-least-k半束縛が空文化する純緩和のバグで、n7 ge15のshuffleショットが0秒SATを返したことで発覚した。models(pre-fix) ⊇ models(post-fix) なので**pre-fixのUNSAT判定はすべてa fortiori有効**、pre-fixのSAT判定は単独では無価値 (全SAT witnessは復号+独立検証済みで、行非空の証明書としては有効)。修正後のv2で全閉包を再実行した。n4較正を透過した機構 (最小極大サイズ5とat-most-k底の相互作用) をも含めて教訓を実験READMEに記録する。

## 非主張

- K0029の値更新はない (K_7=14・K_8=15は既刊値の再確定)。s値も不変。
- K_9の上界への主張は一切ない (ge19判定はn9-ge19レーン所有・本レーンのshotはINDET)。fresh探索が240sで18石witnessに到達できないという負の知見のみ。
- 有限盤のみ。実装・符号化・kissat 4.0.4 (md5 3a5eba830aa6008a604fcc9bbe99a325) のtrust込み・形式証明ではない。
- 標準11×11空盤・二石root・S2・closure classは非接触 (UNKNOWNのまま)。
- n=7〜9の行の**個数** (行ヒストグラム) は対象外 (witness existenceのみ)。ゼロ行のうち本項が確定したのはn7 k≥15・n8 k≥16 (safe側閉包) と較正行 (n4/n6/n7既知行) のみで、n7のk≤6・n8のk≤9の行状況は既刊 (K1224/K0031/K0032) に依る。
