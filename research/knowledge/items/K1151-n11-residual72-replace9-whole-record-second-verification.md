---
id: K1151
title: 残余23行 代替9根d10掃引（K1146）whole-record独立第二検証: 334 gate全PASS・残余72→20行連鎖の独立再導入・5掃引横断census（75根・WIN17/REFUTED58衝突0・pool P⁗ 120,416）・win16 intrinsic footprint再現・新WIN8-D10候補のintrinsic footprint初計測
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - whole-record independent second verification of the replace9 depth-10 sweep (K1146): published masters and 18 probe records SHA-pinned and cross-checked by a separate implementation; residual universe chain 72-49-40-30-23-20 independently re-derived; 75-root cross-sweep census WIN17 vs REFUTED58 canonical conflicts 0; pool arithmetic safe8 120,474 - 50 - 8 = 120,416 reproduced; win16 intrinsic footprints reproduced; new WIN8-D10 candidate intrinsic footprint first measured (== claimed 3 rows, surplus 0)
relations:
  - type: verifies
    target: K1146
    note: 代替9根depth-10掃引の出版正本（e8f5d674…）と18 probe記録（bdacf0e7…）のwhole-record二次照合。掃引機と別実装でper_root数値・verdict分類・残余23行exactly-once被覆・gains hist・nodes総計3,574,172・terminal union [14,18]を全数検査
  - type: depends_on
    target: K1097
    note: refsolve正本（2896deb0…）のper_row帳簿・greedy選定・win16 intrinsic footprints・除外50根リスト・pool算術の照合に使用
  - type: depends_on
    target: K1147
    note: 外部検証監査正本（17dbd6ab…）・8根被覆判定正本（c5aaf83e…）の残余着手12行hex・数え上げ証明書算術・availability表との交叉照合に使用
artifacts:
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/README.md
  role: document
  note: 実験README（10入力pin表・5検査群・334 gate・trust境界・再現手順）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/scripts/verify_replace9_whole_record_20261120.py
  role: verifier
  note: whole-record第二検証機（出版掃引機と別実装・stdlibのみ・fail-closed・10入力SHA-256 pin・334 gate・乱数・時刻・環境依存出力なし・SHA-256 e92fb755…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/replace9-whole-record-second-verification-20261120.json
  role: data
  note: 監査正本（SHA-256 5888afb3…・115,002 bytes・334 gate全PASS・残余宇宙72/49/40/30/23/20行hex全リスト・75根census表・WIN17/REFUTED58 verdict表・interpretation_guard 5文言同梱）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1085.json
  role: data
  note: 入力スナップショット（K1085 base残差正本・SHA-256 5fdd342d…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1086.json
  role: data
  note: 入力スナップショット（K1086 greedy23掃引正本・SHA-256 3045e152…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1089.json
  role: data
  note: 入力スナップショット（K1089 replace16掃引正本・SHA-256 808fbda1…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1091.json
  role: data
  note: 入力スナップショット（K1091 replace15掃引正本・SHA-256 edd7ac84…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1095.json
  role: data
  note: 入力スナップショット（K1095 replace12掃引正本・SHA-256 335eca5e…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1097.json
  role: data
  note: 入力スナップショット（K1097 refsolve正本・SHA-256 2896deb0…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-replace9.json
  role: data
  note: 入力スナップショット（K1146掃引正本・SHA-256 e8f5d674…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-probe-records-replace9.jsonl
  role: data
  note: 入力スナップショット（K1146 18 probe記録・SHA-256 bdacf0e7…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-cover-decision.json
  role: data
  note: 入力スナップショット（8根被覆判定正本・SHA-256 c5aaf83e…）
- path: research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/.input-k1147-external-audit.json
  role: data
  note: 入力スナップショット（K1147外部検証監査正本・SHA-256 17dbd6ab…）
- path: research/log/2026-11-20-n11-residual72-replace9-whole-record-second-verification.md
  role: log
  note: 実行記録（宣言参照・検査群別結果・周辺レーンとの補完関係・宣言ノートSHA転写誤記の訂正記録）
