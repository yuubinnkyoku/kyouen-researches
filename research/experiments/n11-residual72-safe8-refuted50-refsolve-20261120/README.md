# n11 残余72行 safe8再解決 第4ラウンド: REFUTED-D10 50根除外後の残余23行再解決（2026-11-20）

## 目的

K1095（代替12根 depth-10掃引・正本 SHA-256
`335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707`）の結果
（WIN8-D10 candidate 3根・REFUTED-D10 fact 9根）を受け、K1095「次の一手」
第1項（pool P‴ 再解決）・第2項（累計16根の内在被覆確認）を実施した。
単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-safe8-refuted50-refsolve-single-owner-note.md`
（commit 22d85b72fce5fc27d617a6d283841175a1407c6d）の下で実施した。

**計画簿記のみを行う**。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは
一切行っていない。REFUTED-D10 は LOSS 証明ではない。標準11×11空盤・二石root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## プロトコル

- 入力5正本をSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・
  K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`）でfail-closed読み出し。
- universe82（残余72行×空き2石のgeneration witness→canonical dedup 380,098根）・
  unsafe8（整数4×4行列式）・safe8 pool 120,474根・coverage・per-row demand・
  greedy 23根計画（根順序・主張被覆行とも）を本実験機械内で独立再導入
  （coverage crosscheck 39,255根）。
- 残余49行宇宙はK1085+K1086から再導入、K1089代替16根の主張をcanonical化して
  49行exactly-once分割を再検証し残余40行、さらにK1091代替15根の主張をcanonical化
  して40行exactly-once分割（WIN8-3根主張10行+REFUTED-12根主張30行）を再検証して
  残余30行、さらにK1095代替12根の主張をcanonical化して30行exactly-once分割
  （WIN8-3根主張7行+REFUTED-9根主張23行・union==30・claims ⊆
  generation-witness被覆）を検証した（残余23行宇宙はK1094正本から取らず
  上流4正本から独立再導入）。
- 除外: REFUTED-D10 50根（K1086の16根+K1089の13根+K1091の12根+K1095の9根）。
  pool P‴ = safe8 − 50 = **120,424根**。
- 残余23行 = K1095 REFUTED-9根の主張被覆行（canonical化）。
- 内在被覆: 累計16 WIN8-D10候補根（K1086の7根+K1089の3根+K1091の3根+
  K1095の3根）のC(8,6)=28部分集合のcanonical再導入によるintrinsic coverage。

## 結果（全27 gate PASS・3実行byte-identical）

- **残余23行は pool P‴ 上で stranded行0**（per-row demand min 1,781 / max 2,934 /
  sum 50,670・23行に触れるprovider 45,219根・
  provider被覆ヒストグラム {1: 40,065, 2: 4,857, 3: 297}）。
- **greedy 9根が残余23行をleftover 0で完全被覆**
  （gains {3:6, 2:2, 1:1}・情報論的下界ceil(23/4)=6に対し+3）。
  選定根（greedy順）:
  `00000000000000083800040048100000`(3), `00000000000000143800000209000000`(3),
  `00000000000000821082000000001018`(3), `00000000000000821086800000000800`(3),
  `00000000000040809002000800100200`(3), `00000000010000809002000040002001`(3),
  `00000000000000103800000008080041`(2), `00000000020000801202000800100001`(2),
  `00000010000000801202000000000448`(1)
- **二部最大マッチング23**（全23行に互いに異なる被覆根が存在・每行1根の
  witnessも構成可能）。
- **WIN8-D10候補累計16根のper-root内在被覆は主張を包含**
  （K1086の7根=23行・K1089の3根=9行・K1091の3根=10行・K1095の3根=7行。
  うち15根はintrinsic==主張で完全一致。K1095の3根は本実験で初めて機械検験し、
  3根目 `0000000800000000380000000810000a` は主張+1行のintrinsic余剰
  `00000000000000003800000008001080` を持つ: 初の「余剰あり」WIN候補。
  当該余剰行は K1086 WIN根 `00000000000000003800000008003180`（証明書がK1096で
  出版済み）の主張行であり、残余23行ではない）。
  **残余23行へのWIN候補intrinsic被覆は0行**: 将来のWIN8 receipt foldは残余23行の
  需要構造を変えない（scope1=scope2同一9根選定で機械保証）。
- 全体計画: **16 WIN8候補根（主張49行）+ 9代替根（23行）= 25根で72行**
  （第3ラウンドの13 WIN+12代替=25根から、WIN層13→16根・代替層12→9根に再編。
  候補根の簿記であり証明書ではない）。

## 独立再導入と決定性

- greedy23根計画の完全再現・replacement16/15/12のclaims canonical化
  （49行/40行/30行exactly-once・claims ⊆ generation-witness被覆）・
  pool P‴ size 120,424・residual23定義（ref9主張23行・win3c主張7行と
  disjoint・残余30行の部分集合）を含め全27 gate PASS。
- 計3実行（同一cwd2回＋別cwd別プロセス1回）で正本JSON byte-identical
  （SHA-256 `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`）。
  機械は出版済みK1094機械（`research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/scripts/`）
  にStage C4（K1095 verdict join）・除外50根・残余23行化・win16の4 alterationsを
  deterministic editor（assert付きexact置換・py_compile検証）で加えて構築した。
- stdlibのみ・乱数・時刻なし。実行時間は各実行約75秒（universe82再構築が主要費）。

## 解釈規約

1. greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
2. REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
   LOSS証明ではない。候補poolの浸食にしかならない。
3. nodes数・solved数を勝敗として読まない。
4. K1095 3根目のintrinsic余剰行は幾何学的事実の記録であり、当該rootの証明書の
   有効性・範囲には一切影響しない（余剰行は残余23行に含まれない）。
5. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
   UNKNOWN のまま。** 本計算は行を1つも閉じない: 残余72行は全行open。

## 次の一手（着手時は単一オーナー宣言を要する）

- 代替9根の depth-10 verdict 掃引（両AND順序18 probes・K1089/K1091/K1095と同一
  protocol）。WIN8が出れば累計候補に加算、REFUTEDが出たらさらに除外して
  第5ラウンド再解決へ。
- 累計16根のWIN8-D10候補の証明書抽出（1根単位の単一オーナー宣言と独立二重検証。
  累計16根のうちroot `8003180` は並走レーンが抽出・三重検証・K1096として出版済み。
  別1根の宣言ノートが先行出版済み: commit 4496c888）。
- K1096証明書のreceipt fold（root `8003180` の主張行の閉鎖簿記。別作業）。
