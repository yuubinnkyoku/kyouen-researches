# 6×25 q=6 frontier crunch — class-split SAT witness（2026-11-22 高速レーン・adopt+republish）

単一オーナー宣言: `research/log/2026-11-22-six-row-q6-m25-adopt-single-owner-note.md`（本採用セッション）
・元宣言（中断）: `research/log/2026-11-22-six-row-q6-m25-single-owner-note.md`（commit `2c3254ef9f`・2026-11-22T00:26Z）。

## 主張

1. **6×25 整数格子盤（q=6・q点共円/共線禁止・標準ルール）に行欠損の極大安全配置が存在する**:
   29石・行構成 [5,5,4,5,5,5]（class {2}・欠損行2・krow=2:4・minpos=11 分解インスタンス）の
   witness を SAT で発見・decode した。
2. したがって **(6,6) の witness 帯は m=25 まで伸び、M_{6,6} ∈ [26, 495]**（下界 25→26 の更新。
   上界は K0318 代入 U=495〔K0806〕不変）。K1215 の 6×24 witness を1幅延長し、
   6×24 レーンがfrontierとした 6×25 を解決（存在側）。
3. witness は 6×25 矩形上の D4+平行移動の意味で既知の 6×23 witness（K0818 正本アンカー）・
   K1215 の 6×24 class{1}/class{2} witness のいずれとも非合同（石集合正規化比較・機械確認）。
4. witness 側の追加構造観測: bbox 幅23で、正規化後の純並進配置は 6×23 / 6×24 / 6×25 の3幅すべてで
   極大安全（R(S)=25・crosscheck で 6×24 t=1 を Fraction 系で陽性再検証・同時に 6×24 t=0 と
   6×26 t=0 の追い出し〔not maximal (23,2)〕も一致）。R>25 への純並進被覆はなし。

## 来歴（adopt+republish・中断レーンの引き取り）

- 元セッション（宣言 `2c3254ef9f`・00:26Z）は class {1} の krow=1:0 分解、class {0}/{3}/{4}/{5}/
  {0..5} の plain 掃引（いずれも cap 到達 INDET・honest negatives）を実行した後、
  **class {2} の krow=2:4+minpos=11 分解で SAT witness（3,574,244 conflicts・00:47:37Z）を発見**し、
  決定性 rerun（00:52:05Z・conflicts 一致・model byte-identical）まで記録したが、
  その後 main への成果出版 없く中断した（最終 kit 記録時刻 00:52Z・01:36Z 時点で出版なし。
  中断 session の kit は `_q66-m25-crunch-kit`〔records 7行・enc/out・staged witness〕）。
- 本採用セッションは (6,5) 6×31 レーン（`bc11e28b`・adopt+republish の前例）に従い、
  staged witness を「候補」として引き取り、機材較正から全検証をやり直した上で出版する。
  採用側の検証は被採用成果に依存せず、CNF 再生成（byte-identical）と3回目のコールドランから
  全系統を再構築している（下記）。

## 被覆と走査状況

走査は行鏡映正準欠損クラス分割（K0818/K0819 と同一機材・全63非空クラスを35正準代表で被覆）。
本レーン（元セッション+採用セッション併せ）の 6×25 判定状況:
- class {2}（欠損行2）: **SAT**（krow=2:4・minpos=11 分解・3,574,244 conflicts）→ witness。
  plain/krow=2:4 固定は前レーンで 250s/260s INDET（K1215 記録どおり）。
- class {1}（欠損行1）: krow=1:0 分解 260s INDET（5,072,556 conflicts）。krow=1:1..1:3 分解は
  meta 生成までで未実行。plain/krow固定は前レーンで INDET。
- class {0}/{3}/{4}/{5}: plain cap 110..130s INDET（1,202,123/1,240,081/1,068,528/1,035,933 conflicts）。
- class {0..5} 全欠損: plain 110s INDET（828,368 conflicts）。
- **主張（下界更新）は class {2} の SAT 1件で確定**。上記 INDET は cap 到達の honest negative
  で不在を意味しない。残り未走査クラス・未実行分解の不在主張はしない。6×26 が新 frontier。

## 機材と pin

- `scripts/sat3.js` sha256 `e04581eb…` + `sat2.js` `14ceb854…` + `sat.js` `fcc0cfd8…`
  （K1215 の `six-row-q6-m24-class-split-20261121` 出版正本と byte 同一・sha256 照合済み）
- kissat 4.0.4 公式バイナリ（sha256 `21da5d984e38…aac93a1`・元宣言と同一 pin）
- `scripts/translate_census2.py`（sha256 `63373c5110…`）・`verify_py.py`/`verify_py_lib.py`
  （sha256 `0c21377650…`/`27c0f3ac…`・K1215 pin・知識kit側の import path 検証済み）
- CNF は保存しない（K1215 先例）。決定的再生成:
  `node scripts/sat3.js 6 25 6 --class=2 --krow=2:4 --minpos=11 ../output/<name>.cnf`
  → **CNF sha256 `46c485af2084f572b3cbdb17468a6d6fabbd59845f07c74a16ebbe6630c50643`**
  （vars 53,532 / clauses 187,536・採用セッションが再生成し中断レーンの CNF と byte-identical）。

## 検証プロトコル（すべて PASS のみ本主張）

