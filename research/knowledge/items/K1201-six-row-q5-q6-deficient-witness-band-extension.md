---
id: K1201
title: "6xm q=5,6 row-deficient witness bands — q=5: 6x8..6x28, q=6: 6x8..6x24; M_{6,5} >= 29, M_{6,6} >= 25 (K0808 open cases resolved SAT)"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases:
  - six-row q5 q6 SAT frontier band extension
  - K0808 open greedy non-discovery cases resolved
relations:
  - type: depends_on
    target: K0808
    note: 下界の直接の前段。greedy witness 帯 (6,5) m=8..19・(6,6) m=8..15 と、greedy が発見できず「存在是非は未解決」と明記していた 2 幅 ((6,5) 6x20・(6,6) 6x16) を引き継ぎ、両方とも SAT 存在で決着した。
  - type: depends_on
    target: K0810
    note: sat2.js def-mode 符号化（全三つ組 census・逐次カウンタ・極大性）。def 単一節は「合計石数 < 6(q-1) ⟺ ∃行 ≤ q-2」の完全符号化であり、UNSAT ならその幅の行欠損極大安全配置の非存在の完全証明、SAT なら有限存在証明。
  - type: depends_on
    target: K0829
    note: rowY=0/1/2 行固定分割（V-鏡映 y↔5-y で3クラスが全6行を被覆）。(7,5)/(7,6) 前線解決と同一の被覆論を (6,5) m=28 に適用し成功（7例目）。
  - type: depends_on
    target: K0318
    note: 上界の代入元。U_{6,5}=658・U_{6,6}=495 は本項では変更しない。
artifacts:
  - path: research/experiments/six-row-q5-q6-frontier-20261120/README.md
    role: proof
    note: claim・手法・較正・結果・スコープ。(6,5)/(6,6) の掃引全記録。着手時境界 M_{6,5}∈[20,658]・M_{6,6}∈[16,495] からの更新。
  - path: research/experiments/six-row-q5-q6-frontier-20261120/output/records.jsonl
    role: data
    note: 29 レコード。各レコードに tag・生成 meta（vars/clauses/curves）・CNF md5・kissat conflicts・cap・sec・SAT witness 石配置・3系統検証（js verifyConfig/py Fraction/TS BigInt）の生出力を埋め込み。INDET 6件は cnf_deleted:true の正直な cap 内未解決記録。
  - path: research/experiments/six-row-q5-q6-frontier-20261120/scripts/run65.sh
    role: source
    note: 1 instance runner。sat2.js 生成→kissat 4.0.4 cap 実行→records.jsonl 追記→SAT 時 sat3.js decode + 3系統検証。--lex=H・kissat --sat 構成は探索支援のみで witness 正当性は 3系統検証にのみ依存。
  - path: research/experiments/six-row-q5-q6-frontier-20261120/scripts/recorder.py
    role: source
    note: レコード組立。生成器 md5 pin 表記と INDET 時 cnf_deleted 記録を含む。
  - path: research/experiments/six-row-q5-q6-frontier-20261120/scripts/jsverify.cjs
    role: verifier
    note: 第1系統 sat.js verifyConfig ドライバ（census 不使用）。
  - path: research/experiments/six-row-q5-q6-frontier-20261120/scripts/pyverify.py
    role: verifier
    note: 第2系統 verify_witness.py ドライバ（純Python Fraction・repo md5 0530d166… pin の上流をそのまま呼ぶ）。
  - path: research/experiments/six-row-q5-q6-frontier-20261120/scripts/tsverify.mjs
    role: verifier
    note: 第3系統 verify_independent.ts ドライバ（純TS/BigInt・repo md5 b918dc50… pin・node --experimental-strip-types）。
  - path: research/log/2026-11-20-six-row-q5-q6-frontier.md
    role: source
    note: 単一オーナー宣言（13:25Z・commit 796cbb46）と掃引・出版の記録。
