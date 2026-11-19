# 2026-11-20 n11 残余78行 39 live witness depth-10掃引（K1069）

## 経緯

- 20:29Z実行開始。最新main取得: 並走のwindfall4実験（4 WIN根の証明書抽出・
  三重独立検証）が20:27Zに着地した直後で、item/logはまだ無い状態だったため、
  windfall4出版の補完は並走に委任し、K1063 resolve6が宣言した
  「39 live witnessのdepth-10両順序掃引」（READMEの次の一手2番）を取得。
- 20:32Z: 単一オーナー調整ノート
  （2026-11-20-n11-residual78-39livewitness-sweep-concurrency-note.md）
  をpush（k38レーン方式の踏襲）。以降の並走push（windfall4証明書4本・K1066
  item/log/README・第13〜第16receipt fold〔残余78→74行〕）と本レーンの
  掃引は完全に分離して進行した。並走はfoldに専念し掃引には着手しなかった
  （調整ノート方式の有效性 第2例目）。
- 入力pin: resolve6正本（SHA-256 e85d4bfb…c281a）・runner v17（commit-SHAピン
  raw取得・当環境でgit blob SHA-1再計算が出版値 c132cc6425eee3feaeef1d697dd74f968cfedb59 と一致）。
  roots.jsonはresolve6 witness_full（39根・全7石・全safe・covered rows和集合==78行）
  から機械生成しassemble gateまで込みで検証。

## 実行

- driver.py: K1059 driverの4-worker改造（cap 30M均一・probe 280s timeout・
  records append resume・両AND順序・pilot_d6制御・生child hex）。
- セッション1（20:32:23Z launch・285s）: 54 probe完了。
- セッション2（20:37:25Z再launch・235s）: ここで運用事故。アップグレード実行環境の
  background workerはbash呼び出しをまたいで生存し続けており、セッション1の
  worker4本がまだ走っていたため、セッション2のworkerが未記録のprobeを
  再実行した。最終的に98記録（78 unique + 20重複・15 probe分）となったが、
  重複は全て nodes・loss・capped 完全一致（duplicate-agreement gate 0不一致）。
  決定論的node-exact再現の無料証拠15件になったが、本来は再launch前に
  worker生存（記録数・プロセス）を確認すべき（README運用記録に明記）。
- 20:41Z: 78/78 unique完走。assemble.py 全9 gate PASS。

## 結果

- **WIN 1 / REFUTED-D10 38 / CAPPED 0 / 順序矛盾 0**（総nodes 169,615,508・
  最大probe 14,249,420〔root 00000000010000809002000040000080〕）。
- **WIN7-D10: `00004000000000821082000000000100`**（bit 8・child
  00004000000000821082000000000000・両順序loss=true・uncapped・
  terminal [13,17]・nodes 1,576,372 / 2,544,178）。
  被覆行: `00000000000000821082000000000001`・`00000000000000821082000000000004`。
  windfall4 fold（第13〜第16・残余78→74）の4行とは交差しないため、
  第17証明書として抽出・三重検証・foldされれば残余は74→72行。
- 38 REFUTED rootはdepth-10閉鎖witnessとして使用不能（depth-saturation
  による永久使用不能判定は別audit待ち。K1059の39 dead root除外と同型）。

## 解釈規約（不変）

- 本掃引はそれ自体ではどの行も閉じない。被覆簿記の進行は証明書foldのみ。
- REFUTED-D10はLOSS証明でない。pn/dn・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## 次の一手

1. WIN根の証明書抽出（repo-verbatim extractor exact ms23・blind）と三重独立
   検証（K1066規約・BigInt 3x3 / Bareiss 4x4 / extractor再実行byte一致）。
2. 第17receipt fold（fold機械の入力chain再構築・残余74行のうち2行の閉鎖計上）。
3. 38 REFUTED根のdepth-saturation audit（d12/14/16）とresolve7再照合
   （fresh-safe・pair辺・matching・strandedの再計算）は次回以降の候補。

## 並走の採番観察（次回レーンへの引継ぎ・本レーンは不介入）

- 20:34:17Zに高速レーンがK1067（z=17,y=3切片）を着地済みの状態で、windfall4
  fold系の並走2実行が20:43〜20:45Zに fold を二重出版した:
  (a) 実験dir n11-residual78-windfall4-receipt-fold-20261120 + item
  K1067-n11-windfall4-receipt-fold.md（b90f3cdd4d・20:45:16Z）と
  (b) 実験dir n11-residual78-windfall4-receipt-fold-thirteenth-sixteenth-20261120
  + item K1068-n11-windfall4-thirteenth-sixteenth-receipt-fold.md
  （f46a03d106・20:45:22Z）。両記録のfold数値は完全一致（frontier
  6,213/492,021→6,209/491,722・5親target 34→38/112・残余78→74）で、
  同一foldの独立二重計算として相互クロスチェックの価値はある。
- ただし (a) のitem id K1067 は高速レーンの z=17,y=3 切片と衝突しており
  **mainにK1067重複ID状態が発生**（check.pyの既知重複ID課題〔K0936/K0974/
  K0975〕に新たな1組）。AGENTS.md規則（main既存番号は不変・衝突側が再採番）
  では衝突側=windfall4 foldの再採番が正解で、実質的に (b) K1068 がそれに
  該当するため、(a) のK1067 item（内容はK1068と同一命題）が孤立重複になって
  いる。折を見て (a) item（と安全ならそのlog）の削除・またはK番号不変の
  範囲での重複解消が望ましい（所有レーンが継続中の可能性があるため
  本レーンは手を出さず記録のみ。K1037-era の誤採番item削除の前例手法
  github_app.delete_file が使える）。
- 本レーンの掃引itemは**K1069**を採番（push直前にitem slug 404・実験dir 404・
  log 404を確認済み・K1067/K1068/K1069の3点セットで空きを機械確認）。

## 追記: README弾丸のping-pong観察（20:46Z）

- f46a03d106（K1068 fold側）がK1068弾丸をREADMEに追加した直後、
  8fe0d9d7c1（K1067 fold側）が**K1068弾丸を削除して**K1067弾丸に差し替えた
  （base取得が相互に相手のpushを抜いた古い版）。K1037-era のREADME
  lost-update戦争と同一パターン。「README編集pushの安全条件は最新mainに対する
  diffの純追加」が両レーンに守られていない状態。和集合復元（両弾丸の共存）は
  数値一致している同一foldの二重出版なので実質損失はない。本レーンは自分の
  弾丸appendのみを行い、fold系の弾丸間衝突には介入しない。
