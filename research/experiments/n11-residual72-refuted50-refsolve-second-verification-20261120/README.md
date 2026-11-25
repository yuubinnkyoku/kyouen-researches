# n11 残余72行 safe8第4ラウンド再解決（K1097）の独立第二検証（2026-11-20）

## 目的

K1097（残余72行 safe8 pool 第4ラウンド再解決・正本 SHA-256
`2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`・
git blob SHA-1 `4660c012333b04896c36a23a0837fbdbc2572ef9`）の
計画簿記全体を、出版済みK1097機械とは独立な実装で再導入し、全項目を正本と
照合する。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-refuted50-refsolve-second-verification-single-owner-note.md`
（commit de8c44ac96fbde0616a216f184dd54b42b3f2c49）の下で実施した。

**第二検証のみを行う**。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖claimは
一切行っていない。REFUTED-D10 は LOSS 証明ではない。標準11×11空盤・二石root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## 手順

1. **実行形再現**: 出版済みK1097機械
   `research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/scripts/safe8_refuted50_refsolve_20261120.py`
   （SHA-256 `f01f459f4f9ec2b9d38c0ed61f14132cf36c870f316d1fae840fe534181192c0`）
   を本環境で再実行し、出力正本が出版SHA-256
   `2896deb0…`（git blob SHA-1 `4660c012…`）とbyte-identicalであることを確認した。
2. **独立第二検証機械**（`scripts/verify_refuted50_second.py`）を新規実装し、
   K1097機械と意図的に別経路で全量再導入した:
   - 4点禁止判定は**アンカー並進3×3整数行列式**（第4点集合独立の
     `(dx, dy, d(x²+y²))` 3×3行列式。原点を通る円の方程式
     x²+y²+ux+vy=0 による零条件で、K1097機械の「3×3余因子4項交替和」と同じ
     4×4行列式の零集合を別経路で計算する）。さらに72基底行については
     **Bareiss 4×4完全整数前進消去**による第二経路で交差確認した。
   - **全数被覆検査**: safe8 120,474根すべてについて C(8,6)=28 部分集合の
     内在被覆を全数再導出し、生成witness被覆と**全域一致**（mismatch 0）を
     要求した。K1097機械のcrosscheckは39,255根のサンプリングだった。
   - 二部最大マッチングは **Hopcroft-Karp**（K1097機械はKuhn増大路）。
   - 4掃引のノード総計（K1086 18,032,471・K1089 6,339,079・K1091 7,383,022・
     K1095 5,700,222）は出版フィールド値でなく**probeレコードからの独立総和**
     として再計算した。
   - greedy被覆はlexicographically-smallest max-gain規則を独立走査で再実装した。
3. 入力5正本をSHA-256 pin でfail-closed読み出し、K1097正本はSHA-256・
   git blob SHA-1の二点pinで読み出した。

## 結果（全42 gate PASS・3実行byte-identical）

- **K1097の全主要値が独立再導入で一致**: universe82 380,098根（生成事象
  471,960）・safe8 120,474根・unsafe8 259,624根・被覆ヒストグラム
  {1: 82,602, 2: 33,104, 3: 4,718, 4: 50}・safe8需要 min 1,714 / max 2,944 /
  sum 163,164・K1085 census欄とも一致。greedy 23根計画は根順序・主張被覆行
  とも byte単位で完全再現。残余宇宙列 72→49→40→30→23行のexactly-once分割、
  REFUTED除外50根、pool P‴ = 120,424根、残余23行、需要 min 1,781 / max 2,934 /
  sum 50,670、stranded 0、provider被覆 {1: 40,065, 2: 4,857, 3: 297}
  （45,219根）、WIN16足跡（15根 intrinsic==主張・K1095 3根目の余剰1行
  `00000000000000003800000008001080` のみ・残余23行への内在被覆0行）、
  scope1 greedy 9根（gains {3:6, 2:2, 1:1}・leftover 0）とscope2同一選定、
  二部最大マッチング23、per-row表の全欄が正本と一致。
- **全数被覆検査でsafe8全根の生成witness被覆==内在被覆が確定**（mismatch 0）。
  K1097の候補poolの被覆簿記は全域で機械保証された。
- 正本の27 gateはすべてok、K1086/K1089/K1091/K1095の構内ノード総計は
  独立総和と一致した。
- 監査正本 `output/refuted50-refsolve-second-verification-20261120.json`
  （SHA-256 `d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b`）
  は同一cwd 2回＋別cwd別プロセス 1回の計3実行でbyte-identical。

## 再現

```sh
python3 scripts/verify_refuted50_second.py \
  --k1085 <K1085 census JSON> --k1086 <K1086 sweep JSON> \
  --k1089 <K1089 sweep JSON> --k1091 <K1091 sweep JSON> \
  --k1095 <K1095 sweep JSON> \
  --k1097canon <K1097 canonical JSON> \
  --k1097machine <K1097 machine .py> \
  --k1097rerun <K1097 machine rerun output JSON> \
  --out output/refuted50-refsolve-second-verification-20261120.json
```

すべての入力はSHA-256 pin でfail-closed検査される。stdlibのみ・乱数・時刻なし。
1実行約39〜70秒（universe82再構築と全数被覆検査が主要費）。

## 解釈規約

1. 第二検証はK1097の計画簿記の独立性を高めるが、**行を1つも閉じない**:
   greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
2. REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
   LOSS証明ではない。nodes数・solved数を勝敗として読まない。
3. 信任境界は出版corpusと同一（engine depth-10 verdict健全性＋D4不変性）。
   第1〜第3ラウンドの代替根集合はK1097機械と同じ上流正本
   （K1089/K1091/K1095のper_root）経由であり、K1088/K1090/K1094の再解決機械の
   再実行は対象外。
4. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
   すべてUNKNOWNのまま。** 残余72行は全行open。
