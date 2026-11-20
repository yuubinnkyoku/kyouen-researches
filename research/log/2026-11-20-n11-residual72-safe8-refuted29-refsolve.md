# n11 残余72行 safe8 pool 第2ラウンド再解決（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-safe8-refuted29-refsolve-single-owner-note.md](2026-11-20-n11-residual72-safe8-refuted29-refsolve-single-owner-note.md)
（commit c5dee3deb566a8ee3ad5a61e4a600b6be5e1aaa4）の下で、K1089
（代替16根 depth-10掃引: WIN8 3根・REFUTED 13根）の結果を受けて
**REFUTED-D10 29根除外後の pool P′（120,445根）での残余40行再解決**を実施した。
**新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは行っていない**。

- 機械: `research/experiments/n11-residual72-safe8-refuted29-refsolve-20261120/scripts/safe8_refuted29_refsolve_20261120.py`
  （stdlibのみ・入力3正本SHA pin・universe82/safe8/greedy23計画の独立再導入・
  claims canonical化・全20 gate fail-closed）
- 正本: `research/experiments/n11-residual72-safe8-refuted29-refsolve-20261120/output/safe8-refuted29-refsolve-20261120.json`
  （SHA-256 `48af6810173060eb769eb52b1fd50ceb81222c07ba7738c8a15832f8c552d3f5`）

## プロトコルと入力の信頼境界

入力はK1085 census正本（SHA-256 `5fdd342d…`）・K1086掃引正本（`3045e152…`）・
K1089掃引正本（`808fbda1…`）の3点をSHA-256 pinでfail-closed読み出し。
universe82（残余72行×空き2石のgeneration witness 471,960 events→canonical dedup
380,098根・unsafe8 259,624・safe8 120,474）・coverage hist {1:82,602, 2:33,104,
3:4,718, 4:50}・per-row demand（min 1,714/max 2,944/sum 163,164）・
coverage crosscheck（39,255根・全C(8,6)=28部分集合再導入）・greedy 23根計画
（根順序・各根の主張被覆行の両方の完全再現）をK1088機械と同じく独立再導入した。
残余49行宇宙はK1085+K1086から再導入し（WIN8 7根の主張23行とREFUTED 16根の主張49行の
disjoint exactly-once union==72分割）、K1089代替16根の主張被覆はcanonical化
（D4 orbit最小hex）して「49行exactly-once分割・各主張がgeneration-witness被覆に包含」
を検証した上で使用した。除外集合はREFUTED-D10 29根（K1086の16根+K1089の13根）で、
pool P′ = 120,474 − 29 = **120,445根**。残余40行はK1089 REFUTED-13根の主張40行と定義し
（WIN8-3根の主張9行とdisjoint・残49行の補集合）、per-root需要・greedy・
二部最大マッチング・WIN8候補累計10根の内在被覆（C(8,6)=28部分集合のcanonical再導入）を
計算した。

## 結果（全20 gate PASS・3実行byte-identical）

1. **残余40行は pool P′ 上で stranded行0**（demand min 1,783 / max 2,942 /
   sum 89,467・40行に触れるprovider 75,738根）。
2. **greedy 15根が残余40行をleftover 0で完全被覆**（gains {4:2, 3:9, 2:1, 1:3}・
   情報論的下界ceil(40/4)=10に対し+5）。選定根は K1088形式で実験README表の通り
   （先頭2根が4行、9根が3行、1根が2行、3根が1行）。
3. **二部最大マッチング40**: 全40行に互いに異なる被覆根が存在し、每行1根の
   witnessも構成可能。
4. **WIN8-D10候補累計10根（K1086の7根+K1089の3根）のper-root内在被覆は
   主張と完全一致**（23行+9行・主張外の行へのintrinsic余剰なし）。
   **残余40行へのWIN候補intrinsic被覆は0行**: 将来のWIN8 receipt foldは
   残余40行の需要構造を変えない（scope1=scope2が同一15根選定で機械保証）。
5. 全体計画: **10 WIN8候補根（主張32行）+ 15代替根（40行）= 25根で72行**
   （第1ラウンドの7 WIN8+16代替=23根から、REFUTED浸食で代替層が16→15根に
   再編された計画。候補根の簿記であり証明書ではない）。

決定性: 同一cwd2回＋別cwd別プロセス1回の3実行に加え、輸送直前の同一cwd再実行
（計4実行）で正本JSON byte-identical
（SHA-256 `48af6810…`）を再確認した（末尾実行はcmpによるbyte比較済み）。stdlibのみ・乱数・時刻なし。
実行時間は各実行約76秒（universe82再構築が主要費）。

## 解釈規約（再掲）

greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
LOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。本計算は行を1つも閉じない: 残余72行は全行open。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. 代替15根の depth-10 verdict 掃引（両AND順序30 probes・runner v17・cap 30M・
   pilot_d6制御・K1086/K1089と同一protocol）。
2. 累計10根のWIN8-D10候補の証明書抽出（windfall型extractorの8石拡張・
   1根単位の単一オーナー宣言と独立二重検証。1根抽出は並走レーンが宣言済み: commit 4496c888）。
3. 掃引でREFUTEDが出た場合の第3ラウンド再解決（除外33根超のpoolでの反復）。