- path: research/log/2026-11-20-n11-residual72-replace9-whole-record-second-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit edc231213f・2026-11-20T14:29:00Z・先行出版）
scope: >-
  K1146（残余23行代替9根depth-10掃引）のwhole-record独立第二検証。出版済み正本
  （掃引正本・18 probe記録）+ 前段5正本（K1085/K1086/K1089/K1091/K1095/K1097）+
  被覆判定正本・K1147外部監査正本の計10入力をSHA-256 pinで固定し、出版掃引機と
  別実装の照合機で334 gateを検査する。DFPNエンジンの再実行・新規probe・掃引・
  証明書抽出・receipt fold・行の閉鎖は含まない。検査対象は出版記録の帳簿整合・
  残余宇宙連鎖の独立再導入・被覆幾何・5掃引横断verdict census・intrinsic
  footprint。trust境界は出版記録の二次照合（エンジン健全性は並走の再実行レーン
  K1149管轄）。
evidence: >-
  （1）入力固定: 10入力すべてSHA-256 pin一致（k1085 5fdd342d…・k1086 3045e152…・
  k1089 808fbda1…・k1091 edd7ac84…・k1095 335eca5e…・k1097 2896deb0…・replace9
  e8f5d674…・probes bdacf0e7…・decision c5aaf83e…・k1147audit 17dbd6ab…）。
  （2）probe記録経路: 18 probes（9根×両AND順序）と掃引正本per_rootの全数値一致
  （nodes/loss/capped/terminalStoneRange・ms/wall_s除く）・pilot_d6制御
  （nodes 3,402・loss=false・capped=false）・生child hex規約
  （child==root−最低セットビット）・verdict再分類（WIN⇔両順序uncapped
  loss=true）・nodes総計3,574,172・terminal石数union [14,18]。
  （3）残余宇宙連鎖の独立再導入: base72→49→40→30→23→20行。各ラウンドのWIN主張+
  REFUTED主張が当時の残余宇宙のdisjoint exactly-once分割であることを104 gateで
  行ごとに機械検証（K1086 WIN7根23行・K1089 WIN3根9行・K1091 WIN3根10行・
  K1095 WIN3根7行・K1146 WIN1根3行+REFUTED8根20行）。残余23行はK1097帳簿と集合一致、
  残余20行のうち12行はK1147監査の残余着手12行hexと一致。
  （4）被覆幾何: 9根すべてpopcount 8・D4 min-canonical・quadruple-free
  （C(8,4)=70四点組の4×4整数行列式・Bareiss）・主張行は6石でrootのD4像の部分集合・
  27主張が残余23行のexactly-once被覆・gains hist {3:6, 2:2, 1:1}・K1097 greedy
  選定==掃引9根の根本一致。
  （5）5掃引横断census（本検証の独立成果物）: 掃引済み75根のD4正準形一意性・
  quadruple-free再検証・累積WIN8-D10 candidate 17根（主張52行）と累積REFUTED-D10
  58根の正準形空間衝突スキャン（衝突0）・pool算術 safe8 120,474 −除外50 = 120,424
  〔P‴〕、−REFUTED総58 = 120,416〔P⁗〕の再計算・K1097除外50根リストの恒等性・
  宇宙簿計の独立再計算（生成事象150,765==23×C(115,2)・137,959==45,263+92,696・
  45,219==45,263−44・50==44+6・50,670==40,065·1+4,857·2+297·3）。
  （6）intrinsic footprint: K1097 win16のbase72宇宙上intrinsicを独立再計算し
  15根がintrinsic==主張・K1095第3根 `0000000800000000380000000810000a` が主張1行+
  余剰1行（K1086 WIN根 `00000000000000003800000008003180` の主張行）であることを
  再現。新WIN候補（K1146 root `00000000010000809002000040002001`）のintrinsic
  footprintを初計測: intrinsic==主張3行・residual23内余剰0行
  （round-5 refsolve計画の需要構造の定量基礎）。
  （7）決定性とfail-closed: 検証機はstdlibのみで乱数・時刻・環境依存の出力なし。
  同一cwd 2回+隔離cwd/隔離HOME 1回+PYTHONHASHSEED=random（隔離）の計3以上実行で
  監査正本byte-identical（SHA-256 5888afb3…・115,002 bytes）。334/334 gate PASS。
  改ざんテストで正本nodes+1がpin gateで捕捉されることを確認。
  本検証は行を1行も閉じない。WIN8-D10 candidateは抽出・二重検証・receipt foldを
  経るまで証明書ではない。REFUTED-D10はLOSS証明ではなく、nodes数・solved数を
  勝敗として読まない。greedy選定は条件付き計画簿記である。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
  UNKNOWNのまま。
