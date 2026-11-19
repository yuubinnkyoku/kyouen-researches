# n11-residual78-39livewitness-depth10-sweep-20261120

K1063（resolve6）が「次の一手」として宣言した39 live witness（post-saturation
full-cache join・最大matching 39・stranded 0・covered rowsの和集合==残余78行）
のdepth-10全面掃引の実行部。単一オーナーは当レーン
（調整ノート: research/log/2026-11-20-n11-residual78-39livewitness-sweep-concurrency-note.md）。
branch/PRは作らずmainに直接出版。

## 前提（全てrepo既出版のpin）

- resolve6正本: research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json
  SHA-256 e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a
  （witness_full 39 root: 全7石・D4正準形・全safe・covered rows==残余78行。本実験の
  roots.jsonはresolve6 witness_fullから機械生成・popcount==7・child|1<<bit==root gate込み）
- runner v17: git blob c132cc6425eee3feaeef1d697dd74f968cfedb59
  （raw.githubusercontent.com commit-SHA pin取得・当環境でblob SHA-1再計算一致を確認済み）
- depth 10・cap 30M（均一）・両AND順序（andclose 1/0）・pilot_d6制御行
  （loss=false・3,402 nodes要求・runner内fail-closed）・生整数hex child
  （child = root − 最小セットビット・canon_hex被せ禁止・K1046事故規約継承）。
  分解非依存性は39witness版READMEの検証実績（sweep43[0]代替分解でnodes完全一致）どおり。

## 実行方法

- python3 driver.py <worker_id> （4 worker分割 roots[W::4]・probe単位280s timeout・
  records append resume式・中断/再開安全）
- 分類組立: assemble.py（生記録から独立組立・9 gate fail-closed:
  no-error / partition-78 / duplicate-agreement / both-orders / uncapped /
  pilot-d6 / order-consistency / covered-rows-equal-residual78 / anatomy）
- 決定論: 同一(root, ordering)の重複ok記録15件はnodes・loss・capped全て完全一致
  （後述のスライス再開に伴う同一probeの別プロセス再実行で、run-to-runの
  node-exact再現が追加コストゼロで15件観測された）。

## 結果（2026-11-19 20:32Z〜20:41Z UTC・約9分・4 worker・78 probe完走）

- pilot_d6: 全probe合格（3,402 nodes・loss=false）。CAPPED 0・error 0・順序矛盾 0。
- **WIN 1 / REFUTED-D10 38 / CAPPED 0**（39 root全判定。総nodes 169,615,508・
  最大単一probe 14,249,420〔root 00000000010000809002000040000080・loss=false〕）。
- **WIN7-D10 root: `00004000000000821082000000000100`**（bit 8・child
  `00004000000000821082000000000000`・両順序一致でloss=true・uncapped・
  terminal石数 [13,17]・nodes 1,576,372〔andclose1〕/ 2,544,178〔andclose0〕）。
  被覆行: `00000000000000821082000000000001`・`00000000000000821082000000000004`
  （windfall4 fold〔第13〜第16receipt fold・残余78→74〕で閉じた4行とは無関係の
  別行なので、証明書抽出・独立検証・foldを経れば残余は74→72行）。
- 帰結: 選択39-live-witness計画のうち38 rootはdepth-10閉鎖witnessとして使用不能。
  残余78行（fold後74行）の被覆簿記はwindfall4+本WIN根の証明書fold待ちであり、
  本掃引はそれ自体ではどの行も閉じない。REFUTED-D10はLOSS証明ではない。

## 解釈規約（他のn11項目と同一）

- 本掃引は行の被覆簿記と候補供給の観察。勝敗には一切言及しない。
- WIN rootは証明書抽出候補（抽出・BigInt 3x3 / Bareiss 4x4独立二重検証・
  receipt foldまでは閉鎖計上しない）。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## 運用記録（他レーン参考）

- アップグレード実行環境ではbash呼び出しをまたいでbackground workerが
  生存し続けることがある。スライス再開時にworker生存確認をしないと
  同一probeを別プロセスで重複実行する（今回は15 probe分で、結果は
  node-exact一致したため決定論の追加証拠になったが、本来は
  記録数で生存確認してから再launchするのが正しい）。

## 次の一手

1. WIN root `00004000000000821082000000000100` の証明書抽出（repo-verbatim
   extractor exact ms23・blind・kill table空）と三重独立検証
   （K1066 windfall4と同一規約）→ 第17証明書候補。
2. 証明書を入力とするreceipt fold（残り74行のうち2行の閉鎖計上）。
3. 38 REFUTED rootのdepth-saturation audit（12/14・必要なら16。K1059の
   dead root除外と同型の永久使用不能判定）と、それを含むresolve7再照合
   （fresh-safe候補の再計算・新matching・stranded算出）は別レーン/別実行。
