# Three-row q=4 frontier (M_{3,4} レーン・2026-11-21)

単一オーナー宣言: commit `72fdd106793151a72dcea5bcc9298577879188de`
（`research/log/2026-11-21-three-row-q4-stabilization-single-owner-note.md`・2026-11-21T02:14Z）。
3行 (w=3) 固定幅・q=4 の行欠損極大 witness band と witness-free 前線の確立。
K0070（M_{3,6}=9）・K0071（M_{3,5}=12）の妹分。安定化長は
M_{w,q} = least m0 such that P(m) for all m >= m0、
P(m) ⟺「3×m の全極大安全配置がちょうど (q−1)·3 = 9 石」（K1134/K1177 と同一の定式化）。

## 主張（有限機械検証の正確な範囲）

1. **witness band m=4..22 完全**: 各幅 m ∈ {4,...,22} に行欠損（ある行 ≤ 2 石）かつ
   極大な安全配置が存在する（def-mode SAT・kissat 4.0.4・19幅すべて決着・INDET 0）。
   witness は2系統独立検証（後述）。代表 witness 石数: m=4: 5石, m=5: 6石, m≥6: 8石
   （= 満容量 9−1・行型 (3,3,2) の置換）。
   **従って M_{3,4} ≥ 23。**
2. **m=23, 24 は未決（INDET）**: (3,23,4) def-mode plain は 250s cap で 1,348,967
   conflicts 到達も判定なし。--lex=H 交差符号化も 250s cap 1,482,744 conflicts で
   判定なし。(3,24,4) plain は 100s cap 481,364 conflicts で判定なし。
   cap 下の conflicts は環境依存の参考値（決定インスタンスの bit-exact 保証対象外）。
   witness-free 幅はまだ1幅も確定していない。
3. **上界は K0024 のまま 69**: K0024 十分長さ T_{3,4} = min(A,B) = 69。
   K0318 packing 境界を独立再計算（`curve_packing_fixed_width.py`・commit 49891aaf の
   正本をそのまま実行）すると **U_{3,4} = 69 = old_T** すなわち q=4 では packing 改善が
   生成しない（r=q−1=3 ゆえ d1 = C(2,3) = 0・cross_cost = C(2,2) − 1 = 0 で
   点対被覆項も三つ組余剰項も作用せず、整数最適化解 [x=18, y=30]・2x+y=66・U=3+66=69）。
   **従って M_{3,4} ∈ [23, 69]**（Γ 内側は open）。69 は閉包掃引目標幅。
