# SATによる行欠損極大witness探索 — 4組の下界更新と候補予想の反証（2026-11-14）

## 概要

K0808/K0809 の貪欲・行capハンディキャップ探索では発見できなかった m 帯に行欠損極大witnessが
実際に存在することを、自作SAT（CDCL）探索で示した。
(6,5)/(6,6)/(6,8)/(5,6) の4組すべてで、K0809 が候補予想として挙げていた
M=22/17/12/16 を反証するwitnessを発見・独立検証した。

## 主結果（すべて独立検証 PASS: safe + maximal）

| (w,q) | 満容量 | 新witness（石数@盤） | 旧下界 | 新下界 | 上界 |
|---|---|---|---|---|---|
| (6,5) | 24 | 23石@6×22 | 22 | **23** | 658 |
| (6,6) | 30 | 29石@6×17・6×19 | 17 | **20** | 495 |
| (6,8) | 42 | 41石@6×12..6×17（6m連続） | 12 | **18** | 371 |
| (5,6) | 25 | 24石@5×16・5×17 | 16 | **18** | 249 |

追加: 6×12・q=8 には 40石の極大安全配置も存在する（cap=40 SAT・独立検証 PASS）。
**さらに cap=39 も SAT（39石・行構成 5,7,7,7,6,7・独立検証 PASS・
別プロセス再検証 PASS）であり、6×12 q=8 の最小極大サイズは ≤39 に更新される**
（cap=38 は2回試行して timeout・不在証明ではない。下界は未確定のまま）。
(5,7) m=19 と (6,7) m=20 は本バジェットでは未解決（timeout・非不在）。

## 手法

`scripts/row_deficient_sat.js`:

- **census**: 危険曲線（≥q点を含む直線・円）の完全列挙。直線は全点ペアの
  正準整数係数 (a,b,c)、円は全3点組の Cramer 整数解 (A,B,C,D)
  （A(x²+y²)+Bx+Cy+D=0・gcd正規化・符号正準化）。全整数厳密演算。
  完全性: ≥q≥4 点の円は必ず非共線3点組を含む（円と直線の交点は≤2）ため
  3点組列挙で網羅される。≥q 点の直線はペア列挙で網羅される。
- **SAT符号化**: 各セルに変数。各危険曲線に sequential ≥-counter（s[i][j] ⟺
  「先頭i点中≥j石」・レベルqまで）を1本だけ作り、
  safety（¬s[n][q]・つまり ≤q−1石）と blocking（s[n][q−1] ⟺ ≥q−1石）の両方に使う。
  極大性: 各空セル c について「cが石 ∨ cを含む何らかの曲線が ≥q−1石」。
  欠損条件: safety が各行を ≤q−1 石にcapするので、「全ての行が ≥q−1 石」の否定
  （=ある行が ≤q−2 石 ⇔ 全体 ≤ w(q−1)−1 石）を**単一節**で符号化
  （`row-deficient` モード。TOTAL計数器モードも --cap で使用可）。
- **ソルバ**: 自作CDCL（watched literals・VSIDS・1UIP学習・Luby的再起動・
  5000競合ごとの学習節削減）。独立系の単純DPLL（計数ベース単伝播・chronological）も
  内蔵し、制御で相互検証。
- **独立検証**: census不使用。石ペアの直線・石3点組の円を全列挙して
  safety・maximality・行石数を厳密判定（K0808 と同じ原理・独立実装）。

## 制御（全PASS）

- 6×12・q=8 census: 6直線 + 86円（各ちょうど8点）= **92曲線** — K0809 のcensus 92 と一致。
- 2×8・q=4: SAT・5石witness・独立検証 PASS（K0796 の5石witness帯の再発見）。
- 2×9・q=4: UNSAT（CDCL）+ UNSAT（DPLL）+ 全列挙（欠損極大0）→ M_{2,4}=9 制御。
- 2×8 全列挙: 欠損極大16個・最小5石（K0796 一致）。
- ソルバfuzz: 乱数3-SAT 400題 × 2ソルバ vs 全列挙: **800検査・不一致0**
 （SAT model全検証・UNSAT全照合）。
- 全11 witness を別プロセスで再検証: safe+maximal PASS・記録と行石数完全一致。

## 実装上の注意（本実験で実際に捕捉したバグ）

1. sequential counter の j≤i 場合の S→Sp∨(x_i∧Spp) を1節に圧縮すると
   機能的完全性が壊れる（S→Sp∨x_i と S→Sp∨Spp の2節が必須）。
   圧縮版では非極大な「witness」をSATが返した（2×8制御で検出）。
2. DPLL の衝突時早期 return は計数器の更新対称性を壊す
 （衝突節より後の節の加算が抜け、undo が二重減算する）。
   衝突フラグ方式に修正（乱数3-SAT fuzz の claimed-SAT/真UNSAT 不一致で検出）。
3. CDCL の決定レベル配列（lim）への push 忘れは「すべてレベル0」化し
   最初の衝突で偽UNSATを出す（2×8制御・fuzzで検出）。
4. 円のCramer整数解の係数は det 倍で (A,B,C,D)=(det,−B,−C,−D)（d の符号に注意。
   単位円制御で検出）。

## 非発見と未解決（不在証明ではない）

- timeout: (6,8) m=18・(5,6) m=18,19・(5,7) m=19（2回）・(6,7) m=20（2回）・
  (6,6) m=18,20,21・6×12 q=8 cap=38,36。いずれもCDCL予算切れで不在を意味しない。
- 6×12 q=8 の最小極大サイズは **≤39**（cap=39 SAT・39石witness独立検証 PASS。
  cap=38 は2回試行で未解決・不在証明ではない。下界は未確定）。
- UNSAT（不在証明）は本実験では1つも得ていない。下界更新のみ。

## 解釈

K0809 の5件の候補予想（M_{6,5}=22・M_{6,6}=17・M_{6,8}=12・M_{5,6}=16・M_{5,7}=19）のうち
4件が反証された。貪欲系探索の「非発見 m」は実際の不在と系統的にズレており、
SAT探索は同じ盤で数十秒〜数分で witness を発見した。
(6,8) では 6×12..6×17 の6連続で witness が存在し、難度は m に対して非単調
（6×16: 4331 conflicts vs 6×17: 242,874 conflicts）。

## 再現

```sh
node --max-old-space-size=2500 scripts/row_deficient_sat.js sat 6 22 5     # row-deficient (default)
node scripts/row_deficient_sat.js sat 2 9 4 --dpll                          # DPLL cross-check
node scripts/row_deficient_sat.js census 6 12 8
node scripts/row_deficient_sat.js brute 2 8 4
node scripts/row_deficient_sat.js sat 6 12 8 --cap=40                       # total-cap mode
```

出力: `output/sat_results.json`（全16実行・witness座標・独立検証詳細・
fuzz/制御記録・timeout記録）。

## 関連

- K0810（knowledge item）・K0808/K0809（貪欲系の既往witness）・
  K0806（上界）・K0796/K0069（2行制御）・K0759（5×19 完全列挙）
