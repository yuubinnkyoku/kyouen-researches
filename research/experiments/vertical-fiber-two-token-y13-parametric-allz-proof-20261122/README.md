# 2トークン残余ゲーム y=13族 全称証明: 正本検証器14機械チェック part1+part2（K1231 fit の正本監査・observed→proved 昇格）

- 実験名: vertical-fiber-two-token-y13-parametric-allz-proof-20261122
- 対象族: H(R; (x,13); z), z >= 0, x >= 13, R >= 0（標準 11×11 とは無関係の数学的残余ゲーム族）
- 対象item: [K1231](../../knowledge/items/K1231-two-token-y13-parametric-closed-form-fit.md)（fit出版時 observed→part1 出版時点でも observed→part2 出版で **observed→proved に昇格**）
- 単一オーナー宣言: [2026-11-22-y13-universal-verifier-single-owner-note.md](../../log/2026-11-22-y13-universal-verifier-single-owner-note.md)（commit 7196cbd570c638ffbdcf8edfb17ccd8b6df8ead3・2026-11-22T17:59:40Z・part1+part2保持・K1231 fitレーンの宣言〔d3404db8・17:01:05Z〕はfitから全称証明段階まで保持を明示済みで自宣言が重複保持・互いに矛盾なし）
- 実行環境: Python 3.12.14 標準ライブラリのみ・cgroup RAM 上限 1,090,519,040 bytes（約1.0 GiB）・2コア・x86_64

## 機械構成（verify_y13_universal.py・part1出版時 SHA-256 b73d9aaa94f04f1f4922d84808ac7afe6f5bfb55631b4c990cae29734279141f・36,457 bytes・937行 → part2拡張版 SHA-256 079b49ad5d11c22c7c6c5f8d103eff9ee2194c7d587e7f2432172616c03c1114・50,865 bytes・1,314行）

y=12 正本機械（K1152/K1162 part2・verify_y12_universal.py SHA-256
e209297603f68c9a82a50f90cac0bc678211d1517f137b5d490dfca3c492eb04）と出版 cand13.py
（K1231 fit・SHA-256 cb903c56b589310907d44f21674ef61a21a4baf7cec8b2e314d5720ff68e2e09）から機械的に組み立て。
転写は組み立てスクリプトの count-assert 付き全置換で機械保証:

1. 生 2エンジン（H_ordered/H_canonical）+ K0832 単一トークン表 single_token + mex: y12 機械から
   verbatim（同領域は y11 正本の 77 行 verbatim と y12 part1 出版時に確定済みの byte）。
2. cand12 ブロック（B子・y=12 出版族の逐語ブロック）: y12 機械の cand12 セクションをブロック内
   Y→Y12 改名のみで転写（改名行数 count-assert・改名以外の差 0 行・Y12 = 12 併置で cand13 ブロックの
   Y = 13 と共存。B子 = cand12(z,x,R-1) 全域〔x>=12・全z・全R〕が出版全称域内）。
3. cand13 ブロック: 出版 cand13.py から fit driver（main）と docstring を除き verbatim（差 0 行）。
   ブロック内 q_odd/single_token_val/_bk の重複定義は y10..y12 検証器と同じくブロック毎に併置。
4. これ以外（docstring・imports・opts13・型機械・12チェック・census runner・main）は本実験のために
   書かれた y=13 機械本体。x=13 合流子: opts13 で A子 = cand12(z,13,R-1)
   （(12,13)≡(13,12) の多重集合同値・x>=14 は cand13(z,x-1,R-1)）、C子 = 1 xor cand13(z-1,x,R-1)。
5. 型機械: clip 窓 2y+2 = 28・番兵 ±29（9族連続 tight 候補・y=5..12: 12/14/16/18/20/22/24/26 に続く）、
   tail x+z+14・merge x<=z-14 は corollary として機械照合。
   y12 part2 版機械からは C1d/C11r 系（part2 の増分チェック）を除去した part1 構成。

## 12チェック構成と実行結果（overall PASS・total_points 6,353,143・total_bad 0）

