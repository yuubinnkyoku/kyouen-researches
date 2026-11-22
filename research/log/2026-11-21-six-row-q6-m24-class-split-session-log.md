# Session log: six-row (6,6) m=24 class-split witness band extension（2026-11-21/22 高速レーン）

- 単一オーナー宣言: `research/log/2026-11-21-six-row-q6-m24-class-split-single-owner-note.md`（commit `12012dd3`・宣言時 HEAD `64f2d6490`）
- 成果物: `research/experiments/six-row-q6-m24-class-split-20261121/`（37ファイル+manifest）
- K item: `K1215`（(6,6) witness band m=24・M_{6,6} ∈ [25,495]）
- CSV: `results/fixed-width/mwq_stabilization.csv` (6,6) 行の M 列 24..495 → **25..495**・note/source 追記

## タイムライン（UTC）

1. **23:06時点の main `64f2d6490` を確認**（AGENTS.md・knowledge README 末尾〔K1213〕・CSV・並走宣言との
   disjoint を確認: five-row (5,4) m45〔`59b1251aa7`〕・five-row sd(4,3)/(3,4)〔`0b2a6466`〕・
   n11 third-impl bank recalib〔`451e0fe8e4`〕・seven-row m69〔`c476182ae8`〕はいずれも 6×24/q=6 非接触）。
2. K0818 機材を特定（`six-row-q8-m20-class-split-20261114/scripts/`・m19 実験report と照合で
   `sat3.js` が byte 同一・sat2.js/sat.js pin 確立・6×23 q=6 class{1} SAT 77,932 conflicts という
   bit-exact アンカーと 6×26... の vacuum 2×9 陰性対照 517 を発見）。
3. **23:50 宣言出版**（commit `12012dd3`）。
4. **ゲート**（all PASS）: census gate 4/4 MATCH（(5,12,6)=212・(5,15,5)=629・(5,23,6)=996・(5,27,5)=2355）
   ・陽性対照 6×23 class{1} SAT conflicts 77,932 = 出版アンカー bit 一致・decode 石集合 = 出版 witness
   （後述のとおり JSON 全体も byte-identical と判明）・陰性対照 2×9 UNSAT 517 bit 一致・
   Fraction 系 witness/tamper 検証 PASS（tamper→unsafe 6）。
5. **6×24 class-split 走査**: {012345} 120s INDET 924,268（honest negative）→
   **{2} SAT 404,422 conflicts（95s）・{1} SAT 1,837,912 conflicts（232s）で 29石 witness ×2**。
   ここで主張が確定（下界 25）したため残り32クラスの UNSAT 掃引は不要として打ち切り
   （不在主張はしない・M の下界更新のみを主張）。
6. **検証**: 両 witness decode→sat.js verifyConfig ok（rows [5,4,5,5,5,5] / [5,5,4,5,5,5]）→
   Python Fraction 系 true ok 29、tamper 2件 false unsafe 6 →
   D4+全並翻訳 embedding の石集合合同性分類で m=23 witness・相互とも非合同（K1206 教訓の実施）→
   2回再実行で conflicts bit 一致（決定性）。
7. **並進 census（R(S)）**: 初版 Fraction 直接実装は1試行数十秒で 300s bash cap 超過・実行環境
   リセット（23:55前後。kit は knowledge 直下で全成果残存）。BLOCKED 前計算の整数版
   `translate_census2.py` に置換（2.4s/全体）→ 両 witness とも R=24（22/23/24 の3幅 witness・
   25で停止）。crosscheck 4点で verify_py と一致（陽性 (23,t=1)・陰性 (25,t=0) not maximal (22,1)）。
8. **6×25 ラダー**: {1}/{2} plain 250s INDET（1,222,228/1,207,894）・krow固定(k=4) 260s INDET
   （1,126,385/1,294,221）→ 6×25 未決着・honest negative として記録（不在不主張・他33クラス未走査）。
9. **出版**: 実験dir 37ファイル+MANIFEST.sha256 → K1215 item → CSV (6,6) 行更新 →
   knowledge README bullet。

## 数値まとめ

| 対象 | 結果 | conflicts | 備考 |
|---|---|---|---|
| census gate (5,12,6)...(5,27,5) | 4/4 MATCH | - | 6×24q6=2,088・6×23q6=1,890 |
| ctrl 6×23 q6 class{1} | SAT | 77,932 | 出版 K0818 アンカー bit 一致（×2実行）・decode byte-identical |
| ctrl 2×9 q4 class{0} | UNSAT | 517 | ×2実行 bit 一致 |
| 6×24 q6 class{2} | **SAT** | 404,422 | witness rows [5,5,4,5,5,5] 29石（×2実行 bit 一致） |
| 6×24 q6 class{1} | **SAT** | 1,837,912 | witness rows [5,4,5,5,5,5] 29石（×2実行 bit 一致） |
| 6×24 q6 class{012345} | INDET | 924,268 | 120s cap・honest negative |
| 6×25 q6 class{1}/{2} plain | INDET | 1,222,228/1,207,894 | 250s cap |
| 6×25 q6 class{1}/{2} k4固定 | INDET | 1,126,385/1,294,221 | 260s cap |
| 並進 census | c1: 22@t0,23@t1,24@t2 / c2: 22@t0,23@t0,24@t1 | - | R=24 で停止・crosscheck 4点一致 |

## 事故・運用知見

1. **driver tag衝突バグ**（詳細は実験 README erratum）: --krow 引数が CNF/log の tag に反映されず
   plain CNF を再利用した誤ラベル records 2行を混入→records から除外・driver 修正・生ログは事故記録として残置。
2. **低速検証器の落とし穴**: Fraction 全走査（translate_census v1）は1試行あたり数十秒で
   bash cap 300s を超え実行環境リセットを起こす。数個の判定に fusible なのは BLOCKED 前計算型
   （整数正規化曲線キー・covariant）で、同一論理の verify_py との交差検査を必須とする設計。
   *環境リセットを1回経験したが、kit が knowledge 直下だったため成果は全て残存*（移設設計が効いた）。
3. knowledge 配下は fuse マウントで noexec: 実行バイナリは workspace 側に置き、スクリプトは
   `node`/`python3` の引数として起動する分には影響なし。
4. 6×23 対照の decode --json 出力は出版 `positive_control_6x23_class1_witness.json` と**byte-identical**
   （sha256 `76656499…`）: decode→witness の全経路が出版正本に一致する通常より強いアンカー。

## 引き継ぎ（次回レーン・着手前に必ず最新main再取得・hourly並走に注意）

1. (6,6) 6×25 の追い込み: {1}/{2} とも cap 内未収束。--krow k∈{0..3} 拍分解と minpos split、
   残り33クラス走査、または m=24 witness からの bounded surgery（five-row の surgery4.js 系の
   6行移植）。SAT なら M ≥ 26 のもう1段。
2. 6×24 の「witness-free」側（残32クラス UNSAT 判定）は M 確定に必要ないが、帯内部の
   欠損構造把握（どのクラスに witness があるかの全数確定）には有用。
3. (6,5)/(6,7) 前線（6×31/6×22）は未着手。同機材で即時参戦可。
4. 器材: `/home/user/knowledge/kyouen-research/_q66-m24-lane-kit/`（pub-stage/=repo刊行物と同一byte・
   enc/ に CNF 6件〔未刊行〕・records/生網走は全て kit 内）。CNF は刊行していない
   （`node sat3.js 6 24 6 --class=D` で決定的再生成）。

**標準11×11空盤・二石root・S2・class 1/2/4は本レーン非接触でUNKNOWNのまま。
conflicts数・cap到達数を勝敗として読まない。**
