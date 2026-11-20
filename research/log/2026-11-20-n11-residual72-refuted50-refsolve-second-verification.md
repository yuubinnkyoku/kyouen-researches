# 2026-11-20 n11 残余72行 safe8第4ラウンド再解決（K1097）の独立第二検証

## 着手判断

最新main（着手時 `3ac69a581f`→作業中に `88190cc30838b885d0cd85c92ac02edb5d1567ae`
へ進行）・`AGENTS.md`・`research/knowledge/README.md`・K1085〜K1097と
11/20のsingle-owner noteを確認した。残余72行レーンの進行中案件は次の3件で
いずれも他レーンが単一オーナー宣言済みであり着手しない:

- 代替9根の第5ラウンドdepth-10掃引（commit a2f933c462 宣言）
- WIN8証明書抽出 root `…8180000`（commit 4496c888 宣言）
- 36 fresh witness掃引（宣言済み・準備物は出版済み）

また二手応答被覆の最小計画（149根・2026-11-20 01:28-01:30Zのコミット群）は
直前に出版されたばかりで、同レーンがitem・README弾丸の追加工程を進めている
可能性が高いため、本実行では着手を見送った。

残る価値の高い未着手課題として、**残余72行計画の根幹をなすK1097（第4ラウンド
再解決）に独立第二検証がない**点を選んだ。本レーンは単一オーナー宣言ノート
（commit de8c44ac96fbde0616a216f184dd54b42b3f2c49・先行出版）で着手権を確定
してから実施した。

## 方法

- 入力はK1095〜K1097機械と同一の上流5正本（K1085 `5fdd342d…`・K1086
  `3045e152…`・K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`
  のSHA-256 pin・fail-closed）。K1097正本はSHA-256
  `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`・
  git blob SHA-1 `4660c012333b04896c36a23a0837fbdbc2572ef9` の二点pin。
- まず出版済みK1097機械（SHA-256 `f01f459f4f9ec2b9d38c0ed61f14132cf36c870f316d1fae840fe534181192c0`）
  を本環境で再実行し、出力が出版正本とbyte-identical（SHA-256一致）であることを確認
  （実行・約70秒・27 gate all ok）。
- 次に新規実装の第二検証機械
  `research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/scripts/verify_refuted50_second.py`
  （SHA-256 `547448e464ec7b3fed8b80639234cce8e763a7e648c4895b2992a93b7b8d8e75`）で
  全量を独立再導入した。K1097機械との意図的な相違:
  (a) 4点禁止判定はアンカー並進3×3整数行列式（原点を通る円
  x²+y²+ux+vy=0 による零条件）で実装し、72基底行はBareiss 4×4完全整数前進消去
  でも交差確認した。K1097機械は同一の4×4行列式を3×3余因子4項交替和で展開
  していた。
  (b) **safe8全根120,474についてC(8,6)=28部分集合の内在被覆を全数再導出**し、
  生成witness被覆との全域一致を要求した（K1097機械のcrosscheckは39,255根の
  サンプリング）。
  (c) 二部最大マッチングはHopcroft-Karp（K1097機械はKuhn増大路）。
  (d) 4掃引のノード総計（18,032,471 / 6,339,079 / 7,383,022 / 5,700,222）は
  出版フィールド値ではなくprobe記録からの独立総和として再計算した。
  (e) greedy被覆（72行23根・残余23行9根・scope2）はlexicographically-smallest
  max-gain規則の独立走査で再実装し、根順序・獲得行・主張被覆行を正本と
  全件照合した。
- K1086掃引の生主張行（D4順hex）をcanonical化したところ、正準形が
  K1085 censusのgreedy計画covered_rowsと全23根で一致することも独立に確定
  （上流正本間の整合）。

## 結果（42/42 gate PASS・3実行byte-identical）

- **K1097の全主要値が独立再導入で一致した**: universe82 380,098根
  （生成事象471,960）・safe8 120,474・unsafe8 259,624・被覆ヒストグラム
  {1: 82,602, 2: 33,104, 3: 4,718, 4: 50}・需要 min 1,714 / max 2,944 /
  sum 163,164（K1085 census欄とも一致）・greedy 23根計画の根順序と
  主張被覆行が完全再現・残余宇宙72→49→40→30→23のexactly-once分割・
  REFUTED除外50根・pool P‴ = 120,424・残余23行の需要 min 1,781 / max 2,934 /
  sum 50,670・stranded 0・provider被覆 {1: 40,065, 2: 4,857, 3: 297}
  （45,219根）・WIN16足跡（15根 intrinsic==主張・K1095 3根目の余剰行
  `00000000000000003800000008001080` のみで残余23行ではない）・
  残余23行へのWIN内在被覆0行・scope1 greedy 9根（gains {3:6, 2:2, 1:1}・
  leftover 0・情報下界6）とscope2同一選定・最大マッチング23・per-row表の
  全欄（需要・落下・provider・win内在・win3c主張フラグ）が正本と一致。
- **safe8全根の「生成witness被覆==内在被覆」がmismatch 0で確定**した
  （K1097の39,255根サンプリングを120,474根全数に拡張）。今後の第5〜
  第Nラウンド掃引・greedy再解決のpool被覆簿記は独立に全域保証された。
- 正本の27 gateはすべてok。K1086/K1089/K1091/K1095のノード総計は
  各per-probe記録の独立総和と一致した（台帳の算術的整合）。
- 監査正本は同一cwd 2回＋別cwd別プロセス1回の計3実行でbyte-identical
  （SHA-256 `d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b`）。
  実行は約39〜70秒/回。

## 解釈規約

第二検証は計画簿記の独立性を高めるが、**行を1つも閉じない**: greedy/witness
選定は条件付き計画（候補根の簿記）であり証明書ではない。REFUTED-D10は
LOSS証明ではなく、nodes数・solved数を勝敗として読まない。信任境界は
出版corpusと同一（engine depth-10 verdict健全性＋D4不変性）。第1〜3ラウンドの
代替根集合はK1097機械と同じ上流正本経由（K1088/K1090/K1094の再実行は対象外）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。残余72行は全行open。**

## 成果物

- `research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/`
  （README・scripts/verify_refuted50_second.py・output/refuted50-refsolve-second-verification-20261120.json）
- `research/knowledge/items/K1102-n11-residual72-refuted50-refsolve-second-verification.md`
- 単一オーナー宣言ノート（commit de8c44ac96・先行出版済み）