| check | 内容 | points | bad |
|---|---|---|---|
| C1 | 両生エンジン vs cand13・z=0..14・x=13..31・R<=x+z+47 | 21,945 | 0 |
| C1b | K0832 単一トークン raw anchor・出版 cand12（y=12族=B子）raw anchor・x=13 合流子 (12,13)≡(13,12) raw anchor | 42,041 | 0 |
| C2 | 閉形式恒等式格子 z=0..48・x=13..58・R<=x+z+41（merge/tail 併合） | 226,527 | 0 |
| C2b | 深tail行 z∈{60,72,84,96,108,120,240,400}・x=13..63(step5)・R<=x+z+31 で (x+13) mod 2 | 19,052 | 0 |
| C3 | 選択肢分解の生エンジン子列挙照合 z=0..5・x=13..17 | 1,155 | 0 |
| C4 | 型機械 box ±60（clip 28/番兵29）・(value, sorted子) 完全収束 | 611,504 | 0（C4時点 214,984 型） |
| C4t | tightness probe clip 27/番兵28: 2,987 収束違反・最初 (60,90,90) → clip 2y+2=28 が tight | 611,504 | （bad 総計外・情報提示） |
| C7 | シード 20261132・200k 点・z,x<=3000 | 200,000 | 0 |
| C8 | 境界多様体 z<=3000・dx∈[-28,17]・tail 窓（B子 tail 値 (x+12) mod 2 の raw 窓アンカーも実施） | 953,151 | 0 |
| C9 | v空間シェル [61,64]/[89,92]/[117,120] | 913,194 | 0 |
| C11 | 生 census アンカー z=0..79・x=13..70・R<=x+z+14・両エンジン（後述） | 890,880 | 0 |
| C12 | 深格子 z=0..120・x=13..120・R<=x+z+16 | 1,862,190 | 0 |

- corollary merge（x<=z-14 → single_token(x+13,z,R)）: 1,391,747 点・不一致 0
- corollary tail（R>=x+z+14 → (x+13) mod 2）: 217,342 点・不一致 0
- 型総数（全チェック終了時）: 234,180
- **C4t で clip 27 では 2,987 点の収束違反（最初の違反 (60,90,90)）があり、clip 2y+2=28 が tight。
  2y+2 clip tight は 9 族連続（y=5..13: 12/14/16/18/20/22/24/26/28）**

## C11 census の bounded-memoization twin（y12 part1 と同一設計・本ホストの 1 GiB cgroup 制約）

census box（445,440 点/エンジン）を無制限 memo の生エンジンで 1 プロセス実行すると再帰キャッシュが
cgroup 上限（約1.0 GiB）を超えて OOM kill する（y12 前身試行で exit 137・maxrss 996MB・行ごと
cache-clear 版は 300 秒コマンド上限超過を実測記録済み・y=13 でも同一ホスト同一制約）。そこで:

1. **bounded-memoization twin**: 出版生エンジンの code object を module globals の浅い複写に再束縛し、
   再帰参照（H_ordered/H_canonical 名）を LRU 上限 1,600,000 のキャップ付きキャッシュへ張り替えた双生機。
   再帰定義の byte は正本と同一（types.FunctionType + globals 複写）で、決定的純関数の memo化は透過・
   LRU 追い出しは固定訪問順の下で決定的。したがって値は出版エンジンと厳密一致し、上限は residency のみ制限。
2. **engine 別コマンド分割**: `C11ordered` / `C11canonical` 各コマンドが census 一式（445,440 点・twin cache・
   merge/tail corollary 併合）を実行し `output/census-<engine>.json` を書く。実測: ordered 13.3秒・
   canonical 16.4秒・各 maxrss 約 549-562MB（cgroup 上限内・余裕あり）。
3. **fail-closed merge**: `C11` モードは両 part ファイルを読み、engine 名・box 表記・cache 上限・
   点数（= census 幾何からの再計算期待値 445,440・merge 153,117・tail 4,640 を全て公式から再計算して照合）・
   bad==0 を検証した上で merge し audit の C11 に記録。part ファイル欠落・1 点改ざん・corollary 改ざんは
   全て fail-closed（SystemExit・監査不成立）で捕捉。
4. 無制限 verbatim エンジンは引き続き C1・C1b・C3・C2/C2b・C8 等の生アンカーを担う。

## 決定性（3回実行 byte-identical）

- audit.json: run1（同一cwd）→ run2（同一cwd再実行）→ run3（隔離 tree/cwd/HOME + PYTHONHASHSEED=random）の
  3 実行とも byte-identical（SHA-256 db7c5fa56f407f09ed6604d7677aaab681d78649dc85379d977c5bd58c8e42de・3,103 bytes）。
- census-ordered.json: run1/run2/run3 全て byte-identical
  （SHA-256 264d7cd817583e2a88f617296e2cf03703fd24153b62743a000ec3440c275b22・486 bytes）。
- census-canonical.json: 同様に byte-identical
  （SHA-256 82fb880381358917c47d3f8ab6c4deffabc617d5e45876d46652852f1e306b38・488 bytes）。
- 監査は時刻・実行時間・パスを含めない。seed 固定・sorted keys。
- 付帯確認: 検証器ドキュメント内の cand13 SHA-256 表記は実 byte 再計算値（cb903c56…6e2e09）。
- 機械組み立てスクリプトによる正規再生成物は実行物と byte-identical（sha256 一致）。

