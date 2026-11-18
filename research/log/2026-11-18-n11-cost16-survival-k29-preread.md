# 2026-11-18 N11 cost-16 parent 生存曲線: k=29構造preread — rank-29 (0,16) は過去最多24本のdisjoint partnerを持つ深い非ハブ根・b_only quint 331→2,128本に急増・行16が二重行に初登場

本logはk=28出版（script+log commit `a6010eef`・result JSON commit `efc500fa`・JSONL commit `42182831`）とrank-28構造preread（commit `e6cc8e05`）を受けて、**k=29の本計算に先立つrank-29の純構造census**を確定したものである。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

入力は出版済み3ファイルのみ（git blob sha1 pin検証済み）: phase-B aggregate `31bdefdb2e2cc90b706cbb8090e98eb5eece4d87`・k27 result JSON `3dc30ad6c51cc2d7678cc8777e4af2376267ddb8`・k28 result JSON `99db3a9a48d044727b3a4d83fb7fc97daa7513d2`。k28 preread script（18,491B）からの機械変換は19ブロックすべてに単一発生assertを付けて実施（衝突回避のため文脈付きブロック置換・残存grepでstale token 0件）。

## rank-29構造確定値（2分類器合意・24,157組合せ 0 mismatch）

1. **rank-29 root = `(0, 16)`**（root hex `00000000000000801202000000101001`・**m29 = 120,237,984,360,505,181**〔A = 92,134,149,767,703,050 / B = 28,103,834,592,802,131・A+B=m29照合済み〕）。行16はこのrootで初被覆。**行0と行16のprior被覆は各2本のみで、行18を持たない深い非ハブ根**。
2. **28新pairs: shared 4 / disjoint 24**。**disjoint partner 24本は過去最多**（k23: 17本→k26: 23本→k29: 24本）。shared 4本も近世最少（k26の2本に次ぐ低さ）。
3. **378新triples: b_only 195 / zero 32 / disjoint 151**。disjoint割合39.9%は構造的に高い。
4. **3,276新quads: b_only 1,516 / zero 1,535 / disjoint 225**。disjoint quadは225本で単一rankとして過去最多（k28の22本の10倍超）。**累積 disjoint quad 277 → 502本**（225本すべて|union|=8を機械検証）。
5. **quint era継続・急増**: 20,475新quints中 **b_only 2,128本**（前層331本の6.4倍・quint era開始以来の急増）。zero 18,347 / **disjoint 0**。累積b_only quint 2,512 → **4,640本**（全C(29,5)=118,755中）。二重行ヒストグラム: **行18: 1,297 / 行15: 283 / 行16: 172 / 行19: 376 — 行16が二重行族に初登場**（{15,18,19}以外の二重行はquint eraで初めて）。全b_only quintの4-subset profileはすべて3/2/0のまま。
6. 全C(29,3)=3,654 triple census: b_only 2,204 / zero 759 / disjoint 691。全C(29,5)=118,755 quint census: b_only 4,640 / zero 114,115 / disjoint 0（k28 published値2,512/95,768/0との差分が新層censusと厳密一致）。

## 予測（k=29本計算の前評）

- **disjoint-partner法則上、marginalの大幅な急落が予測される**。法則本体「marginal ≈ m − disjoint本数×約5.3〜5.4e15 + j3補正」（平均disjoint pair jointの実績値）に24本を代入するとΣ新j2 ≈ 24×5.3e15 ≈ **127e15 > m29 = 120.2e15**で、k26と同型（k26はΣj2がm26の100.45%に到達しmarginal 26.34%）を超える反転が見込まれる。k23（17本→38.1%）・k26（23本→26.34%）の観測を外挿すると**marginalはm29の26%前後またはそれ以下の過去最低**となり、B_surviveは3.7928%からさらに更新される。
- **本計算コストの急増**: b_only quint record 331 → 2,128本（MyPm count対象・zeroはclassify即skip）・disjoint quad 22 → 225本（B型Σ_{d,a<b}多次元pm呼び出し）・disjoint triple 38 → 151本。k28実績13分の数倍、概算20〜40分（1並列CPU・スライス分割前提）。
- **C(29,6)=475,020のsextet構造的ゼロ確認が本計算で必要**（quint-order I-E打ち切りの安全性証明・`583b0bf1`のsextet census機構のk29への拡張）。b_only quintが4,640本に達しても全6-subsetがzeroなら打ち切りは正当。

## 検証

- **21 checks all PASS**。上位3common check（top50濃度・root一意性・2行妥当性）+ rank-28回帰3check（published k28とのcensus/root全一致・2分類器0 mismatch・anchor照合）+ rank-29主体15check。
- rank-28回帰: 新census（pair 14/13・triple 214/99/38・quad 626/2,277/22・quint 331/17,219/0）・全C(28,3)/C(28,5) census・二重行ヒストグラム差分（`quints_zero_synth_count`=17,219込み）が出版k28 JSONと完全一致。
- 2分類器（list-based `classify_map` と bitmask-based `classify_masks`）が新層+全層censusの全24,157組合せで一致（0 mismatch）。
- 双方向の層接続: rank-29全quint census − 新層 = published k28全census（b_only/zero/disjointすべて）。二重行和は{15,16,18,19}の4行で再合成一致（行16のprev側は0を`.get`で補完）。
- finalize二重実行byte-identical（出力JSON sha256 `3fb89ef29fb818b641067b9a0f7df6f078545d739671bdf13744c40fb2b4cff6`・605,999B）。
- git blob: script = `7e86e52826f37df2889b6af6e44c18271c8653cf`（18,582B）・preread JSON = `ad9dd779161141b9db1a6de14d096f676fb5b454`。

## 11×11空盤の現況（interpretation guard）

標準11×11空盤は**UNKNOWN**。空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4のいずれについても、本prereadは何のverdictも生成しない（cover-plan組合せ数の構造censusのみ）。
