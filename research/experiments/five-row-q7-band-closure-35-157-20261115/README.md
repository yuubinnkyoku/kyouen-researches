# five-row-q7-band-closure-35-157-20261115

IN FLIGHT (claim) — 高速レーン。(5,7) の現在の境界は **19 ≤ M_{5,7} ≤ 158**
（下界 19: K0332 の 5×18・29石・occupancy (5,6,6,6,6) 欠損極大証人・最小不在幅 19 は
K0738–K0759 の 5×19 全 occupancy クラス完全列挙で確定。上界 158: K0332 の同和弦
energy + Melchior による全称証明・SAT に依らない）。witness-free 幅集合は
{19,...,34}（K0738–K0759・K0816・K0821・K0834–K0847 の class-split / 完全列挙）。
本実験は残る帯 **m=35..157（123幅）** を掃引し、**M_{5,7} の完全決着**を狙う
（全幅 UNSAT なら **M_{5,7} = 19 exact・w=5 で初の真の安定化長の完全確定**。
帯内 SAT なら witness 発見として dual-verify して下界を更新し前線を進める）。

## 手法

- CNF 生成: **genfast3.js**（弦対抽象円 census・q≥w+2 限定・
  `six-row-q8-band-closure-22-370-20261114` と同一 blob sha a2fc1cb5・
  `seven-row-q9-band-extension-201-612-20261114` 由来）。(5,7) は q=7=w+2 で
  適用条件を満たす。完全性論は同 script のヘッダ注释（q≥w+2 なら全 q点円が
  ≥2つの double row を持ち、(ya,yb,ℓ,ℓ') の弦対抽象で決まる・4点は自動的に共円）。
  O(C(w,2)·m²·w) で m=157 は秒級。sat2.js 全三つ組 census の OOM 壁を回避。
- 較正（`output/controls/` に記録）:
  - **CNF byte-identity vs sat2.js 全三つ組 census**: 5x18 def / 5x18 def+lex=H,V,HV /
    5x19 def / 5x19 def+lex=H,V,HV / 5x24 def+lex=H,V,HV / 5x34 def の6サンプル全て cmp 0 diff。
  - **陽性対照 instance-identity**: 5x18 def-mode kissat SAT（conflicts 2,412,032・75.6s）、
    decode 29石 witness rows [6,6,6,6,5]（K0332 の occupancy (5,6,6,6,6) と V-鏡像で一致）、
    js census-free verifyConfig + Python Fraction verify_witness.py の二重検証 PASS。
  - **honest negative**: 5x19 def-mode は 230s cap で INDET（6,046,287 conflicts）。
    m=19 の不在は K0738–K0759 の完全列挙が担保（def-OR は小 m で難しい・既知パターン）。
- 帯掃引: 各幅 genfast3 def-mode CNF → kissat 4.0.4（230s cap）→ 記録は
  `output/records.jsonl` に resume-safe に追記。INDET 幅が出た場合は rowY=0/1/2
  行固定分割（V-鏡像 y↔4-y で 3クラスが全5行を被覆・K0829 と同一の被覆論の w=5 版）
  で継続。交差確認は代表幅で def+lex=H,V,HV、決定性は代表幅の再生成・再解 bit-exact。
- ソルバ: kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。

## 進捗

- 2026-11-15: IN FLIGHT claim。較正完了（byte-identity 6/6・陽性対照二重検証 PASS・
  honest negative 5x19）。帯掃引 m=35 から開始。m=35..49 は全幅 def-mode UNSAT
  （conflicts 2,809,004 (m=35) → 漸減 → 1,483,146 (m=49)、cap 内・INDET 0）。
  生ログと records.jsonl は掃引進行に合わせて batch push する。

## スコープ

有限機械検証（genfast3 弦対 census の完全性論 q≥w+2・CNF byte-identity・
陽性対照の witness 再発見、kissat 4.0.4 の正確性まで）。m=35..157 の各幅
def-mode UNSAT はその幅の欠損極大非存在の完全証明。全幅 UNSAT の場合、
witness 幅 {7..18}（K0808..K0815 系）・witness-free {19..34}（class-split 系）・
m≥158 witness-free（K0332 全称上界・証明済み）と合わせて **M_{5,7} = 19 が
exact に決着**する（w=5 初・q=w+2 帯では (6,8) に次ぐ例）。SAT 幅が出た場合は
そこで停止し、witness を dual-verify して下界更新として記録する。
