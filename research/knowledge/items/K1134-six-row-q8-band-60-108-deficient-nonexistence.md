---
id: K1134
title: 6×m・q=8の欠損極大安全配置は幅60..108でも存在しない（witness-free帯 19..108）
kind: proposition
status: proved
topics: [rectangles, variants, maximal-safe, grundy]
aliases: []
relations:
- type: depends_on
  target: K0848
  note: witness-free {19..59} の掃引完了と 6x60 フロンティア・K0821監査規約の鋭い形
- type: depends_on
  target: K0829
  note: def-mode CNF（sat2.js K0810 census + sequential counter + maximality）とrowY被覆論の規約
- type: depends_on
  target: K0815
  note: 6x18 の41石欠損極大 witness（M_{6,8} >= 19 の下界）
- type: depends_on
  target: K0806
  note: 代入上界 U_{6,8}=371（本項では不変）
artifacts:
- path: research/experiments/six-row-q8-band-closure-22-370-20261114/output/band3/records.jsonl
  role: data
  note: m=60..108 の def-mode 49レコード + m=106 lex=H 交差符号化 1レコード（全 UNSAT）
- path: research/experiments/six-row-q8-band-closure-22-370-20261114/output/band3/s6x60q8_none.kissat.txt
  role: proof
  note: 各幅の生 kissat 4.0.4 ログ（49本・rc=20・出力 's UNSATISFIABLE'）
- path: research/experiments/six-row-q8-band-closure-22-370-20261114/scripts/lean6q8.sh
  role: solver
  note: genfast3.js def-mode CNF 生成 + kissat 230s cap（CNFは実行後削除・recordsは本機が追記）
- path: research/experiments/six-row-q8-band-closure-22-370-20261114/scripts/genfast3.js
  role: solver
  note: 弦対抽象円 census（q>=w+2 限定・完全性論はスクリプトヘッダに記載）
- path: research/log/2026-11-20-six-row-q8-band-closure-resume.md
  role: source
  note: 再開log（較正・二重実行のbit-exact性・解釈規約）
---

# 6×m・q=8 の欠損極大安全配置は幅 60..108 でも存在しない

## 主張

1. 6×m 整数格子盤・q=8（8点共円・共線禁止）において、幅 m ∈ {60,...,108} の各幅で、
   def-mode SATインスタンス（欠損行の存在〔安全上の行cap q−1=7・全census曲線で cap 7〕・
   極大性〔全空点が >=7石曲線で被覆〕・単一節 \"∃行 <=6石\"〔sat2.js deficient モード〕）が
   **UNSAT（kissat 4.0.4・rc=20）**。これは各幅に対する 6×m 欠損極大安全配置の
   非存在の完全な決定論的証明である（1インスタンス/幅・INDET 0・SAT 0）。
2. m=106 については --lex=H 交差符号化（列鏡映lex-leader節追加・別変数順序）でも UNSAT
   （conflicts 542,986・54.4s）。符号化を変えても判定は不変であることを代表幅で確認した。
3. 上位被覆論は K0829/K0848 と同一: 極大安全配置が満容量42石でない ⇔ ある行が <=6 石、
   これは def-mode の単一節そのものである（行は「長さ m>=q の直線」だから安全capは行每に 7）。
   よって **6×m・m∈{60..108} の全極大安全集合は42石（各行7石）**。
4. K0818/K0819/K0829/K0848（{19..59}）と合わせて witness-free 幅集合は **{19,...,108}**。
   K0821 監査規約の鋭い形: **M_{6,8} = 19 or M_{6,8} >= 110**（幅60..108を含む全ての
   m' in {20..108} で安定化が始まるには m'−1 に witness が必要だが m'−1 はすべて witness-free。
   109 は掃引外であり M_{6,8} の候補は M=19 のみか M>=110）。上界 371（K0318/K0806 代入）は不変。
   帯掃引は m=109..370 を残す（残り262幅・IN FLIGHT 継続）。

## 数値（全レコード records.jsonl 参照）

- conflicts 系列（def-mode）: m=60: 490,889 → m=65: 657,367 → m=79: 1,032,882（極大）→
  m=83: 1,048,030 → m=96: 678,697 → m=99: 643,094 → m=108: 675,709。
  時間は 26s..79s/幅（230s cap に対して十分小さい・INDET 0）。総解時間 2,732s。
- 曲線数（census）は 2冪の線形増加: m=45: 816 → m=60: 1,216 → m=97: 2,580 → m=106: 2,940
  （各 meta.json と records.jsonl の curves フィールドで照合可能）。

## 検証構造

- **較正（着手中の決定性アンカー）**: 出版済みレコード m=45（2026-11-14T21:18:15Z・conflicts 518,261）
  を同一バイナリ（kissat 4.0.4 official linux-amd64・md5 3a5eba830aa6008a604fcc9bbe99a325）
  で再生成・再解し meta（vars 31,422・clauses 112,417・curves 816）と conflicts 518,261 が
  **bit-exact 一致**。genfast3.js（md5 12c2bd9c…）・sat.js/sat2.js（0cc6021a…/282ae832…）は
  repo正本と同一。
- **二重実行の bit-exact 性**: 本帯は同一環境で2回完全掃引された（1回目 2026-11-20 06:37..07:14Z・
  実行環境でワークスペース喪失、2回目 07:34..08:25Z・出版上の正本）。共有47幅 m=60..106 の
  conflicts は**全幅で完全一致**（例: m=60 490,889・m=83 1,048,030・m=106 656,069）。
  出版するのは2回目の正本であり、1回目は transcripts 上の数値照合にのみ使用した
  （fail-closed: 出版物に欠落・不整合は0・records.jsonl は50行で重複なし。
  重複検査: 1回目の driver が record 二重追記する不具合を持っていたが全二重行は byte-identical
  であり、出版前に機械照合で排除済み）。
- **着地検証**: band3 の全101ファイル（records + 49ペア + lex=H 1ペア）は git blob SHA-1 が
  push後にGitHub側一覧（fields name/sha/size）とローカル sha1(\"blob len\\0\"+bytes) 表で完全一致。

## 解釈規約

- 各幅の UNSAT はその幅単体の完全証明であり、掃引外の幅（109..370）について一切主張しない。
  M_{6,8}=19 の確定には残り全幅の UNSAT か幅371以降の全称証明が必要。
- conflicts/sec 数値は勝敗ではなく決定性のアンカー。SAT換算のwitness価値は本案では発生していない。
- 標準 11×11 空盤・二石root{49,60} 他の未解決局面に本項は影響しない。