## fail-closed 検査（census part 経路・出版前に実施）

1. census-ordered.json の points を 445,440→445,439 に改ざん → `FAIL-CLOSED: census points 445439 != 445440`。
2. corollary merge 点数を 153,117→153,118 に改ざん → `FAIL-CLOSED: census merge corollary mismatch`。
3. census-canonical.json を一時退避（欠落）→ `FAIL-CLOSED: census part file for engine 'canonical' is missing...`。
   （いずれも監査不成立で PASS 出力なし。改ざん後は正本を復元し再実行で PASS・byte-identical を確認。
   なお audit.json は最後に実行したモードの監査を同じパスに書くため、単体 C11 モードや default モード
   （C11 抜き）は部分監査で正本 audit.json を上書きする。本実験では検査・計測後にフル 12 チェックを
   再実行して正本監査を再確定し byte-identical を確認した。）

## part2: C1d 出版切片アンカー + 独立 census 消費者（2026-11-22 追加・observed→proved 昇格段階）

part1 出版（commit ee3b6f73）で残した昇格工程（K1152/y=12・K1141/y=10 と同一手続き）を実行した。
検証器は part1 正本を in-place に拡張（anchor block は y=12 part2 正本検証器〔SHA-256 e2092976…〕から
verbatim 抽出・`Y` は関数ローカル変数のみで cand12/cand13 ブロックと干渉しない）。part1 の 12 チェックの
byte は不変（census part 能力は出版 byte と同一・part2 実行で census-ordered/census-canonical は
part1 出版 byte〔264d7cd8…/82fb8803…〕のまま再確認）。

### C1d（出版固定 z 切片アンカーの y=13 特殊化・139,356 点・bad 0）

出版 uniform closed form（z=8: K0999/K1000・z=9: K1001・z=10: K1011・z=15/16/17:
K1065/K1077/K1087）のアンカー関数 A8u..A17u を x=13..159・R=1..x+61 で y=13 行
（引数 (x,13,r)）と cand13 が一致することを機械照合（内訳: 6 z0 × x=13..159 × R=1..x+61 の
アンカー掃引 129,654 点 ＋出版低 R 単一トークン縮約 R<=z+6（z0=15,16,17）の y=13 行照合
〔cand13 vs single_token(x+13,z0,R)〕9,702 点。y=12 part2 の 130,092+9,768=139,860 点構成の鏡像）。
**組み込み前事前検証（fail-closed）**: 各 z0 について x=13..45・R<=x+z0+30 の 14,157 点を
出版アンカー×H_ordered×H_canonical×cand13 の 4 方照合で不一致 0
（z 別 2,211/2,244/2,277/2,442/2,475/2,508）・低 R 縮約 9,702 点も不一致 0・約 2.2 秒
（`scripts/preflight_c1d_y13.py`・結果 `output/preflight-c1d-y13.json`・SHA-256 a9307d33…・2 回実行
byte-identical。y=10 でこの段階が K1087 転写初稿の評価順バグ 170 点を捕捉した実績があり、
本族ではアンカーは y=12 正本からの verbatim 再転写のため 4 方照合で初めから一致）。
z=15/16/17 の (y,d) 過渡セルと S<17/S==17 分岐は y=13 で到達不能（S=x+13>=26）。

### C11r（独立 census 台帳消費者・450,080 点・bad 0・fail-closed）

census_rows.py（y=13 版・第三実装）が z=0..79・x=13..70・R=0..x+z+15 の 4,640 行
（450,080 点・値0点 224,203・エンジン状態計算〔LRU misses〕6,630,827・約 15 秒・maxrss 約 557MB）の
行ごとの Thue-Morse 指数・値2/値1台帳（T/P 集合）・tail を出力した census.txt
（829,622 bytes・4,640 行＋空行 80・SHA-256 505f05bf04c3819561707f42927da354fdefcdd315b1a3792b0c3e9eb1fe5989。
tail アサート R>=x+z+14 の (x+13) mod 2 全行成立）。C11r は census.txt の全行を
cand13 から再導出して T/P 集合・idx・tail を照合する（行重複・欠落・rows != 80*58・
終端改行なしは FAIL-CLOSED）。census_rows.py の本体は y=5..y=10/y=12 出版版と同一の
生 tuple 二重再帰で、本実行ホストの 1 GiB cgroup 制約のみ LRU 上限 1,600,000
（CENSUS_CACHE_MAXSIZE）として明示キャップ（docstring 記載）。決定的純関数の
memo 化は透過で、LRU 追い出しは固定訪問順の下で決定的。

### part2 フル監査（14 チェック・overall PASS・total_points 6,942,579・total_bad 0）