---

## 詳細

単一オーナー宣言ノート（commit `edc231213f`・2026-11-20T14:29:00Z・先行出版）の
下で、K1146残余23行代替9根depth-10掃引（commit `e9ea153bc4` 系で出版・掃引正本
SHA-256 `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`）の
whole-record独立第二検証を実施した（K1102・replace16独立第二検証・
candidate-supply whole-record第二検証と同じ第二検証枠組みの継続）。

掃引機（runner v17）の再実行は行わない。出版正本と18 probe記録のみをSHA-256 pin
で読み、別実装の照合機（stdlibのみ・fail-closed・334 gate）で
(1) probe記録経路、(2) 残余72→49→40→30→23→20行の連鎖独立再導入、
(3) 9根の被覆幾何、(4) 5掃引横断verdict census、(5) win16+新WIN候補のintrinsic
footprint、を検査し、全gate PASSで完了した。

並走レーンの全probe再実行第二検証（K1149・両AND順序18 probes再実行・pristine
re-assemble byte-identical）はエンジン出力側の独立検証であり、本項は出版記録の
帳簿・幾何・census側の独立検証で補完関係にある。両者の報告するnodes総計
3,574,172・WIN8-D10 candidate 1根・REFUTED-D10 8根は相互に一致する。

### 新規の定量的成果

1. **5掃引横断census**: 75根のD4正準形一意性・quadruple-free・WIN17 vs REFUTED58
   の正準形衝突0を、5掃引（greedy23・replace16・replace15・replace12・replace9）の
   出版正本5種の向量を横断して初めて一つの表に束ね、cumulative pool算術
   （120,474→120,424→120,416）を単一の機械で再計算した。
2. **新WIN8-D10候補のintrinsic footprint初計測**: base72宇宙上のintrinsicが
   主張3行に等しく余剰がない。第5ラウンドrefsolve（残余20行・pool P⁗ 120,416根）
   の需要構造の変化はこの根のreceipt foldが主張3行ぶんのみであることを示す定量
   基礎となる。
3. **採番の協調**。本項のK番号K1151は、K1149の二重採番（後着six-rowレーン）
   の再採番移動先としてK1150を意図的に空けて選定した（AGENTS.md再採番規則:
   main上の既存番号は不動・衝突した新規項目が空き番号へ再採番する）。
   出版時点で別レーン（general-multiset merge帯還元）が既にK1150を取得したため、
   six-row再採番の移動先は更に次の空き番号（K1152以降）へ繰り下がる。
   なお、単一オーナー宣言ノート（commit `edc231213f`）本文のK1146掃引正本SHA-256
   にknowledge README K1146 bullet由来の1文字転写誤り（`…bf3eefbf…`・正しくは
   `…bf3eebf…`）があった。正しい全桁は
   `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e` であり、
   入力pin（本項 `.input-replace9.json`）が原byteで固定する。
   探索の実行と何の矛盾も生まないため宣言原文を保持し、ここに訂正を記録する。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual72-replace9-whole-record-second-verification-20261120/README.md)・
[監査正本](../../experiments/n11-residual72-replace9-whole-record-second-verification-20261120/output/replace9-whole-record-second-verification-20261120.json)・
[研究ログ](../log/2026-11-20-n11-residual72-replace9-whole-record-second-verification.md)。
