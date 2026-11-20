# 2トークン残余ゲーム y=12族 全称証明: 正本検証器14機械チェック part1+part2（K1152 fit の正本監査・observed→proved 昇格）

- 実験名: vertical-fiber-two-token-y12-parametric-allz-proof-20261120
- 対象族: H(R; (x,12); z), z >= 0, x >= 12, R >= 0（標準 11×11 とは無関係の数学的残余ゲーム族）
- 対象item: [K1152](../../knowledge/items/K1152-two-token-y12-parametric-closed-form-fit.md)（fit・status: observed・その正本監査段階が本実験）
- 単一オーナー宣言: [2026-11-20-y12-universal-verifier-single-owner-note.md](../../log/2026-11-20-y12-universal-verifier-single-owner-note.md)（commit d345c645・2026-11-20T17:03:31Z・K1152 fitレーンは自宣言で全称段階を保持範囲外と明示済み）
- 実行環境: Python 3.12.14 標準ライブラリのみ・cgroup RAM 上限 1,090,519,040 bytes（約1.0 GiB）・2コア・x86_64

## 機械構成（verify_y12_universal.py・part1出版時 SHA-256 f73614f7…36,170 bytes・commit 60622f35 → part2拡張版 SHA-256 e209297603f68c9a82a50f90cac0bc678211d1517f137b5d490dfca3c492eb04・49,295 bytes・1,287行）

y=11 正本検証器（K1143 part1・verify_y11_universal.py SHA-256 c57baf5c5270c47ef9f29cc390a2d2eb6b18de438f576aa8f5e94264e3fd8c6b）と
出版 cand12.py（K1152 fit・SHA-256 79e588b3d44bada83355676d9da1db559c57167574ed58ce118ef3c897149131）から機械的に組み立て。
転写は行単位で照合済み:

1. 生 2エンジン（H_ordered/H_canonical）+ K0832 単一トークン表 single_token + mex: y11 正本から 77 行 verbatim。
2. cand11 ブロック（B子・x=12 合流子 (11,12)≡(12,11) の子値）: y11 正本の cand11 ブロック 102 行を
   ブロック内 Y→Y11 改名のみで転写（改名以外の差 0 行・Y11 = 11 併置で cand12 ブロックの Y = 12 と共存）。
3. cand12 ブロック: 出版 cand12.py から fit driver（main()）と docstring を除く 92 行 verbatim（差 0 行）。
   ブロック内 q_odd/single_token_val/_bk の重複定義は y10/y11 検証器と同じくブロック毎に併置（最終定義が呼び出し時点で有効）。
4. これ以外（docstring・imports・opts12・型機械・12チェック・census runner・main）は本実験のために書かれた y=12 機械本体。
   x=12 合流子: opts12 で A子 = cand11(z,12,R-1)（B子と同値・多重集合として (11,12)==(12,11)）、
   C子 = 1 xor cand12(z-1,x,R-1)。
5. 型機械: clip 窓 2y+2 = 26・番兵 ±27（8族連続 tight 候補・y=5..11: 12/14/16/18/20/22/24 に続く）、
   tail x+z+13・merge x<=z-13 は corollary として機械照合。

## 12チェック構成と実行結果（overall PASS・total_points 6,311,993・total_bad 0）

| check | 内容 | points | bad |
|---|---|---|---|
| C1 | 両生エンジン vs cand12・z=0..14・x=12..30・R<=x+z+47 | 21,660 | 0 |
| C1b | K0832 単一トークン raw anchor・出版 cand11（y=11族=B子）raw anchor・x=12 合流子 (11,12)≡(12,11) raw anchor | 41,666 | 0 |
| C2 | 閉形式恒等式格子 z=0..48・x=12..57・R<=x+z+41（merge/tail 併合） | 224,273 | 0 |
| C2b | 深tail行 z∈{60,72,84,96,108,120,240,400}・R>=x+z+13 で (x+12) mod 2 | 18,964 | 0 |
| C3 | 選択肢分解の生エンジン子列挙照合 z=0..5・x=12..16 | 1,125 | 0 |
| C4 | 型機械 box ±60（clip 26/番兵27）・(value, sorted子) 完全収束 | 616,484 | 0（C4時点 181,374 型） |
| C4t | tightness probe clip 25/番兵26: 3,540 収束違反・最初 (60,88,88) → clip 2y+2=26 が tight | 616,484 | （bad 総計外・情報提示） |
| C7 | シード 20261132・200k 点・z,x<=3000 | 200,000 | 0 |
| C8 | 境界多様体 z<=3000・dx∈[-26,16]・tail 窓 | 890,765 | 0 |
| C9 | v空間シェル [61,64]/[89,92]/[117,120] | 915,654 | 0 |
| C11 | 生 census アンカー z=0..79・x=12..70・R<=x+z+13・両エンジン（後述） | 892,080 | 0 |
| C12 | 深格子 z=0..120・x=12..120・R<=x+z+16 | 1,872,838 | 0 |

