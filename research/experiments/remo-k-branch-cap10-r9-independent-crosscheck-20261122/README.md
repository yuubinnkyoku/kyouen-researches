# remo-k-branch-cap10-r9-independent-crosscheck-20261122

## 目的と経緯

2026-11-22 の高速レーン実行は「3枝REMO決定性のr=9境界（cap≤10
・15863正準プロファイルの完全スイープ）」を単一オーナー宣言
（`049d7d1c`・宣言時HEAD `3de95445`）の下で開始したが、その後の
調査で **K0893〔2026-11-17出版〕が宣言スコープの全内容
（定理I r=9・FATE44・ECHO9・剰余レンズ・4/10族・FL/G′/D0・
エンジンpack符号欠陥修正・r=9完全スイープのpacked出版）を
すでに出版済み**であることが判明した。宣言は冗長として撤回し
（撤回記録は session log）、本実験はその掃引を実施していた
K0864 verbatim Python エンジンの計算資産（r=9 verdicts・
6457/15863プロファイル分）を **K0893 出版 packed 記録に対する
独立交差検証** に転用したものである。

## 主結果

1. **独立交差検証（部分・6457/15863件）**: K0864 verbatim
   region-game エンジンを別プロセス・別環境で新規実行して得た
   r=9 verdict スナップショット 6457件（output/
   r9_python_partial_verdicts.jsonl・sha256
   `f8fffc4602e3efa62ccf7d726c53a87f6f6bc7614dc90a610db8da9f65640e06`）
   を、K0893 出版 packed 記録
   （`../remo-k-branch-cap10-r9-boundary-20261117/output/
   js_cap10_r9.packed.jsonl`・sha256
   `a2bb16bc8d03f341704d902f0a50ce4352b14ad08043cbced54b8e8f83b9973b`）
   とプロファイル単位（atoms一致）で比較した。
   **survivors / first_losers / determined の3フィールド全件一致
   （不一致 0/0/0）**。うち13件は reachable-state 数も一致
   （C6 witness・live 再実行込み）。
2. **正準列挙順序の相互非互換（運用上の重要事実）**: K0869 の
   r=8 compact（enumerate_profiles系・a0,a1,a2,a3,a4,a5,a6
   ネスト + max-size filter）と K0862系 direct_constrained
   （v0,v1,v3,v2,v4,v5,v6 ネスト・K0875/K0876/K0881/K0893 が
   使用）は **同一の15863プロファイル集合を異なる順序で列挙**
   する。両者は先頭125件（i=0..124）でのみ一致し、i=125 以降は
   ずれる（オフセット変化点1098個・写像は複雑な非一様ずれ）。
   **両系統の i をrawで結合してはならない**（atoms または明示的
   reindex 写像 phi[their_i -> my_i] が必要）。本実験の最初の
   per-index 比較はこの違いを約80%の「不一致」として示し、
   一見すると verdict 不一致に見えたが、atoms 一致の下では
   不一致0である（二重の教訓として記録）。
3. **アンカー類（スナップショット上）**: 補題FL（K0864で全称
   証明済み）の剰余一致 6457/6457・違反0。Δ=0 プロファイル
   （スナップショット内267件）は定理D再帰の r=9 列と全一致
   （不一致0）。C6 の13件は states 数（エンジンの内部状態計数）
   も packed と一致し、Python/JS 両実装の到達状態空間一致の
   直接的な傍証となる。
4. **K0893 pinned 定数の packed bytes からの独立再解析**:
   検証器 C9 は K0893 検証器の R9_SWEEP/R9_PARTITIONS/K0872
   prefilter の定数（34失敗キー・34行の分割表・剰余センサス
   57/336/322・一様決定98/一様非決定583/mixed 34・
   max_states 363,630）を、K0862系列挙の下で出版 packed 記録
   から再導出して全一致を確認した（K0893 の検証器自体は
   live engine 再実行中心であり、この形の bytes→統計再解析は
   本実験が独立系統で行う）。