scope: "有限機械検証: sat2.js def-mode（K0810 完全符号化）+ kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。SAT 15 幅（(6,5) m=19..27 def・m=28 rowY=0・(6,6) m=16..24 def）は全て witness 3系統検証済み。INDET 6件（(6,5) m=28 def・m=29 rowY=0/1/2・(6,6) m=25 def/rowY=0(×3)/rowY=1/rowY=2 のうちの記録済み分）は cap 130〜240s 到達の未解決記録で不在主張ではない。上界は K0318 代入（U=658/495）不変。6xm の真の安定化長の全帯閉包・標準11×11空盤には一切言及しない。"
evidence: "K0808 出版 witness（6x19 q5・23石・6x15 q6・29石）の3系統再検証全PASS（陽性対照）+ 実行環境リセット2回を跨いだ def-mode conflicts の byte-exact 再現（m=20..27: 750/985/657/15,541/17,610/19,169/20,212/89,830・同一スクリプト/バイナリ md5）+ 全 SAT witness の3独立系統検証（sat.js verifyConfig・verify_witness.py Python Fraction・verify_independent.ts 純TS/BigInt・全レコードに生出力埋め込み）+ CNF md5 pin（再生成検証可能）。--lex=H symmetric breaking と kissat --sat 構成は SAT witness の科学的主張に影響しない（検証は発見後の独立幾何検査のみに依存）。"
---

# 6xm q=5,6 行欠損極大 witness 帯の SAT 延伸 — M_{6,5} ≥ 29・M_{6,6} ≥ 25

## 命題・範囲

w×m 格子盤・q点共円/共線禁止の行欠損極大安全配置（row-deficient maximal safe
configuration）に関して:

1. **(6,5)**: m=8..28 の全幅で witness が存在する（m=8..19 は K0808 greedy・
   m=19..27 は本項の def-mode SAT・m=28 は rowY=0 行固定分割 SAT）。
   **M_{6,5} ∈ [29, 658]**（着手時 [20, 658]）。
2. **(6,6)**: m=8..24 の全幅で witness が存在する（m=8..15 は K0808・
   m=16..24 は本項 def-mode SAT）。**M_{6,6} ∈ [25, 495]**（着手時 [16, 495]）。
3. K0808 が greedy（≤1000 restart）で発見できず「存在是非は未解決」としていた
   2 幅はいずれも **witness 存在** で決着: (6,5) 6x20（750 conflicts・0.6s・
   23石）・(6,6) 6x16（46 conflicts・0.1s・29石 rows [5,4,5,5,5,5]）。
4. 副次的: (6,19,5) の def SAT witness は 22石深欠損（rows [4,4,4,2,4,4]）で、
   K0808 が記録した m=19 の greedy min 23 を改善し、m=19 の行欠損極大の
   最小石数は ≤ 22 と確定。同様に (6,20,6) の witness は 28石（rows
   [5,3,5,5,5,5]）。いずれも最小性の主張ではない（def-mode は石数を
   最小化しない）。

## 現在の根拠と限界

- 根拠: experiments/six-row-q5-q6-frontier-20261120（sat2.js md5 282ae832…・
  kissat 4.0.4 md5 3a5eba83…・3系統検証・29レコード）。
- 前線の未解決記録（いずれも不在主張ではない）:
  - (6,5) m=29: def-mode 無実施（m=28 def 240s INDET 894,706 を参照）・
    rowY=0 220s INDET 720,202・rowY=1/2 --sat 130s INDET 502,044/469,125。
  - (6,6) m=25: def 140s INDET 857,314・rowY=0 140s INDET 860,873（--lex=H
    838,046・--sat 1,014,217）・rowY=1/2 --sat 130s INDET 951,654/929,165。
- 限界: SAT witness の存在証明は有限。帯の全体閉包（M の確定）には前線の
  UNSAT 証明または上界の改善が必要。--sat 構成は witness 探索支援であり
  UNSAT 性能を意図しない。

## 観測（全称主張ではない）

- (6,5) def-mode conflicts は m=22 (657) < m=20 (750) < m=21 (985) ≪
  m=23 (15,541)..m=27 (89,830) と非単調で、m=28 def は cap 240s でも
  未解決（894,706）なのに rowY=0 分割は 146.1s で SAT（464,040）。
  (7,5)/(7,6) に続く「OR 前線は行固定分割で突破できる」観察の
  6行版の実例（rowY 成功は7例目）。
- (6,6) m=16 が 46 conflicts で SAT な一方、m=23/24 は 90万/89万 conflicts
  を要し、m=25 は全構成で cap 内未解決。witness 密度の幅方向の疎化が
  観察される（Q> w の witness-free 帤出現（K0824 等）と整合的な定性的
  転移の前段である可能性があるが、本項では主張しない）。
- greedy 最小石数の改善例（m=19 q5: 23→22 実在、m=16〜20 q6 の 29石に
  代わる 28石実在）は、greedy min が真の最小でないことの実例。

## 備考

- K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
- 単一オーナー宣言: research/log/2026-11-20-six-row-q5-q6-frontier.md
  （13:25Z・commit 796cbb46）。