- corollary merge（x<=z-13 → single_token(x+12,z,R)）: 1,417,623 点・不一致 0
- corollary tail（R>=x+z+13 → (x+12) mod 2）: 232,510 点・不一致 0
- 型総数（全チェック終了時）: 191,789
- **C4t で clip 25 では 3,540 点の収束違反（最初の違反 (60,88,88)）があり、clip 2y+2=26 が tight。2y+2 clip tight は 8 族連続（y=5..12: 12/14/16/18/20/22/24/26）**

## C11 census の bounded-memoization twin 設計（本実行ホストの 1 GiB cgroup 制約への適合）

census box（446,040 点/エンジン）を無制限 memo の生エンジンで 1 プロセス実行すると、
再帰キャッシュが cgroup 上限（約1.0 GiB）を超えて OOM kill する（前身試行で exit 137・maxrss 996MB を実測・
行ごと cache-clear 版は 300 秒コマンド上限を超過）。そこで本機は:

1. **bounded-memoization twin**: 出版生エンジンの code object を module globals の浅い複写に再束縛し、
   再帰参照（H_ordered/H_canonical 名）を LRU 上限 1,600,000 のキャップ付きキャッシュへ張り替えた双生機。
   再帰定義の byte は正本と同一（types.FunctionType + globals 複写）で、決定的純関数の memo化は透過・
   LRU 追い出しは固定訪問順の下で決定的。したがって値は出版エンジンと厳密一致し、上限は residency のみ制限。
2. **engine 別コマンド分割**: `C11ordered` / `C11canonical` 各コマンドが census 一式（446,040 点・twin cache・
   merge/tail corollary 併合）を実行し `output/census-<engine>.json` を書く。実測: ordered 13-15秒・canonical 15秒・
   各 maxrss 約 550-563MB（cgroup 上限内・余裕あり）。
3. **fail-closed merge**: `C11` モードは両 part ファイルを読み、engine 名・box 表記・cache 上限・
   点数 (= census 幾何からの再計算期待値 446,040・merge 161,700・tail 4,720 を全て公式から再計算して照合)・
   bad==0 を検証した上で merge し audit の C11 に記録。part ファイル欠落・1 点改ざん・corollary 改ざんは
   全て fail-closed（SystemExit・監査不成立）で捕捉。
4. 無制限 verbatim エンジンは引き続き C1・C1b・C3・C2/C2b 等の生アンカーを担う（本 box を除く全域で
   residency は上限内に収まる）。

## 決定性（3回実行 byte-identical）

- audit.json: run1（同一cwd）→ run2（同一cwd再実行）→ run3（隔離 tree/cwd/HOME + PYTHONHASHSEED=random）の
  3 実行とも byte-identical（SHA-256 7dcc4505b270596b7cef7e395761b1741f54edb74b4732efb1d64b1ac78249db・3,141 bytes）。
- census-ordered.json: run1/run2/run3 全て byte-identical
  （SHA-256 195670f0c90aecaf0a1d5dc4ac5b1fdb2bd026cc8df6b0f84badee62b4873008・486 bytes）。
- census-canonical.json: 同様に byte-identical
  （SHA-256 af4111f8b6f7f18f0488d09beb468a9abaeb983ecd1cd4991b4888af255af4e4・488 bytes）。
- 監査は時刻・実行時間・パスを含めない。seed 固定・sorted keys。
- 付帯確認: 検証器ドキュメント内の cand12 SHA-256 表記は実 byte 再計算値（79e588b3…131）。

## fail-closed 検査（census part 経路・出版前に実施）

