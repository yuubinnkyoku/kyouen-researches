# four-six-row-q4-q5-band-extension-20261115

IN FLIGHT (claim) — 高速レーン。`four-six-row-q4-q5-witness-search-20261114`
（同族の前レーン）が残した5つの未掃引前線を一括して進める:
sat3.js streaming census で sat2.js の OOM 壁（(5,4) m>=37・(6,4) m>=32）を越え、
(4,4) m=35+・(5,4) m=37+・(6,4) m=32+・(5,5) m=24+・(4,5) m=21+ を
kissat def-mode / rowY 分割 / 構成的列延伸で掃引する。
SAT なら witness を js+py 2系統検証して下界を更新し、
INDET は honest negative として記録し不在主張とはしない。

## 着手時点の境界（main d65002b5 時点）

| family | 現在 | 前線 | 上界 |
|---|---|---|---|
| (4,4) | witness 帯 m=4..34・M ∈ [35, 237] | m=35 | K0068 T_4=237 |
| (5,4) | witness 帯 m=5..36・M ∈ [37, 567] | m=37（sat2 OOM 壁） | K0068 T_5=567 |
| (6,4) | witness 帯 m=6..31・M ∈ [32, 1113] | m=32（sat2 OOM 壁） | K0068 T_6=1113 |
| (4,5) | witness 帯 m=5..20・M ∈ [21, 140] | m=21（rowY 0..3 INDET 55s・rowY=3 200s/2.7M） | K0318 U=140 |
| (5,5) | witness 帯 m=5..23・M ∈ [24, 336] | m=24（INDET 90s/699k） | K0318 U=336 |

## 手法

- 生成器: sat3.js（`seven-row-q4-extension-band-sat3-20261115/scripts/sat3.js`
  md5 18ab1e432bf85f293015922898bb765d を再利用・commit しない）。
  sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c・
  decode_verify.js md5 e355e4b51abe93f7c3f85886360f3baf・
  verify_witness.py md5 0530d166572987988a01ec40dee12d4c も同実験dirから再利用。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64
  （md5 3a5eba830aa6008a604fcc9bbe99a325・GitHub rel-4.0.4・不変）。
- runner: scripts/lean5.sh（本実験で新規・sat3 生成 + kissat + JSONL record +
  SAT 時 decode + js/sat.js verifyConfig と verify_witness.py Python Fraction
  の2系統検証・CNF は実行後削除し cnf_md5 を記録）。
- 構成的延伸: scripts/ext_constructive.js（列追加/シフト純構成・ソルバ不使用。
  前レーンの m=33 off=0 / m=34 off=1 を再現確認済み）。
- 符号化の注記: 前レーンの m>=26 の実行は lex "H,V,HVHV" と記録されているが、
  sat2/sat3 の SIG は {H,V,HV} のみで "HVHV" はフィルタされ、実効符号化は
  [H,V] だった（repo (6,31,4) meta vars=797554/clauses=2651655 が
  --lex=H,V で完全一致・--lex=H,V,HV では一致しないことで確認）。
  判定は等長不変なので結果に影響しない。本レーンは実効符号化を
  記録どおり明示する（デフォルト --lex=H,V,HV）。

## 較正（着手時に実施済み・全 PASS）

- sat3 ≡ sat2 DIMACS バイト一致 11 対照:
  (3,11,5)/(3,12,5)/(4,34,4)/(4,20,5)/(5,23,5)/(5,24,5 rowY=0)/(4,11,8)/
  (5,22,6 rowY=2) lex 付き・(4,20,5 rowY=3)/lex=H・(6,32,4 lex=H)。
  さらに repo meta 一致: (6,31,4) lex=H,V で vars/clauses/curves 完全一致。
- kissat 既知閾値コントロール 8 点中 7 点再現
  ((3,5) 11 SAT/12 UNSAT・(4,8) 10 SAT/11 UNSAT・(4,6) 15 SAT/16 UNSAT・
  (3,4) 23 SAT 66,895 conflicts bit-exact)。残る 1 点 (3,4) m=24 は 120s INDET —
  前レーンの既知 honest negative（def-mode UNSAT は K0351 全列挙で閉じた幅でも
  難しい）と整合。
- lean5.sh 端到端: (6,31,4) SAT・js+py 2系統検証 PASS。
- ext_constructive.js: m=32 base → m=33 off=0・m=34 off=1 を repo 構成記録どおり再現。

## スコープ

有限機械検証まで。各幅の SAT はその幅の欠損極大安全配置の存在証明
（witness 有限証拠）。INDET は cap 到達であり不在を意味しない。
上界（K0068 parity / K0318 substitution）は不変。
