# n11 残余72行 safe8 pool 第3ラウンド再解決（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-safe8-refuted41-refsolve-single-owner-note.md](2026-11-20-n11-residual72-safe8-refuted41-refsolve-single-owner-note.md)
（commit 934a4ceb4a5c918418b46594e124f4a4335f940e）の下で、K1091
（代替15根 depth-10掃引: WIN8 3根・REFUTED 12根）の結果を受けて
**REFUTED-D10 41根除外後の pool P″（120,433根）での残余30行再解決**を実施した。
**新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは行っていない**。

- 機械: `research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/scripts/safe8_refuted41_refsolve_20261120.py`
  （stdlibのみ・入力4正本SHA pin・universe82/safe8/greedy23計画の独立再導入・
  claims canonical化2段（replacement16/replacement15）・全23 gate fail-closed）
- 正本: `research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/output/safe8-refuted41-refsolve-20261120.json`
  （SHA-256 `e19244904779d906853de603d42c07903e08ab80008aeeb621913669a249baa8`）

## プロトコルと入力の信頼境界

入力はK1085 census正本（SHA-256 `5fdd342d…`）・K1086掃引正本（`3045e152…`）・
K1089掃引正本（`808fbda1…`）・K1091掃引正本（`edd7ac84…`）の4点を
SHA-256 pinでfail-closed読み出し。universe82（残余72行×空き2石のgeneration
witness→canonical dedup 380,098根・unsafe8 259,624・safe8 120,474）・
coverage hist {1:82,602, 2:33,104, 3:4,718, 4:50}・per-row demand・
coverage crosscheck（39,255根・全C(8,6)=28部分集合再導入）・greedy 23根計画
（根順序・各根の主張被覆行の両方の完全再現）をK1088/K1090機械と同じく
独立再導入した。残余49行宇宙はK1085+K1086から再導入し（WIN8 7根の主張23行と
REFUTED 16根の主張49行のdisjoint exactly-once union==72分割）、K1089代替16根の
主張をcanonical化して49行exactly-once分割を再検証、残余40行を定義した。
さらにK1091代替15根の主張被覆をcanonical化（D4 orbit最小hex）して
「40行exactly-once分割・各主張がgeneration-witness被覆に包含・
WIN8-3根の主張10行とREFUTED-12根の主張30行のdisjoint union==40」を検証した上で
使用した。除外集合はREFUTED-D10 41根（K1086の16根+K1089の13根+K1091の12根）で、
pool P″ = 120,474 − 41 = **120,433根**。残余30行はK1091 REFUTED-12根の
主張30行と定義し（WIN8-3根の主張10行とdisjoint・残余40行の補集合）、
per-root需要・greedy・二部最大マッチング・WIN8候補累計13根の内在被覆
（C(8,6)=28部分集合のcanonical再導入）を計算した。

## 結果（全23 gate PASS・5実行byte-identical）

1. **残余30行は pool P″ 上で stranded行0**（demand min 1,782 / max 2,935 /
   sum 65,952・30行に触れるprovider 58,259根・被覆ヒストグラム
   {1: 50,956, 2: 6,913, 3: 390}）。
2. **greedy 12根が残余30行をleftover 0で完全被覆**（gains {3:8, 2:2, 1:2}・
   情報論的下界ceil(30/4)=8に対し+4）。選定根は実験README表の通り
   （先頭8根が3行、2根が2行、2根が1行）。
3. **二部最大マッチング30**: 全30行に互いに異なる被覆根が存在し、每行1根の
   witnessも構成可能。
4. **WIN8-D10候補累計13根（K1086の7根+K1089の3根+K1091の3根）の
   per-root内在被覆は主張と完全一致**（23行+9行+10行・主張外の行への
   intrinsic余剰なし。K1091の3根は本実験で初めて機械検証）。
   **残余30行へのWIN候補intrinsic被覆は0行**: 将来のWIN8 receipt foldは
   残余30行の需要構造を変えない（scope1=scope2が同一12根選定で機械保証）。
5. 全体計画: **13 WIN8候補根（主張42行）+ 12代替根（30行）= 25根で72行**
   （第2ラウンドの13 WIN8+15代替=28根計画から、代替層が15→12根に
   再編された計画。候補根の簿記であり証明書ではない）。

決定性: 計5実行で正本JSON byte-identical（SHA-256 `e1924490…`）を確認した
（リセット前の同一cwd2回に加え、実行環境リセットを跨いで出版済みK1090機械から
決定的編集再適用で機械を再構築し、同一cwd2回＋別cwd別プロセス1回。
末尾実行同士はcmpによるbyte比較済み）。stdlibのみ・乱数・時刻なし。
実行時間は各実行約75秒（universe82再構築が主要費）。

## 解釈規約（再掲）

greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
LOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。本計算は行を1つも閉じない: 残余72行は全行open。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. 代替12根の depth-10 verdict 掃引（両AND順序24 probes・runner v17・cap 30M・
   pilot_d6制御・K1089/K1091と同一protocol）。
2. 累計13根のWIN8-D10候補の証明書抽出（1根単位の単一オーナー宣言と
   独立二重検証。累計13根のうち2根は宣言済み: commit 4496c888・0360f21a）。
3. 掃引でREFUTEDが出た場合の第4ラウンド再解決（除外53根超のpoolでの反復）。