1. census-ordered.json の points を 446,040→446,039 に改ざん → `FAIL-CLOSED: census points 446039 != 446040`。
2. corollary merge 点数を 1 に改ざん → `FAIL-CLOSED: census merge corollary mismatch`。
3. census-canonical.json を一時退避（欠落）→ `FAIL-CLOSED: census part file for engine 'canonical' is missing...`。
   （いずれも監査不成立で PASS 出力なし。改ざん後は正本を復元し再実行で PASS・byte-identical を確認。）

## part2: C1d 出版切片アンカー + 独立 census 消費者（2026-11-20 追加・observed→proved 昇格段階）

part1 出版（commit 60622f35）で残した昇格工程（K1143/y=11・K1141/y=10 と同一手続き）を実行した。
検証器は part1 正本を in-place に拡張（テンプレート再生成・検証器本文は 12 チェック構成から変わらず
C1d/C11r の 2 チェックが追加。anchor block は y=10 part2 正本検証器〔SHA-256 f9169449…・3 回
byte-identical 監査 41b7a315…〕から 238 行 verbatim 抽出・`Y` は関数ローカル変数のみで
y=11/y=12 ブロックと干渉しない）。part1 の 12 チェックの byte は不変（census part
能力は出版 byte と同一・part2 実行で census-ordered/census-canonical は part1 出版 byte
〔195670f0…/af4111f8…〕のまま再確認）。

### C1d（出版固定 z 切片アンカーの y=12 特殊化・139,860 点・bad 0）

出版 uniform closed form（z=8: K0999/K1000〔verify_z8_y_ge9_proof.py SHA-256 e88e5ea7…〕・
z=9: K1001〔db1d60c6…〕・z=10: K1011 〔42db00b2…〕・z=15/16/17:
K1065/K1077/K1087〔131e1c64…/d07c3b0e…/e49d24d2…〕）のアンカー関数 A8u..A17u を
x=12..159・R<=x+61 で y=12 行（引数 (x,12,r)）と cand12 が一致することを機械照合
（内訳: 6 z0 × x=12..159 × R=1..x+61 のアンカー掃引 130,092 点
＋出版低 R 単一トークン縮約 R<=z+6（z0=15,16,17）の y=12 行照合
〔cand12 vs single_token(x+12,z0,R)〕9,768 点。y=10 part2 の 130,950+9,900=140,850 点構成の鏡像）。
**組み込み前事前検証（fail-closed）**: 各 z0 について x=12..45・R<=x+z0+30 の
14,484 点を出版アンカー×H_ordered×H_canonical×cand12 の 4 方照合で不一致 0
（z 別 2,261/2,295/2,329/2,499/2,533/2,567）・低 R 縮約 9,768 点も不一致 0・約 2.2 秒
（`scripts/preflight_c1d_y12.py`・結果 `output/preflight-c1d-y12.json`・SHA-256 7562b8dd…・2 回実行
byte-identical。y=10 でこの段階が K1087 転写初稿の評価順バグ 170 点を捕捉した実績があり、
本族ではアンカーは y=10 正本からの verbatim 再転写のため三者照合で初めから一致）。
z=15/16/17 の (y,d) 過渡セルと S<17/S==17 分岐は y=12 で到達不能（S=x+12>=24）。

### C11r（独立 census 台帳消費者・450,760 点・bad 0・fail-closed）

census_rows.py（y=12 版・第三実装）が z=0..79・x=12..70・R=0..x+z+14 の 4,720 行
（450,760 点・値0点 225,361・エンジン状態計算〔LRU misses〕6,121,227・約 13 秒・maxrss 約 556MB）の
行ごとの Thue-Morse 指数・値2/値1台帳（T/P 集合）・tail を出力した census.txt
（828,655 bytes・4,720 行＋空行 80・SHA-256 67e48cbeae46c061b1393fbfd863431b7fbfd48b631e5a8de569a675fb0b331b。
tail アサート R>=x+z+13 の (x+12) mod 2 全行成立）。C11r は census.txt の全行を
cand12 から再導出して T/P 集合・idx・tail を照合する（行重複・欠落・rows != 80*59・
終端改行なしは FAIL-CLOSED）。census_rows.py の本体は y=5..y=10 出版版と同一の
生 tuple 二重再帰で、本実行ホストの 1 GiB cgroup 制約のみ LRU 上限 1,600,000
（CENSUS_CACHE_MAXSIZE）として明示キャップ（docstring 記載）。決定的純関数の
memo 化は透過で、LRU 追い出しは固定訪問順の下で決定的。

