---
id: K1102
title: 残余72行 safe8第4ラウンド再解決（K1097）の独立第二検証
kind: verification
status: verified
topics: [search-methods, certificates, geometry]
aliases:
  - independent second verification of the residual72 safe8 refuted-50 round-4 refsolve
  - K1097 refsolve round-4 bookkeeping verification
relations:
- type: verifies
  target: K1097
  note: K1097の残余23行再解決・pool P‴簿記・WIN16足跡を独立実装で全量照合する
- type: depends_on
  target: K1085
- type: depends_on
  target: K1086
- type: depends_on
  target: K1089
- type: depends_on
  target: K1091
- type: depends_on
  target: K1095
artifacts:
- path: research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/README.md
  role: source
  note: 対象・入力pin・独立再導入方法・検証境界
- path: research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/scripts/verify_refuted50_second.py
  role: verifier
  note: アンカー並進3×3整数行列式・safe8全数内在被覆再導入・Hopcroft-Karp・独立greedyで42 gateをfail-closed検査
- path: research/experiments/n11-residual72-refuted50-refsolve-second-verification-20261120/output/refuted50-refsolve-second-verification-20261120.json
  role: data
  note: 42/42 gate PASS・3実行byte-identical（SHA-256 d0b5d845…）
- path: research/log/2026-11-20-n11-residual72-refuted50-refsolve-second-verification.md
  role: log
  note: 独立第二検証の結果と限界
- path: research/log/2026-11-20-n11-residual72-refuted50-refsolve-second-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言（commit de8c44ac96・先行出版）
scope: >-
  K1097の計画簿記全体: 残余72行のsafe8 pool再構築・K1086/K1089/K1091/K1095の
  verdict joinと残余宇宙72→49→40→30→23行のexactly-once分割・REFUTED除外50根
  ・pool P‴ = 120,424根・残余23行の需要構造・greedy 9根再解決とscope2・
  WIN16内在足跡。新規probe・掃引・証明書抽出・receipt fold・S6行の閉鎖は対象外。
evidence: >-
  上流5正本（K1085/K1086/K1089/K1091/K1095）をSHA-256 pinでfail-closed読み出し、
  K1097正本をSHA-256・git blob SHA-1の二点pinで固定した。出版済みK1097機械の
  本環境での再実行が出版正本とbyte-identicalであることをまず確認した。
  次に独立実装（アンカー並進3×3整数行列式による4点禁止判定＋72行のBareiss
  4×4交差確認、safe8全根120,474のC(8,6)内在被覆全数再導入と生成witness被覆の
  全域一致、Hopcroft-Karp最大マッチング、4掃引ノード総計のprobe記録からの
  独立総和、greedyの独立走査）で42 gateを検査し全PASSした。greedy 9根の根順序
  ・主張被覆行、needs/gains、WIN16のintrinsic==主張（15根）と余剰1行
  （K1095 3根目・残余23行外）、per-row表の全欄が正本と一致した。
  監査正本は同一cwd 2回＋別cwd別プロセス1回でbyte-identical。これは計画簿記の
  二次照合であり、行のゲーム理論的値や証明書の正しさを確定しない。
---

## 判定範囲

greedy/witness選定は条件付き計画（候補根の簿記）であり証明書ではない。
REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
本第二検証は行を1つも閉じない: 残余72行は全行openのまま。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**

## 主要な独立確定事実

1. safe8 pool全根（120,474）の生成witness被覆がC(8,6)内在被覆と全域一致
   （mismatch 0）。K1097の39,255根サンプリングcrosscheckを全数に拡張した。
2. K1097の全数値（universe82 380,098・safe8 120,474・P‴ 120,424・残余23行の
   需要 min 1,781 / max 2,934 / sum 50,670・stranded 0・provider
   {1: 40,065, 2: 4,857, 3: 297}・greedy 9根 gains {3:6, 2:2, 1:1}・
   マッチング23・scope1=scope2同一選定）が別実装・別アルゴリズムで再現。
3. K1086/K1089/K1091/K1095のノード総計がprobe記録の独立総和と一致
   （18,032,471 / 6,339,079 / 7,383,022 / 5,700,222）。
4. K1086の生主張行のcanonical化がK1085 censusのgreedy計画covered_rowsと
   23根すべてで一致（上流正本間整合）。
