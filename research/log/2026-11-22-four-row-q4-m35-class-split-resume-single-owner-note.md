# 単一オーナー宣言: (4,4) 4×35 class-split 掃引の resume（高速レーン）

- 宣言時刻: 2026-11-22T05:10Z（実測）
- 宣言時 HEAD: d73bb0b8ad8e4a1bd4ea5c1b800df82c59403d39
- オーナー: 本ノートを push した2026-11-22高速レーン実行（Vibe自動実行）。以後この時刻から
  掃引完了または次の明示的な中断まで、d73bb0b8ad8e4a1bd4ea5c1b800df82c59403d39 以降にこの lane への書き込みを行う場合は
  本ノートへの追記（take over）を必須とする。

## 対象

`research/experiments/four-row-q4-m35-class-split-20261115/`（4行q=4・m=35の
absence-capable 82インスタンス class-split 掃引・IN FLIGHT宣言は2026-11-15
`55bc34d4`・driver v2 hardening `1828b78b` で以後7日間停滞・records.jsonl 未着地）。

Rresumeの前例: six-row (6,5) 6x32 t2 resume scan宣言（2026-11-22T02:16Z `b1afb181`）
と同じく、停滞laneを本日付の単一オーナー宣言で引き継ぐ。K1208 の
「another owner's IN FLIGHT work and is untouched」は2026-11-21時点の
敬意ある非接触記録であり、本宣言がそれに取って代わるオーナー宣言である。

## 判定規約（元READMEのまま・不変）

- 全82インスタンス UNSAT ⟹ 4×35 row-deficient 極大安全配置の不在が確定し
  **M_{4,4} = 35 または ≥ 37**（K0821-audit 規約）。
- いずれか SAT ⟹ witness 帯は m=4..35 に拡大し **M_{4,4} ∈ [36,237]**。
  SAT 時は model decode + sat.js verifyConfig + verify_witness.py (Python Fraction)
  の2系統検証を driver が自動実行する。
- INDET（cap到達）は honest negative であり不在主張ではない。
- K1207（w=4 34計数クラス表・m≥35で15/34生存）は本掃引の入力と整合:
  単一クラス {0},{1} の k∈{0,1,2} プロファイルは全て生存
  (B=(0,3,3,3)162 / (1,3,3,3)199 / (2,3,3,3)236) であり、9クラスいずれも
  生存プロファイルを含むためインスタンス単位の刈り込みは行わない。
  multi クラスの krowピン分解（死プロファイル除外）は INDET 追加分割batchで
  行う場合に限り、dead プロファイルの走査を K1207 定理により省略できる。

## 本環境の制約と CAP

- bash call上限 300sのため piece CAP=220 で実行し、外部 `timeout 275` で
  1呼び出しを完結させる（呼び出し内で完了したインスタンスのみ records.jsonl に
  append され、killされた進行中pieceは record 不作成=次回再実行）。
- records.jsonl は増分push・append-only・repo側が正本（kit は退避ミラー）。
- 元 driver `sweep35.sh` は kissat path のみ本環境用に修正（KS行）。
  論理・keys・記録形式は不変。

## 較正（宣言済み・本環境 2026-11-22T05:02Z）

- kissat 4.0.4 static md5 `3a5eba830aa6008a604fcc9bbe99a325`（README pin と一致）。
- 制御CNF (4,34,4) class{1} krow=1:2 minpos=7 を再生成し
  **vars=392,614 / clauses=1,300,317** — 出版対照ログ `r_ctrl_4x34_c1k2p7.txt`
  の DIMACS header "p cnf 392614 1300317" と完全一致（生成器の byte-exact 較正）。
- 陽性対照 (4,34,4) c1k2p7 の kissat 実行は掃引1発目として CAP=220 で実施し、
  出版240s probe（INDET・SIGTERM 239.75s・1,052,475 conflicts）と
  conflicts 乖離が合理的範囲にあることを確認する。

## 中断条件

- SAT 発見（全掃引停止・witness 検証・即時出版）。
- 82インスタンス完了（UNSAT完走→判定出版・K0833更新・CSV反映をこの宣言の下で実施）。
- 環境リセット・push 失敗時は状況を records/README に記録して次回実行へ回す。