### part2 フル監査（14 チェック・overall PASS・total_points 6,902,613・total_bad 0）

C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12 を 1 コマンドで実行:
C1d 139,860 点・C11r 450,760 点が part1 の 6,311,993 点に加算され
**total_points 6,902,613・total_bad 0・型総数 191,789**（C4t は情報提示で bad 総計外）。
merge corollary 1,417,623 点・tail corollary 232,510 点は part1 と不変のまま bad 0。
audit.json（3,673 bytes・SHA-256 6bca3fa27b1490ea2bb10d39dd9a4c916359b6888c9d0e961c790db7954b8229・
stage 文言は part2）。

### 決定性（part2・3 実行 byte-identical)

run1（同一cwd）→ run2（隔離 tree/cwd/HOME + PYTHONHASHSEED=random・census_rows.py と
両 census part も隔離側で再生成）→ run3（同一cwd）の 3 実行で
audit.json・census.txt（census_rows.py 再生成を含む）・census-ordered.json・
census-canonical.json が全て byte-identical（preflight も 2 回 byte-identical）。

### fail-closed 検査（part2・出版前に実施）

4. census.txt の P 集合 1 桁を改ざん → C11r が行不一致として捕捉・監査 FAIL（rc=1・PASS 出力なし）。
5. census.txt を一時退避（欠落）→ `FAIL-CLOSED: census.txt is missing; run census_rows.py first`。
   （復元後のフル 14 チェック再実行で clean PASS・baseline と byte-identical を確認。
   なお検証器は引数に未知の文字列を渡すと 0 チェック実行として空監査を書く仕様のため、
   再現コマンドはチェック名を明示して実行すること。）

### 昇格判定

以上（part1 12 チェック全 PASS＋part2 C1d/C11r 追加・フル監査 14 チェック PASS・
census_rows.py 第三実装・3 回 byte-identical・fail-closed 検査）により、
**K1152（y=12 族閉形式 cand12）を observed→proved に昇格する**
（AGENTS.md「同じ命題は同じ K 項目・新規採番なし」・K1141/y=10 の前例と同一手続き）。
マージ命題の y=12 版（x<=z-13 → single_token(x+12,z,R)）・tail 値 (x+12) mod 2 も
全称系として確定。B子に先行出版族の閉形式を逐語転写する構成は cand9（y=10 の B 子）・
cand10（y=11 の B 子・K1141 全称）・cand11（y=12 の B 子・K1143 出版 fit）の 3 連。

## 再現コマンド

```sh
python3 verify_y12_universal.py                  # 12チェックのうち C11 以外（約33秒）
python3 verify_y12_universal.py C11ordered       # census part1（約14秒）
python3 verify_y12_universal.py C11canonical     # census part2（約15秒）
python3 verify_y12_universal.py C1 C1b C2 C2b C3 C4 C4t C7 C8 C9 C11 C12  # part1 12チェック
python3 census_rows.py                            # census.txt（約13秒・約556MB）
python3 scripts/preflight_c1d_y12.py              # C1d 事前検証（約2.2秒）
python3 verify_y12_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12  # part2 フル14チェック
sha256sum verify_y12_universal.py census_rows.py output/audit.json output/census.txt output/census-ordered.json output/census-canonical.json output/preflight-c1d-y12.json
```

実行細部は [published_run.txt](output/published_run.txt) 記録の通り。

## 解釈規約

- K1152（y=12族閉形式）の status は本 part2 の出版（14チェック監査 PASS・3回 byte-identical
  記録・census 第三実装・item 同番号更新）をもって **observed→proved に昇格**した
  （part1 出版時点では observed のままだった。K1141/y=10 の前例と同一手続き・新規採番なし）。
- 有限照合は有限観察の機械的証拠であって、trust 境界（選択肢分解の健全性・mex 恒等式・有限型空間の完全性）は
  y=1..12 系列と同一の機械分類に依存する。C1d アンカー切片の正しさは
  K0999/K1000/K1001/K1011/K1065/K1077/K1087 の主張のy=12行である。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本実験は残余ゲーム族の数学的構造の証明であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=13 族・固定幅・q点版安定化長は範囲外。
