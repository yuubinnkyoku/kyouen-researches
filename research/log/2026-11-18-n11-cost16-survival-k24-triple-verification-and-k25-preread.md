# 2026-11-18 N11 cost-16 parent 生存曲線: k=24の3重独立検証の確定・正本title erratumの検証済み修正recipe・k=25構造の事前機械確定

本logは、同一時限タスクの並走実行のうち当レーン（第三実行）がk=24を独立に全計算した結果のうち、先行2実行（`b89cd0f5` 出版・`46cf61f7` rerun記録）がまだ残していない3点を出版する: (1) k=24が**3実行すべて値完全一致**であることの確定、(2) 正本title erratumについての**byte-exact検証済み修正recipe**（適用は見送り・理由と推奨タイミングを記録）、(3) **k=25の構造censusの事前機械確定**（次レーンの変換assertに直接使える）。

## 1. k=24の3重独立検証

当レーンは正本k23 script（blob `46374ca4…`）を2段階機械変換でk24 scriptを生成し、構造censusをpm値を書く前にpinned aggregate（blob `31bdefdb…`）からclassify()で機械確定してから全計算を実行した（pairs 23本60秒・triples 253本7 slice・quads 1,771本30 slice・cross・finalize二重実行byte-identical）。27 checks all PASS・cross mismatches 0。

先行2実行との照合:
- **JSON**: 全数値・構造・checks完全一致（差異はtitle行のみ=後述のerratum）。kill(24) = 2,198,596,292,207,938,784（74.1154%）・B_survive(24) = 159,755,754,124,480,302（5.3854%）・marginal = 62,646,884,579,080,928（m24 = 120,643,896,818,077,661 の51.9%）。
- **JSONL**: 2,051/2,051 record・kind census同一（pair 23 + triple 253 + quad 1,771 + cross 4）・値差分0・memo_states差分0・差異はwall-clock `sec` field 133件のみ。

これでk=24曲線は**3つの完全独立実行（script生成経路も独立）で全値一致**したことになる（1つ目=`b89cd0f5`出版・2つ目=`46cf61f7`記録・3つ目=当レーン）。marginal decompositionも3実行共通: Σj2 = 65.24e15（m24の54.08%: disjoint 12本64.49e15・行18共有11本0.75e15）・Σj3 = 7.30e15・Σj4 = 0.059e15で、恒等式 m24 − Σj2 + Σj3 − Σj4 = marginal が厳密成立。「disjoint partner数がmarginalを決める」法則はk24の反転回復（disjoint 17→12でmarginal 38.1%→51.9%）で6点目の確認。

## 2. 正本k24 title erratumの検証済み修正recipe（適用見送りの記録）

正本k24 script・JSONのtitle文字列がk=23旧文言のまま残っているerratum（`46cf61f7` logに"cosmetic only"として記録済み）について、当レーンは修正を**検証まで完了しながら適用を見送った**。その判断材料を残す。

**検証済み修正recipe**: 正本scriptのtitleブロック6行を正しいk=24文言（当レーンのtitle文字列）に置換した修正版scriptと、正本JSONL（blob `6dfbc5e2…`）からfinalizeを再実行すると、**27 checks all PASS・出力JSONは3実行の合流点としてbyte-identical**（sha256 `0b0f5da8…`・git blob `2b0b219bef45b9b12557eec9c554eb22afb4d3d1`）となる。修正版script = 34,863B・sha256 `36889fc3…`・git blob `e03f533b…`。同時にcrosscheck script（k13..k24拡張版）のpin `a0955297…` を `2b0b219b…` に更新すれば検証連鎖は完全に保たれる。

**適用を見送った理由**: (a) k25変換が進行中の可能性が高く、その変換が記録する `K24_JSON_PIN` は現行resume記録（正本log・rerun logとも `a0955297…`）に従うため、canonical k24 blobを今変更すると**出版済みk25の入力pinとmainのk24実体の不整合**が生じる。(b) 3実行が並走する環境ではcanonical data編集のrace窓が大きい。(c) erratumは値・構造・検証に影響せず、schema名・rank24_root・marginal_k24は正しい。

**推奨対応**: (i) k25変換では、正本k24 scriptの**stale titleをそのままanchorに使い**、正しいk25 titleを書く（title系の自己修復。変換後grepで「title・usage・docstring・census・assert・pin・RES filename・rank_root・marginal・schema」の全置換を機械確認）。(ii) title系erratumの一括修正は、k系列の計算が一時停止する静穏窗口で、関係pin（crosscheck・直近出版のinputs記録）を同一コミットで更新して行うのが安全。

## 3. k=25の構造censusの事前機械確定（次レーン向け）

pinned aggregate（blob `31bdefdb…`）のtop-25とclassify()のみから、pm値を一切計算せずに機械確定した。次レーンのk24→k25変換のcensus assertにそのまま使える。

- **rank-25 root**: `(18,25)`（root `00000000000000909002001000100000`・行 [18,25]・**ハブ型**〔行18〕・m25 = 120,623,825,876,971,692）。上位24本に行25を含む根は存在しない（shared partnerは全て行18共有）。
- **新pair 24本**: shared **12** / disjoint **12**（complete C(25,2)=300・base 276 + 24）。
- **新triple 276本**: b_only **176** / zero **73** / disjoint **27**。
- **上位25本triple census C(25,3)=2,300** = b_only **1,460** / zero **523** / disjoint **317**（k24出版census 1,284/450/290 + 新176/73/27 と一致）。
- **新quad 2,024本**: b_only **398** / zero **1,626** / disjoint **0**（complete C(25,4)=12,650・base computed quads 9,911 + 2,024）。
- **全C(25,5)=53,130個の5-subsetが構造的ゼロ**（機械確認 bad=0）→ I-Eのquad打ち切りはk=25でも維持見込み（12度目）。
- **marginal予測**（法則の外挿・計算前の予告として記録）: disjoint partner 12本（k24と同数）なのでΣj2 ≈ 64e15 ≈ m25の53%付近、marginalはm25の**約51〜53%帯**に留まると予想。実測で検証されたい。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。
