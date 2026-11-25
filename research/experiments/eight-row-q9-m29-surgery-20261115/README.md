# (8,9) 8x29 bounded-edit witness surgery — 完全局所負（19インスタンス 0 witness）+ 8x28 witnessクラスタ34個

2026-11-15 高速レーン（純JS・SAT不使用）。前回 push の anchored window-SAT frontiers
（095c4d04、prefix 合意による条件付き閉包）の直接の続きとして、相補的な条件付け
「既知 witness 埋め込みからの有界編集距離」を導入し、(8,9) 前線 8x29 を攻めた。
手法は (7,5) m=38 two-edit surgery（ba89bc3e）の流儀に準拠（T' 未遮断セル・完全
場合分け・end-to-end 陽性対照・局所負であることの明示）。

## 主張

1. **m=29、s8x28 anchor 5配置（id/H/V/HV @ offX=0、H @ offX=1）から |P|≤2・|Rm|≤3
   （対称差 ≤ 5）の編集球内に 8x29 witness は存在しない**（完全列挙、各配置
   ~1.5M 葉点、全て非極大で棄却）。**局所負記録であり 8x29 の不在主張ではない**。
   M_{8,9} ∈ [29, 984]・前線 8x29 は不変。
2. **m=29、s8x27 anchor（offX=0,1,2）と s8x26 anchor（offX=0,1,2,3）から |P|≤2・
   |Rm|≤2（対称差 ≤ 4）の編集球内にも存在しない**（計 12 インスタンス、完全列挙）。
   T' はそれぞれ欠損行の自由列セル 2 個・3 個（w27 系: row 3、w26 系: row 4）。
3. **連続埋め込みの T' 構造（センサス）**: いずれの連続埋め込みも未遮断セルは
   欠損行の右端のみで、T' を通る曲線は行（7石）+ 円（≤4石）に限る:
   - s8x28→8x29: T'=(28,3)、行 y=3（7石・29点）+ 円4本（3,1,1,1石・9〜12点）
   - s8x27→8x28: T'=(27,3)、行 y=3（7石）+ 円4本（4,4,2,1石）
   - s8x26→8x27: T'=(26,4)、行 y=4（7石）+ 円4本（4,2,1,0石）
   円経由の遮断には |c∩P|−|c∩Rm| ≥ 5 が必要で |P|≤2,3 では構造的不可能 →
   本 bound での T' 遮断は「欠損行に +1 石」または「T' の占有」に尽きる
   （(7,5) の「row 0 に石を1つ追加に帰着」と同型）。
4. **帯内 witness の編集距離センサス**: 既知 witness ペア（8x26/27/28、全4鏡像
   変換込み）の最小対称差は 46（w26 HV→w27）、w27→w28 は 78。**witness 帯は小
   編集の連鎖では伸びない**（(7,5) の winA→winC が 2 編集だったのと対照的）。
   したがって本実験の局所負は「前線が遠い witness で破れる」可能性を排除しない。
5. **8x28 witness クラスタ（副産物）**: 既知 s8x28q9_rowY3 から石 (17,3) を除いた
   62石 seed からの (2,2) 手術で、**63石 maximal safe 配置 34 個**（既知 witness
   含む、新規 33 個）を 0.3 秒で完全列挙（output/cluster-m28-witnesses.json）。
   すべて既知 witness との対称差 ≤ 4。34 個全て js 検証（完全センサス安全 +
   極大）済み、サンプル 5 個（index 0,1,2,24,33、24 は既知 witness 自身）を
   verify_witness.py（exact Fraction・独立実装）で検証 ok。残り 29 個の py 検証は
   今後課題（各 ~39s）。構造データ: s8x28 の 63 石中 6 石はどの 8 石曲線上にも
   無い（free stones、b-ヒストグラム {0:6, 1:1, 2:36, 3:13, 4:5, 6:2}）。
6. **較正（0 ≠ 不在 の実証）**: 同一機械を m=28（seed=s8x27 埋め込み）と m=27
   （seed=s8x26 埋め込み）に適用すると (2,2) で 0。これらの盤には witness が
   存在するが距離 46〜80 であり、**局所 0 が不在を意味しないことを具体的に示す**。

## 機械（scripts/surgery.js）

seed（safe・非極大可）から F = seed ∪ P \ Rm（P は seed 空セル、Rm は seed 石）、
|P|≤maxP、|Rm|≤maxRm、|F|≤63=8(9−1)−1 を全列挙し、安全（全センサス曲線 ≤8 石）
と極大（F の全空セルがちょうど 8 石のセンサス曲線上）を検証する。63 石以下なら
鳩の巣により欠損行 ≤7 が従属し witness となる。剪定補題（すべて厳密）:

- **L1（安全=赤字被覆）**: F safe ⟺ 全曲線 c で |c∩Rm| ≥ cnt(c)+|c∩P|−8。
- **L2（除去石は赤字曲線上）**: 各 r∈Rm の穴は曲線 c'∋r（F でちょうど 8 石）で
  再ブロックされる必要があり、その c' は cnt(c')+|c'∩P|>8（赤字正）を満たす。
  ゆえに Rm ⊆ 赤字曲線上の石。
- **L3（T' 必要条件）**: 未遮断 seed セル t（P で占有されない限り）は
  cnt(c)+|c∩P| ≥ 8 なる曲線 c∋t を必要とする。

