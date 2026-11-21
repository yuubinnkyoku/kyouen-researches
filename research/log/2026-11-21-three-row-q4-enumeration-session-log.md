# Three-row q=4 enumeration closure — session log (2026-11-21, 高速レーン)

単一オーナー宣言: `research/log/2026-11-21-three-row-q4-enumeration-single-owner-note.md`
（7b5bdfec・宣言時 HEAD a8e4b0a6・受入条件5項目）に従う出版セッションの記録。
正本: [three-row-q4-enumeration-20261121](../experiments/three-row-q4-enumeration-20261121/README.md)・
知識項目 [K1183](../knowledge/items/K1183-three-row-q4-witness-band.md)。

## 成果（掃引・検証は fresh run・第二実行環境）

1. **witness-free 幅 {24,25,26,27} の確定**（列挙閉包・SAT 非依存・新結果）:
   P(25), P(26), P(27) が今回新規に成立。P(24) は SAT frontier レーン（行和63分割・kissat）
   と独立な第二方法で一致。
   - family 9プロファイル (3,3,a): m=24..27 × Y∈{0,1,2} 全掃引、全 0 witness。
   - fast 13プロファイル（(3,a,b) 置換 + (2,2,2)）: m=13..27 全掃引で全 0
     （dx_sweep_13_23.jsonl 143/143 + dx_sweep_24_27.jsonl 52/52）。
     m ≥ 13 の def-mode witness は family 型のみ、と簡約。
   - lemma 41プロファイル（石数和 k≤5）: crossing-supply 補題
     D(m)=Σ(m−rᵢ) > 2·nDef·C(k,3) が m≥22 で41/41算術キル
     （m=21 では9プロファイル残る・killed 32/41）。
   - **M_{3,4} ∈ [24, 69] は不変**（P の幅単調性は未証明・m≥28 は未掃引）。
2. **検証チェーン**（crossval_summary.json overall PASS・全機械）:
   - dx34 direct ≡ brute_3x{4..8}（全プロファイル一致・def totals 182/674/1724/4607/11542）。
   - fast ≡ direct: selftest m=4..12、13プロファイル×全幅 mismatch 0。
   - wsearch34 ≡ brute family: m=4..8 × Y×a 15実行一致。
   - m=23 陽性対照: family witness Y=0:2件・Y=1:4件・Y=2:2件、各2系統検証 PASS
     （sat.js verifyConfig + witness_check.py 整数行列式）。**Y=0 第2 witness が
     先行出版 wit_3x23_outer_4 と石集合 byte-exact 再発見**（独立方法による witness 再現）。
   - closure_check.py validate: 補題キルは m=4..12 の全数列挙と矛盾 0。

## 出版と事故の記録（透明性のため）

- 出版は part 1..7 に分割し各回 fetch-back md5/diff 照合（全33ファイルで byte-exact を確認）。
- **part 2 で dx34.js の転写事故が発生**: chunk ペイロードを手書き再構成した際、
  fastFull 内 gC2/gB2 構築部に閉じ波括弧を各1個余分に打鍵（commit dba01978・md5 28fa6227）。
  fetch-back md5 照合（期待 b02235a9 に対し不一致）で即座に検出し、
  正本を `file_system.read_file` で直接読んで修正出版（commit 01ac240c・md5 b02235a9・
  `node --check` PASS・selftest m=4/5 の direct fast 一致を再確認）。
  影響: 破損版は約40分 main に存在したが、該当 commit は実験ディレクトリ新設のみで
  他のレーンからの参照なし。以後の part 3..7 はすべて正本直接読込方式で出版し
  同種事故なし。
- K1183 item: title/scope/evidence/artifacts を witness-free 幅 {24..27}・m≥28 未掃引に
  更新（commit 3b2a768a・fetch-back byte-exact）。
- knowledge README K1183 bullet（377行目）: 追更で列挙閉包の結果・検証チェーンを反映
  （commit 29f1a7b1・python 独立再構成との diff で byte-exact）。

## 運用メモ

- 環境リセットが2回発生（git clone の 120s timeout が引き金）。
  実験正本は knowledge 側（q34-lane-kit/enumeration-20261121）に退避して継続。
  git なし・GitHub 操作は github_app ツール + raw URL fetch-back。
  出版内容は tool sandbox から `file_system.read_file` で正本を直接読む方式が最も安全。

## 次の延伸候補

1. **m=28 の family 掃引**（推定 ~150s/Y・fast は軽量・lemma は m≥22 自動キル）。
   witness-free 28..68 が揃えば M_{3,4}=24 が確定（69=K0024 全称側）。
2. m=21..22 の lemma 残り9プロファイルを fast/direct で掃引すれば
   「m≥13 では family 型のみ」の簡約を m≥21 に強化できる（単調でない幅の理解）。
3. frontier レーンの m=24 中央行系 piece との交叉: 列挙閉包が (3,3,a) と
   (3,a,b)/(2,2,2) を殺しているため、SAT 側の残る必要条件は実質
   「各行 ≥ 2 石かつ最小行 = 2」に絞られる。行和62（(2,3,3) 型）の
   UNSAT との整合記録が両レーンの接続点。
