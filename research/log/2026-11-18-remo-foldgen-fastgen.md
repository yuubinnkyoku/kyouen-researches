# 2026-11-18 remo-foldgen-fastgen（K0951 高速レーン）

## 目的
ユーザーの定例指示（高速レーン・短〜中時間で厳密な新結果・重複回避・main直push）。
前回までの K0945（ONE-CHAR/FOLD/FAST・センサス1e5）を土台に、K0945 が観察として
残した bump 展開・連分数様再帰の厳密化と、fold 評価の高速化（FOLD-GEN）に着手。

## 経過（発見順）
1. **環境**: 本セッションも bash/Node 実行環境が再試行 2 回とも利用不能。
   歴代 remo 項目と同じ扱い（純JSサンドボックス転写 + sha ピンで再現性担保）
   として続行。uv/check/build は未実施と注記。
2. **FOLD-GEN 導出**: bump-fold フレーム (1,c,k,kTop) の評価を静寂 slack
   f(ℓ)=ℓ−x−c(ℓ−a+1) の単調性（c≥2）で特徴づけ、最初の bite レベル
   L₀=max(a,⌈(cb−D)/(c−1)⌉) と閉形式三分法を導出。境界 a≥c−1（単一wrap条件
   u≤L₀+c−2<2L₀）と x≤a−2（L₀=a のときの静寂 at a−1）の由来が明確化。
   鋭い反例 c=5,a=2,b=2,x=0（直接1・三分法3）で境界の鋭さを確認。
   grid 428,220 evals + xorshift32 20,000 点で 0 不一致。
3. **センサス拡張**: (100000,200000] を 25k チャンク E/F/G/H で掃引
   （742/759/709/663 = 2,873 件）。各チャンク rhs（下記 FINAL 方程式）・
   終端 bite・σ_Z スポット 0 違反。チャンクリスト sha をピンとして記録。
4. **構造定理**: RUNG-1（U-RUNG2-FOLD）・RUNG-2 構造（k₁=4s+a′+3、post-bump
   E(5;4s+2a′−2,4−a′)）をbump算術の直接計算で証明。その上で FINAL
   （mod-5 残差篩）を三分法のケース解析で証明: (i) 静寂不能（r=1 は K0948
   U0-CLASSIFY で u≥6 不能、u=1 例外）、(ii) u=2 のみ、(iii) L₀=k₁ 必須 →
   σ₅=4s+2a′−1・v₀=a′+1∈[0,3] → a′∈{0,1,2}、r=4 と r=1 は EXCL。
   系 TERMINAL-BITE（u∈U, u≥3 は単 bite at k₁）が証明から従う。
5. **並走レーンの K0950 出現**: セッション中に K0949→K0950 が push された。
   PAIR-3（σ_Z(3,4u)=1 ⟺ 4u+1,6u+1 素数対 ∨ u=2）は私の FINAL と同じ
   locus の独立特徴付け。重複を回避し「相互検証」に位置づけ直した:
   FINAL⟺PAIR-3 を u∈[2,20000] で 0 不一致、拡張域 (100k,200k] で
   素数篩との完全一致（2,873=2,873）、出版ドメイン 3,658 件両方向 0 違反。
   結果として U の三角形特徴付け（ones軌跡=素数対=mod-5篩）が揃った。
6. **H リスト転写ミスの発見と復元**: コンパクション跨ぎの H チャンクリスト
   転写に順序外の 183338（U 外・素数対なし）を検出。素数対集合との対称差から
   真の要素 184338 を復元し、修正後 sha がチャンクピン 3c431924… と byte 一致。
   E/F/G は最初からピン一致。この経緯は audit に記録して出版した。
7. **出版**: experiments 8 ファイル（pinned cores 2 本、foldgen_core.js・
   census_extend.js・foldgen_verify.js、fast_census.json・foldgen_audit.json、
   report.md）→ K0951 item + 本ログ。

## 判断メモ
- K0951 は push 直前 2 回（実験 push 前・item push 前）に items listing で
  空きを確認してから使用した（並走レーンとの競合回避）。
- deep_census.json は sha ピンで不変確認してから結合（並走による改変検知）。
- σ_E 掃引センサスは本項目で完成・役割終了と明記した（u>2e5 は PAIR-3 の
  素数対掃引が優位。次レーンの無駄な再拡張を防ぐ）。

## 次課題（高速レーン候補）
- rung-3 構造: decomposeE(5,12j−4,3) の bump 解析 → rung-4 方程式。
  r=0 方程式が rung-2 目標と同形（M:4→5, u→4j）であることから、一般 M の
  rung 篩の帰納的構成が本命候補。K0950 K0-FAMILY・K0949 relay-prime-m 接続。
- 一般 M rung 篩が立つなら、U の特徴付けの族（ones軌跡族）全体の
  mod-sieve 化が視野に入る。

## 成果
- FOLD-GEN（全称・証明）: K0945 FOLD の一般化、fold 評価 O(1) 化。
- U-RUNG2-FOLD・RUNG-2 構造・U-RUNG2-FINAL・EXCL-U-MOD5・TERMINAL-BITE
  （全称・証明）: U の fold 力学的 mod-5 篩。K0945 観察の厳密化完了。
- U センサス 2×10⁵（6,531 件）+ PAIR-3 相互検証（両方向 0 違反）。
- 三角形特徴付けの確定: U = ones 軌跡（K0945）= 素数対∪{2}（K0950）
  = mod-5 篩（K0951）。
