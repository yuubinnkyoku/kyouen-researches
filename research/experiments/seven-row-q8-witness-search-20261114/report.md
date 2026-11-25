# 7×m q=8 行欠損witness探索 — 新ファミリー (7,8) のwitness 7×8..7×24 と M_{7,8} ≥ 25

日付: 2026-11-14（高速レーン第9回・第1バッチ）

## 主張

1. **(7,8)（7×m・q=8・q点共円/共線禁止）**: 行欠損の極大安全配置（満容量
   49 = 7·(q−1) 石に対し総石数 ≤ 48・ある行 ≤ 6 石）が **m=8..24 の全幅で存在する**。
   - m=8..12 は深欠損（38, 38, 45, 46, 47 石・ deficiency 11..2）。
   - m=13..24 はすべて単一欠損の **48石**（行パターンは 6 が1行のみ）。
   - m=24 は def 単一節（OR）符号化が 240s cap で INDET（conflicts 3,829,302・
     lex=H,V,HV でも INDET 3,710,480）だったため、**rowY=3 固定（第4行の欠損を固定）
     に分解**したところ kissat 4.0.4 が 641,005 conflicts（約41秒）で SAT。
   - 全 witness は census 不使用 sat.js verifyConfig と Python Fraction 独立実装の
     **2系統検証で safe+maximal+行欠損 PASS**。
   - よって witness 幅集合は {8..24} を含み、**M_{7,8} ≥ 25**
     （上界は K0318 曲線パッキング代入 U=651・`w7_upper_bounds.json`）。
2. **m=25 は未決着（正直な負記録）**: rowY=3 固定でも 250s cap で INDET
   （3,534,747 conflicts・欠損行は V 対称で 4 クラスあり、他 3 クラスは未走査）。
   不在の主張ではない。

## 手法と検証

- 符号化: `seven-row-inband-families-20261114/scripts/sat2.js`（K0810 census +
  sequential counter + 極大性・def 単一節 ∨¬rowGe[y] は行欠損存在の完全符号化）。
  q=8 = w+1 ≥ w+1 のため genfast.js（半整数中心census・K0820）が適用可能で、
  **q=8 で sat2.js とバイト一致を4サンプル（m=9,12・lex有無）で検証**
  （md5 一致・`output/controls/genfast_q8_byteidentity.json`）。
- ソルバ: kissat 4.0.4 公式 linux-amd64 バイナリ（変更なし・240-250s cap）。
- 制御（`output/controls/records.jsonl`）:
  - 2×8 q=4 def+lex=H,V,HV SAT・fastsat conflicts **121** / 2×9 q=4 def+lex UNSAT・
    fastsat **535** — **K0820 の controls record と bit-exact**（K0796 整合）。
  - 2×8 q=4 def 単独（fastsat SAT 81・kissat SAT 65）/ 2×9 q=4 def 単独
    （fastsat UNSAT 2002・kissat UNSAT 1268）— 両ソルバ判定一致。
  - **インスタンス同一性較正**: (7,10) m=46 def+lex=H,V,HV を再生成し
    kissat UNSAT **861 conflicts** — K0820 の q10-band records.jsonl の記録値と
    bit-exact（vars 8440・clauses 32759 同一）。
- 決定性: 実行環境リセット1回を挟み、m=8..22 の再生成で conflicts が全幅
  bit-exact 一致（191, 824, 140, 292, 601, 4717, 49349, 49711, 681530 …）。
  genfast/sat2 の CNF md5 も一致。

## 結果（def-search/records.jsonl・17レコード）

| m | 石数 | 行パターン | kissat conflicts |
|---|------|-----------|------------------|
| 8 | 38 | 2,5,4,6,7,7,7 | 0 |
| 9 | 38 | 2,4,4,7,7,7,7 | 0 |
| 10 | 45 | 7,7,7,7,7,7,3 | 0 |
| 11 | 46 | 7,7,7,7,7,7,4 | 0 |
| 12 | 47 | 7,7,7,7,7,7,5 | 0 |
| 13 | 48 | 7,7,7,7,7,7,6 | 0 |
| 14 | 48 | 7,7,6,7,7,7,7 | 191 |
| 15 | 48 | 7,7,7,7,7,7,6 | 824 |
| 16 | 48 | 7,7,6,7,7,7,7 | 140 |
| 17 | 48 | 7,7,6,7,7,7,7 | 292 |
| 18 | 48 | 7,7,7,7,7,7,6 | 601 |
| 19 | 48 | 7,7,7,7,6,7,7 | 4717 |
| 20 | 48 | 7,7,7,6,7,7,7 | 49349 |
| 21 | 48 | 7,7,7,6,7,7,7 | 49711 |
| 22 | 48 | 7,7,7,6,7,7,7 | 681530 |
| 23 | 48 | 7,7,7,6,7,7,7 | 1325637 |
| 24 | 48 | 7,7,7,6,7,7,7 | 641005 (rowY=3 分割) |

row-split/records.jsonl に m=24 rowY=3 SAT と m=25 rowY=3 INDET の2レコード。

## 範囲と限界

有限機械検証（census 完全性 — m=8..24 は sat2.js 直接适用範囲だが生成は
genfast.js・バイト一致検証済み — とソルバ正確性まで）。数論的証明ではない。
M_{7,8} の確定には 7×25 以降の持続性評価（witness 探索の前線は **7×25**）と
上界 651 の改善（K0342 型 tail 評価）が残る。def OR 実例の難化は顕著
（m=23 SAT 1.3M → m=24 OR 3.8M INDET）で、以後の帯評価は
行固定分解（4つの V-クラス）を軸にするのが効率的。

## 再現

```sh
./scripts/lean3.sh 7 24 8 output/def-search none   # OR 実例（INDET 240s）
node ../genfast.js 7 24 8 --rowY=3 r3.cnf && kissat r3.cnf  # 分割 SAT
```

sat2.js / sat.js / fastsat.js / verify_witness.py / genfast.js / decode_verify.js は
`seven-row-inband-families-20261114/scripts/` と
`seven-row-q9-q10-bands-20261114/scripts/` から verbatim 使用（scripts/README.md 参照）。
