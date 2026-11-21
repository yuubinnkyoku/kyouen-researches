# Three-row q=4 frontier (M_{3,4} レーン・2026-11-21)

単一オーナー宣言: commit `72fdd106793151a72dcea5bcc9298577879188de`
（`research/log/2026-11-21-three-row-q4-stabilization-single-owner-note.md`・2026-11-21T02:14Z）。
3行 (w=3) 固定幅・q=4 の行欠損極大 witness band と witness-free 前線の確立。
K0070（M_{3,6}=9）・K0071（M_{3,5}=12）の妹分。安定化長は
M_{w,q} = least m0 such that P(m) for all m >= m0、
P(m) ⟺「3×m の全極大安全配置がちょうど (q−1)·3 = 9 石」（K1134/K1177 と同一の定式化）。

## 主張（有限機械検証の正確な範囲）

1. **witness band m=4..23 完全**: 各幅 m ∈ {4,...,23} に行欠損（ある行 ≤ 2 石）かつ
   極大な安全配置が存在する（def-mode SAT・kissat 4.0.4・20幅すべて決着・INDET 0）。
   witness は全20幅で2系統独立検証 PASS（後述）。代表 witness 石数: m=4: 5石,
   m=5: 6石, m≥6: 8石（= 満容量 9−1・行型 (3,3,2) の置換）。
   **従って M_{3,4} ≥ 24。**
2. **m=23 の判定は不足行固定の row-split 部分問題で取得**: `--rowY=Y`（行 Y を
   欠損行に固定）は不足行の所在で全状況を分割する case-split であり、
   行 0 と行 2 の部分問題は V 鏡映（y→2−y）でインスタンス同型なので行 0 側のみ
   見れば十分。`--lex=H`（列鏡映 lex-leader）は行を保存するので行固定との併用が健全。
   **(3,23,4) --rowY=1 --lex=H が SAT**（471,357 conflicts・106.83s・cap 285s に到達前に
   決着）し、witness（8石・行型 [3,2,3]・中央行欠損）を抽出。
   witness は plain board 上で sat.js verifyConfig (ok) + verify34.py (pass) の
   2系統検証を直接通るため、band 主張は witness 自身に立脚する（部分問題の意味論には
   依存しない）。
3. **m=23 の外側行欠損 witness が存在（分割で判定）**: 行0 欠損側の完全分割 − row-k
   piece（sat3 --rowY=0 --kex=0/1 の2件で r0=0/1 の32通り）と row-sum piece
   （sat4 rspec=(2,a,b) の16件）− は48通りのうち47通りを UNSAT で殺し、
   **piece (2,3,3) が SAT（1,004,683 conflicts）**: 8石 witness・rows [2,3,3]
   （行0が2石・coord `5:0,21:0,9:1,12:1,15:1,10:2,12:2,13:2`）。
   witness は sat.js verifyConfig（witness json の verify.ok=true）+ verify34.py
   （safe=1・maximal=1・deficient=1・rows [2,3,3]）の2系統で検証済み
   （(3,3,2) は (2,3,3) のV鏡像として交差 SAT 対照でも再生）。
   **m=23 では中央行・外側の両方の行欠損型の witness が存在する。**
4. **m=24 は witness-free（P(24) の有限機械証明）**: 安全配置では水平線（禁止曲線）
   のため各前行の石数 ≤ 3。従って行欠損極大配置の行和3つ組 (r0,r1,r2) は
   {0..3}^3 ∖ {(3,3,3)} の63通りを走る。これを **(i) row-k piece**
   （sat3 rowfixed-kex: --rowY=Y --kex=K・K∈{0,1}・行1はV不変で --lex=H,V・
   行0は --lex=H で行2はV同型から4件が48通りを被覆）と **(ii) row-sum piece**
   （sat4 rspec: 3行の石数の完全指定・12件〔決定打は (2,3,3) の 2,671,271
   conflicts・V鏡映で (3,3,2) も同時反証〕が残り7通りを被覆）で完全に分割し、
   **63通りすべて UNSAT・pending 0・uncovered 0**（`partition_closure.json`・
   exactly-once 検査つき）。**witness-free 幅は {24}。**
   m=24 plain/row-split の cap 下 INDET プローブ（481k〜1.60M conflicts・
   3レコード）は分割決着前の参考記録として records に残す。
   **M_{3,4} はなお [24, 69]**（P(m) の幅単調性は知られておらず、m=24 の反証は
   m≥25 に自動継承しない。witness band の終端 23 は確定）。
