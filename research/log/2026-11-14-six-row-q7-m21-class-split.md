# 2026-11-14 six-row q=7 m=21 class-split witness (K0815 第7弾)

高速レーン第8回・第2成果。K0818 の class-split 機構を q=7 に初適用し、(6,7) の
未決着前線 6x21 を攻撃した。

- **6x21 q=7 class {2} SAT（1,904,706 conflicts・98.6秒）**: 35石欠損極大witness
  （行構成 6,6,5,6,6,6）を発見 → **M_{6,7} ∈ [22,402]**（旧 21..402）。
- 2系統独立検証（JS census不使用 verifyConfig・Python Fraction）とも safe+maximal PASS。
- 正制御: 6x20 q=7 class {2} が 641,859 conflicts・29.1秒で SAT・K0815 第2弾の
  witness盤を同経路で再発見（2系統検証PASS）。符号化→ソルバ→decode→検証の全経路検証。
- 単一の巨大インスタンス（第2弾 def+lex 4.55M 未決着）が class分割で99秒決着 —
  分割の難度崩壊効果の q=7 でもの再確認。
- 次前線: 6x22 q=7。class {2} は単発280秒 5,038,264 conflicts で INDET（非不在）。
  残34クラス未走査。krow/minpos 分割か lex 併用が次の一手。
- 併せて本セッションでは K0819（6x20 q=8 全35クラス UNSAT・witness-free {19,20}）を
  反映済み。実験: research/experiments/six-row-q7-m21-class-split-20261114/。