4. **census 2実装交差検証**: sat.js（md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`）の
   buildCensus（JS・determinant 円生成・直線は点対）と、K0318 正本の curve_key リフト幾何
   を用いた独立 Python 実装（`pycensus.py`）が、m ∈ {4,5,6,7,8,10,13,16,20} の全9幅で
   **禁止曲線集合を byte-identical** で一致（曲線数 29/50/86/141/221/434/982/1865/3693・
   型・原始係数・点集合すべて）。
5. **小盤 (m ≤ 8) 完全分類（第三の独立系・全数列挙）**: `brute34.py`（安全集合を
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
6. **境界幅の交差符号化陽性対照**: (3,12,4) と (3,22,4) の def-mode + --lex=H
   （列鏡映 lex-leader 節・別符号化）が双方 SAT（76 conflicts・178,116 conflicts@30s）。
   SAT 側の符号化独立性確認。UNSAT 側はまだ存在しないため UNSAT 交差は未実施。

## 観察（予想として記録・未証明）

- witness band の石数が m ≥ 6 で一様に 8（= 満容量−1）で行型 (3,3,2) であること、
  および m=4,5 のみ小 witness（5,6石）が現れることから、欠損極大の構造は
  「不足行の空点を残り2行の ≤6 石 + 円（各行 ≤2 点・全計 ≤6 点）で被覆する」
  一様パターンに乗っていると観察される。m=23 での被覆要求（不足行の空点 20 個を
  依然として6石側の円で賄う）が構造的に破綻する可能性が境界の候補理由だが未証明。
  証明候補は K1177 観察と同型のブロッキング計数（円の3行板上での局所形分類 +
  一般計数。K0077 が (4,m,8) で同種の「8点円の局所形」計数で m≥13 を閉じた実績あり）。
- 円は3行板上で最大6点（各行 ≤2）。q=4 では4点円が大量に存在するため CNF は重い
  （m=23 で禁止曲線 5,633・plain CNF vars 57,675・clauses 190,744・lexH vars 57,742・
  clauses 191,141・m=24 は禁止曲線 6,413・vars 65,594・clauses 216,922）。
  UNSAT 証明（あるいは witness 発見）は 1,000万 conflicts 規模になる可能性があり、
  1幅ずつ cap を上げて INDET を縮める増分出版が現実的な前線進行法。

## 検証構造

- **器材 pin**: sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js
  `282ae832efa0080127c6c153e65e1c3c`（repo の four-row-q6-q7-frontier-20261121 lane
  正本を改変なし参照・w代入のみ）・kissat 4.0.4 linux-amd64
  `3a5eba830aa6008a604fcc9bbe99a325`（公式 rel-4.0.4 zip から再取得し同一 md5）・
  curve_packing_fixed_width.py（commit 49891aaf・K0318 正本）。
- **witness 2系統検証**: (i) sat.js verifyConfig（安全+極大・kissat model から抽出した
  石配置に対し ok:true）・(ii) verify34.py（K0318 curve_key 幾何の独立実装・
  安全=各禁止曲線上の石数 ≤ 3・極大=各空点が石数 ≥ 3 の禁止曲線上・欠損=ある行 ≤ 2
  の意味論で pass）。19/19 PASS。
- **既知の落とし穴（透明性のため記録）**: verify34.py 初版は極大性を「曲線上の全点が
  石」と誤って実装しており、JS 側（kissat + verifyConfig）と判定が食い違った。
  正しい意味論は「曲線上の石数 ≥ q−1」で両系統ともこれに統一した。すなわち交差検証が
  本来は第三系統由来のバグを検出した事例。C の過剰要求は witness を誤って棄却する
  方向にのみ作用し、採用した witness 群への影響はない。
- **records**: 22レコード（19 SAT + 3 INDETプローブ）。決定インスタンスの conflicts は
  pinned kissat での決定論的再現対象、INDET の cap 下 conflicts は参考値。

## 出力

- `output/records.jsonl` — 全幅レコード（cnf md5・vars・clauses・verdict・conflicts・
  witness・両系統検証結果）。
- `output/brute_3x{4..8}_4.json` — 小盤全数分類（安全集合数・極大行型プロファイル分布・
  欠損極大数・最小 witness・代表 witness 座標）。
- `output/witnesses/wit_3x{4..22}_4.witness.json` — 各幅の抽出 witness
  （石数・座標・JS 検証結果）。
- `scripts/` — census_dump.js・pycensus.py・verify34.py・extract_witness.js・brute34.py。
  sat.js/sat2.js は重複を避けるため本 dir には含めない（上記 pin で four-row lane
  正本を参照）。

## 再現コマンド

    node scripts/sat2.js 3 M 4 --deficient cnf/def_3xM_4.cnf   # CNF 生成
    kissat-4.0.4-linux-amd64 cnf/def_3xM_4.cnf                # rc=10 SAT / 20 UNSAT
    node scripts/extract_witness.js cnf/kis_3xM_4.out 3 M 4   # witness 抽出+JS検証
    python3 scripts/verify34.py 3 M 4 "x:y,x:y,..."           # 独立検証
    python3 scripts/brute34.py 3 M 4                          # m ≤ 8 全数分類

## レジューム（次回・着手前に必ず最新main再取得・宣言ノートの有効性を再確認）

1. m=23, 24 の判定: cap を段階的に引き上げ（1幅/呼び出し・bash 外装 cap 240s 内）て
   SAT/UNSAT を確定。まず m=23 plain に 300s 規模を複数回…ではなく単一長 cap で
   （kissat は再開不可なので都度最初から）。SMT 的な rowY 分割（--rowY=Y で不足行固定）
   が SAT 側の探索分割として有効かもしれない（四行 lane の rowfixed モード）。
2. witness-free 帯の先上げ: UNSAT が取れた幅から増分出版（records 追記・1コミット/
   幅以上の粒度）。
3. 閉包: witness-free が m=69（=T_{3,4}）に達すれば M_{3,4} = onset として
   K0318×有限排除の K1182-precedent 接続で閉包（新K item）。
4. ブロッキング計数の定式化が書けた場合は予想として item に昇格（全称証明前）。

標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま（本レーンは固定幅 w=3 で標準盤に無関係）。REFUTED-D10 は LOSS 証明ではない。
