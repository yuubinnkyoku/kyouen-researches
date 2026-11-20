---
id: K1106
title: 残余68行のWIN8-D10証明書抽出 root 8005021（三重検証・19 gate・初の正真正銘第二WIN8証明書）
kind: experiment
status: verified
topics: [search-methods, certificates]
aliases:
  - WIN8 cert extract root 8005021
  - greedy計画順2位8石rootの完全勝利戦略26,083行
relations:
  - type: depends_on
    target: K1085
    note: K1086 addtwo-greedy23掃引の入力census。本項ではK1086正本（SHA-256 3045e152…）のper_root記録を直接pin
  - type: depends_on
    target: K1086
    note: 両AND順序uncapped probe（619,138/751,581・loss=true）の出版値を本環境でnode-exact再現
  - type: depends_on
    target: K1096
    note: 抽出器・BigInt検証器・Bareiss検証器・監査機械の機材はK1096実験と同一bytes（root定数のみ差し替え+g19追加）
  - type: depends_on
    target: K1097
    note: win16 footprint（root 8005021: claimed == intrinsic == 3行）をg19で照合。
  - type: relates_to
    target: K1105
    note: fold11直後の残余68行レーン。root 8003180のfoldとは別root・独立プロセス
artifacts:
  - path: research/experiments/n11-residual72-win8-cert-extract-root8005021-20261120/README.md
    role: source
    note: プロトコル・入力pin・結果・再現方法・解釈上の制限
  - path: research/experiments/n11-residual72-win8-cert-extract-root8005021-20261120/certs/win8-root-00000000000000003800000008005021-20261120.n11
    role: certificate
    note: 945,298 bytes・26,083行・SHA-256 69f32661…
  - path: research/experiments/n11-residual72-win8-cert-extract-root8005021-20261120/output/win8-cert-extract-verification-20261120.json
    role: data
    note: 19/19 gate監査正本（3実行byte-identical・SHA-256 0bd2dd10…）
  - path: research/experiments/n11-residual72-win8-cert-extract-root8005021-20261120/scripts/cert_extractor_win8_root8005021.ts
    role: source
    note: K1096抽出器のroot差し替え版（探索核同一bytes）
  - path: research/experiments/n11-residual72-win8-cert-extract-root8005021-20261120/scripts/assemble_win8_audit_root8005021.py
    role: verifier
    note: 第三方法監査機械・python stdlibのみ・g19追加
  - path: research/log/2026-11-20-n11-residual72-win8-cert-extract-root8005021-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 7ffddc66・先行出版）
  - path: research/log/2026-11-20-n11-residual72-win8-cert-extract-root8005021.md
    role: log
    note: 発見・実行・再現・限界の研究記録
---

# WIN8-D10 root 8005021 証明書抽出・三重検証

単一オーナー宣言ノート（commit `7ffddc66`・先行出版）の下で、K1086 addtwo-greedy23掃引が
両AND順序 uncapped（andclose1 619,138・andclose0 751,581・どちらも loss=true）で
WIN8-D10 candidate として確定した greedy計画順2位の 8石root `00000000000000003800000008005021`
（石 [0,5,12,14,27,59,60,61]・quadruple-free・D4正準・loser初手41手）に対して、
完全勝利戦略証明書の盲抽出と三重検証を行った。fold11（K1105）直後の残余68行レーンで、
証明済み1根（K1096）と並走宣言済み2根を除く候補中で最上位の未着手根である。

**結果**: 証明書 26,083行・945,298 bytes（SHA-256 `69f32661…`・3実行byte-identical）。
抽出は A1（初手毎41プロセス・総nodes 3,272,039・fbt_drops 0）・A2（完全再実行・初手単位
node-exact一致）・B（単一プロセス・総nodes 2,876,091・戦略行不変）の3実行で行集合が完全一致。
三重検証（TS BigInt 3×3余因子・TS Bareiss 4×4・python第三方法全木再走査）が
visited 59,594・winner-to-move 38,442・loser-to-move 10,961・loser応手辺 53,352・
終端 10,191（全てloser-stuck）・終端石数 [14,18]・consumed union 26,083 == 証明書行
（missing 0/extra 0）の全数値で一致。監査機械（K1096機械のroot差し替え+g19追加）は
**19/19 gate PASS**（probe再現のK1086出版値node-exact一致・root mobility 41の独立再導出・
行format sorted-unique・証明書SHA pin・K1097 win16 footprint三点一致を含む）で、
同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical（SHA-256 `0bd2dd10…`）。

解釈上の制限（不変）: 本証明書は当該8石rootのゲーム木のみを証明する。S6親行の
被覆幾何・fold（fold12候補）は別工程であり、行の閉鎖claimは本項では行わない。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