C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12 を 1 コマンドで実行:
C1d 139,356 点・C11r 450,080 点が part1 の 6,353,143 点に加算され
**total_points 6,942,579・total_bad 0・型総数 234,180**（C4t は情報提示で bad 総計外）。
merge corollary 1,391,747 点・tail corollary 217,342 点は part1 と不変のまま bad 0。
audit.json（3,673 bytes・SHA-256 2f5f56c0da4578252db8bf12d536764562ded134e5bad45ca832c58b17424bb1d・
stage 文言は part2）。

### 決定性（part2・3 実行 byte-identical）

run1（同一cwd）→ run2（同一cwd再実行）→ run3（隔離 tree/cwd/HOME + PYTHONHASHSEED=random・
census_rows.py・preflight・両 census part も隔離側で再生成）の 3 実行で
audit.json・census.txt・census-ordered.json・census-canonical.json・preflight-c1d-y13.json
が全て byte-identical（census_rows.py は記録時にもう 1 回再実行し計 4 回 byte-identical）。

### fail-closed 検査（part2・出版前に実施）

4. census.txt の P 集合 1 桁を改ざん → C11r が行不一致として捕捉・監査 FAIL（rc=1・PASS 出力なし）。
5. census.txt を一時退避（欠落）→ `FAIL-CLOSED: census.txt is missing; run census_rows.py first`。
   （復元後のフル 14 チェック再実行で clean PASS・baseline と byte-identical を確認。
   なお検証器は引数に未知の文字列を渡すと 0 チェック実行として空監査を書く仕様のため、
   再現コマンドはチェック名を明示して実行すること。）

### 昇格判定

以上（part1 12 チェック全 PASS＋part2 C1d/C11r 追加・フル監査 14 チェック PASS・
census_rows.py 第三実装・3 回 byte-identical・fail-closed 検査）により、
**K1231（y=13 族閉形式 cand13）を observed→proved に昇格する**
（AGENTS.md「同じ命題は同じ K 項目・新規採番なし」・K1152/y=12 の前例と同一手続き）。
マージ命題の y=13 版（x<=z-14 → single_token(x+13,z,R)）・tail 値 (x+13) mod 2 も
全称系として確定。B子に先行出版族の閉形式を逐語転写する構成は cand9（y=10 の B 子）・
cand10（y=11 の B 子・K1141 全称）・cand11（y=12 の B 子・K1143）・cand12（y=13 の B 子・K1152 全称）
の 4 連。
なお現行 main の knowledge.yml に y=11（K1143）・y=12（K1152）実験機の CI step が存在しない
（CI 登録は y=10/K1141 まで）ため、本実験も CI step を登録せず出版 byte を監査正本とする
（直近 2 族と同一の扱い）。

## 再現コマンド

```sh
python3 verify_y13_universal.py                  # 12チェックのうち C11 以外（約33秒）
python3 verify_y13_universal.py C11ordered       # census part1（約13秒・約550-562MB）
python3 verify_y13_universal.py C11canonical     # census part2（約16秒）
python3 verify_y13_universal.py C1 C1b C2 C2b C3 C4 C4t C7 C8 C9 C11 C12  # part1 フル12チェック
python3 census_rows.py                            # census.txt（約15秒・約557MB）
python3 scripts/preflight_c1d_y13.py              # C1d 事前検証（約2.2秒）
python3 verify_y13_universal.py C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12  # part2 フル14チェック
sha256sum verify_y13_universal.py census_rows.py scripts/preflight_c1d_y13.py output/audit.json output/census.txt output/census-ordered.json output/census-canonical.json output/preflight-c1d-y13.json
```

実行細部（part1・part2 両段階）は [published_run.txt](output/published_run.txt) 記録の通り。

## 解釈規約

- K1231（y=13族閉形式 cand13）の status は本 part2 の出版（14チェック監査 PASS・3回 byte-identical
  記録・census 第三実装・item 同番号更新）をもって **observed→proved に昇格**した
  （part1 出版時点では observed のままだった。K1152/y=12 の前例と同一手続き・新規採番なし）。
  有限照合は有限観察の機械的証拠であって、trust 境界（選択肢分解の健全性・mex 恒等式・有限型空間の完全性）は
  y=1..13 系列と同一の機械分類に依存する。C1d アンカー切片の正しさは
  K0999/K1000/K1001/K1011/K1065/K1077/K1087 の主張のy=13行である。
  B子に先行出版族の閉形式を逐語転写する構成は cand10（y=11 正本機械の B 子）・cand11（y=12 正本機械の
  B 子）に続き cand12（y=13 正本機械の B 子・K1152 全称）で 3 連。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本実験は残余ゲーム族 H(R;(x,13);z) の数学的構造の証明であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=14 族・固定幅・q点版安定化長は範囲外。
