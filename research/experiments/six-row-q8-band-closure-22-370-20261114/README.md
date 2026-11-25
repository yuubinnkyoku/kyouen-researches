# six-row-q8-band-closure-22-370-20261114

IN FLIGHT (claim). (6,8) の現状: 41石欠損極大 witness は 6x9..6x18（K0810/K0815）、
witness-free 幅集合 {19,20,21}（K0818/K0819 の35正準クラス完全列挙・K0829 の3鏡像
rowY クラス）、上界 **U_{6,8}=371**（K0318 代入・K0806 proved）。本実験は残る帯
**m=22..370** を掃引し、**M_{6,8} の完全決着**（全幅 UNSAT なら M_{6,8}=19 exact・
w=6 で初の真の安定化長の完全確定。帯内 SAT なら witness 発見として下界更新・
dual-verify して前線を進める）を目指す。

## 手法

- CNF 生成: **genfast3.js**（弦対抽象円 census・q≥w+2 限定・`seven-row-q9-band-extension-201-612-20261114`
  から verbatim・commit d06d8015系）。(6,8) は q=8=w+2 で適用条件を満たす。
  生成 O(C(w,2)·m²·w) — m=370 で秒級・sat2.js の全三つ組 census（n=2220 で OOM）を回避。
- 較正（本実験で実施・`output/controls/` に記録）:
  - **CNF byte-identity vs sat2.js 全三つ組 census**: 6x19 def / 6x21 def / 6x21 rowY=1 /
    6x24 def / 6x24 def+lex=H,V,HV / 6x30 def+lex=H,V,HV の6サンプル全て cmp 0 diff。
  - **instance-identity**: 6x18 def-OR 陽性対照 SAT 492,432 conflicts（K0829 記録と
    bit-exact・41石 rows 7,7,7,7,6,7 盤の再発見）・6x21 rowY=1 UNSAT 2,862,649 conflicts
    （K0829 最難クラス記録と bit-exact）。
- m=22 の攻略順: def-OR → rowY=0/1/2（V-鏡像3クラスで全6行を被覆・K0829 と同一の
  被覆論）→ それでも INDET のクラスは --lex=H,V,HV 交差符号化と
  K0818/K0819 の k/minpos クラス細分割で継続。
- 帯掃引 m=23..370: 各幅 genfast3 def-mode CNF → kissat 4.0.4（230s cap）→
  全幅 UNSAT で INDET 0 を目指す。交差確認は代表幅で def+lex=H,V,HV、
  決定性は代表幅の再生成・再解 bit-exact。
- ソルバ: kissat 4.0.4 official linux-amd64。

## スコープ

有限機械検証（census 完全性は q≥w+2 の弦対引数・CNF byte-identity・instance-identity
較正、kissat 正確性まで）。m=22..370 の各幅 UNSAT はその幅の行欠損極大非存在の完全証明。
全幅 UNSAT の場合、witness 幅集合 {9..18}（K0810/K0815）・witness-free {19,20,21}
（K0818/K0819/K0829）・m≥371 witness-free（K0318 代入 U=371・K0806）と合わせて
**M_{6,8} = 19 が exact に決着**する。SAT 幅が出た場合はそこで停止し、witness を
dual-verify（sat.js census-free verifyConfig + verify_witness.py Python Fraction）して
下界更新として記録する。

## scripts

- `genfast3.js` — verbatim from seven-row-q9-band-extension-201-612-20261114
  (chord-pair abstract-circle census; O(C(w,2)·m²·w); asserts q>=w+2).
- `lean6q8.sh` — 1幅 def-mode 実行（genfast3 CNF + kissat 230s + records.jsonl append +
  SAT なら decode+dual-verify）。
- `leanrow6q8.sh` — rowfixed 実例（--rowY=Y・240s cap）。K0829 と同一の被覆論。
- `batch6q8.sh` — 連続幅帯掃引（wall-clock GUARD 付き）。
- `decode_verify.js` — verbatim from eight-row-bands-20261114/scripts。
- sat.js / sat2.js / verify_witness.py は複製せず
  `seven-row-inband-families-20261114/scripts/` を SEVEN_SCRIPTS 経由で使用。

## 進捗

- 2026-11-15: IN FLIGHT claim。較正完了（CNF byte-identity 6/6・instance-identity 2/2）。
  m=22 攻略と帯掃引 23..370 は後続コマンドで実施。
