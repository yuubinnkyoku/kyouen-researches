# n11 残余72行 safe8 pool 第3ラウンド再解決（REFUTED-D10 41根除外・残余30行）の単一オーナー宣言（2026-11-20）

本レーンは K1091（代替15根 depth-10掃引・正本 SHA-256
`edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`）
README「次の一手」第1項・第2項である **REFUTED-D10 41根除外後の pool P″
（120,433根）上での残余30行 greedy計画再解決と、WIN8-D10候補累計13根の
内在被覆（intrinsic coverage）確認** について単一オーナーとして着手する。
並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- 対象: K1091掃引でREFUTED-D10 12根が出たことにより浸食した代替planningの再解決。
  除外集合は REFUTED-D10 41根（K1086の16根+K1089の13根+K1091の12根）。
  pool P″ = safe8 120,474 − 41 = **120,433根**。
  再解決行は残余30行（K1091 REFUTED-12根の主張被覆行・canonical）。
- 計算: (1) 残余30行のpool P″上のper-row demand・stranded行・情報論的下界・
  二部最大マッチング、(2) lex-smallest max-gain greedy計画の再構成、
  (3) WIN8-D10候補累計13根（K1086の7根+K1089の3根+K1091の3根）の
  C(8,6)=28部分集合による内在被覆がper-root主張と一致するか・残余30行への
  余剰の有無、(4) 主張・被覆幾何の整数幾何再導入（K1091正本から直接取らず
  K1085+K1086+K1089から再導入した残余40行宇宙上で検証）。
- 決定性: stdlibのみ・乱数・時刻なし。複数実行（同一cwd・別cwd別プロセス）で
  正本JSONがbyte-identicalとなることを確認してから出版する。全gateは
  fail-closed。

## やらないこと

- 新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは一切行わない。
- greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。

## 解釈規約

本計算は行を1つも閉じない。REFUTED-D10は「当該rootの当該sideのdepth-10内
必勝不存在」のprobe事実記録であり、それ以前の局面のLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**
