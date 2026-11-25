# セッション log: 3行 q=4 列挙閉包レーン ext28plus（m=28..31 掃引）2026-11-21

- レーン: `research/experiments/three-row-q4-enumeration-20261121/`（拡張）
- 拡張宣言: `research/log/2026-11-21-three-row-q4-enumeration-m28-single-owner-note.md`
  （08:38Z・宣言時 HEAD `f57060f8`・出版 commit `e9c3cd86`・受入条件5項目）
- 前回完了状態: m=24..27 witness-free（part1-10・宣言 7b5bdfec）・M_{3,4} ∈ [24,69]。

## 実行内容（chronological）

1. **器材較正**: knowledge 側退避キット（q34-lane-kit/enumeration-20261121）の
   7 scripts md5 が pin と一致（526cf1c3/b02235a9/0cc6021a/cafc3978/8ae34f3d/
   06bead66/e48f9bf2・`node --check` PASS）。掃引前に pinned wsearch34.js で
   m=23 Y=0 を再実行し witness 2件（a2=2・configs 3136441・safe 2352504）の
   byte 同一出力を再発見して環境較正（陽性対照・`control_m23_Y0.txt`）。
2. **m=28**: family Y=0,1,2 各1実行（139/143/148s・configs 10,732,176/Y）・
   fast 13 プロファイル（全 count 0・322 系最大 8.7s）。
3. **m=29**: family Y=0,1,2 各1実行（200/191/202s・configs 13,351,716/Y）・
   fast 13（全0・最大 11.1s）。
4. **閉包台帳**: `closure_check.py check 28 29 30 31` が 41/41 closed
   （m≥22 単調そのまま）。
5. **m=30**: family は --ia/--ib 2chunk×3Y（各 121-133s・各 (m,Y) 16,483,600 configs）。
   途中、「1 call 内 3 process 背景並走」を試みたが 2 core 環境では出力が
   残らず（リソース競合で打ち切り）、foreground 単独に切り替えてやり直した
   （喪失 chunk 1 件・foreground で補填）。fast 13（全0・最大 ~14s）。
6. **m=31**: family 3chunk×3Y（各 109-113s〔初回 Y0c1 は 216s の乱れあり〕・
   各 (m,Y) 20,205,025 configs）。1 call で 2 chunk 逐次が安定（~245s）。
   途中 09:34Z に Koyeb remote command 失敗で call 経由の chunk 2件が未実行
   （`Failed to execute Koyeb remote command`・環境自体は無事・退避キットも無事）だったが
   個別再実行で補填。fast 13（全0）。
7. **集計・検証**: `output/ext28plus/agg_chunks.py`（同一 dir に出版）が
   chunk 区間の exactly-once 分割〔点検: [0,C(m,3)) の重複なし全被覆〕・
   configs 和 = C(m,3)²・a 計数全0・fast 52/52 zero・閉包 41/41 closed・
   m=23 対照一致を検査し `crossval_summary_ext28_31.json` を出力（全 PASS）。

## 結果

- **P(28), P(29), P(30), P(31) 確定（列挙閉包単独）**。witness-free 幅は
  {24..31}。実行系を通じた 1 事例も witness は出ていない（family 12掃引・
  fast 52行・lemma 41×4）。
- **M_{3,4} ∈ [24,69] は不変**。残る不確定幅は 32..68 の 37 幅。
  P の幅単調性は未証明（m≥32 での witness 復活は現在のところ否定されない）。
- m≥32 は pinned wsearch34.js の `4 <= m <= 31` 上限（31-bit mask）のため
  未掃引。治具拡張（BigInt / 2-word 化）が必要。

## 誠実な負の結果・運用知見

- 背景並走: 2 core 環境の 1 call 内 `(... &)` は出力消失（1回）。call を
  またぐ背景 node は次 call 開始時に殺されるまで CPU を奪い続ける（1回・
  foreground chunk が約 2 倍遅くなる遅延として観測）。heavy は foreground 逐次。
- raw URL /main/ の stale 既知事象は今回は未使用（get_file_contents の
  resource text で byte 照合）。get_file_contents の dir listing は 1000 件
  打ち切りの既知制約どおり items/ では機能しない（commit 逆引きで対応）。
- 09:34Z の Koyeb remote command 失敗（harness 側）で 1 call 分の chunk 出力を
  喪失（環境リセットには至らず・kit 消防）。個別 foreground 再実行で同一
  出力を取得。決定性確認: 補填 chunk の ms は乱れるが計数類（configs/safe/
  deep/a0/a1/a2）は呼び出しごとに同一。

## 次の実行可能課題（着手前に最新 main 再取得・拡張宣言の有効性確認）

1. **m≥32 治具拡張（最有力）**: wsearch34.js の BigInt / 2-word mask 版
   （wsearch35.js 等の別名・pinned 原版は不変更）を作り、
   m=4..8 brute family 計数一致・m=23 witness 再発見・m=24..31 の全0
   再現（既知答との一致）を交差検証した上で m=32..に展開。
   fast/lemma 型 dx34.js 側も同様に m 上限を確認（dx34 の mask 依存は
   別途個別確認が必要）。
2. **理論側**: family 消滅の一般計数（m≥24 で family witness が存在しない
   ことの算術証明）が書ければ 32..68 の掃引を全て置き換えられる
   （K1196 = 4行 q7 の第二certificate 型の計数議論の 3行 q4 版を探索する
   価値あり・fast 型 witness の非存在は m=13..31 の観測で family 系幾何
   とは異なる構造）。
3. frontier レーン（SAT）の m=25 以降との交叉検証は継続有効
   （records.jsonl は frontier レーン正本のため触れない）。

## 解釈規約

- 本拡張の主張は有限完全列挙（chunk 分割の機械検査つき）であり、
  m≥32 への外挿は行わない。conflicts/nodes 系統と同様、本レーンの
  wall time・ms 値は環境依存の参考値。
- 標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  本レーンと無関係・UNKNOWN のまま。REFUTED-D10 は LOSS 証明ではない。