## 検証器

`verify_crosscheck_r9_partial.py`（自己完結・決定的・stdlibのみ・
外部データは同一commitのスナップショットとK0893実験dir相対参照）。
9機械チェック全合格・二重実行で audit byte 同一
（output/crosscheck_r9_partial_audit.json・sha256
`2a6846b81b17641c7fa75797f71b2c030aca60522f97f21f79aec9332cdfc95c`）。
コールド実行数分以内。live チェックは（a) C6 の13件 witness
（states 含む全フィールド）、(b) C7 のスナップショット先頭12件
（order_determined・o0 含む全コミットフィールド）を verbatim
エンジンで再実行する。

## 実装ノート

- 列挙A（K0869系）は枝刈り版（enumerate_A_pruned）を使用した
  （K0869 検証器の enumerate_profiles(3*cap)+filter と等価・
  同一出力順序）。等価性の根拠: (i) filter の合否は orbit
  representative 不変量（サイズ集合の多重集合が不変 therefore
  max不変）、(ii) 枝刈りは部分サイズが cap を超えたcandidateのみ
  を除去し、その候補の rep は kept プロファイルの rep と一致
  できない、(iii) 巡回順序は不変。オフラインで verbatim 構成と
  15863件の全順序一致を検証済み。
- スナップショットは atoms を格納しない（atoms は i から列挙Aで
  純関数として再導出できるため）。determined / order_determined /
  survivors / first_losers / o0 を格納する。
- スナップショット生成は本セッションの掃引（resume-safe・
  20M node budget・fail-closed・予算スキップ0）から凍結した。
  同ワークスペースには同タスクの並走実行（逐次掃引・sweep.log
  形式）が観測されており、スナップショットの凍結時点の union を
  重複排除（重複レコードは全て byte 同一を確認済み）して採用
  した。凍結後の追加レコードは本実験の対象外。

## 限界（読み過ぎ禁止）

- 交差検証は **部分**（6457/15863・約41%）。K0893 の全体主張の
  再証明ではなく、その packed 記録と K0864 verbatim エンジンの
  別実行が広い範囲で一致することの確認。
- 順位決定性（order_determined・o0）は packed 記録に存在しない
  ため JS 側と交差検証していない（K0893 自身と同じ制限）。
  order フィールドは C7 のみ（Python snapshot vs verbatim 再実行）
  で検証する。
- 列挙順序の非互換は r=2..8 の K0876/K0881 packed と K0869
  compact の間にもそのまま存在する（双方 K0862/K0869 系の
  それぞれの列挙を使用）が、r≤8 での phi の数値表は本実験では
  出版しない（機材を示したので必要時に再導出できる）。
- 本項はいかなる r・cap・盤面の値主張も変更しない。K0893/K0869
  の本文・status は不変。
- 標準11×11空盤・二石root・S2・class 1/2/4 は本実験と無関係で
  UNKNOWNのまま。

## 別刷（erratum）: スナップショット初回pushの打ち切りと修復

- 2026-11-22T12:01Z のアーカイブpush（`3de9e95e`）において、
  `output/r9_python_partial_verdicts.jsonl` が push パイプラインの
  ファイル読み取り上限により **981行（63,983 bytes）で打ち切られた
  状態**で出版されていたことが、fetch-back 検証で判明した
  （完全版は 6457行・422,048 bytes）。
- sha256 ピン `f8fffc46…` は常に完全ローカルファイルに対して
  計算されたものであり、検証器・audit JSON・本 README の記載は
  すべて完全版を参照しているため修正不要。機械検査（C1〜C9）は
  ローカルの完全スナップショットに対して実行済みで影響なし。
- 修復コミット `9759774b`（2026-11-22T12:02Z）で完全版を再pushし、
  fetch-back で byte同一（sha256 `f8fffc46…`・422,048 bytes）を
  確認済み。以後、64KB超の成果物は分割読み取りで完全性を確認して
  from に載せること。
