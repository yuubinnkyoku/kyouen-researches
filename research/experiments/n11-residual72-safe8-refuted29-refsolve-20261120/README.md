# n11 残余72行 safe8再解決 第2ラウンド: REFUTED-D10 29根除外後の残余40行再解決（2026-11-20）

## 目的

K1089（代替16根 depth-10掃引・正本 SHA-256
`808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`）の結果
（WIN8-D10 candidate 3根・REFUTED-D10 fact 13根）を受け、K1089 README
「次の一手」第1項・第2項を実施した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-safe8-refuted29-refsolve-single-owner-note.md`
（commit c5dee3deb566a8ee3ad5a61e4a600b6be5e1aaa4）の下で実施した。

**計画簿記のみを行う**。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは
一切行っていない。REFUTED-D10 は LOSS 証明ではない。標準11×11空盤・二石root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## プロトコル

- 入力3正本をSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・K1089 `808fbda1…`）で
  fail-closed読み出し。
- universe82（残余72行×空き2石のgeneration witness→canonical dedup 380,098根）・
  unsafe8（整数4×4行列式）・safe8 pool 120,474根・coverage・per-row demand・
  greedy 23根計画（根順序・主張被覆行とも）を本実験機械内で独立再導入
  （coverage crosscheck 39,255根）。
- 残余49行宇宙はK1085+K1086から再導入（WIN8 7根の主張23行と REFUTED 16根の主張49行の
  disjoint exactly-once union==72 分割）。K1089の代替16根の主張被覆は
  canonical化（D4 orbit最小hex）して49行exactly-once分割・generation-witness被覆包含を検証。
- 除外: REFUTED-D10 29根（K1086の16根+K1089の13根）。pool P′ = safe8 − 29 = **120,445根**。
- 残余40行 = K1089 REFUTED-13根の主張被覆行（canonical化）。
- 内在被覆: 累計10 WIN8-D10候補根（K1086の7根+K1089の3根）のC(8,6)=28部分集合の
  canonical再導入によるintrinsic coverage。

## 結果（全20 gate PASS・3実行byte-identical）

- **残余40行は pool P′ 上で stranded行0**（per-row demand min 1,783 / max 2,942 /
  sum 89,467・40行に触れるprovider 75,738根）。
- **greedy 15根が残余40行をleftover 0で完全被覆**
  （gains {4:2, 3:9, 2:1, 1:3}・情報論的下界ceil(40/4)=10に対し+5）。
  選定根（greedy順）:
  `00000000000000801212000001009000`(4), `00000000020008003800000009001000`(4),
  `00000000000000003800000008d10000`(3), `00000000000000043800000008180010`(3),
  `0000000000000010380000000b080000`(3), `00000000000000801202000000901002`(3),
  `00000000000000801202000001000448`(3), `00000000000000821082000000000890`(3),
  `00000000000000a21083000000001000`(3), `00000000000040809002000022100000`(3),
  `00000010000000003840000008080040`(3), `00000000000000801202020001005000`(2),
  `00000000010000809002000040000006`(1), `00000008000000003800000008100006`(1),
  `00000010000000801202000000000414`(1)
- **二部最大マッチング40**（全40行に互いに異なる被覆根が存在・每行1根のwitnessも構成可能）。
- **WIN8-D10候補累計10根のper-root内在被覆は主張と完全一致**（K1086の7根=23行・
  K1089の3根=9行・主張外の行へのintrinsic余剰なし）。
  **残余40行へのWIN候補intrinsic被覆は0行**: 将来のWIN8 receipt foldは残余40行の
  需要構造を変えない（scope1=scope2同一15根選定で機械保証）。
- 全体計画: **10 WIN8候補根（主張32行）+ 15代替根（40行）= 25根で72行**。
  代替15根は未掃引で、depth-10掃引には両AND順序30 probesを要する
  （候補根の簿記であり証明書ではない）。

## 独立再導入と決定性

- greedy23根計画の完全再現（根順序・主張被覆行ともK1085出版と一致）・
  replacement16のclaims canonical化で49行exactly-once・claims ⊆ generation-witness被覆・
  pool P′ size 120,445・residual40定義（ref13主張40行・win3主張9行と disjoint）を含め
  全20 gate PASS。
- 3実行（同一cwd 2回＋別cwd別プロセス1回）で正本JSON byte-identical
  （SHA-256 `48af6810173060eb769eb52b1fd50ceb81222c07ba7738c8a15832f8c552d3f5`）。
- stdlibのみ・乱数・時刻なし。

## 解釈規約

1. greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
2. REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
   LOSS証明ではない。候補poolの浸食にしかならない。
3. nodes数・solved数を勝敗として読まない。
4. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
   UNKNOWN のまま。** 本計算は行を1つも閉じない: 残余72行は全行open。

## 次の一手（着手時は単一オーナー宣言を要する）

- 代替15根の depth-10 verdict 掃引（両AND順序30 probes・K1089と同一protocol）。
  WIN8が出れば累計候補に加算、REFUTEDが出たらさらに除外して第3ラウンド再解決へ。
- 累計10根のWIN8-D10候補の証明書抽出（windfall型extractorの8石拡張・1根単位の
  単一オーナー宣言と独立二重検証。1根抽出は並走レーンが宣言済み: commit 4496c888）。