5. **m=25 以降は未掃引**: (3,25,4) plain は 115s cap 507,461 conflicts の INDET
   のみ。閉包の条件は witness-free 帯が 25..68 に達すること（69 = T_{3,4} は
   K0024 の全称側）。cap 下の conflicts は環境依存の参考値。
6. **上界は K0024 のまま 69**: K0024 十分長さ T_{3,4} = min(A,B) = 69。
   K0318 packing 境界を独立再計算（`curve_packing_fixed_width.py`・commit 49891aaf の
   正本をそのまま実行）すると **U_{3,4} = 69 = old_T** すなわち q=4 では packing 改善が
   生成しない（r=q−1=3 ゆえ d1 = C(2,3) = 0・cross_cost = C(2,2) − 1 = 0 で
   点対被覆項も三つ組余剰項も作用せず、整数最適化解 [x=18, y=30]・2x+y=66・U=3+66=69）。
   **従って M_{3,4} ∈ [24, 69]**（Γ 内側は open）。69 は閉包掃引目標幅。
7. **census 2実装交差検証**: sat.js（md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`）の
   buildCensus（JS・determinant 円生成・直線は点対）と、K0318 正本の curve_key リフト幾何
   を用いた独立 Python 実装（`pycensus.py`）が、m ∈ {4,5,6,7,8,10,13,16,20} の全9幅で
   **禁止曲線集合を byte-identical** で一致（曲線数 29/50/86/141/221/434/982/1865/3693・
   型・原始係数・点集合すべて）。
8. **小盤 (m ≤ 8) 完全分類（第三の独立系・全数列挙）**: `brute34.py`（安全集合を
   枝刈り DFS で全列挙し極大性・欠損性を分類）が m=4..8 の全極大安全配置を決定:

   | m | safe集合 | 極大総数 | 欠損極大 | 最大石数(満容量極大) | min deficient size |
   |---|---|---|---|---|---|
   | 4 | 1,199 | 182 | 182 | なし（全て欠損） | 5 |
   | 5 | 4,672 | 674 | 674 | なし（全て欠損） | 5 |
   | 6 | 16,992 | 1,724 | 1,724 | なし（全て欠損） | 5 |
   | 7 | 55,964 | 4,671 | 4,607 | 9石(3,3,3) ×64 | 5 |
   | 8 | 167,055 | 12,518 | 11,542 | 9石(3,3,3) ×976 | 5 |

   全幅で kissat の SAT 判定と brute の「欠損極大存在」が一致（符号化の両方向較正の
   うち SAT 側の全数照合）。満容量極大は m=7 で初出（64個）。
9. **境界幅の交差符号化陽性対照**: (3,12,4) と (3,22,4) の def-mode + --lex=H
   （列鏡映 lex-leader 節・別符号化）が双方 SAT（76 conflicts・178,116 conflicts@30s）。
   SAT 側の符号化独立性確認。
   さらに (3,23,4) --rowY=1 --lex=H,V の陽性対照が 173,883 conflicts で lexH 単独
   （471,357）と同一 witness を再生し、V 鏡映（中央行を固定）を行列併用した
   HV 符号化の健全性・有効性を較正した。
   **UNSAT 交差は m=24 分割の決着後に初めて可能になり、実施済み**: (2,2,2) と
   (3,2,3) の row-sum piece を --lex=H 単独の別符号化で再判定して同一 UNSAT、
   m=23 (2,3,3) SAT piece の V 鏡像 rspec (3,3,2) を別 CNF で再判定して SAT
   （V 鏡像 witness 再生）。3件とも records に交差対照レコードとして収録。

## 観察（予想として記録・未証明）

- witness band の石数が m ≥ 6 で一様に 8（= 満容量−1）で行型 (3,3,2) の置換であること、
  および m=4,5 のみ小 witness（5,6石）が現れることから、欠損極大の構造は
  「不足行の空点を残り2行の ≤6 石 + 円（各行 ≤2 点・全計 ≤6 点）で被覆する」
  一様パターンに乗っていると観察される。m=23 が被覆破綻の候補幅という予想は
  **計算で反証された**: m=23 では中央行欠損・外側行欠損の両方の 8 石 witness
  （rows [3,2,3] / [2,3,3]）が存在する。しかし **m=24 で行和63分割の全 UNSAT により
  witness band は 23 で終端**した: 8石被覆パターンは幅 24 以上では成立しない
  （有限機械証明）。被覆構造の分析（cover families A/B/C/D・master 判別式の
  exact-rational 恒等検証 `analyze_cover.py`/`verify_families.py`/
  `master_cover_identity.py`、S/X/Y 剰余パリティ補題の有限証明 `parity_lemmas.py`
  〔794円スキャン 0違反〕・`cover_analysis.json`〔21 witness の exact rational
  profile〕）はこの破綻の構造的理由の特定に向けた足場で、一般計数への昇格は次課題。
- 円は3行板上で最大6点（各行 ≤2）。q=4 では4点円が大量に存在するため CNF は重い
  （m=23 で禁止曲線 5,633・plain CNF vars 57,675・clauses 190,744・lexH vars 57,742・
  clauses 191,141・m=24 は禁止曲線 6,413・plain vars 65,594・clauses 216,922・
  row1+lexH vars 65,667・clauses 217,355・m=25 は禁止曲線 7,258・plain vars 74,163・
  clauses 245,245）。cap 未到着の決定インスタンスの conflicts は pinned kissat での
  再現対象、INDET の cap 下 conflicts は参考値。1幅ずつ cap を上げて INDET を縮める
  増分出版が現実的な前線進行法。

## 検証構造

- **器材 pin**: sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js
  `282ae832efa0080127c6c153e65e1c3c`（repo の four-row-q6-q7-frontier-20261121 lane
  正本を改変なし参照・w代入のみ）・kissat 4.0.4 linux-amd64
  `3a5eba830aa6008a604fcc9bbe99a325`（公式 rel-4.0.4 zip から再取得し同一 md5）・
  curve_packing_fixed_width.py（commit 49891aaf・K0318 正本）。
- **witness 2系統検証**: (i) sat.js verifyConfig（安全+極大・kissat model から抽出した
  石配置に対し ok:true）・(ii) verify34.py（K0318 curve_key 幾何の独立実装・
  安全=各禁止曲線上の石数 ≤ 3・極大=各空点が石数 ≥ 3 の禁止曲線上・欠損=ある行 ≤ 2
  の意味論で pass）。20/20 PASS（m=4..23）。
- **既知の落とし穴（透明性のため記録）**: verify34.py 初版は極大性を「曲線上の全点が
  石」と誤って実装しており、JS 側（kissat + verifyConfig）と判定が食い違った。
  正しい意味論は「曲線上の石数 ≥ q−1」で両系統ともこれに統一した。すなわち交差検証が
  本来は第三系統由来のバグを検出した事例。C の過剰要求は witness を誤って棄却する
  方向にのみ作用し、採用した witness 群への影響はない。
- **第二環境での独立再検証（2026-11-21 session3）**: 前セッション出版の分割
  16+18件+較正1件の計 **35 run を別環境で CNF 再生成・kissat 再実行し、全ピースの
  conflicts が出版台帳（partition_closure.py の R 表）と bit-exact 一致**
  （CNF は同一 pin 器材から同一符号化で再生成・md5 は records 参照）。被覆の完全性
  （63/63・48/48・exactly-once）は partition_closure.py の機械検査。m=23 外側 witness
  に verify34.py（第二系統）の別環境 PASS を追加し、両系統検証が完成。
  分析器 4本（analyze_cover・verify_families・master_cover_identity・parity_lemmas）
  も本環境で再実行して全 PASS（all_witnesses_cover_ok・2,124 checks 0 mismatch・
  S/X/Y 補題 machine-complete・794円 0違反）を再現。
- **records**: 67レコード（24 SAT + 35 UNSAT〔m=24 分割16件 + m=23 分割17件 + 交差
  対照2件〕 + 8 INDETプローブ）。決定インスタンスの conflicts は pinned kissat での
  決定論的再現対象、INDET の cap 下 conflicts は参考値。

## 出力

- `output/records.jsonl` — 全幅レコード（cnf md5・vars・clauses・verdict・conflicts・
  witness・両系統検証結果・row-split 部分問題レコード）。
- `output/brute_3x{4..8}_4.json` — 小盤全数分類（安全集合数・極大行型プロファイル分布・
  欠損極大数・最小 witness・代表 witness 座標）。
- `output/witnesses/wit_3x{4..23}_4.witness.json` — 各幅の抽出 witness
  （石数・座標・JS 検証結果）。m=23 は中央行系（wit_3x23_4）と外側行系
  （wit_3x23_outer_4・rows [2,3,3]）の2種。
- `output/partition_closure.json` — m=24 63-triple / m=23 外側 48-triple の
  完全被覆台帳（各 triple を殺す piece と conflicts・pending/uncovered 0）。
- `output/families.json` / `output/cover_analysis.json` — witness 被覆円の
  家族分類（A/B/C/D identity checks）と exact-rational profile。
- `scripts/` — census_dump.js・pycensus.py・verify34.py・extract_witness.js・brute34.py・
  sat3.js（rowfixed-kex piece 符号器）・sat4.js（rspec row-sum piece 符号器）・
  partition_closure.py（被覆台帳）・make_records.py（records 組立・決定打 (2,3,3) と
  交差対照3件を含む拡張版）・analyze_cover.py・verify_families.py・
  master_cover_identity.py・parity_lemmas.py。
  sat.js/sat2.js は重複を避けるため本 dir には含めない（上記 pin で four-row lane
  正本を参照）。

## 再現コマンド

    node scripts/sat2.js 3 M 4 --deficient cnf/def_3xM_4.cnf   # plain CNF
    node scripts/sat2.js 3 M 4 --rowY=Y --lex=H cnf/rowY.cnf   # row-split 部分問題
    node scripts/sat3.js 3 24 4 --rowY=1 --kex=0 --lex=H,V cnf3/k.cnf  # row-k piece
    node scripts/sat4.js 3 24 4 --rspec=0:2,1:3,2:3 --lex=H cnf4/s.cnf # row-sum piece
    kissat-4.0.4-linux-amd64 cnf/def_3xM_4.cnf                # rc=10 SAT / 20 UNSAT
    node scripts/extract_witness.js cnf/kis_out 3 M 4          # witness 抽出+JS検証
    python3 scripts/verify34.py 3 M 4 "x:y,x:y,..."           # 独立検証
    python3 scripts/brute34.py 3 M 4                          # m ≤ 8 全数分類

## レジューム（次回・着手前に必ず最新main再取得・宣言ノートの有効性を再確認）

1. m=25 の分割掃引: m=24 と同一の63分割手法を適用。piece は重くなる（決定打 (2,3,3)
   型は m=24 で 2.67M conflicts・476s なので m=25 では数倍が見込まれる）: 単独
   バックグラウンドで piece 毎に cap を吊り上げる単独バックグラウンド実行・増分出版は records 追記。
2. UNSAT が出た幅から増分出版（records・partition_closure 更新・1コミット/幅以上の粒度）。
3. 閉包: witness band が 23 で終端したので M_{3,4} = 24 ⟺ witness-free 帯が
   25..68の44幅すべてに達する（69以降は K0024 の全称側）。M が 24 より大きい場合は
   witness band が 24 以降のどこかの幅で再開する（P(m) の単調性はないので m≥25 の
   SAT可能性は m=24 の反証で排除されない）。
4. ブロッキング計数の定式化が書けた場合は予想として item に昇格（全称証明前）。
   m=24 で被覆破綻が確定した今、S/X/Y パリティ補題（parity_lemmas.py）と家族分類
   （families.json）を一般計数に繋ぐのが最有望の解析方向。行→幅の単調性（m=24 の
   反証が m≥25 に継承される条件・e.g. 列surgery）も未開拓。

標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま（本レーンは固定幅 w=3 で標準盤に無関係）。REFUTED-D10 は LOSS 証明ではない。
