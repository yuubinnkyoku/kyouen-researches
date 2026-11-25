# n11 残余72行 safe8 pool 第4ラウンド再解決（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-safe8-refuted50-refsolve-single-owner-note.md](2026-11-20-n11-residual72-safe8-refuted50-refsolve-single-owner-note.md)
（commit 22d85b72fce5fc27d617a6d283841175a1407c6d）の下で、K1095
（代替12根 depth-10掃引: WIN8-D10 candidate 3根・REFUTED-D10 fact 9根）の結果を
受けて**REFUTED-D10 50根除外後の pool P‴（120,424根）での残余23行再解決**を
実施した。**新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは
行っていない**。

- 機械: `research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/scripts/safe8_refuted50_refsolve_20261120.py`
  （stdlibのみ・入力5正本SHA pin・universe82/safe8/greedy23計画の独立再導入・
  claims canonical化3段（replacement16/15/12）・Stage C4（K1095 verdict join）・
  全27 gate fail-closed）
- 正本: `research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json`
  （SHA-256 `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`）

## プロトコルと入力の信頼境界

入力はK1085 census正本（SHA-256 `5fdd342d…`）・K1086掃引正本（`3045e152…`）・
K1089掃引正本（`808fbda1…`）・K1091掃引正本（`edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`）・
K1095掃引正本（`335eca5e…`）の5点をSHA-256 pinでfail-closed読み出し。
universe82（残余72行×空き2石のgeneration witness→canonical dedup 380,098根・
unsafe8 259,624・safe8 120,474）・coverage hist {1:82,602, 2:33,104, 3:4,718, 4:50}・
per-row demand・coverage crosscheck（39,255根・全C(8,6)=28部分集合再導入）・
greedy 23根計画（根順序・各根の主張被覆行の両方の完全再現）をK1088/K1090機械と
同じく独立再導入した。残余49行宇宙はK1085+K1086から再導入し（WIN8 7根の主張
23行とREFUTED 16根の主張49行のdisjoint exactly-once union==72分割）、K1089代替
16根の主張をcanonical化して49行exactly-once分割を再検証して残余40行、さらに
K1091代替15根の主張をcanonical化して40行exactly-once分割（WIN8-3根主張10行+
REFUTED-12根主張30行）を再検証して残余30行、さらにK1095代替12根の主張を
canonical化して30行exactly-once分割（WIN8-3根主張7行+REFUTED-9根主張23行・
union==30・claims ⊆ generation-witness被覆）を検証した
（残余23行宇宙はK1094正本から取らず上流4正本から独立再導入）。
除外集合はREFUTED-D10 50根（K1086の16根+K1089の13根+K1091の12根+
K1095の9根）で、pool P‴ = 120,474 − 50 = **120,424根**。残余23行は
K1095 REFUTED-9根の主張23行と定義し（WIN8-3根の主張7行とdisjoint・残余30行の
部分集合）、per-root需要・greedy・二部最大マッチング・WIN8候補累計16根の
内在被覆（C(8,6)=28部分集合のcanonical再導入）を計算した。

## 結果（全27 gate PASS・3実行byte-identical）

1. **残余23行は pool P‴ 上で stranded行0**（demand min 1,781 / max 2,934 /
   sum 50,670・23行に触れるprovider 45,219根・被覆ヒストグラム
   {1: 40,065, 2: 4,857, 3: 297}）。
2. **greedy 9根が残余23行をleftover 0で完全被覆**（gains {3: 6, 2: 2, 1: 1}・
   情報論的下界ceil(23/4)=6に対し+3）。選定根は実験README表の通り
   （6根が3行、2根が2行、1根が1行）。
3. **二部最大マッチング23**: 全23行に互いに異なる被覆根が存在し、每行1根の
   witnessも構成可能。
4. **WIN8-D10候補累計16根（K1086の7根+K1089の3根+K1091の3根+K1095の3根）の
   per-root内在被覆は主張を包含**（23行+9行+10行+7行=主張49行。うち15根は
   intrinsic==主張で完全一致。K1095の3根は本実験で初めて機械検証し、
   3根目 `0000000800000000380000000810000a` は主張+1行のintrinsic余剰
   `00000000000000003800000008001080` を持つ: 初の「余剰あり」WIN候補の機械
   記録。当該余剰行は残余23行ではなく K1086 WIN根
   `00000000000000003800000008003180`（証明書がK1096で出版済み）の主張行で
   あり、残余23行の需要構造には無影響）。
   **残余23行へのWIN候補intrinsic被覆は0行**: 将来のWIN8 receipt foldは残余
   23行の需要構造を変えない（scope1=scope2が同一9根選定で機械保証）。
5. 全体計画: **16 WIN8候補根（主張49行）+ 9代替根（23行）= 25根で72行**
   （第3ラウンドの13 WIN+12代替=25根から、WIN層13→16根・代替層12→9根に
   再編された計画。候補根の簿記であり証明書ではない）。

決定性: 計3実行（同一cwd2回＋別cwd別プロセス1回）で正本JSON byte-identical
（SHA-256 `2896deb0…`）をcmp確認した（別cwd実行は入力5正本のコピーを持つ
別作業ディレクトリ・別プロセス）
。機械は出版済みK1094機械（`research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/scripts/`）に
Stage C4（K1095 verdict join）・除外50根・残余23行化・win16の4 alterationsを
deterministic editor（assert付きexact置換・py_compile検証）で加えて構築した。
stdlibのみ・乱数・時刻なし。実行時間は各実行約75秒（universe82再構築が主要費）。

## 解釈規約（再掲）

greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
LOSS証明ではない。nodes数・solved数を勝敗として読まない。K1095 3根目の
intrinsic余剰行は幾何学的事実の記録であり、当該rootの証明書の有効性・範囲に
一切影響しない（余剰行は残余23行に含まれない）。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。本計算は行を1つも閉じない: 残余72行は全行open。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. 代替9根の depth-10 verdict 掃引（両AND順序18 probes・runner v17・cap 30M・
   pilot_d6制御・K1089/K1091/K1095と同一protocol）。WIN8が出れば累計候補に
   加算、REFUTEDが出たらさらに除外して第5ラウンド再解決へ。
2. 累計16根のWIN8-D10候補の証明書抽出（1根単位の単一オーナー宣言と独立二重
   検証。累計16根のうちroot `8003180` は並走レーンが抽出・三重検証・K1096と
   して出版済み。別1根の宣言ノートが先行出版済み: commit 4496c888）。
3. K1096証明書のreceipt fold（root `8003180` の主張行の閉鎖簿記。別作業）。