1. **census gate**: `buildCensus` 曲線数が published アンカー
   (5,12,6)=212 / (5,15,5)=629 / (5,23,6)=996 / (5,27,5)=2355 に 4/4 MATCH。
   6×23 q=6 = 1,890・6×24 q=6 = 2,088（K1215 と同一）・**6×25 q=6 = 2,302（新アンカー）**。
2. **陽性対照**: 6×23 q=6 class{1} SAT・conflicts **77,932**（K0818 published アンカーと同一）。
   model v-line 全数 byte-identical・decode JSON が出版 witness（sha256 `766564994c…`）と
   byte-identical。
3. **陰性対照**: 2×9 q=4 class{0} UNSAT・conflicts 517（M_{2,4}=9 と整合）。
4. **決定性（3コールドラン）**: 中断レーン run1（00:47:37Z）+ rerun run2（00:52:05Z）+
   **採用セッション run3（01:43:04Z・新環境で CNF 再生性から全再構築）**。3回とも
   SAT・conflicts 3,574,244 一致・model 4,700 v-line 全数 byte-identical。
5. **witness 2系統検証**: (a) sat.js verifyConfig（decode 内蔵・整数）ok 29石 rows [5,5,4,5,5,5]・
   (b) verify_py.py Fraction 系 `safe_maximal` True 'ok' 29。**tamper 対照 4種**: 石移動×2 →
   not maximal (3,2)/(5,2)、石削除 → not maximal (0,0)、石追加 (0,0) → unsafe 6
   （追加石が q=6 共円を1本完成=極大性の帰結と整合）→ 検証器は fail loudly。
   アンカー再検証（出版 6×24 class{1}/{2}・6×23 witness）も Fraction 系で True ok 29。
6. **合同性分類**: D4像+全並進 embedding の石集合正規化比較で 6×23 witness・K1215 の
   6×24 class{1}/class{2} のいずれとも非合同（新規の石集合）→ `witness/congruence_vs_published.json`。
7. **高速並進 census の交差検査**: translate_census2.py（bbox幅23・maxOnCurve=5・R(S)=25・
   widths 23,24,25被覆・firstFail 26）と verify_py（Fraction）の4点照合:
   (a) 6×23 t=0 陽性一致・(b) 6×24 t=1 陽性一致（fast t_hit=1 と同 conclusion）・
   (c) 6×24 t=0 陰性一致（not maximal (23,2)）・(d) 6×26 t=0 陰性一致（同一理由）。

## 記録

- `output/records.jsonl`: 8行。中断レーンの7行（verbatim 採用: class{1} krow=1:0 INDET・
  class{0}/{3}/{4}/{5}/{0..5} plain INDET・class{2} SAT）+ 採用 run3 行（provenance フィールド付）。
- 生ログ: SAT 3件 `output/adopted_run1_*.txt`（中断L・443KB）・`output/adopted_run2_*.txt`（同上）・
  `output/run3_*.txt`（採用環境）。INDET honest negative 6件 `output/c6x25q6_{0,3,4,5}.txt`・
  `output/c6x25q6_0_1_2_3_4_5.txt`・`output/c6x25q6_1_x--krow=1:0.txt`。
  対照 `output/controls/ctrl_6x23q6_c1.txt`・`output/controls/ctrl_2x9q4_c0.txt`・
  `output/controls/census_gates.json`。enc meta 9件（file フィールドは各実行環境のパスを記録）。
- witness: `witness/w6x25_class2.json`（decode+verify・中断レーン staged witness と byte-identical）・
  `witness/census_class2.json`（並進census）・`witness/crosscheck_*.json`（4点）・
  `witness/congruence_vs_published.json`。

## 範囲と限界

- 有限機械計算。SAT 判定は witness 本体が2系統の独立整数/Fraction 検証で安全+極大を満たすので
  solver 健全性に依存しない（充填充足的証拠）。census は all-triples 構成で完全。
- 6×25 の witness-free 判定（=不在側）は本実験の対象外。残りクラス・分解除外の不在主張はしない。
- M_{6,6} の確定には 6×26..494 の持続性判定が残る（6×26 が新 frontier）。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。
  conflicts 数・nodes 数を勝敗として読まない。

## 再現

```sh
# census gates（scripts/sat3.js と同dirに sat.js/sat2.js 必須）
node -e "const S=require('./scripts/sat.js');for(const[t,w,m,q,e]of[['5x12q6',5,12,6,212],['5x15q5',5,15,5,629],['5x23q6',5,23,6,996],['5x27q5',5,27,5,2355]])console.log(t,S.buildCensus(w,m,q).curves.length,e);console.log('6x25',S.buildCensus(6,25,6).curves.length)"
# 主インスタンス（再生成 CNF sha256 46c485af…）
node scripts/sat3.js 6 25 6 --class=2 --krow=2:4 --minpos=11 out.cnf
kissat out.cnf   # SAT / 3,574,244 conflicts（決定性）
# decode + 2系統検証
node scripts/sat3.js decode 6 25 6 kissat_log.txt --json=witness.json
python3 scripts/verify_py.py   # extended.json = witness/extended_verify_input.json から
# 並進census
python3 scripts/translate_census2.py witness/w6x25_class2.json 6 70
```
