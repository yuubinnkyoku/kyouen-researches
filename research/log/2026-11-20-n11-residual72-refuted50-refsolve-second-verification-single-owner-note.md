# n11 残余72行 safe8第4ラウンド再解決（K1097）の独立第二検証の単一オーナー宣言（2026-11-20）

本レーンは K1097（残余72行 safe8 pool 第4ラウンド再解決・正本 SHA-256
`2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`・
git blob SHA-1 `4660c012333b04896c36a23a0837fbdbc2572ef9`）の
**独立第二検証**を単一オーナーとして着手する。並走レーンは本宣言項目に着手しないこと。

宣言時の main は `88190cc30838b885d0cd85c92ac02edb5d1567ae`。

## 範囲（やること）

- 入力は上流5正本をSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・
  K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`）でfail-closed読み出し、
  K1097正本はSHA-256・git blob SHA-1の二点pinで読み出す。
- (a) 出版済みK1097機械
  `research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/scripts/safe8_refuted50_refsolve_20261120.py`
  を本環境で再実行し、
  出力正本が出版SHA-256とbyte-identicalであることを確認する（実行形再現）。
- (b) 第二検証機械を**独立実装**する。K1097機械とは意図的に別経路を取る:
  - 4点共円判定は 4×4 整数行列式（Bareiss完全整数前進消去）で再実装
    （K1097機械は 3×3 余因子の交互和）。
  - 内在被覆はサンプリングcrosscheckでなく **全 safe8 120,474根** について
    C(8,6)=28部分集合の全数再導出で構成し、生成witness被覆と全域一致を要求する。
  - 二部最大マッチングは Hopcroft-Karp で実装する（K1097機械はKuhn増大路）。
  - greedy被覆・残余宇宙導出（49/40/30/23行・exactly-once分割）も独立に書き、
    再導出した全中間量をK1097正本の該当フィールドと**全項目照合**する。
- (c) 監査正本JSONは同一cwd 2回 + 別cwd別プロセス 1回の計3実行で
  byte-identicalであることを確認する。
- 成果は `research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/`
  に置く。実験dir名にK番号は含めない。

## やらないこと

- 新規probe・掃引は行わない。代替9根の第5ラウンドdepth-10掃引
  （`2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md`）と
  36 fresh witness掃引（`2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`）
  は他レーンの単一オーナー宣言済み作業であり本レーンは着手しない。
- 証明書抽出・receipt fold・二手応答被覆計画のprobe化・行の閉鎖claimは対象外。
- REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。

## 解釈規約

本第二検証はK1097の計画簿記の独立性を高めるのが目的であり、**行を1つも閉じない:
残余72行は全行openのまま。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4はすべてUNKNOWNのまま。**