P 部分集合には安全の緩和剪定（cnt+adds+1−maxRm>8 で枝刈り）、赤字被覆 DFS は
スロット下界で枝刈り、被覆 Rm の真スーパーセットも独立の最終状態として走査する。
v1 では L3 が「t∈P（占有）の場合」にも課される過剰剪定があった（本インスタンス
では全 T' が欠損行上のため無害、CTRL-A/B で v1/v2 完全一致を確認済み）。v2 で
修正済み。決定性: RNG 不使用、実行は bit 再現可能（環境再構築後の再実行で
CTRL-A/B・全対象の同一結果を確認）。

## 検証（機械の健全性）

1. **CTRL-A（62石 seed = s8x28 − (17,3)、(2,2)）**: 34 witness を発見、既知
   s8x28q9_rowY3 を含む（index 24）。end-to-end 陽性対照。
2. **CTRL-B（61石 seed = s8x28 − (17,3),(4,0)、(3,3)、T'26セル）**: 同一 34
   witness 集合を発見（6.2M 葉点、38.6s）。多T'・大 bound での対照。
3. **py 独立検証**: クラスタ 5 サンプル + 既知 witness が verify_witness.py で
   ok（残り 29 個は今後課題として明記）。
4. **鏡像整合**: H@1（真の鏡像配置）の結果は id@0 と鏡像一致（T'=(0,3) vs
   (28,3)、いずれも 0 witness）。

## スコープと限界

- 本実験の全 0 結果は**編集球周りの局所閉包**であり、8x29 witness の不在主張では
  ない（較正 6 参照）。3 編集超・別基底の witness は排除していない。
- (3,3)（対称差 ≤ 6）は 230 秒の単一実行予算を超え、今回未実施。L3 を |P|<maxP
  の段階で前瞻的に課す改良があれば桁違いに高速化できる見込み。
- sa_machine_incremental.js（K0811 系 SA）の q=9 正制御は今回も負（8x26、
  seed 1-4 @100k iters・seed 1 @1M iters、全て best_n=64 で既知 63石 witness の
  再発見に失敗、~12s/M iters）。スクラッチ SA は (8,9) では下界探索器として
  機能しない。warm-start 修復型 SA は未試行のまま残る。
- window-SAT（095c4d04）との接続: 8x29 witness は (a) s8x28（±1 shift）と
  列 0..20 での一致が存在せず、かつ (b) 今回の s8x28 系 5 配置の sd≤5 球・
  s8x27 系 3 配置/s8x26 系 4 配置の sd≤4 球の外にあることが確定した。

## ファイル

- output/results.jsonl: m=29 19 インスタンス + 較正 2 の全 summary（再実行コマンドは各行頭の ### コメント）
- output/controls.jsonl: CTRL-A/CTRL-B summary
- output/cluster-m28-witnesses.json: 8x28 クラスタ 34 witness + 検証状況
- output/embeddiag.jsonl: 連続埋め込み 3 件の T' センサス詳細
- scripts/surgery.js: 手術機械 v2（chord-pair センサスは genfast3/sa_machine_incremental.js 系列の移植）
- scripts/embeddiag.js: 埋め込み診断
- seeds/: CTRL-A/B seed、s8x28 の 4 鏡像 seed
- 使い方: node scripts/surgery.js 8 9 29 seeds/seed_w28_id.json 2 3 63 [offX]

## 次の課題

1. (3,3) のための L3 前瞻剪定の実装と m=29 s8x28 系の sd≤6 完全閉包
2. クラスタ残り 29 witness の py 検証（各 ~39s・並列化可能）
3. H/V 鏡像 seed による両側 window-SAT（freeCols を左側にした掃引）
4. m=29 の def-mode SAT 直接評価（kissat 環境があるレーンでの実施が望ましい）

## 追記（同日・第2バッチ）

1. **クラスタ 34 witness の検証完結**: 新しい第2実装 verify_witness_int.py
   （純整数・exact・census 不使用、 Fraction なしで 39s→0.3s）を追加。相互検証:
   既知 band witness 3 個（s8x26q9_none / s8x27q9_rowY3 / s8x28q9_rowY3 — うち
   8x26/8x27 は canonical verify_witness.py でも追検証 ok）と canonical 済み
   クラスタサンプル 5 個のすべてで verify_witness.py と一致。残り 29 個を
   verify_witness_int.py で検証し、**34/34 全検証**（5 canonical + 29 int）。
   （output/intver-validation.json, output/cluster-m28-witnesses.json 更新版）
2. **m=30 probe**: 8x30 に s8x28 anchor（offX=0,1,2）で (2,2)/(2,3)（sd≤5）、
   s8x27 anchor（offX=0,1,2）で (2,2)（sd≤4）の計 9 インスタンス完全走査。
   **全て 0 witness**。T' は欠損行の自由列セル 2〜3 個（row 3）。8x30 も
   局所閉包（不在主張ではない）。M_{8,9} ∈ [29, 984] 不変。
   （output/results-m30.jsonl）
3. **両側 window-SAT についての対称性注記**: H 鏡像（x→28−x）は 8x29 盤の
   自己同型なので「H(s8x28) と列 k..28 で一致する witness 不存在」は
   「s8x28 と列 0..28−k で一致する witness 不存在」と同値。既報の
   window-SAT（右側自由列）により左側自由列の掃引は全て論理的に被覆済みで、
   新規情報はない。今後の作業から除外すべき。
